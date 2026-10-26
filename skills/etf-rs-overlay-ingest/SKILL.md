---
name: ETF RS Overlay Ingest
description: >-
  Use this when Market Awareness or US Swing Scanner needs Justin’s daily ETF
  Relative Strength / rotation as a non-scoring overlay — prefer Market Master
  tab ETF 輪動; legacy Drive only if Justin says; never invent RS numbers.
---
# ETF RS Overlay Ingest

Shared **read-only** ingest for Justin’s ETF theme RS / rotation overlay. Overlay only — never a TOTAL / band / BUY-STALK score input.

## Source of truth (LOCKED 2026-10-22)

| Priority | Source |
|----------|--------|
| **1 (default)** | Market Master spreadsheetId `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` tab **`ETF 輪動`** |
| **2 (legacy only if Justin says)** | Drive file id `1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ` — ETF Relative Strength Dashboard (tabs `Dashboard`, `Price History`, `Import Log`, `Universe`) |
| Local snapshot (legacy fallback) | `/workspace/etf-rs/ETF_Relative_Strength_Dashboard.xlsx` |

Canonical: `/workspace/docs/market-master-canonical-2026-10-22.md`.

**Usage gate:** Prefer `ETF 輪動` on Market Master every run. Do **not** rebuild the ~124 ETF universe daily. Do **not** use legacy Drive as primary unless Justin / 總指揮 explicitly says so for that run.

## Metric definitions (locked — do not reinterpret)

- **RS actual** = 30d PERCENTRANK of (ETF/VOO). **Not** “beat VOO by X%”.
- **vs VOO 5d / 20d** = actual relative return (sheet decimals; report as % when writing prose).
- **2-day / 5-day trend** = `Rising` / `Declining` / `No Trend` when RS moves by more than ±7.5 pts.
- **US trade date** on Dashboard / 輪動 row = US session date. HK download day is often T+1 — **always stamp the sheet’s US trade date** in every consumer output. Never substitute HK calendar day.

## Themes (align with Regime P1–P7 / L2)

`P1 FCF/Quality`, `P2 Hardware/Infra`, `P3 Biotech`, `P4 Speculation`, `P5 Defensive`, `P6 Frontier Tech`, `P7 Software/Cyber`, plus `L2 …` narratives, `Macro Rates` / `Macro Credit` / `Macro Vol` / `Macro USD`, `Risk Appetite`, `Benchmark` (VOO — exclude from Favor/Avoid aggregates).

## Steps

1. Prefer Google Sheets MCP on Market Master tab **`ETF 輪動`**. Only if Justin authorized legacy: Drive `read_file_content` / download on `1cgrNJ…`, or local snapshot **only if** Import Log / Dashboard US trade date matches expected US session.
2. Read columns equivalent to: `Theme`, `Description`, `Ticker`, `Latest Price`, `RS actual`, `RS 2d ago`, `RS 5d ago`, `2-day trend`, `5-day trend`, `vs VOO 5d`, `vs VOO 20d`, `US trade date` (map 輪動 column names if renamed).
3. Read Universe / theme map if present (Scanner mapping aid).
4. Write structured extract to `/workspace/etf-rs/overlay/YYYY-MM-DD/dashboard.json` (use sheet US trade date as `YYYY-MM-DD`) with:
   - `us_trade_date`
   - `source` (`market_master_etf_rotation` | `drive_legacy` | `local`)
   - `rows[]` (per ticker; include `trend_2d` + `trend_5d`)
   - `theme_agg[]`: per Theme (exclude Benchmark): `n`, `avg_rs`, `median_rs`, `rising_5d_share`, `declining_5d_share`, `avg_vs_voo_5d`, `avg_vs_voo_20d`, `top_by_rs`
5. Hand extract to [ETF RS Theme Tilt](sand-workflow:etf-rs-theme-tilt) and/or [US Swing Sector Wind](sand-workflow:us-swing-sector-wind).

## DATA GATE

- Sheet missing, empty 輪動/Dashboard, or **US trade date stale vs expected US session** → **STOP** that overlay phase; notify 總指揮. Do not invent RS / trends / vs VOO.
- Do **not** trip Regime Pillar A/B TOTAL gate solely because RS overlay failed — mark overlay DATA GAP and omit Favor/Avoid section per consumer skill. If Justin / 總指揮 marked RS overlay **mandatory** for that run, STOP the consumer deliverable.

## ANTI-JOBS

- Do not feed RS into Regime TOTAL, band, hysteresis, FT/CC, or Exposure math.
- Do not invent PERCENTRANK or relative returns.
- Do not rebuild universe tickers from TradingView as a substitute.
- Do not default to legacy `1cgrNJ…` when Market Master `ETF 輪動` is reachable.

## VERIFY

- [ ] Market Master `ETF 輪動` used first (or Justin-authorized legacy disclosed)
- [ ] `us_trade_date` = sheet stamp (not HK download day)
- [ ] RS actual treated as PERCENTRANK 0–100
- [ ] `theme_agg` excludes Benchmark; numbers from sheet only
- [ ] No path into Pillar A/B / TOTAL / BUY-STALK score formulas
- [ ] On miss/stale: gate or explicit DATA GAP (no fabrications)
