#!/usr/bin/env python3
"""Hermes Soft Final ranker + 書面語 draft + judgment flags (model decides; script executes).

Collapses token-heavy ranking/filters/handoff copy and the locked Soft Final skeleton
from a local Hermes pack (v5.5.2+; Tradeable gate when Contract has Tradeable col — v5.5.4).
Soft-demote is a draft suggestion only; ranked_candidates.json / handoff_blocks.md stay
pre-LLM script stalks. LLM starts from the draft + flags; may confirm or undo a soft
demote; never upgrades WATCH/AVOID; does not recap regime/Brief/MM/RS.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

GRADE_ORDER = {"A+": 0, "A": 1, "B": 2, "C": 3, "D": 4}
STALKABLE_VERDICTS = {"BUY", "STALK"}
HARD_EARNINGS = {"PASS", "UNKNOWN"}
HARD_ENTRY = {"INVALIDATED", "MISSED"}
BANNED_TOKEN_PATTERNS = [
    re.compile(r"\bRR_Ratio\b", re.I),
    re.compile(r"\bRisk.?Reward.?Ratio\b", re.I),
    re.compile(r"\bTarget_[123]\b", re.I),
    re.compile(r"\bPRIMARY.?TARGET\b", re.I),
    re.compile(r"\bSetup_Type\b", re.I),
    re.compile(r"\bAdjusted_Stop\b", re.I),
    re.compile(r"\bADJUSTED.?STOP\b", re.I),
    re.compile(r"\bENTRY.?ZONE\b", re.I),
]

ADR_BANDS = {
    "BREAKOUT": (0.3, 1.2),
    "PULLBACK": (0.8, 2.5),
    "REVERSAL": (0.8, 2.5),
}

PRIMARY_FILES = (
    "verdicts_US.jsonl",
    "L2_Input.csv",
    "Contract_US.csv",
)


def _s(val: Any, default: str = "") -> str:
    if val is None:
        return default
    if isinstance(val, float) and pd.isna(val):
        return default
    text = str(val).strip()
    if text.lower() in {"nan", "none", "<na>"}:
        return default
    return text


def _f(val: Any) -> float | None:
    text = _s(val)
    if text == "":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _grade_key(grade: str) -> tuple[int, str]:
    g = _s(grade).upper()
    if g in GRADE_ORDER:
        return (GRADE_ORDER[g], g)
    if g in {"", "NA", "N/A", "NONE"}:
        return (99, "NA")
    return (50, g)


def load_verdicts(path: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        ticker = _s(row.get("ticker") or row.get("Ticker")).upper()
        if ticker:
            out[ticker] = row
    return out



def load_trigger_tickers(path: Path) -> set[str]:
    """Tickers present in Trigger_US.csv (I30 ⇒ Tradeable=PASS upstream)."""
    out: set[str] = set()
    if not path.exists():
        return out
    try:
        df = pd.read_csv(path, keep_default_na=False)
    except Exception:
        return out
    col = "Ticker" if "Ticker" in df.columns else ("ticker" if "ticker" in df.columns else None)
    if not col:
        return out
    for val in df[col].tolist():
        t = _s(val).upper()
        if t:
            out.add(t)
    return out


def folder_date_hint(pack_dir: Path) -> str | None:
    # Prefer parent folder YYYY-MM-DD, else pack name containing date
    for candidate in (pack_dir.parent.name, pack_dir.name):
        m = re.search(r"(20\d{2}-\d{2}-\d{2})", candidate)
        if m:
            return m.group(1)
    return None


def merge_rows(
    contract: pd.DataFrame, l2: pd.DataFrame, verdicts: dict[str, dict],
    *, tradeable_col_present: bool = False, trigger_tickers: set[str] | None = None,
) -> list[dict[str, Any]]:
    l2_by = { _s(r["Ticker"]).upper(): r for _, r in l2.iterrows() }
    trigger_tickers = trigger_tickers or set()
    rows: list[dict[str, Any]] = []
    for _, crow in contract.iterrows():
        ticker = _s(crow.get("Ticker")).upper()
        if not ticker:
            continue
        lrow = l2_by.get(ticker)
        vrow = verdicts.get(ticker)

        # Verdict preference: jsonl wins; else L2 Baseline_Verdict
        if vrow and _s(vrow.get("verdict")):
            verdict = _s(vrow.get("verdict")).upper()
            verdict_source = "verdicts_US.jsonl"
        elif lrow is not None and _s(lrow.get("Baseline_Verdict")):
            verdict = _s(lrow.get("Baseline_Verdict")).upper()
            verdict_source = "L2_Baseline"
        else:
            verdict = ""
            verdict_source = "missing"

        grade = ""
        if vrow and _s(vrow.get("grade")):
            grade = _s(vrow.get("grade"))
        elif lrow is not None:
            grade = _s(lrow.get("Setup_Quality_Grade"))

        speak_up = _s(lrow.get("Speak_Up")) if lrow is not None else ""
        quality_detail = _s(lrow.get("Setup_Quality_Detail")) if lrow is not None else ""
        closer = _s(vrow.get("closer")) if vrow else ""

        family = _s(crow.get("Setup_Family"))
        code = _s(crow.get("Setup_Code"))
        room = _f(crow.get("Room_To_Supply_R"))
        rs = _f(crow.get("RS_Score"))
        risk_ok = _s(crow.get("Risk_OK")).upper()
        earn_flag = _s(crow.get("Earnings_Proximity_Flag")).upper()
        entry_feasible = _s(crow.get("Entry_Feasible")).upper()
        risk_adr = _f(crow.get("Risk_ADR_Plan"))

        # Tradeable (v5.5.4): Contract wins; else L2 / verdicts passthrough
        tradeable = _s(crow.get("Tradeable")).upper()
        tradeable_why = _s(crow.get("Tradeable_Why"))
        if not tradeable and lrow is not None:
            tradeable = _s(lrow.get("Tradeable")).upper()
            if not tradeable_why:
                tradeable_why = _s(lrow.get("Tradeable_Why"))
        if not tradeable and vrow:
            tradeable = _s(vrow.get("Tradeable") or vrow.get("tradeable")).upper()
            if not tradeable_why:
                tradeable_why = _s(vrow.get("Tradeable_Why") or vrow.get("tradeable_why"))
        room_at_plan = _f(crow.get("Room_At_Plan_Stop_R"))
        room_at_12 = _f(crow.get("Room_At_1_2ADR_R"))
        in_trigger = ticker in trigger_tickers

        out_of_band = False
        band = ADR_BANDS.get(family.upper()) if family else None
        if band and risk_adr is not None:
            lo, hi = band
            if not (lo <= risk_adr <= hi):
                out_of_band = True

        row: dict[str, Any] = {
            "ticker": ticker,
            "date": _s(crow.get("Date")),
            "verdict": verdict,
            "verdict_source": verdict_source,
            "baseline_verdict": _s(lrow.get("Baseline_Verdict")).upper() if lrow is not None else "",
            "grade": grade or "NA",
            "room": room,
            "rs_score": rs,
            "rs_status": _s(crow.get("RS_Status")),
            "risk_ok": risk_ok,
            "risk_why": _s(crow.get("Risk_Why")),
            "earnings_flag": earn_flag,
            "earnings_date": _s(crow.get("Earnings_Date")),
            "entry_feasible": entry_feasible,
            "setup_family": family,
            "setup_code": code,
            "entry_ref": _s(crow.get("Entry_Ref")),
            "entry_src": _s(crow.get("Entry_Src")),
            "invalidate_below": _s(crow.get("Invalidate_Below")),
            "stop_type_plan": _s(crow.get("Stop_Type_Plan")),
            "risk_pct_plan": _s(crow.get("Risk_Pct_Plan")),
            "risk_adr_plan": _s(crow.get("Risk_ADR_Plan")),
            "supply_level": _s(crow.get("Supply_Level")),
            "supply_source": _s(crow.get("Supply_Source")),
            "supply_soft_level": _s(crow.get("Supply_Soft_Level")),
            "room_to_soft_r": _s(crow.get("Room_To_Soft_R")),
            "speak_up": speak_up,
            "quality_detail": quality_detail,
            "closer": closer,
            "downgrade_reason": _s(vrow.get("downgrade_reason")) if vrow else "",
            "out_of_band": out_of_band,
            "candidate_class": _s(crow.get("Candidate_Class")),
            "screen_flag": _s(crow.get("Screen_Flag")),
            "tradeable": tradeable,
            "tradeable_why": tradeable_why,
            "tradeable_col_present": bool(tradeable_col_present),
            "room_at_plan_stop_r": room_at_plan,
            "room_at_1_2adr_r": room_at_12,
            "in_trigger": bool(in_trigger),
            "close": _s(crow.get("Close")) or (_s(lrow.get("Close")) if lrow is not None else ""),
            "leader_ok": (
                _s(crow.get("Leader_OK"))
                or (_s(lrow.get("Leader_OK")) if lrow is not None else "")
            ).upper(),
            "leader_why": _s(crow.get("Leader_Why")) or (
                _s(lrow.get("Leader_Why")) if lrow is not None else ""
            ),
            "priority_score": _s(crow.get("Priority_Score")) or (
                _s(lrow.get("Priority_Score")) if lrow is not None else ""
            ),
            "minervini_trend": crow.get("Minervini_Trend")
            if "Minervini_Trend" in crow.index
            else (lrow.get("Minervini_Trend") if lrow is not None else ""),
            "minervini_stage2": crow.get("Minervini_Stage2")
            if "Minervini_Stage2" in crow.index
            else (lrow.get("Minervini_Stage2") if lrow is not None else ""),
            "dist_from_52w_high_pct": _s(crow.get("Dist_from_52W_High_Pct"))
            or (_s(lrow.get("Dist_from_52W_High_Pct")) if lrow is not None else ""),
            "volume_confirm": _s(crow.get("Volume_Confirm"))
            or (_s(lrow.get("Volume_Confirm")) if lrow is not None else ""),
            "class_note": _s(crow.get("Class_Note"))
            or (_s(lrow.get("Class_Note")) if lrow is not None else ""),
            "days_to_earnings": _s(crow.get("Days_To_Earnings"))
            or (_s(lrow.get("Days_To_Earnings")) if lrow is not None else ""),
            "supply_soft_source": _s(crow.get("Supply_Soft_Source"))
            or (_s(lrow.get("Supply_Soft_Source")) if lrow is not None else ""),
        }
        rows.append(row)
    return rows


def classify_row(
    row: dict[str, Any],
    prior: set[str],
    no_repeat_exclude: bool,
) -> tuple[str, list[str], list[str]]:
    """Return (status, hard_reasons, soft_tags). status: stalk_candidate|observe|excluded"""
    reasons: list[str] = []
    tags: list[str] = []

    if row["risk_ok"] != "PASS":
        reasons.append(f"Risk_OK={row['risk_ok'] or 'EMPTY'}!=PASS")

    # Tradeable hard gate when Contract (or pack) has the column.
    # FAIL / empty never enter stalk list. Trigger membership ⇒ PASS by I30.
    if row.get("tradeable_col_present"):
        tstat = _s(row.get("tradeable")).upper()
        why = _s(row.get("tradeable_why"))
        if tstat == "PASS" or row.get("in_trigger"):
            if tstat != "PASS" and row.get("in_trigger"):
                tags.append("trigger_implies_tradeable")
        else:
            label = tstat or "EMPTY"
            reason = f"Tradeable={label}!=PASS"
            if why:
                reason += f"; Tradeable_Why={why}"
            reasons.append(reason)

    if row["earnings_flag"] in HARD_EARNINGS:
        reasons.append(f"Earnings_Proximity_Flag={row['earnings_flag']}")
    if row["entry_feasible"] in HARD_ENTRY:
        reasons.append(f"Entry_Feasible={row['entry_feasible']}")

    room = row["room"]
    if room is None:
        reasons.append("Room_To_Supply_R=missing")
    elif room < 1.0:
        reasons.append(f"Room_To_Supply_R={room}<1.0")
    elif room < 2.0:
        tags.append("thin_room")

    verdict = row["verdict"]
    if verdict in {"WATCH", "AVOID"}:
        reasons.append(f"never_upgrade_{verdict}")
    elif verdict not in STALKABLE_VERDICTS:
        reasons.append(f"verdict_not_stalkable={verdict or 'EMPTY'}")

    if row["out_of_band"]:
        tags.append("out_of_band_adr")

    if no_repeat_exclude and row["ticker"] in prior:
        reasons.append("no_repeat_exclude")
    elif row["ticker"] in prior:
        tags.append("prior_stalk_remark")

    if reasons:
        # Observe = notable non-stalks for Justin remarks (2–5); else excluded
        notable = False
        if verdict in {"AVOID", "WATCH"}:
            if row["risk_ok"] == "PASS":
                notable = True
            if "Earnings_Proximity_Flag=PASS" in reasons:
                notable = True
            if row.get("downgrade_reason"):
                notable = True
            if row.get("verdict_source") == "verdicts_US.jsonl":
                notable = True
            if any(r.startswith("Tradeable=") for r in reasons):
                notable = True
        elif any(r.startswith("Tradeable=") for r in reasons):
            # BUY/STALK demoted by Tradeable → observe with Why (WATCH wording)
            notable = True
        elif "Earnings_Proximity_Flag=PASS" in reasons and row.get("baseline_verdict") in STALKABLE_VERDICTS:
            notable = True
        return ("observe" if notable else "excluded"), reasons, tags

    return "stalk_candidate", reasons, tags


def rank_key(row: dict[str, Any]) -> tuple:
    g_ord, _ = _grade_key(row["grade"])
    room = row["room"] if row["room"] is not None else -1.0
    rs = row["rs_score"] if row["rs_score"] is not None else -1.0
    return (g_ord, -room, -rs, row["ticker"])


def why_line(row: dict[str, Any]) -> str:
    parts: list[str] = []
    if row["speak_up"]:
        parts.append(row["speak_up"])
    if row["quality_detail"]:
        parts.append(row["quality_detail"])
    if row["closer"]:
        parts.append(row["closer"])
    text = " · ".join(p for p in parts if p)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 220:
        text = text[:217].rstrip() + "…"
    return text or f"{row['verdict']} · quality {row['grade']}"


def fmt_num(val: Any) -> str:
    text = _s(val)
    return text if text else "—"


def handoff_block(row: dict[str, Any], tags: list[str]) -> str:
    room = row["room"]
    room_s = f"{room}" if room is not None else "—"
    soft_r = fmt_num(row["room_to_soft_r"])
    lines = [
        f"{row['ticker']} · {row['setup_family']}/{row['setup_code']} · {row['verdict']} · quality {row['grade']}",
        (
            f"entry {fmt_num(row['entry_ref'])} ({fmt_num(row['entry_src'])}) · "
            f"stop {fmt_num(row['invalidate_below'])} ({fmt_num(row['stop_type_plan'])}) · "
            f"risk {fmt_num(row['risk_pct_plan'])}% = {fmt_num(row['risk_adr_plan'])}xADR"
        ),
        (
            f"room {room_s}R → {fmt_num(row['supply_level'])} ({fmt_num(row['supply_source'])}) · "
            f"soft {fmt_num(row['supply_soft_level'])} ({soft_r}R)"
        ),
        (
            f"RS {fmt_num(row['rs_score'])} ({fmt_num(row['rs_status'])}) · "
            f"earnings {fmt_num(row['earnings_flag'])} {fmt_num(row['earnings_date'])}"
        ),
        f"speak-up: {row['speak_up'] or '—'}",
        f"why: {why_line(row)}",
    ]
    # thin_room / out_of_band live in ranked JSON + stub headings — not inside §3.3 fence
    _ = tags
    return "\n".join(lines)


def default_out_dir(pack_dir: Path, contract_date: str) -> Path:
    parent = pack_dir.parent
    if re.fullmatch(r"20\d{2}-\d{2}-\d{2}", parent.name):
        return parent
    if contract_date and re.fullmatch(r"20\d{2}-\d{2}-\d{2}", contract_date):
        return Path.cwd() / contract_date
    return Path.cwd() / "soft-final-out"


def banned_scan(text: str) -> list[str]:
    hits: list[str] = []
    for pat in BANNED_TOKEN_PATTERNS:
        m = pat.search(text)
        if m:
            hits.append(m.group(0))
    return hits


def build_soft_final_stub(
    *,
    pack_dir: Path,
    contract_date: str,
    stalks: list[dict[str, Any]],
    handoff_text: str,
    observe_rows: list[dict[str, Any]],
    ranked: list[dict[str, Any]],
    date_ok: bool,
    primary_ok: bool,
) -> str:
    pack = pack_dir.resolve()
    stalk_count = len(stalks)
    observe_lines: list[str] = []
    for r in observe_rows[:5]:
        reasons = ", ".join(r.get("reasons") or [])
        why = _s(r.get("tradeable_why"))
        demote = ""
        if why and any(str(x).startswith("Tradeable=") for x in (r.get("reasons") or [])):
            demote = f" · 暫不掛單／要等／原因：{why}"
        observe_lines.append(
            f"- **{r['ticker']}** · verdict **{r['verdict'] or '—'}** · "
            f"Grade {r['grade']} · Room {r['room'] if r['room'] is not None else '—'}R · "
            f"exclude/observe: {reasons}{demote}"
        )
    if not observe_lines:
        observe_lines = ["- (none notable)"]

    if stalk_count == 0:
        stalks_section = (
            "## AUTHORIZE Soft Final — stalks **0**（cannot find；唔 pad）\n"
            "No ticker cleared hard-exclude + stalkable verdict (BUY/STALK) + Room≥1.0.\n"
        )
    else:
        blocks = []
        # Split handoff into per-ticker fenced blocks
        parts = [p.strip() for p in handoff_text.split("\n\n") if p.strip()]
        for i, (row, block) in enumerate(zip(stalks, parts), start=1):
            tags = row.get("tags") or []
            tag_note = " · **thin_room**" if "thin_room" in tags else ""
            blocks.append(
                f"### Stalk {i} — {row['ticker']}{tag_note}\n```\n{block}\n```\n"
            )
        stalks_section = (
            f"## AUTHORIZE Soft Final — stalks **{stalk_count}**（≤3；唔 pad）\n"
            + "\n".join(blocks)
        )

    verify = [
        f"- [{'x' if primary_ok else ' '}] Primary Hermes files present for session Date",
        f"- [{'x' if date_ok else ' '}] Folder Date matches Contract `Date` ({contract_date or '—'})",
        f"- [{'x' if stalk_count <= 3 else ' '}] ≤3 stalks ({stalk_count}); never force 3",
        f"- [{'x' if stalk_count > 0 else ' '}] Stalks are Hermes §3.3 handoff blocks (script-filled)",
        "- [x] Hard excludes applied (Risk_OK / Tradeable FAIL|empty when col present / earnings PASS|UNKNOWN / Entry INVALIDATED|MISSED / Room<1 / never upgrade WATCH|AVOID)",
        "- [x] Banned Hermes-deleted fields (RR / target-N / setup-type / adjusted-stop) scanned in script_verify.json",
        "- [ ] Tape one-liner filled by LLM",
        "- [ ] Stockbee / regime / brief prose filled by LLM",
        "- [ ] Reflection (5) filled by LLM",
        "- [ ] X dig filled by LLM",
        "- [ ] Notion sync / overview / Jev (LLM or downstream)",
        "- [x] PINNED_INPUTS pack paths filled by script",
    ]

    thin_note = ""
    if any("thin_room" in (s.get("tags") or []) for s in stalks):
        thin_note = "At least one stalk tagged **thin_room** (Room in [1.0, 2)).\n"

    return f"""# Second-brain Soft Final — STUB (script-first)
