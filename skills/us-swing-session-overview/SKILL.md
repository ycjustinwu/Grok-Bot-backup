---
name: US swing session overview
description: >-
  When Justin or 總指揮 asks for a US swing session overview / market map ahead of
  (or without) stock picks: write one Traditional Chinese pre-pick market
  commentary page for that US close — prose, zero jargon, Arabic digits (not
  Chinese number-words), no pick list.
---

> **Canonical (2026-10-22):** Market Master `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` — tabs 美股市寬／港股市寬／ETF 輪動／形態篩選／Setup_Latest. Doc: `/workspace/docs/market-master-canonical-2026-10-22.md`.
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
3. **US Market Monitor** — sheet `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`
4. **Stockbee 50 momentum** — Drive folder `1Fw2IfpQupYCrTtQTZMymt7VdjQnDWJv3` (latest 熱度圖 / analysis; do not Notion-sync that folder).
5. **ETF / ticker RS** — sheet `1QXQAHFL8bp-N4QN0D9Iwu2hVzN1n6AXY` (if Sheets API fails, use Drive xlsx / overlay and say so in 資料缺口).
6. **RS full pic** — sheet `1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ` (or overlay JSON).
7. **Market Master setups (形態篩選 / Setup_Latest)** — sheet `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` → **one sentence** on market setup climate only (e.g. 深回調／反轉氣候仍在). No ticker rewrite, no stalk nesting.
8. **Weekly only (if available):** 交易日誌分析 vs that week’s 大盤判斷／倉位上限 — followed / broken / face-slap. If no journal → one prose sentence under 資料缺口.

Out of scope for v1 (say N/A in 資料缺口 if asked, do not chase): event calendar, overnight futures, HK tape, X feed, stock pick shortlists.

Research order: Google Sheets MCP → Tavily → Firecrawl → Browser Use → box desktop last. Skip Browserless / Finance. Prefer MCP over browser.

## Methods

- **Commentary first** — open with one stance line + one headline sentence.
- Explain **every number in 文字** with meaning (not bare code tables).
- **Digits, not Chinese number-words** — write `133`, `0.95`, `32%`, `−1.5`, `過 1`, `當 0`. Never `一百三十三` / `零點九五` / `三成二` / `負一分半`. Keep ordinary words like 一週／一日／兩邊.
- **Zero jargon** — ban or translate: EFFECTIVE, Exposure %, Stance codes, bare P3/P4/P5/P6/P7 labels, z-scores, ATR, raw RS dumps, TC_deep, soft-cap, DATA GAP checklists as UI clutter. If a sleeve matters, name it in plain TC (e.g. 「生技／減息想像袖」「投機袖」「前沿科技袖」「防守輪動」).
- Conflicts → plain sentences：「兩邊講法唔夾」+ explain both sides in words.
- Regime = reference only; say 「只係參考，唔係落單指令」.

## Outside judges (do not replace)

1. Next 1–3 sessions: did market action face-slap that day’s 大盤姿態?
2. Weekly journal ↔ 大盤判斷／倉位上限 reconciliation when journal exists.
3. High-stakes Finals still go through **Work Verifier** when 總指揮 routes — this skill does not replace WV.

## Output shape (Traditional Chinese; one page, prose-first)

Save: `/workspace/second-brain/YYYY-MM-DD/us-swing-overview.md`

Also prefer HTML with embedded visuals (prose as skeleton): `/workspace/second-brain/YYYY-MM-DD/us-swing-overview.html` — upload to Drive folder `1djZ778a9Gzf2ahDA8kXTPJCPUyohZxLc` when delivering.

Title date-tagged for the **US close** reflected (e.g. `US Swing Overview — YYYY-MM-DD 收市`).

Sections in order:

1. **總覽姿態** — one stance line (plain words) + one headline sentence of what the session was. Explicit 參考／非落單.
2. **發生咗咩** — short prose: breadth, momentum, rotation in words.
3. **點解重要** — why that picture matters for swing orientation (no orders).
4. **兩邊唔夾嘅地方** — conflicts in plain sentences (or 「本 session 無明顯打架」).
5. **錢流向邊** — favored vs avoided themes in words; heat map only if it changes the map.
6. **最大風險** — biggest misread risks; brief vs regime conflict check in one breath.
7. **之後要睇咩** — watch list in prose (levels of breadth, theme alignment, whether 大盤判斷 changes).
8. **資料有冇缺口** — **one prose paragraph** (not a big checklist table). Name what was missing and what substitute was used.

Optional tiny footer: `非投資建議。大盤判斷只係參考，唔係落單指令。`

**Do not include:** stock pick / stalk section, ticker shortlist, 「如何嵌進全圖」, scanner handoff tickers, Setup rank tables.

Keep it one page. No US Brief full merge. No regime-as-order language.

## VERIFY

Before Justin treats as Final:

- Every required raw either used in prose or named under 資料缺口.
- Opening has stance + headline.
- Zero jargon / no bare code tables; numbers explained in 文字; **Arabic digits only** (no 一百／零點／三成).
- No pick list / no stalk-embedding section.
- Regime labeled 參考.
- Brief used for conflict only.
- File path written under `/workspace/second-brain/YYYY-MM-DD/`.

Self-check with work-verify / harness-bot-standard habits. If 總指揮 marks the run high-stakes, wait for Work Verifier PASS before Notion sync (if any).

## Notion

When Justin asks to sync overview to Notion, run [US second-brain Notion sync](sand-workflow:us-second-brain-notion-sync) destination **B**: create the dated page under parent **US Swing Overviews** (`3fc77383-f89c-8163-b6d6-f89308b737af`), not loose under the 庫 and not inside US Attention Picks.

Default without an ask: file on disk + Drive HTML + short status in Second brain chat.

## Anti-jobs

- Not a new bot; not a whole Second brain rewrite.
- Not regime author, US brief author, scanner, Setup writer, or stock-pick dig.
- Do not embed ≤3 stalks or any ticker shortlist into the overview.
- Do not pull event calendar / futures / HK / X for v1.
- Do not post or trade.
