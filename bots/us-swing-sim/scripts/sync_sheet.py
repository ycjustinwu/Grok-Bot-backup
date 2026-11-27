#!/usr/bin/env python3
"""Single writer: rebuild US swing sim Google Sheet tabs from ledger.

Protocol: safe-sync-v1
Writes .sheet_payloads/*.json + apply_plan.json for Sheets MCP apply.
Does NOT call Sheets API. Does NOT patch cells ad-hoc.
See ../SHEET_CONTRACT.md and tools/sheet_safe_sync.sh.
"""
from __future__ import annotations

import argparse
import json
import sys
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("/workspace/us-swing-sim")
PAYLOAD = ROOT / ".sheet_payloads"
SPREADSHEET_ID = "1mtSZo10jrCC_o4x0HnjjyrCEj_3FbBCcN8pgvZkU7v4"
HKT = ZoneInfo("Asia/Hong_Kong")

SHEET_IDS = {
    "Dashboard": 1341387052,
    "Book": 1527041040,
    "Watchlist": 1233150494,
    "Orders": 1596349931,
    "Positions": 1417146068,
    "Journal": 1116679681,
    "Logic_Audit": 600868846,
}

GRADES = ["追蹤中", "精準到價", "假突破止蝕", "未到價過期", "結構作廢"]
SKIP_NAMES = {"FORMAT.md", "_TEMPLATE.json", "_index.json"}


def now_hkt() -> str:
    return datetime.now(HKT).strftime("%Y-%m-%d %H:%M HKT")


def as_text_date(s) -> str:
    """Force YYYY-MM-DD to text under parseInput=true (avoid Sheets serial)."""
    if s is None or s == "":
        return ""
    s = str(s)
    if len(s) >= 10 and s[4] == "-" and s[7] == "-":
        return "'" + s[:10] if not s.startswith("'") else s
    return s


def load_json(path: Path):
    return json.loads(path.read_text())


def glob_json(folder: Path):
    if not folder.exists():
        return []
    out = []
    for p in sorted(folder.glob("*.json")):
        if p.name in SKIP_NAMES or p.name.startswith("_"):
            continue
        out.append((p, load_json(p)))
    return out


def blank_rows(n_cols: int, n_rows: int):
    return [[""] * n_cols for _ in range(n_rows)]


def upsert_equity_curve(portfolio: dict) -> list[dict]:
    path = ROOT / "state" / "equity_curve.json"
    if path.exists():
        data = load_json(path)
    else:
        data = {"equity_start": float(portfolio.get("equity_start_usd", 100000)), "rows": []}
    start = float(data.get("equity_start", 100000))
    rows = list(data.get("rows") or [])
    session = portfolio["marks_session"]
    nav = float(portfolio["equity_mark_usd"])
    cash = float(portfolio["cash_usd"])
    open_count = len(portfolio.get("open_tickers") or [])
    note = (portfolio.get("note") or "")[:120]
    new_row = {
        "session": session,
        "nav": nav,
        "cash": cash,
        "open_count": open_count,
        "note": note,
        "cum_pct": round((nav - start) / start * 100, 4),
        "cum_r": round((nav - start) / 1000.0, 4),
    }
    found = False
    for i, r in enumerate(rows):
        if r.get("session") == session:
            rows[i] = new_row
            found = True
            break
    if not found:
        rows.append(new_row)
    rows.sort(key=lambda r: r["session"])
    # Dedup by session (keep last)
    dedup = {}
    for r in rows:
        dedup[r["session"]] = r
    rows = [dedup[k] for k in sorted(dedup)]
    data["rows"] = rows
    data["equity_start"] = start
    data["updated_hkt"] = now_hkt()
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return rows


