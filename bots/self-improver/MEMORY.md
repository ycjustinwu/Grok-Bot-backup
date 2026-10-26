# Memory disaster-recovery backup — Self Improver
- **agent_id:** `1d369773-e1f5-4fdf-9a3a-2a38b1f54e16`
- **serverId:** `2410911`
- **snapshot_at:** 2026-10-26 20:45 HKT
- **path:** `/workspace/1d369773-e1f5-4fdf-9a3a-2a38b1f54e16-memory-backup.md`
- **supersedes:** prior body at same path (snapshot 2026-10-03 20:09 HKT); older `/workspace/2410911-memory-backup.md` (2026-09-14) still stale — do not restore from it
- **own store:** `/cursor/stores/store-d6bf6035-5d45-41cd-9f9c-8a78c87c8d69`

## Identity
- **Name:** Self Improver (named by user)
- **Title field:** empty in profile.json (role is the name itself)
- **User:** Justin Wu (Asia/Hong_Kong)
- **Harness:** temporal
- **ONE JOB / PRIMARY ROLE:** Capture task outcomes, user corrections, and execution failures for Justin’s Grok Bot team; reflect on patterns; propose skill and instruction improvements; never overwrite Job Descriptions, skills, or guardrails without Justin’s explicit approval.
- **Workflow:** [self-improve](sand-workflow:self-improve) — learnings → drafts → Justin approve → archive `prompt_history/` → apply. Weekly Friday ~18:00 HKT routine.
- **ANTI-JOBS:** Do not invent lessons; do not overwrite without approval; do not delete learnings or history without asking; do not turn one-off noise into standing rules; do not create bots or routines just to save usage.
- **Jev (B+C):** TypeSafe `pre_task` / `exit` via `/workspace/typesafe-jev/jev_client.py`; key `[REDACTED:TYPESAFE_API_KEY]` only. Front-door A OFF (總指揮 routing). Never invent tickers/prices via Jev; never auto-send / auto-trade from a Noul.
- **pstack hang (meta Option A, TC-20261016-10):** encode-lessons + subtract + laziness when rewriting bots/skills; no raw architect/arena/swarm/tdd/create-verification-skill hang; no invent Firstmate CLI; no fleet-wide mass hang.
- **Partners / handoff faces:**
  - **總指揮** `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` — TCs, routing, JD paste targets
  - **Work Verifier** `037de516-dbc1-4565-a127-5dbb0f691729` — feature maps under `verify-work-verifier/features/`
  - **Prompt Architect** `cfe4ca9b-b60f-49d3-bd0d-454c269f4388` — JD/skill rewrites when needed
  - **记忆管家** `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` — fleet memory backups (this file)
  - Market producers (learn-only / draft targets): US Market Daily Brief, 港股收市簡報, Market Awareness Orchestrator, X Monitor, Visual Director / sketchnote
- **Primary artifacts:**
  - `/workspace/learnings.md` — living lesson log (**341** lines at snapshot)
  - `/workspace/draft_instructions.md` — proposed improvements (**541** lines)
  - `/workspace/v2_prompt.md` — candidate JD / feature patches (**75** lines)
  - `/workspace/prompt_history/` — **11** archive files before apply
  - Skill: `self-improve` (`/home/box/agent-data/workflows/self-improve/SKILL.md`); Jev: `jev-fleet-decisions`
- **Settings:** `notifyOnAgentUpdates: true`; not hidden from sidebar
- **Avatar:** shape blob, color blue (default mark; no custom picture)

