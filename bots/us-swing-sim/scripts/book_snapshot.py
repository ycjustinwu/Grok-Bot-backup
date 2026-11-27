#!/usr/bin/env python3
"""Print US swing sim book crowding header + JSON snapshot (local SoT)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path("/workspace/us-swing-sim")
PORTFOLIO = ROOT / "state" / "portfolio.json"
STALKS = ROOT / "state" / "stalks.json"


def load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def snapshot(portfolio_path: Path = PORTFOLIO, stalks_path: Path = STALKS) -> dict:
    pf = load_json(portfolio_path)
    st = load_json(stalks_path)

    open_tickers = pf.get("open_tickers") or st.get("open") or st.get("open_positions") or []
    working = pf.get("working_orders") or st.get("working") or st.get("working_orders") or []
    observe = st.get("observe") if "observe" in st else pf.get("observe", [])
    n_open = len(open_tickers)
    max_pos = int(pf.get("max_positions") or 7)
    cash = float(pf.get("cash_usd") or 0)
    nav = float(pf.get("equity_mark_usd") or pf.get("nav_usd") or 0)
    r_reserved = float(pf.get("r_reserved_usd") or 0)
    r_used = float(pf.get("r_used_usd") or 0)
    working_notional = float(pf.get("working_notional_usd") or 0)

    header = (
        f"OPEN {n_open}/{max_pos} · cash {cash:.2f} · R reserved {r_reserved:.2f} "
        f"· working notional {working_notional:.2f} · R used {r_used:.2f} · NAV {nav:.2f}"
    )

    return {
        "header": header,
        "OPEN": f"{n_open}/{max_pos}",
        "open_n": n_open,
        "max_positions": max_pos,
        "cash": cash,
        "nav": nav,
        "r_reserved": r_reserved,
        "r_used": r_used,
        "working_notional": working_notional,
        "open_tickers": list(open_tickers),
        "working_orders": list(working),
        "observe": list(observe or []),
        "pending_market_open": pf.get("pending_market_open") or [],
        "marks_session": pf.get("marks_session") or st.get("marks_session"),
        "updated_hkt": pf.get("updated_hkt"),
        "last_open_skip_tc": pf.get("last_open_skip_tc"),
        "portfolio_path": str(portfolio_path),
        "stalks_path": str(stalks_path) if stalks_path.is_file() else None,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Book crowding snapshot")
    p.add_argument("--portfolio", default=str(PORTFOLIO))
    p.add_argument("--stalks", default=str(STALKS))
    p.add_argument("--json-only", action="store_true", help="Omit human header line on stdout")
    args = p.parse_args(argv)

    out = snapshot(Path(args.portfolio), Path(args.stalks))
    if not args.json_only:
        print(out["header"])
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
