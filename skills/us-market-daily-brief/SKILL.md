---
name: US Market Daily Brief
description: >-
  Use this when Justin wants the US daily market-focus brief (美股市場每日簡報) from
  US-ETF CSV + TradingView MCP abnormal-volume seeds (Justin paste overrides),
  with VIX, cash Focus, and a required after-hours large-cap earnings block for
  overnight tape — Traditional Chinese, silent analysis, start at the report
  title.
---
# US Market Daily Brief

Produce **美股市場每日簡報** for an experienced trader. Entire user-facing report in **繁體中文**. Analysis Steps 1–5 are **silent** (no screening tables, no self-check dump). Start output at `## 美股市場每日簡報`.

## Inputs

- `US-ETF_[DATE].csv` — pull latest from Google Drive folder `1k5dJy7ny5n-W_EV5Aglt0QeeXS_-5Ijn` when not attached; notify Justin if missing.
- **Abnormal volume (locked 2026-10-14):** **Primary** = [TV Abnormal Volume MCP](sand-workflow:tv-abnormal-volume-mcp) / [US Abnormal Volume](sand-workflow:us-abnormal-volume) via TradingView MCP **before** analysis. Justin paste/CSV **overrides** if he supplies one. Do **not** run disabled Python OpenClaw scripts or browser-scrape TV when MCP works.
- VIX: user paste **or** [FRED VIX Term Structure](sand-workflow:fred-vix-term-structure) / [Breadth Daily Report](sand-workflow:breadth-daily-report)
- **X Monitor (AH seed, locked 2026-10-22):** Prefer same-session / evening X Monitor soft Final (or weekday soft) for **盤後／after-hours large-cap earnings** names and first-pass reaction notes. Treat as a seed list — still verify prints vs est and AH % with IR／wires／Tavily; do **not** invent from tweets alone. If X Monitor missing, still run AH search (below).

If MCP AV fails after US close and Justin did not paste, **STOP** and notify 總指揮. Empty UP with non-empty DOWN (or vice versa) can be valid — continue. If only ETF is missing, say which and still deliver what is verifiable. **No** `[待補充]` / `[工具搜尋結果]` placeholders.

## Pipeline (complete each; mark ✅ internally)

1. [US ETF Theme Scan](sand-workflow:us-etf-theme-scan) — Tier 1 always; Tier 2 confirm; Tier 3 on trigger
2. [US Abnormal Volume](sand-workflow:us-abnormal-volume) — MCP seeds first (OpenClaw: |Δ|≥5%, RelVol>2, mcap>$5B, Value>$5M, drop OTC) + ETF linkage
3. [US Focus Catalyst](sand-workflow:us-focus-catalyst) — 3 **cash** Focus names + live web search (epicenter boost; ≥2 sourced facts each). Cash Focus stays AV-ranked; do **not** force Mag7／named AH reporters into Part 2 solely because they reported after the close.
4. Trump / **major policy** search — **include Part 4 when material** (below); omit only if nothing material
5. [US Rotation Structure](sand-workflow:us-rotation-structure) — flows with 1D+1W+YTD, RSP/SPY, SCHD/IWM, MEME, tape+VIX
6. 港股影響 — **default include** as US→HK theme map (strong/weak US sectors → HK themes/names to watch); omit only if Part 1 has no usable theme signal
7. **盤後業績（AH large-cap earnings）** — **default include** after Part 6 (Justin 2026-10-22). See section below.

Sources as one-line `來源：…`. No footnote dumps.

## Header

Prefer reader-friendly:
`**YYYY年M月D日（星期X，反映[session date]收市） | 香港時間翌日早上7:00**`

Session date = US cash close date. Alternate short form `**[DATE] 收市 | 香港時間翌日早上7:00**` is OK.

## Opening (before Part 1)

Dense paragraph: VIX path (prev→today, Δ) + **1–2 震央** (same-day tariff effective / retaliation, mega clinical fail/win, geo→oil, etc.) **before** the theme list. Do not open with only a generic “themes were mixed.”

