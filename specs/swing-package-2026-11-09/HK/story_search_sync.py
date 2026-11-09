#!/usr/bin/env python3
"""
Story Search DB Sync Helper
Streamlines updating Google Sheet Story_Search_DB after each narrative report.

Usage:
  python3 story_search_sync.py --rows run_v55        # build rows from stories/*.json + verdicts
  python3 story_search_sync.py                        # historical backfill (CSV)
Or import and call build_row(dict) then use Sheets append tool.

v5.5.2 changes
--------------
* synced_by defaults to "DeepSeek" (the executor moved, see 01_RULES/story_search/SKILL.md).
* `from_story()` maps stories/<T>_story.json + verdicts_<market>.jsonl + L2_Input.csv onto COLUMNS,
  so nobody re-types a number by hand.
* `conviction` holds the VERDICT only (BUY / STALK / WATCH / AVOID) and keeps the existing 27
  rows valid. The Fusion assessment goes in its own column, `narrative_conviction`
  (CONFIRM / CHALLENGE / NEUTRAL); old rows stay blank. `kb_note` is for KB notes only.
  There is no mode switch on purpose: one column, one meaning.
* Rows are built and emitted by column NAME (the header row travels with the data), so the
  sheet can be reordered without corrupting anything.

Schema matches GROK_SYNC_INSTRUCTIONS exactly.
"""

import json
import markets
import csv
import sys
from datetime import datetime
from typing import Dict, List, Optional

COLUMNS = [
    "ticker", "company", "search_date", "handoff_date", "market",
    "market_theme", "policy_layer", "earnings_window", "narrative_main",
    "why_now", "moat", "transmission_certainty", "kb_note",
    "primary_title", "primary_strength", "primary_summary",
    "secondary_title", "secondary_strength", "secondary_summary",
    "risk_title", "risk_score", "risk_summary",
    "vs_technical", "one_liner_yue", "sentiment_tag", "conviction", "narrative_conviction",
    "sources", "full_report_url", "synced_at", "synced_by"
]

VERDICTS = ("BUY", "STALK", "WATCH", "AVOID")
NARRATIVE = ("CONFIRM", "CHALLENGE", "NEUTRAL")


def _clean(col: str, val) -> str:
    """Refuse anything outside the agreed vocabulary; a bad value is dropped, never written."""
    s = "" if val is None else str(val).strip()
    if col == "conviction" and s and s not in VERDICTS:
        print(f"WARN: conviction {s!r} is not one of {VERDICTS} — left blank", file=sys.stderr)
        return ""
    if col == "narrative_conviction" and s and s not in NARRATIVE:
        print(f"WARN: narrative_conviction {s!r} is not one of {NARRATIVE} — left blank", file=sys.stderr)
        return ""
    return s


def build_row(data: Dict) -> List:
    """Build a row list matching COLUMNS order. Missing keys become empty string."""
    row = []
    for col in COLUMNS:
        val = data.get(col, "")
        if col == "synced_at" and not val:
            val = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        if col == "synced_by" and not val:
            val = "DeepSeek"
        row.append(_clean(col, val))
    return row

def row_to_csv_line(row: List) -> str:
    """Escape for CSV."""
    parts = []
    for v in row:
        s = str(v)
        if "," in s or '"' in s or "\n" in s:
            s = '"' + s.replace('"', '""') + '"'
        parts.append(s)
    return ",".join(parts)