def build_book(portfolio, opens, closeds, orders, watches, sync_ts):
    """Ops home: compact strip + OPEN / PENDING MOO / WORKING LIMITS only.
    CLOSED → Positions; WATCH → Watchlist; full Account → Dashboard.
    closeds/watches kept in signature for call-site stability; unused.
    """
    cols = 10
    rows = []
    nav = float(portfolio["equity_mark_usd"])
    cash = float(portfolio["cash_usd"])
    open_n = len(opens)
    max_pos = portfolio.get("max_positions", 7)
    working = [o for _, o in orders if o.get("status") == "working"]
    working_n = len(working)
    r_used = float(portfolio.get("r_used_usd") or 0)
    r_res = float(portfolio.get("r_reserved_usd") or 0)

    # Row 1 title
    rows.append(["US swing 模擬倉 · Book", as_text_date(portfolio["marks_session"]), sync_ts] + [""] * 7)
    # Row 2 compact one-line strip (not full Account block)
    rows.append([
        "NAV", nav,
        "Cash", cash,
        f"Open {open_n}/{max_pos}",
        f"Working {working_n}",
        f"R used {r_used}",
        f"R reserved {r_res}",
        f"marks_session {portfolio['marks_session']}",
        f"sync {sync_ts}",
    ])

    rows.append([""] * cols)
    rows.append(["OPEN", "", "", "", "", "", "", "", "", ""])
    rows.append(["Ticker", "Shares", "Entry", "Stop", "Mark", "uPnL", "R$", "Held", "Grace", "Note"])
    if not opens:
        rows.append(["(none)"] + [""] * 9)
    else:
        for _, p in opens:
            grace = "ON" if p.get("ema9_grace_active") else "OFF"
            note = (p.get("pending_exit_note") or p.get("pending_trim_note") or p.get("ema9_grace_note") or p.get("thesis") or "")[:80]
            rows.append([
                p.get("ticker"),
                int(p.get("shares") or 0),
                float(p.get("entry") or 0),
                float(p.get("stop") or 0),
                float(p.get("mark") or 0),
                float(p.get("unrealized_pnl_usd") or 0),
                float(p.get("r_usd") or 0),
                int(p.get("sessions_held") or 0),
                grace,
                note,
            ])

    rows.append([""] * cols)
    rows.append(["PENDING MOO"] + [""] * 9)
    rows.append(["Ticker", "Action", "Trim sh", "Remain", "BE", "Execute session", "", "", "", ""])
    pending = portfolio.get("pending_market_open") or []
    if not pending:
        rows.append(["(none)"] + [""] * 9)
    else:
        for item in pending:
            rows.append([
                item.get("ticker"),
                item.get("action"),
                item.get("trim_shares"),
                item.get("remain"),
                item.get("be"),
                as_text_date(item.get("session")),
                "", "", "", "",
            ])

    rows.append([""] * cols)
    rows.append(["WORKING LIMITS"] + [""] * 9)
    rows.append(["Ticker", "Limit", "Stop", "Shares", "R$", "Expire", "", "", "", ""])
    if not working:
        rows.append(["(none)"] + [""] * 9)
    else:
        for o in working:
            rows.append([
                o.get("ticker"),
                o.get("limit_price") or o.get("reclaim_level") or "",
                o.get("stop"),
                o.get("shares"),
                o.get("r_usd"),
                o.get("expire") or "",
                "", "", "", "",
            ])

    # Pad wipe zone (clear ghosts of old CLOSED/WATCH blocks)
    target = max(80, len(rows) + 15)
    while len(rows) < target:
        rows.append([""] * cols)
    return rows


