# Memory disaster-recovery snapshot — 港股 Swing Setup
- Agent id: 28b5646e-bfc2-440b-8a63-b68440a1de4b
- Server id: 2410941
- Snapshot written: 2026-10-03 (Asia/Hong_Kong)
- Writer: 港股 Swing Setup (self)

## Identity
- Name: 港股 Swing Setup
- Role: 港股 Swing Trade Setup 分析師（v4.7.1-HK）
- ONE JOB: 分析港股 Python CSV → Setup/止損驗證 → Trade Entry CSV → 標籤版 GEMINI HANDOFF 給 投資敘事分析師
- Skills (shared with 美股 Swing Setup, market rules differ): Swing CSV Validate, Swing Setup Playbook, Swing Scenario Stop, Swing Trade Analysis
- Skill files: `/home/box/agent-data/workflows/hk-swing-{csv-validate,setup-playbook,scenario-stop,trade-analysis}/SKILL.md`
- Market rules: RS = Stock% − HSI%; ADR = 20-day; prices HK$; Earnings missing → UNKNOWN (not CLEAR; never BUY)
- IO in: `/workspace/hk-swing-scanner/output/run-*/`
- IO out: `/workspace/hk-swing-setup/output/run-*/`
- Compatible scripts: HK_swing_v4.5.3_final / HK_swing_v4.6.1_Colab (Tight Zone v2.1)
- Downstream: 投資敘事分析師 (id 3f297e81-4667-4dae-b517-b4f7ddee3537) → Fusion Formatter (id c45141fc-c050-49e2-9635-dca556a0cc1f)
- Sibling (US only): 美股 Swing Setup (id 747b3374-ada7-44d7-8cf4-73098b1c10af) — now described as v4.8-US; shared skills currently carry v4.7.1-HK logic
- Upstream scanner: HK Swing Scanner (id 162f41b3-b93f-4d05-abdf-07b938f6ab56)
- Liaison: 總指揮 (id 7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4)
- High-stakes QA: Work Verifier (id 037de516-dbc1-4565-a127-5dbb0f691729)
- User: Justin Wu; timezone Asia/Hong_Kong
- ANTI-JOBS: 不分析美股 CSV；禁止捏造；STOP INVALID 不得發布；從不使用名稱「港美股 Swing Setup」；不構成投資建議
- Avatar: hex / gray; namedBy user; harness box
- Routines: none

## Historical decisions
- 2026-09-07 — First live job (via 總指揮): analyze **only 2616** from `/workspace/hk-swing-scanner/output/run-20260907-2346/2616_SwingAnalysis.csv`.
- 2026-09-07 — VERDICT **STALK** (override Python WATCH). Hidden Pullback Setup B; Trend_Basic=0; Score 65; pullback T1 RR≈2.2x. Entry HK$5.86–5.93; Stop **5.56** PB_STRUCT (MA20); Ladder 6.65 → 8.06 → 8.25. Earnings UNKNOWN. Conviction MEDIUM. RS 23.44.
- 2026-09-07 — Trade Entry: `/workspace/hk-swing-setup/output/run-20260907-2346/2616_TradeEntry.csv`
- 2026-09-07 — Justin sent Handoff to Story Search (基石藥業). Catalysts noted: 9/7 Stock Connect; ~Oct FDA 1L NSCLC Phase III. VERDICT stayed STALK.
- 2026-09-07 — Justin approved Fusion. Fusion delivered OUTPUT①+②; stop $5.56; infographic waited on Justin layout×style. No later close-out recorded here.
- 2026-09-14 — Prior fleet backup written to `/workspace/2410941-memory-backup.md` (48 lines) for 记忆管家.
- 2026-09-16 — Justin pasted prompt **v4.7.1-HK** (approved fixes 1–8 + TZ v2.1). Skills rewritten and profile bumped from v4.7-HK to v4.7.1-HK.
- v4.7.1 rules now in force:
  1. AVOID = Minervini_Trend_Basic=0 AND RS_Score<0 (not OR)
  2. Core vs Optional columns; missing Optional continues with a note; missing Core stops
  3. Three RR systems kept separate; RR_Ratio_Best ≠ Swing-Low RR and is not sole BUY basis
  4. Priority Pillar 4 uses RR_Zone_Best (≥3 +20 / ≥2.5 +10 / ≥2.0 +5); UNKNOWN earnings −5
  5. BUY/STALK/WATCH/PASS gates aligned to Python; UNKNOWN never BUY
  6. Red Flag 5: (Res20−Close)/Close×100 < ADR_Pct × 0.5 (percent, not ×0.5%)
  7. Setup C: if TZ dead, do not use stale Zone Low; fall back Swing_Low_10D−0.5 ATR or ATR_FALLBACK
  8. Paired RR (scenario for pullback) is the decision RR
  - TZ v2.1: vol < 0.85×Vol_Avg_20; range ≤ 1.20×ADR; Active 2–10 days; max 2 non-tight exemptions; Minervini OR Soft Trend
- 2026-09-20 — Standing usage gate from Justin via 總指揮: reuse fresh artifacts; stop after the same approach fails twice; chat-only if no tools needed; prefer connector/API over clicking; do not create bots or routines to save usage. Canon: `/workspace/fleet-policies/USAGE_GATE.md`

## Live snapshot
- Prompt version in profile and four skills: **v4.7.1-HK** (updated 2026-09-16).
- Last analyzed ticker: 2616 only. No newer HK CSV run processed by this bot after run-20260907-2346.
- Agent durable memory: thin. A one-line note was written to `.../memory/profile.md` on 2026-09-16; UpdateState memory write failed that turn (brain snapshot cut short). This file is the fuller record.
- Open user questions: none. Fusion infographic layout was Fusion's wait, not this bot's.
- No connectors required for the core job (local CSV on shared workspace).

## Secrets
- None held. No API tokens, passwords, or session cookies.
- Placeholders only: `[REDACTED:broker_api]`, `[REDACTED:sheets_token]`, `[REDACTED:mcp_auth]` — not in use.

## Pending confirms
- None.
