# Memory disaster-recovery backup — 總指揮
- Written: 2026-09-14 ~20:31 HKT
- Agent id: `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`
- Path: `/workspace/2410895-memory-backup.md`

## 1. Identity

- **Name:** 總指揮
- **Title:** 總指揮
- **Role:** Justin Wu’s single Grok Bot liaison (Firstmate-style captain contact). Justin talks here; crew reports outcomes/blockers to 總指揮, not past him to Justin (unless he opened their chat).
- **ONE JOB:** Coordinate bots and handoffs. Do not do specialist analysis when a specialist exists.
- **User:** Justin Wu · timezone Asia/Hong_Kong · X `@Ycjustinwu`

## 2. Historical decisions (lasting preferences / rules)

### Orchestration / harness
- New bots/skills must pass harness-bot-standard (ONE_JOB, ANTI_JOBS, IO, VERIFY, handoff, approval-by-reversibility); gate via 總指揮, Prompt Architect, dr eggbot.
- Hybrid verification: producer self-VERIFY → Work Verifier (high-stakes) → 總指揮 relays → Justin.
- Firstmate essentials absorbed into 總指揮 (not a replace): TC-YYYYMMDD-## handoffs; default handoff for grind; one decision card; outcomes over mechanics.
- High-stakes → Work Verifier: Swing Setup, Story, Fusion, Regime, Daily Briefs (HK/US). Scanners skip unless asked.

### US cash-session stack
- Order: (A) Market Awareness (T2108 → StockCharts breadth → regime) → (B) US Market Brief → (C) Potential Setups via US Swing Scanner → STOP → (D) Setup→Story→Fusion only on Justin’s explicit ticker pick.
- Pullback buy = Google Drive Excel `Pullback buy` fileId `1CXYi_h8t26x_ABZmTiqQSpJc91uZWZ3ad-QQ5qnI2UU` in folder `1tnTfbYp13vdjEV4Bc123ehloII-iodor` — **not** filtering Pine BUY rows.
- Pine screener lists Justin pastes are a separate Potential Setups path.
- **DATA GATE (highest priority):** missing/stale/abnormal yfinance, StockCharts, Stockbee Monitor/T2108, bad CSVs, OCR fail → STOP phase, notify Justin with source + expected vs actual date; never invent.
- Playbook: skill `us-daily-market-potential-setups` + `/workspace/docs/us-daily-workflow.md`.

### Token-save locks
- Fusion: report MD + infographic prompt MD → STOP; no baoyu image in Grok Bot unless Justin asks (he generates elsewhere).
- 港股收市簡報: Markdown only `HK brief-YYYY-MM-DD.md` under `/workspace/hk-brief-inputs/YYYY-MM-DD/`; no Kami/PDF unless he asks that day.

### Visuals / docs
- HK finance briefs: baoyu-infographic defaults dashboard × craft-handmade, landscape, zh; parchment+ink-blue preference historically.
- Kami for PDF/DOCX when PDF is wanted; sketchnote-infographic for cream educational; visual-director for other assets.
- Prefer infographic visuals over photo/cinematic cover art for HK/finance briefs.

### Life / connectors
- Gmail, Google Calendar, Google Drive, X connected; 全富決策副手 uses Google for schedule/email-aware decisions.
- Elder son ~12 at Queen’s College (皇仁); younger ~9 at Raimondi College Primary + British Council Primary Plus.
- 旅行計劃助手 = trips only; 全富決策副手 = family/finance decisions (no full itineraries).

### Self-improve / ops
- Self Improver: `/workspace/learnings.md`; drafts in `draft_instructions.md` / `v2_prompt.md`; human approval before apply.
- 2026-09-11 Friday SI proposed A–D (HK Monitor session-date gate, visuals addendum, sketchnote, re-enable HK cron); Justin chose **Hold — apply nothing yet**.
- Weekly self-improve reflection on 總指揮: **paused** 2026-09-14 (moving Friday wake to Self Improver per Sweeper/Justin).
- Kick HK after-close brief (`5 18 * * 1-5`): **paused**/never-run; 港股收市簡報 own 18:00 cron historically flaky (scheduler).

### Work Verifier refine (2026-09-11)
- Same bot id `037de516-dbc1-4565-a127-5dbb0f691729`.
- Skills: `work-verify` + `verify-work-verifier` with feature maps (hk-after-close, us-daily-brief, regime, hk-swing, us-swing, story+fusion).
- Pipeline: Launch → Doctor → Drive → Evidence → Cleanup.

### Grok Build (2026-09-14)
- CLI installed `~/.local/bin/grok` v1.0.30; use headless `grok -p` when local coding fits; CloudAgent for big repo fleets.
- Auth: SuperGrok device OAuth as `ycjustinwu@gmail.com` — **not** console API key. Session: `~/.grok/auth.json`.

