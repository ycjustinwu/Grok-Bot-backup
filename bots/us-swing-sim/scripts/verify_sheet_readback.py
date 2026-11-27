#!/usr/bin/env python3
"""Verify Google Sheet readback against apply_plan.verify (safe-sync-v1).

Exit 0 + PASS JSON on success; exit 1 + FAIL reasons on failure.

Readback JSON schema (sheet-readback-done-v1)::

    {
      "dashboard": {
        "NAV": 100073.9,
        "cash": 72709.17,
        "Open": "2 / 7",          # or open ticker list
        "Working": 3,             # or working ticker list
        "marks_session": "2026-11-06",
        "raw_A1H20": "optional concatenated cells"
      },
      "book": {
        "raw_A1J40": "optional concatenated cells"
      },
      "positions_open": ["TEM", "UNTY"],
      "orders_working": ["CRL", "DNA", "EL"]
    }

Also accepts legacy dedupe readback shape under numbers/open_tickers/working_tickers.

Modes:
  --expect PATH     apply_plan.json (default .sheet_payloads/apply_plan.json)
  --readback PATH   agent-written readback after MCP reads
  --from-ledger     smoke: build expected from portfolio.json + orders/ (no Sheet)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path("/workspace/us-swing-sim")
DEFAULT_EXPECT = ROOT / ".sheet_payloads" / "apply_plan.json"
TOL = 0.05
SKIP_NAMES = {"FORMAT.md", "_TEMPLATE.json", "_index.json"}


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


def as_float(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace(",", "").replace("$", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


def as_ticker_set(v) -> set[str]:
    if v is None:
        return set()
    if isinstance(v, (list, tuple, set)):
        return {str(x).strip().upper() for x in v if str(x).strip()}
    s = str(v).strip()
    if not s:
        return set()
    # "2 / 7" or "2/7" → empty set (count only); tickers come elsewhere
    if re.fullmatch(r"\d+\s*/\s*\d+", s):
        return set()
    if re.fullmatch(r"\d+", s):
        return set()
    parts = re.split(r"[,|\s]+", s)
    return {p.strip().upper() for p in parts if p.strip() and not p.strip().isdigit()}


def near(a, b, tol=TOL) -> bool:
    fa, fb = as_float(a), as_float(b)
    if fa is None or fb is None:
        return False
    return abs(fa - fb) <= tol


def expect_from_ledger() -> dict:
    portfolio = load_json(ROOT / "state" / "portfolio.json")
    opens = [
        d
        for _, d in glob_json(ROOT / "positions")
        if (d.get("status") or "open") == "open"
    ]
    file_tickers = sorted(d.get("ticker") for d in opens)
    working = sorted(
        o.get("ticker")
        for _, o in glob_json(ROOT / "orders")
        if o.get("status") == "working"
    )
    return {
        "protocol": "safe-sync-v1",
        "from_ledger": True,
        "verify": {
            "nav": portfolio["equity_mark_usd"],
            "cash": portfolio["cash_usd"],
            "marks_session": portfolio["marks_session"],
            "open_tickers": file_tickers,
            "working": working,
            "must_not_appear_in_open": ["AUGO", "DK"],
            "book_must_not_contain": ["CLOSED (recent)", "WATCH", "Account"],
            "dashboard_must_not_contain": ["Logic_Audit rates", "Open snapshot"],
        },
    }


def normalize_readback(rb: dict) -> dict:
    """Accept both sheet-readback-done-v1 and legacy dedupe shape."""
    if "dashboard" in rb or "positions_open" in rb or "orders_working" in rb:
        dash = rb.get("dashboard") or {}
        return {
            "nav": dash.get("NAV", dash.get("nav")),
            "cash": dash.get("cash"),
            "marks_session": dash.get("marks_session"),
            "open_tickers": rb.get("positions_open")
            or as_ticker_set(dash.get("Open"))
            or [],
            "working": rb.get("orders_working")
            or as_ticker_set(dash.get("Working"))
            or [],
            "book_raw": (rb.get("book") or {}).get("raw_A1J40") or "",
            "dashboard_raw": dash.get("raw_A1H20") or "",
        }

    # Legacy: numbers + open_tickers + working_tickers
    nums = rb.get("numbers") or {}
    return {
        "nav": nums.get("nav"),
        "cash": nums.get("cash"),
        "marks_session": nums.get("marks_session"),
        "open_tickers": nums.get("open_tickers") or rb.get("open_tickers") or [],
        "working": nums.get("working_tickers") or rb.get("working_tickers") or [],
        "book_raw": rb.get("book_raw") or "",
        "dashboard_raw": rb.get("dashboard_raw") or "",
    }


def verify(expect: dict, readback: dict) -> dict:
    v = expect.get("verify") or expect
    got = normalize_readback(readback)
    fails = []

    if not near(got["nav"], v.get("nav")):
        fails.append(f"NAV mismatch: got {got['nav']} expect {v.get('nav')} (tol {TOL})")
    if not near(got["cash"], v.get("cash")):
        fails.append(f"cash mismatch: got {got['cash']} expect {v.get('cash')} (tol {TOL})")

    exp_open = {str(x).upper() for x in (v.get("open_tickers") or [])}
    got_open = {str(x).upper() for x in as_ticker_set(got["open_tickers"])}
    # if got_open empty but positions_open was a count-only Open string, try list from expect path
    if isinstance(got["open_tickers"], list):
        got_open = {str(x).upper() for x in got["open_tickers"] if x}
    if got_open != exp_open:
        fails.append(f"open_tickers set mismatch: got {sorted(got_open)} expect {sorted(exp_open)}")

    exp_w = {str(x).upper() for x in (v.get("working") or [])}
    if isinstance(got["working"], list):
        got_w = {str(x).upper() for x in got["working"] if x}
    else:
        got_w = as_ticker_set(got["working"])
    if got_w != exp_w:
        fails.append(f"working set mismatch: got {sorted(got_w)} expect {sorted(exp_w)}")

    banned_open = {str(x).upper() for x in (v.get("must_not_appear_in_open") or [])}
    bad = sorted(got_open & banned_open)
    if bad:
        fails.append(f"must_not_appear_in_open present: {bad}")

    book_raw = got.get("book_raw") or ""
    if book_raw:
        for needle in v.get("book_must_not_contain") or []:
            if needle and needle in book_raw:
                fails.append(f"book_must_not_contain hit: {needle!r}")

    dash_raw = got.get("dashboard_raw") or ""
    if dash_raw:
        for needle in v.get("dashboard_must_not_contain") or []:
            if needle and needle in dash_raw:
                fails.append(f"dashboard_must_not_contain hit: {needle!r}")

    # Optional marks_session check when present on both sides
    exp_ms = v.get("marks_session")
    got_ms = got.get("marks_session")
    if exp_ms and got_ms:
        exp_s = str(exp_ms).lstrip("'")[:10]
        got_s = str(got_ms).lstrip("'")[:10]
        if exp_s != got_s:
            fails.append(f"marks_session mismatch: got {got_ms} expect {exp_ms}")

    ok = not fails
    return {
        "result": "PASS" if ok else "FAIL",
        "protocol": expect.get("protocol") or "safe-sync-v1",
        "nav": got.get("nav"),
        "cash": got.get("cash"),
        "open": sorted(got_open),
        "working": sorted(got_w),
        "fails": fails,
    }


def build_ledger_smoke_readback(expect: dict) -> dict:
    """Synthetic readback that mirrors ledger — for --from-ledger smoke only."""
    v = expect["verify"]
    return {
        "dashboard": {
            "NAV": v["nav"],
            "cash": v["cash"],
            "Open": f"{len(v['open_tickers'])} / 7",
            "Working": len(v["working"]),
            "marks_session": v["marks_session"],
            "raw_A1H20": "Portfolio Summary NAV Cash Invested",
        },
        "book": {
            "raw_A1J40": "OPEN PENDING MOO WORKING LIMITS",
        },
        "positions_open": list(v["open_tickers"]),
        "orders_working": list(v["working"]),
    }


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Verify Sheet readback (safe-sync-v1).")
    p.add_argument(
        "--expect",
        default=str(DEFAULT_EXPECT),
        help="Path to apply_plan.json (default .sheet_payloads/apply_plan.json)",
    )
    p.add_argument(
        "--readback",
        default="",
        help="Path to agent readback JSON after MCP reads",
    )
    p.add_argument(
        "--from-ledger",
        action="store_true",
        help="Smoke: build expected from portfolio.json + orders/; verify synthetic self-readback",
    )
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if args.from_ledger:
        expect = expect_from_ledger()
        readback = build_ledger_smoke_readback(expect)
        # Also enforce portfolio.open_tickers == positions files
        port = load_json(ROOT / "state" / "portfolio.json")
        if sorted(port.get("open_tickers") or []) != sorted(expect["verify"]["open_tickers"]):
            out = {
                "result": "FAIL",
                "protocol": "safe-sync-v1",
                "fails": [
                    "portfolio.open_tickers != positions/ open files: "
                    f"{port.get('open_tickers')} vs {expect['verify']['open_tickers']}"
                ],
            }
            print(json.dumps(out, ensure_ascii=False, indent=2))
            sys.exit(1)
    else:
        if not args.readback:
            print("FAIL: --readback PATH required unless --from-ledger", file=sys.stderr)
            sys.exit(1)
        expect_path = Path(args.expect)
        rb_path = Path(args.readback)
        if not expect_path.exists():
            print(f"FAIL: expect not found: {expect_path}", file=sys.stderr)
            sys.exit(1)
        if not rb_path.exists():
            print(f"FAIL: readback not found: {rb_path}", file=sys.stderr)
            sys.exit(1)
        expect = load_json(expect_path)
        readback = load_json(rb_path)

    out = verify(expect, readback)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["result"] == "PASS" else 1)


if __name__ == "__main__":
    main()