## Historical decisions / locked rules
1. **2026-09-07 — Empty finance-brief infographic:** **Applied:** visual-director Execute content gate only. Archive: `prompt_history/2026-09-07_2246_visual-director.md`. 總指揮 JD empty-visual twin still HOLD.
2. **2026-09-08 — HK swing→infographic pipeline:** HK Swing Scanner → 港股 Swing Setup → 投資敘事分析師 → Fusion Formatter → fusion-swing-infographic / baoyu. Do not skip Fusion.
3. **2026-09-08 — 港股收市簡報 cron miss:** Enabled `0 18 * * 1-5` can have null wake; JD ~16:30 vs cron 18:00 mismatch still OPEN ops.
4. **2026-09-09 — pullback buy:** Drive Pullback buy → US Swing Scanner → **Potential Setups STOP**. No auto 美股 Swing Setup. Canon: `/workspace/docs/us-daily-workflow.md`.
5. **2026-09-09 — US DATA GATE:** Missing/stale yfinance / StockCharts / Stockbee / critical inputs → STOP → 總指揮→Justin; never invent numbers.
6. **2026-09-09 — US brief Claude-compare deltas:** Applied to us-focus-catalyst / us-rotation-structure / us-market-daily-brief. Archives `2026-09-09_1012_*`.
7. **2026-09-14 — Weekly SI routine** moved onto this bot (not 總指揮 chat).
8. **2026-09-18 / 09-25 / 10-09 / 10-16 weekly widgets:** Justin Hold / skip = hold drafts; do not assume approve or reject.
9. **2026-09-20 — USAGE_GATE:** Canon `/workspace/fleet-policies/USAGE_GATE.md`. Reuse fresh artifact; stop after same approach fails twice; prefer connectors; never create bots/routines to save usage.
10. **2026-09-23 — Regime 5B hysteresis multi-band confirm** live in producer; Index DD Gate **2026-10-01** live.
11. **2026-09-24 — US Swing Scanner Drive:** parent `US_Stock_Data` `1Jn7yi0sXFBqVjLvjCsIazZnOvw0_E4TY`; dated folders; native CSV.
12. **2026-09-30 — HK producer locks:** No 100億 H-cap gate; Justin TV AV authoritative (no Yahoo AV FAIL); hide clean verify clutter; research ladder Sheets → Tavily → Firecrawl → Browserless → Browser Use → desktop last.
13. **2026-10-02 — Justin Apply:** same-contract commodity % (US+HK briefs) + WV `hk-after-close-brief` map sync to Sep 30. Archives `2026-10-02_1830_*`.
14. **2026-10-05 — TZ Step 2b** on pullback (`hk-swing-scenario-stop`) applied outside SI path; US Swing NBIS+SMCI learnings logged.
15. **2026-10-13 — One-shot sandwich cron never-run:** enabled ≠ delivered (mode A). Draft routine-delivery note.
16. **2026-10-14→16 — US AV keeper >$5B** + TV MCP AV primary; Second brain driven by US Swing Scanner (noon cron paused).
17. **2026-10-21 — X Monitor Weekday Activity task failed** (mode B wake-then-fail before tools). Learning `SI-20261021-02`. Recovery one-shot OK.
18. **2026-10-21 — WV default pool:** Regime + US Market Daily Brief + 港股收市簡報 only. 美股 Swing Setup off WV unless Justin re-opens.
19. **2026-10-22 — US brief `### 盤後業績`:** AH large-cap earnings required; seed X Monitor; Justin-named AH always covered. Doc: `/workspace/docs/us-brief-ah-earnings-lock-2026-10-22.md`. Regime `### 今日動作` / Trial carve-out same window.
20. **2026-10-23 — Regime Intermediate Land (producer):** pending FAIL + raw R > prior effective E → land effective=R, clear pending; day-1 ladder still forbidden. Canon: `docs/hysteresis-intermediate-land-2026-10-23.md` + `regime-bands.md`.
21. **2026-10-23 18:16 — Justin Apply 1+2 (`SI-20261023-01`):** (a) WV `regime-market-awareness.md` Intermediate Land sync; (b) 總指揮 JD `ROUTINE DELIVERY RISK` paste. Archives `2026-10-23_1815_*`. Mid-apply PLACEHOLDER staging glitch restored same minute.
22. **Fleet Market Master sheet** (shared): `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` — US/HK breadth, industry, ETF rotation, Setup_Latest.

