#!/usr/bin/env python3
"""Risk=R position sizing for US swing paper book (skill math verbatim).

Hermes §3.4 UNTY acceptance (FULL size, thin_room OFF):
  entry 58.10 stop 56.654 → stop%≈0.0249 R$≈497.76 shares 344

Note: AUTHORIZE may tag thin_room for honesty while still using FULL size
when Room_To_Supply_R > 1.5. Pass --thin-room only when Room is in 1.0–1.5
(or Justin forces half). Default OFF so acceptance stays 344.
"""
from __future__ import annotations

import argparse
import json
import math
import sys


def size_position(
    entry: float,
    stop: float,
    equity: float = 100_000.0,
    thin_room: bool = False,
    paper_probe_r: float = 1.0,
) -> dict:
    if entry <= 0:
        raise ValueError("entry must be > 0")
    risk_ps = abs(entry - stop)
    if risk_ps <= 0:
        raise ValueError("entry and stop must differ")
    if equity <= 0:
        raise ValueError("equity must be > 0")
    if paper_probe_r <= 0:
        raise ValueError("paper_probe_r must be > 0")

    stop_pct = risk_ps / entry
    r_usd = min(0.01 * equity, 0.20 * equity * stop_pct)
    if paper_probe_r < 1.0:
        r_usd *= paper_probe_r

    shares = math.floor(r_usd / risk_ps)
    tags: list[str] = []

    if thin_room:
        shares = math.floor(shares / 2)
        tags.append("thin_room")

    if paper_probe_r < 1.0:
        tags.append("paper_probe")

    notional = shares * entry
    cap = 0.20 * equity
    if notional > cap and entry > 0:
        shares = math.floor(cap / entry)
        notional = shares * entry
        tags.append("notional_cap_20pct")

    effective_r = shares * risk_ps

    return {
        "entry": entry,
        "stop": stop,
        "equity": equity,
        "stop_pct": stop_pct,
        "r_usd": r_usd,
        "shares": int(shares),
        "notional": notional,
        "effective_r": effective_r,
        "risk_per_share": risk_ps,
        "paper_probe_r": paper_probe_r,
        "thin_room": thin_room,
        "tags": tags,
    }


def _self_test() -> int:
    """UNTY Hermes §3.4 acceptance: full size, no thin_room half."""
    out = size_position(58.10, 56.654, equity=100_000.0, thin_room=False)
    ok = True
    errs: list[str] = []
    if out["shares"] != 344:
        ok = False
        errs.append(f"shares={out['shares']} want 344")
    if abs(out["r_usd"] - 497.76) > 0.5:
        ok = False
        errs.append(f"r_usd={out['r_usd']} want ≈497.76 (±0.5)")
    if "thin_room" in out["tags"]:
        ok = False
        errs.append("thin_room tag present with thin_room=False")

    # thin_room halves after base
    half = size_position(58.10, 56.654, thin_room=True)
    if half["shares"] != 172:
        ok = False
        errs.append(f"thin_room shares={half['shares']} want 172")
    if "thin_room" not in half["tags"]:
        ok = False
        errs.append("thin_room tag missing")

    # paper_probe_r < 1 scales R$
    probe = size_position(58.10, 56.654, paper_probe_r=0.5)
    if abs(probe["r_usd"] - out["r_usd"] * 0.5) > 1e-9:
        ok = False
        errs.append(f"paper_probe_r scale fail: {probe['r_usd']}")
    if probe["shares"] != 172:
        ok = False
        errs.append(f"paper_probe shares={probe['shares']} want 172")

    if ok:
        print(
            json.dumps(
                {
                    "self_test": "PASS",
                    "unty": {
                        "shares": out["shares"],
                        "r_usd": round(out["r_usd"], 4),
                        "stop_pct": round(out["stop_pct"], 6),
                        "notional": out["notional"],
                        "effective_r": round(out["effective_r"], 4),
                    },
                    "thin_room_half_shares": half["shares"],
                    "paper_probe_0.5_shares": probe["shares"],
                },
                ensure_ascii=False,
            )
        )
        return 0
    print(json.dumps({"self_test": "FAIL", "errors": errs}, ensure_ascii=False), file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="US swing sim Risk=R sizing")
    p.add_argument("--entry", type=float, help="Entry / max fill")
    p.add_argument("--stop", type=float, help="Stop / Invalidate_Below")
    p.add_argument("--equity", type=float, default=100_000.0)
    p.add_argument(
        "--thin-room",
        action="store_true",
        help="Half size after base (Room 1.0–1.5). Default OFF (UNTY acceptance 344).",
    )
    p.add_argument(
        "--paper-probe-r",
        type=float,
        default=1.0,
        help="If <1, scale R$ by this factor before share floor (default 1.0).",
    )
    p.add_argument("--json", action="store_true", help="Print JSON (default always JSON)")
    p.add_argument("--self-test", action="store_true", help="Run UNTY acceptance + thin/probe checks")
    args = p.parse_args(argv)

    if args.self_test:
        return _self_test()

    if args.entry is None or args.stop is None:
        p.error("--entry and --stop required (or use --self-test)")

    try:
        out = size_position(
            entry=args.entry,
            stop=args.stop,
            equity=args.equity,
            thin_room=args.thin_room,
            paper_probe_r=args.paper_probe_r,
        )
    except ValueError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        return 2

    # Stable JSON for agents
    printable = {
        "entry": out["entry"],
        "stop": out["stop"],
        "stop_pct": out["stop_pct"],
        "r_usd": out["r_usd"],
        "shares": out["shares"],
        "notional": out["notional"],
        "tags": out["tags"],
        "effective_r": out["effective_r"],
        "equity": out["equity"],
        "paper_probe_r": out["paper_probe_r"],
        "thin_room": out["thin_room"],
        "risk_per_share": out["risk_per_share"],
    }
    print(json.dumps(printable, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
