# Fusion Formatter — Durable Memory Snapshot
Agent id: `c45141fc-c050-49e2-9635-dca556a0cc1f`
Legacy server id: `2410902`
Snapshot time: 2026-10-03T20:09+08:00 (Asia/Hong_Kong)
Backup request: 记忆管家 full fleet memory backup (Justin)

## Identity
- Name: Fusion Formatter (named by user)
- Title: empty in profile.json; sidebar role chip unset
- Avatar: blob / green; custom picture not set in this snapshot
- Settings: notifyOnAgentUpdates true; hidden_from_sidebar not set
- Role: 投資報告融合編輯 Fusion Formatter v1.3
- Bridge: 港股 Swing Setup or 美股 Swing Setup (technical) ↔ 投資敘事分析師 / Story Search (narrative)
- Inputs: technical_report + story_report. Always label MARKET. HK RS benchmark HSI; US RS benchmark SPY.
- Pipeline: Fusion Ingest → Fusion Report (OUTPUT① ≤500字, 繁中) → Fusion Infographic Prompt (OUTPUT②) → STOP
- Report budgets (字, excluding whitespace): 核心故事 ≤80, 技術狀態 ≤100, 風險 ≤80 (max 3 items), 執行劇本 ≤150, 一句講晒 ≤50, total body ≤500
- Hard rules: technical VERDICT is locked and the story never upgrades it; stop is always the ADJUSTED/FINAL STOP from the handoff; STALK and WATCH mean wait, never chase; 一句講晒 is Cantonese ≤50字; add no facts beyond the inputs
- Default deliverables: Fusion report MD + infographic prompt MD, saved under `/workspace/fusion/output/run-YYYYMMDD-HHMMSS/`, pointer `/workspace/fusion/output/LATEST_<T>.txt`, then paths to 總指揮 (priority) so 總指揮 can route Work Verifier
- ANTI-JOBS: no facts outside the two inputs; never upgrade story into BUY; never mix HK/US benchmarks without MARKET; do not default-generate baoyu / Fusion Swing Infographic images inside Grok Bot
- Routines: none
- Channels: none

