---
name: HK Market Alerts
description: >-
  Use this when checking for Hong Kong after-close key alerts —
  geopolitics/macro and market structure (southbound/northbound flows,
  volatility, ETF/block trades) — and skip the section if nothing qualifies.
---
# HK Market Alerts

Surface high-signal geo/macro and market-structure alerts for a Hong Kong after-close brief. Skip the geopolitics/volatility/ETF subsections if nothing qualifies — but **always attempt Stock Connect flows from HKEX** when writing the daily brief (see below).

## Include only when true

### Geopolitics / macro
- China policy that moves markets (PBOC, NDRC stimulus, regulatory shifts)
- US–China tension, Hong Kong rules, Taiwan Strait developments with market impact
- Supply-chain shocks (critical minerals, semiconductors)

### Market structure
- Southbound / northbound flows: single-day > HK$20B **or** >50% above average (these still trigger a **警示** callout)
- Volatility spike (HSI volatility index >30)
- Material ETF flows or block trades

## Stock Connect / 北水（required data source）

**Authority:** HKEX Mutual Market → Stock Connect → **Historical Daily** (zh-HK), not third-party blogs or unverified press numbers.

Base: https://www.hkex.com.hk/Mutual-Market/Stock-Connect/Statistics/Historical-Daily?sc_lang=zh-HK  
Select the session date (e.g. `8-Sept-2026`, `data_tab_daily_YYYYMMDDc`). Pull both relevant daily tabs Justin cares about (southbound buy/sell / turnover and top active names as shown on the page).

For the after-close brief:
1. Fetch today’s HKEX Historical Daily figures (南向／北向 as available on the selected tabs).
2. Report **major, active, important** flows in the brief (淨額、成交、主要活躍標的) even when below the HK$20B alert threshold — put summary in 關鍵警示 or a short 北水 paragraph; escalate to full alert style only if thresholds hit.
3. Never invent or paste conflicting third-party 北水 numbers. If HKEX page fails to load, state the gap.

## Steps

1. Open HKEX Historical Daily for the session date; capture southbound (and material northbound) totals + notable actives.
2. Scan policy/volatility/ETF headlines from HKEX, wires, CN/HK press.
3. Keep geo/vol/ETF items only if thresholds hit; always include a concise HKEX-sourced 北水 note when data is available.
4. Cite `[港交所 Stock Connect Historical Daily，日期]`.

## Anti-jobs

- No filler geopolitics without a market hook.
- No fabricated flow numbers; no third-party 北水 that conflicts with HKEX.
