---
name: Swing CSV Validate
description: >-
  Use this when the user uploads a HK or US swing-trade Python CSV — validate
  Core vs Optional columns (v4.7.1 / v4.5.3+), detect market, run stop/TZ/target
  health checks, then hand off to analysis.
---
# Swing CSV Validate

Validate a swing-trade CSV before analysis. **v4.7.1** (fix #2 + TZ v2.1). Compatible: `HK_swing_v4.5.3_final` / `HK_swing_v4.6.1_Colab` / US equivalents.

## Market detect

- `.HK` / 港股 / HSI / filename `HK_Swing` → **HK** (RS vs HSI; ADR=20d)
- US ticker / SPY / `US_Swing` → **US** (RS vs SPY; ADR=14d)

State market in the load line.

## Step 0.1 — Field tiers (v4.7.1 fix #2)

**Core** (v4.5.3+ must have): Date (or index), Close, Volume, MA10/20/50/150/200, ATR, ADR_Pct, Vol_Avg_20/50, Vol_Expansion, RS_Score, RS_1M, RS_3M, Suggested_Stop, Risk_Dollar, Risk_Pct, Resistance_20D, Minervini_Trend_Basic, Minervini_Stage2_Strict, Higher_Lows/Highs_Count, Tight_Zone_*, Mini_Breakout_*, Breakdown_Flag, Slap_Back_*, RR_Zone_*, Playbook_Flag, RSI_14, AVWAP_*, POC_*, FVG*, Target_1/2/3, RR_Ratio_T*, Setup_Type, Priority_Score, Adjusted_Stop, Stop_Type, Adj_*, SR_Flip_*, MA_Compression_Zone, Earnings_*, Action_Refined

**Optional** (v4.6.1 guarantees; v4.5.3 may lack): Swing_Low_20D, Risk_ATR_Multiple, Reward_Dollar, Reward_Pct, RR_Ratio, Resistance_20D_Prior, HSI_Close / SPY_Close, Target_2_Source, Target_3_Source

- Missing **Optional** → continue; note「本 CSV 未含 v4.6.1 補充欄位」
- Missing **Core** → list gaps; ask regenerate with v4.5.3+ / v4.6.1. **Stop.**


## Step 0.1b — US RS enhance columns (MARKET=US only; optional)

After 2026-10-15 Scanner A+≤+5 B export, US Summary_US / Claude_Input_Slim / per-ticker CSVs may include:

`RS_Line`, `RS_Line_Slope`, `RS_Line_Chg_20`, `RS_Line_Up`, `RS_Line_NH`, `RSNHBP`, `Weak_Day_RS_Pct`, `Highest_Vol_Edge`, `RS_Role`

(+ overlay still appends `ETF_RS_theme` / `sector_wind` / `sector_wind_note` after Slim/Summary).

- These are **Optional** — never FAIL Core for missing them (pre-2026-10-15 / HK / mid-transition runs).
- **MARKET=US** and columns missing → ⚠️ WARN/note「US RS enhance 欄缺席（舊 run 或未 export）；interpret 跳過質素旗／RS_Role；唔好發明值」.
- **MARKET=HK** → ignore this block entirely (HK path unchanged).
- Present but NaN/empty `RS_Role` is valid (means neither leader nor candidate) — do not invent `leader`/`candidate`.
- Do not treat Slim as fixed 22-col: post-enhance Slim is ~31 cols before overlay (~34 after sector_wind trio); validate by **name**, not column count.
- Prefer `RS_Line_Up` (20d RS_Line change ≥ +1%) over raw `RS_Line_Slope>0` when both present — Slope alone can be ≈0 float noise.
- `RSI_14` remains momentum only — not relative strength.

## Step 0.2 — Health check (last row)

1. Last date vs today >3 days → stale warn
2. Close=0 / Volume=0 / ATR NaN → anomaly
3. Minervini_Trend_Basic, Extension_MA20_Pct, RSI_14
4. Stop sanity:
   - Adjusted_Stop ≥ Close → ❌ data anomaly
   - Stop_Type=TZ but (Tight_Zone_Active≠True **or** Close < Tight_Zone_Low) → ⚠️ TZ stop stale; Phase 4 must re-anchor (Python may keep Zone ≤5 bars TTL — still ban TZ stop if Gate fails)
   - Target_1/2/3 not ascending → ⚠️ re-sort in Phase 4
5. Success: `✅ 已成功載入 [ticker]（[HK|US]）數據，共 [N] 日記錄。最後交易日：[date]。`

Never invent columns. Hand off to Swing Setup Playbook.