In the **篩選／AV note** (or one line near opening): if material AH large-cap earnings exist, **point forward** to `### 盤後業績` — do **not** treat “cash Focus N for named Mag7” as permission to skip the AH block.

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

## 盤後業績 — after-hours large-cap earnings (locked 2026-10-22)

**Why:** Mag7／mega-cap／key semi-equipment prints **after the cash close** drive **tonight’s** futures／NQ／sector beta. Cash AV Focus alone is **not** enough when those names report AH.

**Default: include** a dedicated section **after Part 6**, titled `### 盤後業績`.

### Who to cover

1. **Justin-named** tickers for this run (e.g. META／TSLA／LRCX) — always cover if he named them, even if “optional Focus” wording was used for cash Part 2.
2. Else seed from **X Monitor** same-session／evening soft (AH／earnings／Mag7／semi equipment).
3. Else search: Mag7, mega-cap, and **material semi-equipment／AI-hardware** names with **session-date after-hours earnings** that can move overnight NQ／SOXX／peers.

Prefer **large caps** that matter for overnight tape. Skip micro names unless Justin asked.

### What each name needs

- Cash close ±% (from TV／tape) vs **AH reaction %** (and approx AH level when reported)
- Print vs estimate (rev／EPS／guidance) with ≥1 IR／wire source
- One line on **overnight／next-open** read-through (e.g. equipment chain sets semi beta; Mag7 buffers sentiment)
- Omit AH volume detail when not uniformly reported — say so once, do not invent

Group lightly as 主要升幅／主要跌幅 when useful. End with a short **隔夜／翌日開盤含義** paragraph. Label clearly: **盤後／after-hours（非現金 AV）**.

### Omit only when

No material large-cap／key-sector AH earnings for the session **and** Justin did not name any — then one explicit line: `盤後：無重大大型股業績` (do not silently drop the heading on earnings nights).

### Do not

- Replace cash Part 2 Focus with AH names solely because they reported AH
- Skip the block because keepers “weren’t in AV”
- Mix cash RelVol／epicenter claims into AH names without labeling

## Report skeleton

```markdown
## 美股市場每日簡報
**[header as above]**

[Opening: VIX path + 1–2 震央；篩選註可指向盤後業績]

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

### 盤後業績   ← AH large-cap earnings（隔夜／今晚走勢；常規段）
主要升幅／主要跌幅；print vs est；AH %；隔夜含義

**數據來源**：TradingView MCP AV + US-ETF [DATE]；X Monitor（若用）；…
```

## Boundary vs Market Awareness Orchestrator

- YOU = themes, movers, catalysts, rotation narrative for the cash session **plus** AH large-cap earnings for overnight tape.
- Orchestrator = regime TOTAL / pillars / stance. Do **not** emit TOTAL/21.5.

## Commodity / futures tape (locked 2026-10-02)

When quoting oil / gold / other futures:

1. Name the contract month (e.g. Brent Nov front month) when the continuous ticker has rolled.
2. % change must be **same-contract** settle-to-settle (or label as snapshot / not like-for-like).
3. Never mix `BZ=F` (or other continuous) after a roll against a prior-month settle without an explicit 更正註記.

## Anti-jobs

Do not print Step 1–5 working tables. Do not invent prices, RelVol, mcap, VIX, or catalysts. Do not dump full search transcripts or footnote lists. Do not invent HK same-day prices or fake causal spillover — map themes only. Do not omit Part 6 when Part 1 has clear strong/weak themes. Do not omit `### 盤後業績` on sessions with material large-cap／key-sector AH earnings (or when Justin named AH tickers). Do not treat “optional cash Focus” as skip-AH. Do not limit Part 4 to tariffs only. Do not use fuzzy index ranges when one verified close exists. English is not the main report. Do not replace Orchestrator’s regime daily. Do not run disabled Python OpenClaw AV scripts; use TradingView MCP (or Justin paste override). Do not report commodity % across different contract months without labeling the mix.
