---
name: US Focus Catalyst
description: >-
  Use this when picking 3 US cash-session focus stocks from abnormal-volume keepers and
  searching the web for same-day catalysts — earnings, downgrade, sector
  rotation — with cited sources. After-hours Mag7/large-cap earnings belong in
  us-market-daily-brief 盤後業績, not as forced cash Focus.
---
# US Focus Catalyst

Pick **exactly 3** **cash-session** focus names from the abnormal-volume ranked list (gainers **or** losers). Prefer theme-linked, then isolated, then large-cap high RelVol — **except** epicenter boost below.

**Boundary (Justin 2026-10-22):** Part 2 Focus = **cash AV keepers**. Large-cap **after-hours** earnings that drive **tonight’s** tape (Mag7, mega-cap, key semi-equipment) go in the parent brief’s `### 盤後業績` ([US Market Daily Brief](sand-workflow:us-market-daily-brief)) — do **not** displace AV Focus solely because Justin named AH reporters or X Monitor flagged them. If Justin names tickers that are also cash keepers／epicenters, they may still land in Focus via ranking.

## Ranking (Claude-compare 2026-09-09)

1. Theme-linked movers（板塊聯動）in today’s strong/weak ETFs
2. Isolated movers（個股行情）
3. Larger cap + higher RelVol as tie-break

**Epicenter boost (mandatory):** any keeper with **|1D| ≥ 10%** AND **RelVol ≥ 4×** must land in the top 3 even if another name is a “cleaner” theme-linked spillover. Prefer the **epicenter ticker** (e.g. NVS) over a secondary spillover (e.g. AMGN) when both pass filters, unless Justin asks for theme-confirmation names. Different focus sets vs another model are OK if filters + live search are satisfied.

## Mandatory live search

For **each** of the 3 tickers, run web search (do not skip):

- `[TICKER] [MONTH DAY YEAR] earnings news catalyst`
- For the weakest / selloff name also: `[TICKER] [MONTH DAY YEAR] downgrade selloff reason`
- Plus one sector query: `[TICKER] [MONTH DAY YEAR] sector rotation`

Date = the **session date** of the CSVs (US cash close), not Hong Kong tomorrow.

## Catalyst depth

Each focus stock needs **≥2 sourced factual bullets** (clinical metric, policy/effective date, index inclusion date, peer move, etc.) **before** 可行動洞察 — not only a one-line catalyst. Never invent a catalyst. If search is empty, say **催化劑未確認** and still report price/volume from the CSV.

Cite as a one-line `來源：Reuters` (or Bloomberg / CNBC / company PR) — **no** search-process dump, **no** footnote lists, **no** `[工具搜尋結果]` placeholders.

Classify each name **個股行情** vs **主題聯動** using the ETF 1D already computed.

**可行動洞察** = one concrete sentence (hold for continuation, fade isolated spike, watch peer confirmation) — not generic advice.

## Extra searches (orchestrator may call)

- Trump / trade: `Trump policy [DATE] tariff stocks market impact` and same-day **tariff effective / retaliation** — feed Part 4 when material (see us-market-daily-brief).
- Tape: `S&P 500 Nasdaq Dow VIX close [DATE]`
- HK spillover: only if a theme clearly hits 港股 — else omit soft speculation.
- **AH handoff:** When Mag7／mega-cap／key equipment report **after** the cash close, pass ticker list + any X Monitor seed notes up to the parent brief for `### 盤後業績` — do not silently drop them just because they are outside the AV top 3.

Return structured notes for the three stocks + optional Trump/tape/HK bullets + optional **AH seed list** for the parent brief.
