---
name: FRED VIX Term Structure
description: >-
  Use this when adding VIX/VXVCLS to a breadth report — fetch public FRED series
  pages VIXCLS and VXVCLS (no API key required); optional fred_vix.py if a key
  exists.
---
# FRED VIX Term Structure

Pull **VIX/VXVCLS**. Prefer **public FRED series pages** (no API key):

- https://fred.stlouisfed.org/series/VIXCLS
- https://fred.stlouisfed.org/series/VXVCLS

Also try CSV: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS` (same for `VXVCLS`).

`ratio = VIXCLS / VXVCLS` on the latest **common trading date**. FRED `date` = that session’s close (often published next morning HKT).

## Script (optional, needs key)

`/workspace/scripts/fred_vix.py` if `FRED_API_KEY` is set. Else scrape/fetch the public URLs above — **do not block on a key**.

```bash
python3 /workspace/scripts/fred_vix.py --quiet   # only if key present
```

`--alert` Telegram only if `TELEGRAM_BOT_TOKEN` is set.

Intraday VIX still comes from StockCharts OCR; FRED is EOD.

## Signal map

| Ratio | Label |
|-------|--------|
| > 1.00 | 🔴 UNCERTAINTY |
| 0.82–1.00 | 🟢 CALM (0.95–1.00 may note STRETCHED) |
| < 0.82 | 🟡 POOR_RETURNS |

If FRED lags vs OCR VIX, mark **推算** when mixing. Row 2 of the 9-row table, right after $VIX.