## Live snapshot
### Agent memory still in force (profile / journal)
- USAGE_GATE; HK swing pipeline; pullback-buy STOP; US DATA GATE.
- Hybrid WV: default pool Regime + US Daily Brief + 港股收市簡報; outputs `/workspace/work-verifier/output/`.
- Journal 2026-10-23: Apply 1+2 done; soft HOLDs remain.
- Journal 2026-10-21 / 10-13: cron delivery risk (never-run + Activity-task failed).
- Shared: Intermediate Land lock; AH 盤後業績; WV pool; Market Master id; TV MCP AV for US+HK briefs.

### Routine
| Name | Schedule | Enabled | last known run | Folder |
|------|----------|---------|----------------|--------|
| Weekly self-improve reflection | `CRON_TZ=Asia/Hong_Kong 0 18 * * 5` (Fri ~18:00 HKT, flexible ±15m) | true | 2026-10-23 ~18:12 HKT succeeded (system automation_status); local `automation.json` lastRunAt may lag null | `795f3874-6232-55f4-9e98-71b9ee5b2761` |

Prompt intent: run self-improve, short digest + apply/hold widget to Justin; stay quiet if nothing useful. Do not announce “routine triggered.”

### Paths / open work
- Live WV Regime map: `/home/box/agent-data/workflows/verify-work-verifier/features/regime-market-awareness.md` (Intermediate Land applied).
- Drafts still listing OPEN HOLDs: `/workspace/draft_instructions.md` §2026-10-23 apply log + Finding F; `/workspace/v2_prompt.md` empty-visual + Monitor-date JD still candidates.
- No in-flight apply at snapshot time.

### Connectors
- Self Improver day-to-day: box files + Jev client; may use fleet MCPs when investigating. Does not own Gmail/Calendar/Drive/X sessions for this role.
- Secrets: see below — never paste values into backups or chat.

## Secrets
- `[REDACTED:TYPESAFE_API_KEY]` — present in box env for Jev client only; never paste
- `[REDACTED:FIRECRAWL_API_KEY]` — may exist on shared box; not owned by this agent’s profile
- `[REDACTED:AGENTMAIL_API_KEY]` — shared box; not used for SI core loop
- `[REDACTED:oauth_tokens]` — none held in this agent’s profile/memory
- `[REDACTED:github_token]` — none held
- Drive/sheet folder ids above are operational ids, not secrets

## Pending confirms (still HOLD — list only; do not act on restore)
1. Silver / continuous vs named-month tighten (same-contract already live; named-month tighten still draft).
2. HK Stock360 「其餘板塊」 remainder-band honesty skill rule (behavior improved Oct 16–23; draft still OPEN).
3. theme-% 「均跌逾」 anti-job (`us-market-daily-brief` + `us-focus-catalyst`).
4. `us-rotation-structure` full-threshold rows or 「節錄」 header.
5. 總指揮 JD: empty market-brief visual content gate (`v2_prompt.md`) — skill gate already live 2026-09-07; JD twin not pasted.
6. 總指揮 JD: Market Monitor date anti-job (HK same day; US CUP/Regime D+1 disclose) — producer skills locked; JD twin not pasted.
7. sketchnote-infographic content reinforce (low).
8. Ops: HK after-close cron re-arm + align JD ~16:30 ↔ cron 18:00.

**Do not re-apply (already live):** Intermediate Land producer + WV map; US `盤後業績`; Regime 今日動作/Trial; WV pool; same-contract commodity; HK Sep 30 producer + WV HK map; visual-director Execute gate; USAGE_GATE; ROUTINE DELIVERY RISK on 總指揮 JD.

## Coverage
| Area | Covered |
|------|---------|
| Identity / ONE JOB / ANTI-JOBS / partners / Jev / pstack | yes |
| Historical decisions through 2026-10-23 Apply 1+2 | yes |
| Live memory, routine, settings, paths | yes |
| Applied vs HOLD | yes |
| Secrets | placeholders / names only |
| Full verbatim learnings.md / draft bodies | no — pointers + line counts (341 / 541 / 75) |
| Acting on pending confirms | **no** (list only per 记忆管家) |
