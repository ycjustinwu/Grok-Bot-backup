---
name: US Market Daily Brief
description: >-
  Use this when Justin wants the US daily market-focus brief (美股市場每日簡報) from
  TradingView US-ETF + abnormal-volume CSVs, with VIX from StockCharts/FRED —
  Traditional Chinese, silent analysis, start at the report title.
---
# US Market Daily Brief

Produce **美股市場每日簡報** for an experienced trader. Entire user-facing report in **繁體中文**. Analysis Steps 1–5 are **silent** (no screening tables, no self-check dump). Start output at `## 美股市場每日簡報`.

## Inputs

- `US-ETF_[DATE].csv` — sector + thematic ETF 1D (also use 1W / YTD columns when present)
- **Abnormal volume (manual only — locked 2026-09-18):** Justin paste or `abnormal-volume-spike-US_[DATE].csv` / day-folder files he placed. **Never** run `/workspace/scripts/us_abnormal_volume_screener.py`, `tradingview_screener`, or `scanner.tradingview.com`. Script is disabled.
- VIX: user paste **or** [FRED VIX Term Structure](sand-workflow:fred-vix-term-structure) / [Breadth Daily Report](sand-workflow:breadth-daily-report)

If abnormal-volume is missing, **STOP** and notify 總指揮 — do not scrape TradingView. If only ETF is missing, say which and still deliver what is verifiable. **No** `[待補充]` / `[工具搜尋結果]` placeholders.

## Pipeline (complete each; mark ✅ internally)

1. [US ETF Theme Scan](sand-workflow:us-etf-theme-scan) — Tier 1 always; Tier 2 confirm; Tier 3 on trigger
2. [US Abnormal Volume](sand-workflow:us-abnormal-volume) — |Δ|>5%, RelVol>2, mcap>$10B + ETF linkage
3. [US Focus Catalyst](sand-workflow:us-focus-catalyst) — 3 names + live web search (epicenter boost; ≥2 sourced facts each)
4. Trump / **major policy** search — **include Part 4 when material** (below); omit only if nothing material
5. [US Rotation Structure](sand-workflow:us-rotation-structure) — flows with 1D+1W+YTD, RSP/SPY, SCHD/IWM, MEME, tape+VIX
6. 港股影響 — **default include** as US→HK theme map (strong/weak US sectors → HK themes/names to watch); omit only if Part 1 has no usable theme signal

Sources as one-line `來源：…`. No footnote dumps.

## Header

Prefer reader-friendly:
`**YYYY年M月D日（星期X，反映[session date]收市） | 香港時間翌日早上7:00**`

Session date = US cash close date. Alternate short form `**[DATE] 收市 | 香港時間翌日早上7:00**` is OK.

## Opening (before Part 1)

Dense paragraph: VIX path (prev→today, Δ) + **1–2 震央** (same-day tariff effective / retaliation, mega clinical fail/win, geo→oil, etc.) **before** the theme list. Do not open with only a generic “themes were mixed.”

## Part 4 — Trump / major policy (material gate; **not limited to tariffs**)

**Do NOT omit** when any of these hold for the session (search beyond tariffs):

- Same-day **tariff effective** / **retaliation**, or other trade measures
- Major White House / UN / campaign **policy statements** with market read-through (energy export bans or ban *intent*, Iran/geo economic isolation, Fed/Treasury-linked remarks, AI regulation or naming mandates, security/base deals, pharma/pricing, immigration/labor that moves keepers)
- Named executive action or administration examining a policy that clearly ties to day’s sectors (e.g. diesel → XLE/USO; AI rhetoric → semis/software)

Still omit pure noise (generic campaign slogans with no sector map). Prefer 3–6 dense bullets: what was said → which US themes it maps to.

## Part 6 — 港股影響（US→HK theme map; Justin 2026-09-23）

**Default: include.** After Part 5, write a short bridge:

1. Recap **which US sectors/themes were strong and weak** today (from Part 1; 2–4 lines).
2. For each strong (and material weak) theme, name **HK-relevant themes / representative tickers or sub-sectors to watch** next session (e.g. semis → 0981 SMIC／半導體設備; biotech → 1801／9926／HSTECH 生技; copper/uranium → 銅礦／中廣核礦業; finance washout → 銀行／券商防守; oil down → 油氣股份壓力).
3. Label clearly as **主題對照／留意清單**, not verified same-day HK price causation.
4. Omit Part 6 **only** if Part 1 has no usable theme signal (should be rare).

## Report skeleton

```markdown
## 美股市場每日簡報
**[header as above]**

[Opening: VIX path + 1–2 震央]

### 第一部分：市場大主題（基於 Thematic ETF）
#### 強勢主題 … / 弱勢主題 …
驅動因素 / 代表股 / 聯動程度：強|中|弱

### 第二部分：三大焦點股深度分析
焦點股 1–3：TICKER 名 ±%（個股行情|主題聯動）
價格 / 成交量·市值 / ≥2 催化劑事實 / 板塊對照 / 可行動洞察

### 第三部分：板塊輪動分析
資金流入 / 流出（1D + 1W + YTD when available）；RSP vs SPY（>0.5% 才寫）；SCHD vs IWM；MEME（>2%）；整體判斷

### 第四部分：Trump／重大政策   ← material (不限關稅)
### 第五部分：市場結構     ← 大盤點值 + VIX
### 第六部分：港股影響     ← 美股強弱板塊 → 港股主題／相關股留意（常規段落）

**數據來源**：TradingView Pro Screener [DATE]；…
```

## Boundary vs Market Awareness Orchestrator

- YOU = themes, movers, catalysts, rotation narrative for the cash session.
- Orchestrator = regime TOTAL / pillars / stance. Do **not** emit TOTAL/21.5.


## Commodity / futures tape (locked 2026-10-02)

When quoting oil / gold / other futures:

1. Name the contract month (e.g. Brent Nov front month) when the continuous ticker has rolled.
2. % change must be **same-contract** settle-to-settle (or label as snapshot / not like-for-like).
3. Never mix `BZ=F` (or other continuous) after a roll against a prior-month settle without an explicit 更正註記.

## Anti-jobs

Do not print Step 1–5 working tables. Do not invent prices, RelVol, mcap, VIX, or catalysts. Do not dump full search transcripts or footnote lists. Do not invent HK same-day prices or fake causal spillover — map themes only. Do not omit Part 6 when Part 1 has clear strong/weak themes. Do not limit Part 4 to tariffs only. Do not use fuzzy index ranges when one verified close exists. English is not the main report. Do not replace Orchestrator’s regime daily. Do not run Python TradingView abnormal-volume screener (disabled 2026-09-18); wait for Justin’s list. Do not report commodity % across different contract months without labeling the mix.
