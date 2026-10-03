# Memory disaster-recovery backup — Self Improver
- **agent_id:** `1d369773-e1f5-4fdf-9a3a-2a38b1f54e16`
- **serverId:** `2410911`
- **snapshot_at:** 2026-10-03 20:09 HKT
- **path:** `/workspace/1d369773-e1f5-4fdf-9a3a-2a38b1f54e16-memory-backup.md`
- **supersedes:** `/workspace/2410911-memory-backup.md` (stale 2026-09-14 body; do not restore from it)

## Identity
- **Name:** Self Improver (named by user)
- **Title field:** empty in profile.json (role is the name itself)
- **User:** Justin Wu (Asia/Hong_Kong)
- **Harness:** temporal
- **Role:** Capture task outcomes, user corrections, and execution failures for Justin’s Grok Bot team; reflect on patterns; propose skill and instruction improvements; never overwrite Job Descriptions, skills, or guardrails without Justin’s explicit approval.
- **Anti-jobs:** Do not invent lessons; do not overwrite without approval; do not delete learnings or history without asking; do not turn one-off noise into standing rules; do not create bots or routines just to save usage.
- **Primary artifacts:**
  - `/workspace/learnings.md` — living lesson log (209 lines at snapshot)
  - `/workspace/draft_instructions.md` — proposed improvements (311 lines; mixed applied / open)
  - `/workspace/v2_prompt.md` — candidate JD snippets still open (47 lines)
  - `/workspace/prompt_history/` — archives before apply
  - Skill: self-improve (`/home/box/agent-data/workflows/self-improve/SKILL.md`)
- **Settings:** `notifyOnAgentUpdates: true`; not hidden from sidebar; drafts not disabled by this agent
- **Avatar:** shape blob, color blue (default mark; no custom picture)

## Historical decisions
1. **2026-09-07 — Empty finance-brief infographic:** 總指揮/Visual Director shipped a placeholder shell. Justin required content from 港股收市簡報. **Applied (Justin-approved):** visual-director Execute content gate only. Archive: `prompt_history/2026-09-07_2246_visual-director.md`. CoS/總指揮 JD addendum + sketchnote reinforce stayed drafts.
2. **2026-09-08 — HK swing→infographic pipeline:** HK Swing Scanner → 港股 Swing Setup → 投資敘事分析師 → Fusion Formatter → fusion-swing-infographic / baoyu. Do not skip Fusion. Doc: `/workspace/hk-swing-infographic-pipeline.md`.
3. **2026-09-08 — 港股收市簡報 18:00 miss:** Enabled cron `0 18 * * 1-5` had `lastRunAt` null; manual补跑 used TradingView CSV + 信報 360. JD still ~16:30 vs cron 18:00. Watchdog / re-arm never approved.
4. **2026-09-09 — “pullback buy”:** Google Drive spreadsheet Pullback buy (folder `1tnTfbYp13vdjEV4Bc123ehloII-iodor`, sheet `1CXYi_h8t26x_ABZmTiqQSpJc91uZWZ3ad-QQ5qnI2UU`) → US Swing Scanner → **Potential Setups STOP**. Not a Pine BUY filter. No auto-handoff to 美股 Swing Setup. Unauthorized Setup + Verifier PASS = PROCESS_HOLD. Canon: `/workspace/docs/us-daily-workflow.md` and `/workspace/us-pullback-buy-source.md`.
5. **2026-09-09 — DATA GATE (TC-20260909-11):** Missing/stale/abnormal yfinance, StockCharts, Stockbee, or other critical inputs → STOP → 總指揮→Justin; never invent numbers.
6. **2026-09-09 — US brief Claude-compare skill deltas:** Applied to us-focus-catalyst / us-rotation-structure / us-market-daily-brief. Archives: `prompt_history/2026-09-09_1012_*.md`. Do not re-propose.
7. **2026-09-14 — Weekly routine on this bot:** “Weekly self-improve reflection” moved here from 總指揮 (Sweeper / Justin) so it does not wake 總指揮’s long chat.
8. **2026-09-18 / 09-25 weekly widgets:** Apply options skipped by Justin. Treat skip as hold drafts; do not assume approve or reject.
9. **2026-09-20 — USAGE_GATE:** Canon `/workspace/fleet-policies/USAGE_GATE.md`. Reuse a fresh artifact; stop after the same approach fails twice; chat-only when no tools needed; prefer connectors/APIs; never create bots or routines to save usage.
10. **2026-09-23 — Regime 5B hysteresis:** Two consecutive days in the same raw band confirm an upgrade (multi-band jump OK). Applied in regime-modifiers-and-stance. Old one-band rule stuck Deep Bear.
11. **2026-09-23 — US brief Part 4/6:** Material policy section not tariffs-only; default 港股影響 theme map. Applied outside SI archive path.
12. **2026-09-24 — US Swing Scanner Drive uploads:** Parent `US_Stock_Data` id `1Jn7yi0sXFBqVjLvjCsIazZnOvw0_E4TY`; folder named by US session date; reuse same-name folder; native CSV only. In `us-daily-workflow.md`.
13. **2026-09-30 — HK producer locks:** Remove 100億 H-cap gate; Justin TradingView AV UP/DOWN always valid (no Yahoo price/RV/name FAIL); hide clean verification clutter; research ladder Google Sheets → Tavily → Firecrawl → Browserless → Browser Use → desktop last. Applied in `hk-after-close-brief` skill. Infographic preference for HK/finance briefs is baoyu dashboard/dense-modules.
14. **2026-10-01 — Index Drawdown Gate:** Regime Step 5, stance-only. Live.
15. **2026-10-02 — Justin approved partial apply:** (a) same-contract commodity % in `us-market-daily-brief` + `hk-after-close-brief` (name the month; settle-to-settle; no silent BZ=F mix after roll); (b) Work Verifier `features/hk-after-close-brief.md` synced to Sep 30 (no Yahoo AV FAIL, no H-cap hard check, hide clean clutter, same-contract hard, Monitor same calendar day not US D+1). Archives: `prompt_history/2026-10-02_1830_us-market-daily-brief.md`, `…_hk-after-close-brief.md`, `…_verify-wv-hk-after-close-brief.md`.

