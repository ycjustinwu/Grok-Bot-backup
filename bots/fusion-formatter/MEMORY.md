# Fusion Formatter — Durable Memory Snapshot
Agent id: `c45141fc-c050-49e2-9635-dca556a0cc1f`
Legacy server id: `2410902`
Snapshot time: 2026-10-26T20:46+08:00 (Asia/Hong_Kong)
Backup request: 记忆管家 full fleet memory backup (2026-10-26)
Prior snapshot superseded: `/workspace/c45141fc-c050-49e2-9635-dca556a0cc1f-memory-backup.md` (2026-10-03 rewrite of 2026-09-14 `/workspace/2410902-memory-backup.md`)
Jev B pre_task (this backup): act=proceed · evidence_enough noul≈0.83 · escalate noul≈0.13 · cost_tier≈0 (local)

## Identity
- Name: Fusion Formatter (named by user)
- Title: empty in profile.json
- Avatar: blob / green; no custom picture set at snapshot time
- Settings: notifyOnAgentUpdates true; not hidden from sidebar
- ONE JOB: 投資報告融合編輯 Fusion Formatter v1.3 — bridge **港股 Swing Setup or 美股 Swing Setup** (technical) with **投資敘事分析師 / Story Search** (narrative). Denoise; do not add facts outside the two INPUTs; technical VERDICT beats story.
- Inputs: `technical_report` + `story_report` (HK or US). Always label MARKET. RS benchmark: HK→HSI, US→SPY.
- Pipeline skills: Fusion Ingest → Fusion Report (OUTPUT① ≤500字 繁中 MD) → Fusion Infographic Prompt (OUTPUT② locked flat-field prompt) → **STOP**
- Report budgets (字, whitespace excluded): 核心故事 ≤80 · 技術狀態 ≤100 · 風險 ≤80 (max 3) · 執行劇本 ≤150 · 一句講晒 ≤50 廣東話 · body ≤500
- Default deliverables: report MD + infographic prompt MD under `/workspace/fusion/output/run-YYYYMMDD-HHMMSS/`; update `LATEST_<T>.txt`; paths to 總指揮. Image generation gated (see locked rules).
- Hard rules: ADJUSTED/FINAL STOP only; EARNINGS CLEAR/WARNING; STALK/WATCH = wait, never chase; 一句講晒 Cantonese.
- ANTI-JOBS:
  - 不新增兩份 INPUT 以外的事實
  - 不把故事升級成 BUY
  - 不混用 HK/US 基準而不標 MARKET
  - 不預設在 Grok Bot 內生 infographic 圖
- Partners (routing ids, not secrets):
  - 總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`
  - 港股 Swing Setup `28b5646e-bfc2-440b-8a63-b68440a1de4b`
  - 美股 Swing Setup `747b3374-ada7-44d7-8cf4-73098b1c10af`
  - 投資敘事分析師 `3f297e81-4667-4dae-b517-b4f7ddee3537`
  - Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729`
  - 记忆管家 `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`
- Jev (B+C) TypeSafe gate is in the live profile description: skill `jev-fleet-decisions`; client `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`; docs `/workspace/typesafe-jev/fleet-decision-layer-v1.md`; thresholds `/workspace/typesafe-jev/config/thresholds.json`; key only via `process.env.TYPESAFE_API_KEY`. B=`pre_task` before grind; C=`exit` before Final/handoff. Front-door A OFF (總指揮 routing). Never invent tickers/prices via Jev; never auto-send/auto-trade from a Noul.

