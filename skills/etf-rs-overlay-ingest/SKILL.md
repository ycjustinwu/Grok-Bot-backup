---
name: ETF RS Overlay Ingest
description: >-
  Use this when Market Awareness or US Swing Scanner needs Justin’s daily ETF
  Relative Strength Dashboard as a non-scoring overlay — load Drive/local sheet,
  stamp US trade date, aggregate themes; never invent RS numbers.
---
# ETF RS Overlay Ingest

Shared **read-only** ingest for Justin’s **ETF Relative Strength Dashboard**. Overlay only — never a TOTAL / band / BUY-STALK score input.

## Source of truth

| Field | Value |
|-------|--------|
| Drive file id | `1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ` |
| Title | ETF Relative Strength Dashboard |
| Tabs | `Dashboard` (daily), `Price History`, `Import Log`, `Universe` |
| Local snapshot | `/workspace/etf-rs/ETF_Relative_Strength_Dashboard.xlsx` |

**Usage gate:** reuse this sheet (Drive id or fresh local xlsx). Do **not** rebuild the ~124 ETF universe daily.

## Metric definitions (locked — do not reinterpret)

- **RS actual** = 30d PERCENTRANK of (ETF/VOO). **Not** “beat VOO by X%”.
- **vs VOO 5d / 20d** = actual relative return (sheet decimals; report as % when writing prose).
- **2-day / 5-day trend** = `Rising` / `Declining` / `No Trend` when RS moves by more than ±7.5 pts.
- **US trade date** on Dashboard row = US session date. HK download day is often T+1 — **always stamp the sheet’s US trade date** in every consumer output. Never substitute HK calendar day.

## Themes (align with Regime P1–P7 / L2)

`P1 FCF/Quality`, `P2 Hardware/Infra`, `P3 Biotech`, `P4 Speculation`, `P5 Defensive`, `P6 Frontier Tech`, `P7 Software/Cyber`, plus `L2 …` narratives, `Macro Rates` / `Macro Credit` / `Macro Vol` / `Macro USD`, `Risk Appetite`, `Benchmark` (VOO — exclude from Favor/Avoid aggregates).

## Steps

1. Prefer Google Drive `read_file_content` / download on file id above. If Drive unavailable, use local snapshot **only if** Import Log / Dashboard US trade date matches expected US session (or Justin confirmed).
2. Read **Dashboard** columns: `Theme`, `Description`, `Ticker`, `Latest Price`, `RS actual`, `RS 2d ago`, `RS 5d ago`, `2-day trend`, `5-day trend`, `vs VOO 5d`, `vs VOO 20d`, `US trade date`.
3. Read **Universe** for Symbol→Theme map (Scanner mapping aid).
4. Write structured extract to  
   `/workspace/etf-rs/overlay/YYYY-MM-DD/dashboard.json`  
   (use sheet US trade date as `YYYY-MM-DD`, not HK download day) with:
   - `us_trade_date`
   - `source` (`drive` | `local`)
   - `rows[]` (per ticker; include `trend_2d` + `trend_5d` from sheet `2-day trend` / `5-day trend` — required for theme-tilt 趨勢觀察)
   - `theme_agg[]`: per Theme (exclude Benchmark): `n`, `avg_rs`, `median_rs`, `rising_5d_share`, `declining_5d_share`, `avg_vs_voo_5d`, `avg_vs_voo_20d`, `top_by_rs` (up to 5 tickers with RS + vs VOO 5d + 2d/5d trend)
5. Hand extract to [ETF RS Theme Tilt](sand-workflow:etf-rs-theme-tilt) and/or [US Swing Sector Wind](sand-workflow:us-swing-sector-wind).

## DATA GATE

Critical for consumers that require the overlay:

- Sheet missing, empty Dashboard, or **US trade date stale vs expected US session** → **STOP** that overlay phase; notify 總指揮 (who notifies Justin). Do not invent RS / trends / vs VOO.
- Do **not** trip Regime Pillar A/B TOTAL gate solely because RS overlay failed — mark overlay DATA GAP and omit Favor/Avoid section (or Scanner columns = `N/A`) per consumer skill. If Justin / 總指揮 marked RS overlay **mandatory** for that run, STOP the consumer deliverable.

## ANTI-JOBS

- Do not feed RS into Regime TOTAL, band, hysteresis, FT/CC, or Exposure math.
- Do not invent PERCENTRANK or relative returns.
- Do not rebuild universe tickers from TradingView as a substitute for this sheet.
- Do not treat crypto/meme ETFs as equity sector wind for ordinary stocks (see sector-wind skill).

## VERIFY

- [ ] File id / local path used; no daily universe rebuild
- [ ] `us_trade_date` = Dashboard stamp (not HK download day)
- [ ] RS actual treated as PERCENTRANK 0–100, not “% beat VOO”
- [ ] `theme_agg` excludes Benchmark; numbers from sheet only
- [ ] No path into Pillar A/B / TOTAL / BUY-STALK score formulas
- [ ] On miss/stale: gate or explicit DATA GAP (no fabrications)
