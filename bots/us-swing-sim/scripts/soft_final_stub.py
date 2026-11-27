#!/usr/bin/env python3
"""Write a short Soft Final markdown skeleton from a decision JSON.

Does NOT call WV. Banned tokens never written: RR_ Target_ Setup_Type Adjusted_Stop
(and Hermes-deleted underscore field names). Agent fills narrative; script owns structure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

HKT = ZoneInfo("Asia/Hong_Kong")
BANNED = re.compile(
    r"\b(RR_|Target_|Setup_Type|Adjusted_Stop|Risk_Reward|AdjRR)\b",
    re.IGNORECASE,
)


def now_hkt() -> str:
    return datetime.now(HKT).strftime("%Y-%m-%d %H:%M HKT")


def md5_file(path: Path) -> str:
    h = hashlib.md5()
    h.update(path.read_bytes())
    return h.hexdigest()


def render(tc_id: str, decision: dict) -> str:
    header = decision.get("header") or decision.get("crowding_header") or ""
    regime = decision.get("regime_ref") or decision.get("regime") or "(fill)"
    upstream = decision.get("upstream") or decision.get("authorize_note") or ""
    decisions = decision.get("decisions") or decision.get("lines") or []
    pinned = decision.get("pinned") or []
    open_q = decision.get("open_questions") or []
    book_after = decision.get("book_after") or {}
    hermes_gate = decision.get("hermes_gate") or {}
    script_rung = decision.get("script_rung") or "Script"
    ran = decision.get("ran_hkt") or now_hkt()

    lines: list[str] = []
    lines.append(f"# Soft Final — {tc_id} (open/skip)")
    if header:
        lines.append(f"**Header crowding:** {header}")
    lines.append(f"**Ran:** {ran} (Asia/Hong_Kong)")
    if upstream:
        lines.append(f"**Upstream:** {upstream}")
    lines.append(f"**Regime ref (do NOT rescore):** {regime}")
    lines.append("**WV:** skip (fleet) → Soft Final = Final (self-VERIFY)")
    lines.append(f"**script-first rung:** **{script_rung}**")
    lines.append("")

    if pinned:
        lines.append("## PINNED_INPUTS")
        lines.append("| Artifact | Path / id | md5 / note |")
        lines.append("|----------|-----------|------------|")
        for row in pinned:
            if isinstance(row, dict):
                lines.append(
                    f"| {row.get('name','')} | {row.get('path','')} | {row.get('md5','')} |"
                )
            else:
                lines.append(f"| | {row} | |")
        lines.append("")

    if hermes_gate:
        lines.append("## Hermes gate")
        lines.append(f"- gate: **{hermes_gate.get('gate', '')}**")
        for w in hermes_gate.get("warnings") or []:
            lines.append(f"- warning: {w}")
        for r in hermes_gate.get("reasons") or []:
            lines.append(f"- reason: {r}")
        lines.append("")

    lines.append("## DECISIONS_MADE")
    lines.append("| Ticker | Decision | L / SL / sh / R$ | paper_probe | Reason |")
    lines.append("|--------|----------|------------------|-------------|--------|")
    for d in decisions:
        if not isinstance(d, dict):
            continue
        ticker = d.get("ticker", "")
        dec = d.get("decision", d.get("action", ""))
        plan = d.get("plan") or ""
        if not plan and d.get("limit") is not None:
            plan = f"{d.get('limit')} / {d.get('stop')} / {d.get('shares')} / {d.get('r_usd')}"
        probe = d.get("paper_probe", "")
        reason = d.get("reason", "")
        lines.append(f"| **{ticker}** | **{dec}** | {plan} | {probe} | {reason} |")
    lines.append("")

    if book_after:
        lines.append("## Book after")
        for k, v in book_after.items():
            lines.append(f"- **{k}:** {v}")
        lines.append("")

    lines.append("## OPEN_QUESTIONS")
    if open_q:
        for i, q in enumerate(open_q, 1):
            lines.append(f"{i}. {q}")
    else:
        lines.append("(none)")
    lines.append("")
    lines.append("**soft_ambition:** N/A")
    lines.append("")

    body = "\n".join(lines)
    if BANNED.search(body):
        raise ValueError("banned token detected in Soft Final stub body")
    return body


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Soft Final stub from decision JSON")
    p.add_argument("--tc", required=True, help="TC id e.g. TC-20261106-v55-dry-SIM")
    p.add_argument("--decision-json", required=True, help="Path to decision JSON")
    p.add_argument("--out", required=True, help="Output Soft Final markdown path")
    args = p.parse_args(argv)

    decision = json.loads(Path(args.decision_json).read_text(encoding="utf-8"))
    try:
        body = render(args.tc, decision)
    except ValueError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        return 2

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    digest = md5_file(out)
    md5_path = out.with_suffix(out.suffix + ".md5")
    md5_path.write_text(digest + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"out": str(out), "md5": digest, "bytes": out.stat().st_size},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