def build_dashboard(portfolio, opens, curve_rows, grade_counts, n_stalks, sync_ts):
    """Summary + equity curve only. Logic_Audit rates → Logic_Audit tab;
    Open snapshot → Book/Positions. grade_counts/n_stalks kept for call-site.
    """
    cols = 8
    # Size for curve growth; clear_range A1:H200 wipes old rates/snapshot ghosts
    n_curve = len(curve_rows)
    rows = blank_rows(cols, max(80, 24 + n_curve + 5))
    nav = float(portfolio["equity_mark_usd"])
    cash = float(portfolio["cash_usd"])
    start = float(portfolio.get("equity_start_usd", 100000))
    unreal = float(portfolio.get("unrealized_pnl_usd") or 0)
    realized = float(portfolio.get("realized_pnl_session_usd") or 0)
    r_used = float(portfolio.get("r_used_usd") or 0)
    r_res = float(portfolio.get("r_reserved_usd") or 0)
    invested = round(nav - cash, 2)
    cum_pct = round((nav - start) / start * 100, 4)
    open_n = len(opens)
    # Prefer portfolio.working_orders list; fall back to count if missing
    working_n = len(portfolio.get("working_orders") or [])

    rows[0][0] = "US swing 模擬倉 · Dashboard"
    rows[0][1] = as_text_date(portfolio["marks_session"])
    rows[0][2] = sync_ts

    # Portfolio Summary A3:B16 (canonical summary — only here)
    left = [
        (2, "Portfolio Summary", ""),
        (3, "Equity start", start),
        (4, "NAV", nav),
        (5, "Cash", cash),
        (6, "Invested", invested),
        (7, "Unrealized", unreal),
        (8, "Realized (session)", realized),
        (9, "Cum % vs start", cum_pct),
        (10, "R used", r_used),
        (11, "R reserved", r_res),
        (12, "Open / max", f"{open_n} / {portfolio.get('max_positions', 7)}"),
        (13, "Working", working_n),
        (14, "marks_session", as_text_date(portfolio["marks_session"])),
        (15, "Note", (portfolio.get("note") or "")[:90]),
    ]
    for i, a, b in left:
        rows[i][0] = a
        rows[i][1] = b

    # Equity curve A22+ (charts 1180293779 / 165455414 point here)
    rows[21][0] = "每日淨值走勢表"
    headers = ["日期", "資產淨值 NAV ($)", "累積回報 (%)", "累積 R 數 (R)", "現金 ($)", "開倉數", "備註"]
    for j, h in enumerate(headers):
        rows[22][j] = h
    for i, r in enumerate(curve_rows):
        rr = rows[23 + i]
        rr[0] = as_text_date(r["session"])
        rr[1] = float(r["nav"])
        rr[2] = float(r["cum_pct"])
        rr[3] = float(r["cum_r"])
        rr[4] = float(r["cash"])
        rr[5] = int(r["open_count"])
        rr[6] = r.get("note") or ""

    meta = {
        "curve_header_row": 23,  # 1-based sheet row of header = 23
        "curve_data_start": 24,
        "curve_data_end": 23 + len(curve_rows),  # 1-based inclusive end
        "n_curve": len(curve_rows),
        "open_tickers": [p.get("ticker") for _, p in opens],
    }
    return rows, meta


def build_positions(opens, closeds):
    cols = 12
    rows = []
    rows.append(["OPEN POSITIONS"] + [""] * 11)
    rows.append(["Ticker", "Shares", "Entry", "Stop", "Hard SL", "Mark", "uPnL", "R$", "Notional", "Held", "Grace", "Note"])
    if not opens:
        rows.append(["(none)"] + [""] * 11)
    else:
        for _, p in opens:
            rows.append([
                p.get("ticker"),
                int(p.get("shares") or 0),
                float(p.get("entry") or 0),
                float(p.get("stop") or 0),
                float(p.get("hard_sl") or p.get("stop") or 0),
                float(p.get("mark") or 0),
                float(p.get("unrealized_pnl_usd") or 0),
                float(p.get("r_usd") or 0),
                float(p.get("notional_usd") or 0),
                int(p.get("sessions_held") or 0),
                "ON" if p.get("ema9_grace_active") else "OFF",
                (p.get("pending_exit_note") or p.get("pending_trim_note") or "")[:60],
            ])
    rows.append([""] * cols)
    rows.append(["CLOSED ARCHIVE"] + [""] * 11)
    rows.append(["Ticker", "Exit reason", "Exit px", "Exit sh", "Realized", "Closed session", "Entry", "Held", "Path", "", "", ""])
    closed_sorted = sorted(
        closeds,
        key=lambda x: x[1].get("exit_session") or "",
        reverse=True,
    )
    for path, c in closed_sorted:
        rows.append([
            c.get("ticker"),
            c.get("exit_reason") or "",
            float(c.get("exit_price") or 0),
            int(c.get("exit_shares") or 0),
            float(c.get("realized_pnl_usd") or 0),
            as_text_date(c.get("exit_session") or ""),
            float(c.get("entry") or 0),
            int(c.get("sessions_held") or 0),
            f"closed/{path.name}",
            "", "", "",
        ])
    while len(rows) < 60:
        rows.append([""] * cols)
    return rows


