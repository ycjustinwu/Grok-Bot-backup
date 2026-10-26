# Memory backup — US Market Daily Brief

Snapshot time: 2026-10-03 (Asia/Hong_Kong). Agent id: 44fb5c78-45d1-4716-b849-a5a6a0c1867b. Server id: 2410917.

## Identity

- Name: US Market Daily Brief. Role: 美股市場焦點分析師. One job: 美股市場每日簡報 for the US cash session, 繁體中文, first line `## 美股市場每日簡報`.
- User: Justin Wu, timezone Asia/Hong_Kong.
- Liaison: 總指揮 (id 7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4). Tickets arrive from 總指揮. Reply against the ticket id with path + TLDR. Do not treat the brief as Final until 總指揮 routes Work Verifier (id 037de516-dbc1-4565-a127-5dbb0f691729). Do not self-call Work Verifier as the final pass.
- Boundary: this agent owns themes, movers, catalysts, and rotation narrative. Market Awareness Orchestrator owns regime TOTAL / pillars / stance. Never emit a competing TOTAL/21.5 scorecard.
- Skills: us-market-daily-brief, us-etf-theme-scan, us-abnormal-volume, us-focus-catalyst, us-rotation-structure. Docs under /workspace/refactored_us_market_daily_brief/docs/.
- Gold sample (Justin, 2026-09-22): 2026-09-05 Perplexity Finance PDF (9/4 close). Dense VIX+macro open, 強/弱主題 with 驅動/代表股/聯動程度, 3 focus with 催化劑+板塊對照, ETF inflow/outflow tables, RSP/SCHD/IWM/MEME, tape+VIX. One-line 來源 only.
- Header: `[session] 收市 | 香港時間翌日早上7:00`.
- No routines. Avatar wedge / magenta. No secrets stored in memory.

## Historical decisions

- 2026-09-09: Claude-vs-Grok skill deltas applied (震央開篇, epicenter priority, ≥2 sourced catalyst facts, ETF 1D+1W+YTD). Archives under /workspace/prompt_history/2026-09-09_1012_*.md.
- 2026-09-09 DATA GATE (highest): missing, stale, or abnormal critical input → STOP and notify 總指揮. Never invent prices, RelVol, mcap, VIX, or catalysts. Never use [待補充] or [工具搜尋結果].
- 2026-09-17: screener script and upstream cron were documented (mcap>$5B at screener, brief keepers mcap>$10B). SUPERSEDED 2026-09-18 — do not run it.
- 2026-09-18 lock TC-20260918-04: abnormal volume is Justin manual paste/CSV only. Never run /workspace/scripts/us_abnormal_volume_screener.py, tradingview_screener, or scanner.tradingview.com. Missing list → DATA GATE STOP. Do not scrape TradingView to backfill. Empty UP or DOWN is valid if Justin states it.
- Keeper filter: |Δ|>5%, RelVol>2, market cap strictly greater than $10B, plus ETF linkage. Epicenter: |1D|≥10% AND RelVol≥4× AND mcap>$10B. Soft FAIL (label, do not force epicenter) when size/RV pass but mcap fails — used for LQDA, CTVA/Vylor.
- 2026-09-22/23 Justin locks: Part 4 is any market-moving Trump/admin statement, not tariffs only. Part 6 港股影響 is always on: map US strong/weak sectors to HK themes/tickers. Do not invent HK same-day prices or causation. Profile description still says "omit unless material" — live lock wins. See pending confirms.
- 2026-09-20 USAGE GATE: reuse fresh artifacts; same approach failed twice → stop and report; prefer connector/API over browser.
- 2026-09-30 research escalation (locked): Sheets MCP → Tavily → Firecrawl CLI (env name only) → Browserless → Browser Use → box desktop last.
- 2026-10-02 onward (總指揮, repeated 2026-10-03): Justin AV tape is authoritative. Do not overwrite close, chg%, RelVol, or names against Yahoo. Still look up mcap for the gate. Still verify ETF 1D%, index closes, and VIX from real sources. Non-AV percentages in the prose must match a real source.
- Session date: CUP export dated D+1 = cash session D. Confirmed 2026-10-03: Justin label 「2026-10-03（週五收市）」 was Saturday; CSV stamp 2026-10-03 HKT + Yahoo last bar → session 2026-10-02. Do not invent a session the file does not contain.
- Verifier lessons (9/25 FAIL, applied since): no blanket "all fell over N%" without checking each name; cite RelVol only from Justin's list, the ETF CSV, or a stated Yahoo volume ratio; name the commodity contract; spreads from own settles; round YTD once from raw CSV; label inflow/outflow tables 節錄 or 全列; sources line = sources actually cited.
- Delivery: recent tickets want MD at /workspace/us-brief-inputs/<session>/US brief-<session>.md plus ASCII twin, abnormal-volume.md, _work-notes.json, and a mirror under /workspace/us-brief-output/<session>/. Some tickets say reply to 總指揮 only, not Justin.
- 2026-10-02 Justin correction: SNPS 10/01 move is the Ansys acquisition (~$35B, closed 2025-07-17; IR banner SYNOPSYS COMPLETES ACQUISITION OF ANSYS). Investor Day is secondary. Do not lead with OpenAI/Amazon.

