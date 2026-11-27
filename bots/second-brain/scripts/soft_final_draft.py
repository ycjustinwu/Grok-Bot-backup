#!/usr/bin/env python3
"""Draft a 書面語 Soft Final + judgment_flags from script-ranked Hermes rows.

Called by hermes_soft_final.py (single CLI). Soft-demote is a draft suggestion only:
ranked_candidates.json / handoff_blocks.md stay pre-LLM script stalks.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

HKT = ZoneInfo("Asia/Hong_Kong")
STRONG_GRADES = {"A", "A+"}
MONTH_ABBR = {
    1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "jun",
    7: "jul", 8: "aug", 9: "sep", 10: "oct", 11: "nov", 12: "dec",
}
MONTH_TITLE = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
}
FLIP_FIELDS = (
    ("tradeable", "Tradeable"),
    ("risk_ok", "Risk_OK"),
    ("entry_feasible", "Entry_Feasible"),
    ("verdict", "verdict"),
)


def _h():
    import hermes_soft_final as h
    return h


def _s(val: Any, default: str = "") -> str:
    return _h()._s(val, default)


def _f(val: Any) -> float | None:
    return _h()._f(val)


def yn_flag(val: Any) -> str:
    if isinstance(val, bool):
        return "Y" if val else "N"
    text = _s(val).upper()
    if text in {"Y", "YES", "TRUE", "1"}:
        return "Y"
    if text in {"N", "NO", "FALSE", "0"}:
        return "N"
    if text in {"", "NA", "N/A", "NONE", "—"}:
        return ""
    return text


def parse_quality_marks(detail: str) -> tuple[int | None, int | None, str]:
    text = _s(detail)
    if not text:
        return None, None, ""
    parts = [p.strip() for p in text.split("|") if p.strip()]
    if not parts:
        return None, None, ""
    plus = 0
    total = 0
    for p in parts:
        if p[0] in "+-?":
            total += 1
            if p[0] == "+":
                plus += 1
    if total == 0:
        return None, None, ""
    return plus, total, f"{plus}/{total}"


def file_md5(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.md5()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fmt_copy(val: Any) -> str:
    text = _s(val)
    return text if text else "—"


def fmt_priority(val: Any) -> str:
    num = _f(val)
    if num is None:
        return "—"
    if abs(num - round(num)) < 1e-9:
        return str(int(round(num)))
    return _s(val)


def fmt_days(val: Any) -> str | None:
    num = _f(val)
    if num is None:
        return None
    if abs(num - round(num)) < 1e-9:
        return str(int(round(num)))
    return _s(val)


def today_hkt() -> date:
    return datetime.now(HKT).date()


def parse_run_date(raw: str | None) -> str:
    if raw and _s(raw):
        text = _s(raw)
        return date.fromisoformat(text[:10]).isoformat()
    return today_hkt().isoformat()


def derive_tc(run_date: str, contract_date: str) -> str:
    run_compact = run_date.replace("-", "")
    if contract_date:
        d = date.fromisoformat(contract_date)
        return f"TC-{run_compact}-SB-{MONTH_ABBR[d.month]}{d.day}"
    return f"TC-{run_compact}-SB"


def folder_label(contract_date: str) -> str:
    if not contract_date:
        return "Hermes"
    d = date.fromisoformat(contract_date)
    return f"{MONTH_TITLE[d.month]} {d.day}"


def drive_link(raw: str | None) -> tuple[str, str]:
    text = _s(raw)
    if not text:
        return "", ""
    if text.startswith("http://") or text.startswith("https://"):
        m = re.search(r"/folders/([A-Za-z0-9_-]+)", text)
        return text, (m.group(1) if m else "")
    return f"https://drive.google.com/drive/folders/{text}", text


def parse_book(raw: str | None) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for part in (raw or "").split(","):
        part = part.strip()
        if not part:
            continue
        if "@" in part:
            ticker, px = part.split("@", 1)
            items.append({"ticker": ticker.strip().upper(), "entry": px.strip(), "raw": part})
        else:
            items.append({"ticker": part.upper(), "entry": None, "raw": part})
    return items


def enrich_row(row: dict[str, Any]) -> dict[str, Any]:
    close = _f(row.get("close"))
    entry = _f(row.get("entry_ref"))
    stop = _f(row.get("invalidate_below"))
    risk_pct = _f(row.get("risk_pct_plan"))
    away = None
    if close not in (None, 0) and entry is not None:
        away = abs(close - entry) / close * 100.0
    plus, total, frac = parse_quality_marks(_s(row.get("quality_detail")))
    l_near = False
    if entry is not None and stop is not None:
        if abs(entry - stop) / max(abs(entry), 1e-9) < 0.005:
            l_near = True
    if risk_pct is not None and risk_pct < 0.5:
        l_near = True
    row["close_num"] = close
    row["entry_num"] = entry
    row["stop_num"] = stop
    row["away_pct"] = away
    row["quality_pass"] = plus
    row["quality_total"] = total
    row["quality_pass_total"] = frac
    row["l_near_sl"] = bool(l_near)
    row["minervini_trend_yn"] = yn_flag(row.get("minervini_trend"))
    row["minervini_stage2_yn"] = yn_flag(row.get("minervini_stage2"))
    row["leader_ok"] = _s(row.get("leader_ok")).upper()
    return row


def soft_demote_reasons(row: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if _s(row.get("leader_ok")).upper() == "FAIL":
        reasons.append("leader_wait")
    away = row.get("away_pct")
    if away is not None and away >= 5:
        reasons.append("fillable_gate")
    if row.get("l_near_sl"):
        reasons.append("l_near_sl")
    room = row.get("room")
    tags = row.get("tags") or []
    thin = "thin_room" in tags or (room is not None and 1.0 <= room < 2.0)
    grade = _s(row.get("grade")).upper()
    if thin and grade not in STRONG_GRADES:
        reasons.append("thin_room_weak_grade")
    return reasons


def parse_index_md(text: str) -> dict[str, Any]:
    claimed_counts: dict[str, int] = {}
    ticker_universe = None
    story_claim = None
    asetup_claimed = None
    asetup_raw: list[str] = []
    tickers_line = ""
    lines = text.splitlines()
    tickers_re = re.compile(r"tickers:\s*\*?\*?(\d+)\s*→\s*(.+)", re.I)
    count_re = re.compile(r"(BUY|STALK|WATCH|AVOID|LEADER_WAIT)\s+(\d+)", re.I)
    story_re = re.compile(
        r"no story was commissioned|story_status:\s*`?not_required`?|no BUY ticket means no story",
        re.I,
    )
    heading_re = re.compile(r"^##\s+A_SETUP rows", re.I)
    none_re = re.compile(r"^[-*]\s*(none|無)\s*$", re.I)

    for i, line in enumerate(lines):
        m = tickers_re.search(line)
        if m:
            ticker_universe = int(m.group(1))
            tickers_line = line.strip()
            for mm in count_re.finditer(m.group(2)):
                claimed_counts[mm.group(1).upper()] = int(mm.group(2))
        if story_re.search(line) and story_claim is None:
            story_claim = line.strip().strip("- ").strip()
        if heading_re.search(line):
            collected: list[str] = []
            for nxt in lines[i + 1 :]:
                if nxt.startswith("#"):
                    break
                if nxt.strip():
                    collected.append(nxt.strip())
            asetup_raw = collected
            if collected and all(
                none_re.match(x) or x.lower() in {"none", "- none", "無"} for x in collected
            ):
                asetup_claimed = 0
            elif collected:
                asetup_claimed = len(collected)

    if not claimed_counts:
        for line in lines:
            found = list(count_re.finditer(line))
            labels = {mm.group(1).upper() for mm in found}
            if found and {"BUY", "STALK"} & labels and len(found) >= 2:
                for mm in found:
                    claimed_counts[mm.group(1).upper()] = int(mm.group(2))
                if not tickers_line:
                    tickers_line = line.strip()
                break

    return {
        "ticker_universe": ticker_universe,
        "claimed_counts": claimed_counts,
        "tickers_line": tickers_line,
        "story_claim": story_claim,
        "asetup_claimed": asetup_claimed,
        "asetup_raw": asetup_raw,
    }


def discover_stories(pack_dir: Path) -> list[dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}

    def bucket(ticker: str) -> dict[str, Any]:
        key = ticker.upper()
        return found.setdefault(
            key, {"ticker": key, "stance": None, "files": [], "sources": []}
        )

    for path in sorted(pack_dir.glob("*_story.json")):
        ticker = path.name[: -len("_story.json")].upper()
        stance = None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            ticker = _s(data.get("ticker") or ticker).upper()
            for key in ("conviction", "stance", "conclusion", "story_stance"):
                if _s(data.get(key)):
                    stance = _s(data.get(key)).upper()
                    break
        except (OSError, json.JSONDecodeError):
            pass
        item = bucket(ticker)
        item["files"].append(str(path))
        item["sources"].append(path.name)
        if stance and not item["stance"]:
            item["stance"] = stance

    for path in sorted(pack_dir.glob("*_投資快報.md")):
        ticker = path.name.split("_")[0].upper()
        text = path.read_text(encoding="utf-8", errors="replace")
        stance = None
        m = re.search(r"CONVICTION\s*[:：]\s*([A-Za-z]+)", text)
        if m:
            stance = m.group(1).upper()
        else:
            m = re.search(r"敘事信念\s*[:：]\s*([A-Za-z]+)", text)
            if m:
                stance = m.group(1).upper()
        item = bucket(ticker)
        item["files"].append(str(path))
        item["sources"].append(path.name)
        if stance and not item["stance"]:
            item["stance"] = stance

    for path in sorted(pack_dir.glob("*_search_log.json")):
        ticker = path.name[: -len("_search_log.json")].upper()
        item = bucket(ticker)
        item["files"].append(str(path))
        item["sources"].append(path.name)

    out = []
    for item in found.values():
        item["note"] = "no further S4 unless Justin asks"
        out.append(item)
    out.sort(key=lambda x: x["ticker"])
    return out


def discover_context(contract_date: str) -> dict[str, Any]:
    out: dict[str, Any] = {
        "regime": None,
        "brief": None,
        "stockbee": [],
        "market_master": [],
        "notes": [],
    }
    if not contract_date:
        out["notes"].append("contract_date missing; context paths not discovered")
        return out

    ma = Path("/workspace/market-awareness") / contract_date
    if ma.is_dir():
        regime = ma / f"regime-daily-{contract_date}.md"
        if regime.exists():
            out["regime"] = str(regime)
        else:
            cands = [
                p
                for p in sorted(ma.glob("regime-daily-*.md"))
                if ".compact" not in p.name and ".table" not in p.name
            ]
            if cands:
                out["regime"] = str(cands[0])
            else:
                out["notes"].append(f"regime missing under {ma}")
        for name in ("stockbee-t2108.xlsx", "stockbee-1a.json", "stockbee-monitor.xlsx"):
            p = ma / name
            if p.exists():
                out["stockbee"].append(str(p))
        out["market_master"] = [str(p) for p in sorted(ma.glob("_mm_*.csv"))]
        if not out["stockbee"]:
            out["notes"].append(f"Stockbee missing under {ma}")
    else:
        out["notes"].append(f"regime dir missing: {ma}")

    brief_root = Path("/workspace/us-market-daily-brief")
    if brief_root.is_dir():
        hits: list[Path] = []
        for p in brief_root.rglob("*"):
            if not p.is_file():
                continue
            if contract_date not in p.name:
                continue
            if p.suffix.lower() not in {".md", ".html"}:
                continue
            if p.name.startswith("_"):
                continue
            hits.append(p)

        def score(p: Path) -> tuple[int, int, int]:
            name = p.name.lower()
            exact = name in {
                f"us brief-{contract_date}.md",
                f"us-brief-{contract_date}.md",
            }
            return (0 if exact else 1, 0 if "brief" in name else 2, len(str(p)))

        if hits:
            hits.sort(key=score)
            out["brief"] = str(hits[0])
        else:
            out["notes"].append(
                f"US brief matching {contract_date} not found under {brief_root}"
            )
    else:
        out["notes"].append("US brief tree missing")
    return out


def discover_prior_dirs(
    out_dir: Path,
    contract_date: str,
    prior_dir: str | None,
    prior_pack_dir: str | None,
) -> tuple[Path | None, Path | None]:
    pdir = Path(prior_dir).expanduser().resolve() if prior_dir else None
    ppack = Path(prior_pack_dir).expanduser().resolve() if prior_pack_dir else None

    if pdir is None and re.fullmatch(r"20\d{2}-\d{2}-\d{2}", out_dir.name):
        try:
            prev = date.fromisoformat(out_dir.name) - timedelta(days=1)
            cand = out_dir.parent / prev.isoformat()
            if (cand / "ranked_candidates.json").exists():
                pdir = cand.resolve()
        except ValueError:
            pass

    prior_contract = None
    if pdir and (pdir / "ranked_candidates.json").exists():
        try:
            meta = json.loads((pdir / "ranked_candidates.json").read_text(encoding="utf-8"))
            prior_contract = _s(meta.get("contract_date")) or None
        except (OSError, json.JSONDecodeError):
            prior_contract = None
    if prior_contract is None and contract_date:
        try:
            prior_contract = (date.fromisoformat(contract_date) - timedelta(days=1)).isoformat()
        except ValueError:
            prior_contract = None

    if ppack is None and prior_contract:
        candidates = [
            Path("/workspace/second-brain/hermes-packs") / f"hermes-{prior_contract}",
            Path("/workspace/second-brain") / prior_contract / f"hermes-{prior_contract}",
        ]
        if pdir:
            candidates.append(pdir / f"hermes-{prior_contract}")
            for child in pdir.glob("hermes-*"):
                candidates.append(child)
        for cand in candidates:
            if (cand / "Contract_US.csv").exists():
                ppack = cand.resolve()
                break
    return pdir, ppack


def load_prior_state(
    prior_dir: Path | None,
    prior_pack_dir: Path | None,
) -> dict[str, Any]:
    state: dict[str, Any] = {
        "available": False,
        "prior_dir": str(prior_dir) if prior_dir else None,
        "prior_pack_dir": str(prior_pack_dir) if prior_pack_dir else None,
        "prior_contract_date": None,
        "rows": {},
        "stalk_candidates": [],
        "soft_stalk_suggestion": [],
        "universe": [],
    }
    rows: dict[str, dict[str, Any]] = {}
    if prior_dir and (prior_dir / "ranked_candidates.json").exists():
        try:
            meta = json.loads((prior_dir / "ranked_candidates.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            meta = {}
        state["prior_contract_date"] = _s(meta.get("contract_date")) or None
        for row in meta.get("rows") or []:
            ticker = _s(row.get("ticker")).upper()
            if ticker:
                rows[ticker] = dict(row)
        selected = [_s(t).upper() for t in (meta.get("selected_tickers") or [])]
        stalks = [
            _s(r.get("ticker")).upper()
            for r in (meta.get("rows") or [])
            if r.get("status") == "stalk_candidate"
        ]
        state["stalk_candidates"] = selected or stalks
        state["universe"] = list(rows.keys())
        state["available"] = True
        flags_path = prior_dir / "judgment_flags.json"
        if flags_path.exists():
            try:
                flags = json.loads(flags_path.read_text(encoding="utf-8"))
                sugg = flags.get("soft_stalk_suggestion") or flags.get("soft_stalks") or []
                state["soft_stalk_suggestion"] = [
                    _s(x).upper() if isinstance(x, str) else _s(x.get("ticker")).upper()
                    for x in sugg
                ]
            except (OSError, json.JSONDecodeError):
                pass

    if prior_pack_dir and (prior_pack_dir / "Contract_US.csv").exists():
        try:
            import pandas as pd

            contract = pd.read_csv(prior_pack_dir / "Contract_US.csv", keep_default_na=False)
            for _, crow in contract.iterrows():
                ticker = _s(crow.get("Ticker")).upper()
                if not ticker:
                    continue
                item = rows.setdefault(ticker, {"ticker": ticker})
                mappings = (
                    ("Close", "close", False),
                    ("Leader_OK", "leader_ok", True),
                    ("Leader_Why", "leader_why", False),
                    ("Tradeable", "tradeable", True),
                    ("Risk_OK", "risk_ok", True),
                    ("Entry_Feasible", "entry_feasible", True),
                    ("Room_To_Supply_R", "room", False),
                    ("Entry_Ref", "entry_ref", False),
                    ("Invalidate_Below", "invalidate_below", False),
                    ("Candidate_Class", "candidate_class", False),
                    ("Setup_Quality_Grade", "grade", False),
                )
                for src, dest, upper in mappings:
                    if dest not in item or item.get(dest) in (None, ""):
                        if src == "Room_To_Supply_R":
                            item[dest] = _f(crow.get(src))
                        else:
                            val = _s(crow.get(src))
                            item[dest] = val.upper() if upper else val
            if not state["prior_contract_date"] and len(contract):
                dates = sorted({_s(d) for d in contract["Date"].tolist() if _s(d)})
                if dates:
                    state["prior_contract_date"] = dates[0]
            if not state["universe"]:
                state["universe"] = list(rows.keys())
                state["available"] = True
        except Exception:
            pass

    for row in rows.values():
        if "room" in row and row.get("room") is not None and not isinstance(row.get("room"), float):
            row["room"] = _f(row.get("room"))
        enrich_row(row)
    state["rows"] = rows

    if not state["soft_stalk_suggestion"] and state["stalk_candidates"]:
        sugg: list[str] = []
        for ticker in state["stalk_candidates"]:
            row = rows.get(ticker) or {"ticker": ticker}
            if not soft_demote_reasons(row):
                sugg.append(ticker)
        state["soft_stalk_suggestion"] = sugg
    return state


def index_conflicts(
    pack_dir: Path,
    ranked_rows: list[dict[str, Any]],
    verdicts: dict[str, dict],
    stories: list[dict[str, Any]],
) -> dict[str, Any]:
    path = pack_dir / "index.md"
    parsed: dict[str, Any] = {}
    if path.exists():
        raw = path.read_text(encoding="utf-8", errors="replace")
        parsed = parse_index_md(raw)

    if verdicts:
        verdict_counts = Counter(_s(v.get("verdict")).upper() or "EMPTY" for v in verdicts.values())
    else:
        verdict_counts = Counter(_s(r.get("verdict")).upper() or "EMPTY" for r in ranked_rows)
    asetup_tickers = [
        r["ticker"] for r in ranked_rows if _s(r.get("candidate_class")).upper() == "A_SETUP"
    ]
    conflicts: list[dict[str, Any]] = []

    claimed_a = parsed.get("asetup_claimed")
    if claimed_a is not None and claimed_a != len(asetup_tickers):
        conflicts.append(
            {
                "kind": "a_setup_count",
                "index": "A_SETUP rows: none" if claimed_a == 0 else parsed.get("asetup_raw"),
                "actual": len(asetup_tickers),
                "tickers": asetup_tickers,
                "note": f"index A_SETUP {claimed_a} vs pack {len(asetup_tickers)}",
            }
        )

    claimed = parsed.get("claimed_counts") or {}
    if claimed:
        actual_map = {k: int(verdict_counts.get(k, 0)) for k in set(claimed) | set(verdict_counts)}
        mismatched = {
            k: {"index": claimed.get(k, 0), "actual": actual_map.get(k, 0)}
            for k in sorted(set(claimed) | {"BUY", "STALK"})
            if claimed.get(k, 0) != actual_map.get(k, 0)
        }
        if mismatched:
            conflicts.append(
                {
                    "kind": "verdict_counts",
                    "index": claimed,
                    "actual": {k: int(verdict_counts.get(k, 0)) for k in sorted(verdict_counts)},
                    "mismatched": mismatched,
                    "note": "verdicts win; never treat index BUY as buyable",
                }
            )

    story_claim = parsed.get("story_claim")
    if story_claim and stories:
        conflicts.append(
            {
                "kind": "story_commissioned",
                "index": story_claim,
                "actual": [s["ticker"] for s in stories],
                "files": [f for s in stories for f in s.get("sources") or []],
                "note": "story already on disk; index claim is false",
            }
        )

    return {
        "has_conflict": bool(conflicts),
        "conflicts": conflicts,
        "parsed": {k: v for k, v in parsed.items() if k != "asetup_raw" or v},
        "rule": "verdicts win; never treat index BUY as buyable",
    }


def max_stalk_room(script_stalks: list[dict[str, Any]]) -> float | None:
    rooms = [r["room"] for r in script_stalks if r.get("room") is not None]
    return max(rooms) if rooms else None


def do_not_upgrade_rows(
    ranked_rows: list[dict[str, Any]],
    script_stalks: list[dict[str, Any]],
    prior: dict[str, Any],
) -> list[dict[str, Any]]:
    cap = max_stalk_room(script_stalks)
    prior_rows = prior.get("rows") or {}
    flagged: list[dict[str, Any]] = []
    stalk_names = {r["ticker"] for r in script_stalks}
    for row in ranked_rows:
        ticker = row["ticker"]
        if ticker in stalk_names:
            continue
        verdict = _s(row.get("verdict")).upper()
        if verdict not in {"WATCH", "AVOID"}:
            continue
        reasons: list[str] = []
        tradeable = _s(row.get("tradeable")).upper()
        grade = _s(row.get("grade")).upper()
        room = row.get("room")
        thicker = cap is not None and room is not None and room > cap
        if thicker and tradeable == "PASS":
            reasons.append("thicker_room")
        if thicker and grade in STRONG_GRADES:
            reasons.append("thicker_room_strong_grade")
        prior_row = prior_rows.get(ticker)
        prior_t = _s((prior_row or {}).get("tradeable")).upper() if prior_row else ""
        if prior_row and prior_t != "PASS" and tradeable == "PASS":
            reasons.append("tradeable_flipped_pass")
        if not reasons:
            continue
        flagged.append(
            {
                "ticker": ticker,
                "verdict": verdict,
                "grade": row.get("grade"),
                "room": room,
                "tradeable": tradeable,
                "tradeable_why": _s(row.get("tradeable_why")),
                "candidate_class": _s(row.get("candidate_class")),
                "reasons": reasons,
                "note": "never upgrade WATCH/AVOID",
            }
        )
    def _dnu_key(x: dict[str, Any]):
        reasons = x.get("reasons") or []
        pass_thicker = "thicker_room" in reasons  # Tradeable PASS + thicker room
        flipped = "tradeable_flipped_pass" in reasons
        return (0 if pass_thicker else 1, 0 if flipped else 1, -(x["room"] or -1), x["ticker"])

    flagged.sort(key=_dnu_key)
    return flagged


def prior_changes(
    ranked_rows: list[dict[str, Any]],
    script_stalks: list[dict[str, Any]],
    prior: dict[str, Any],
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "available": bool(prior.get("available")),
        "prior_dir": prior.get("prior_dir"),
        "prior_pack_dir": prior.get("prior_pack_dir"),
        "prior_contract_date": prior.get("prior_contract_date"),
        "room_collapse": [],
        "flips": [],
        "dropped_from_universe": [],
        "window_closed": [],
    }
    if not prior.get("available"):
        return out

    today = {r["ticker"]: r for r in ranked_rows}
    prior_rows = prior.get("rows") or {}
    today_names = set(today)
    prior_universe = prior.get("universe") or list(prior_rows.keys())
    prior_stalks = set(prior.get("stalk_candidates") or [])
    prior_sugg = set(prior.get("soft_stalk_suggestion") or [])

    notable_drop: list[str] = []
    extra_keep = set(prior.get("book_tickers") or [])
    for ticker in prior_universe:
        if ticker in today_names:
            continue
        prow = prior_rows.get(ticker) or {"ticker": ticker}
        verdict = _s(prow.get("verdict")).upper()
        tradeable = _s(prow.get("tradeable")).upper()
        grade = _s(prow.get("grade")).upper()
        room = prow.get("room")
        if isinstance(room, str):
            room = _f(room)
        notable = (
            ticker in prior_stalks
            or ticker in prior_sugg
            or ticker in extra_keep
            or verdict in {"STALK", "BUY"}
            or (tradeable == "PASS" and verdict in {"WATCH", "STALK", "BUY"})
            or (
                grade in STRONG_GRADES
                and verdict == "WATCH"
                and room is not None
                and room >= 2.0
            )
        )
        if notable:
            notable_drop.append(ticker)
    out["dropped_from_universe"] = sorted(notable_drop)

    closest_prior = list(prior.get("soft_stalk_suggestion") or [])
    if not closest_prior:
        closest_prior = list(prior.get("stalk_candidates") or [])

    for ticker, prow in prior_rows.items():
        trow = today.get(ticker)
        if not trow:
            continue
        pr = prow.get("room")
        tr = trow.get("room")
        if isinstance(pr, str):
            pr = _f(pr)
        if pr is not None and tr is not None and tr < pr and (tr < 1.0 or (pr - tr) >= 0.5):
            out["room_collapse"].append({"ticker": ticker, "from": pr, "to": tr})
        for field, label in FLIP_FIELDS:
            a = _s(prow.get(field)).upper()
            b = _s(trow.get(field)).upper()
            if a and b and a != b:
                out["flips"].append({"ticker": ticker, "field": label, "from": a, "to": b})

        was_stalk = ticker in prior_stalks or ticker in prior_sugg
        trad_today = _s(trow.get("tradeable")).upper()
        trad_prior = _s(prow.get("tradeable")).upper()
        closed = False
        why_parts: list[str] = []
        if was_stalk and tr is not None and tr < 1.0:
            closed = True
            why_parts.append(f"room {pr}R→{tr}R")
        if was_stalk and trad_prior == "PASS" and trad_today == "FAIL":
            closed = True
            why_parts.append("Tradeable PASS→FAIL")
        prior_v = _s(prow.get("verdict")).upper()
        today_v = _s(trow.get("verdict")).upper()
        if was_stalk and today_v not in {"BUY", "STALK"} and prior_v in {"BUY", "STALK"}:
            closed = True
            why_parts.append(f"verdict {prior_v}→{today_v}")
        if closed:
            out["window_closed"].append(
                {
                    "ticker": ticker,
                    "why": "; ".join(why_parts) or "prior stalk window closed",
                    "room_from": pr,
                    "room_to": tr,
                    "tradeable_from": trad_prior,
                    "tradeable_to": trad_today,
                    "was_closest": ticker in closest_prior,
                    "note": (
                        "yesterday's closest name whose window closed"
                        if ticker in closest_prior
                        else "prior script stalk window closed"
                    ),
                }
            )
    return out


def book_remarks(
    book: list[dict[str, Any]],
    ranked_rows: list[dict[str, Any]],
    universe_size: int,
) -> list[dict[str, Any]]:
    by = {r["ticker"]: r for r in ranked_rows}
    out: list[dict[str, Any]] = []
    for item in book:
        ticker = item["ticker"]
        row = by.get(ticker)
        remark = {
            "ticker": ticker,
            "book_entry": item.get("entry"),
            "in_universe": bool(row),
            "universe_size": universe_size,
            "note": "never auto-wake 模擬倉",
        }
        if row:
            remark.update(
                {
                    "verdict": row.get("verdict"),
                    "grade": row.get("grade"),
                    "room": row.get("room"),
                    "tradeable": row.get("tradeable"),
                    "entry_feasible": row.get("entry_feasible"),
                    "close": row.get("close"),
                }
            )
        else:
            remark["status"] = f"不在本包 {universe_size} 名宇宙"
        out.append(remark)
    return out


def leftover_notes(
    ranked_rows: list[dict[str, Any]],
    already: set[str],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in ranked_rows:
        ticker = row["ticker"]
        if ticker in already:
            continue
        klass = _s(row.get("candidate_class")).upper()
        grade = _s(row.get("grade")).upper()
        tradeable = _s(row.get("tradeable")).upper()
        interesting = False
        why: list[str] = []
        if klass == "B_LEADER_WAIT":
            interesting = True
            why.append("B_LEADER_WAIT leftover")
        if grade in STRONG_GRADES and tradeable != "PASS":
            interesting = True
            why.append(f"Grade {row.get('grade')} but not tradeable")
        if not interesting:
            continue
        out.append(
            {
                "ticker": ticker,
                "verdict": row.get("verdict"),
                "grade": row.get("grade"),
                "room": row.get("room"),
                "tradeable": tradeable,
                "tradeable_why": _s(row.get("tradeable_why")),
                "candidate_class": klass,
                "leader_ok": row.get("leader_ok"),
                "why": why,
            }
        )
    out.sort(key=lambda x: (0 if "B_LEADER_WAIT" in (x.get("why") or []) else 1, x["ticker"]))
    return out[:6]


def build_judgment_flags(
    *,
    pack_dir: Path,
    out_dir: Path,
    contract_date: str,
    run_date: str,
    tc: str,
    ranked_rows: list[dict[str, Any]],
    script_stalks: list[dict[str, Any]],
    verdicts: dict[str, dict],
    book: list[dict[str, Any]],
    prior: dict[str, Any],
    drive_url: str,
    drive_id: str,
    context: dict[str, Any],
) -> dict[str, Any]:
    stories = discover_stories(pack_dir)
    story_by = {s["ticker"]: s for s in stories}

    demote: list[dict[str, Any]] = []
    remain: list[dict[str, Any]] = []
    for row in script_stalks:
        reasons = soft_demote_reasons(row)
        story = story_by.get(row["ticker"])
        entry = {
            "ticker": row["ticker"],
            "reasons": reasons,
            "grade": row.get("grade"),
            "quality_pass_total": row.get("quality_pass_total"),
            "room": row.get("room"),
            "away_pct": row.get("away_pct"),
            "l_near_sl": bool(row.get("l_near_sl")),
            "leader_ok": row.get("leader_ok"),
            "leader_why": _s(row.get("leader_why")),
            "tradeable": row.get("tradeable"),
            "verdict": row.get("verdict"),
            "story_stance": (story or {}).get("stance"),
            "story_is_info_only": True,
        }
        if reasons:
            demote.append(entry)
        else:
            remain.append(entry)

    if verdicts:
        verdict_counts = Counter(_s(v.get("verdict")).upper() or "EMPTY" for v in verdicts.values())
    else:
        verdict_counts = Counter(_s(r.get("verdict")).upper() or "EMPTY" for r in ranked_rows)
    class_counts = Counter(_s(r.get("candidate_class")).upper() or "EMPTY" for r in ranked_rows)
    tradeable_counts = Counter(_s(r.get("tradeable")).upper() or "EMPTY" for r in ranked_rows)

    conflicts = index_conflicts(pack_dir, ranked_rows, verdicts, stories)
    dnu = do_not_upgrade_rows(ranked_rows, script_stalks, prior)
    prior = dict(prior)
    prior["book_tickers"] = [b["ticker"] for b in book]
    changes = prior_changes(ranked_rows, script_stalks, prior)
    books = book_remarks(book, ranked_rows, len(ranked_rows))
    already = {r["ticker"] for r in script_stalks} | {x["ticker"] for x in dnu} | {b["ticker"] for b in books}
    leftovers = leftover_notes(ranked_rows, already)

    closest_vs_quality = None
    if len(script_stalks) >= 2:
        by_grade = sorted(script_stalks, key=lambda r: _h()._grade_key(r.get("grade") or "NA"))
        highest = by_grade[0]
        remain_tickers = [x["ticker"] for x in remain]
        highest_demoted = any(d["ticker"] == highest["ticker"] for d in demote)
        if highest_demoted and remain_tickers:
            closest_vs_quality = {
                "highest_quality": highest["ticker"],
                "highest_grade": highest.get("grade"),
                "highest_demoted_reasons": next(
                    d["reasons"] for d in demote if d["ticker"] == highest["ticker"]
                ),
                "closest_remaining": remain_tickers[0],
                "note": "最高品質者已建議降級；最接近 Soft-stalk 者並非質素最高者",
            }

    return {
        "contract_date": contract_date,
        "run_date": run_date,
        "tc": tc,
        "out_dir": str(out_dir),
        "pack_dir": str(pack_dir),
        "universe_size": len(ranked_rows),
        "verdicts_counts": dict(verdict_counts),
        "candidate_class_counts": dict(class_counts),
        "tradeable_counts": dict(tradeable_counts),
        "stalk_candidate": [r["ticker"] for r in script_stalks],
        "soft_demote": demote,
        "suggest_demote": demote,
        "soft_stalk_suggestion": [r["ticker"] for r in remain],
        "index_conflicts": conflicts,
        "story_in_pack": stories,
        "do_not_upgrade": dnu,
        "prior_changes": changes,
        "book_remarks": books,
        "leftovers": leftovers,
        "closest_vs_quality": closest_vs_quality,
        "drive_folder_url": drive_url,
        "drive_folder_id": drive_id,
        "context_paths": {
            "regime": context.get("regime"),
            "brief": context.get("brief"),
            "stockbee": context.get("stockbee") or [],
            "market_master": context.get("market_master") or [],
            "notes": context.get("notes") or [],
        },
        "llm_rules": {
            "never_upgrade_watch_avoid": True,
            "verdicts_win": True,
            "never_treat_index_buy_as_buyable": True,
            "no_further_s4_unless_asked": True,
            "never_auto_wake_sim_book": True,
            "may_confirm_or_undo_soft_demote": True,
            "do_not_recap_regime_brief_mm_rs": True,
            "do_not_rerank_from_raw_csv": True,
            "story_stance_is_info_not_auto_demote": True,
        },
    }


DEMOTE_REASON_ZH = {
    "leader_wait": "Leader_OK FAIL，依 11/07 規則改列 leader_wait",
    "fillable_gate": "距收盤已達 ≥5%，觸及自動觀察門檻，僅作觀察",
    "l_near_sl": "限價與止損貼近（差距 <0.5% 或風險 <0.5%）",
    "thin_room_weak_grade": "thin_room 且 Grade 非 A／A+，不足以討論薄空間",
}
DEMOTE_GAP_ZH = {
    "leader_wait": "龍頭",
    "fillable_gate": "時機",
    "l_near_sl": "止損結構",
    "thin_room_weak_grade": "品質／空間",
}
CANT_MISS_ZH = {
    "leader_wait": "須先成為龍頭（Leader_OK PASS），且硬空間接近 ≥2R",
    "fillable_gate": "限價須靠近收盤（偏離 <5%）",
    "l_near_sl": "限價與止損須拉開，不再貼近",
    "thin_room_weak_grade": "品質與硬空間需轉厚（接近 ≥2R 且 Grade 轉強）",
}


def grade_cell(row: dict[str, Any]) -> str:
    grade = _s(row.get("grade")) or "—"
    frac = _s(row.get("quality_pass_total"))
    pri = fmt_priority(row.get("priority_score"))
    head = f"**{grade} {frac}**" if frac else f"**{grade}**"
    if pri != "—":
        return f"{head} · {pri}"
    return head


def away_cell(row: dict[str, Any]) -> str:
    away = row.get("away_pct")
    if away is None:
        return "—"
    gate = "已達 ≥5% 自動觀察門檻" if away >= 5 else "未達 ≥5% 自動觀察門檻"
    near = "限價與止損貼近" if row.get("l_near_sl") else "限價與止損並不貼近"
    pct = "0%" if abs(away) < 1e-9 else f"{away:.2f}%"
    entry = _f(row.get("entry_ref"))
    close = _f(row.get("close"))
    if entry is not None and close is not None and entry < close - 1e-9:
        rel = "限價低於收盤 "
    elif entry is not None and close is not None and entry > close + 1e-9:
        rel = "限價高於收盤 "
    else:
        rel = "限價等於收盤 "
    return f"{rel}**{pct}**（{gate}）· {near}"


def room_cell(row: dict[str, Any], *, soft: bool = False) -> str:
    if soft:
        level = fmt_copy(row.get("supply_soft_level"))
        rr = _s(row.get("room_to_soft_r"))
        if level in {"", "—"} and not rr:
            return "無（NONE_ABOVE）"
        src = fmt_copy(row.get("supply_soft_source"))
        src_bit = f"（{src}）" if src != "—" else ""
        if rr:
            return f"{rr}R @ {level}{src_bit}"
        return f"{level}{src_bit}"
    room = row.get("room")
    room_s = fmt_copy(room)
    thin = " thin" if room is not None and 1.0 <= room < 2.0 else ""
    return f"**{room_s}R{thin}** → {fmt_copy(row.get('supply_level'))}（{fmt_copy(row.get('supply_source'))}）"


def leader_cell(row: dict[str, Any]) -> str:
    ok = _s(row.get("leader_ok")) or "—"
    why = _s(row.get("leader_why"))
    trend = row.get("minervini_trend_yn") or yn_flag(row.get("minervini_trend")) or "—"
    stage = row.get("minervini_stage2_yn") or yn_flag(row.get("minervini_stage2")) or "—"
    why_bit = f"（{why}）" if why else ""
    return f"**{ok}**{why_bit}· Minervini **{trend}** · Stage2 **{stage}**"


def earnings_cell(row: dict[str, Any]) -> str:
    flag = fmt_copy(row.get("earnings_flag"))
    dt = fmt_copy(row.get("earnings_date"))
    days = fmt_days(row.get("days_to_earnings"))
    if days:
        return f"{flag} {dt}（{days} 個交易日）"
    return f"{flag} {dt}".strip()


def risk_cell(row: dict[str, Any]) -> str:
    return (
        f"{fmt_copy(row.get('risk_pct_plan'))}% = **{fmt_copy(row.get('risk_adr_plan'))}xADR** · "
        f"Risk_OK {fmt_copy(row.get('risk_ok'))}"
    )


def levels_cell(row: dict[str, Any]) -> str:
    feas = fmt_copy(row.get("entry_feasible"))
    stop_t = fmt_copy(row.get("stop_type_plan"))
    return (
        f"{fmt_copy(row.get('close'))} / **{fmt_copy(row.get('entry_ref'))}** / "
        f"**{fmt_copy(row.get('invalidate_below'))}**（{stop_t}）· {feas}"
    )


def verdict_cell(row: dict[str, Any]) -> str:
    parts = [
        fmt_copy(row.get("verdict")),
        fmt_copy(row.get("candidate_class")),
        f"Tradeable **{fmt_copy(row.get('tradeable'))}**",
    ]
    why = _s(row.get("downgrade_reason"))
    if why:
        parts.append("降級：" + why[:80])
    return " · ".join(parts)


def story_cell(ticker: str, flags: dict[str, Any]) -> str:
    stories = {s["ticker"]: s for s in flags.get("story_in_pack") or []}
    s = stories.get(ticker)
    if not s:
        return "本包未見快報"
    stance = s.get("stance") or "—"
    return f"**{stance}**（已在資料包內）· 無需再做 S4"


def demote_why_cell(reasons: list[str]) -> str:
    if not reasons:
        return "—"
    return "；".join(DEMOTE_REASON_ZH.get(r, r) for r in reasons)


def cant_miss_cell(reasons: list[str]) -> str:
    seen: list[str] = []
    for r in reasons:
        text = CANT_MISS_ZH.get(r)
        if text and text not in seen:
            seen.append(text)
    return "；".join(seen) if seen else "須達 can’t-miss 標準，不為填席而放寬門檻"


def plan_cell(row: dict[str, Any]) -> str:
    note = _s(row.get("class_note"))
    return note if note else "—"


def rs_cell(row: dict[str, Any]) -> str:
    bits = [f"RS {fmt_copy(row.get('rs_score'))}（{fmt_copy(row.get('rs_status'))}）"]
    dist = _s(row.get("dist_from_52w_high_pct"))
    if dist:
        bits.append(f"距 52 週高 {dist}%")
    return " · ".join(bits)


def decision_line(flags: dict[str, Any]) -> str:
    stalks = flags.get("stalk_candidate") or []
    demote = flags.get("soft_demote") or []
    remain = flags.get("soft_stalk_suggestion") or []
    n_script = len(stalks)
    n_remain = len(remain)
    names = "、".join(stalks)
    if n_script == 0:
        return "**0 stalks**。腳本無 stalk_candidate。空席出於硬門檻，並非 Bear 否決。"
    if n_remain == 0:
        return (
            f"**0 stalks**。腳本產出 {names} {n_script} 張 STALK 票，經建議降級，不予照單全收。"
            "空席出於 can’t-miss 標準，並非 Bear 否決。"
        )
    demote_names = "、".join(d["ticker"] for d in demote)
    remain_names = "、".join(remain)
    extra = f"建議降級 {demote_names}，" if demote_names else ""
    return (
        f"**{n_remain} stalks**。腳本產出 {names} {n_script} 張 STALK 票，{extra}保留 {remain_names}。"
        "不為填席而放寬門檻。"
    )


def book_header_line(book: list[dict[str, Any]]) -> str:
    bits = []
    for b in book:
        bits.append(f"{b['ticker']}@{b['entry']}" if b.get("entry") else b["ticker"])
    names = " / ".join(bits) if bits else "—"
    return f"OPEN {len(book)}/7 {names} · 未喚醒模擬倉"


def judgment_bullets(flags: dict[str, Any]) -> list[str]:
    bullets: list[str] = []
    conflicts = flags.get("index_conflicts") or {}
    if conflicts.get("has_conflict"):
        a_setup = verdict_mis = story_lie = None
        for c in conflicts.get("conflicts") or []:
            if c.get("kind") == "a_setup_count":
                a_setup = c
            elif c.get("kind") == "verdict_counts":
                verdict_mis = c
            elif c.get("kind") == "story_commissioned":
                story_lie = c
        index_bits: list[str] = []
        if a_setup is not None:
            idx = a_setup.get("index")
            if idx == "A_SETUP rows: none" or (isinstance(idx, str) and "none" in idx.lower()):
                index_bits.append("「A_SETUP rows: none」")
            else:
                index_bits.append(f"A_SETUP {idx}")
        if verdict_mis is not None:
            idxc = verdict_mis.get("index") or {}
            if idxc.get("BUY") and not (verdict_mis.get("actual") or {}).get("BUY"):
                index_bits.append(f"「BUY {idxc.get('BUY')}」")
            else:
                for k, pair in (verdict_mis.get("mismatched") or {}).items():
                    index_bits.append(f"「{k} {pair.get('index')}」")
        if story_lie is not None:
            index_bits.append("並稱「no BUY ticket means no story was commissioned」")
        actual_bits: list[str] = []
        if a_setup is not None:
            names = "、".join(a_setup.get("tickers") or [])
            actual_bits.append(
                f"{a_setup.get('actual')} 張 A_SETUP" + (f"（{names}）" if names else "")
            )
        if verdict_mis is not None:
            actual = verdict_mis.get("actual") or {}
            if actual.get("STALK") and not actual.get("BUY"):
                actual_bits.append("verdicts 為 STALK 而非 BUY")
            else:
                bits_v = "、".join(f"{k} {v}" for k, v in actual.items() if v)
                actual_bits.append(f"verdicts 為 {bits_v}")
        if story_lie is not None:
            stances = []
            for s in flags.get("story_in_pack") or []:
                if s["ticker"] in (story_lie.get("actual") or []):
                    stances.append(
                        f"{s['ticker']} 快報已經落地"
                        + (f"、結論為 {s['stance']}" if s.get("stance") else "")
                    )
            actual_bits.append("、".join(stances) if stances else "快報已經落地")
        lead = "、".join(index_bits) if index_bits else "與 verdicts／資料包不一致"
        actual = "，".join(actual_bits) if actual_bits else "資料包內容不同"
        bullets.append(
            f"**Index 記述與資料包內容互相矛盾。** Index 寫{lead}。實際資料包為 {actual}。"
            "以 **verdicts_US.jsonl** 為準，不以 index 為據。不得把 index 的 BUY 視為可買。"
        )

    cq = flags.get("closest_vs_quality")
    if cq:
        bullets.append(
            f"**最接近者為 {cq['closest_remaining']}，而非 {cq['highest_quality']}。** "
            f"{cq['highest_quality']} 品質最高（Grade {cq.get('highest_grade') or '—'}），"
            f"但因 {'／'.join(cq.get('highest_demoted_reasons') or [])} 建議降級。"
            f"{cq.get('note') or ''}"
        )

    demote = flags.get("soft_demote") or []
    remain = flags.get("soft_stalk_suggestion") or []
    if demote and not remain:
        parts = []
        for d in demote:
            why = "、".join(d.get("reasons") or [])
            qp = d.get("quality_pass_total") or ""
            grade = d.get("grade") or "—"
            room = d.get("room")
            room_s = f"、硬空間 {room}R" if room is not None else ""
            frac = f" {qp}" if qp else ""
            parts.append(f"{d['ticker']}（Grade **{grade}{frac}**{room_s}；{why}）")
        bullets.append(
            "**腳本 STALK 經建議降級，未達 can’t-miss。** "
            + "；".join(parts)
            + "。thin_room 僅在 Grade 為 A／A+、且別無 ≥2R 選擇時方可討論。不可因具 STALK 標籤而照單全收。"
        )
    elif demote:
        parts = [f"{d['ticker']}（{'、'.join(d.get('reasons') or [])}）" for d in demote]
        bullets.append("**部分腳本 STALK 經建議降級：** " + "；".join(parts) + "。")

    stories = flags.get("story_in_pack") or []
    if stories:
        bits = []
        for s in stories:
            stance = s.get("stance")
            bits.append(f"{s['ticker']}" + (f" 結論為 {stance}" if stance else " 快報已在資料包內"))
        bullets.append(
            "**故事已在資料包內，無需再做故事搜索。** "
            + "；".join(bits)
            + "。Story 立場僅作獨立判斷參考，不自動降級。除非 Justin 另行指定，否則不做 S4。"
        )

    for item in flags.get("do_not_upgrade") or []:
        reasons = item.get("reasons") or []
        flip = "tradeable_flipped_pass" in reasons
        thicker = "thicker_room" in reasons or "thicker_room_strong_grade" in reasons
        room = item.get("room")
        extra = ""
        if flip:
            extra = "，且今日 Tradeable 已改為 PASS" if thicker else "今日 Tradeable 已改為 PASS"
        room_bit = f"硬空間 **{room}R**" if room is not None else "空間更厚"
        lead = "空間其實厚於腳本 STALK" if thicker else "表面看似轉好"
        bullets.append(
            f"**{item['ticker']} {lead}**（{room_bit}{extra}），"
            f"惟屬 {item.get('verdict')}（{item.get('candidate_class') or '—'}，Grade {item.get('grade') or '—'}）。"
            "**永不升級 WATCH／AVOID。** 不可因具 STALK 標籤，便假定優於其他 Tradeable PASS。"
        )

    changes = flags.get("prior_changes") or {}
    for w in changes.get("window_closed") or []:
        closest = "昨日最接近者" if w.get("was_closest") else "昨日腳本 STALK"
        rf, rt = w.get("room_from"), w.get("room_to")
        room_bit = ""
        if rf is not None and rt is not None:
            room_bit = f"硬空間由 {rf}R 收窄至 **{rt}R**"
        trad = ""
        if w.get("tradeable_from") and w.get("tradeable_to"):
            trad = f"，Tradeable {w['tradeable_from']}→{w['tradeable_to']}"
        bullets.append(
            f"**{closest} {w['ticker']}，今日並非漏看，而是窗口已關閉。** "
            f"{room_bit}{trad}。{w.get('why') or ''}。"
            "Room < 1 永不列入 stalk。不得自動把昨日降級票升回今日 stalk。"
        )

    books = flags.get("book_remarks") or []
    if books:
        parts = []
        for b in books:
            if b.get("in_universe"):
                parts.append(
                    f"{b['ticker']} 在宇宙內（{_s(b.get('verdict')) or '—'}，"
                    f"Entry {_s(b.get('entry_feasible')) or '—'}，"
                    f"room {b.get('room') if b.get('room') is not None else '—'}R）"
                )
            else:
                parts.append(f"{b['ticker']} 不在本包 {b.get('universe_size')} 名宇宙")
        bullets.append("**書倉 " + "、".join(parts) + "。僅作備註，未喚醒模擬倉。**")

    covered = {x["ticker"] for x in (flags.get("do_not_upgrade") or [])} | {
        w["ticker"] for w in (changes.get("window_closed") or [])
    }
    flip_by: dict[str, list[dict[str, Any]]] = {}
    for fl in changes.get("flips") or []:
        flip_by.setdefault(fl["ticker"], []).append(fl)
    for ticker, flips in flip_by.items():
        if ticker in covered:
            continue
        interesting = [
            f for f in flips if f["field"] in {"Tradeable", "Risk_OK", "Entry_Feasible", "verdict"}
        ]
        if not interesting:
            continue
        desc = "、".join(f"{f['field']} {f['from']}→{f['to']}" for f in interesting)
        bullets.append(
            f"**{ticker} 今日否決或狀態理由已改變。** {desc}。不可僅因單一欄位改善即視為轉好，亦不升級。"
        )

    if len(bullets) > 6:
        bullets = bullets[:6]
    return bullets


def observe_table(
    demoted_rows: list[tuple[dict[str, Any], list[str]]], flags: dict[str, Any]
) -> str:
    if not demoted_rows:
        return "無腳本 STALK 經建議降級。"
    headers = [
        "**" + r["ticker"] + "** " + ("／".join(reasons) if reasons else "")
        for r, reasons in demoted_rows
    ]

    def cells(fn) -> str:
        return " | ".join(fn(r, reasons) for r, reasons in demoted_rows)

    return "\n".join(
        [
            "| | " + " | ".join(headers) + " |",
            "|" + "|".join(["---"] * (len(demoted_rows) + 1)) + "|",
            "| Verdict（以 verdicts 為準） | " + cells(lambda r, rs: verdict_cell(r)) + " |",
            "| Grade / Priority | " + cells(lambda r, rs: grade_cell(r)) + " |",
            "| 收盤 / 限價 / 止損 | " + cells(lambda r, rs: levels_cell(r)) + " |",
            "| 距收盤 | " + cells(lambda r, rs: away_cell(r)) + " |",
            "| 風險 | " + cells(lambda r, rs: risk_cell(r)) + " |",
            "| 硬空間 | " + cells(lambda r, rs: room_cell(r, soft=False)) + " |",
            "| 軟空間 | " + cells(lambda r, rs: room_cell(r, soft=True)) + " |",
            "| Leader / 趨勢 | " + cells(lambda r, rs: leader_cell(r)) + " |",
            "| 財報 | " + cells(lambda r, rs: earnings_cell(r)) + " |",
            "| 計畫 | " + cells(lambda r, rs: plan_cell(r)) + " |",
            "| 故事 | " + cells(lambda r, rs: story_cell(r["ticker"], flags)) + " |",
            "| 主題／RS | " + cells(lambda r, rs: rs_cell(r)) + " |",
            "| 不列入 stalk 之原因 | " + cells(lambda r, rs: demote_why_cell(rs)) + " |",
            "| 須達 can’t-miss 之條件 | " + cells(lambda r, rs: cant_miss_cell(rs)) + " |",
        ]
    )


def other_remarks_table(
    flags: dict[str, Any],
    ranked_rows: list[dict[str, Any]],
    book: list[dict[str, Any]],
) -> str:
    by = {r["ticker"]: r for r in ranked_rows}
    rows_out: list[tuple[str, str, str]] = []
    seen: set[str] = set()

    def add(ticker: str, status: str, note: str) -> None:
        if ticker in seen:
            return
        seen.add(ticker)
        rows_out.append((ticker, status, note))

    for item in flags.get("do_not_upgrade") or []:
        r = by.get(item["ticker"])
        status_bits = [
            f"{item.get('verdict')}（{item.get('candidate_class') or '—'}）",
            f"Grade {item.get('grade') or '—'}",
            f"Tradeable **{item.get('tradeable') or '—'}**",
        ]
        if item.get("room") is not None:
            status_bits.append(f"room **{item['room']}R**")
        note = "空間厚於腳本 STALK 或 Tradeable 已轉 PASS，**永不升級 WATCH／AVOID。**"
        if r and _s(r.get("tradeable_why")) and _s(r.get("tradeable")).upper() != "PASS":
            note += f" Tradeable_Why：{_s(r.get('tradeable_why'))}"
        if r and _s(r.get("class_note")):
            note += " " + _s(r.get("class_note"))
        add(item["ticker"], " · ".join(status_bits), note)

    for w in (flags.get("prior_changes") or {}).get("window_closed") or []:
        r = by.get(w["ticker"])
        status = "不在本包宇宙"
        if r:
            status = (
                f"{r.get('verdict')} · Grade {r.get('grade')} · "
                f"room **{r.get('room')}R** · Tradeable **{r.get('tradeable')}**"
            )
            if _s(r.get("tradeable_why")):
                status += f" `{_s(r.get('tradeable_why'))}`"
        add(w["ticker"], status, f"窗口已關閉。{w.get('why') or ''}。不升級，亦不把昨日票自動召回。")

    for b in flags.get("book_remarks") or []:
        book_note = "書倉 OPEN" + (f" @{b['book_entry']}" if b.get("book_entry") else "") + "。僅作備註，**未喚醒**模擬倉。"
        if b.get("in_universe"):
            r = by.get(b["ticker"])
            status = (
                f"{b.get('verdict')} · Entry {b.get('entry_feasible')} · "
                f"room {b.get('room') if b.get('room') is not None else '—'}R · "
                f"Tradeable {b.get('tradeable') or '—'}"
            )
            if r and _s(r.get("close")):
                status = f"收盤 {_s(r.get('close'))} · " + status
            add(b["ticker"], status, book_note)
        else:
            add(b["ticker"], f"不在本包 {b.get('universe_size')} 名宇宙", book_note)

    for ticker in (flags.get("prior_changes") or {}).get("dropped_from_universe") or []:
        add(ticker, "不在本包宇宙", "昨日觀察或降級名單已跌出；不自動召回。")

    for item in flags.get("leftovers") or []:
        why = "；".join(item.get("why") or [])
        tw = f" `{item['tradeable_why']}`" if item.get("tradeable_why") else ""
        add(
            item["ticker"],
            f"{item.get('verdict')}（{item.get('candidate_class') or '—'}）· Grade {item.get('grade')} · "
            f"Tradeable {item.get('tradeable')} · room {item.get('room') if item.get('room') is not None else '—'}R{tw}",
            f"{why}。不重開、不升級。",
        )

    if not rows_out:
        return "無。"
    lines = ["| 代號 | 本包狀態 | 備註 |", "|---|---|---|"]
    for ticker, status, note in rows_out:
        lines.append(f"| **{ticker}** | {status} | {note} |")
    return "\n".join(lines)


def soft_stalks_section(remain_rows: list[dict[str, Any]], flags: dict[str, Any]) -> str:
    n_script = len(flags.get("stalk_candidate") or [])
    n_demote = len(flags.get("soft_demote") or [])
    if not remain_rows:
        suffix = "，經建議降級" if n_demote or n_script else ""
        return f"**無。** 腳本產出 {n_script} 個 stalk_candidate{suffix}。不為填席而放寬門檻。"
    h = _h()
    blocks = ["```\n" + h.handoff_block(row, row.get("tags") or []) + "\n```" for row in remain_rows]
    note = ""
    if n_demote:
        note = f"\n\n另有 {n_demote} 個腳本 stalk_candidate 經建議降級，見觀察表。不為填席而放寬門檻。"
    return "\n\n".join(blocks) + note


def remaining_gaps(flags: dict[str, Any]) -> str:
    gaps: list[str] = []
    for d in flags.get("soft_demote") or []:
        for r in d.get("reasons") or []:
            g = DEMOTE_GAP_ZH.get(r)
            if g and g not in gaps:
                gaps.append(g)
    for s in flags.get("story_in_pack") or []:
        if _s(s.get("stance")).upper() == "CHALLENGE" and "故事信念" not in gaps:
            gaps.append("故事信念")
    if not gaps and flags.get("story_in_pack"):
        gaps = ["龍頭", "空間", "時機"]
    if not gaps:
        return ""
    return "剩餘缺口為" + "／".join(gaps) + "。"


def pinned_section(
    *,
    pack_dir: Path,
    out_dir: Path,
    contract_date: str,
    flags: dict[str, Any],
    context: dict[str, Any],
    drive_url: str,
    optional_missing: list[str],
) -> str:
    pack = pack_dir.resolve()
    lines = ["| 來源 | 路徑 / id |", "|---|---|"]
    label = folder_label(contract_date)
    if drive_url:
        lines.append(f"| Drive folder | {drive_url} （「{label}」） |")
    else:
        lines.append("| Drive folder | （未提供 --drive-folder） |")

    def add(label_: str, path: Path, extra: str = "") -> None:
        if path.exists():
            md = file_md5(path)
            md_bit = f" · md5 `{md}`" if md else ""
            extra_bit = f" · {extra}" if extra else ""
            lines.append(f"| {label_} | `{path}`{md_bit}{extra_bit} |")
        else:
            lines.append(f"| {label_} | `{path}` · 缺失 |")

    add("Soft Final draft", out_dir / "attention-3-picks.draft.md")
    add("verdicts_US.jsonl", pack / "verdicts_US.jsonl", "權威")
    add("L2_Input.csv", pack / "L2_Input.csv", f"Date={contract_date or '—'}")
    add("Contract_US.csv", pack / "Contract_US.csv", "price truth")
    add("index.md", pack / "index.md", "結論參考；與 verdicts 衝突處以 verdicts 為準")
    trig = pack / "Trigger_US.csv"
    if trig.exists():
        add("Trigger_US.csv", trig, "已在資料包內")
    else:
        lines.append("| Trigger_US.csv | 可選檔案缺失 |")

    stories = flags.get("story_in_pack") or []
    if stories:
        bits = []
        for s in stories:
            stance = f"（{s['stance']}）" if s.get("stance") else ""
            bits.append(" / ".join(s.get("sources") or []) + stance)
        lines.append("| 故事 | " + "；".join(bits) + " 已在資料包內；無需再做 S4 |")
    else:
        lines.append("| 故事 | 本包未見快報／story.json |")

    if context.get("regime"):
        lines.append(f"| Regime | `{context['regime']}`（僅作獨立判斷，正文不覆述） |")
    else:
        lines.append("| Regime | 未發現本地路徑（不發明） |")
    if context.get("brief"):
        lines.append(f"| US Brief | `{context['brief']}`（路徑 only；正文不覆述） |")
    else:
        lines.append("| US Brief | 未發現本地路徑（不發明） |")
    if context.get("market_master"):
        mm = "；".join(f"`{p}`" for p in context["market_master"])
        lines.append(f"| Market Master | {mm}（路徑 only；正文不覆述） |")
    else:
        lines.append("| Market Master | 未發現本地路徑（不發明） |")
    if context.get("stockbee"):
        sb = "；".join(f"`{p}`" for p in context["stockbee"])
        lines.append(f"| Stockbee | {sb}（路徑 only；正文不覆述） |")
    else:
        lines.append("| Stockbee | 未發現本地路徑（不發明） |")

    for note in context.get("notes") or []:
        lines.append(f"| 缺口 | {note} |")
    if optional_missing:
        lines.append("| 可選檔案缺失 | " + ", ".join(optional_missing) + " |")

    prior = flags.get("prior_changes") or {}
    if prior.get("prior_dir"):
        prior_final = Path(prior["prior_dir"]) / "attention-3-picks.md"
        extra = ""
        if prior_final.exists():
            extra = f" md5 `{file_md5(prior_final)}`"
        dest = prior_final if prior_final.exists() else Path(prior["prior_dir"])
        lines.append(f"| 昨日 Soft（未改動） | `{dest}`{extra} |")
    lines.append(f"| 腳本交接（降級前備份） | `{out_dir / 'handoff_blocks.script.md'}` |")
    lines.append(f"| judgment_flags | `{out_dir / 'judgment_flags.json'}` |")
    return "\n".join(lines)


def strip_pinned(md: str) -> str:
    parts = re.split(r"\n---\s*\n+## PINNED_INPUTS\b", md, maxsplit=1)
    if len(parts) == 1:
        parts = re.split(r"\n## PINNED_INPUTS\b", md, maxsplit=1)
    return parts[0].rstrip() + "\n"


def build_draft_markdown(
    *,
    pack_dir: Path,
    out_dir: Path,
    contract_date: str,
    run_date: str,
    tc: str,
    flags: dict[str, Any],
    ranked_rows: list[dict[str, Any]],
    script_stalks: list[dict[str, Any]],
    book: list[dict[str, Any]],
    context: dict[str, Any],
    drive_url: str,
    optional_missing: list[str],
) -> str:
    remain_names = set(flags.get("soft_stalk_suggestion") or [])
    remain_rows = [r for r in script_stalks if r["ticker"] in remain_names]
    reason_map = {d["ticker"]: d.get("reasons") or [] for d in flags.get("soft_demote") or []}
    demoted = [(r, reason_map[r["ticker"]]) for r in script_stalks if r["ticker"] in reason_map]

    n_remain = len(remain_rows)
    header = (
        f"# Soft Final — **{tc}**\n"
        f"**{n_remain} stalks** · Contract **{contract_date or '—'}** · run **{run_date} HKT** · "
        "Soft Final = Final · 非投資建議（attention / stalk only）\n"
    )
    drive_cell = "本地資料包 · 以 verdicts 為準"
    if drive_url:
        drive_cell = f"[{folder_label(contract_date)}]({drive_url}) · 以 verdicts 為準"

    meta = (
        "| | |\n|---|---|\n"
        f"| 決定 | {decision_line(flags)} |\n"
        f"| 書倉 | {book_header_line(book)} |\n"
        f"| Drive | {drive_cell} |\n"
        "| Overview | skip（除非另行指定） |\n"
    )

    bullets = judgment_bullets(flags)
    if bullets:
        judgment = "\n".join(f"{i}. {b}" for i, b in enumerate(bullets, 1))
    else:
        judgment = "（腳本未偵測到額外的漏看旗標；LLM 可覆核後補上獨立判斷。）"

    gap = remaining_gaps(flags)
    story_note = ""
    if flags.get("story_in_pack"):
        story_note = "快報已在資料包內，無需再做故事搜索。"
        if gap:
            story_note += gap
    elif gap:
        story_note = gap

    observe_heading = "觀察"
    if demoted:
        observe_heading = f"觀察 — {len(demoted)} 檔腳本 STALK（建議降級，不予照單全收）"

    md = "\n".join(
        [
            header,
            meta,
            "假設已閱讀當日 regime、US Brief、Market Master、RS 總覽 — 此處不再覆述。",
            "",
            "## 獨立判斷（可能漏看之處）",
            "",
            judgment,
            "",
            story_note,
            "",
            "## Soft stalks",
            "",
            soft_stalks_section(remain_rows, flags),
            "",
            f"## {observe_heading}",
            "",
            observe_table(demoted, flags),
            "",
            "## 其他備註（非 stalk；不升級）",
            "",
            other_remarks_table(flags, ranked_rows, book),
            "",
            "---",
            "",
            "## PINNED_INPUTS",
            "",
            pinned_section(
                pack_dir=pack_dir,
                out_dir=out_dir,
                contract_date=contract_date,
                flags=flags,
                context=context,
                drive_url=drive_url,
                optional_missing=optional_missing,
            ),
            "",
            "非投資建議。僅作 Stalk / observe 框架。",
            "",
        ]
    )
    return re.sub(r"\n{3,}", "\n\n", md)


def write_soft_final_artifacts(
    *,
    pack_dir: Path,
    out_dir: Path,
    contract_date: str,
    run_date: str,
    tc: str,
    ranked_rows: list[dict[str, Any]],
    script_stalks: list[dict[str, Any]],
    verdicts: dict[str, dict],
    book_raw: str,
    prior_dir: Path | None,
    prior_pack_dir: Path | None,
    drive_folder: str | None,
    optional_missing: list[str],
    handoff_text: str,
) -> dict[str, Any]:
    for row in ranked_rows:
        enrich_row(row)
    book = parse_book(book_raw)
    drive_url, drive_id = drive_link(drive_folder)
    context = discover_context(contract_date)
    prior = load_prior_state(prior_dir, prior_pack_dir)
    flags = build_judgment_flags(
        pack_dir=pack_dir,
        out_dir=out_dir,
        contract_date=contract_date,
        run_date=run_date,
        tc=tc,
        ranked_rows=ranked_rows,
        script_stalks=script_stalks,
        verdicts=verdicts,
        book=book,
        prior=prior,
        drive_url=drive_url,
        drive_id=drive_id,
        context=context,
    )
    draft = build_draft_markdown(
        pack_dir=pack_dir,
        out_dir=out_dir,
        contract_date=contract_date,
        run_date=run_date,
        tc=tc,
        flags=flags,
        ranked_rows=ranked_rows,
        script_stalks=script_stalks,
        book=book,
        context=context,
        drive_url=drive_url,
        optional_missing=optional_missing,
    )
    flags_path = out_dir / "judgment_flags.json"
    flags_path.write_text(json.dumps(flags, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    draft_path = out_dir / "attention-3-picks.draft.md"
    draft_path.write_text(draft, encoding="utf-8")
    notion_path = out_dir / "attention-3-picks-notion.md"
    notion_path.write_text(strip_pinned(draft), encoding="utf-8")
    script_handoff = out_dir / "handoff_blocks.script.md"
    script_handoff.write_text(handoff_text, encoding="utf-8")
    stub_path = out_dir / "soft_final_stub.md"
    stub_path.write_text(
        "Deprecated. Soft Final draft is `attention-3-picks.draft.md` (書面語 template). "
        "Do not fill old PLACEHOLDERs; start from the draft + judgment_flags.json.\n",
        encoding="utf-8",
    )
    h = _h()
    banned = h.banned_scan(draft) + h.banned_scan(strip_pinned(draft))
    return {
        "draft_path": str(draft_path),
        "notion_path": str(notion_path),
        "flags_path": str(flags_path),
        "script_handoff_path": str(script_handoff),
        "stub_path": str(stub_path),
        "soft_demoted": [d["ticker"] for d in flags.get("soft_demote") or []],
        "soft_stalk_suggestion": flags.get("soft_stalk_suggestion") or [],
        "flag_counts": {
            "index_conflicts": len((flags.get("index_conflicts") or {}).get("conflicts") or []),
            "story_in_pack": len(flags.get("story_in_pack") or []),
            "do_not_upgrade": len(flags.get("do_not_upgrade") or []),
            "prior_window_closed": len((flags.get("prior_changes") or {}).get("window_closed") or []),
            "book_remarks": len(flags.get("book_remarks") or []),
            "suggest_demote": len(flags.get("suggest_demote") or []),
        },
        "banned_token_hits_draft": banned,
        "tc": tc,
        "run_date": run_date,
    }
