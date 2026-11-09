---
name: US Abnormal Volume
description: >-
  Use this when building US brief focus stocks from TradingView MCP
  abnormal-volume seeds (Justin paste overrides) plus mega-cap industry-cluster
  sweep, then map keepers to thematic ETFs.
---
# US Abnormal Volume

Build the US brief mover seed list, then map keepers to thematic ETFs. Also fold the **mega-cap sweep** cluster into epicenter ranking.

## 1. Get seeds (locked 2026-10-14)

**Primary:** run [TV Abnormal Volume MCP](sand-workflow:tv-abnormal-volume-mcp) for **US** UP and DOWN **before** analysis.

**Override:** if Justin pastes/attaches an AV list for that session, use his list and skip MCP for that side.

Do **not** run `/workspace/scripts/us_abnormal_volume_screener.py` or scrape TradingView in the browser when MCP is available.

US MCP gates (OpenClaw): close>$1, |chg|≥5%, mcap>$5B USD, RelVol10d>2 both sides, Value.Traded>$5M USD; **post-filter drop OTC** (and `OTC:` prefixes) **before** RelVol ranking. Report raw vs US-primary counts.

## 1b. Mega-cap sweep (locked 2026-10-31)

Also run the MCP **mega-cap sweep** (mcap≥$50B, |Δ|≥3%, drop OTC — see tv-abnormal-volume-mcp). Detect **same-industry clusters** (typically 8–12 names at −3~−6% or +3~+6%).

- Cluster present → flag as **震央候選** for parent brief opening / headline #1 even if RelVol≤2.
- Map cluster to the closest Tier-1 thematic ETF when possible.
- Do not force every mega-sweep name into cash Focus — Focus stays AV-ranked + epicenter boost; sweep feeds **narrative epicenter**, not automatic Part 2 slots.

## 2. Keepers

MCP (or Justin) OpenClaw seeds that already passed gates are keepers. Do **not** re-apply the old mcap>$10B gate. If using a raw Justin CSV that was not pre-filtered, apply the OpenClaw gates above and drop OTC.

Missing RelVol or mcap on a non-MCP row → exclude and note; do not invent.

Suspended / stale-print names: exclude and state count.

## 3. For every keeper

1. Map to the closest **tier 1 thematic ETF** from the day’s theme scan (SOXX/SMH for semis, XBI for biotech, etc.).
2. Linkage:
   - Matching ETF same direction **> +1% / < −1%** → **板塊聯動**
   - ETF opposite or |Δ| **< 0.5%** → **個股行情**
3. Record: ticker, **official name from data source** (never infer from a peer), 1D%, RelVol, mcap, theme ETF + ETF 1D%, linkage.
4. Note low-RV large |Δ| vs high-RV large |Δ| separately (passive wash vs active supply).

## 4. Rank for focus-stock pick

1. Theme-linked movers (板塊聯動) in today’s strong/weak ETFs
2. Isolated movers (個股行情)
3. Then larger cap + higher RelVol as tie-break

Hand the ranked list **plus** mega-sweep cluster note to catalyst research. If **zero** OpenClaw keepers after a closed session, say so and do not invent names (DATA GATE via 總指揮 if MCP failed). Mega-sweep-only days can still supply opening 震央 without filling Part 2 inventively.
