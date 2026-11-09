---
name: story-package-s4
description: >
  Use when 投資敘事分析師 is routed a Swing Package PINNED run (Ops scan DONE or
  Justin opt-in package S4): read story_handoffs.md + L2_Input Story_Needed rows,
  write stories/<T>_story.json + _search_log.json per docs/05. Not for Hermes-healthy
  daily US auto-route. Not GEMINI/Fusion chat reports.
---

# story-package-s4

ONE JOB: Fill package S4 for `Story_Needed=True` names only — narrative JSON + search log that `story_search_sync.py` can merge. Never invent prices or upgrade Tradeable FAIL / WATCH / AVOID.

## Locked OQs (TC-20261109-story-PKG)
1. Universe = **Story_Needed only**
2. Hermes-healthy daily US stays OFF unless **Justin / 總指揮 opt-in** package S4 TC
3. After JSON land → **Package Ops** owns sync + check + render + Drive (not this skill)
4. HK package = **JSON-only** (no GEMINI / Fusion for package runs)

## Wake
- TC from 總指揮 / Justin with `PINNED_INPUTS` pointing at a package run folder
- Ops announced scan DONE + Story_Needed ≥1 + stories missing
- Idle if no Story_Needed, or Hermes healthy daily with no opt-in

## PINNED reads (exact paths from handoff)
| File | Use |
|---|---|
| `story_handoffs.md` | Primary STORY HANDOFF v5 blocks |
| `L2_Input.csv` | Filter `Story_Needed=True`; Tradeable / Why / baseline |
| `Contract_US.csv` or HK Contract | Price/verdict ground truth only |
| `index.md` | optional as_of / session |

Do **not** invent universe from Trigger alone. Skip tickers not in Story_Needed.

## Pipeline
1. [story-handoff-parse](sand-workflow:story-handoff-parse) — MARKET=US → STORY HANDOFF v5; HK package → same JSON path (not GEMINI)
2. [story-theme-match](sand-workflow:story-theme-match) — theme route only; no prices
3. [story-web-search](sand-workflow:story-web-search) — search **before** write; log queries/URLs
4. [story-narrative-validate](sand-workflow:story-narrative-validate) — no invent; no verdict upgrade
5. **This skill emit** — write JSON files (not Fusion MD report)

## Output schema (`docs/05_HANDOFF_S4_S5.md`)
Write under `<run>/stories/`:
- `<TICKER>_story.json` — fields: ticker, market_line, story_main, story_main_score, why_now, moat, numbers, story_sub, story_sub_score, risks (≤4), conviction (CONFIRM|CHALLENGE|NEUTRAL), conviction_why, story_tag, hard_event, earnings_check, sources (≥2), traps
- `<TICKER>_search_log.json` — `{ticker, queries, urls, retrieved}`

Hard rules (reject file if broken):
1. No invented targets / T1–T3 / RR / RSI / MA / ADR / volume-ratio / stop prices
2. Sell-side figures need source + date
3. Never change baseline verdict, entry, stop, risk from handoff
4. US English · HK Traditional Chinese · no simplified
5. CONFIRM needs two distinct source domains
6. If story conflicts system call → conviction=CHALLENGE + why
7. Tradeable=FAIL → never CONFIRM a hang; copy `Tradeable_Why` into traps/risks

## After write
Announce to 總指揮 one line: tickers written, run path, stories dir.  
`NEXT_GATE: Package Ops` → sync / check / render / Drive.  
Do **not** run `story_search_sync.py` / `run_l2.sh` / Drive upload from this skill (Ops owns).  
Do **not** wake Second brain / 模擬倉 / Fusion.

## VERIFY
- [ ] Only Story_Needed tickers processed
- [ ] Each story + search_log exist under `stories/`
- [ ] No invented prices/targets; conviction ∈ allowed set
- [ ] Tradeable FAIL not upgraded
- [ ] PINNED_INPUTS / DECISIONS_MADE / OPEN_QUESTIONS / NEXT_GATE filled
- [ ] No sync/render/Drive; no SB/sim/Fusion wake
- [ ] Hermes-healthy daily US not run without Justin opt-in

## HANDOFF
```
PINNED_INPUTS: <run>/story_handoffs.md · L2_Input.csv · Contract · stories/
DECISIONS_MADE: Story_Needed-only; Ops owns sync; HK JSON-only; Hermes daily OFF unless opt-in
OPEN_QUESTIONS: none | missing handoff block | search thin
NEXT_GATE: Package Ops sync+check+render+Drive → 總指揮 → SB/sim if verdicts ready
```

## ANTI-JOBS
- Hermes healthy daily US auto-route without opt-in
- GEMINI / Fusion chat path on package runs
- Scanner / Setup / install / sim open
- Invent tickers, prices, catalysts, volumes