**Header:** session **{contract_date or 'UNKNOWN'}** · Contract Date **{contract_date or 'UNKNOWN'}** · run script `{datetime.now().strftime('%Y-%m-%d %H:%M')} HKT`
Artifacts dir: `{pack.parent}/`
Local pack: `{pack}/`
**Soft Final = stub** · Script-first rung: **Script** (`hermes_soft_final.py`)
LLM must NOT re-rank from raw CSV when this stub + ranked_candidates.json exist; may demote stalks, never upgrade.

## Tape one-liner
<!-- PLACEHOLDER: regime label + exposure cue + what's working / dying -->

## Stockbee read
<!-- PLACEHOLDER: latest Stockbee 熱度圖 1–3 lines -->

## Context note（MM／native RS／regime／brief）
<!-- PLACEHOLDER: Market Master / native RS / regime / US brief conflict-only notes -->

{stalks_section}{thin_note}
## Observe（非 stalk；唔 upgrade）
{chr(10).join(observe_lines)}

## Why not pad to 3
<!-- PLACEHOLDER optional: script already selected {stalk_count}; LLM may explain empty seats -->
Script stalk_candidates after hard-exclude: {stalk_count}. Ranked universe size: {len(ranked)}.

## Reflection（5）
1. **Better candidates?** <!-- PLACEHOLDER -->
2. **Market focus now?** <!-- PLACEHOLDER -->
3. **Timing?** <!-- PLACEHOLDER -->
4. **Why this ticker vs the big trend?** <!-- PLACEHOLDER -->
5. **Evidence conflict?** <!-- PLACEHOLDER -->

