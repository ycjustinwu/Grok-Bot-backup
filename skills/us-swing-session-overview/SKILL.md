---
name: US swing session overview
description: >-
  When Justin or 總指揮 asks for a US swing session overview / market map ahead of
  (or without) stock picks: write one Traditional Chinese pre-pick market
  commentary using Hermes index/L2 climate and Room_To_Supply_R (not RR /
  Setup_Latest).
---
> **Canonical context sheets (still OK for breadth/rotation):** Market Master `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` — 美股市寬／港股市寬／ETF 輪動／形態篩選. Setup climate now prefers Hermes Drive `index.md` / L2 Speak_Up — not Setup_Latest as order truth.
# US swing session overview

ONE JOB: Produce **one Traditional Chinese pre-pick market commentary** page for the US close Justin is trading. Orientation only — what happened, why it matters, where money rotated, biggest risk, what to watch. Can run **before** ≤3 stalks (or on a day with no stalks).

Not advice. Not a buy/sell list. Not a merge of US Market Daily Brief into the body. Regime / 大盤判斷 is **reference only**, never an execution order.

## When to run

- When Justin or 總指揮 asks for overview / session map / 全圖.
- As the **session map ahead of** stock picks (overview first; stalks separate).
- Same US close date as the materials being read.
- Skip only if Justin says skip overview for that day.

Do **not** wait for `attention-3-picks.md`. Do **not** nest stalks into this page.

## Required raw materials (read / cite; missing → note in prose)

1. **Regime report** — latest Market Awareness / regime Final for the US close (translate codes into plain TC; never dump EFFECTIVE / Exposure % / Stance codes as UI).
2. **US Market Daily Brief** — Final for that close (**conflict check only** — do not paste the brief body).
3. **US Market Monitor / 美股市寬** — sheet `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`
4. **Stockbee 50 momentum** — Drive folder `1Fw2IfpQupYCrTtQTZMymt7VdjQnDWJv3`
5. **ETF / ticker RS** — native sheet `1D3BrzLH3DmxX8Gv3W9Yhvd9q_LNOGXyNyUzjnXzqmHk` (fallback overlay / Drive xlsx; say so in 資料缺口).
6. **Hermes session climate (preferred when present):** Drive `US_Stock_Data/<Mon D>/index.md` conclusions + `L2_Input.csv` Speak_Up aggregate — **one sentence** on setup climate. If naming room/space use **`Room_To_Supply_R`**, never old risk-reward ratio language. Do **not** use Setup_Latest as order/setup truth.
7. **Weekly only (if available):** 交易日誌分析 vs that week’s 大盤判斷／倉位上限. If no journal → one prose sentence under 資料缺口.

Out of scope for v1 (say N/A in 資料缺口 if asked, do not chase): event calendar, overnight futures, HK tape, X feed, stock pick shortlists.

Research order: Google Sheets/Drive MCP → Tavily → Firecrawl → Browser Use → box desktop last. Skip Browserless / Finance.

## Methods

- **Commentary first** — open with one stance line + one headline sentence.
- Explain **every number in 文字** with meaning (not bare code tables).
- **Digits, not Chinese number-words** — write `133`, `0.95`, `32%`, `−1.5`. Never `一百三十三` / `零點九五`.
- **Zero jargon** — ban or translate: EFFECTIVE, Exposure %, Stance codes, bare P3–P7, z-scores, ATR dumps, TC_deep, soft-cap as UI clutter.
- If mentioning stalks elsewhere in chat, cite Hermes §3.3 handoff fields only — **still no pick list embedded** here.
- Conflicts → plain sentences：「兩邊講法唔夾」.
- Regime = reference only; say 「只係參考，唔係落單指令」.

## Outside judges (do not replace)

1. Next 1–3 sessions: did market action face-slap that day’s 大盤姿態?
2. Weekly journal ↔ 大盤判斷／倉位上限 reconciliation when journal exists.
3. High-stakes Finals still go through **Work Verifier** when 總指揮 routes.

## Output shape (Traditional Chinese; one page, prose-first)

Save: `/workspace/second-brain/YYYY-MM-DD/us-swing-overview.md`

Also prefer HTML: `/workspace/second-brain/YYYY-MM-DD/us-swing-overview.html` — upload to Drive `1djZ778a9Gzf2ahDA8kXTPJCPUyohZxLc` when delivering.

Title date-tagged for the **US close** (e.g. `US Swing Overview — YYYY-MM-DD 收市`).

Sections in order:

1. **總覽姿態**
2. **發生咗咩**
3. **點解重要**
4. **兩邊唔夾嘅地方**
5. **錢流向邊**
6. **最大風險**
7. **之後要睇咩**
8. **資料有冇缺口** — one prose paragraph

Optional footer: `非投資建議。大盤判斷只係參考，唔係落單指令。`

**Do not include:** stock pick / stalk section, ticker shortlist, scanner handoff tickers, Setup rank tables.

## VERIFY

- Every required raw either used in prose or named under 資料缺口.
- Opening has stance + headline.
- Zero jargon; Arabic digits only.
- No pick list / no stalk-embedding.
- Climate uses `Room_To_Supply_R` (not old RR ratio language); Hermes index/L2 preferred over Setup_Latest.
- Banned tokens absent: Hermes-deleted underscore fields (risk-reward ratio*, target-N*, setup-type*, adjusted-stop*)
- Regime labeled 參考; Brief conflict-only.
- File path under `/workspace/second-brain/YYYY-MM-DD/`.

## Notion

When Justin asks to sync overview to Notion, run [US second-brain Notion sync](sand-workflow:us-second-brain-notion-sync) destination **B**: parent **US Swing Overviews** (`3fc77383-f89c-8163-b6d6-f89308b737af`).

## Anti-jobs

- Not a new bot; not a whole Second brain rewrite.
- Not regime author, US brief author, scanner, Setup writer, or stock-pick dig.
- Do not embed ≤3 stalks or any ticker shortlist into the overview.
- Do not pull event calendar / futures / HK / X for v1.
- Do not post or trade.