## Live snapshot
### Agent memory still in force
- Profile: USAGE_GATE; HK swing pipeline; pullback-buy stop; US DATA GATE; hybrid verification (Work Verifier id `037de516-dbc1-4565-a127-5dbb0f691729` on Swing Setup, Story, Fusion, Regime, Daily Briefs → `/workspace/work-verifier/output/`).
- Log (2026-10-02): commodity rule + WV HK map applied. Still HOLD listed under Pending confirms.
- Shared user fact written by this agent (2026-09-09): 總指揮 once mistook pullback buy for a Pine BUY filter; correct path is Drive Pullback buy Excel first.

### Routine
| Name | Schedule | Enabled | last run | Folder |
|------|----------|---------|----------|--------|
| Weekly self-improve reflection | `CRON_TZ=Asia/Hong_Kong 3 18 * * 5` (Fri ~18:03 HKT) | true | 2026-10-02 18:10 HKT succeeded | `795f3874-6232-55f4-9e98-71b9ee5b2761` |

Prompt intent: run self-improve, digest to Justin, stay quiet if nothing useful. Do not announce “routine triggered.”

### Connectors
- This agent does not own Gmail, Calendar, Drive, or X sessions. Fleet research ladder is used by brief bots, not by Self Improver day to day.
- Secrets: none stored in this agent’s memory or profile.

## Secrets
- `[REDACTED:api_keys]` — none held
- `[REDACTED:oauth_tokens]` — none held
- `[REDACTED:github_token]` — none held
- Drive folder/sheet IDs above are operational ids, not secrets.

## Pending confirms (still HOLD — do not apply on restore)
1. Theme-% anti-job: no unsourced 「均跌逾 X%」 / volume claims need RelVol (`us-market-daily-brief` + `us-focus-catalyst`). Draft only.
2. `us-rotation-structure` full table or 節錄 label. Draft only.
3. 總指揮 JD: empty market-brief visual content gate (`v2_prompt.md`). Not applied.
4. 總指揮 JD: Market Monitor date anti-job (HK same day, not US D+1). Skill side already locked 2026-09-18; JD addendum not applied.
5. sketchnote-infographic content reinforce. Low priority, not applied.
6. Ops: re-arm HK after-close 18:00 / 總指揮 18:05 if still dead; align JD ~16:30 with cron 18:00. Not approved.

## Coverage
| Area | Covered |
|------|---------|
| Identity / JD / anti-jobs / artifacts | yes |
| Historical decisions through 2026-10-02 | yes |
| Live memory, routine, settings | yes |
| Applied vs HOLD | yes |
| Secrets | placeholders only; none held |
| Full verbatim learnings.md | no — pointer only (209 lines on disk) |
