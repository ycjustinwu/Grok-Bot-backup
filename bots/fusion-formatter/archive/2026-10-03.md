# Fusion Formatter — Durable Memory Snapshot
Agent id: `c45141fc-c050-49e2-9635-dca556a0cc1f`
Snapshot time: 2026-09-14T20:32:45.049764+08:00 (Asia/Hong_Kong)
Backup request: 记忆管家 full fleet DR (Justin)

## Identity
- Name: Fusion Formatter
- Title: Fusion Formatter (profile title field empty)
- Role: 投資報告融合編輯 v1.3
- Bridge: **港股 Swing Setup** or **美股 Swing Setup** (technical) ↔ **投資敘事分析師／Story Search** (narrative)
- Inputs: `technical_report` + `story_report` (HK or US; always label MARKET)
- Pipeline skills: Fusion Ingest → Fusion Report (OUTPUT① ≤500字 MD) → Fusion Infographic Prompt (OUTPUT② prompt file) → **STOP**
- Default deliverables: Fusion report MD + infographic prompt MD to 總指揮 / Justin
- Hard rules: ADJUSTED STOP only; EARNINGS warnings; STALK = wait volume / do not chase; 一句講晒 = 廣東話; tech VERDICT beats story
- ANTI-JOBS: no facts outside the two INPUTs; never upgrade story into BUY; never mix HK/US benchmarks without MARKET; do **not** default-generate baoyu/infographic images inside Grok Bot
- Upstream tickets: typically from 總指揮 (e.g. TC-YYYYMMDD-NN)
- Downstream: Work Verifier may second-pass high-stakes Fusion outputs under `/workspace/work-verifier/output/`

## Historical decisions
- (2026-09-09) **Process lock (Justin via 總指揮):** After Fusion Report MD + Infographic Prompt, **STOP**. Do not run Fusion Swing Infographic / baoyu image generation in Grok Bot unless Justin or 總指揮 explicitly asks `GENERATE` / 出圖. Justin generates images elsewhere to save Grok Bot tokens. Deliver both MD files to 總指揮.
- (2026-09-07) Pipeline for 2616 基石藥業 (HK): tech VERDICT locked STALK; fused Story Search narrative; OUTPUT①+② delivered; user selected dense-modules × craft-handmade and image was generated **before** process lock (legacy exception; do not repeat unless asked).
- (2026-09-09) Ticket **TC-20260909-14** SRRK (MARKET=US): VERDICT BUY (tech-locked); ADJUSTED STOP $53.77 PB_STRUCT; SELF-VERIFY PASS; MD delivered; infographic deferred (MD priority / later process lock). Work Verifier routed as TC-20260909-15 by 總指揮.
- User preference (shared / fleet): HK/finance briefs prefer baoyu-infographic (dashboard or dense-modules) over photo/cinematic art; Kami for PDF/DOCX print — but **this bot stops at prompt MD** under process lock.
- Hybrid verification live (fleet): high-stakes Fusion may be independently verified by Work Verifier; self-VERIFY still required on deliverables.

## Live snapshot
### Memory on disk
- Agent memory profile: `/home/box/agent-data/agents/c45141fc-c050-49e2-9635-dca556a0cc1f/memory/profile.md` (1 profile fact: process lock)
- Agent memory log/: none present at snapshot time
- Routines / automations: none
- Channels: none noted

### Recent fusion artifacts (workspace)
- SRRK run: `/workspace/fusion/output/run-20260909-1236/`
  - `FUSION_REPORT_SRRK.md`
  - `FUSION_INFOGRAPHIC_PROMPT_SRRK.md`
  - `FUSION_INGEST_SRRK.md`
  - `SELF_VERIFY_SRRK.md`
- Pointer: `/workspace/fusion/output/LATEST_SRRK.txt`
- Legacy 2616 infographic workdir: `/workspace/infographic/2616-cstone/` (source, structured-content, prompts; image path under sand-data assets if retained)

### Key teammate ids (for routing; not secrets)
- 總指揮: `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`
- 港股 Swing Setup: `28b5646e-bfc2-440b-8a63-b68440a1de4b`
- 美股 Swing Setup: `747b3374-ada7-44d7-8cf4-73098b1c10af`
- 投資敘事分析師 / Story Search: `3f297e81-4667-4dae-b517-b4f7ddee3537`
- Work Verifier: `037de516-dbc1-4565-a127-5dbb0f691729`
- 记忆管家: `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`

### Skills relied on (workflow library)
- fusion-bridge, fusion-ingest, fusion-report, fusion-infographic-prompt
- fusion-swing-infographic / baoyu-infographic — **gated by process lock** (prompt only by default)
- work-verify (self-VERIFY on deliverables)

## Secrets placeholders only
- No connector tokens stored in this agent’s durable memory.
- Any future API keys / bot tokens / session cookies: `[REDACTED:name]` only — never paste real values into this backup.
- Placeholders (none currently held by Fusion Formatter):
  - `[REDACTED:CURSOR_API_KEY]` — not used by this bot’s core job
  - `[REDACTED:MCP_*]` — none required for Fusion Ingest/Report/Prompt

## Coverage
- Identity: yes (profile + JD)
- Historical decisions: yes (process lock + 2616/SRRK tickets)
- Live snapshot: yes (memory files, outputs, teammate routing)
- Secrets: placeholders only (no real secrets present)
- Pending confirms: none

## Pending confirms
- None. No open user widgets or blocked approvals at snapshot time.
