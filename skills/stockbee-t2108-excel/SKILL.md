---
name: Stockbee T2108 Excel
description: >-
  Use this after Stockbee T2108 Fetch to build the styled 16-column Market
  Monitor xlsx (frozen header, T2108 + S&P) with moccasin highlight if the
  latest row is a stale snapshot.
---
# Stockbee T2108 Excel

Build `Stockbee_Monitor_YYYY-MM-DD.xlsx` from the verified CSV.

## Layout

- Sheet `Stockbee Monitor`
- Headers (row 1, frozen `A2`): Date, # Up 4%, # Down 4%, 5D Ratio, 10D Ratio, # Up 25%+ Q, # Down 25%+ Q, # Up 13%+ M, # Down 13%+ M, # Up 50%+ M, # Down 50%+ M, # Up 13%+ 34D, # Down 13%+ 34D, Universe, T2108, S&P
- Map CSV columns 0–14 + last col as S&P (strip commas/quotes)
- Header: white bold on `#2E5090`; date col `#F0F0F0`; thin borders; center
- If stale-snapshot: moccasin fill on the latest data row; optional sheet `Authoritative` with StockCharts actuals

Save under `/workspace/` (or `/tmp/`) with a **readable dated filename**. Then **Telegram Xlsx Send** / attach in chat — never a hash name.
