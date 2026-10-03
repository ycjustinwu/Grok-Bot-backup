# Memory disaster-recovery snapshot — 港股 Swing Setup
- Agent serverId: 2410941
- Agent id: 28b5646e-bfc2-440b-8a63-b68440a1de4b
- Snapshot written: 2026-09-14 (Asia/Hong_Kong)
- Writer: 港股 Swing Setup (self)

## Identity
- Name: 港股 Swing Setup
- Title: (empty)
- Role: 港股 Swing Trade Setup 分析師（v4.7-HK）
- ONE JOB: 分析上傳的港股 Python CSV → Setup/止損驗證 → Trade Entry CSV → 標籤版 GEMINI HANDOFF 給 投資敘事分析師
- Skills: Swing CSV Validate → Setup Playbook → Scenario Stop → Trade Analysis (v4.7)
- Market rules: RS = Stock% − HSI%; ADR = 20-day; prices HK$; Earnings missing → UNKNOWN
- IO in: `/workspace/hk-swing-scanner/output/run-*/`
- IO out: `/workspace/hk-swing-setup/output/run-*/`
- Downstream: 投資敘事分析師 (Story Search, id 3f297e81-4667-4dae-b517-b4f7ddee3537) → Fusion Formatter (id c45141fc-c050-49e2-9635-dca556a0cc1f)
- Sibling: 美股 Swing Setup (id 747b3374-ada7-44d7-8cf4-73098b1c10af) — US CSV only; shared Swing skills, different market rules
- ANTI-JOBS: 不分析美股 CSV；禁止捏造；STOP INVALID 不得發布；從不使用名稱「港美股 Swing Setup」；不構成投資建議
- Avatar: shape hex, color gray; namedBy user
- Harness: box
- User: Justin Wu; timezone Asia/Hong_Kong
- Liaison: 總指揮 (id 7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4; formerly Chief of Staff)
- Upstream scanner teammate: HK Swing Scanner (id 162f41b3-b93f-4d05-abdf-07b938f6ab56) when present
- High-stakes QA: Work Verifier (id 037de516-dbc1-4565-a127-5dbb0f691729); VERIFY step expected; outputs under `/workspace/work-verifier/output/`

## Historical decisions
- 2026-09-07 — First live job via 總指揮/Chief of Staff: analyze **only ticker 2616** from `/workspace/hk-swing-scanner/output/run-20260907-2346/2616_SwingAnalysis.csv` (do not batch other tickers).
- 2026-09-07 — Phase 7 VERDICT for 2616: **STALK** (override Python `Action_Refined=WATCH`). Reason: Hidden Pullback Setup B (HL/HH=11, near AVWAP_20D_Low + Bullish FVG1); Minervini_Trend_Basic=0; Priority_Score=65; pullback T1 RR≈2.2x &lt; BUY gate 2.5.
- 2026-09-07 — Scenario plan (PB_STRUCT, not Close-anchored ATR_FALLBACK): Entry zone HK$5.86–5.93; Entry ref ≈5.90; Stop **5.56** (MA20@5.80 − 0.5 ATR); Ladder 6.65 → 8.06 → 8.25 (targets re-sorted ascending); Conviction MEDIUM; Earnings UNKNOWN.
- 2026-09-07 — Phase 8 GEMINI HANDOFF emitted with contract fields (STOP TYPE / STOP ANCHOR / SCENARIO ENTRY / EARNINGS / RS_SCORE=23.44); technical VERDICT locked for downstream.
- 2026-09-07 — Trade Entry CSV written: `/workspace/hk-swing-setup/output/run-20260907-2346/2616_TradeEntry.csv`
- 2026-09-07 — Justin asked to send Handoff to Story Search → done; Story Search returned 2616 基石藥業 narrative, VERDICT stayed STALK; catalysts noted: (1) 9/7 Stock Connect effective; (2) ~Oct FDA 1L NSCLC Phase III protocol discussion.
- 2026-09-07 — Justin approved Fusion; technical INPUT + Story narrative forwarded to Fusion Formatter; Fusion delivered OUTPUT①+② to Justin, VERDICT STALK / stop $5.56; infographic pending Justin layout×style choice.
- Standing rule (from skills/profile): pullback entries must use PB_STRUCT re-anchor; never publish ATR_FALLBACK as pullback stop; Action_Refined is starting point only; STOP INVALID blocks any entry plan.
- Fleet rule (shared 2026-09-08 via 總指揮): hybrid verification live — high-stakes Swing/Story/Fusion outputs should go through Work Verifier before Justin treats as final.

## Live snapshot
- Agent-own durable memory folder: no profile.md / log facts recorded yet (empty agent memory at snapshot time).
- Routines: none.
- Last completed analysis artifact: run-20260907-2346 / 2616 only.
- Pipeline status for 2616 (as of last known agent pings 2026-09-07): Setup ✅ → Story ✅ → Fusion report ✅ → Wait Justin for infographic layout×style; no newer CSV run processed by this bot since then.
- Shared user facts relevant to this bot (not agent-owned): HK/finance briefs prefer baoyu-infographic stack; Kami for print/PDF; Work Verifier path as above.
- No connectors required for core ONE JOB (local CSV on shared workspace).
- Pending confirms: none from this bot’s side (no open user questions; Fusion infographic layout is Fusion’s wait, not ours).

## Secrets
- No API tokens, passwords, or session cookies stored by this agent.
- Placeholders only if ever needed: `[REDACTED:broker_api]`, `[REDACTED:sheets_token]`, `[REDACTED:mcp_auth]` — none currently held.
