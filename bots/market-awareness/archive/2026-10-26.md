# Memory backup — Market Awareness Orchestrator

- Agent id: e4e8d80f-26c5-48c1-bd11-f56c0a9cc077
- Snapshot time: 2026-10-03 20:09 HKT
- Requested by: 记忆管家 (fleet memory backup, Justin)
- Sources: profile.json, settings.json, memory/profile.md, memory/log.md, memory/log/2026-09.md, memory/USAGE_GATE.md, RecallMemory, /workspace/refactored_market_awareness/thread-memory/latest-state.json (as_of 2026-10-02)

## Identity

- Name: Market Awareness Orchestrator (named by user). Title chip on profile still says "Regime Scoring v6.4.5"; description and live scoring are v6.4.6. Avatar squircle / violet. Settings: notify on agent updates = true. No custom avatar path recorded here.
- User: Justin Wu, Asia/Hong_Kong. Daily reports in 繁體中文.
- One job: US cash-session Regime Scoring only. Owns TOTAL, Pillar A, Pillar B, stance, hysteresis, Fast-Track, Change C. Does not own the US Market Daily Brief.
- Liaison: 總指揮 (7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4). High-stakes dailies go back to 總指揮 for Work Verifier (037de516-dbc1-4565-a127-5dbb0f691729) before Justin treats them as final. When a ticket says reply to 總指揮 only, send path + score TLDR there and do not paste the full daily to Justin.
- Version in force: v6.4.6 = v6.4.3 scoring spine + v6.4.5 add-ons (Fast-Track, Change C, Leading Sector, FT Day2 memory) + multi-band hysteresis confirm (locked 2026-09-23) + Index Drawdown Gate (locked 2026-10-01) + ETF RS overlay with 趨勢觀察 (overlay 2026-09-24; trend watch locked 2026-10-02).
- Caps: A/12 + B/9.5 = TOTAL/21.5, range [−10.5, 21.5]. No Pillar C. Pillar A floor is −4 (A1 can reach −2; A2 and A3 each clipped at −1). Print e.g. "A −3 (floor −4)".
- Primary skills (under /home/box/agent-data/workflows/): market-awareness-orchestrator, regime-data-ingest, regime-pillar-a, regime-pillar-b, regime-layer-context, regime-modifiers-and-stance, regime-daily-report, etf-rs-overlay-ingest, etf-rs-theme-tilt. Workspace mirrors under /workspace/refactored_market_awareness/skills/ are older (v6.3-era); append locked notes only, do not full re-sync.
- Deliverable: /workspace/market-awareness/YYYY-MM-DD/regime-daily-YYYY-MM-DD.md. Mirror: /workspace/regime-output/YYYY-MM-DD/ (daily, regime-summary.json, scoring-worksheet, stockbee-1a, breadth-1b, etf-1c, us-market-monitor, etf-rs-overlay). State: /workspace/refactored_market_awareness/thread-memory/latest-state.json.
- Research order (shared 2026-09-30): Google Sheets → Tavily → Firecrawl → Browserless → Browser Use → box desktop last. MCP before browser.
- No routines owned by this agent.

## Historical decisions

Locked rules (do not reopen without Justin):

