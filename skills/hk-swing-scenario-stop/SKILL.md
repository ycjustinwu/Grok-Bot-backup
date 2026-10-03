---
name: Swing Scenario Stop
description: >-
  Use this when computing HK or US swing-trade stops and RR (v4.7.1) — pullback
  must use PB_STRUCT; ban Close-anchored ATR_FALLBACK for pullbacks; Freshness
  Gate; Risk% band; ascending Ladder.
---
# Swing Scenario Stop

**v4.7.1** for **HK and US**: choose stops by **entry scenario**, not blindly from Close-anchored `Adjusted_Stop`.

## Market notes

Use `ADR_Pct` from CSV as-is (🇺🇸 14d / 🇭🇰 20d). Prices: US `$` / HK `HK$`. Buffer must be real (not zero ticks above support).

## Step 1 — Scenario type

- **At-market / breakout** (Entry ≈ Close ±1%, or TZ-B / TZ-C) → may use `Adjusted_Stop` after Step 3
- **Pullback** (Scenario Entry < Close) → **forbid** direct `Adjusted_Stop` / ATR_FALLBACK; MUST re-anchor (Step 2)

## Step 2 — Pullback re-anchor (PB_STRUCT)

1. Entry Zone = support confluence band (e.g. `[FVG_Lower, AVWAP_20D_Low]`)
2. `Scenario_Stop` = nearest structure **below zone low** − 0.5×ATR  
   Candidates near→far: AVWAP_20D_Low, MA20, MA50, Bullish_FVG_Lower, Swing_Low_10D, VAL_60D, SR_Flip_Level  
   If **all** candidates sit inside/above the entry zone → **invalid → PASS**
3. Label `Stop_Type=PB_STRUCT` + anchor name/price
4. `Scenario_RR_Tn = (Target_n − Entry) / (Entry − Stop)`  
   If Target_n ≤ Entry → RR = N/A (cannot use that rung as reward)  
   Do **not** reuse Adj_RR_Ratio / Close-anchored RR_Ratio_Tn

Other types when setup dictates: `MA_STRUCT` (MA20−1×ATR), `VP_STRUCT` (VAL−0.5×ATR), `SR_FLIP`, `TZ` (Freshness Gate only)

## Step 3 — Validity (all scenarios)

1. Stop < entry-zone low (else ❌ STOP INVALID)
2. Stop below its structure anchor (buffer > 0)
3. Risk% = (Entry−Stop)/Entry×100 in **`[0.5×ADR_Pct, 2.5×ADR_Pct]`**  
   ADR_Pct is Close-based; if Entry vs Close differs >3%, note band is Close-approximated
4. Stop_Type=TZ → Freshness Gate: `Tight_Zone_Active=True` **and** `Close≥Tight_Zone_Low`

Any fail → `❌ STOP INVALID: [reason]` — re-anchor before publishing. Never publish STOP INVALID plans.

## Step 4 — Target ladder

Collect Target_1_Resistance / Target_2_Pattern / Target_3_ATR (ignore NaN).  
Sort **ascending** → Ladder 1/2/3 with scale-out **50% / +25% (cum 75%) / clear (100%)**.  
If original T2/T3 inverted → note「已重排」.  
If `Target_2_Source` / `Target_3_Source` present, label formula from Source — do not assume column suffix = formula.

Each entry scenario gets **its own** stop + paired RR. Never share one Close-anchored stop across scenarios.
