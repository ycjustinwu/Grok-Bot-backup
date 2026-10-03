---
name: Stockbee T2108 Fetch
description: >-
  Use this when fetching Stockbee T2108 / Market Monitor CSV — dual-verify head
  and tail, then stale-snapshot check against the prior row before publishing.
---
# Stockbee T2108 Fetch

Download Stockbee Market Monitor CSV and prove it is fresh. Triggers: `stockbee` / `t2108` / `stockbee monitor`.

## Source

Google Sheet CSV:
`https://docs.google.com/spreadsheets/d/1O6OhS7ciA8zwfycBfGPbP2fWJnR0pn2UUvFZVDP9jpE/export?format=csv`

```bash
curl -sL "https://docs.google.com/spreadsheets/d/1O6OhS7ciA8zwfycBfGPbP2fWJnR0pn2UUvFZVDP9jpE/export?format=csv" -o /tmp/stockbee_full.csv
```

## Dual-verify (mandatory)

Check **both** ends + a date grep. One end only is a blind spot.

- `head -10`
- `tail -10`
- grep latest year rows (e.g. `^2026/` or `^2025/`)

If all three are stale → **source dead**, stop. If any is fresh → proceed.

## Stale-snapshot (mandatory before publish)

Latest row vs previous: non-rolling cols `[1,2,5,6,7,8,11,12,14]` (Up4%, Down4%, Quarter, Month, 34D, Universe, T2108).

- All match → **full stale**: do not publish those figures as live. Fall back to morning StockCharts breadth OCR ($SPX / $SPXA50R / $SPXA200R / $SPXA20R / $VIX). Flag in the report. Highlight the row in Excel (moccasin) + add an “Authoritative” sheet.
- Some match → **partial stale**: note which cols.
- None match → fresh.

Headers are sheet row 2; data from row 3. Hand rows to **Stockbee T2108 Excel**.
