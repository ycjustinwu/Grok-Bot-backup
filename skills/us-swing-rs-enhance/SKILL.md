---
name: US Swing RS Enhance
description: >-
  Use when running or changing US Swing Scanner Haber-style RS fields (RS_Line,
  RSNHBP, RS_Role, quality ≤+5) or explaining how Potential Setups rank leaders
  vs candidates.
---
# US Swing RS Enhance (A + ≤+5 B)

Locked 2026-10-15 with Justin / 美股 Swing Setup. Applies to `/workspace/us-swing-scanner/scripts/us_swing_v451.py` after the shared-SPY `RS_Score` block.

## Do / don't

- **Do** export bypass columns on `Summary_US.csv` + `Claude_Input_Slim.csv`.
- **Do** keep `RS_Score` (≈63d stock%−SPY%) as the only RS magnitude bucket in Priority (+10 / +20 / +30).
- **Do not** invent IBD `RS_Rating` 1–99 (no full-market universe).
- **Do not** let Setup re-add the quality points (Scanner already caps ≤+5).
- **Do not** change Action_Refined gates from RS flags alone; `RSNHBP` never triggers BUY.

## Formulas

| Field | Definition |
|-------|------------|
| `RS_Line` | `Close / SPY_Close` |
| `RS_Line_Slope` | `(RS_Line_t − RS_Line_{t−20}) / 20` (display only) |
| `RS_Line_Chg_20` | `RS_Line_t / RS_Line_{t−20} − 1` |
| `RS_Line_Up` | `RS_Line_Chg_20 ≥ 0.01` (**≥ +1% over 20 sessions** — use this, not raw Slope＞0) |
| `RS_Line_NH` | `RS_Line` ≥ 63d max `RS_Line` |
| `RSNHBP` | `RS_Line_NH` and `Close` ＜ 63d max `Close` |
| `Weak_Day_RS_Pct` | Among last 20 SPY-down days, % where stock daily return ＞ SPY return |
| `Highest_Vol_Edge` | Today volume ≥ 95% of 252d max volume |
| `RS_1M` / `RS_3M` | Existing 20d / 60d relative % vs SPY |

## Priority quality (cap ≤+5)

1. `RS_Line_Up` **and** `RS_Line_NH` → +3
2. `Weak_Day_RS_Pct ≥ 60` → +2
3. `Highest_Vol_Edge` **and** setup tags contain `Power_Play` or `VCP_Breakout` → +2
4. Sum capped at **+5**; **`RSNHBP` never adds**

## `RS_Role` (export label, not a score input)

Priority order:

1. `RSNHBP` → `candidate`
2. Else `RS_Score > 20` and (`RS_Line_Up` or `RS_Line_NH`) → `leader`
3. Else `RS_Line_Up` and `Weak_Day_RS_Pct ≥ 60` → `candidate`
4. Else blank

## Sort tie-break (same Priority_Score)

`RSNHBP` → `RS_Line_Chg_20` → `Weak_Day_RS_Pct` → `Highest_Vol_Edge` (all descending).

## Slim / overlay

Scanner Slim ends with RS bypass cols including `RS_Role`. [US Swing Sector Wind](sand-workflow:us-swing-sector-wind) still **appends** `ETF_RS_theme`, `sector_wind`, `sector_wind_note` after. Keep stock RS (`RS CONTEXT`) separate from ETF theme wind.

## Known bug fixed

Raw `RS_Line_Slope > 0` false-labeled HTFL as `leader` when Slope≈0 (float noise). Always gate on `RS_Line_Up` (≥1% / 20d).

## VERIFY

- [ ] New cols on Summary + Slim; `RS_Role` ∈ {`leader`,`candidate`,``}
- [ ] Priority still uses RS_Score buckets; quality ≤+5; RSNHBP not in Priority
- [ ] No dual-count with Setup checklist
- [ ] Overlay wind cols still appended; scores unchanged by overlay