# Historical tickers from project memory (basic backfill — full reports not archived)
HISTORICAL = [
    {"ticker": "NTSK", "company": "Netskope", "handoff_date": "2026-09-11", "search_date": "2026-09-13", "market": "US", "conviction": "STALK", "sentiment_tag": "觀望等位"},
    {"ticker": "1797.HK", "company": "East Buy / 東方甄選", "handoff_date": "2026-09-14", "search_date": "2026-09-14", "market": "HK", "conviction": "WATCH", "sentiment_tag": "觀望等位"},
    {"ticker": "MGNI", "company": "Magnite", "handoff_date": "2026-09-14", "search_date": "2026-09-15", "market": "US", "conviction": "BUY", "sentiment_tag": "穩陣上車"},
    {"ticker": "DAR", "company": "Darling Ingredients", "handoff_date": "2026-09-15", "search_date": "2026-09-16", "market": "US", "conviction": "BUY", "sentiment_tag": "穩陣上車"},
    {"ticker": "BILL", "company": "BILL Holdings", "handoff_date": "2026-09-15", "search_date": "2026-09-16", "market": "US", "conviction": "WATCH", "sentiment_tag": "觀望等位"},
    {"ticker": "PGY", "company": "Pagaya Technologies", "handoff_date": "2026-09-16", "search_date": "2026-09-17", "market": "US", "conviction": "WATCH", "sentiment_tag": "觀望等位"},
    {"ticker": "FA", "company": "First Advantage", "handoff_date": "2026-09-16", "search_date": "2026-09-17", "market": "US", "conviction": "BUY", "sentiment_tag": "穩陣上車"},
    {"ticker": "NTAP", "company": "NetApp", "handoff_date": "2026-09-18", "search_date": "2026-09-19", "market": "US", "conviction": "STALK", "sentiment_tag": "觀望等位"},
    {"ticker": "ZBRA", "company": "Zebra Technologies", "handoff_date": "2026-09-18", "search_date": "2026-09-20", "market": "US", "conviction": "BUY", "sentiment_tag": "穩陣上車"},
    {"ticker": "1070.HK", "company": "TCL Electronics / TCL電子", "handoff_date": "2026-09-18", "search_date": "2026-09-20", "market": "HK", "conviction": "WATCH", "sentiment_tag": "觀望等位"},
    {"ticker": "9969.HK", "company": "InnoCare / 諾誠健華", "handoff_date": "2026-09-21", "search_date": "2026-09-21", "market": "HK", "conviction": "BUY", "sentiment_tag": "穩陣上車"},
    {"ticker": "0400.HK", "company": "Ingdan / 硬蛋創新", "handoff_date": "2026-09-21", "search_date": "2026-09-21", "market": "HK", "conviction": "WATCH", "sentiment_tag": "觀望等位"},
    {"ticker": "0376.HK", "company": "Yunfeng Financial / 雲鋒金融", "handoff_date": "2026-09-21", "search_date": "2026-09-22", "market": "HK", "conviction": "WATCH", "sentiment_tag": "觀望等位"},
    {"ticker": "TGB", "company": "Trekor Metals", "handoff_date": "2026-09-21", "search_date": "2026-09-22", "market": "US", "conviction": "STALK", "sentiment_tag": "觀望等位"},
    {"ticker": "BETA", "company": "BETA Technologies", "handoff_date": "2026-09-21", "search_date": "2026-09-22", "market": "US", "conviction": "WATCH", "sentiment_tag": "觀望等位"},
    {"ticker": "NLST", "company": "Netlist", "handoff_date": "2026-09-23", "search_date": "2026-09-24", "market": "US", "conviction": "WATCH", "sentiment_tag": "觀望等位"},
    {"ticker": "OCTV", "company": "Octave Intelligence", "handoff_date": "2026-09-23", "search_date": "2026-09-24", "market": "US", "conviction": "WATCH", "sentiment_tag": "觀望等位"},
    {"ticker": "ACHR", "company": "Archer Aviation", "handoff_date": "2026-09-24", "search_date": "2026-09-25", "market": "US", "conviction": "WATCH", "sentiment_tag": "觀望等位"},
    {"ticker": "CORT", "company": "Corcept Therapeutics", "handoff_date": "2026-09-25", "search_date": "2026-09-26", "market": "US", "conviction": "STALK", "sentiment_tag": "觀望等位"},
    {"ticker": "S", "company": "SentinelOne", "handoff_date": "2026-09-29", "search_date": "2026-09-30", "market": "US", "conviction": "STALK", "sentiment_tag": "觀望等位"},
    {"ticker": "PAYC", "company": "Paycom Software", "handoff_date": "2026-10-01", "search_date": "2026-10-02", "market": "US", "conviction": "STALK", "sentiment_tag": "觀望等位"},
    {"ticker": "QLYS", "company": "Qualys", "handoff_date": "2026-10-01", "search_date": "2026-10-02", "market": "US", "conviction": "WATCH", "sentiment_tag": "觀望等位"},
    {"ticker": "TALO", "company": "Talos Energy", "handoff_date": "2026-10-05", "search_date": "2026-10-06", "market": "US", "conviction": "STALK", "sentiment_tag": "觀望等位"},
    {"ticker": "FIGS", "company": "FIGS Inc", "handoff_date": "2026-10-06", "search_date": "2026-10-07", "market": "US", "conviction": "STALK", "sentiment_tag": "觀望等位"},
    {"ticker": "LIFE", "company": "Ethos Technologies", "handoff_date": "2026-10-08", "search_date": "2026-10-09", "market": "US", "conviction": "STALK", "sentiment_tag": "觀望等位"},
    {"ticker": "CRL", "company": "Charles River Laboratories", "handoff_date": "2026-10-15", "search_date": "2026-10-16", "market": "US", "conviction": "STALK", "sentiment_tag": "觀望等位"},
    {"ticker": "ATEC", "company": "Alphatec Holdings", "handoff_date": "2026-10-15", "search_date": "2026-10-16", "market": "US", "conviction": "WATCH", "sentiment_tag": "觀望等位"},
]

