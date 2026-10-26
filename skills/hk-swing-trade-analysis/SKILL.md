---
name: Swing Trade Analysis
description: >-
  Use this for full HK or US swing-trade CSV analysis (v4.7.1) — validate, score
  setups, scenario-anchor stops, Python-aligned verdict gates, Trade Entry CSV,
  and labeled GEMINI HANDOFF for 投資敘事分析師.
---
# Swing Trade Analysis

Full pipeline for **港股或美股** swing CSV (**v4.7.1-HK logic**; shared skills). Output **繁體中文**. Feeds **投資敘事分析師** via labeled GEMINI HANDOFF.

## Orchestration

1. **Swing CSV Validate** — Core/Optional tiers, market detect, health
2. **Swing Setup Playbook** — TZ v2.1, A–H, three RR systems, Priority, red flags
3. **Swing Scenario Stop** — scenario stops; pullback = PB_STRUCT (or TZ under Step 2b exception); Ladder ascending
4. Phase 7 verdict + Phase 8 handoff
5. Trade Entry CSV row(s) for Sheets
6. Q&A / education as asked

## Output template (run folder)

Write under `/workspace/{us|hk}-swing-setup/output/run-*/`:

| File | Purpose |
|------|---------|
| `{T}_validate.md` | CSV validate + health |
| `{T}_setup.md` | Playbook score / red flags / RS soft |
| `{T}_scenario_stop.md` | Scenario stop + Ladder |
| `{T}_verdict.md` | Phase 7 VERDICT block |
| `{T}_GEMINI_HANDOFF.md` | **Copy-ready** Phase 8 body only (see below) |
| `{T}_Final.md` | Soft Final = verdict + fenced HANDOFF + Trade Entry path |
| `{T}_Trade_Entry.csv` | Sheets row(s) |
| `{T}_SELF_VERIFY.md` | Self-VERIFY checklist |
| `MANIFEST.txt` | Absolute paths + HKT timestamp |

### One-click copy rule (Justin 2026-10-21)

1. **`{T}_GEMINI_HANDOFF.md`** = plain Phase 8 contract text only (banner → closing banner). No `#` headings, no Self-VERIFY, no CSV tables above/below the contract.
2. When Justin asks to send MD / HANDOFF / "one click copy": deliver the HANDOFF in chat inside **one** fenced block so the UI copy button grabs the whole contract:

````markdown
```text
══════════════════════════════════════════════
GEMINI HANDOFF — …
…
══════════════════════════════════════════════
```
````

3. **`{T}_Final.md`** must embed that same HANDOFF inside a single ` ```text ` fence (not raw unfenced prose).
4. Attach `{T}_GEMINI_HANDOFF.md` as a file **and** paste the fenced block in chat when he asks for copy/handoff.
5. Never put markdown tables or commentary inside the copy fence — paste pollution breaks Gemini paste.

## US RS enhance (MARKET=US) — soft interpret only

When MARKET=US and enhance columns present:

1. Read `RS_Role` / RSNHBP / Slope / NH / WeakDay / VolEdge per **Swing Setup Playbook** US RS section.
2. `RS_Role=candidate` or `RSNHBP=True` → bias STALK/WATCH; **never** alone raise to BUY.
3. `RS_Role=leader` → RS confirms; still pass hard BUY gates (Score/RR/Earnings/TZ/structure).
4. Missing quality flags → one-line TECHNICAL CONCERN only; do **not** alone BUY→WATCH.
5. **Do not** add Priority quality points again (Scanner already capped ≤+5 in Priority_Score).
6. HK CSV → skip.

## Phase 7 Decision (v4.7.1 fixes #1, #5)

Always report:

```
VERDICT:      [BUY|STALK|WATCH|PASS|AVOID]
PYTHON SAID:  [Action_Refined]
OVERRIDE:     [Yes/No] + reason
KEY REASON:   [one sentence]
RR BASIS:     [Close-anchored | Scenario-anchored @ $Entry, Stop $X (Stop_Type)]
```

### Hard rules (align Python)

```
if Breakdown and not Slap_Back:          AVOID
if Minervini=0 and RS_Score < 0:         AVOID   # AND, not OR (fix #1)
if Earnings PASS:                        PASS
```

### BUY

- Score ≥ 70
- **Paired RR** ≥ 2.5 (at-market: RR_Zone_Best or Tier RR; pullback: Scenario RR)
- Earnings CLEAR or CAUTION (CAUTION with note)
- No red flags 5/9/10; pullback must have valid PB_STRUCT (or a valid TZ stop under Scenario Stop Step 2b)
- Never BUY on UNKNOWN earnings
- Never use `RR_Ratio_Best` alone as BUY basis (fix #8)

### STALK (any)

- Score ≥ 55 and TZ_Active and Vol_Expansion < 0.80
- Score ≥ 60 and (Slap or SR_Flip) and Earnings ∈ {CLEAR, **UNKNOWN**}
- Score ≥ 55 and TZ_Active and MA_Compression
- Hidden pullback + Scenario RR ≥ 2.5 and entry zone not yet tagged

### WATCH

- Score ≥ 40 and paired RR ≥ 1.5
- Score ≥ 45 and Earnings CAUTION or UNKNOWN

### PASS

- Paired RR < 2.0 and not STALK; or Earnings PASS; or Score < 45

### AVOID

- Trend_Basic=0 **and** RS_Score<0; or Breakdown without Slap Back

### ATR_FALLBACK raise (at-market / breakout only)

If Stop_Type=ATR_FALLBACK and no TZ_Active and no SR_Flip and Entry≈Close:  
BUY only if RR≥3.0 **and** RS>20 **and** Stage2_Strict=1; else WATCH/STALK.  
Pullback with PB_STRUCT ignores this raise; no valid PB anchor → PASS.

### Override

- Python BUY but major red flag → downgrade + explain
- Python WATCH/PASS but Scenario RR≥2.5 and structure healthy → may raise to STALK
- Always state RR BASIS

## Phase 8 — GEMINI HANDOFF (contract)

Write this **exact body** into `{T}_GEMINI_HANDOFF.md` (plain file). On chat delivery, wrap the same body in one ` ```text ` fence for one-click copy.

