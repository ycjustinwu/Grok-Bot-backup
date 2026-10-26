# US Market Daily Brief

Daily US cash-session market-focus brief (美股市場每日簡報): thematic ETFs, abnormal volume, focus catalysts, rotation — 繁體中文; silent analysis steps; DATA GATE overrides completion.

## Sub-features

- `us-brief-schema` — Starts at `## 美股市場每日簡報`; header with session date + 香港時間翌日早上7:00; Parts for themes / movers / catalysts / rotation.
- `us-brief-inputs` — `US-ETF_[DATE].csv`, abnormal-volume CSVs, VIX/breadth path present or explicitly stopped by DATA GATE.
- `us-brief-data-gate` — Missing/stale critical inputs → STOP + notify path; no `[待補充]` placeholders; no invent.
- `us-brief-boundary` — No competing Regime TOTAL/21.5 scorecard (hand off to Market Awareness Orchestrator).
- `us-brief-catalysts` — Three focus names with sourced facts; no search-process dump.

## How to get to it (user POV)

- Justin attaches US-ETF / abnormal-volume CSVs or asks for 美股每日簡報.
- 總指揮 routes completed brief path to Work Verifier before Justin treats as final.
- Typical outputs under `/workspace/` producer run folders or attached brief MD (follow intake paths).

## Driving it with work-verify harness

Preconditions:

- Doctor GO on claimed brief path + cited CSVs / VIX notes.
- Feature id `us-market-daily-brief`.

- **Locate deliverable.** Open claimed MD/chat export path on disk.
- **Schema.** Title, date header, opening (VIX path + 震央), thematic / volume / catalyst / rotation sections as claimed; Trump/HK sections only if material.
- **Input trace.** Spot-check ETF Δ% and abnormal-volume keepers against CSV/MCP rows; RelVol/mcap gates match producer OpenClaw rules (|Δ|≥5%, RelVol>2, **mcap>$5B**, drop OTC). Do **not** re-apply the old mcap>$10B soft FAIL (locked 2026-10-14 in `us-abnormal-volume` / `tv-abnormal-volume-mcp`). TV MCP AV is authoritative when Justin did not paste.
- **DATA GATE.** If brief finished despite missing critical bars/charts/CSV, → FAIL. If producer stopped and notified, verify notice quality (what failed, source, session vs got).
- **No fabricate.** Prices, RelVol, VIX, catalysts traceable; English-only main body → FAIL schema.
- **ANTI_JOBS.** No screening-table dump as user deliverable; no Orchestrator TOTAL replacement; no invented placeholders.
- **Proof.** Evidence report; PASS / PASS_WITH_NOTES / FAIL per soft vs hard gaps.

## Gotchas

- Shared VIX/breadth with Orchestrator is OK; a second TOTAL/21.5 inside this brief is ANTI_JOBS FAIL.
- Soft omit of Trump/HK is correct when non-material — do not NOTES-force those sections.
- Keeper mcap gate is **>$5B** (OpenClaw 2026-10-14). Requiring soft FAIL for $5–10B names is a **verifier error**.
- DATA GATE failure papered over with invented numbers is FAIL, not NOTES.