## No-repeat
<!-- PLACEHOLDER: prior Soft stalk tickers remark -->

## What I can dig on X（≤7）
<!-- PLACEHOLDER -->

## X dig update
<!-- PLACEHOLDER -->

## PINNED_INPUTS
- Local: `{pack / 'verdicts_US.jsonl'}`
- Local: `{pack / 'L2_Input.csv'}`
- Local: `{pack / 'Contract_US.csv'}`（Date={contract_date or '—'}；price truth）
- Local: `{pack / 'Trigger_US.csv'}`
- Local: `{pack / 'index.md'}`（conclusions only）
- Local: `{pack / 'Data_Quality_Report.csv'}`
- Drive parent US_Stock_Data: `1Jn7yi0sXFBqVjLvjCsIazZnOvw0_E4TY`
- Regime: <!-- PLACEHOLDER path -->
- Brief: <!-- PLACEHOLDER path -->
- Stockbee: <!-- PLACEHOLDER path -->

## VERIFY checklist
{chr(10).join(verify)}

非投資建議。Stalk / observe framing only.
"""


def run(args: argparse.Namespace) -> int:
    pack_dir = Path(args.pack_dir).expanduser().resolve()
    missing = [f for f in PRIMARY_FILES if not (pack_dir / f).exists()]
    # Trigger + index + DQR optional but noted
    optional_missing = [
        f
        for f in ("Trigger_US.csv", "index.md", "Data_Quality_Report.csv")
        if not (pack_dir / f).exists()
    ]

    exit_code = 0
    primary_ok = not missing

    if missing:
        print(f"ERROR: missing primary files in {pack_dir}: {missing}", file=sys.stderr)
        exit_code = 2

    contract = (
        pd.read_csv(pack_dir / "Contract_US.csv", keep_default_na=False)
        if (pack_dir / "Contract_US.csv").exists()
        else pd.DataFrame()
    )
    l2 = (
        pd.read_csv(pack_dir / "L2_Input.csv", keep_default_na=False)
        if (pack_dir / "L2_Input.csv").exists()
        else pd.DataFrame()
    )
    verdicts = load_verdicts(pack_dir / "verdicts_US.jsonl")

    contract_dates = sorted({_s(d) for d in contract["Date"].tolist()}) if len(contract) else []
    contract_date = contract_dates[0] if len(contract_dates) == 1 else (contract_dates[0] if contract_dates else "")
    hint = folder_date_hint(pack_dir)
    date_ok = True
    date_note = ""
    if hint and contract_date and hint != contract_date:
        date_ok = False
        date_note = f"folder hint {hint} != Contract Date {contract_date}"
        print(f"ERROR: date mismatch — {date_note}", file=sys.stderr)
        exit_code = 2
    elif len(contract_dates) > 1:
        date_ok = False
        date_note = f"multiple Contract dates: {contract_dates}"
        print(f"ERROR: {date_note}", file=sys.stderr)
        exit_code = 2

    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else default_out_dir(pack_dir, contract_date)
    out_dir.mkdir(parents=True, exist_ok=True)

    prior = {t.strip().upper() for t in (args.prior_stalks or "").split(",") if t.strip()}

    tradeable_col_present = bool(len(contract) and "Tradeable" in contract.columns)
    trigger_tickers = load_trigger_tickers(pack_dir / "Trigger_US.csv")

    ranked_rows: list[dict[str, Any]] = []
    if primary_ok and len(contract):
        merged = merge_rows(
            contract,
            l2 if len(l2) else pd.DataFrame(columns=["Ticker"]),
            verdicts,
            tradeable_col_present=tradeable_col_present,
            trigger_tickers=trigger_tickers,
        )
        for row in merged:
            status, reasons, tags = classify_row(row, prior, args.no_repeat_exclude)
            g_ord, g_label = _grade_key(row["grade"])
            item = {
                **row,
                "status": status,
                "reasons": reasons,
                "tags": tags,
                "rank_components": {
                    "grade": row["grade"],
                    "grade_order": g_ord,
                    "grade_sort_label": g_label,
                    "room": row["room"],
                    "rs_score": row["rs_score"],
                },
            }
            ranked_rows.append(item)

    candidates = [r for r in ranked_rows if r["status"] == "stalk_candidate"]
    candidates.sort(key=rank_key)
    selected = candidates[: max(0, int(args.max_stalks))]

    # Observe notables: observe status, prefer AVOID with downgrade / earnings / high room
    observe = [r for r in ranked_rows if r["status"] == "observe"]
    observe.sort(
        key=lambda r: (
            0 if r["verdict"] == "AVOID" else 1,
            0 if "Earnings_Proximity_Flag=PASS" in (r["reasons"] or []) else 1,
            -(r["room"] or -1),
        )
    )

    # Write ranked_candidates.json
    ranked_payload = {
        "pack_dir": str(pack_dir),
        "contract_date": contract_date,
        "folder_date_hint": hint,
        "date_ok": date_ok,
        "date_note": date_note,
        "primary_missing": missing,
        "optional_missing": optional_missing,
        "prior_stalks": sorted(prior),
        "no_repeat_exclude": bool(args.no_repeat_exclude),
        "max_stalks": int(args.max_stalks),
        "tradeable_col_present": tradeable_col_present,
        "trigger_ticker_count": len(trigger_tickers),
        "counts": {
            "universe": len(ranked_rows),
            "stalk_candidate": len(candidates),
            "selected": len(selected),
            "observe": len(observe),
            "excluded": sum(1 for r in ranked_rows if r["status"] == "excluded"),
        },
        "selected_tickers": [r["ticker"] for r in selected],
        "rows": ranked_rows,
    }
    ranked_path = out_dir / "ranked_candidates.json"
    ranked_path.write_text(json.dumps(ranked_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # handoff_blocks.md
    if selected:
        handoff_text = "\n\n".join(handoff_block(r, r.get("tags") or []) for r in selected) + "\n"
    else:
        handoff_text = (
            "# cannot find — no stalk survivors\n"
            "Hard-exclude (incl. Tradeable when col present) + stalkable verdict (BUY/STALK) + Room≥1.0 left 0 names. Do not pad.\n"
        )
    handoff_path = out_dir / "handoff_blocks.md"
    handoff_path.write_text(handoff_text, encoding="utf-8")
    handoff_md5 = hashlib.md5(handoff_text.encode("utf-8")).hexdigest()

    # Draft + flags (soft-demote is a suggestion only; ranked/handoff stay pre-demote)
    import soft_final_draft as sfd

    run_date = sfd.parse_run_date(getattr(args, "run_date", None))
    tc = _s(getattr(args, "tc", None)) or sfd.derive_tc(run_date, contract_date)
    prior_dir, prior_pack_dir = sfd.discover_prior_dirs(
        out_dir,
        contract_date,
        getattr(args, "prior_dir", None),
        getattr(args, "prior_pack_dir", None),
    )
    draft_info = sfd.write_soft_final_artifacts(
        pack_dir=pack_dir,
        out_dir=out_dir,
        contract_date=contract_date,
        run_date=run_date,
        tc=tc,
        ranked_rows=ranked_rows,
        script_stalks=selected,
        verdicts=verdicts,
        book_raw=getattr(args, "book", None) or "TEM@72.21,UNTY@57.46",
        prior_dir=prior_dir,
        prior_pack_dir=prior_pack_dir,
        drive_folder=getattr(args, "drive_folder", None),
        optional_missing=optional_missing,
        handoff_text=handoff_text,
    )
    # Re-write ranked after enrich_row mutated rows (away_pct, quality_pass_total, …)
    ranked_path.write_text(json.dumps(ranked_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    stub_path = out_dir / "soft_final_stub.md"
    banned_hits = banned_scan(handoff_text) + list(draft_info.get("banned_token_hits_draft") or [])
    verify = {
        "pack_dir": str(pack_dir),
        "out_dir": str(out_dir),
        "contract_date": contract_date,
        "folder_date_hint": hint,
        "date_ok": date_ok,
        "date_note": date_note,
        "primary_ok": primary_ok,
        "primary_missing": missing,
        "optional_missing": optional_missing,
        "selected_tickers": [r["ticker"] for r in selected],
        "tradeable_col_present": tradeable_col_present,
        "tradeable_fail_in_stalks": [
            r["ticker"]
            for r in selected
            if tradeable_col_present
            and _s(r.get("tradeable")).upper() != "PASS"
            and not r.get("in_trigger")
        ],
        "thin_room": [r["ticker"] for r in selected if "thin_room" in (r.get("tags") or [])],
        "counts": ranked_payload["counts"],
        "handoff_blocks_md5": handoff_md5,
        "banned_token_hits": banned_hits,
        "exit_code_hint": 3 if primary_ok and date_ok and len(selected) == 0 else exit_code,
        "notable_excludes": {
            t: next((r["reasons"] for r in ranked_rows if r["ticker"] == t), None)
            for t in ("ECVT", "HOMB", "SSB", "XERS")
            if any(r["ticker"] == t for r in ranked_rows)
        },
        "draft_path": draft_info.get("draft_path"),
        "soft_demoted": draft_info.get("soft_demoted") or [],
        "soft_stalk_suggestion": draft_info.get("soft_stalk_suggestion") or [],
        "flag_counts": draft_info.get("flag_counts") or {},
        "banned_token_hits_draft": draft_info.get("banned_token_hits_draft") or [],
        "tc": tc,
        "run_date": run_date,
        "prior_dir": str(prior_dir) if prior_dir else None,
        "prior_pack_dir": str(prior_pack_dir) if prior_pack_dir else None,
    }
    verify_path = out_dir / "script_verify.json"
    verify_path.write_text(json.dumps(verify, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Summary stdout
    print("=== hermes_soft_final ===")
    print(f"pack: {pack_dir}")
    print(f"out:  {out_dir}")
    print(f"date: Contract={contract_date} hint={hint} ok={date_ok}")
    print(f"counts: {json.dumps(ranked_payload['counts'])}")
    print(f"stalks: {verify['selected_tickers']} thin_room={verify['thin_room']}")
    for t, reasons in (verify.get("notable_excludes") or {}).items():
        print(f"exclude {t}: {reasons}")
    print(f"handoff md5: {handoff_md5}")
    print(f"banned hits: {banned_hits or 'none'}")
    print(f"soft demote: {verify.get('soft_demoted')} remain={verify.get('soft_stalk_suggestion')}")
    print(f"flags: {json.dumps(verify.get('flag_counts') or {})}")
    print(
        f"wrote: {ranked_path.name}, {handoff_path.name}, handoff_blocks.script.md, "
        f"attention-3-picks.draft.md, attention-3-picks-notion.md, judgment_flags.json, "
        f"{stub_path.name}, {verify_path.name}"
    )

    if verify.get("tradeable_fail_in_stalks"):
        print(
            f"ERROR: Tradeable FAIL/empty leaked into stalks: {verify['tradeable_fail_in_stalks']}",
            file=sys.stderr,
        )
        return 2
    if exit_code == 2:
        return 2
    if len(selected) == 0:
        return 3
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Hermes Soft Final ranker + 書面語 draft + judgment flags")
    p.add_argument("--pack-dir", required=True, help="Local Hermes pack directory")
    p.add_argument("--out-dir", default=None, help="Output directory (default: dated parent / sibling)")
    p.add_argument("--max-stalks", type=int, default=3)
    p.add_argument("--prior-stalks", default="", help="Comma list T1,T2 for no-repeat remark")
    p.add_argument(
        "--no-repeat-exclude",
        action="store_true",
        help="If set, drop prior tickers from stalks (default: remark only)",
    )
    p.add_argument(
        "--prior-dir",
        default=None,
        help="Previous Soft out-dir (has ranked_candidates.json). Auto-discovered if out-dir is /workspace/second-brain/YYYY-MM-DD",
    )
    p.add_argument(
        "--prior-pack-dir",
        default=None,
        help="Previous Hermes pack directory",
    )
    p.add_argument(
        "--book",
        default="TEM@72.21,UNTY@57.46",
        help="Book names as TICKER@entry,TICKER@entry (never auto-wake 模擬倉)",
    )
    p.add_argument(
        "--drive-folder",
        default=None,
        help="Drive folder URL or id for PINNED / header",
    )
    p.add_argument(
        "--tc",
        default=None,
        help="TC id (default: TC-YYYYMMDD-SB-novN from run date + contract month/day)",
    )
    p.add_argument(
        "--run-date",
        default=None,
        help="Run date YYYY-MM-DD (default: today Asia/Hong_Kong)",
    )
    args = p.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
