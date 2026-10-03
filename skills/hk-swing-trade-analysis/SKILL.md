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
3. **Swing Scenario Stop** — scenario stops; pullback = PB_STRUCT; Ladder ascending
4. Phase 7 verdict + Phase 8 handoff
5. Trade Entry CSV row(s) for Sheets
6. Q&A / education as asked

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
- No red flags 5/9/10; pullback must have valid PB_STRUCT
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
MARKET:            [HK|US]
══════════════════════════════════════════════
```

Technical VERDICT locked — Story must not upgrade. Disclaimer at end. Not investment advice.

## Market reminder

🇺🇸 RS vs SPY, ADR 14d · 🇭🇰 RS vs HSI, ADR 20d · Scripts: HK_swing_v4.5.3 / v4.6.1_Colab (+ US peers)
