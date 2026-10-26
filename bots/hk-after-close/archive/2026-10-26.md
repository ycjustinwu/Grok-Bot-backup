# Memory backup — 港股收市簡報
Agent id: b9d6b823-8ae3-46a7-bc08-9beb4a35c631
Snapshot: 2026-10-03 HKT
Owner: Justin Wu (Asia/Hong_Kong)
Source: agent profile + agent memory (RecallMemory) + standing skills. Not a full chat transcript dump.

## Identity
- Name: 港股收市簡報
- Role: 港股收市後每日簡報（繁體中文），服務經驗交易員 Justin Wu
- Title chip: (empty)
- Avatar: pebble / orange; namedBy user
- Settings: notifyOnAgentUpdates true; not hidden
- Skills used: hk-after-close-brief, hk-unusual-movers, hk-catalyst-research, hk-sector-rotation, hk-market-alerts
- Teammate routing: tickets arrive from 總指揮 (7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4). Work Verifier (037de516-dbc1-4565-a127-5dbb0f691729) is routed by 總指揮 — this agent does not message Work Verifier directly.
- Routine: 「港股收市後簡報」 folder 2bb7f9ad-34a2-5346-ac9b-5f5ac64b4eee — **paused**. Cron was weekdays 18:00 HKT. Last recorded run 2026-09-09 18:25 succeeded. Live work is ticket-driven from 總指揮, not the paused routine.

## Historical decisions
Chronological. Later locks supersede earlier ones where they conflict.

### Delivery and format
- Entire brief in 繁體中文. Close 16:00 HKT; target ~16:30.
- Filename: `HK brief-YYYY-MM-DD.md` under `/workspace/hk-brief-inputs/YYYY-MM-DD/`. Also write identical copies to `/workspace/hk-brief/YYYY-MM-DD/` and ASCII twin `HK_brief-YYYY-MM-DD.md` in the inputs folder; confirm md5 match. (2026-09-08 filename lock; later practice added the twin paths.)
- Final deliverable is the **complete** MD, not a TLDR alone (Justin 2026-09-16).
- Default **no PDF** / no Kami / no WeasyPrint. PDF only if Justin explicitly asks that day (token lock 2026-09-09). Kami skill exists if PDF is asked.
- For ticketed runs from 2026-09-28: report path + TLDR to **總指揮 only**. Do not post the brief body to Justin. 總指揮 delivers Final after Work Verifier. Fixes return under the same task id.
- Section order used in recent briefs: 大市膠帶; 一、三大頭條 (發生什麼事／哪些股票異動／可行動洞察); 二、板塊輪動 (only material); 三、個股顯著異動 (A seeds / B mega-caps |Δ|>~3% / C by sector); 四、關鍵警示含北水; 五、Market Monitor; 資料缺口 (only real problems); 明日觀察.
- Cite figures `[來源，日期]`. Never invent numbers. Non-seed price/volume and 北水: HKEX wins on conflict.

### Abnormal volume
- 2026-09-18 lock: seeds come **only** from Justin (chat paste, CSV, or day-folder file, often relayed by 總指揮). **Never** run `/workspace/tools/hk-abnormal-volume/hk_abnormal_volume_screener.py`, `tradingview_screener`, or any TradingView scanner API. If no list → STOP and notify 總指揮.
- SUPERSEDED 2026-09-17 note that the Python screener may run (max 1 UP + 1 DOWN, no 429 retry). That path is disabled.
- SUPERSEDED 2026-09-07 note to treat TV paste as a screen and still verify price/volume on HKEX/AAStocks/Yahoo. From 2026-09-30 the paste is authoritative (see Live snapshot).

### Market-cap gate (superseded)
- 2026-09-28: 100億 gate used **H-share** cap only (H shares × HK close), not whole-company. Example 2889 ~59.7億 H = FAIL. Saved into skills then.
- **REMOVED 2026-09-30**, effective the **next** brief after 9/30 Final (first applied on 2026-10-02). Do not FAIL/filter seeds on mcap. Do not show PASS/FAIL gate columns. Optional mcap for context only. Do **not** reissue 9/28 or 9/30 briefs for this.

### Verification clutter
- 2026-09-30: if checks find nothing wrong, auto-hide verification detail (identity checks, RV cross-tables, method dumps). Only surface real gaps/problems.

### Sources (non-seed tape)
- Prices/volumes/indices for non-seed tape: yfinance. HSTECH often has a single Yahoo point — compute change vs prior brief close and cross-check 財聯社/智通.
- VHSI: Google Finance, cross-check 高盛窩輪. Alert if >30.
- Sectors, turnover, advance ratio: HKEJ Stock360 Industry https://stock360.hkej.com/marketWatch/Industry . Spot page is lower priority (many small-caps). 2026-09-09 Industry/stock page was blank.
- 北水: HKEX Mutual Market Historical Daily zh-HK / CSM JS `data_tab_daily_YYYYMMDDe.js` (eng c.js may 404). Net = buy − sell. Alert if |net| > 200億. HKEX beats third parties (e.g. 鳳凰). Do not redo the 2026-09-08 brief after the HKEX sourcing switch.
- Commodities: name the contract (e.g. 布蘭特 11 月 BZX26). Compare only within the same contract month. Yahoo BZ=F rolls months (caused a 9/25 error, corrected 9/26 as TC-20260926-04: Brent Nov settle ~104.32, about −2.1%, not −7.2%).
- Market Monitor Google Sheet fileId `1yIZLgTIqq38i_fK-q5oBWFogk0OCH1WuZ9a6AiAP8WI` https://docs.google.com/spreadsheets/d/1yIZLgTIqq38i_fK-q5oBWFogk0OCH1WuZ9a6AiAP8WI/edit
  - HK is **NOT D+1** (locked 2026-09-18). Use Summary/History row labeled the same session date. US CUP offset must not be copied.
  - Sections: Summary/History/Sector/Industry only. Up4/Down4, % above SMA20/50, MLI n / daily % / 升%. Top3 Sector + Top5 Industry. Side-channel only, not a second score. Flag MLI 升% < ~40% when indices look strong. Sheet filters Price≥1 HKD, Vol≥300k. Do not invent ATR/52w highs. Do not redo 2026-09-08 brief just to add this section.
