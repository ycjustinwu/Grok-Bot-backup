# Memory disaster-recovery backup — Self Improver
- **agent_id:** `1d369773-e1f5-4fdf-9a3a-2a38b1f54e16`
- **serverId:** `2410911`
- **snapshot_at:** 2026-09-14 20:32 HKT
- **path:** `/workspace/2410911-memory-backup.md`

## Identity
- **Name:** Self Improver
- **Title:** Self Improver
- **User:** Justin Wu (Asia/Hong_Kong)
- **Role:** Capture task outcomes, user corrections, and execution failures for Justin’s Grok Bot team; reflect on patterns; propose skill/instruction improvements for human approval only.
- **Anti-jobs:** Do not invent lessons; do not overwrite Job Descriptions/skills/guardrails without explicit approval; do not delete learnings/history without asking; do not turn one-off noise into standing rules.
- **Primary artifacts:**
  - `/workspace/learnings.md` — living lesson log
  - `/workspace/draft_instructions.md` — proposed improvements awaiting review
  - `/workspace/v2_prompt.md` — candidate JD/prompt updates
  - `/workspace/prompt_history/` — archived prior versions before apply
  - Skill: [self-improve](sand-workflow:self-improve)
- **Settings:** `notifyOnAgentUpdates: true`
- **Avatar:** shape blob, color blue (default mark)

## Historical decisions
1. **2026-09-07 — Empty finance-brief infographic:** 總指揮/Visual Director generated placeholder-only HK brief visual; Justin required content from 港股收市簡報. Justin approved applying **only** the visual-director Execute content gate; archived to `prompt_history/2026-09-07_2246_visual-director.md`. CoS JD addendum + sketchnote reinforce remain drafts (not applied).
2. **2026-09-08 — Canonical HK swing→infographic pipeline:** HK Swing Scanner → 港股 Swing Setup → 投資敘事分析師 (Story Search) → Fusion Formatter → fusion-swing-infographic / baoyu-infographic. Do not skip Fusion; no empty visuals. Doc: `/workspace/hk-swing-infographic-pipeline.md`.
3. **2026-09-08 — 港股收市簡報 18:00 miss:** Routine `0 18 * * 1-5` enabled but `lastRunAt` null; manual补跑 used TradingView CSV + 信報 360. JD still said ~16:30 vs cron 18:00. Watchdog/JD-align widgets skipped by Justin (log only).
4. **2026-09-09 — “pullback buy” glossary:** Means Google Drive spreadsheet **Pullback buy** extract → US Swing Scanner → **Potential Setups STOP** — not Pine BUY filter. Folder id `1tnTfbYp13vdjEV4Bc123ehloII-iodor`; sheet id `1CXYi_h8t26x_ABZmTiqQSpJc91uZWZ3ad-QQ5qnI2UU`. Doc: `/workspace/us-pullback-buy-source.md` + `/workspace/docs/us-daily-workflow.md`.
5. **2026-09-09 — TC-20260909-10 fold:** No auto-handoff scanner→美股 Swing Setup; Verifier PASS on unauthorized Setup = PROCESS_HOLD/archival. Fixes applied by 總指揮 (skill + docs + US Scanner JD); Self Improver did not re-overwrite.
6. **2026-09-09 — DATA GATE (TC-20260909-11):** Missing/stale/abnormal yfinance / StockCharts / Stockbee (or other critical inputs) → STOP → 總指揮→Justin; never invent numbers.
7. **2026-09-09 — US brief Claude-compare skill deltas:** Applied (via fleet) to us-focus-catalyst / us-rotation-structure / us-market-daily-brief; archives under `prompt_history/2026-09-09_1012_*.md`.
8. **2026-09-14 — Weekly routine moved onto Self Improver:** Friday `0 18 * * 5` “Weekly self-improve reflection” enabled here so it no longer wakes 總指揮’s long chat (per Sweeper / Justin). Old copy on 總指揮 to be paused by Sweeper.

## Live snapshot
### Agent memory (profile)
- Canonical HK swing→infographic pipeline (see Historical #2).
- pullback buy → Drive Excel → US Swing Scanner → Potential Setups STOP (see #4).
- US swing path: Drive + Pine both Potential Setups only; Setup only on Justin’s explicit pick; unauthorized Verifier PASS = PROCESS_HOLD. Canonical: `/workspace/docs/us-daily-workflow.md`.
- US stack DATA GATE (see #6).

### Agent memory (log)
- Empty infographic + draft CoS/sketchnote still pending apply (except visual-director gate applied).
- visual-director content gate applied 2026-09-07 with Justin approval.
- 港股收市簡報 18:00 routine miss 2026-09-08.

### Shared user memory written by this agent
- 2026-09-09: 總指揮 mistook pullback buy candidates for Pine BUY filter; corrected to Drive Pullback buy Excel first.

### Routines
| Name | Schedule | Enabled | lastRunAt | Folder |
|------|----------|---------|-----------|--------|
| Weekly self-improve reflection | `0 18 * * 5` (Fri 18:00 HKT) | true | null (never run) | `weekly-self-improve-reflection` |

### Workspace learning corpus (pointers)
- `learnings.md` — full lesson log (empty-infographic, pipelines, cron miss, US brief compare, pullback buy, DATA GATE, fusion stop, HK brief MD-only, weekly reflection entries, …)
- `draft_instructions.md` — mixed applied/superseded/pending proposals
- `v2_prompt.md` — CoS JD addendum candidate (pending)
- Pipeline docs: `hk-swing-infographic-pipeline.md`, `us-pullback-buy-source.md`, `docs/us-daily-workflow.md`

### Connectors / credentials
- None held by Self Improver specifically.
- Secrets: `[REDACTED:any-api-tokens]` — none stored in this agent’s memory files.

## Secrets placeholders only
- `[REDACTED:CURSOR_API_KEY]` — not used/stored by Self Improver
- `[REDACTED:MCP_TOKENS]` — none in agent memory
- `[REDACTED:GOOGLE_OAUTH]` — not owned by this agent (other bots may have Gmail/Calendar/Drive)
- Operational Drive resource IDs for Pullback buy are **not** secrets; listed under Historical decisions for restore fidelity.

## Pending confirms (awaiting Justin)
1. CoS standing directive: pull 港股收市簡報 content before finance-brief GenerateImage (draft in `v2_prompt.md` / `draft_instructions.md`) — **not applied**.
2. sketchnote-infographic reinforce line for live-brief content — **not applied**.
3. 港股收市簡報 18:10 miss watchdog and/or JD 16:30→18:00 align — Justin skipped widget; **log only**.
4. Weekly reflection on Self Improver is **created/enabled**; confirm Sweeper paused duplicate on 總指揮 if not already.
