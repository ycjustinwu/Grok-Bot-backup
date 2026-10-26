---
name: HK After-Close Brief
description: >-
  Use this when the user wants the daily Hong Kong after-close market brief
  (港股收市後簡報) — TradingView MCP AV seeds (Justin paste overrides), movers,
  catalysts, sectors, alerts/北水, short-sell fallback, and CUP Market Monitor
  breadth into one Traditional Chinese trader Markdown report (no PDF by
  default).
---

> **Canonical (2026-10-22):** Market Master `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` — tabs 美股市寬／港股市寬／ETF 輪動／形態篩選／Setup_Latest. Doc: `/workspace/docs/market-master-canonical-2026-10-22.md`.
Produce the daily **港股收市後簡報** for an experienced trader. Entire report in **繁體中文**. Run after the 16:00 HKT close (target delivery ~16:30 HKT). Data-driven, actionable, no fluff.

## Orchestration

1. **HK Unusual Movers** — first pull [TV Abnormal Volume MCP](sand-workflow:tv-abnormal-volume-mcp) for HK UP/DOWN (after close); Justin paste overrides
2. **HK Catalyst Research** → 三大頭條
3. **HK Sector Rotation**
4. **個股顯著異動**
5. **HK Market Alerts**（港交所北水 + 達標警示）
6. **HK Market Monitor**（CUP 廣度 side-channel — below）
7. Assemble Markdown; skip empty sections (keep Monitor when today’s Summary row exists)

## Delivery (locked)

**Default: Markdown only.**

- Save: `/workspace/hk-brief-inputs/YYYY-MM-DD/HK brief-YYYY-MM-DD.md`
- **Final output (required every time):** deliver the **full** Traditional Chinese brief in chat — attach the `.md` and/or paste the body. A short tape/TLDR may precede it, but **must not replace** the full brief as the Final. (Justin 2026-09-16: "Final output like this every time" referring to the full MD.)
- **Do not** run Kami, WeasyPrint, or any PDF pipeline by default
- PDF only if Justin **explicitly** asks for PDF that day
- For tickets from 總指揮: report path + TLDR to 總指揮 only; do **not** post the brief body to Justin — 總指揮 delivers Final after Work Verifier. Soft-shorten tickets that say "deliver Final in your chat" override this for that run.

## Sources

- **Prices / volumes (tape):** `yfinance` / public sources for index, 北水, VHSI, non-seed movers. Never invent.
- **Market-cap gate (REMOVED 2026-09-30):** no post-seed 100億 / H-share mcap filter. Do not PASS/FAIL Justin/MCP seeds on market cap again (MCP already applied OpenClaw >$10B HKD).
- **VHSI:** Google Finance / 高盛窩輪站 close for alerts / tape.
- **News / catalysts:** public news + HKEX when available is OK.
- **Abnormal volume (locked 2026-10-14):** **Primary** = TradingView MCP via [TV Abnormal Volume MCP](sand-workflow:tv-abnormal-volume-mcp) / [HK Unusual Movers](sand-workflow:hk-unusual-movers) **after 16:00 HKT**. Mid-session empty is expected — do not DATA-GATE during RTH. Justin paste **overrides**. Do **not** run disabled Python OpenClaw scripts. MCP failure after close with no Justin paste → STOP + notify 總指揮.
- **沽空總額（locked 2026-10-14 Justin）:** Fallback chain only — (1) HKEX dated `ashtYYMMDD.htm` → (2) HKEX `ashtmain.htm` / Daily Short Sell Turnover → (3) etnet per-stock short-sell page column **「主板總賣空金額」** (e.g. `quote_shortsell.php?code=700`; same designated-short market total). Cite which step succeeded. **If all three fail: omit the Tape 沽空 line entirely** — do not invent a number and do not print a hollow “404／未能讀取” as a substitute figure. Optional one-liner in 資料缺口 is OK. Do not sum AAStocks/etnet per-name rows into a DIY market total; GS「十大正股沽空」is ranking only.
- **Verification clutter (locked 2026-09-30):** if identity / method / gate checks find nothing wrong, **auto-hide** that verification detail; only surface gaps or real problems.
- HKEJ Industry / Spot；HKEX Stock Connect Historical Daily（北水）；day-folder CSVs only if Justin already placed them
- **RESEARCH ESCALATION (locked 2026-10-14):** Google Sheets MCP → Tavily → Firecrawl CLI → Browser Use MCP → box desktop/computerUse last. **Skip Browserless** while broken.
- **Market Master · 港股市寬／港股行業** fileId `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`  
  https://docs.google.com/spreadsheets/d/1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk/edit  
  Playbook aligned with Market Awareness Orchestrator US CUP monitor (`/workspace/refactored_market_awareness/docs/cup-market-monitor.md`).