def build_orders(orders):
    cols = 10
    rows = []
    active = [o for _, o in orders if o.get("status") in {"working", "pending_market_open"}]
    archive = [o for _, o in orders if o.get("status") in {"filled", "cancelled", "canceled", "expired"}]

    rows.append(["PENDING + WORKING"] + [""] * 9)
    rows.append(["Ticker", "Status", "Side", "Type", "Limit/Open", "Stop", "Shares", "R$", "Expire/Session", "Note"])
    if not active:
        rows.append(["(none)"] + [""] * 9)
    else:
        for o in active:
            limit = o.get("limit_price")
            if o.get("order_type") == "market_open_sell":
                limit = f"Open {as_text_date(o.get('execute_session') or '')}".replace("'", "").strip()
            rows.append([
                o.get("ticker"),
                o.get("status"),
                o.get("side"),
                o.get("order_type"),
                limit if limit is not None else "",
                o.get("stop_after") or o.get("stop") or "",
                o.get("shares"),
                o.get("r_usd") or 0,
                as_text_date(o.get("execute_session") or "") or (o.get("expire") or ""),
                (o.get("standing_rule") or o.get("source") or "")[:50],
            ])

    rows.append([""] * cols)
    rows.append(["ARCHIVE (filled / cancelled)"] + [""] * 9)
    rows.append(["Ticker", "Status", "Side", "Type", "Limit/Open", "Stop", "Shares", "R$", "Fill/Cancel", "Note"])
    for o in archive:
        rows.append([
            o.get("ticker"),
            o.get("status"),
            o.get("side"),
            o.get("order_type"),
            o.get("limit_price") if o.get("limit_price") is not None else (o.get("fill_price") or ""),
            o.get("stop") or "",
            o.get("shares"),
            o.get("r_usd") or 0,
            as_text_date(o.get("fill_session") or "") or (o.get("filled_hkt") or o.get("cancelled_hkt") or ""),
            (o.get("track_note") or o.get("exit_reason") or "")[:50],
        ])
    while len(rows) < 80:
        rows.append([""] * cols)
    return rows


def build_watchlist(watches, opens, portfolio):
    cols = 6
    rows = []
    rows.append(["Ticker", "Status", "Decision", "Note", "Source", "Updated"])
    # Contract: observe names only (skip open/filled/cancelled mirrors)
    shown = []
    for _, w in watches:
        st = (w.get("status") or "").lower()
        if st in {"observe_only", "observe", "watch"} or w.get("decision") == "SKIP":
            shown.append(w)
    if not shown:
        rows.append(["(none)", "", "", "no observe names", "", ""])
    else:
        for w in shown:
            rows.append([
                w.get("ticker"),
                w.get("status") or "observe",
                w.get("decision") or "",
                (w.get("reason") or w.get("note") or "")[:120],
                (w.get("source") or "").replace("/workspace/", "")[:60],
                w.get("listed_hkt") or "",
            ])
    while len(rows) < 40:
        rows.append([""] * cols)
    return rows


def build_logic_audit(audits):
    cols = 16
    headers = [
        "Ticker", "Grade", "Filled", "Baseline", "Baseline date",
        "T+1%", "T+3%", "T+5%", "MFE%", "MAE%",
        "Last close", "Grade note", "Regime", "Source", "Updated HKT", "Sessions",
    ]
    rows = [headers]
    for _, a in sorted(audits, key=lambda x: x[1].get("date_listed") or ""):
        rows.append([
            a.get("ticker"),
            a.get("grade") or "",
            a.get("filled") or "N",
            a.get("baseline_close") if a.get("baseline_close") is not None else "",
            as_text_date(a.get("baseline_date") or ""),
            a.get("t1_return_pct") if a.get("t1_return_pct") is not None else "",
            a.get("t3_return_pct") if a.get("t3_return_pct") is not None else "",
            a.get("t5_return_pct") if a.get("t5_return_pct") is not None else "",
            a.get("mfe_pct") if a.get("mfe_pct") is not None else "",
            a.get("mae_pct") if a.get("mae_pct") is not None else "",
            a.get("last_close") if a.get("last_close") is not None else "",
            (a.get("grade_note") or "")[:80],
            (a.get("regime_note") or "")[:40],
            (a.get("source_path") or "").replace("/workspace/", "")[:50],
            a.get("updated_hkt") or "",
            a.get("sessions_tracked") if a.get("sessions_tracked") is not None else "",
        ])
    while len(rows) < 40:
        rows.append([""] * cols)
    return rows


def grade_stats(audits):
    stats = {g: {"count": 0, "y": 0, "n": 0} for g in GRADES}
    for _, a in audits:
        g = a.get("grade") or "追蹤中"
        if g not in stats:
            stats[g] = {"count": 0, "y": 0, "n": 0}
        stats[g]["count"] += 1
        if (a.get("filled") or "N").upper() == "Y":
            stats[g]["y"] += 1
        else:
            stats[g]["n"] += 1
    return stats, len(audits)