- 2026-09-09 checklist: A2 post-matrix zero-rejection −1; Pair3 near-zero fail −1; never skip B3 RSP ±0.5; PRE-FOMC if ≤7 days; Layer2 cooling list; BUG vs IGV split on the short side. Hysteresis priors come from latest-state.json / the archive, not a later re-score.
- 2026-09-08 Claude cross-check: missed A2 −1 and Pair3 −1; corrected 9/08 TOTAL about 7.5 was noted; hysteresis Bear/Avoid 2/2 and prior 2.0 were kept vs Claude drift. Learnings: /workspace/refactored_market_awareness/docs/learnings-2026-09-08-claude-crosscheck.
- v6.4.3 vs v6.3 (2026-09-15): A1-ii parity-first (|5D−10D|<0.2 → 0 stop); McClellan priority CROSS → AGREEMENT → DIVERGENCE → FLAT (cross ≥0); 0A④ = NYMO≥0 AND NAMO≥0; A2/A3 clips [−1,4]/[−1,2]; A3 zero-cross = NYSI only; B3% = positive÷found (found=0 → 0 + DATA GAP); Late Stage uses % vs 50%; P5 = XLU/XLP/XLV only (SCHD in P1); Pair7 improving ∈ {PR, NR, CU}; stance uses EFFECTIVE band; exposure ratchet +20pp upper cap, lower = new regime floor.
- v6.4.5 (2026-09-22/23): scoring spine unchanged. Fast-Track only if 4% ratio ≥3 AND VIX single-day drop >10% AND leading-sector volume. Leading Sector = Layer1 #1 by 1W excess (P5 #1 → N/A auto-fail). Change C only when T2108<20 V-REVERSAL: relax McClellan leg ② if B2-i ≥+2% and LS volume. FT Day1 exposure cap 30%; Day2 unknown → keep 30%.
- v6.4.6 hysteresis (2026-09-23): pending target = today's raw band. Two consecutive sessions in the same raw band, strictly above prior effective, confirm on day 2 (multi-band jumps allowed). Day 1 = pending 1/2. If day 2 raw leaves the target, pending fails and restarts. Downgrades are immediate. Hysteresis uses the archived prior score, not a later Stockbee re-score. Cautious exposure 30–50%. Bear/Avoid exposure 0–10%. One-band-only upgrade is superseded.
- CUP forever lock (2026-09-18 date rule; 2026-09-19 self-pull): every run pulls Google Drive sheet 1NMWO4-bmO8clwceamTGXZjG7rSYpljoz2jCupTk-zCQ. US stamp S = cash session S−1. Non-scoring 附加觀察 only. Drive fail = one-line DATA GAP, does not block TOTAL. Never invent CUP from Stockbee. HK Market Monitor is not this bot's job. Docs: docs/cup-market-monitor.md.
- DATA GATE: never invent values. Missing or stale critical input → STOP and report source + expected vs actual. Justin TradingView AV UP/DOWN inputs are always valid (shared 2026-09-30); do not overwrite breadth he supplied. VIX/VXVCLS: his snapshot wins for Pair7; if he marks N/A or lagged FRED, carry a stale label (Pair7 only, not a stop). ETF CSV must be that session; missing fresh CSV stops Pillar B.
- Stockbee prior-day revision (Work Verifier, two runs missed it; patched TC-20260929-05): if the xlsx revises a prior-day row vs that run's stockbee-1a.json, re-score that prior day's Pillar A and print 前值 X (存檔) → 修訂 Y. Put prior_revised / delta_revised in regime-summary.json. Do not reissue the prior daily. Literal line MARKET=US near the top of every daily. A floor −4 printed.
- Index Drawdown Gate (Justin 2026-10-01), Step 5, before V-REVERSAL, stance-only, no change to TOTAL / band / hysteresis. SPX dd = (252-session high close − today close) / 252-session high from Stockbee. If history <252 sessions, use the longest window and label ⚠️ 窗口不足 (recent files ~195–198 rows). ≥8% PASS: evaluate V-REVERSAL / DEAD CAT / UNCERTAIN as before. <5% FAIL: forbid V-REVERSAL; at most UNCERTAIN, or DEAD CAT only if DEAD CAT's own three conditions fire. Flag ⚠️ 參與度收縮但指數未跌. 5%≤dd<8% NEUTRAL: V-REVERSAL may be evaluated; if it fires, 首注輕試 + Exposure cap 10%. Gate is N/A when T2108≥20 (informational dd may still print). Justin said do not re-run the 9/29 daily after this lock. Backups: /workspace/regime-output/_skill-backups-index-drawdown-gate-2026-10-01/.
- ETF RS overlay (non-scoring): after CUP, before Modifier Notes. Heading ### 附加觀察｜ETF RS 主題傾斜（非計分）. Favor 2–3 and Avoid 2–3; if fewer than 2 themes qualify, say 不足 2 個主題達標. Sheet 1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ; local /workspace/etf-rs/ETF_Relative_Strength_Dashboard.xlsx refreshed each run. Include only if sheet US trade date = session date; else DATA GAP. Never feeds TOTAL / band / hysteresis / FT / Exposure. Never invent PERCENTRANK.
- ETF RS 趨勢觀察 (Justin 2026-10-02): after Favor/Avoid. He wrote 5d and 2d. Dashboard has literal columns `2-day trend` and `5-day trend`. There is no Rising/Declining 20-day trend, so the pair is 5d+2d, not 5d+20d. 雙升 = both Rising (strengthening watch, not necessarily strongest RS; cite only names that are actually both Rising). 雙降且仍領先 = both Declining AND (RS≥70 or Favor or theme-top) → 領導版塊有機會轉弱. 10/1 daily was amended narrative-only (scores unchanged). Backups: /workspace/regime-output/_skill-backups-etf-rs-trend-watch-2026-10-02/.
- Usage gate (Justin 2026-09-20, all bots): reuse a fresh artifact; same approach fails twice → stop and report; no tools → chat only; prefer connector/API; do not create bots or routines to save usage. Canon: /workspace/fleet-policies/USAGE_GATE.md.
- T2108 <20 → display Reversal Watch and Step 5 (V-REVERSAL 3 legs / DEAD CAT / UNCERTAIN). Exposure on upgrade confirm: lower limit = new regime floor (floor wins if higher).
- Infographic preference (shared, not this bot's primary output): baoyu-infographic for finance briefs; Kami for PDF/print. This bot's deliverable is markdown.

Score trail (archive, not all re-scored):

- Through 2026-09-04 (v6.3): 8/28 0.5 Deep Bear; 8/31 1.5 Bear/Avoid confirmed; 9/1 −3.0 Deep Bear; 9/2 0.0 pending 1/2; 9/3 −0.5 upgrade failed; 9/4 2.0 pending 1/2. Archive: regime-history-through-2026-09-04.md.
- 2026-09-08: first print 8.5 (A2/B6.5), effective Bear/Avoid, raw Cautious pending 1/2. Cross-check later put a corrected figure near 7.5; hysteresis was not rewritten to Claude's Deep Bear.
- 2026-09-16: TOTAL −7.5, effective Deep Bear. CUP 附加觀察 after 重要旗號, not in TOTAL.
- 2026-09-21 and 2026-09-22: TOTAL 5.0 raw Cautious, effective still Deep Bear, Bear/Avoid pending restart 1/2, Exposure 0%, FT off. 2026-09-22 redo under v6.4.6: TOTAL 5.0, effective Cautious, stance 防守性機會, Exposure 30% (floor wins). That redo is the hysteresis lock example, not a replacement of the 9/22 file's original pending state unless the daily was rewritten; next runs used latest-state.
- 2026-09-23: TOTAL 1.5 (A−2/B3.5), raw=eff Bear/Avoid, immediate downgrade from Cautious, stance 防守, Exposure 0%.
- 2026-09-24: TOTAL 0.5 (A−3/B3.5), Bear/Avoid HOLD, T2108 19.95 Reversal Watch UNCERTAIN. First ETF RS overlay: Favor P4 only, Avoid P5/Nuclear/Gold.
- 2026-09-25 (TC-20260926-06): TOTAL 4.5 (A−0.5/B5.0), Bear/Avoid HOLD, T2108 19.89 Reversal Watch. Later Stockbee revision T2108 19.89→20.26 re-scored that day to 3.5 (A2 +1→0); hysteresis kept archived 4.5. Delta into 9/28 is −7.0 vs revised prior.
- 2026-09-28 (TC-20260929-03, amended TC-20260929-05): TOTAL −3.5 (A−3 floor −4 / B−0.5), immediate downgrade to Deep Bear. T2108 17.58. RS later filled: Favor L2 Japan only. MARKET=US line added.
- 2026-09-29 (TC-20260930-03): TOTAL −2.5 (A−1.5/B−1.0), Deep Bear HOLD. VIX/VXVCLS 0.881 from Justin (ends the 9/22 FRED lag). Do not re-score this day for the Index DD Gate.
- 2026-09-30 (TC-20261001-03): TOTAL −5.0 (A−4 floor / B−1.0), Deep Bear HOLD. First live Index DD Gate = FAIL, dd 1.88%, window 196, high 7798.99 on 2026-08-13. V-REVERSAL forbidden. Pair7 used FRED 9/29 stale 0.887 because Justin marked VIX/VXV N/A.
- 2026-10-01 (TC-20261002-05): TOTAL +2.0 (A−0.5/B+2.5), raw Bear/Avoid, effective Deep Bear, pending Bear/Avoid 1/2. Index DD FAIL dd 1.68%, window 197. Narrative amend for 趨勢觀察: 雙升 FOTO; SOXX both No Trend so not listed; 雙降且領先 IDNA/ARKG/GNOM and ARKK.

## Live snapshot

As of session 2026-10-02 (ticket TC-20261003-03, breadth stamp 2026-10-03 06:40 HKT). Source latest-state.json. Next run starts from this, not from the 10/01 pending state.

- TOTAL +0.5 / 21.5 (A −1.0 = A1 0, A2 0, A3 −1; B +1.5 = B1 −0.5, B2 +2, B3 0). Delta −1.5 vs revised prior +2.0 (10/01 revised score still +2.0; archived prior also +2.0).
- Raw = effective = display Bear/Avoid. Hysteresis CONFIRM day 2 (Deep Bear → Bear/Avoid). Pending cleared. Nothing pending into the next session.
- Stance DEFENSIVE / 防守空倉. Exposure ceiling 0% (band 0–10%). Deployment Sideways, checklist CHOP.
- T2108 20.53 Recovery. Reversal Watch off. Index Drawdown Gate N/A. Informational dd 0.96% (SPX 7724.38 vs window high 7798.99 on 2026-08-13, window 198 <252, ⚠️ 窗口不足).
- Breadth Justin supplied (do not overwrite): VIX 15.31 WEAK (prev 16.39); VIX/VXVCLS 0.882 CALM labelled 1-day stale (10/1; FRED 16.39/18.58 = 0.882 corroborates); SPXA50R 25.00 OVERSOLD; SPXA200R 45.40 NEUTRAL; SPXA20R 26.60 OVERSOLD; NYSI −767.23 WEAK; NYMO −14.55 NEUTRAL neg; NAMO −11.80 NEUTRAL neg; NASI −624.11 WEAK.
- McClellan state NR, tier AGREEMENT (both neg and rising). Fast-Track off. Change C not eligible. FOMC off-cycle, next Oct 27–28, about 25 days out on that run.
- Stockbee session row: Up4 220 / Down4 131, 5D and 10D ratio both 0.87, Q25 872/1317. Prior-day revision: 10/1 became 181/201, T2108 18.99; re-score still +2.0. Do not reissue the 10/1 daily.
- B3: 15 positive / 45 found = 33.33%.
- Layer1 long P2 Hardware/Infra and P7 Software/Cyber. Layer1 short P4 Speculation. Leading sector P2, volume confirm false (avg 1D 1.51, avg RelVol 1.07). Layer2 active: Oil Check (USO+/XLE−). Cooling empty.
- CUP stamp 2026-10-03 (session 10/02): sample 2423, Up4 163 / Down4 65, MLI升% 57.24. Non-scoring.
- ETF RS sheet trade date 2026-10-02. Favor P7 / P2 / L2 Japan. Avoid L2 Nuclear / Defense / Gold. 趨勢觀察: 雙升 FOTO/GRID/AIQ/NASA/EWY; 雙降且仍領先 GNOM/IDNA; SOXX was No Trend on both, not 雙升.
- Report: /workspace/market-awareness/2026-10-02/regime-daily-2026-10-02.md. Mirror /workspace/regime-output/2026-10-02/.
- Next session: effective Bear/Avoid confirmed. A downgrade to Deep Bear would be immediate. An upgrade needs two consecutive raw days in a band strictly above Bear/Avoid (Cautious starts at TOTAL ≥ 5). Index DD Gate and Reversal Watch return only if T2108 falls back under 20.

## Secrets

None held by this agent. No API tokens, passwords, or mailbox credentials are stored in profile or memory.

- [REDACTED:none]

Sheet ids above are operational Drive ids already in skills and dailies, not credentials.

## Coverage

- Included: identity, locked scoring rules through 2026-10-03, score trail from 2026-08-28 through 2026-10-02, live state for 2026-10-02, paths, CUP and ETF RS sheet ids, usage gate.
- Not a byte-for-byte dump of every daily markdown or of conversation-blobs.db.
- Early September log lines in memory/log/2026-09.md are summarized in the score trail; the file itself remains the fuller dated log.
- Profile title chip "v6.4.5" lags the description and latest-state version "v6.4.6". Not changed in this backup.

## Pending confirms

- Work Verifier soft note 3 (upgrade-condition wording 「raw 連續兩日同處 ≥0 band」 is loose vs the locked rule "same raw band strictly above prior effective") was left for 總指揮 and has not been answered. Skills were not reworded.
- No open question from Justin. Do not re-run 2026-09-29 for the Index Drawdown Gate.
