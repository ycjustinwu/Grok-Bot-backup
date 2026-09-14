# Market Awareness Orchestrator — durable memory snapshot
- Agent id: `e4e8d80f-26c5-48c1-bd11-f56c0a9cc077`
- Server id / backup slug: `2410919`
- Snapshot time (UTC): 2026-09-14
- User: Justin Wu (Asia/Hong_Kong)

## Identity
- Name: Market Awareness Orchestrator
- Title: (empty in profile.json)
- Role: Daily US market regime intelligence — Regime Scoring **v6.3**
- Primary job: When Justin pastes Stockbee / attaches TradingView US-ETF CSV / asks 市場制度日報 or regime score → run market-awareness-orchestrator pipeline → emit 繁體中文 daily
- Pipeline skills: regime-data-ingest → regime-pillar-a (/12) → regime-pillar-b (/9.5) → regime-layer-context → regime-modifiers-and-stance → regime-daily-report
- Boundary: THIS bot = regime TOTAL A+B=/21.5, pillars, stance, hysteresis. US Market Daily Brief = themes/movers/catalysts. Do not produce competing 美股市場每日簡報; hand that ask to US Market Daily Brief (id `44fb5c78-45d1-4716-b849-a5a6a0c1867b`)
- Hard rules v6.3: NO Pillar C; NO Section 5D units table; Section 0 ①② = VOO EMA from CSV not Stockbee DMA; B2-i = 7 offensive names (no MAGS in average); B3 Tier1 = 45 incl IGV+BUG; B1-iii = HYG vs LQD; 今日部署 = one qualitative sentence; never invent history; first thread run = DEGRADED MODE
- DATA GATE (Justin 2026-09-09, highest priority): data quality > finishing report. Missing/stale/abnormal critical input → STOP phase, notify 總指揮 with what failed / source / expected vs got / what Justin must fix. Never fabricate past a failed gate.
- Refs: `/workspace/refactored_market_awareness/docs/`
- Output language for daily: 繁體中文

## Historical decisions
- Thread = data memory for prev day, 3D trends, hysteresis; never invent multi-day history
- CUP Market Monitor (US) is **side-channel only** — Layer 0 flags / Focus Themes corroboration; never substitutes Stockbee into Pillar A
- Shared playbook with 港股收市簡報 for CUP skeleton (Summary/History/Sector/Industry; Up4/Down4, MLI, SMA20/50, Top Sector/Industry)
- 2026-09-08 Claude cross-check: we missed A2 zero-rejection −1 and Pair3 −1; Claude missed B3 RSP−VOO −0.5; corrected TOTAL ≈7.5; our hysteresis Bear/Avoid 2/2 and 前值 2.0 correct vs Claude Deep Bear / 前值 1.0 drift. Justin chose **lock learnings only** (no errata rewrite of published 8.5 daily)
- Locked checklist (2026-09-09) for next run: A2 post-matrix zero-rejection −1; Pair3 near-zero fail −1; never skip B3 RSP±0.5; hysteresis one-band from `latest-state.json` only; PRE-FOMC if ≤7d; Layer2 cooling list; BUG vs IGV split on short
- Skills/docs patched: regime-pillar-a, regime-pillar-b, regime-modifiers-and-stance, regime-layer-context, market-awareness-orchestrator, `docs/scoring-matrices.md`, `docs/learnings-2026-09-08-claude-crosscheck.md`, `docs/cup-market-monitor.md`
- High-stakes outputs go through Work Verifier via 總指揮 before Justin treats as final
- TC-20260909-01: Regime-only run for session 2026-09-08; US Brief held

## Live snapshot
### Regime hysteresis / last scored session
- Authoritative file: `/workspace/refactored_market_awareness/thread-memory/latest-state.json`
- Archive through 9/4: `/workspace/refactored_market_awareness/thread-memory/regime-history-through-2026-09-04.md`
- Score timeline: 8/28 0.5 Deep Bear; 8/31 1.5 Bear/Avoid 2/2; 9/1 −3.0 Deep Bear; 9/2 0.0 Deep Bear pending 1/2; 9/3 −0.5 Deep Bear upgrade failed; 9/4 2.0 Deep Bear pending 1/2; **9/8 8.5 Bear/Avoid** (Deep Bear→2/2; raw Cautious pending 1/2; no scored 9/5 — Labor Day gap)
- `prev_for_next_run` (as_of 2026-09-08): score 8.5; effective Bear/Avoid; raw Cautious; hysteresis upgrade_pending_1_of_2_to_Cautious; stance 防守; Exposure 0–10%; Market Trend CHOP 2 YES; mega_cap_divergence true; Long P4/P2; Short P7 half-size; L2 Carry Unwind + Oil USO
- Key breadth at last score: T2108 36.41; NYMO −26.57; NAMO −13.77; NYSI 17.2; NASI −118.31; VIX 15.72; VIX/VXVCLS 0.8251 (FRED date 2026-09-04 lag); SPXA50R 43.2; SPXA200R 62.2; SPXA20R 27.8
- Deliverables dir: `/workspace/regime-output/2026-09-08/` (Stockbee xlsx, breadth-1b, etf-1c, scoring-worksheet, regime-daily, regime-summary, cup-sidechannel)
- Note: published daily TOTAL left at **8.5**; learnings imply corrected ≈**7.5** if A2−1 applied — not rewritten per Justin

### CUP / Sheets (IDs only — public Drive objects Justin owns)
- US CUP Sheet: `1NMWO4-bmO8clwceamTGXZjG7rSYpljoz2jCupTk-zCQ` (title: US market breadth)
- HK CUP Sheet: `1yIZLgTIqq38i_fK-q5oBWFogk0OCH1WuZ9a6AiAP8WI` (title: HK market breadth; for 港股收市簡報)
- Integration doc: `/workspace/refactored_market_awareness/docs/cup-market-monitor.md`

### Profile memory facts (agent shard)
- Regime thread was loaded from Justin’s v6.3 memory attach (through 9/4)
- CUP US side-channel rules + Sheet ID
- Next-run locked checklist (2026-09-09)

### Log memory facts (agent shard)
- Full score timeline path notes
- CUP US Summary snapshot 2026-09-05 (later Sheet also showed 2026-09-09 Summary during 9/8 run)
- HK CUP Sheet ID for 港股收市簡報
- Regime 2026-09-08 outcome paths
- Claude cross-check learnings path

## Secrets placeholders only
- FRED_API_KEY: `[REDACTED:FRED_API_KEY]` (optional; public FRED CSV preferred per skill)
- TELEGRAM_BOT_TOKEN: `[REDACTED:TELEGRAM_BOT_TOKEN]` (optional for Stockbee Telegram send — not used in TC-20260909-01)
- Google Drive / Sheets access: via connected MCP `user-Google-drive` session — `[REDACTED:google_drive_oauth]` (no raw tokens stored in this snapshot)
- No API keys or passwords written in agent memory files

## Coverage
- Identity / job / anti-jobs / DATA GATE: yes
- Hysteresis timeline + latest-state: yes
- CUP US/HK Sheet IDs + side-channel rules: yes
- 2026-09-08 run paths + Claude learnings lock: yes
- Skill patch pointers: yes
- Secrets: placeholders only

## Pending confirms
- None blocking backup
- Open product note (not a user confirm): next Regime session should apply locked checklist; Justin did not request errata rewrite of 9/8 published 8.5 daily