### Key Drive / sheet IDs
- HK Market Monitor / “HK market breadth”: `1yIZLgTIqq38i_fK-q5oBWFogk0OCH1WuZ9a6AiAP8WI`
- US Pullback buy sheet: `1CXYi_h8t26x_ABZmTiqQSpJc91uZWZ3ad-QQ5qnI2UU`
- Pullback folder: `1tnTfbYp13vdjEV4Bc123ehloII-iodor`

### Roster map (ids)
- Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729`
- X Brief `0ba0445d-a3df-4430-8a47-0eeb0cbbafcf`
- HK Swing Scanner `162f41b3-b93f-4d05-abdf-07b938f6ab56`
- Self Improver `1d369773-e1f5-4fdf-9a3a-2a38b1f54e16`
- 港股 Swing Setup `28b5646e-bfc2-440b-8a63-b68440a1de4b`
- US Swing Scanner `293d30a5-d04e-4443-89d9-f313f9ca873e`
- 投資敘事分析師 `3f297e81-4667-4dae-b517-b4f7ddee3537`
- US Market Daily Brief `44fb5c78-45d1-4716-b849-a5a6a0c1867b`
- 美股 Swing Setup `747b3374-ada7-44d7-8cf4-73098b1c10af`
- 旅行計劃助手 `83647ac1-ec27-4889-aa08-1e376d4b738c`
- 全富決策副手 `925c3eaa-b0c0-440d-84a2-d28f7ed881e8`
- 港股收市簡報 `b9d6b823-8ae3-46a7-bc08-9beb4a35c631`
- Fusion Formatter `c45141fc-c050-49e2-9635-dca556a0cc1f`
- dr eggbot `cfe284bb-b01f-4f60-81af-4345d37a42f8`
- Prompt Architect `cfe4ca9b-b60f-49d3-bd0d-454c269f4388`
- Market Awareness Orchestrator `e4e8d80f-26c5-48c1-bd11-f56c0a9cc077`
- 记忆管家 `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`
- Sweeper / 清道夫 `8dbca7e8-e0d0-4447-821a-f9a3ad9d7e06`

## 3. Live snapshot (worth restoring)

### Routines on this bot
| Folder | Name | Schedule | Enabled |
|--------|------|----------|---------|
| `weekly-self-improve-reflection` | Weekly self-improve reflection | `0 18 * * 5` | **paused** |
| `kick-hk-after-close-brief` | Kick HK after-close brief | `5 18 * * 1-5` | **paused** |

### Recent deliverables / paths
- HK briefs: `/workspace/hk-brief-inputs/YYYY-MM-DD/HK brief-YYYY-MM-DD.md` (e.g. 2026-09-10 verified PASS_WITH_NOTES).
- Work Verifier output: `/workspace/work-verifier/output/` (+ refined drafts `/workspace/work-verifier/refine-20260911/`).
- US stack docs: `/workspace/docs/us-daily-workflow.md`
- SI drafts (not applied): `/workspace/draft_instructions.md`, `/workspace/v2_prompt.md`, learnings `TC-20260911-SI` in `/workspace/learnings.md`
- US scanner: `/workspace/us-swing-scanner/scripts/us_swing_v451.py` → `output/run-*/`
- HK scanner: `/workspace/hk-swing-scanner/scripts/hk_swing_v451.py` → `output/run-*/`

### Open / held items
- SI items A–D (Monitor session-date gate; visuals JD addendum; sketchnote; re-enable HK 18:00/18:05 + pick 16:30 vs 18:00) — **held** per Justin 2026-09-11.
- HK auto-brief still off; manual kick when Justin pastes movers.
- Grok Build ready (authenticated); use when applicable for local coding tasks.

### ANTI-JOBS reminder
- Do not run swing math, regime scoring, or specialist research inline.
- Do not invent tickers/prices/VERDICTs.
- Do not skip Work Verifier on high-stakes finals.
- Never use 「港美股 Swing Setup」 alias.
- Do not keep multi-minute grind in this chat when a crewmate owns it.

## 4. Secrets placeholders (names only — no values)

- `[REDACTED:XAI_API_KEY]` — **not used**; SuperGrok OAuth preferred
- `[REDACTED:~/.grok/auth.json]` — Grok Build OAuth session (device login as ycjustinwu@gmail.com)
- `[REDACTED:Google connector tokens]` — Gmail / Calendar / Drive (MCP; not stored in this agent’s chat memory)
- `[REDACTED:X connector / API credits]` — X MCP as @Ycjustinwu
- Browser/session cookies on shared computer for StockCharts / Stockbee / TradingView — `[REDACTED:box-browser-sessions]` (not copied here)

**Confirm with Justin if restoring:** whether to re-enable paused routines; whether SI drafts A–D should still stay held; Grok Build auth may need re-login on a fresh machine (do not copy `auth.json` into git/tickets).