def write_payload(name: str, values: list):
    PAYLOAD.mkdir(parents=True, exist_ok=True)
    path = PAYLOAD / f"{name}.json"
    path.write_text(json.dumps(values, ensure_ascii=False, indent=2) + "\n")
    return path


MANAGED_CLEAR_RANGES = [
    {"sheet": "Book", "cells": "A1:L200"},
    {"sheet": "Dashboard", "cells": "A1:H200"},
    {"sheet": "Positions", "cells": "A1:L100"},
    {"sheet": "Orders", "cells": "A1:L120"},
    {"sheet": "Watchlist", "cells": "A1:L80"},
    {"sheet": "Logic_Audit", "cells": "A1:R80"},
]

WRITE_TABS = (
    ("Book", "book_write.json"),
    ("Dashboard", "dashboard_write.json"),
    ("Positions", "positions_write.json"),
    ("Orders", "orders_write.json"),
    ("Watchlist", "watchlist_write.json"),
    ("Logic_Audit", "logic_audit_write.json"),
)


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Rebuild Sheet payloads from ledger (safe-sync-v1). No Sheets API."
    )
    g = p.add_mutually_exclusive_group()
    g.add_argument(
        "--strict",
        dest="strict",
        action="store_true",
        default=True,
        help="Exit 1 if portfolio.open_tickers != open files in positions/ (default).",
    )
    g.add_argument(
        "--no-strict",
        dest="strict",
        action="store_false",
        help="Warn-only on open_tickers mismatch.",
    )
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    sync_ts = now_hkt()
    portfolio = load_json(ROOT / "state" / "portfolio.json")

    opens_all = glob_json(ROOT / "positions")
    opens = [(p, d) for p, d in opens_all if (d.get("status") or "open") == "open"]
    # Safety: only trust positions/ folder for open
    opens.sort(key=lambda x: x[1].get("ticker") or "")

    closeds = glob_json(ROOT / "closed")
    orders = glob_json(ROOT / "orders")
    watches = glob_json(ROOT / "watchlist")
    audits = glob_json(ROOT / "logic-audit")

    # Align open_tickers with files
    file_tickers = [d.get("ticker") for _, d in opens]
    port_tickers = list(portfolio.get("open_tickers") or [])
    mismatch = sorted(file_tickers) != sorted(port_tickers)
    if mismatch:
        msg = (
            f"portfolio.open_tickers != positions/ open files: "
            f"{port_tickers} vs {file_tickers}"
        )
        if args.strict:
            print(f"STRICT FAIL: {msg}", file=sys.stderr)
            sys.exit(1)
        print(f"WARN: {msg}", file=sys.stderr)

    curve_rows = upsert_equity_curve(portfolio)
    gstats, n_stalks = grade_stats(audits)

    book = build_book(portfolio, opens, closeds, orders, watches, sync_ts)
    dash, dash_meta = build_dashboard(portfolio, opens, curve_rows, gstats, n_stalks, sync_ts)
    positions = build_positions(opens, closeds)
    orders_tab = build_orders(orders)
    watchlist = build_watchlist(watches, opens, portfolio)
    logic = build_logic_audit(audits)

    write_payload("book", book)
    write_payload("dashboard", dash)
    write_payload("positions", positions)
    write_payload("orders", orders_tab)
    write_payload("watchlist", watchlist)
    write_payload("logic_audit", logic)

    # Trimmed write payloads FIRST so apply_plan can point at *_write.json
    for name in ("book", "dashboard", "positions", "orders", "watchlist", "logic_audit"):
        rows = load_json(PAYLOAD / f"{name}.json")

        def _nonempty(r):
            return any(c != "" and c is not None for c in r)

        last = max((i for i, r in enumerate(rows) if _nonempty(r)), default=0)
        trimmed = rows[: last + 1 + 3]
        (PAYLOAD / f"{name}_write.json").write_text(
            json.dumps(trimmed, ensure_ascii=False) + "\n"
        )

    working_tickers = [o.get("ticker") for _, o in orders if o.get("status") == "working"]

    # safe-sync-v1: ONE batch clear of all managed tabs, then writes, then polish
    steps = [
        {
            "op": "batch_clear_values",
            "ranges": [f"{r['sheet']}!{r['cells']}" for r in MANAGED_CLEAR_RANGES],
            "note": "Single conceptual clear of all managed tabs. Journal excluded.",
        },
    ]
    for sheet, payload in WRITE_TABS:
        steps.append(
            {
                "op": "write_range",
                "sheet": sheet,
                "cells": "A1",
                "payload": payload,
                "parseInput": True,
            }
        )
    steps.extend(
        [
            {
                "op": "update_chart",
                "chartId": 1180293779,
                "sheetId": SHEET_IDS["Dashboard"],
                "chartType": "LINE",
                "title": "紙倉淨值成長曲線 vs 起算",
                "ranges": [
                    {"cells": f"A23:A{dash_meta['curve_data_end']}"},
                    {"cells": f"B23:B{dash_meta['curve_data_end']}"},
                ],
                "headerCount": 1,
            },
            {
                "op": "update_chart",
                "chartId": 165455414,
                "sheetId": SHEET_IDS["Dashboard"],
                "chartType": "LINE",
                "title": "累積回報 %",
                "ranges": [
                    {"cells": f"A23:A{dash_meta['curve_data_end']}"},
                    {"cells": f"C23:C{dash_meta['curve_data_end']}"},
                ],
                "headerCount": 1,
            },
            {"op": "freeze", "sheet": "Book", "sheetId": SHEET_IDS["Book"], "frozenRowCount": 1},
            {"op": "freeze", "sheet": "Dashboard", "sheetId": SHEET_IDS["Dashboard"], "frozenRowCount": 1},
            {"op": "freeze", "sheet": "Logic_Audit", "sheetId": SHEET_IDS["Logic_Audit"], "frozenRowCount": 1},
            {"op": "format_header", "sheetId": SHEET_IDS["Book"], "cells": "A1:J1", "bold": True, "fontSize": 12},
            {"op": "format_header", "sheetId": SHEET_IDS["Dashboard"], "cells": "A1:C1", "bold": True, "fontSize": 12},
            {
                "op": "set_column_width",
                "sheet": "Book",
                "sheetId": SHEET_IDS["Book"],
                "dimension": "COLUMNS",
                "position": 1,
                "count": 10,
                "pixelSize": 110,
            },
            {
                "op": "set_column_width",
                "sheet": "Dashboard",
                "sheetId": SHEET_IDS["Dashboard"],
                "dimension": "COLUMNS",
                "position": 1,
                "count": 7,
                "pixelSize": 130,
            },
        ]
    )

    apply_plan = {
        "protocol": "safe-sync-v1",
        "rules": [
            "never_hand_patch_cells",
            "journal_leave_alone",
            "verify_required",
        ],
        "spreadsheetId": SPREADSHEET_ID,
        "sync_hkt": sync_ts,
        "marks_session": portfolio["marks_session"],
        "nav": portfolio["equity_mark_usd"],
        "open_tickers": file_tickers,
        "sheet_ids": SHEET_IDS,
        "dashboard_meta": dash_meta,
        "journal": "LEAVE_ALONE",
        "managed_clear_ranges": MANAGED_CLEAR_RANGES,
        "steps": steps,
        "verify": {
            "nav": portfolio["equity_mark_usd"],
            "cash": portfolio["cash_usd"],
            "marks_session": portfolio["marks_session"],
            "open_tickers": file_tickers,
            "working": working_tickers,
            "must_not_appear_in_open": ["AUGO", "DK"],
            "book_must_not_contain": ["CLOSED (recent)", "WATCH", "Account"],
            "dashboard_must_not_contain": ["Logic_Audit rates", "Open snapshot"],
        },
    }
    write_payload("apply_plan", apply_plan)

    summary = {
        "protocol": "safe-sync-v1",
        "strict": args.strict,
        "sync_hkt": sync_ts,
        "nav": portfolio["equity_mark_usd"],
        "cash": portfolio["cash_usd"],
        "marks_session": portfolio["marks_session"],
        "open": file_tickers,
        "closed": [d.get("ticker") for _, d in closeds],
        "pending_moo": portfolio.get("pending_market_open"),
        "working": working_tickers,
        "n_stalks": n_stalks,
        "grade_counts": {k: v["count"] for k, v in gstats.items()},
        "curve_rows": len(curve_rows),
        "payload_dir": str(PAYLOAD),
        "apply_plan": str(PAYLOAD / "apply_plan.json"),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


if __name__ == "__main__":
    main()
