---
name: US Abnormal Volume
description: >-
  Use this when screening a US abnormal-volume-spike CSV for movers — |change| >
  5%, RelVol > 2, market cap > $10B — then map each name to a thematic ETF for
  linkage.
---
# US Abnormal Volume

Screen **Justin-supplied** abnormal-volume only (chat paste or `abnormal-volume-spike-US_[DATE].csv` / day-folder files). Read **all** rows.

**Locked 2026-09-18:** Do **not** run `/workspace/scripts/us_abnormal_volume_screener.py` or TradingView scanner. If no Justin list, STOP and escalate — do not scrape.

## Keep only rows that meet **all three**

- Price Change % **> +5% or < −5%**
- Relative Volume **> 2**
- Market Cap **> $10B**

Drop names that fail any check. Missing RelVol or mcap → exclude and note the gap; do not invent.

## For every keeper

1. Map to the closest **Tier 1 thematic ETF** from the day’s theme scan (SOXX/SMH for semis, XBI for biotech, etc.).
2. Linkage:
   - Matching ETF same direction **> +1% / < −1%** → **板塊聯動**
   - ETF opposite or \|Δ\| **< 0.5%** → **個股行情**
3. Record: ticker, name, 1D%, RelVol, mcap, theme ETF + ETF 1D%, linkage.

## Rank for focus-stock pick

1. Theme-linked movers (板塊聯動) in today’s strong/weak ETFs
2. Isolated movers (個股行情)
3. Then larger cap + higher RelVol as tie-break

Hand the ranked list to catalyst research. If **zero** keepers, say so and do not invent names.