- Research escalation locked 2026-09-30: Google Sheets MCP → Tavily search/extract → Firecrawl CLI (FIRECRAWL_API_KEY) → Browserless MCP → Browser Use MCP → box desktop/computerUse last.
- News/catalysts: HKEX announcements first, then public news. No special paid feed required.
- Priority data Justin *could* still supply (2026-09-17 wish-list, partly stale because mcap gate is gone): authoritative daily price/volume feed; verified VHSI; optional broker southbound for cross-check only; curated same-day HKEX announcements. The old “ticker+mcap table for the 100億 gate” item is obsolete.

### Sessions completed (this agent)
| Session | Ticket | Notes |
|---|---|---|
| 2026-09-08 | — | TV CSVs staged; brief stands; do not redo for 北水 source change or Monitor add |
| 2026-09-09 | — | Stock Connect saved; northbound splits unavailable; Monitor sheet only through 09-08; Spot 25 names |
| 2026-09-21 | — | Innovative-drug cluster; southbound about +40.7億 |
| 2026-09-22 | TC-20260922-07 | 0700 = 騰訊 (seed name error caught then); southbound +126.9億 |
| 2026-09-23 | TC-20260923-11 | HSI 24,834; southbound +34.5億 |
| 2026-09-24 | TC-20260924-06 | 6623 陸控 −40.83%; southbound +29.0億 |
| 2026-09-25 | TC-20260925-10 | HSI 24,510 (−1.01%); Stock Connect suspended so southbound 0; VHSI 18.32; 0659 周大福創建 ~383.5億 |
| 2026-09-26 | TC-20260926-04 | Correction to 9/25 oil contract mismatch; Stock Connect reopen 9/28 then close 10/1–10/7 |
| 2026-09-28 | TC-20260928-01 | HSI 24,642.51 (+0.54%); southbound −65.54億; md5 a681e3a7…; 2889 mcap question raised then |
| 2026-09-28 | TC-20260928-03 | H-share gate written into skills (later removed 9/30) |
| 2026-09-29 | TC-20260929-07 | HSI 24,523.57 (−0.48%); southbound +0.15億; md5 cc6595e8…; then-gate FAIL 2202/2889 (historical; gate since removed) |
| 2026-09-30 | TC-20260930-06 | Last session under old gate. HSI 24,613.27 (+0.37%); southbound +68.63億; VHSI 16.99; last Stock Connect day before National Day; md5 05d9e24a…; Work Verifier as TC-20260930-07 |
| 2026-10-02 | TC-20261002-08 | First session under new locks. UP=0; DOWN 0005/02888/09698. HSI 23,972.29 (−2.60%); VHSI 19.34; 北水 holiday = 0 until 10/8; md5 4557a89e… |

## Live snapshot
Effective rules for the **next** brief:
1. No 100億 / H-share market-cap gate. No PASS/FAIL seed column.
2. Justin TradingView AV UP/DOWN paste is authoritative. Do not overwrite close, chg%, RV, or names from Yahoo or 披露易.
3. Hide verification clutter when nothing is wrong. Surface only real DATA GAPs.
4. Manual AV only. Missing list → STOP, tell 總指揮.
5. Markdown only. Primary path `/workspace/hk-brief-inputs/YYYY-MM-DD/HK brief-YYYY-MM-DD.md` plus twins. Report path + TLDR + epicenter/focus + DATA GAPs to 總指揮 only.
6. MCP-first research order as above.
7. Market Monitor: same calendar session date, not D+1.
8. 北水 from HKEX; |net| > 200億 alert; VHSI > 30 alert. Stock Connect closed 10/1–10/7; next southbound session **2026-10-08** (as of 10/02 brief).
9. Commodities: named contract, same-month comparisons only.
10. Output language: 繁體中文. No fluff, no full quiet-sector dump, no invented catalysts.

Open operational state:
- No unfinished ticket. Waiting for the next TC from 總指揮 plus Justin’s manual AV list.
- Paused weekday routine should stay paused unless Justin/總指揮 says to resume.
- 2889 market-cap question is **closed** (gate removed); do not re-ask.

## Secrets
No API keys, tokens, or passwords are stored in this agent's memory or profile.
- Firecrawl, if used, reads env `FIRECRAWL_API_KEY` — value **[REDACTED:FIRECRAWL_API_KEY]** (not held here).
- Google Sheets / Tavily / Drive access is via connected MCP accounts, not copied secrets.

## Coverage
- Included: identity, profile description, settings flag, all recalled agent-memory facts that still matter, superseded rules marked, session/ticket log from this conversation's working record, live locks, routine state, secret posture.
- Not included: full brief bodies (on disk under `/workspace/hk-brief*` and `/workspace/hk-brief-inputs*`), raw day-folder extracts, chat transcripts, other agents' memories.
- Shared user-memory facts learned by other assistants are not copied here except where this agent also stored the same rule.

## Pending confirms
- None. Justin’s 2026-09-30 locks are saved and already applied on 2026-10-02. No open question waiting on Justin.
