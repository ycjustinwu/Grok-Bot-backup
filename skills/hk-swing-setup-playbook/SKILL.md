---
name: Swing Setup Playbook
description: >-
  Use this when identifying and scoring HK or US swing setups from Python CSV
  last-row data — Tight Zone v2.1, setups A–H (incl. Setup C TZ fallback), three
  RR systems, Priority Score (v4.7.1), hidden pullbacks, red flags.
---
# Swing Setup Playbook

Identify and score setups from the CSV last row (**HK or US**). **v4.7.1** (fixes #3–4, #6–8 + TZ v2.1).

## Market

- 🇺🇸 RS = Stock% − SPY% · ADR in CSV = 14-day
- 🇭🇰 RS = Stock% − HSI% · ADR in CSV = 20-day

## Soft Trend

Close>MA50 **and** Close>MA20 **and** SMA50_Slope>0.

## Three RR systems (v4.7.1 fixes #3, #8) — keep separate

| Field | Entry anchor | Stop anchor | Use |
|-------|--------------|-------------|-----|
| `RR_Ratio` (Optional) | Close | Swing_Low_10D (Suggested_Stop) | Conservative ref only |
| `RR_Zone_T1/T2/T3/Best` | Close | Tight_Zone_Low | TZ structural RR |
| `RR_Ratio_T1/T2/T3/Best` | Close | **Adjusted_Stop** | Python main target RR |
| **Scenario RR** (Claude) | **Scenario Entry** | **Scenario Stop** | **Only legal RR for pullback BUY/STALK** |

**Forbidden:** call `RR_Ratio_Best` 「Swing Low RR」.  
**Forbidden:** use any Close-anchored RR for pullback BUY.  
`RR_Ratio_Best` = max(T1,T2,T3) with fixed risk → always biased to farthest target — **never** sole BUY basis. Use **paired** RR (at-market: Zone/Tier; pullback: Scenario).

## Tight Zone v2.1

| Param | Value |
|-------|-------|
| Tight Day vol | Volume < Vol_Avg_20 × **0.85** |
| Tight Day range | (High−Low) ≤ ADR × **1.20** |
| Zone Active length | **2–10** days |
| Non-tight exemptions | max **2** days |
| Start trend | Minervini=1 **or** Soft Trend |

**Freshness Gate** before any TZ stop: last bar `Tight_Zone_Active=True` **and** `Close ≥ Tight_Zone_Low`. Else Zone dead — ban TZ stop (re-anchor).

Playbook priority: TZ-C > TZ-B > TZ-A (last bar only).

## Hidden pullback

If `Setup_Type=No_Clear_Setup`: Higher_Lows≥**8**, SMA50_Slope>0, price within ±3% of AVWAP_20D_Low / MA20 / MA50 / Bullish_FVG / POC / SR_Flip → treat as Setup B + note Claude override. Stop **MUST** PB_STRUCT.

## Setups A–H

| ID | Name | Entry bias | Stop bias |
|----|------|------------|-----------|
| A | VCP Breakout | Break Res20 / Zone High | TZ − 0.5 ATR (Gate) |
| B | Pullback Support | Support confluence | **PB_STRUCT** |
| C | Power Play | Break Zone High | See Setup C routing |
| D | Trend Respect | MA10/20 pullback | **MA_STRUCT** |
| E | Bottom Reversal | POC+0.5 ATR | **VP_STRUCT** |
| F | TZ-B Mini BO | Mini_Breakout_Price | TZ − 0.5 ATR |
| G | TZ-C Slap Back | Slap_Back_Entry | Slap_Back_Stop |
| H | S/R Flip Retest | Near SR_Flip_Level | SR_FLIP − 0.5 ATR |

### Setup C routing (v4.7.1 fix #7)

Need: RS>15, Days≥4, 5%≤Ext≤15%, Dist_52W≥−5%, Vol_Exp≥1.5.

- If **TZ_Active and Close ≥ Zone Low** → stop = Zone Low − 0.5×ATR
- If Zone dead → **do not** use stale Zone Low; fall back to Swing_Low_10D − 0.5×ATR **or** Close − 1×ATR (ATR_FALLBACK); note「Zone 已離開，止損改結構/波動回退」; raise BUY bar (Phase 7 ATR_FALLBACK rules)

## Red flags 1–10

1 Overextended (Ext>15% or RSI>75)  
2 Vol_Expansion<0.8 (non-VCP)  
3 Minervini=0 (except Bottom Reversal / hidden pullback)  
4 Paired RR < 2:1 (pullback → Scenario RR)  
5 **(Resistance_20D − Close)/Close×100 < ADR_Pct × 0.5** — both sides are %; **not** ×0.5% (fix #6)  
6 Core setup vs Extended conflict  
7 Breakdown w/o Slap Back → AVOID  
8 Tight_Zone_Days > **10** (v2.1 cap)  
9 Stop ≥ entry-zone low → STOP INVALID  
10 Target order inverted → re-sort then assign

**Earnings:** PASS≤7 → hard AVOID · CAUTION 8–14 → shorten · **UNKNOWN is not CLEAR** — never BUY; STALK only slap/SR paths; user must verify date

## Priority Score (v4.7.1 fix #4 — align Python)

| Item | Pts |
|------|-----|
| Minervini_Trend_Basic=1 | +20 |
| Close>MA20 and MA20>MA50 | +10 |
| RS_Score >20 / >10 / >0 | +30 / +20 / +10 (skip if NaN) |
| TZ Active and Days≥5 / ≥3 | +20 / +10 |
| Slap_Back=True | +8 |
| **RR_Zone_Best** ≥3 / ≥2.5 / ≥2.0 | +20 / +10 / +5 |
| (if Zone Best NaN) RR_Ratio_Best ≥3 / ≥2 | +20 / +10 |
| Extended / Low_Vol_Grind | −20 / −10 |
| (Res20−Close)/Close×100 < ADR_Pct×0.5 | −10 |
| Vol_Expansion ≥1.5 / ≥1.2 / <0.8 | +5 / +3 / −5 |
| Power_Play / VCP / Pullback | +10 / +8 / +5 |
| Earnings PASS / CAUTION / **UNKNOWN** | −30 / −15 / **−5** |
| SR_Flip and not Slap_Back | +5 |
| **Clamp 0–100 integer** | |

Stars: 80–100 ★5 · 60–79 ★4 · 40–59 ★3 · 20–39 ★2 · 0–19 ★1  
If Scenario RR ≫ Close RR, note Pillar 4 understates pullback quality.
