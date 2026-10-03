---
name: Stockbee T2108 Monitor
description: >-
  Use this when Justin says stockbee / t2108 / stockbee monitor — fetch the
  public Market Monitor CSV, stale-check, build Excel, and send with a real
  .xlsx filename.
---
# Stockbee T2108 Monitor

Daily Stockbee Market Monitor → Excel for Justin. Triggers: `stockbee` / `t2108` / `stockbee monitor`.

## Pipeline

1. **Stockbee T2108 Fetch** — CSV, dual-verify, stale-snapshot
2. **Stockbee T2108 Excel** — styled 16-col workbook, dated filename
3. **Telegram Xlsx Send** — attach/send with readable `.xlsx` name; short caption (`Stockbee Market Monitor — N trading days`); full notes in a follow-up

If CSV fully stale: do not treat T2108/S&P figures as live; overlay StockCharts breadth actuals and warn.

No secrets in commands. Download a **fresh** CSV every run. History years stay in the sheet.
