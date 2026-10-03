---
name: US daily market + potential setups
description: >-
  Use this when Justin walks the US cash-session morning stack — Market
  Awareness, US Market Brief, Potential Setups (Drive/Pine), or the explicit
  Setup→Story→Fusion MD+prompt chain (no auto infographic image).
---
# US daily market + potential setups

Coordinate Justin’s US cash-session stack. **總指揮 orchestrates; specialists execute.** Do not invent prices, scores, or VERDICTs.

## DATA GATE (highest priority)

**Data quality beats finishing any report.** If a critical input is missing, stale, or abnormal:

1. **STOP** that phase (and do not start the next phase)
2. Do **not** invent, interpolate, or paper over
3. Notify **總指揮 → Justin** with: what failed · source · expected session date vs what you got · what Justin should re-export or fix

Tripwires (non-exhaustive):

- **yfinance** cannot grab latest bars/quotes (scanner / setup)
- **StockCharts** breadth or VIX chart not updated for the session
- **Stockbee** T2108 / Market Monitor sheet not updated
- Empty or truncated TradingView ETF / abnormal-volume CSVs
- OCR/vision numbers that fail cross-check vs chart or FRED

總指揮 treats a DATA GATE fail as an immediate Justin ping — never silently continue the stack.

## Inputs (stage first)

| File | Used by | Stage path |
|------|---------|------------|
| TradingView `US-ETF_YYYY-MM-DD.csv` | Market Awareness **and** US Market Brief | `/workspace/market-inputs/YYYY-MM-DD/` **and** `/workspace/us-brief-inputs/YYYY-MM-DD/` |
| Abnormal volume **rise** + **drop** CSVs | US Market Brief **only** | `/workspace/us-brief-inputs/YYYY-MM-DD/tv-abnormal-rise.csv` + `tv-abnormal-drop.csv` |

Session date = US cash session date on the exports (often prior US day when Justin runs morning HKT).

## Phase A — Market Awareness (first)

**Owner:** Market Awareness Orchestrator  
**Order (hard):**

1. **T2108** — Stockbee Market Monitor → Excel — gate if sheet stale
2. **StockCharts breadth** — capture + OCR/vision (+ FRED VIX) — gate if charts not updated
3. **Regime analysis** — Stockbee + breadth + **US-ETF** → Regime v6.3 繁體中文 daily

**Stop:** Do **not** run US Market Brief inside this phase.  
**High-stakes:** self-VERIFY → Work Verifier → 總指揮 → Justin-final.

## Phase B — US Market Brief (after Awareness)

**Owner:** US Market Daily Brief  
VIX from Phase A StockCharts → abnormal rise/drop CSVs → US-ETF. No Regime TOTAL card. Work Verifier before Justin-final.

## Phase C — Potential Setups (scanner only)

**Owner:** US Swing Scanner  

| Source | How |
|--------|-----|
| **A. Drive Pullback buy Excel** | Latest US-dated symbols; no ticker ask |
| **B. TradingView Pine screener** | List Justin provides |

Clear `swing_data_us` before each run → scoreboard + CSVs → **STOP**. Consolidate Drive+Pine if both ran. **No** auto Setup.

### ANTI-JOBS (Phase C)

- “Pullback buy” ≠ filter Pine BUY rows
- No auto-handoff to 美股 Swing Setup
- No Verifier on unauthorized Setup

## Phase D — Explicit pick chain (Setup → Story → Fusion)

Only when Justin names ticker(s):

1. **美股 Swing Setup** → HANDOFF + Trade Entry  
2. **投資敘事分析師** → Story report (never upgrade VERDICT)  
3. **Fusion Formatter** → `FUSION_REPORT_*.md` + `FUSION_INFOGRAPHIC_PROMPT_*.md`  
4. **Work Verifier** on the chain  
5. 總指揮 delivers **both MDs** to Justin  

### Fusion stop rule (token save)

**Default STOP after Fusion report + infographic prompt.** Do **not** run baoyu / Fusion Swing Infographic inside Grok Bot unless Justin explicitly asks to generate the image here. He often generates the graphic elsewhere from the prompt.

## VERIFY

- High-stakes A/B/D: Work Verifier → `/workspace/work-verifier/output/`
- Phase C: skip unless asked
- DATA GATE → Justin immediately

## Task id pattern (總指揮)

Awareness → Brief → Drive scan (stop) → Pine scan (stop) → **only after pick:** Setup → Story → Fusion (report+prompt) → Verifier → deliver MDs
