---
name: Story Handoff Parse
description: >-
  Use this when receiving a GEMINI HANDOFF from 港美股/港股 Swing Setup — extract
  labeled contract fields including MARKET HK|US, apply earnings gates, lock
  terms before story research.
---
# Story Handoff Parse

Parse a **GEMINI HANDOFF** from **港美股 Swing Setup** / **港股 Swing Setup** (or Claude Phase 8). Do not redo technical analysis. Do not upgrade VERDICT for a good story.

## Required labeled fields

Header `GEMINI HANDOFF — TICKER | DATE` plus:

VERDICT · SETUP TYPE · STOP TYPE · STOP ANCHOR · SCENARIO ENTRY · ENTRY ZONE · ADJUSTED STOP · PRIMARY TARGET+RR · EARNINGS · KEY SUPPORT · TECHNICAL CONCERN · CLAUDE CONVICTION · RS_SCORE (optional) · **MARKET** (HK|US if present)

If MARKET missing: infer from ticker (`.HK` → HK; else US).

If ENTRY ZONE, ADJUSTED STOP, VERDICT, or EARNINGS missing → ask for complete handoff.

## Handoff control fields

Also parse: **PINNED_INPUTS** · **DECISIONS_MADE** · **OPEN_QUESTIONS** · **NEXT_GATE**

- Missing any of these → treat as `none` (do not block) and add `"<FIELD> missing in upstream HANDOFF — treated as none"` to your OPEN_QUESTIONS.
- **PINNED_INPUTS** → read exactly those absolute paths for any data file (Summary_US/Summary_HK, scanner CSV, regime file); never substitute "latest". Need a file that is not pinned → note the path you used under OPEN_QUESTIONS.
- **DECISIONS_MADE** → settled; do not re-open or argue them in the story.
- Carry all four fields forward into the Story output's handoff tail for Fusion.

## Earnings gate

≤14d / CAUTION → pre-earnings catalysts only · PASS≤7d → same-week only · UNKNOWN → search normally + remind user to verify calendar

## Term lock

RS = Stock%−benchmark (SPY or HSI), positive = outperform · Entry ≠ Stop · Tech VERDICT owns the call
