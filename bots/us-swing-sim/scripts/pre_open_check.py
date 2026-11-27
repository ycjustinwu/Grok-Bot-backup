#!/usr/bin/env python3
"""Pre-open check: classify WATCH_GAP / HOLD / pending GO. Never invent Open fills.

Usage:
  python3 pre_open_check.py --print-symbols
  python3 pre_open_check.py --marks marks.json [--dry-run|--apply]

Agent still does one TradingView MCP batch; this script does the grind.
Portfolio cash/shares/NAV are never changed here.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sim_lib as L

ROOT = L.ROOT


def _near_mark(mark: dict, pos: dict) -> tuple[float | None, str]:
    pm = mark.get("premarket_close")
    if pm is not None:
        return float(pm), "盤前"
    for k in ("near", "near_mark", "last"):
        if mark.get(k) is not None:
            return float(mark[k]), "近價"
    if pos.get("mark") is not None:
        return float(pos["mark"]), "近價（上日 mark，無盤前）"
    if mark.get("close") is not None:
        return float(mark["close"]), "近價（上日 close，無盤前）"
    return None, "無近價"


def _pm_delta(mark: dict) -> tuple[float | None, float | None]:
    pct = mark.get("premarket_change_pct")
    if pct is None:
        pct = mark.get("premarket_change")
    vol = mark.get("premarket_volume")
    if pct is None:
        return None, vol if vol is None else float(vol)
    # batch sometimes stores percent already (0.57 meaning +0.57%), sometimes fraction
    p = float(pct)
    if abs(p) <= 1 and mark.get("premarket_close") is not None and mark.get("close"):
        # 0.574 could be percent already (historical 11/13 files store 0.574 as +0.57%)
        # If close is 58.345 and pm 58.68, change is 0.57%, stored as 0.574 — treat as percent.
        p = p  # already percent-like when |p|<2 and pm exists
    return p, None if vol is None else float(vol)


def _fmt_pm_pct(mark: dict, pos: dict, near: float | None) -> str | None:
    prior = mark.get("close")
    if prior is None:
        prior = pos.get("mark")
    pm = mark.get("premarket_close")
    if pm is None or prior in (None, 0):
        raw = mark.get("premarket_change_pct", mark.get("premarket_change"))
        if raw is None:
            return None
        return f"{float(raw):+.2f}%"
    return f"{(float(pm) - float(prior)) / float(prior) * 100:+.2f}%"


def run(root: Path, marks_doc: dict, apply: bool) -> dict:
    session = marks_doc.get("session")
    if not session:
        raise SystemExit("marks JSON missing session (US cash session date)")
    source = marks_doc.get("source") or "TradingView MCP (named in marks file)"
    checked = marks_doc.get("checked_hkt") or L.now_hkt()
    marks = marks_doc.get("marks") or {}
    pf = L.load_json(root / "state" / "portfolio.json")
    positions = L.open_positions(root)
    orders = L.active_orders(root)
    pending = [
        o
        for o in orders
        if str(o.get("order_type") or "") in {"market_open_sell", "market_close_sell"}
        or str(o.get("status") or "") in {"pending", "pending_market_open", "queued"}
    ]
    working = [
        o
        for o in orders
        if str(o.get("order_type") or "") in {"limit_buy", "limit_sell", "buy_stop"}
        and str(o.get("status") or "").lower() not in L.TERMINAL_ORDER
    ]

    decisions = []
    ask_justin = []
    notes = []
    pos_flags = {}

    by_t = {p["ticker"]: p for p in positions}
    for pos in positions:
        t = pos["ticker"]
        stop = float(pos.get("hard_sl") or pos.get("stop"))
        shares = int(pos["shares"])
        mark = marks.get(t) or {}
        near, near_label = _near_mark(mark, pos)
        gap = L.classify_watch_gap(near, stop)
        held = int(pos.get("sessions_held") or 0)
        grace = held < 3
        post_trim = bool(pos.get("post_trim_hold") or pos.get("trim_1_3_done"))
        pm_pct = _fmt_pm_pct(mark, pos, near)
        vol = mark.get("premarket_volume")
        action = gap["action"]
        if action == "NO_PM":
            action = "HOLD"
        detail_bits = [
            f"OPEN {shares}股 @{pos.get('entry')}／SL {stop}",
            f"{near_label} {near if near is not None else '—'}"
            + (f"（{pm_pct}）" if pm_pct else ""),
        ]
        if vol is not None and near_label.startswith("盤前"):
            detail_bits[-1] += f"，vol {vol}"
        detail_bits.append(gap["note"])
        detail_bits.append(f"Open < {stop} 先 GAP_SL 全出 {shares}（而家唔 invent）")
        if post_trim:
            detail_bits.append("post-trim-hold-v1，盤前唔出場")
        if grace:
            detail_bits.append(f"held={held} grace ON")
        else:
            detail_bits.append(f"held={held} grace OFF")
        if L.supply_half_revoked(root):
            detail_bits.append("supply-half 已 REVOKED — 唔套用、唔再問")
        if gap["ask"]:
            ask_justin.append({"ticker": t, "topic": "WATCH_GAP_BAND", "detail": gap["note"]})
        rec = {
            "ticker": t,
            "layer": "open",
            "action": action if action != "NO_PM" else "HOLD",
            "detail": "；".join(detail_bits),
            "cushion_usd": gap["cushion_usd"],
            "cushion_pct": gap["cushion_pct"],
            "near": near,
            "near_label": near_label,
            "hard_sl": stop,
            "shares": shares,
        }
        decisions.append(rec)
        pos_flags[t] = {
            "session": session,
            "checked_hkt": checked,
            "action": rec["action"],
            "pending_trim": None,
            "mark_pm": mark.get("premarket_close"),
            "mark_close": mark.get("close", pos.get("mark")),
            "near_mark": near,
            "hard_sl": stop,
            "cushion_usd": gap["cushion_usd"],
            "cushion_pct": gap["cushion_pct"],
            "shares": shares,
            "gap_rule": f"official Open < {stop} → GAP_SL all {shares} @ Open; else HOLD, Hard SL session-close-based; no invent",
        }

    pending_out = []
    for od in pending:
        t = od["ticker"]
        pos = by_t.get(t)
        stop_before = float(
            od.get("stop_before")
            or (pos.get("hard_sl") or pos.get("stop") if pos else 0)
            or 0
        )
        shares_all = int(pos["shares"]) if pos else int(od.get("shares") or 0)
        trim_sh = int(od.get("shares") or 0)
        remain = od.get("remain_after")
        stop_after = od.get("stop_after")
        reason = od.get("exit_reason") or od.get("order_type")
        mark = marks.get(t) or {}
        near, near_label = _near_mark(mark, pos or {})
        action = "GO"
        gap_note = (
            f"若官方 Open < {stop_before}，{shares_all} 股 GAP_SL 全出、呢張單被取代；而家唔 invent"
        )
        detail = f"{reason} {trim_sh} 股 GO；{gap_note}"
        if remain is not None:
            detail += f"；若成交剩 {remain}，停損改 {stop_after}"
        rec = {
            "ticker": t,
            "layer": "pending_moo",
            "action": action,
            "detail": detail,
            "shares": trim_sh,
            "remain_after": remain,
            "stop_before": stop_before,
            "stop_after": stop_after,
            "exit_reason": reason,
            "near": near,
        }
        decisions.append(rec)
        pending_out.append(rec)
        if t in pos_flags:
            pos_flags[t]["pending_trim"] = {
                "shares": trim_sh,
                "remain_after": remain,
                "stop_after": stop_after,
                "action": "GO",
            }

    working_out = []
    for od in working:
        t = od["ticker"]
        lp = od.get("limit_price")
        mark = marks.get(t) or {}
        near, near_label = _near_mark(mark, {})
        # If no premarket, do not treat prior close as a live near for away flags.
        has_pm = mark.get("premarket_close") is not None
        live_near = float(mark["premarket_close"]) if has_pm else None
        thresh = od.get("away_5pct_thresh")
        if thresh is None and lp is not None:
            thresh = float(lp) * 1.05
        prior = mark.get("close")
        side = str(od.get("side") or "buy").lower()
        bits = [f"限價單 KEEP L{lp}/{od.get('shares')}"]
        vol = mark.get("premarket_volume")
        if live_near is not None:
            pm_bit = f"{near_label} {live_near}"
            if vol is not None:
                pm_bit += f"，vol {vol}"
            bits.append(pm_bit)
            if side == "buy" and thresh is not None and live_near >= float(thresh):
                bits.append(
                    f"盤前已過 L×1.05={thresh}；若官方 Open ≥ {thresh} → observe 不追；盤前唔取消、唔 invent"
                )
            elif side == "sell" and thresh is not None and live_near <= float(thresh):
                bits.append(
                    f"盤前已過賣單 L×0.95={thresh}；若官方 Open ≤ {thresh} → observe 不追；盤前唔取消、唔 invent"
                )
            elif side == "buy" and lp is not None and live_near <= float(lp):
                bits.append("盤前已到／低過限價；官方 session 先計成交、唔 invent")
            else:
                bits.append("盤前唔成交、唔 invent")
        else:
            bits.append("無盤前；盤前唔成交、唔 invent")
            if prior is not None and thresh is not None:
                bits.append(f"上日 close {prior}，L×1.05={thresh}")
                if side == "buy" and float(prior) >= float(thresh):
                    bits.append("上日 close 已過 5%（limit-away 係收市規則，今晚唔盤前取消）")
        rec = {
            "ticker": t,
            "layer": "working",
            "action": "KEEP",
            "detail": "；".join(bits),
            "limit_price": lp,
            "shares": od.get("shares"),
            "stop": od.get("stop"),
            "near": live_near,
            "near_label": near_label if has_pm else "無盤前",
            "away_5pct_thresh": thresh,
            "prior_close": prior,
        }
        working_out.append(rec)
        decisions.append(rec)

    open_n = len(positions)
    max_pos = int(pf.get("max_positions") or 7)
    cash = L.money(pf.get("cash_usd") or 0)
    nav = L.money(pf.get("equity_mark_usd") or 0)
    upnl = pf.get("unrealized_pnl_usd")
    headline_flags = []
    watch = [d["ticker"] for d in decisions if d.get("layer") == "open" and d["action"] == "WATCH_GAP"]
    tight = [d["ticker"] for d in decisions if d.get("layer") == "open" and d["action"] == "TIGHT"]
    holds = [d["ticker"] for d in decisions if d.get("layer") == "open" and d["action"] == "HOLD"]
    if watch:
        headline_flags.append("、".join(watch) + " WATCH_GAP")
    if tight:
        headline_flags.append("、".join(tight) + " TIGHT（ask）")
    if holds:
        headline_flags.append("／".join(holds) + " HOLD")
    pending_txt = "無 pending" if not pending_out else "pending " + "、".join(f"{p['ticker']} GO" for p in pending_out)
    working_txt = "無 working" if not working_out else "working " + "、".join(f"{w['ticker']} KEEP" for w in working_out)

    brief_lines = [
        f"盤前（美股開市約 22:30 HKT · session {session}）：OPEN {open_n}/{max_pos}"
        + (("，" + "，".join(headline_flags)) if headline_flags else "，全部 HOLD")
        + f"。{pending_txt}、{working_txt}。唔 invent Open 成交。",
        "",
    ]
    for d in decisions:
        if d["layer"] == "open":
            brief_lines.append(f"- **{d['ticker']}** {d['detail']}。")
        elif d["layer"] == "pending_moo":
            brief_lines.append(f"- **{d['ticker']} pending**：{d['detail']}。")
        else:
            brief_lines.append(f"- **{d['ticker']}**：{d['detail']}。")
    marks_note = pf.get("marks_session") or "上日"
    brief_lines += [
        "",
        f"Book 未改：cash {cash:,.2f} · NAV {nav:,.2f}"
        + (f" · uPnL {upnl:+.2f}" if upnl is not None else "")
        + f"（marks 仍係 {marks_note} 收市）。來源：{source}；checked {checked}。",
        "Ledger：`state/pre_open_latest.json` + journal。",
    ]
    brief = "\n".join(brief_lines)

    doc = {
        "type": "pre_open_check",
        "session": session,
        "checked_hkt": checked,
        "source": source,
        "marks": marks,
        "decisions": decisions,
        "pending_moo": pending_out,
        "working_orders": working_out,
        "open_positions": [p["ticker"] for p in positions],
        "observe_noted": pf.get("observe") or [],
        "no_invented_fills": True,
        "ask_justin": ask_justin,
        "quiet": False,
        "notes": notes
        + [
            f"OPEN {open_n}/{max_pos} · cash/NAV {cash}/{nav} · 唔改 book",
            "Supply half stays REVOKED — do not re-ask/apply" if L.supply_half_revoked(root) else "",
        ],
    }
    doc["notes"] = [n for n in doc["notes"] if n]

    journal_block = _journal_block(session, checked, source, decisions, pf, cash, nav)

    if apply:
        L.dump_json(root / "state" / "pre_open_latest.json", doc)
        for t, flag in pos_flags.items():
            path = root / "positions" / f"{t}.json"
            pos = L.load_json(path)
            if not pos:
                continue
            pos["pre_open_flag"] = flag
            pos["updated_hkt"] = checked
            L.dump_json(path, pos)
        _append_journal(root, session, journal_block)

    return {
        "brief": brief,
        "doc": doc,
        "ask_justin": ask_justin,
        "applied": apply,
        "symbols": L.desired_shortlist(root),
    }


def _journal_block(session, checked, source, decisions, pf, cash, nav) -> str:
    rows = []
    for d in decisions:
        if d["layer"] == "open":
            rows.append(f"| {d['ticker']} | **{d['action']}** | {d['detail']} |")
    pending = [d for d in decisions if d["layer"] == "pending_moo"]
    working = [d for d in decisions if d["layer"] == "working"]
    lines = [
        f"## PRE-OPEN — US cash open {session} (winter EST)",
        f"- checked: {checked}",
        f"- source: {source}",
        f"- pending MOO: **{'none' if not pending else ', '.join(p['ticker']+' GO' for p in pending)}**",
        f"- working: **{'none' if not working else ', '.join(w['ticker']+' KEEP' for w in working)}**",
        f"- ask_justin: {'none' if not any(d['action']=='TIGHT' for d in decisions) else 'WATCH_GAP band'}",
        "",
        "### Decisions",
        "| Ticker | Action | Detail |",
        "|--------|--------|--------|",
        *rows,
        "",
        "### Flags",
        "- No invent Open fill",
        "- Supply half 已撤回，今晚唔再問／唔再套用",
        "",
        "### Ledger",
        "- `state/pre_open_latest.json`",
        f"- portfolio / shares / cash 未改（cash {cash} · NAV {nav}；等官方 Open）",
        "",
    ]
    return "\n".join(lines)


def _append_journal(root: Path, session: str, block: str) -> None:
    path = root / "journal" / f"{session}.md"
    # Pre-open on session D is written on calendar D (evening HKT, still same date)
    # If box date already next day, still use session file? Pre-open 11/13 was journal/2026-11-13.md.
    if path.exists() and f"PRE-OPEN — US cash open {session}" in path.read_text(encoding="utf-8"):
        return
    if path.exists():
        text = path.read_text(encoding="utf-8").rstrip() + "\n\n" + block
    else:
        text = f"# US swing sim journal — {session}\n\n" + block
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="US swing sim pre-open check")
    p.add_argument("--root", default=str(ROOT))
    p.add_argument("--marks", help="Marks JSON from TV MCP batch (premarket_*)")
    p.add_argument("--print-symbols", action="store_true")
    p.add_argument("--apply", action="store_true", help="Write pre_open_latest + journal + pre_open_flag")
    p.add_argument("--dry-run", action="store_true", help="Default: print brief only")
    p.add_argument("--json-out", help="Write result JSON to this path")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    root = Path(args.root)

    if args.self_test:
        from test_daily_scripts import test_preopen, test_pure

        test_pure()
        test_preopen()
        print("pre_open_check self-test PASS")
        return 0

    if args.print_symbols:
        syms = L.desired_shortlist(root)
        print(",".join(syms))
        print(json.dumps({"symbols": syms, "list_id": L.TV_SHORTLIST_ID}, ensure_ascii=False))
        return 0

    if not args.marks:
        print("Need --marks JSON (or --print-symbols / --self-test)", file=sys.stderr)
        return 2
    marks_doc = L.load_json(Path(args.marks))
    result = run(root, marks_doc, apply=bool(args.apply) and not args.dry_run)
    print(result["brief"])
    if result["ask_justin"]:
        print("\nask_justin:")
        print(json.dumps(result["ask_justin"], ensure_ascii=False, indent=2))
    if args.json_out:
        L.dump_json(Path(args.json_out), {k: v for k, v in result.items() if k != "brief"} | {"brief": result["brief"]})
    if not args.apply:
        print("\n[dry-run] 未寫 ledger。加 --apply 先寫 pre_open_latest + journal。", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