### Market Monitor playbook（mirror US）

**Role:** Side-channel only — corroboration + flags. Does **not** invent a second regime score. Ignore Raw tab for the brief; use **Summary / History / Sector / Industry**.

**HK filters** (sheet-side): Price ≥ 1 HKD, Vol ≥ 300k — note sample size floats.

**Pull via Google Sheets MCP `read_range` (preferred) or Drive:**
1. Today’s Summary: Total Sample, Up4%, Down4%, % Above SMA20/50, MLI n, MLI %, MLI 升%
2. History: compare vs prior 1–few sessions (direction of pulse / MLI升%)
3. Top 3 Sector + Top 5 Industry by Leaders count

**Flags:**
- MLI 升% < ~40% while indices look strong → 「領導股內部不一致」
- Up4/Down4 skew vs prior days → pulse accelerating / fading
- Sector/Industry leader tilt diverges from day’s headline themes → stock-level note only

**Do not invent** ATR / 52w highs — monitor excludes them.

**Date alignment (LOCKED 2026-09-18 — Justin):**
**HK is NOT D+1.** For 港股 session **D**, use Summary/History row labeled **D** (same calendar session day). US CUP alone uses stamp D+1 → US session D (Asia/filename lag). Do not copy the US offset onto HK Monitor.
If Summary date ≠ HK session D → flag 日期錯配 and prefer History row for D; else DATA GAP for this block only.

**Output skeleton（section 五）:**
```
## 五、Market Monitor（CUP／股票層）
日期：YYYY-MM-DD｜樣本：N
脈衝：Up4 A / Down4 B（比率 X.XX｜vs 昨 …）
均線參與：SMA20 a% · SMA50 b%
領導股 MLI：n=…｜日均% …｜升% …
資金集中：Sector Top3 …｜Industry Top5 …
解讀：1–2 句（動能／領導股一致／板塊集中）— 勿當制度分數
```
Cite `[HK Market Monitor sheet，日期]`.

## Ticker rules

HKEX price/volume + 北水 authority; never invent numbers.

## Output order

```markdown
# 港股收市後簡報｜[年月日] 16:00 HKT
## 一、三大頭條故事
## 二、板塊輪動分析
## 三、個股顯著異動
## 四、關鍵警示（含北水）
## 五、Market Monitor（CUP／股票層）
```

## Commodity / futures tape (locked 2026-10-02)

When quoting oil / gold / other futures:

1. Name the contract month (e.g. 布蘭特 11 月近月) when the continuous ticker has rolled.
2. % change must be **same-contract** settle-to-settle (or label as snapshot / not like-for-like).
3. Never mix `BZ=F` (or other continuous) after a roll against a prior-month settle without an explicit 更正註記.

## Anti-jobs

- No fluff emotion paragraphs; skip quiet sectors.
- No invented catalysts or prices.
- No default PDF.
- No disabled Python OpenClaw AV scripts; use TradingView MCP (or Justin paste override).
- No post-seed 100億 H-share market-cap gate; no PASS/FAIL seed columns on mcap.
- No Yahoo/披露易 re-validation of Justin’s AV seed tape.
- Hide clean verification clutter; only print real gaps/problems.
- No commodity % across different contract months without labeling the mix.
- No hollow 沽空 “404／未能讀取” line when all short-sell sources fail — omit instead; use etnet 主板總賣空金額 before giving up.
