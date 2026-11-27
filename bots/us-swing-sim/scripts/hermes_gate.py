#!/usr/bin/env python3
"""Hermes session gate + Contract/Trigger/verdict extract (local files only).

Gate rules (skill verbatim):
- Missing verdicts_US.jsonl → NO_TRADE
- L2_Check_Report.md exists AND contains word FAIL → NO_TRADE
- L2 missing → PASS with warning l2_absent (absence ≠ FAIL)

Never invent prices. Missing fields are omitted.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

# Key Contract columns to surface (omit if blank/missing)
CONTRACT_KEYS = [
    "Ticker",
    "Date",
    "Close",
    "Candidate_Class",
    "Screen_Flag",
    "Entry_Feasible",
    "Risk_OK",
    "Setup_OK",
    "Setup_Family",
    "Setup_Code",
    "Pullback_Code",
    "Stop_Type_Plan",
    "Entry_Ref",
    "Entry_Src",
    "Invalidate_Below",
    "Trigger_Price",
    "Trigger_Min_Vol",
    "BuyStop_Max_Stop",
    "Room_To_Supply_R",
    "Room_Basis",
    "Supply_Level",
    "Supply_Source",
    "Supply_Soft_Level",
    "Supply_Soft_Source",
    "Room_To_Soft_R",
    "Resistance_20D_Prior",
    "Earnings_Proximity_Flag",
    "Earnings_Date",
    "Days_To_Earnings",
    "Risk_Pct_Plan",
    "Risk_ADR_Plan",
    "Leader_OK",
]

TRIGGER_KEYS = [
    "Ticker",
    "Candidate_Class",
    "Setup_OK",
    "Risk_OK",
    "Setup_Family",
    "Setup_Code",
    "Entry_Feasible",
    "Stop_Type_Plan",
    "Trigger_Price",
    "Trigger_Min_Vol",
    "Invalidate_Below",
    "Entry_Ref",
    "BuyStop_Max_Stop",
    "Room_To_Supply_R",
    "Risk_Pct_Plan",
    "Risk_ADR_Plan",
    "Supply_Source",
]


def _blank(v) -> bool:
    if v is None:
        return True
    s = str(v).strip()
    return s == "" or s.upper() == "NONE" or s.upper() == "NONE_ABOVE"


def _row_subset(row: dict, keys: list[str]) -> dict:
    out = {}
    for k in keys:
        if k not in row:
            continue
        v = row[k]
        if _blank(v):
            continue
        # try numeric
        if isinstance(v, str):
            try:
                if "." in v or "e" in v.lower():
                    out[k] = float(v)
                else:
                    out[k] = int(v)
                continue
            except ValueError:
                out[k] = v
        else:
            out[k] = v
    return out


def _read_csv_dict(path: Path) -> list[dict]:
    """Read CSV with keep_default_na=False semantics (empty → '')."""
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for raw in reader:
            # DictReader already gives '' for empty; force str and no NA invent
            rows.append({k: ("" if v is None else v) for k, v in raw.items()})
        return rows


def _load_verdicts(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    out = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def _find_ticker(rows: list[dict], ticker: str, key: str = "Ticker") -> dict | None:
    t = ticker.upper()
    for r in rows:
        # Contract/Trigger use Ticker; verdicts use ticker
        tv = r.get(key) or r.get("ticker") or r.get("Ticker")
        if tv and str(tv).upper() == t:
            return r
    return None


def gate_pack(pack: Path, ticker: str | None = None) -> dict:
    pack = pack.resolve()
    reasons: list[str] = []
    warnings: list[str] = []
    gate = "PASS"

    verdicts_path = pack / "verdicts_US.jsonl"
    l2_path = pack / "L2_Check_Report.md"
    contract_path = pack / "Contract_US.csv"
    trigger_path = pack / "Trigger_US.csv"

    if not verdicts_path.is_file():
        gate = "NO_TRADE"
        reasons.append("verdicts_US.jsonl missing → unique entry gate FAIL")

    if l2_path.is_file():
        text = l2_path.read_text(encoding="utf-8", errors="replace")
        # case-sensitive word FAIL
        if re.search(r"\bFAIL\b", text):
            gate = "NO_TRADE"
            reasons.append("L2_Check_Report.md contains FAIL")
        else:
            warnings.append("l2_present_no_FAIL")
    else:
        warnings.append("l2_absent")

    verdicts = _load_verdicts(verdicts_path) if verdicts_path.is_file() else []
    contracts = _read_csv_dict(contract_path) if contract_path.is_file() else []
    triggers = _read_csv_dict(trigger_path) if trigger_path.is_file() else []

    if not contract_path.is_file():
        warnings.append("Contract_US.csv missing")
    if not trigger_path.is_file():
        warnings.append("Trigger_US.csv missing")

    result: dict = {
        "pack": str(pack),
        "gate": gate,
        "reasons": reasons,
        "warnings": warnings,
        "files": {
            "verdicts_US.jsonl": verdicts_path.is_file(),
            "L2_Check_Report.md": l2_path.is_file(),
            "Contract_US.csv": contract_path.is_file(),
            "Trigger_US.csv": trigger_path.is_file(),
        },
        "verdict_count": len(verdicts),
    }

    if ticker:
        t = ticker.upper()
        vrow = _find_ticker(verdicts, t)
        crow = _find_ticker(contracts, t, "Ticker")
        trow = _find_ticker(triggers, t, "Ticker")
        result["ticker"] = t
        result["ticker_row"] = vrow  # full verdict JSON or null
        result["contract_row"] = _row_subset(crow, CONTRACT_KEYS) if crow else None
        result["trigger_row"] = _row_subset(trow, TRIGGER_KEYS) if trow else None
        if vrow is None:
            warnings.append(f"ticker {t} not in verdicts_US.jsonl")
        if crow is None and contract_path.is_file():
            warnings.append(f"ticker {t} not in Contract_US.csv")
        if trow is None and trigger_path.is_file():
            warnings.append(f"ticker {t} not in Trigger_US.csv")
        result["warnings"] = warnings
    else:
        result["ticker_row"] = None
        result["contract_row"] = None
        result["trigger_row"] = None
        # list tickers present in verdicts for agent convenience
        result["verdict_tickers"] = [
            v.get("ticker") for v in verdicts if v.get("ticker")
        ]

    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Hermes gate + extract")
    p.add_argument("--pack", required=True, help="Local Hermes pack dir")
    p.add_argument("--ticker", default=None, help="Optional ticker to extract")
    p.add_argument("--json", action="store_true", help="Print JSON (default)")
    args = p.parse_args(argv)

    pack = Path(args.pack)
    if not pack.is_dir():
        print(json.dumps({"gate": "NO_TRADE", "reasons": [f"pack not a dir: {pack}"], "warnings": []}))
        return 2

    out = gate_pack(pack, args.ticker)
    print(json.dumps(out, ensure_ascii=False))
    return 0 if out["gate"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
