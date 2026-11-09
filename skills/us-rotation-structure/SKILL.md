---
name: US Rotation Structure
description: >-
  Use this when writing the US daily brief’s rotation and market-structure
  sections — ETF flow tables with 1W/YTD, RSP/SPY, SCHD/IWM, MEME, VIX, index
  closes, and multi-session breadth path from Market Master.
---
# US Rotation Structure

Build Part 3 (板塊輪動) + Part 5 (市場結構) from the same US-ETF CSV + VIX + Market Master breadth when available.

## Presentation handoff (locked 2026-10-31)

Hand parent **tables first**: flows (ETF｜1D｜1W｜YTD｜流入/出), tape/VIX row table, breadth **~10-session path table**. RSP/SCHD/MEME/整體判斷 as **short bullets** — no wall-of-text structure essay.

## Flows (from CSV)

- **資金流入**：ETFs with 1D **> +1%**
- **資金流出**：ETFs with 1D **< −1%**

Table columns: **ETF | 今日(1D) | 週線(1W) | YTD** when CSV has `Performance %, 1 week` and `Performance %, Year to date`. If those columns are missing, 1D only and note the gap — never invent W/YTD.

Prefer clustering by Tier 1 buckets; include Tier 2 SPDRs **only** as confirmation of those themes. Only write rows with material |move| or a clear 5-day trend reverse — quiet names stay out (section contract).

## Special lenses (omit when quiet)

- **RSP vs SPY/VOO**：gap ≤ 0.5% → **omit**. RSP beats SPY > 0.5% → 廣度健康. SPY beats RSP > 0.5% → 廣度收窄 / mega-cap.
- **SCHD vs IWM**：SCHD ahead → 大型高息 / 防守. IWM ahead → 小型 / risk-on.
- **MEME**：list only if |1D| **> 2%**; no standalone analysis.

**整體判斷**：one dense **bullet** tying 震央 + flow direction (e.g. 關稅／地緣 → 商品；生技劇烈分化；硬體強軟體弱). Prefer sector ETF relative strength + RSP/SPY over HK-style “turnover share of whole market” (US adaptation).

## Tape + VIX

Need S&P 500, Nasdaq (Composite and/or NDX/QQQ), Dow, Russell／IWM closes + % (web search `S&P 500 Nasdaq Dow VIX close [DATE]` + TradingView). Prefer a **single verified point** over fuzzy ranges; if sources conflict, print both with sources (indices can diverge from press tape).

Point change must come from **stored prior close**, never a rounded headline percentage alone.

VIX today / prev:
1. User paste, else
2. [FRED VIX Term Structure](sand-workflow:fred-vix-term-structure) or [Breadth Daily Report](sand-workflow:breadth-daily-report) / StockCharts / TradingView `CBOE:VIX`

Label 上升 / 下跌 / 平穩 + one-line sentiment. Never invent VIX. If prev is missing, search the prior US session — do not guess. Failure ladder: omit VIX line if all sources fail.

**技術面**：only if the CSV/MCP has usable index/ETF structure (e.g. VOO vs EMAs, MACD histogram expanding/contracting, ADX, MA stack) or focus epics warrant 1–3 bullet technicals; otherwise omit. A bounce that fails before the **61.8%** retracement of the last decline = failed bounce, not a base — only when 60-bar data is available and computed in code.

## Breadth multi-session path (locked 2026-10-31)

**Default:** pull Market Master sheet `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` tab **美股市寬** (and 美股行業 when useful).

- Prefer a **~10-session sequence table**, not a single print: date｜UP4/DN4｜%>50D｜%>20D｜動力股佔比｜(+ SMA20 participation if present).
- Interpret **path** in 1–2 bullets: e.g. 動力股％ 7.0→5.4 during a bounce = leadership thinning / distribution risk.
- Repeated one-day breadth bursts that collapse next day (twice+) = **bear-market bounce signature**, not a base.
- Momentum names scattered across 5–6 industries (~equal weight) = **領導層碎片化** — independent reason a swing setup may be absent (feed 投資機會).
- Also note index-vs-breadth divergences (e.g. index red, equal-weight/breadth strong).

Fallback: [Breadth Daily Report](sand-workflow:breadth-daily-report) / Stockbee T2108 skills. If all fail → OMIT multi-day path; single-day Market Master/TV print OK if sourced; never invent a fake 10-day series.

## Opportunity handoff

Pass to parent brief for `### 投資機會` / `### 明日價位` as **table-ready rows**:
- Whether leadership is concentrated or fragmented
- Whether breadth path supports executable setups
- Concrete levels only when derived from tape/structure (invalidation of 震央, first re-rate after flush)

Do **not** emit Orchestrator regime TOTAL/21.5.