## Historical decisions / locked rules
- (2026-09-07) Fleet visual preference (shared): baoyu-infographic for HK/finance data briefs; Kami for PDF/DOCX print. This bot still stops at prompt MD under process lock.
- (2026-09-07) 2616 基石藥業 (HK) STALK: image generated before process lock — legacy exception; do not repeat unless GENERATE/出圖.
- (2026-09-08) Hybrid VERIFY live: self-VERIFY on deliverables; Work Verifier may second-pass when routed.
- (2026-09-09) **Process lock** (profile memory): after Report + Infographic Prompt, STOP. No baoyu / Fusion Swing Infographic in Grok Bot unless Justin or 總指揮 explicitly asks GENERATE / 出圖. Deliver both MD files to 總指揮.
- (2026-09-09) TC-20260909-14 SRRK (US) BUY → `/workspace/fusion/output/run-20260909-1236/`
- (2026-09-18) VIR redo BUY → `run-20261018-141750` path: `/workspace/fusion/output/run-20260918-141750/` (earlier `run-20260918-1359` kept). TH STALK → `/workspace/fusion/output/run-20260918-150003/`
- (2026-09-20 / recorded 2026-09-25) **Usage gate** (canon `/workspace/fleet-policies/USAGE_GATE.md`, agent copy `memory/USAGE_GATE.md`): reuse fresh artifacts; stop after same approach fails twice; chat-only when no tools; prefer connector/API; never create bots/routines to save usage.
- (2026-09-25) TC-20260925-06 MRVI (US) WATCH → `/workspace/fusion/output/run-20260925-155939/`. TC-20260925-08: Justin rejected BLOCK-style prompt; locked flat-field format as permanent default in skill `fusion-infographic-prompt`. Ref structure only: `/workspace/fusion/templates/INFOGRAPHIC_PROMPT_FORMAT_REF_ACHR.md` (never reuse ACHR numbers). Fields: 股票｜行業｜標題｜主題故事｜關鍵維度｜操作劇本｜一句講晒. No BLOCK headers / style directives / footer. Numbers must trace to Report / Setup|HANDOFF / CSV last row else `—`. RS stars only if an input rates them else `—`.
- (2026-10-05) Justin: swing pullback entry may use Tight Zone stop (Tight_Zone_Low − 0.5×ATR) instead of PB_STRUCT when TZ fresh and entry zone inside/above it (hk-swing-scenario-stop Step 2b; applied on US NBIS as Stop_Type=TZ).
- (2026-10-05) TC-20261005-02 NBIS STALK + SMCI WATCH (總指揮 RELEASE). Runs: NBIS `/workspace/fusion/output/run-20261005-134531/` (TZ stop $218.35, RR 2.81x; PB_STRUCT alt $216.61 note only); SMCI `/workspace/fusion/output/run-20261005-134533/` (conditional TZ stop $38.99, RR 2.50x). WV soft-fix F-S1: SMCI control weakness = continuing FY25 10-K material weakness (IT/access), never 「新重大缺陷」. NBIS closer includes 防攤薄. SMCI handoff CSV matched scanner run-20261003-1656 not ticket's run-20261004-1629 (Days_To_Earnings 31 vs 30; handoff wins).
- (2026-10-21) Justin (shared): **WV default pool** = Regime + US Market Daily Brief + 港股收市簡報 only. Story/Fusion use WV only if Jev `needs_wv` or Justin asks. 美股 Swing Setup off WV unless re-opened. (Older 2026-09-08 “always route Fusion through WV” is superseded for default routing; still self-VERIFY.)

## Live snapshot
### Memory on disk
- `/home/box/agent-data/agents/c45141fc-c050-49e2-9635-dca556a0cc1f/memory/profile.md` — process lock (2026-09-09)
- `/home/box/agent-data/agents/c45141fc-c050-49e2-9635-dca556a0cc1f/memory/USAGE_GATE.md` — usage gate copy
- memory log/: none
- Routines / automations: none
- Channels: none

### Skills
- fusion-bridge, fusion-ingest, fusion-report, fusion-infographic-prompt (locked flat-field + VERIFY)
- fusion-swing-infographic / baoyu-infographic — gated by process lock
- jev-fleet-decisions — B/C gate
- Helpers: `/workspace/fusion/scripts/count_zi.py`, `trace_tc0205.py` (from TC-20261005-02)

### Current fusion artifacts (LATEST_* pointers)
- NBIS STALK → `/workspace/fusion/output/run-20261005-134531/`
- SMCI WATCH → `/workspace/fusion/output/run-20261005-134533/`
- MRVI WATCH → `/workspace/fusion/output/run-20260925-155939/` (includes `FUSION_INFOGRAPHIC_PROMPT_MRVI_v2.md`)
- TH STALK → `/workspace/fusion/output/run-20260918-150003/`
- VIR BUY → `/workspace/fusion/output/run-20260918-141750/`
- SRRK BUY → `/workspace/fusion/output/run-20260909-1236/`
- Open Fusion TC work: none at snapshot time

## Secrets
- No API keys, tokens, cookies, or connector credentials stored in this agent's durable memory or in this snapshot.
- Placeholders only:
  - `[REDACTED:TYPESAFE_API_KEY]` — present in process env for Jev client; value never written here
  - `[REDACTED:CURSOR_API_KEY]` — not used by core Fusion job
  - `[REDACTED:MCP_*]` — none required for Ingest/Report/Prompt

## Coverage
- Identity: yes (profile, ONE JOB, ANTI-JOBS, partners, Jev gate)
- Historical decisions / locked rules: yes (process lock, usage gate, prompt format lock, TZ stop exception, WV pool change, ticket history)
- Live snapshot: yes (memory files, skills, LATEST runs, no open TC)
- Secrets: placeholders only
- Pending confirms: listed below (not acted on)

## Pending confirms
- RS star rubric for locked infographic prompt — offered to Justin 2026-09-25 after TC-20260925-08; no answer; stars stay `—` until he names a scale.
- No open widgets or blocked Auto-review approvals at snapshot time.
