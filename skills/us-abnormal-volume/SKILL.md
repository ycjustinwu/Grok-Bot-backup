---
name: US Abnormal Volume
description: >-
  Use this when building US brief focus stocks from abnormal-volume seeds —
  primary source is TradingView MCP (OpenClaw US criteria); Justin paste
  overrides; then map keepers to thematic ETFs.
---
# US Abnormal Volume

Build the US brief mover seed list, then map keepers to thematic ETFs.

## 1. Get seeds (locked 2026-10-14)

**Primary:** run [TV Abnormal Volume MCP](sand-workflow:tv-abnormal-volume-mcp) for **US** UP and DOWN **before** analysis.

**Override:** if Justin pastes/attaches an AV list for that session, use his list and skip MCP for that side.

Do **not** run `/workspace/scripts/us_abnormal_volume_screener.py` or scrape TradingView in the browser when MCP is available.

US MCP gates (OpenClaw): close>$1, |chg|≥5%, mcap>$5B USD, RelVol10d>2 both sides, Value.Traded>$5M USD; **post-filter drop OTC**.

## 2. Keepers

MCP (or Justin) seeds that already passed gates are keepers. Do **not** re-apply the old mcap>$10B gate. If using a raw Justin CSV that was not pre-filtered, apply the OpenClaw gates above and drop OTC.

Missing RelVol or mcap on a non-MCP row → exclude and note; do not invent.

## 3. For every keeper

1. Map to the closest **Tier 1 thematic ETF** from the day’s theme scan (SOXX/SMH for semis, XBI for biotech, etc.).
2. Linkage:
   - Matching ETF same direction **> +1% / < −1%** → **板塊聯動**
   - ETF opposite or |Δ| **< 0.5%** → **個股行情**
3. Record: ticker, name, 1D%, RelVol, mcap, theme ETF + ETF 1D%, linkage.

## 4. Rank for focus-stock pick

1. Theme-linked movers (板塊聯動) in today’s strong/weak ETFs
2. Isolated movers (個股行情)
3. Then larger cap + higher RelVol as tie-break

Hand the ranked list to catalyst research. If **zero** keepers after a closed session, say so and do not invent names (DATA GATE via 總指揮 if MCP failed).
