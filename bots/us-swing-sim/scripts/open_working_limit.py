#!/usr/bin/env python3
"""Place / refresh a working limit_buy in the US swing paper ledger (local files).

Writes:
  orders/<T>.json
  state/portfolio.json  (working_orders, r_reserved, working_notional, note)
  state/stalks.json     (working list + skip/open notes)
  journal/YYYY-MM-DD.md append line

Idempotent: same ticker already working with same limit_price → no double-reserve.
--dry-run prints planned writes only.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("/workspace/us-swing-sim")
HKT = ZoneInfo("Asia/Hong_Kong")


def now_hkt() -> str:
    return datetime.now(HKT).strftime("%Y-%m-%d %H:%M HKT")


def today_hkt() -> str:
    return datetime.now(HKT).strftime("%Y-%m-%d")


def load(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_order(args: argparse.Namespace) -> dict:
    notional = args.shares * args.limit
    stop_pct = abs(args.limit - args.stop) / args.limit if args.limit else 0.0
    tags = []
    if args.paper_probe:
        tags.append("paper_probe")
    structure = {}
    if args.soft_supply is not None:
        structure["soft_supply"] = args.soft_supply
    if args.hard_room is not None:
        structure["hard_room_level"] = args.hard_room
    order = {
        "ticker": args.ticker.upper(),
        "status": "working",
        "side": "buy",
        "order_type": "limit_buy",
        "limit_price": args.limit,
        "stop": args.stop,
        "shares": int(args.shares),
        "r_usd": float(args.r_usd),
        "stop_pct": stop_pct,
        "notional_usd": notional,
        "paper_probe": bool(args.paper_probe),
        "trigger": (
            f"Session low <= {args.limit} → fill @ min({args.limit}, better Open) "
            "per better-price-v1; max fill = limit; do not chase"
        ),
        "invalidation": f"Session close < {args.stop} OR leave zone / thesis dead / max_stalk_sessions",
        "expire": "max_stalk_sessions=5 OR thesis dead OR earnings−1",
        "max_stalk_sessions": 5,
        "stalk_sessions_elapsed": 0,
        "tags": tags,
        "structure_notes": structure or None,
        "source": args.source,
        "tc_id": args.tc,
        "placed_hkt": now_hkt(),
        "updated_hkt": now_hkt(),
        "fill_rule": "limit-single-price-v1 + better-price-v1",
        "concrete_plan_rule": "concrete-plan-v1",
    }
    # drop null structure
    if order["structure_notes"] is None:
        del order["structure_notes"]
    return order


def apply(args: argparse.Namespace) -> dict:
    ticker = args.ticker.upper()
    order_path = ROOT / "orders" / f"{ticker}.json"
    portfolio_path = ROOT / "state" / "portfolio.json"
    stalks_path = ROOT / "state" / "stalks.json"
    journal_path = ROOT / "journal" / f"{today_hkt()}.md"

    pf = load(portfolio_path)
    st = load(stalks_path)
    existing = load(order_path) if order_path.is_file() else None

    new_order = build_order(args)
    notional = new_order["notional_usd"]
    r_usd = float(args.r_usd)

    # Idempotent: same ticker working + same limit → no double-reserve
    same = (
        existing
        and existing.get("status") == "working"
        and float(existing.get("limit_price", -1)) == float(args.limit)
        and int(existing.get("shares", -1)) == int(args.shares)
        and ticker in (pf.get("working_orders") or [])
    )

    planned = {
        "order_path": str(order_path),
        "order": new_order,
        "idempotent_skip_reserve": bool(same),
        "portfolio_delta": {},
        "stalks_delta": {},
        "journal_line": "",
    }

    working = list(pf.get("working_orders") or [])
    stalk_tickers = list(pf.get("stalk_tickers") or [])
    r_reserved = float(pf.get("r_reserved_usd") or 0)
    working_notional = float(pf.get("working_notional_usd") or 0)

    if same:
        planned["portfolio_delta"] = {
            "note": "idempotent — same working limit/shares; no r_reserved change",
            "r_reserved_usd": r_reserved,
            "working_notional_usd": working_notional,
        }
    else:
        # If replacing different working on same ticker, free prior reserve first
        if existing and existing.get("status") == "working" and ticker in working:
            prev_r = float(existing.get("r_usd") or 0)
            prev_n = float(existing.get("notional_usd") or 0)
            r_reserved = max(0.0, r_reserved - prev_r)
            working_notional = max(0.0, working_notional - prev_n)
        if ticker not in working:
            working.append(ticker)
        if ticker not in stalk_tickers:
            stalk_tickers.append(ticker)
        r_reserved += r_usd
        working_notional += notional
        planned["portfolio_delta"] = {
            "working_orders": working,
            "stalk_tickers": stalk_tickers,
            "r_reserved_usd": r_reserved,
            "working_notional_usd": working_notional,
            "last_open_skip_tc": args.tc,
            "updated_hkt": now_hkt(),
            "note": f"{args.tc} OPEN working {ticker} L{args.limit}/{args.shares}sh/SL{args.stop} R${r_usd}",
        }

    st_working = list(st.get("working") or st.get("working_orders") or [])
    if ticker not in st_working:
        st_working.append(ticker)
    skip_notes = dict(st.get("skip_notes") or {})
    if args.tc:
        skip_notes[args.tc] = skip_notes.get(args.tc) or f"OPEN working {ticker}"
    planned["stalks_delta"] = {
        "working": st_working,
        "working_orders": st_working,
        "skip_notes": skip_notes,
        "tc_id": args.tc,
        "updated_hkt": now_hkt(),
        "note": f"{args.tc} OPEN working {ticker}",
    }
    planned["journal_line"] = (
        f"- {now_hkt()} · {args.tc} · **OPEN working {ticker}** "
        f"L{args.limit} / SL{args.stop} / {args.shares}sh / R${r_usd}"
        + (" · dry-run" if args.dry_run else "")
    )

    if args.dry_run:
        planned["dry_run"] = True
        return planned

    # Writes
    dump(order_path, new_order)
    if not same:
        pf.update(planned["portfolio_delta"])
        pf["working_orders"] = working
        pf["stalk_tickers"] = stalk_tickers
        dump(portfolio_path, pf)
    st.update(planned["stalks_delta"])
    dump(stalks_path, st)

    journal_path.parent.mkdir(parents=True, exist_ok=True)
    if not journal_path.is_file():
        journal_path.write_text(
            f"# Journal {today_hkt()} (Asia/Hong_Kong)\n\n", encoding="utf-8"
        )
    with journal_path.open("a", encoding="utf-8") as f:
        f.write(planned["journal_line"] + "\n")

    planned["written"] = True
    return planned


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Open working limit_buy in paper ledger")
    p.add_argument("--ticker", required=True)
    p.add_argument("--limit", type=float, required=True)
    p.add_argument("--stop", type=float, required=True)
    p.add_argument("--shares", type=int, required=True)
    p.add_argument("--r-usd", type=float, required=True)
    p.add_argument("--soft-supply", type=float, default=None)
    p.add_argument("--hard-room", type=float, default=None)
    p.add_argument("--paper-probe", action="store_true")
    p.add_argument("--source", default="")
    p.add_argument("--tc", default="")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    if args.limit <= 0 or args.shares <= 0:
        print(json.dumps({"error": "limit/shares must be > 0"}), file=sys.stderr)
        return 2

    out = apply(args)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