def generate_historical_rows() -> List[List]:
    rows = []
    for h in HISTORICAL:
        h.setdefault("kb_note", "歷史 backfill — 完整報告未歸檔")
        h.setdefault("primary_summary", "待補完整敘事（來自 project memory）")
        rows.append(build_row(h))
    return rows

CERTAINTY = {"核心受惠": "高", "邊緣受惠": "中", "無關": "低"}


def from_story(story: Dict, verdict_row: Dict, contract_row: Dict) -> Dict:
    """Map v5.5.2 files onto the sheet schema. Missing values stay empty, never invented."""
    conv_narr = str(story.get("conviction", ""))
    verdict = str(verdict_row.get("verdict", ""))
    return {
        "ticker": story.get("ticker", ""),
        "company": story.get("company", ""),
        "search_date": story.get("story_date", ""),
        "handoff_date": str(contract_row.get("Date", "")),
        "market": "US",
        "market_theme": story.get("market_line", ""),
        "policy_layer": story.get("route_tag", ""),
        "earnings_window": (f"{contract_row.get('Earnings_Proximity_Flag', '')} "
                            f"{contract_row.get('Earnings_Date', '')}").strip(),
        "narrative_main": story.get("story_main", ""),
        "why_now": story.get("why_now", ""),
        "moat": story.get("moat", ""),
        "transmission_certainty": CERTAINTY.get(story.get("route_tag", ""), ""),
        "kb_note": "",
        "primary_title": story.get("story_tag", ""),
        "primary_strength": story.get("story_main_score", ""),
        "primary_summary": story.get("story_main", ""),
        "secondary_title": "",
        "secondary_strength": story.get("story_sub_score", ""),
        "secondary_summary": story.get("story_sub", ""),
        "risk_title": "",
        "risk_score": "",
        "risk_summary": "；".join(map(str, story.get("risks", []))),
        "vs_technical": {"CONFIRM": "呼應", "CHALLENGE": "衝突"}.get(conv_narr, "中性"),
        "one_liner_yue": verdict_row.get("closer", ""),
        "sentiment_tag": verdict_row.get("emotion", ""),
        "conviction": verdict,
        "narrative_conviction": conv_narr,
        "sources": " | ".join(f"{x.get('title', '')} {x.get('url', '')}"
                              for x in (story.get("sources") or [])),
        "full_report_url": "",
    }


def rows_from_run(folder: str) -> List[List]:
    import os
    import pandas as pd
    c = pd.read_csv(os.path.join(folder, "L2_Input.csv"),
                    keep_default_na=False, na_values=[""]).set_index("Ticker")
    with open(markets.verdicts_path(folder), encoding="utf-8") as fh:   # v6.9
        vs = [json.loads(l) for l in fh if l.strip()]
    out = []
    for v in vs:
        t = v.get("ticker")
        sp = os.path.join(folder, "stories", f"{t}_story.json")
        if not os.path.exists(sp) or t not in c.index:
            continue
        story = json.load(open(sp, encoding="utf-8"))
        out.append(build_row(from_story(story, v, c.loc[t])))
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", help="run folder with stories/ + verdicts_<market>.jsonl + L2_Input.csv")
    a = ap.parse_args()
    if a.rows:
        print(",".join(COLUMNS))
        for r in rows_from_run(a.rows):
            print(row_to_csv_line(r))
        raise SystemExit(0)
    print("=== Historical backfill rows (CSV) ===")
    print(",".join(COLUMNS))
    for r in generate_historical_rows():
        print(row_to_csv_line(r))
    print(f"\nTotal historical rows ready: {len(HISTORICAL)}")
    print("Use Sheets append tool with these rows (skip NEOG which already exists).")
