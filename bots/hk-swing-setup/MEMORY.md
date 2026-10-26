# Memory disaster-recovery snapshot — 港股 Swing Setup
- Agent id: 28b5646e-bfc2-440b-8a63-b68440a1de4b
- Server id: 2410941
- Snapshot written: 2026-10-26 ~20:45 HKT
- Writer: 港股 Swing Setup (self)

## Identity
- Name: 港股 Swing Setup
- Role: 港股 Swing Trade Setup 分析師（v4.7.1-HK）
- ONE JOB: 分析上傳的港股 Python CSV → Setup/止損驗證 → Trade Entry CSV → 標籤版 GEMINI HANDOFF 給 投資敘事分析師
- Skills (shared with 美股 Swing Setup; market rules differ): Swing CSV Validate · Setup Playbook · Scenario Stop · Trade Analysis
- Skill paths: `/home/box/agent-data/workflows/hk-swing-{csv-validate,setup-playbook,scenario-stop,trade-analysis}/SKILL.md`
- Market: 🇭🇰 RS = Stock% − HSI%; ADR = 20-day; Earnings missing = UNKNOWN (not CLEAR; never BUY)
- IO in: `/workspace/hk-swing-scanner/output/run-*/`
- IO out: `/workspace/hk-swing-setup/output/run-*/`
- Scripts: HK_swing_v4.5.3_final / HK_swing_v4.6.1_Colab (TZ v2.1)
- Downstream partners: 投資敘事分析師 (id 3f297e81-4667-4dae-b517-b4f7ddee3537) → Fusion Formatter (id c45141fc-c050-49e2-9635-dca556a0cc1f)
- Upstream: HK Swing Scanner (id 162f41b3-b93f-4d05-abdf-07b938f6ab56)
- Sibling US-only: 美股 Swing Setup (id 747b3374-ada7-44d7-8cf4-73098b1c10af)
- Liaison: 總指揮 (id 7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4)
- QA: Work Verifier (id 037de516-dbc1-4565-a127-5dbb0f691729) — gated by Jev `needs_wv` / Justin (see locked rules)
- User: Justin Wu · Asia/Hong_Kong
- Avatar: hex / gray · harness box · namedBy user
- Routines: none

### ANTI-JOBS
- 不分析美股 CSV（轉 美股 Swing Setup）
- 禁止捏造；STOP INVALID 不得發布
- 從不使用名稱「港美股 Swing Setup」
- 不構成投資建議

### Jev (B+C) — TypeSafe (in profile)
- Skill: jev-fleet-decisions · Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md` · thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `[REDACTED:TYPESAFE_API_KEY]` via `process.env.TYPESAFE_API_KEY` only — never paste
- Log: `/workspace/typesafe-jev/logs/` when practical
- B pre-task: `pre_task` pack `act|evidence_enough|escalate|cost_tier` before grind; mid-task only on forks
- C exit: `exit` → `ready_for_justin|needs_wv|conflict|soft_ambition`; WV via 總指揮 only when C says needs_wv / high-stakes path
- Rules: Jev gates; this bot does the work; never invent tickers/prices via Jev; never auto-send/auto-trade; Front-door A OFF

## Historical decisions / locked rules
- 2026-09-07 — First live: **2616 only** from `/workspace/hk-swing-scanner/output/run-20260907-2346/2616_SwingAnalysis.csv`
- 2026-09-07 — VERDICT **STALK** (override Python WATCH). Hidden Pullback B; Trend_Basic=0; Score 65; Entry HK$5.86–5.93; Stop **5.56** PB_STRUCT(MA20); Ladder 6.65→8.06→8.25; Earnings UNKNOWN; RS 23.44; Conviction MEDIUM
- 2026-09-07 — Trade Entry: `/workspace/hk-swing-setup/output/run-20260907-2346/2616_TradeEntry.csv`
- 2026-09-07 — Story Search (基石藥業) + Fusion OUTPUT①+② delivered; VERDICT stayed STALK; Fusion infographic waited Justin layout×style (no close-out recorded)
- 2026-09-14 / 2026-10-03 — Prior fleet backups for 记忆管家 (2410941 path and this agent-id path)
- 2026-09-16 — Prompt **v4.7.1-HK** locked into profile + four skills (fixes 1–8 + TZ v2.1):
  1. AVOID = Trend_Basic=0 **AND** RS_Score<0
  2. Core vs Optional columns
  3. Three RR systems separate; RR_Ratio_Best ≠ Swing-Low RR / not sole BUY basis
  4. Pillar4 = RR_Zone_Best; UNKNOWN earnings −5
  5. BUY/STALK/WATCH/PASS align Python; UNKNOWN never BUY
  6. Red Flag 5: (Res20−Close)/Close×100 < ADR_Pct × 0.5
  7. Setup C: TZ dead → no stale Zone Low; Swing_Low_10D−0.5ATR or ATR_FALLBACK
  8. Paired RR (Scenario for pullback) is decision RR
  - TZ v2.1: vol<0.85×Vol20; range≤1.20×ADR; Active 2–10d; ≤2 non-tight; Minervini OR Soft Trend
- 2026-09-20 — Usage gate (Justin via 總指揮): reuse fresh artifact; stop after same approach fails twice; chat-only if no tools; prefer connector/API; do not create bots/routines to save usage. Canon: `/workspace/fleet-policies/USAGE_GATE.md` (also copied under this agent memory folder)
- 2026-10-21 — WV policy (Justin via 總指揮): default WV pool = Regime + US Market Daily Brief + 港股收市簡報 only. **港股 Swing Setup / Story / Fusion use WV only if Jev `needs_wv` or Justin asks.** (Older hybrid-WV-everything note superseded for this bot.)
- Market Master sheet (fleet): id `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` for breadth/industry/ETF/Setup_Latest when needed

## Live snapshot
- Prompt/skills version: **v4.7.1-HK** (last skill rewrite 2026-09-16; still in force as of this snapshot)
- Last setup output folder present: `run-20260907-2346` only — no newer HK CSV run processed by this bot after 2616
- Open work: none
- Open user questions: none
- Routines: none
- Local memory files: `/home/box/agent-data/agents/28b5646e-bfc2-440b-8a63-b68440a1de4b/memory/{profile.md,USAGE_GATE.md}`
- Connectors: not required for core ONE JOB (local CSV)

## Secrets
- None held as plaintext.
- Placeholders: `[REDACTED:TYPESAFE_API_KEY]`, `[REDACTED:broker_api]`, `[REDACTED:sheets_token]`, `[REDACTED:mcp_auth]`

## Pending confirms
- None (list only; not acted on).