```
══════════════════════════════════════════════
GEMINI HANDOFF — [TICKER] | [DATE]
══════════════════════════════════════════════
VERDICT:           […]
SETUP TYPE:        […]
STOP TYPE:         [TZ/SR_FLIP/PB_STRUCT/MA_STRUCT/VP_STRUCT/ATR_FALLBACK]
STOP ANCHOR:       [name $price | None (volatility only)]
SCENARIO ENTRY:    [$L – $U | At market ≈ $Close]
ENTRY ZONE:        $[lower] – $[upper]
ADJUSTED STOP:     $[final]
PRIMARY TARGET:    $[Ladder 1]  |  RR: [paired]x
EARNINGS:          [CLEAR/CAUTION/PASS/UNKNOWN] — [X] days
KEY SUPPORT:       $[stop] / [SR_Flip if active]
TECHNICAL CONCERN: [one line]
CLAUDE CONVICTION: [HIGH/MEDIUM/LOW]
RS_SCORE:          [n] (Stock% − HSI% or SPY%)
RS CONTEXT:        [US only — omit on HK] RS_Score=…｜1M=…｜3M=…｜Slope=…｜Up=…｜NH=…｜RSNHBP=…｜WeakDay%=…｜VolEdge=…｜質素加成=+n｜RS_Role=leader|candidate|
SECTOR WIND:       [US overlay if present — separate line] ETF_RS_theme=…｜sector_wind=…｜note=…
MARKET:            [HK|US]
PINNED_INPUTS:     [absolute paths of the exact files used: scanner CSV, Summary_US/Summary_HK, regime file]
DECISIONS_MADE:    [Justin/coordinator rulings already settled for this job, e.g. "NBIS Stop_Type=TZ pullback exception approved 2026-10-05" | none]
OPEN_QUESTIONS:    [unresolved items | none]
NEXT_GATE:         [who checks next + what passes, e.g. "Story Search → 敘事報告; Work Verifier → PASS/PASS_WITH_NOTES before Final"]
══════════════════════════════════════════════
```

Handoff control fields (fleet rule, see harness-bot-standard):
- **PINNED_INPUTS** — absolute paths of the exact data files this run used; never write "latest". If the TC pinned inputs, use exactly those files. Needed a file the TC did not pin → list its path under OPEN_QUESTIONS.
- **DECISIONS_MADE** — rulings already settled for this job; downstream must not re-open them. `none` if none.
- **OPEN_QUESTIONS** — `none` if none.
- **NEXT_GATE** — next checker and the pass condition.
- **RS CONTEXT** (MARKET=US) — one line as above; `質素加成=+n` is **documentation only** (already inside Priority_Score; do not re-score). Separate from `SECTOR WIND` / `sector_wind`. If enhance columns missing → `RS CONTEXT: N/A (pre-enhance CSV)` — never invent.
- **SECTOR WIND** — overlay theme/wind when present; never merge into RS CONTEXT.

Technical VERDICT locked — Story must not upgrade. Disclaimer at end (outside the copy fence if delivering in chat). Not investment advice.

## Market reminder

🇺🇸 RS vs SPY, ADR 14d · optional Haber RS enhance + RS_Role (soft) · 🇭🇰 RS vs HSI, ADR 20d (no enhance role) · Scripts: HK_swing_v4.5.3 / v4.6.1_Colab (+ US peers / us_swing_v451)
