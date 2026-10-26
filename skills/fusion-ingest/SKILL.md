---
name: Fusion Ingest
description: >-
  Use this when fusing 港股 Swing Setup technical output with a Story Search 敘事報告
  — parse both inputs, prefer GEMINI HANDOFF fields, enforce tech-over-story and
  Adjusted_Stop rules, no new facts.
---
# Fusion Ingest

Bridge step 1: ingest **港股 Swing Setup** (or Claude) technical output + **Story Search** 敘事報告. Faithful only — no new facts, no web search.

## Inputs

- `<technical_report>` — full Swing/Claude report (must include Phase 7 verdict and/or Phase 8 `GEMINI HANDOFF`)
- `<story_report>` — Story Search 敘事報告 (may be missing)

If technical is missing → stop and ask. If story missing → core story =「技術驅動，敘事待查」.

## Prefer handoff fields when present

From the labeled `GEMINI HANDOFF` block (contract with Swing/Story):

VERDICT · SETUP TYPE · STOP TYPE · STOP ANCHOR · SCENARIO ENTRY · ENTRY ZONE · ADJUSTED STOP · PRIMARY TARGET + paired RR · EARNINGS · KEY SUPPORT · TECHNICAL CONCERN · CLAUDE CONVICTION · RS_SCORE

Handoff control fields (from Swing HANDOFF and Story handoff tail): **PINNED_INPUTS** · **DECISIONS_MADE** · **OPEN_QUESTIONS** · **NEXT_GATE**
- Missing → treat as `none` and add `"<FIELD> missing in <Swing|Story> handoff — treated as none"` to OPEN_QUESTIONS.
- If Fusion reads any data file, read only the PINNED_INPUTS paths, never "latest"; an unpinned file used → note its path under OPEN_QUESTIONS.
- If Swing and Story PINNED_INPUTS point at different versions of the same file (e.g. Summary_US of different dates) → flag the conflict under OPEN_QUESTIONS; do not silently pick one.
- DECISIONS_MADE are settled; carry them, do not re-open them.

Also pull from the full tech body when needed: Priority Score, Playbook/TZ flags, Vol_Expansion, Extension_MA20, RSI, Minervini, Ladder T1/T2/T3, red flags, scenario A/B triggers.

From story: 主線/次線, Why Now, 一句講晒, 情緒標籤, CONVICTION ASSESSMENT, narrative strength.

## Hard rules to pass downstream

1. **Stop price** = `ADJUSTED STOP` from handoff (or validated Scenario_Stop) — never raw Suggested_Stop / SwingLow alone
2. **Tech VERDICT wins** over bullish story (never upgrade to BUY for story alone)
3. **EARNINGS PASS** → flag binary risk ≤7d; **CAUTION** → compressed hold window
4. **STALK** → coiled; wait volume break at Tight_Zone_High; do not chase
5. Weight assertiveness by CLAUDE CONVICTION (and Story CONFIRM/CHALLENGE as color only)

Hand a structured extract object to **Fusion Report** and **Fusion Infographic Prompt**. Include the merged PINNED_INPUTS / DECISIONS_MADE / OPEN_QUESTIONS / NEXT_GATE (e.g. "Work Verifier → PASS/PASS_WITH_NOTES before Final") in the extract and in Fusion's handoff to Work Verifier (not inside the ≤500-字 report body).
