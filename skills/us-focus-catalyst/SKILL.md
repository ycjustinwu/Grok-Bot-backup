---
name: US Focus Catalyst
description: >-
  Use this when picking 3 US cash-session focus stocks from AV keepers and
  searching for same-day catalysts with cited sources, transmission mechanism,
  and optional depth pulls — AH Mag7 stays in 盤後業績; hand off as bullets/tables.
---
# US Focus Catalyst

Pick **exactly 3** **cash-session** focus names from the abnormal-volume ranked list (gainers **or** losers). Prefer theme-linked, then isolated, then large-cap high RelVol — **except** epicenter boost below.

**Boundary (Justin 2026-10-22):** Part 2 Focus = **cash AV keepers**. Large-cap **after-hours** earnings that drive **tonight’s** tape (Mag7, mega-cap, key semi-equipment) go in the parent brief’s `### 盤後業績` ([US Market Daily Brief](sand-workflow:us-market-daily-brief)) — do **not** displace AV Focus solely because Justin named AH reporters or X Monitor flagged them. If Justin names tickers that are also cash keepers／epicenters, they may still land in Focus via ranking.

## Presentation handoff (locked 2026-10-31)

Return notes **ready for tables/bullets** in the parent brief — not essay paragraphs. Per ticker: price/%/RV/mcap as a mini row; catalysts as **≥2 bullets**; 傳導機制 / 板塊對照 / 可行動洞察 each **one line**. Parent will assemble Markdown tables.

## Ranking (Claude-compare 2026-09-09)

1. Theme-linked movers（板塊聯動）in today’s strong/weak ETFs
2. Isolated movers（個股行情）
3. Larger cap + higher RelVol as tie-break

**Epicenter boost (mandatory):** any keeper with **|1D| ≥ 10%** AND **RelVol ≥ 4×** must land in the top 3 even if another name is a “cleaner” theme-linked spillover. Prefer the **epicenter ticker** over a secondary spillover when both pass filters, unless Justin asks for theme-confirmation names.

Mega-cap **industry cluster** from the AV mega-sweep may set opening 震央 in the parent brief without forcing every cluster member into Focus.

## Mandatory live search

For **each** of the 3 tickers, run web search (do not skip):

- `[TICKER] [MONTH DAY YEAR] earnings news catalyst`
- For the weakest / selloff name also: `[TICKER] [MONTH DAY YEAR] downgrade selloff reason`
- Plus one sector query: `[TICKER] [MONTH DAY YEAR] sector rotation`

Date = the **session date** of the CSVs (US cash close), not Hong Kong tomorrow.

**Never infer cause from price.** Verify the trigger (filing, policy, earnings, deal, named upgrade/downgrade) before writing a reason. If unverified → `原因未核實` / `催化劑未確認`.

## Catalyst depth

Each focus stock needs:

1. **≥2 sourced factual bullets** (clinical metric, policy/effective date, index inclusion, peer move, etc.) **before** 可行動洞察
2. One **傳導機制** sentence: why this event reprices the peer group / theme (not just “stock moved”)
3. Optional **falsifier** hint for parent opening when the name is a 震央 (what level tomorrow would invalidate)

Never invent a catalyst. If search is empty, say **催化劑未確認** and still report price/volume from MCP/CSV.

Cite as a one-line `來源：Reuters` (or Bloomberg / CNBC / company PR) — **no** search-process dump, **no** footnote lists, **no** `[工具搜尋結果]` placeholders. Internally keep `[source, session-date]` for the evidence ledger.

Classify each name **個股行情** vs **主題聯動** using the ETF 1D already computed.

**可行動洞察** = one concrete sentence (hold for continuation, fade isolated spike, watch peer confirmation) — not generic advice. Do not treat “it fell a lot” as a buy — need first re-rate signal or say none.

## Depth pulls (for the 3 Focus only — locked 2026-10-31)

When MCP/CSV/sheets allow without inventing, pull for each Focus: RelVol, Value.Traded, RSI, SMA20/50/200, 52w high/low, 1M/3M/YTD when available. Compute **52w position** `(close−low)/(high−low)` when both ends exist. Use only when the number carries the argument — parent may show a small stats row, not a giant dump. Skip any field that fails the source ladder.

Official **name** from data-source description only — never copy a peer’s name onto the ticker.

## Extra searches (orchestrator may call)

- Trump / trade: `Trump policy [DATE] tariff stocks market impact` and same-day **tariff effective / retaliation** — feed Part 4 when material (see us-market-daily-brief).
- Tape: `S&P 500 Nasdaq Dow VIX close [DATE]`
- HK spillover: only if a theme clearly hits 港股 — else omit soft speculation.
- **AH handoff:** When Mag7／mega-cap／key equipment report **after** the cash close, pass ticker list + any **X Monitor** seed notes up to the parent brief for `### 盤後業績` — do not silently drop them just because they are outside the AV top 3. X Monitor = seed only; verify prints vs est.

Return structured notes for the three stocks + optional Trump/tape/HK bullets + optional **AH seed list** for the parent brief.
