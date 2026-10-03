---
name: US Rotation Structure
description: >-
  Use this when writing the US daily brief’s rotation and market-structure
  sections — SPDR inflows/outflows with 1W/YTD when available, RSP vs SPY
  breadth, SCHD vs IWM style, MEME, VIX, and index closes.
---
# US Rotation Structure

Build Part 3 (板塊輪動) + Part 5 (市場結構) from the same US-ETF CSV + VIX.

## Flows (from CSV)

- **資金流入**：ETFs with 1D **> +1%**
- **資金流出**：ETFs with 1D **< −1%**

Table columns: **ETF | 今日(1D) | 週線(1W) | YTD** when CSV has `Performance %, 1 week` and `Performance %, Year to date`. If those columns are missing, 1D only and note the gap — never invent W/YTD.

Prefer clustering by Tier 1 buckets; include Tier 2 SPDRs **only** as confirmation of those themes.

## Special lenses (omit when quiet)

- **RSP vs SPY/VOO**：gap ≤ 0.5% → **omit**. RSP beats SPY > 0.5% → 廣度健康. SPY beats RSP > 0.5% → 廣度收窄 / mega-cap.
- **SCHD vs IWM**：SCHD ahead → 大型高息 / 防守. IWM ahead → 小型 / risk-on.
- **MEME**：list only if |1D| **> 2%**; no standalone analysis.

**整體判斷**：one dense line tying 震央 + flow direction (e.g. 關稅／地緣 → 商品；生技劇烈分化；硬體強軟體弱).

## Tape + VIX

Need S&P 500, Nasdaq, Dow closes + % (web search `S&P 500 Nasdaq Dow VIX close [DATE]`). Prefer a **single verified point** (Yahoo or Reuters) over fuzzy ranges when one source is clear; only use a range if sources genuinely conflict and say so.

VIX today / prev:
1. User paste, else
2. [FRED VIX Term Structure](sand-workflow:fred-vix-term-structure) or [Breadth Daily Report](sand-workflow:breadth-daily-report) / StockCharts VIX chart

Label 上升 / 下跌 / 平穩 + one-line sentiment. Never invent VIX. If prev is missing, search the prior US session — do not guess.

**技術面**：only if the CSV has usable index/ETF structure (e.g. VOO vs EMAs) or focus epics warrant 1–3 bullet technicals; otherwise omit.