## Live snapshot

Last completed brief: session 2026-10-02, ticket TC-20261003-01, gate PASS. Path: /workspace/us-brief-inputs/2026-10-02/US brief-2026-10-02.md (mirrored under us-brief-output). VIX 16.39→15.31. No formal epicenter. Focus STX / WDC (Toshiba HDD capacity) and HPE. DATA GAPS left as flags, seed numbers not overwritten: HPE Justin 176.95 vs Yahoo ~69.33; CTVA paste name Celanese vs Yahoo Corteva, mcap soft FAIL ~$7.95B (Vylor spin pattern from 10/01).

Prior sessions this thread (all gate PASS unless noted):

- 2026-09-23 TC-20260924-01: focus ABNB / EXPE / PAYX. Path under /workspace/us-brief-output/2026-09-23/.
- 2026-09-24 TC-20260925-01: focus FSLR / KGC / GEN. ETF CSV 124 rows not 123; RSHO missing. Path /workspace/us-brief/2026-09-24/.
- 2026-09-25 TC-20260926-01 then fix TC-20260926-03: 6084-row full ETF export filtered to 124. Focus GEN / ZS / MSFT. Verifier FAIL fixed (miners not "all >5%"; empty-UP RelVol wording; Brent Nov spread $11.91; FXY/CLOU YTD). Path /workspace/us-brief-output/2026-09-25/.
- 2026-09-28 TC-20260929-01: epicenter MDB. BA/PA is Boeing NYSE 6% Series A mandatory convertible preferred (BA-PA), not Paris. Path /workspace/us-brief-output/2026-09-28/.
- 2026-09-29 TC-20260930-01: epicenter FICO (FHFA/VantageScore). Keepers FICO/CCL/SMMT. ANDG = Andersen Group, IPO 2025-12-17, dropped on mcap. Reply was 總指揮-only.
- 2026-09-30 TC-20261001-01: epicenter UTHR. LQDA −57% soft FAIL mcap ~$2.7B. CBRS = Cerebras Systems. IBRX at $10.00B dropped (rule is >$10B). Path /workspace/us-brief-inputs/2026-09-30/ plus mirror.
- 2026-10-01 TC-20261002-01 then rewrite TC-20261002-03: epicenter ACN. CTVA −83.81% Vylor spin soft FAIL. SNPS rewritten to Ansys acquisition. False DATA GATE (worker missed the paste in the ticket) was corrected without asking Justin to re-paste. Path /workspace/us-brief-inputs/2026-10-01/.

Work Verifier on the 9/30 brief was running as TC-20261001-02 with no further action unless FAIL. No open FAIL on 10/01 or 10/02 at snapshot time.

Standing operating notes: FRED VIX often lags; Yahoo ^VIX + CNBC .VIX used when FRED stops early. Brent contract must be named (front month); do not mix Dec vs Nov settles. RSHO has been missing from the 124-name ETF list since at least 9/24.

## Secrets

- Firecrawl API key: [REDACTED:FIRECRAWL_API_KEY]. Name only. Value is not in this snapshot and must not be copied into briefs or chat.
- No other credentials, tokens, or session cookies are stored in this agent's memory.

## Pending confirms

1. AV TV-trust (do not overwrite Justin close / chg% / RelVol / name vs Yahoo) was set on TC-20261002-01 and repeated TC-20261003-01. Not yet written into profile.json or the skill. Confirm it is standing, then update the skill.
2. profile.json still says Part 4/6 "omit unless material" and "do not force Trump/HK". Justin's 2026-09-22/23 lock says Part 6 always and Part 4 for any material admin statement. Live practice follows the lock. Confirm profile text should be rewritten.
3. Canonical output folder has drifted (us-brief-output, us-brief, us-brief-inputs). Recent tickets use us-brief-inputs/<session>/ plus an output mirror. Confirm one canonical path.
4. 2026-09-17 screener-cron memory is superseded by the 2026-09-18 never-run lock. Safe to forget the "do not create the cron / script path" lines so they are not revived.
