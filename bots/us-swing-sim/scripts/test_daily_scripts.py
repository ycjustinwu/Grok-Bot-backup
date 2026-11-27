#!/usr/bin/env python3
"""Self-tests for pre_open_check / track_session. Never touch the live ledger root."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sim_lib as L
import pre_open_check
import track_session

LIVE = L.ROOT

MARKS_1113 = {
    "session": "2026-11-13",
    "source": "TradingView MCP official 1D bar 2026-11-13 (fixture from TRACK-20261113)",
    "checked_hkt": "2026-11-14 06:05 HKT",
    "marks": {
        "UNTY": {
            "open": 58.73,
            "high": 59.2,
            "low": 58.1,
            "close": 58.915,
            "volume": 33815,
            "ema9": 58.314453492083246,
            "sma20": 57.8815,
            "premarket_close": 58.68,
            "premarket_change_pct": 0.5741708801096937,
            "premarket_volume": 136,
        },
        "CRL": {
            "open": 342.18,
            "high": 342.58,
            "low": 333.04,
            "close": 337.97,
            "volume": 807019,
            "ema9": 341.2254756458494,
            "sma20": 342.941,
            "premarket_close": 342.46,
            "premarket_change_pct": 0.4841407235703111,
            "premarket_volume": 94,
        },
        "EL": {
            "open": 111.09,
            "high": 112.74,
            "low": 109.5459,
            "close": 111.75,
            "volume": 2330911,
            "ema9": 110.74991509178889,
            "sma20": 108.878,
            "premarket_close": 111.03,
            "premarket_change_pct": 0.47054565197719295,
            "premarket_volume": 313,
        },
    },
}


def _assert(cond, msg):
    if not cond:
        raise AssertionError(msg)


def test_pure():
    g = L.classify_watch_gap(58.68, 57.46)
    _assert(g["action"] == "WATCH_GAP", g)
    _assert(g["cushion_pct"] == 2.12, g)
    _assert(g["cushion_usd"] == 1.22, g)

    h = L.classify_watch_gap(58.50, 56.014)
    _assert(h["action"] == "HOLD", h)
    _assert(h["cushion_pct"] == 4.44 or h["cushion_pct"] >= 4.25, h)  # (58.50-56.014)/56.014*100=4.44

    mid = L.classify_watch_gap(57.46 * 1.03, 57.46)  # 3.00%
    _assert(mid["action"] == "TIGHT" and mid["ask"], mid)

    _assert(L.better_buy_fill(337.52, 335.66, 326.29) == 335.66, "CRL better open")
    _assert(L.better_buy_fill(110.06, 111.75, 109.64) == 110.06, "EL fill at limit")
    _assert(L.better_buy_fill(337.52, 340.00, 338.00) is None, "no fill if low > limit")

    stop, risk = L.reanchor_stop(337.52, 311.68, 335.66)
    _assert(abs(risk - 25.84) < 1e-9, risk)
    _assert(stop == 309.82, stop)

    # remaining room vs 11/13 closes
    unty = L.load_json(LIVE / "positions" / "UNTY.json")
    _assert(L.remaining_room_r(unty, 58.915) == -0.0588, L.remaining_room_r(unty, 58.915))
    crl = L.load_json(LIVE / "positions" / "CRL.json")
    _assert(L.remaining_room_r(crl, 337.97) == 0.2295, L.remaining_room_r(crl, 337.97))
    el = L.load_json(LIVE / "positions" / "EL.json")
    _assert(L.remaining_room_r(el, 111.75) == 0.6937, L.remaining_room_r(el, 111.75))

    prev = 58.164316865104055
    ema = L.ema9_continue(prev, 58.915)
    _assert(abs(ema - 58.314453492083246) < 1e-12, ema)

    _assert(L.supply_half_revoked(LIVE) is True, "supply-half must stay revoked")
    _assert(L.money(114 * 1.03) == 117.42, L.money(114 * 1.03))
    _assert(L.money((10.00 - 11.14) * 364) == -414.96, L.money((10.00 - 11.14) * 364))


def _copy_book(dst: Path) -> Path:
    for sub in ("state", "positions", "orders", "journal", "watchlist", "closed", "_finals"):
        src = LIVE / sub
        if src.is_dir():
            shutil.copytree(src, dst / sub, dirs_exist_ok=True)
    (dst / "tools").mkdir(exist_ok=True)
    return dst


def test_preopen():
    with tempfile.TemporaryDirectory() as td:
        root = _copy_book(Path(td))
        # Use 11/13 PM marks; book already has same shares/stops
        marks = {
            "session": "2026-11-13",
            "source": "fixture premarket from pre_open_latest",
            "checked_hkt": "2026-11-13 22:08 HKT",
            "marks": {
                t: {
                    "close": m.get("close") or {"UNTY": 58.345, "CRL": 340.81, "EL": 110.51}[t],
                    "premarket_close": m["premarket_close"],
                    "premarket_change_pct": m["premarket_change_pct"],
                    "premarket_volume": m["premarket_volume"],
                }
                for t, m in MARKS_1113["marks"].items()
            },
        }
        # Prior closes for PM Δ%
        marks["marks"]["UNTY"]["close"] = 58.345
        marks["marks"]["CRL"]["close"] = 340.81
        marks["marks"]["EL"]["close"] = 110.51
        out = pre_open_check.run(root, marks, apply=True)
        dec = {d["ticker"]: d for d in out["doc"]["decisions"] if d["layer"] == "open"}
        _assert(dec["UNTY"]["action"] == "WATCH_GAP", dec["UNTY"])
        _assert(dec["UNTY"]["cushion_pct"] == 2.12, dec["UNTY"])
        _assert(dec["CRL"]["action"] == "HOLD", dec["CRL"])
        _assert(dec["CRL"]["cushion_pct"] == 10.54, dec["CRL"])
        _assert(dec["EL"]["action"] == "HOLD", dec["EL"])
        _assert(dec["EL"]["cushion_pct"] == 5.74, dec["EL"])
        _assert(out["ask_justin"] == [], out["ask_justin"])
        pf = L.load_json(root / "state" / "portfolio.json")
        live_pf = L.load_json(LIVE / "state" / "portfolio.json")
        _assert(pf["cash_usd"] == live_pf["cash_usd"], "pre-open must not change cash")
        _assert((root / "state" / "pre_open_latest.json").is_file(), "wrote pre_open_latest")
        _assert("WATCH_GAP" in out["brief"] and "唔 invent" in out["brief"], out["brief"][:400])


def _rewind_to_post_1112(root: Path) -> None:
    """Rewind copied book to post-TRACK-20261112 (pre-TRACK-20261113)."""
    unty = L.load_json(root / "positions" / "UNTY.json")
    crl = L.load_json(root / "positions" / "CRL.json")
    el = L.load_json(root / "positions" / "EL.json")
    unty.update(
        {
            "sessions_held": 4,
            "mark": 58.345,
            "unrealized_pnl_usd": 203.55,
            "last_mark_session": "2026-11-12",
            "last_mark_c": 58.345,
            "last_mark_o": 58.49,
            "last_mark_h": 58.49,
            "last_mark_l": 57.93,
            "last_mark_ema9": 58.164316865104055,
            "last_mark_sma20": 57.75575,
            "decision_session": "2026-11-12",
            "ema9_grace_active": False,
            "track_tc": "TRACK-20261112",
        }
    )
    crl.update(
        {
            "sessions_held": 0,
            "mark": 340.81,
            "unrealized_pnl_usd": 97.85,
            "last_mark_session": "2026-11-12",
            "last_mark_c": 340.81,
            "last_mark_o": 335.66,
            "last_mark_ema9": 342.0393445573117,
            "last_mark_sma20": 341.05,
            "decision_session": "2026-11-12",
            "ema9_grace_active": True,
            "track_tc": "TRACK-20261112",
        }
    )
    el.update(
        {
            "sessions_held": 0,
            "mark": 110.51,
            "unrealized_pnl_usd": 40.50,
            "last_mark_session": "2026-11-12",
            "last_mark_c": 110.51,
            "last_mark_ema9": 110.49989386473611,
            "last_mark_sma20": 108.5175,
            "decision_session": "2026-11-12",
            "ema9_grace_active": True,
            "track_tc": "TRACK-20261112",
        }
    )
    L.dump_json(root / "positions" / "UNTY.json", unty)
    L.dump_json(root / "positions" / "CRL.json", crl)
    L.dump_json(root / "positions" / "EL.json", el)
    pf = L.load_json(root / "state" / "portfolio.json")
    pf["marks_session"] = "2026-11-12"
    pf["cash_usd"] = 70578.32
    pf["equity_mark_usd"] = 100418.96
    pf["unrealized_pnl_usd"] = 341.90
    pf["realized_pnl_session_usd"] = -47.30
    pf["last_track_tc"] = "TRACK-20261112"
    pf["session_executes"] = {}
    L.dump_json(root / "state" / "portfolio.json", pf)


def test_track_1113():
    with tempfile.TemporaryDirectory() as td:
        root = _copy_book(Path(td))
        _rewind_to_post_1112(root)
        out = track_session.apply_track(root, MARKS_1113, apply=True)
        _assert(not out.get("already_applied"), out.get("brief"))
        _assert(out["cash"] == 70578.32, out["cash"])
        _assert(out["nav"] == 100607.70, out["nav"])
        _assert(out["r_used"] == 946.36, out["r_used"])
        _assert(out["realized_session"] == 0.0, out["realized_session"])
        _assert(out["open_tickers"] == ["UNTY", "CRL", "EL"] or set(out["open_tickers"]) == {"UNTY", "CRL", "EL"}, out["open_tickers"])
        _assert(out["closed_tickers"] == [], out["closed_tickers"])
        _assert(out["ask_justin"] == [], out["ask_justin"])
        unty = L.load_json(root / "positions" / "UNTY.json")
        crl = L.load_json(root / "positions" / "CRL.json")
        el = L.load_json(root / "positions" / "EL.json")
        _assert(unty["sessions_held"] == 5, unty["sessions_held"])
        _assert(crl["sessions_held"] == 1, crl["sessions_held"])
        _assert(el["sessions_held"] == 1, el["sessions_held"])
        _assert(unty["decision"] == "HOLD", unty["decision"])
        _assert(crl["decision"] == "HOLD", crl["decision_note"])
        _assert(el["decision"] == "HOLD", el["decision"])
        _assert(unty["remaining_Room_To_Supply_R"] == -0.0588, unty.get("remaining_Room_To_Supply_R"))
        _assert(crl["remaining_Room_To_Supply_R"] == 0.2295, crl.get("remaining_Room_To_Supply_R"))
        _assert(el["remaining_Room_To_Supply_R"] == 0.6937, el.get("remaining_Room_To_Supply_R"))
        _assert(unty["unrealized_pnl_usd"] == 334.65, unty["unrealized_pnl_usd"])
        _assert(crl["unrealized_pnl_usd"] == 43.89, crl["unrealized_pnl_usd"])
        _assert(el["unrealized_pnl_usd"] == 152.10, el["unrealized_pnl_usd"])
        _assert("supply-half" in (unty.get("decision_note") or "") or "REVOKED" in (unty.get("decision_note") or ""), unty.get("decision_note"))
        _assert("post-trim-hold" in (unty.get("decision_note") or ""), unty.get("decision_note"))
        # live ledger untouched
        live_u = L.load_json(LIVE / "positions" / "UNTY.json")
        _assert(live_u["sessions_held"] == 5 and live_u["mark"] == 58.915, "live book mutated")
        # idempotent
        again = track_session.apply_track(root, MARKS_1113, apply=True)
        _assert(again.get("already_applied") is True, again)


def test_refuse_invent():
    with tempfile.TemporaryDirectory() as td:
        root = _copy_book(Path(td))
        _rewind_to_post_1112(root)
        bad = {"session": "2026-11-13", "marks": {"UNTY": {"open": 58.73, "close": 58.915}}}
        try:
            track_session.apply_track(root, bad, apply=False)
        except SystemExit as e:
            _assert("invent" in str(e).lower() or "missing" in str(e).lower(), str(e))
        else:
            raise AssertionError("should refuse incomplete marks")


if __name__ == "__main__":
    test_pure()
    test_preopen()
    test_track_1113()
    test_refuse_invent()
    print("all daily-script tests PASS")