## Historical decisions
- (2026-09-07) Fleet visual preference (shared, via 總指揮): HK/finance briefs prefer baoyu-infographic (dashboard or dense-modules), not photo or cinematic cover art. Kami for PDF/DOCX/print. This bot still stops at the prompt MD under the process lock.
- (2026-09-07) 2616 基石藥業 (HK): tech VERDICT locked STALK; fused Story Search narrative; OUTPUT①+② delivered; user picked dense-modules × craft-handmade and an image was generated before the process lock. Legacy exception. Do not repeat unless asked. Workdir noted previously at `/workspace/infographic/2616-cstone/`.
- (2026-09-08) Hybrid verification live (shared, via 總指揮): every bot/skill includes a VERIFY step. Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729` does an independent second pass on high-stakes outputs including Fusion, writing to `/workspace/work-verifier/output/`. 總指揮 routes that pass before Justin treats the output as final. Self-VERIFY still required on this bot's deliverables.
- (2026-09-09) Process lock (Justin via 總指揮; profile memory): after Fusion Report MD + Infographic Prompt, STOP. Do not run baoyu / Fusion Swing Infographic image generation in Grok Bot unless Justin or 總指揮 explicitly asks GENERATE / 出圖. Justin generates images elsewhere to save tokens. Deliver both MD files to 總指揮.
- (2026-09-09) Ticket TC-20260909-14 SRRK (MARKET=US): VERDICT BUY (tech-locked). Run `/workspace/fusion/output/run-20260909-1236/`. SELF-VERIFY written. Infographic image deferred. 總指揮 routed Work Verifier as TC-20260909-15.
- (2026-09-18) VIR (US) redo, ticket TC-20260918-16: VERDICT BUY. Canonical run `/workspace/fusion/output/run-20260918-141750/` (earlier attempt folder `run-20260918-1359` also exists). Pointer `LATEST_VIR.txt`.
- (2026-09-18) TH Target Hospitality (US): VERDICT STALK. Run `/workspace/fusion/output/run-20260918-150003/`. Pointer `LATEST_TH.txt`.
- (2026-09-20, recorded 2026-09-25) Usage gate (Justin via 總指揮; canon `/workspace/fleet-policies/USAGE_GATE.md`, copy also at this agent's `memory/USAGE_GATE.md`): reuse a fresh artifact if one exists; stop and report after the same approach fails twice; chat-only when no tools are needed; prefer connector/API over clicking a site; never create more bots or routines to save usage.
- (2026-09-25) Ticket TC-20260925-06 MRVI (US), requested via 投資敘事分析師: VERDICT WATCH. Run `/workspace/fusion/output/run-20260925-155939/`. Trigger: pullback $7.24–$7.30, no close below $7.04; CSV rerun must show HL ≥5 and SMA50 slope >0 before upgrade to STALK. Conditional stop $6.83 (PB_STRUCT). Ladder $8.98 / $10.25 / $11.47. RR 3.57x at $7.30. Earnings CLEAR 2026-11-05. CONVICTION LOW. Body 416/500. Pointer `LATEST_MRVI.txt`.
- (2026-09-25) Ticket TC-20260925-08 (Justin via 總指揮): Justin rejected the BLOCK-style infographic prompt. MRVI rewritten as `FUSION_INFOGRAPHIC_PROMPT_MRVI_v2.md` in the same run folder. Format locked as the permanent default for every future Fusion prompt, HK and US, in skill `fusion-infographic-prompt`. Structure copied from `/workspace/fusion/templates/INFOGRAPHIC_PROMPT_FORMAT_REF_ACHR.md` (ACHR numbers never reused). Fields in order: 股票｜行業｜標題｜主題故事 (催化/基本面/驅動力 + 時間線)｜關鍵維度 (RS Score + stars + 1M/3M; 趨勢 Minervini/Stage2/MA; 成交量 x + arrow; Risk%/Ext/RSI/距52W)｜操作劇本｜一句講晒 in 「」. No BLOCK headers, no style/layout directives, no footer. Every number must trace to Fusion Report, Setup/HANDOFF, or scanner CSV last row; if absent, write —. RS stars only when an input gives a rating; otherwise —. Offered Justin a fixed RS star rubric; no answer yet.
- Prior snapshot file from 2026-09-14 (`/workspace/2410902-memory-backup.md`) is superseded by this file. It predates VIR, TH, MRVI, the usage gate, and the locked prompt format.

## Live snapshot
### Memory on disk
- Profile facts: `/home/box/agent-data/agents/c45141fc-c050-49e2-9635-dca556a0cc1f/memory/profile.md` (one fact: process lock, 2026-09-09)
- Usage gate copy: `/home/box/agent-data/agents/c45141fc-c050-49e2-9635-dca556a0cc1f/memory/USAGE_GATE.md`
- Agent memory log/: none
- Conversation-scoped memory: none recorded beyond this thread's run history
- Routines: none
- Channels: none

### Skills this bot owns or relies on
- Pipeline: fusion-bridge, fusion-ingest, fusion-report, fusion-infographic-prompt (rewritten 2026-09-25 to the locked flat-field format; VERIFY step kept)
- fusion-swing-infographic / baoyu-infographic: gated by process lock (prompt only unless GENERATE / 出圖)
- work-verify: self-VERIFY on deliverables; Work Verifier does the independent second pass

### Current fusion artifacts
- MRVI (latest, WATCH): `/workspace/fusion/output/run-20260925-155939/` — report, rejected BLOCK prompt, `FUSION_INFOGRAPHIC_PROMPT_MRVI_v2.md` (the format Justin kept), `SELF_VERIFY_MRVI.md`. Pointer `LATEST_MRVI.txt`.
- TH (STALK): `/workspace/fusion/output/run-20260918-150003/`. Pointer `LATEST_TH.txt`.
- VIR redo (BUY): `/workspace/fusion/output/run-20260918-141750/`. Earlier folder `run-20260918-1359` kept. Pointer `LATEST_VIR.txt`.
- SRRK (BUY): `/workspace/fusion/output/run-20260909-1236/`. Pointer `LATEST_SRRK.txt`.

### Teammate ids used for routing (not secrets)
- 總指揮: `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`
- 港股 Swing Setup: `28b5646e-bfc2-440b-8a63-b68440a1de4b`
- 美股 Swing Setup: `747b3374-ada7-44d7-8cf4-73098b1c10af`
- 投資敘事分析師: `3f297e81-4667-4dae-b517-b4f7ddee3537`
- Work Verifier: `037de516-dbc1-4565-a127-5dbb0f691729`
- 记忆管家: `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`

## Secrets
- No API keys, tokens, cookies, or connector credentials are stored in this agent's durable memory or in this snapshot.
- Placeholders only, none currently held:
  - `[REDACTED:CURSOR_API_KEY]` — not used by this bot's core job
  - `[REDACTED:MCP_*]` — none required for Fusion Ingest / Report / Prompt

## Coverage
- Identity: yes (profile.json, description, settings, pipeline, hard rules)
- Historical decisions: yes (process lock, usage gate, format lock TC-20260925-08, tickets 2616 / SRRK / VIR / TH / MRVI)
- Live snapshot: yes (memory files, skills, current run folders, teammate routing)
- Secrets: placeholders only; no real values present
- Pending confirms: one, listed below

## Pending confirms
- RS star rubric for the locked infographic prompt. Offered to Justin on 2026-09-25 after TC-20260925-08. No rating scale exists in the inputs, so stars stay `—` until Justin names a fixed rule. No open widgets or blocked approvals at snapshot time.
