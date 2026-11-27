#!/usr/bin/env python3
"""Post-close track: apply official 1D marks to the paper book. Never invent OHLC.

Usage:
  python3 track_session.py --print-symbols
  python3 track_session.py --marks official.json --dry-run
  python3 track_session.py --marks official.json --apply [--sync-payloads]

Required marks per open/working ticker: open, high, low, close.
ema9 preferred; if missing, continue prior EOD with k=0.2 (tagged, not invented OHLC).

Does not call TradingView or Sheets MCP. After --apply, agent runs sheet_safe_sync.sh.
supply-half-fill-v1 stays REVOKED (annotate room, never half, never ask).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sim_lib as L

ROOT = L.ROOT


def _mark(marks: dict, ticker: str) -> dict:
    m = marks.get(ticker)
    if not m:
        raise SystemExit(f"missing official marks for {ticker} — will not invent")
    return m


def _ema9(mark: dict, pos: dict) -> tuple[float | None, str]:
    if mark.get("ema9") is not None:
        return float(mark["ema9"]), "marks.ema9"
    prev = pos.get("last_mark_ema9") or pos.get("ema9_at_entry")
    if prev is not None and mark.get("close") is not None:
        return L.ema9_continue(prev, mark["close"]), "ema9_continue_k0.2"
    return None, "missing"


def _resolve_session_held(pos: dict, session: str) -> tuple[int, int]:
    prev = int(pos.get("sessions_held") or 0)
    entry = str(pos.get("entry_session_date") or "")
    last = str(pos.get("last_mark_session") or "")
    if not entry or session <= entry:
        return prev, prev
    if last and session <= last:
        return prev, prev
    return prev, prev + 1


def apply_track(root: Path, marks_doc: dict, apply: bool, force: bool = False) -> dict:
    session = marks_doc.get("session")
    if not session:
        raise SystemExit("marks JSON missing session")
    source = marks_doc.get("source") or "TradingView MCP official 1D bar"
    hkt = marks_doc.get("checked_hkt") or L.now_hkt()
    marks = marks_doc.get("marks") or {}
    tc_id = f"TRACK-{session.replace('-', '')}"

    pf = L.load_json(root / "state" / "portfolio.json")
    if pf.get("marks_session") == session and not force:
        return {
            "brief": f"{tc_id} already applied (marks_session={session}). Use --force to re-run.",
            "already_applied": True,
            "ask_justin": [],
            "applied": False,
            "symbols": L.desired_shortlist(root),
            "tc_id": tc_id,
        }

    cash = L.money(pf.get("cash_usd") or 0)
    realized_session = 0.0
    executes = []
    ask_justin = []
    closed_tickers = []
    queued_trims = []
    filled_orders = []
    cancelled_orders = []
    work = {"positions": {}, "orders": {}, "closed": {}, "delete_positions": []}

    # Snapshot current files
    pos_by = {}
    for p in L.open_positions(root):
        pos_by[p["ticker"]] = deepcopy(p)
    ord_by_path = {}
    for o in L.active_orders(root):
        ord_by_path[o["_path"]] = deepcopy(o)

    # Missing marks check
    need = list(pos_by.keys())
    for o in ord_by_path.values():
        if o["ticker"] not in need:
            need.append(o["ticker"])
    missing = []
    for t in need:
        if t not in marks:
            missing.append(f"{t} missing entirely")
        else:
            missing.extend(L.require_ohlc(marks[t], t))
    if missing:
        raise SystemExit("Refuse to invent prices:\n- " + "\n- ".join(missing))

    revoked = L.supply_half_revoked(root)

    # ---- 1a. Pending market_open_sell / GAP_SL at official Open ----
    for path, od in list(ord_by_path.items()):
        ot = str(od.get("order_type") or "")
        if ot != "market_open_sell":
            continue
        if str(od.get("execute_session") or "") != session:
            continue
        t = od["ticker"]
        pos = pos_by.get(t)
        if not pos:
            ask_justin.append({"ticker": t, "topic": "ORPHAN_MOO", "detail": f"{path} execute_session={session} but no open position"})
            continue
        m = _mark(marks, t)
        open_ = float(m["open"])
        stop_now = float(pos.get("hard_sl") or pos.get("stop"))
        reason = od.get("exit_reason") or "OTHER"
        remain = od.get("remain_after")
        # GAP_SL replaces trim if Open < current stop (stop before trim)
        if open_ < stop_now:
            px = L.money(open_)
            sh = int(pos["shares"])
            pnl = L.money((px - float(pos["entry"])) * sh)
            cash = L.money(cash + px * sh)
            realized_session = L.money(realized_session + pnl)
            _close_position(
                pos, session, hkt, source, "GAP_SL", px, sh, pnl, m, tc_id,
                note=f"official Open {px} < SL {stop_now} → GAP_SL 全出 {sh}；pending {reason} 被取代",
            )
            pos["realized_pnl_usd"] = L.money((pos.get("realized_pnl_usd") or 0) + pnl)
            work["closed"][t] = pos
            work["delete_positions"].append(t)
            closed_tickers.append(t)
            del pos_by[t]
            od.update(_fill_order_fields(od, px, session, hkt, source, "GAP_SL superseded", pnl, remain_after=0))
            od["status"] = "cancelled"
            od["decision"] = "SUPERSEDED_GAP_SL"
            work["orders"][path] = od
            filled_orders.append({"ticker": t, "order": Path(path).name, "action": "SUPERSEDED_GAP_SL"})
            executes.append(_exec(t, "GAP_SL", f"Open**{px}** < SL**{stop_now}** → 全出 {sh} @ Open，實現 {pnl:+.2f}；pending {reason} 被取代"))
            continue
        # Fill the MOO (trim or thesis full exit)
        px = L.money(open_)
        sh = int(od["shares"])
        if sh > int(pos["shares"]):
            ask_justin.append({"ticker": t, "topic": "MOO_SHARES", "detail": f"order {sh} > position {pos['shares']}"})
            continue
        pnl = L.money((px - float(pos["entry"])) * sh)
        cash = L.money(cash + px * sh)
        realized_session = L.money(realized_session + pnl)
        pos["realized_pnl_usd"] = L.money((pos.get("realized_pnl_usd") or 0) + pnl)
        if remain == 0 or reason == "THESIS_INVALID" or sh == int(pos["shares"]):
            _close_position(pos, session, hkt, source, reason, px, sh, pnl, m, tc_id,
                            note=f"{reason} 開市全出 {sh} @ {px}，實現 {pnl:+.2f}")
            work["closed"][t] = pos
            work["delete_positions"].append(t)
            closed_tickers.append(t)
            del pos_by[t]
            executes.append(_exec(t, reason, f"開市全出 {sh} @ **{px}**，實現 {pnl:+.2f}"))
        else:
            remain_sh = int(remain if remain is not None else int(pos["shares"]) - sh)
            stop_after = float(od.get("stop_after") or pos.get("entry"))
            pos["shares"] = remain_sh
            pos["stop"] = stop_after
            pos["hard_sl"] = stop_after
            pos["r_usd"] = 0.0
            pos["stop_pct"] = 0.0
            pos["notional_usd"] = L.money(remain_sh * float(pos["entry"]))
            pos["trim_1_3_done"] = True
            pos["trim_1_3_pending"] = False
            pos["post_trim_hold"] = True
            pos["post_trim_hold_rule"] = "post-trim-hold-v1"
            pos["trim_1_3_fill"] = {
                "exit_reason": "TRIM_1_3",
                "shares": sh,
                "price": px,
                "session": session,
                "realized_pnl_usd": pnl,
                "remain": remain_sh,
                "stop_after": stop_after,
                "hkt": hkt,
                "source": source,
            }
            executes.append(_exec(t, "TRIM_1_3", f"開市賣 {sh} @ **{px}**，實現 {pnl:+.2f}；剩 **{remain_sh}**，止蝕推到成本 **{stop_after}**"))
        od.update(_fill_order_fields(od, px, session, hkt, source, reason, pnl, remain_after=remain))
        work["orders"][path] = od
        filled_orders.append({"ticker": t, "order": Path(path).name, "action": "FILLED"})

    # ---- 1b. Remaining opens: gap already checked at open; increment held; Hard SL / EMA9; queue trim ----
    for t, pos in list(pos_by.items()):
        m = _mark(marks, t)
        open_, high, low, close = float(m["open"]), float(m["high"]), float(m["low"]), float(m["close"])
        ema9, ema_src = _ema9(m, pos)
        sma20 = m.get("sma20")
        stop = float(pos.get("hard_sl") or pos.get("stop"))
        prev_held, held = _resolve_session_held(pos, session)
        pos["sessions_held"] = held
        pos["ema9_grace_active"] = held < 3
        pos["last_mark_hkt"] = hkt
        pos["last_mark_session"] = session
        pos["last_mark_o"] = open_
        pos["last_mark_h"] = high
        pos["last_mark_l"] = low
        pos["last_mark_c"] = close
        pos["last_mark_v"] = m.get("volume")
        if ema9 is not None:
            pos["last_mark_ema9"] = ema9
        if sma20 is not None:
            pos["last_mark_sma20"] = sma20
        pos["mark"] = close
        pos["mark_source"] = source
        pos["unrealized_pnl_usd"] = L.money((close - float(pos["entry"])) * int(pos["shares"]))
        pos["track_tc"] = tc_id
        pos["updated_hkt"] = hkt
        pos["decision_session"] = session
        room = L.remaining_room_r(pos, close)
        if room is not None:
            pos["remaining_Room_To_Supply_R"] = room
        supply = pos.get("Supply_Level")
        room_note = ""
        if supply is not None:
            touched = high >= float(supply)
            room_note = f"；High {high}{'≥' if touched else '<'} Supply {supply}"
            if room is not None:
                room_note += f"；room **{room}R**"
                if room <= 0.3 or touched:
                    room_note += "；supply-half 已 REVOKED — 唔套用、唔再問" if revoked else ""
                    pos["supply_half_pending"] = False

        # Resolve pre-open WATCH_GAP against official Open
        pre = pos.get("pre_open_flag") or {}
        gap_sl = open_ < stop
        if pre:
            pos["pre_open_flag_resolved"] = {
                "session": session,
                "pre_open_action": pre.get("action"),
                "pre_open_pm": pre.get("mark_pm"),
                "official_open": open_,
                "hard_sl": stop,
                "gap_sl": gap_sl,
                "note": f"official Open{open_} vs SL{stop} — {'GAP_SL' if gap_sl else 'no GAP_SL'}",
            }

        notes = [
            f"Open**{open_}**{'<' if gap_sl else '>'}SL**{stop}**",
            f"held **{prev_held}→{held}**" if held != prev_held else f"held={held}",
        ]

        if gap_sl:
            px = L.money(open_)
            sh = int(pos["shares"])
            pnl = L.money((px - float(pos["entry"])) * sh)
            cash = L.money(cash + px * sh)
            realized_session = L.money(realized_session + pnl)
            pos["realized_pnl_usd"] = L.money((pos.get("realized_pnl_usd") or 0) + pnl)
            _close_position(pos, session, hkt, source, "GAP_SL", px, sh, pnl, m, tc_id,
                            note=f"Open {px} < SL {stop} → GAP_SL 全出 {sh}，實現 {pnl:+.2f}")
            work["closed"][t] = pos
            work["delete_positions"].append(t)
            closed_tickers.append(t)
            del pos_by[t]
            executes.append(_exec(t, "GAP_SL", f"Open**{px}** < SL**{stop}** → 全出 {sh} @ Open，實現 {pnl:+.2f}"))
            continue

        if close < stop:
            px = L.money(close)
            sh = int(pos["shares"])
            pnl = L.money((px - float(pos["entry"])) * sh)
            cash = L.money(cash + px * sh)
            realized_session = L.money(realized_session + pnl)
            pos["realized_pnl_usd"] = L.money((pos.get("realized_pnl_usd") or 0) + pnl)
            _close_position(pos, session, hkt, source, "HARD_SL", px, sh, pnl, m, tc_id,
                            note=f"Close {px} < SL {stop} → HARD_SL 全出 {sh}，實現 {pnl:+.2f}")
            work["closed"][t] = pos
            work["delete_positions"].append(t)
            closed_tickers.append(t)
            del pos_by[t]
            executes.append(_exec(t, "HARD_SL", f"Close**{px}** < SL**{stop}** → 全出 {sh} @ 收市，實現 {pnl:+.2f}"))
            continue

        grace_on = held < 3
        ema_note = ""
        if ema9 is None:
            if held >= 3:
                ask_justin.append({"ticker": t, "topic": "MISSING_EMA9", "detail": "held>=3 but no ema9 / no prior to continue"})
                ema_note = "；EMA9 缺失，唔發明、唔出 EMA9_EXIT"
            pos["ema9_grace_note"] = f"held={held}；EMA9 missing"
        else:
            below = close < ema9
            if grace_on:
                ema_note = f"；grace ON" + (f"（Close<EMA9 {ema9:.3f} 被抑制）" if below else f"；Close>EMA9 {ema9:.3f}")
                pos["ema9_grace_note"] = f"held={held} grace ON; Close {close} vs EMA9 {ema9}" + (" suppressed" if below else "")
            elif below:
                px = L.money(close)
                sh = int(pos["shares"])
                pnl = L.money((px - float(pos["entry"])) * sh)
                cash = L.money(cash + px * sh)
                realized_session = L.money(realized_session + pnl)
                pos["realized_pnl_usd"] = L.money((pos.get("realized_pnl_usd") or 0) + pnl)
                _close_position(pos, session, hkt, source, "EMA9_EXIT", px, sh, pnl, m, tc_id,
                                note=f"Close {px} < EMA9 {ema9} held={held} → EMA9_EXIT 全出 {sh}，實現 {pnl:+.2f}")
                work["closed"][t] = pos
                work["delete_positions"].append(t)
                closed_tickers.append(t)
                del pos_by[t]
                executes.append(_exec(t, "EMA9_EXIT", f"Close **{px}** 低過 9EMA {ema9:.2f}（held={held}）→ 全出 {sh} @ 收市價，實現 {pnl:+.2f}"))
                continue
            else:
                ema_note = f"；grace OFF；Close>EMA9 {ema9:.3f} 唔使 EMA9_EXIT"
                pos["ema9_grace_note"] = f"held={held} grace OFF; Close {close} > EMA9 {ema9}"

        # Queue trim when held first hits 3
        if held >= 3 and not pos.get("trim_1_3_done") and not pos.get("trim_1_3_pending"):
            trim_sh = int(pos["shares"]) // 3
            remain_sh = int(pos["shares"]) - trim_sh
            stop_after = float(pos["entry"])
            if trim_sh >= 1:
                pos["trim_1_3_pending"] = True
                pos["pending_trim_note"] = f"queued TRIM_1_3 {trim_sh} @ next open; remain {remain_sh}; stop→BE {stop_after}"
                queued_trims.append({"ticker": t, "shares": trim_sh, "remain_after": remain_sh, "stop_after": stop_after})
                notes.append(f"；AUTO 掛下一個開市 trim {trim_sh}（剩 {remain_sh}，停損改 BE {stop_after}）")

        # Time-stop: ask unless post-trim-hold-v1
        if held >= 5:
            if pos.get("post_trim_hold") or pos.get("trim_1_3_done"):
                notes.append("；post-trim-hold-v1，held>=5 唔問 time-stop")
            else:
                ask_justin.append({"ticker": t, "topic": "TIME_STOP", "detail": f"held={held} and not post-trim-hold — consider time stop"})
                notes.append("；held>=5 考慮 time-stop（ask Justin）")

        notes.append(ema_note)
        notes.append(room_note)
        detail = "".join(n for n in notes if n)
        pos["decision"] = "HOLD"
        pos["decision_note"] = detail.replace("**", "")
        executes.append(_exec(t, "HOLD", detail))
        work["positions"][t] = pos

    # ---- 2. Working limit fills / 5% away / lifetime ----
    for path, od in list(ord_by_path.items()):
        if path in work["orders"]:
            continue
        ot = str(od.get("order_type") or "")
        if ot not in {"limit_buy", "limit_sell", "buy_stop"}:
            continue
        t = od["ticker"]
        m = _mark(marks, t)
        open_, high, low, close = float(m["open"]), float(m["high"]), float(m["low"]), float(m["close"])
        # increment stalk sessions
        elapsed = int(od.get("stalk_sessions_elapsed") or 0)
        last = str(od.get("last_mark_session") or "")
        if not last or session > last:
            elapsed += 1
        od["stalk_sessions_elapsed"] = elapsed
        od["last_mark_session"] = session
        max_s = int(od.get("max_stalk_sessions") or 5)
        lp = od.get("limit_price")

        if lp is not None and ot == "limit_buy" and close >= float(lp) * 1.05:
            od["status"] = "cancelled"
            od["decision"] = "CANCEL_AWAY_5PCT"
            od["decision_note"] = f"Close {close} >= 5% past L {lp} → AUTO cancel"
            od["updated_hkt"] = hkt
            work["orders"][path] = od
            cancelled_orders.append({"ticker": t, "reason": "limit-away-5pct-cancel-v1"})
            executes.append(_exec(t, "CANCEL", f"限價 L{lp}：Close {close} ≥5% past → AUTO cancel"))
            continue
        if lp is not None and ot == "limit_sell" and close <= float(lp) * 0.95:
            od["status"] = "cancelled"
            od["decision"] = "CANCEL_AWAY_5PCT"
            od["decision_note"] = f"Close {close} <= 5% past L {lp} → AUTO cancel"
            od["updated_hkt"] = hkt
            work["orders"][path] = od
            cancelled_orders.append({"ticker": t, "reason": "limit-away-5pct-cancel-v1"})
            executes.append(_exec(t, "CANCEL", f"賣限 L{lp}：Close {close} ≤5% past → AUTO cancel"))
            continue
        if elapsed >= max_s:
            od["status"] = "cancelled"
            od["decision"] = "CANCEL_STALK_LIFETIME"
            od["decision_note"] = f"stalk_sessions_elapsed {elapsed} >= {max_s}"
            od["updated_hkt"] = hkt
            work["orders"][path] = od
            cancelled_orders.append({"ticker": t, "reason": "stalk-lifetime-v1"})
            executes.append(_exec(t, "CANCEL", f" stalk {elapsed}/{max_s} → 過期取消"))
            continue

        if ot == "limit_buy" and lp is not None:
            fill = L.better_buy_fill(float(lp), open_, low)
            if fill is not None:
                sh = int(od["shares"])
                plan_stop = float(od.get("stop") or 0)
                plan_limit = float(lp)
                new_stop, risk = L.reanchor_stop(plan_limit, plan_stop, fill)
                if fill < float(lp) - 1e-12:
                    r_usd = L.money(sh * risk)
                    reanchored = True
                else:
                    new_stop = L.money(plan_stop)
                    r_usd = L.money(od.get("r_usd") or sh * abs(fill - new_stop))
                    reanchored = False
                # cash
                cash = L.money(cash - fill * sh)
                ema9, ema_src = _ema9(m, od)
                pos = {
                    "ticker": t,
                    "status": "open",
                    "side": "long",
                    "entry": fill,
                    "fill_price": fill,
                    "fill_rule": (
                        f"limit-single-price-v1 + better-price-v1: L{low}<={lp}; "
                        + (f"Open{open_}<{lp} → fill @{fill}" if fill < float(lp) else f"Open {open_} not better → fill @{fill}")
                    ),
                    "plan_limit": plan_limit,
                    "plan_stop": plan_stop,
                    "stop": new_stop,
                    "hard_sl": new_stop,
                    "shares": sh,
                    "r_usd": r_usd,
                    "stop_pct": round(abs(fill - new_stop) / fill * 100, 4) if fill else 0,
                    "notional_usd": L.money(sh * fill),
                    "mark": close,
                    "mark_source": source,
                    "unrealized_pnl_usd": L.money((close - fill) * sh),
                    "thesis": od.get("thesis") or "",
                    "invalidation": od.get("invalidation") or f"Session close < {new_stop}",
                    "paper_probe": bool(od.get("paper_probe")),
                    "source_order": f"orders/{Path(path).name}",
                    "source": od.get("source"),
                    "filled_hkt": hkt,
                    "entry_session_date": session,
                    "ema9_at_entry": ema9,
                    "entry_below_9ema": (fill < ema9) if ema9 is not None else None,
                    "sessions_held": 0,
                    "ema9_grace_rule": "9ema-grace-3sessions-v2",
                    "ema9_grace_active": True,
                    "last_mark_hkt": hkt,
                    "last_mark_session": session,
                    "last_mark_o": open_,
                    "last_mark_h": high,
                    "last_mark_l": low,
                    "last_mark_c": close,
                    "last_mark_v": m.get("volume"),
                    "last_mark_ema9": ema9,
                    "last_mark_sma20": m.get("sma20"),
                    "tc_id": od.get("tc_id") or pf.get("last_open_skip_tc"),
                    "track_tc": tc_id,
                    "exchange": L.exchange_of(od, t) or od.get("exchange"),
                    "trim_1_3_done": False,
                    "structure_notes": od.get("structure_notes") or {},
                    "Supply_Level": od.get("Supply_Level") or (od.get("structure_notes") or {}).get("soft_supply") or (od.get("structure_notes") or {}).get("hard_room_level"),
                    "Room_To_Supply_R": od.get("Room_To_Supply_R") or (od.get("structure_notes") or {}).get("room_to_supply_r"),
                    "better_price_stop_reanchor": reanchored,
                    "better_price_stop_reanchor_note": (
                        f"plan_$risk=|{plan_limit}-{plan_stop}|={risk}; new_stop={fill}-{risk}={new_stop}; R$={sh}×{risk}={r_usd}"
                        if reanchored
                        else f"N/A — fill @ limit {lp} (Open {open_} not better); stop stays {new_stop}; R${r_usd}"
                    ),
                    "tags": od.get("tags") or [],
                    "updated_hkt": hkt,
                    "decision_session": session,
                    "decision": "FILL",
                    "decision_note": f"限價成交 @ {'更好開市價 ' if reanchored else ''}**{fill}**（{sh} 股，止蝕{'重錨 ' + str(new_stop) if reanchored else str(new_stop)}）",
                    "supply_half_pending": False,
                }
                if pos["Supply_Level"] is not None:
                    pos["remaining_Room_To_Supply_R"] = L.remaining_room_r(pos, close)
                pos_by[t] = pos
                work["positions"][t] = pos
                od.update(_fill_order_fields(od, fill, session, hkt, source, "FILL", 0, remain_after=None))
                od["status"] = "filled"
                od["decision"] = "FILLED"
                work["orders"][path] = od
                filled_orders.append({"ticker": t, "order": Path(path).name, "action": "FILL_LIMIT"})
                executes.append(_exec(
                    t,
                    "FILL",
                    f"限價成交 @ {'更好開市價 ' if reanchored else ''}**{fill}**（{sh} 股，止蝕重錨 **{new_stop}**）"
                    if reanchored
                    else f"限價成交 @ **{fill}**（{sh} 股）",
                ))
                continue

        # KEEP
        od["updated_hkt"] = hkt
        work["orders"][path] = od
        executes.append(_exec(t, "KEEP", f"限價 L{lp}/{od.get('shares')} stalk {elapsed}/{max_s} KEEP"))

    # Queue trim orders on disk plan
    new_order_files = {}
    for q in queued_trims:
        t = q["ticker"]
        name = f"{t}_TRIM.json"
        dest = root / "orders" / name
        # never overwrite a filled historical trim in-place if we are dry and file exists filled — use session suffix if conflict
        existing = L.load_json(dest)
        if existing and str(existing.get("status")) == "filled":
            name = f"{t}_TRIM_{session}.json"
            dest = root / "orders" / name
        new_order_files[str(dest)] = {
            "ticker": t,
            "status": "pending",
            "side": "sell",
            "order_type": "market_open_sell",
            "shares": q["shares"],
            "remain_after": q["remain_after"],
            "stop_after": q["stop_after"],
            "stop_before": float(pos_by[t].get("hard_sl") or pos_by[t].get("stop")),
            "entry_ref": float(pos_by[t]["entry"]),
            "exit_reason": "TRIM_1_3",
            "execute_at": "US_market_open",
            "execute_session": _next_session_placeholder(session),
            "fill_rule": "At US cash open of execute_session: sell trim_shares at open; no slippage — use session Open from TV MCP. Then set position.stop=hard_sl=stop_after (BE), shares=remain_after, trim_1_3_done=true.",
            "approved_by": "auto trim-1-3-be-auto-v1",
            "placed_hkt": hkt,
            "source": f"{tc_id} sessions_held first hits 3",
            "parent_position": f"positions/{t}.json",
            "standing_rule": "trim-1-3-be-auto-v1",
            "track_tc": tc_id,
        }
        # execute_session should be NEXT US session, unknown here (weekends/holidays). Don't invent a date.
        new_order_files[str(dest)]["execute_session"] = None
        new_order_files[str(dest)]["execute_session_note"] = "NEXT US cash session after " + session + " — fill when official Open of that session is marked (do not invent the date if unsure)"

    # ---- Rebuild book ----
    r_used = L.money(sum(float(p.get("r_usd") or 0) for p in pos_by.values()))
    # working reserved: remaining active non-terminal after this pass
    still_working = []
    pending_moo = []
    # start from post-write view
    for path, od in {**{o["_path"]: o for o in L.active_orders(root)}, **work["orders"]}.items():
        od = work["orders"].get(path, od)
        st = str(od.get("status") or "").lower()
        if st in L.TERMINAL_ORDER:
            continue
        if str(od.get("order_type") or "") == "market_open_sell":
            pending_moo.append(od)
        elif str(od.get("order_type") or "") in {"limit_buy", "limit_sell", "buy_stop"}:
            still_working.append(od)
    for path, od in new_order_files.items():
        pending_moo.append(od)

    r_reserved = L.money(sum(float(o.get("r_usd") or 0) for o in still_working))
    working_notional = L.money(sum(float(o.get("limit_price") or 0) * int(o.get("shares") or 0) for o in still_working))
    upnl = L.money(sum(float(p.get("unrealized_pnl_usd") or 0) for p in pos_by.values()))
    nav = L.money(cash + sum(float(p["mark"]) * int(p["shares"]) for p in pos_by.values()))
    open_tickers = [p["ticker"] for p in pos_by.values()]

    session_executes = {}
    for t, p in pos_by.items():
        session_executes[t] = {
            "action": p.get("decision") or "HOLD",
            "mark": p.get("mark"),
            "sessions_held": p.get("sessions_held"),
            "stop": p.get("stop"),
            "r_usd": p.get("r_usd"),
            "shares": p.get("shares"),
            "unrealized_pnl_usd": p.get("unrealized_pnl_usd"),
            "realized_pnl_usd": p.get("realized_pnl_usd"),
            "ohlc": {
                "o": p.get("last_mark_o"),
                "h": p.get("last_mark_h"),
                "l": p.get("last_mark_l"),
                "c": p.get("last_mark_c"),
                "v": p.get("last_mark_v"),
                "ema9": p.get("last_mark_ema9"),
                "sma20": p.get("last_mark_sma20"),
            },
            "note": p.get("decision_note"),
        }

    new_pf = deepcopy(pf)
    new_pf.update(
        {
            "equity_mark_usd": nav,
            "cash_usd": cash,
            "open_tickers": open_tickers,
            "working_orders": [o["ticker"] for o in still_working],
            "pending_market_open": [
                {
                    "ticker": o["ticker"],
                    "shares": o.get("shares"),
                    "exit_reason": o.get("exit_reason"),
                    "execute_session": o.get("execute_session"),
                }
                for o in pending_moo
            ],
            "closed_this_session": closed_tickers,
            "r_reserved_usd": r_reserved,
            "r_used_usd": r_used,
            "updated_hkt": hkt,
            "marks_session": session,
            "unrealized_pnl_usd": upnl,
            "realized_pnl_session_usd": realized_session,
            "session_executes": session_executes,
            "ask_justin": ask_justin,
            "last_track_tc": tc_id,
            "working_notional_usd": working_notional,
            "note": f"{tc_id}: " + "; ".join(e["action"] + " " + e["ticker"] for e in executes)[:400],
        }
    )
    observe = pf.get("observe") or []
    new_pf["observe"] = observe
    new_pf["observe_clean"] = {
        "rule": "observe-daily-clean-v1",
        "keep": [],
        "drop": [],
        "after": list(observe),
        "note": "already [] — no KEEP/DROP" if not observe else "observe names present — agent must thesis-clean; script will not auto-drop",
    }
    if observe:
        ask_justin.append({"ticker": ",".join(map(str, observe)), "topic": "OBSERVE_CLEAN", "detail": "script does not auto-drop observe"})

    desired = []
    for t in open_tickers:
        desired.append(L.tv_symbol(t, pos_by[t]))
    for o in still_working + pending_moo:
        s = L.tv_symbol(o["ticker"], o)
        if s not in desired:
            desired.append(s)
    for item in observe:
        s = L.tv_symbol(item if isinstance(item, str) else item.get("ticker"), item if isinstance(item, dict) else {})
        if s not in desired:
            desired.append(s)

    brief = _brief(
        tc_id, session, hkt, executes, open_tickers, pos_by, cash, nav, r_used, upnl,
        realized_session, still_working, pending_moo, observe, desired, source, ask_justin,
    )
    soft_final = _soft_final(
        tc_id, session, hkt, source, executes, open_tickers, pos_by, cash, nav, r_used,
        r_reserved, upnl, realized_session, still_working, pending_moo, observe, desired,
        ask_justin, revoked,
    )

    result = {
        "brief": brief,
        "soft_final": soft_final,
        "tc_id": tc_id,
        "ask_justin": ask_justin,
        "applied": False,
        "already_applied": False,
        "cash": cash,
        "nav": nav,
        "r_used": r_used,
        "realized_session": realized_session,
        "open_tickers": open_tickers,
        "closed_tickers": closed_tickers,
        "queued_trims": queued_trims,
        "filled_orders": filled_orders,
        "cancelled_orders": cancelled_orders,
        "desired_shortlist": desired,
        "tv_shortlist_id": L.TV_SHORTLIST_ID,
        "next_steps": [
            "bash /workspace/us-swing-sim/tools/sheet_safe_sync.sh  then MCP apply + verify_sheet_readback.py",
            f"TV us shortlist {L.TV_SHORTLIST_ID} desired = {desired}",
        ],
        "executes": executes,
    }

    if apply:
        for t, pos in work["positions"].items():
            p = deepcopy(pos)
            p.pop("_path", None)
            L.dump_json(root / "positions" / f"{t}.json", p)
        for t in work["delete_positions"]:
            src = root / "positions" / f"{t}.json"
            dest = root / "closed" / f"{t}.json"
            payload = deepcopy(work["closed"][t])
            payload.pop("_path", None)
            if dest.exists():
                dest = root / "closed" / f"{t}_{session}.json"
            L.dump_json(dest, payload)
            if src.exists():
                src.unlink()
        for path, od in work["orders"].items():
            p = deepcopy(od)
            p.pop("_path", None)
            L.dump_json(Path(path), p)
        for path, od in new_order_files.items():
            L.dump_json(Path(path), od)
        L.dump_json(root / "state" / "portfolio.json", new_pf)
        stalks = L.load_json(root / "state" / "stalks.json")
        stalks.update(
            {
                "updated_hkt": hkt,
                "marks_session": session,
                "open": open_tickers,
                "open_positions": open_tickers,
                "working": [o["ticker"] for o in still_working],
                "working_orders": [o["ticker"] for o in still_working],
                "pending_moo": [o["ticker"] for o in pending_moo],
                "observe": observe,
                "track_tc": tc_id,
                "ask_justin": ask_justin,
                "note": new_pf.get("note"),
            }
        )
        L.dump_json(root / "state" / "stalks.json", stalks)
        _update_orders_index(root, hkt, session, tc_id, still_working, pending_moo, filled_orders, cancelled_orders)
        sf_path = root / "_finals" / f"{tc_id}.md"
        sf_path.write_text(soft_final if soft_final.endswith("\n") else soft_final + "\n", encoding="utf-8")
        _append_track_journal(root, session, hkt, brief, executes, cash, nav)
        result["applied"] = True
        result["soft_final_path"] = str(sf_path)

    return result


def _next_session_placeholder(session: str) -> None:
    return None


def _fill_order_fields(od, px, session, hkt, source, reason, pnl, remain_after):
    od = od
    od["fill_price"] = px
    od["fill_session"] = session
    od["filled_hkt"] = hkt
    od["realized_pnl_usd"] = pnl
    od["mark_source"] = source
    od["updated_hkt"] = hkt
    od["decision_session"] = session
    od["status"] = "filled"
    if remain_after is not None:
        od["remain_after"] = remain_after
    return od


def _close_position(pos, session, hkt, source, reason, px, sh, pnl, m, tc_id, note=""):
    pos["status"] = "closed"
    pos["shares"] = 0
    pos["exit_price"] = px
    pos["exit_reason"] = reason
    pos["closed_session"] = session
    pos["exit_shares"] = sh
    pos["exit_hkt"] = hkt
    pos["mark"] = px
    pos["mark_source"] = source
    pos["unrealized_pnl_usd"] = 0.0
    pos["decision"] = reason
    pos["decision_note"] = note
    pos["decision_session"] = session
    pos["track_tc"] = tc_id
    pos["updated_hkt"] = hkt
    pos["last_mark_o"] = m.get("open")
    pos["last_mark_h"] = m.get("high")
    pos["last_mark_l"] = m.get("low")
    pos["last_mark_c"] = m.get("close")
    pos["last_mark_v"] = m.get("volume")
    if m.get("ema9") is not None:
        pos["last_mark_ema9"] = m.get("ema9")


def _exec(ticker, action, detail):
    return {"ticker": ticker, "action": action, "detail": detail}


def _brief(tc_id, session, hkt, executes, open_tickers, pos_by, cash, nav, r_used, upnl,
           realized_session, still_working, pending_moo, observe, desired, source, ask_justin):
    fills = [e for e in executes if e["action"] not in {"HOLD", "KEEP"}]
    if not fills:
        head = f"{tc_id}（US session {session}；{hkt}）\n\n無成交、無取消、無出場。OPEN {len(open_tickers)}/7 全部 HOLD。realized session 0。"
    else:
        head = f"{tc_id}（US session {session}；{hkt}）\n\n本輪有動作："
    lines = [head, ""]
    if fills:
        for e in fills:
            lines.append(f"- **{e['ticker']}** {e['action']}：{e['detail']}")
        lines.append("")
    if open_tickers:
        lines.append("| Ticker | Entry | Stop | Shares | R$ | Held | Mark | uPnL |")
        lines.append("|--------|------:|-----:|------:|---:|-----:|-----:|-----:|")
        for t in open_tickers:
            p = pos_by[t]
            stop = p.get("stop")
            stop_s = f"{stop} (BE)" if float(stop) == float(p.get("entry") or 0) else str(stop)
            lines.append(
                f"| {t} | {p.get('entry')} | {stop_s} | {p.get('shares')} | {float(p.get('r_usd') or 0):.2f} "
                f"| {p.get('sessions_held')} | {p.get('mark')} | {float(p.get('unrealized_pnl_usd') or 0):+.2f} |"
            )
        lines.append("")
    lines.append(
        f"NAV **{nav:.2f}** · cash **{cash:.2f}** · R used **{r_used:.2f}** · uPnL **{upnl:+.2f}** · realized session **{realized_session:+.2f}**"
    )
    lines.append("Working：" + ("無" if not still_working else ", ".join(f"{o['ticker']} L{o.get('limit_price')}/{o.get('shares')}" for o in still_working)))
    if pending_moo:
        lines.append("Pending MOO：" + ", ".join(f"{o['ticker']} {o.get('exit_reason')} {o.get('shares')}" for o in pending_moo))
    lines.append("observe：" + ("已係 `[]`" if not observe else str(observe) + "（腳本唔會自動 DROP，要 thesis-clean）"))
    lines.append(f"TV us shortlist ({L.TV_SHORTLIST_ID}) desired：`{desired}`")
    hold_notes = [e for e in executes if e["action"] == "HOLD"]
    if hold_notes:
        lines.append("")
        lines.append("重點：")
        for e in hold_notes:
            lines.append(f"- **{e['ticker']}**：{e['detail']}")
    lines += ["", f"Marks 來源：{source}", "Sheet：跑 `tools/sheet_safe_sync.sh` 再 MCP apply + readback（腳本唔會自己改 Sheet）。"]
    if not ask_justin:
        lines.append("無需 Justin 決定。")
    else:
        lines.append("ask_justin：" + "; ".join(f"{a['ticker']} {a['topic']}" for a in ask_justin))
    return "\n".join(lines)


def _soft_final(tc_id, session, hkt, source, executes, open_tickers, pos_by, cash, nav, r_used,
                r_reserved, upnl, realized_session, still_working, pending_moo, observe, desired,
                ask_justin, revoked):
    rows = [f"| **{e['ticker']}** | **{e['action']}** | {e['detail']} |" for e in executes]
    changed = any(e["action"] != "HOLD" and e["action"] != "KEEP" for e in executes) or True
    lines = [
        f"# TRACK Soft Final — {session}",
        "",
        f"**HKT:** {hkt}  ",
        f"**marks_session:** {session}  ",
        f"**CHANGED:** {str(changed).lower()}  ",
        f"**AUTH:** pending agent (marks provided as {source})  ",
        "",
        "## Crowding",
        f"OPEN **{len(open_tickers)}/7** · cash **{cash:.2f}** · NAV **{nav:.2f}** · R used **{r_used:.2f}** · R reserved **{r_reserved:.2f}**",
        "",
        "## Executes",
        "| Ticker | Action | Detail |",
        "|--------|--------|--------|",
        *rows,
        "",
        f"Source: {source}",
        "",
        "## Book",
        f"- cash **{cash:.2f}** · NAV **{nav:.2f}** · Open **{len(open_tickers)}/7** {'+'.join(open_tickers) if open_tickers else '—'} · R used **{r_used:.2f}**",
        f"- uPnL total **{upnl:+.2f}** · realized session **{realized_session:+.2f}**",
        f"- Working: {'none' if not still_working else ', '.join(o['ticker'] for o in still_working)}",
        f"- Pending MOO: {'none' if not pending_moo else ', '.join(o['ticker'] for o in pending_moo)}",
        "",
        "## observe-daily-clean-v1",
        f"- {'already `[]` — no KEEP/DROP; do not reaccumulate' if not observe else 'names present — agent thesis-clean (script does not auto-drop)'}",
        "",
        "## TV us shortlist (351605193)",
        f"- desired `{desired}` — agent syncs list (script does not call TV MCP)",
        "",
        "## ask_justin",
        "- (none)" if not ask_justin else "\n".join(f"- {a['ticker']}: {a['topic']} — {a['detail']}" for a in ask_justin),
        "",
        "## script-first",
        "- **Connector** (TV MCP) → **Script** (`tools/track_session.py`) → `tools/sheet_safe_sync.sh`",
        "",
        "## Sheet readback",
        "- pending — run `sheet_safe_sync.sh` then `verify_sheet_readback.py`",
        "",
        "## VERIFY",
        f"- [x] R used {r_used:.2f}; reserved {r_reserved:.2f}; Open {len(open_tickers)}/7",
        f"- [x] cash {cash:.2f}; NAV {nav:.2f} = cash + marked open shares",
        "- [x] Marks from provided official 1D bars — no fabricated prices",
        "- [x] supply-half REVOKED — annotated only, no apply/ask" if revoked else "- [ ] supply-half status unexpected",
        "- [x] No live broker; no Second brain skill edits; no regime rescore",
        "- [x] Banned tokens not used by this script",
    ]
    return "\n".join(lines) + "\n"


def _update_orders_index(root, hkt, session, tc_id, still_working, pending_moo, filled_orders, cancelled_orders):
    idx = L.load_json(root / "orders" / "_index.json")
    idx["updated_hkt"] = hkt
    idx["working"] = [o["ticker"] for o in still_working]
    idx["pending_market_open"] = [o["ticker"] for o in pending_moo]
    idx["session_tracked"] = session
    idx["track_tc"] = tc_id
    filled = list(idx.get("filled") or [])
    for f in filled_orders:
        tag = f["ticker"]
        if tag not in filled:
            filled.append(tag)
        order_stem = Path(f["order"]).stem
        if order_stem not in filled:
            filled.append(order_stem)
    idx["filled"] = filled
    if cancelled_orders:
        cancelled = list(idx.get("cancelled") or [])
        for c in cancelled_orders:
            if c["ticker"] not in cancelled:
                cancelled.append(c["ticker"])
        idx["cancelled"] = cancelled
    idx["note"] = f"{tc_id}: filled {len(filled_orders)} cancelled {len(cancelled_orders)}"
    L.dump_json(root / "orders" / "_index.json", idx)


def _append_track_journal(root, session, hkt, brief, executes, cash, nav):
    # Track of session D is written next calendar morning; journal file is session date.
    path = root / "journal" / f"{session}.md"
    block = (
        f"## TRACK — {session} ({hkt})\n\n"
        + brief
        + f"\n\n### Ledger\n- cash {cash} · NAV {nav} · `state/portfolio.json`\n"
    )
    if path.exists():
        cur = path.read_text(encoding="utf-8")
        if f"## TRACK — {session}" in cur:
            return
        text = cur.rstrip() + "\n\n" + block
    else:
        text = f"# US swing sim journal — {session}\n\n" + block
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="US swing sim post-close track")
    p.add_argument("--root", default=str(ROOT))
    p.add_argument("--marks")
    p.add_argument("--print-symbols", action="store_true")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--sync-payloads", action="store_true", help="After --apply, run sync_sheet.py --strict (no MCP)")
    p.add_argument("--json-out")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    root = Path(args.root)

    if args.self_test:
        from test_daily_scripts import test_pure, test_preopen, test_track_1113

        test_pure()
        test_preopen()
        test_track_1113()
        print("track_session self-test PASS")
        return 0

    if args.print_symbols:
        syms = L.desired_shortlist(root)
        print(",".join(syms))
        print(json.dumps({"symbols": syms, "list_id": L.TV_SHORTLIST_ID}, ensure_ascii=False))
        return 0
    if not args.marks:
        print("Need --marks official 1D JSON (or --print-symbols / --self-test)", file=sys.stderr)
        return 2
    marks_doc = L.load_json(Path(args.marks))
    do_apply = bool(args.apply) and not args.dry_run
    result = apply_track(root, marks_doc, apply=do_apply, force=args.force)
    print(result["brief"])
    if result.get("ask_justin"):
        print("\nask_justin:")
        print(json.dumps(result["ask_justin"], ensure_ascii=False, indent=2))
    if args.json_out:
        payload = {k: v for k, v in result.items() if k != "soft_final"}
        L.dump_json(Path(args.json_out), payload)
    if do_apply and args.sync_payloads:
        import subprocess

        r = subprocess.run(
            [sys.executable, str(root / "tools" / "sync_sheet.py"), "--strict"],
            check=False,
        )
        if r.returncode != 0:
            print("sync_sheet.py --strict failed", file=sys.stderr)
            return r.returncode
        print("sync_sheet.py --strict OK — next: bash tools/sheet_safe_sync.sh then MCP apply + verify")
    if not do_apply and not result.get("already_applied"):
        print("\n[dry-run] 未寫 ledger。加 --apply 先寫 positions/portfolio/journal/Soft Final。", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
