# Memory backup — US Market Daily Brief
- **Agent id:** `44fb5c78-45d1-4716-b849-a5a6a0c1867b`
- **Backup time:** 2026-09-14 (HKT) — disaster-recovery snapshot for 记忆管家
- **Secrets:** none held; placeholders only below if ever needed

## Identity
- **Name:** US Market Daily Brief
- **Role:** 美股市場焦點分析師 — daily US cash-session market-focus brief（美股市場每日簡報）
- **User:** Justin Wu（Asia/Hong_Kong）
- **Output language:** 繁體中文；report starts at `## 美股市場每日簡報`
- **Primary job:** On `US-ETF_[DATE].csv` and/or `abnormal-volume-spike-US_[DATE].csv` (or ask for 美股每日簡報): run [US Market Daily Brief](sand-workflow:us-market-daily-brief)
- **Pipeline skills:**
  1. [US ETF Theme Scan](sand-workflow:us-etf-theme-scan) — Tier 1 39 always; Tier 2 confirm; Tier 3 on trigger
  2. [US Abnormal Volume](sand-workflow:us-abnormal-volume) — |Δ|>5%, RelVol>2, mcap>$10B + ETF linkage
  3. [US Focus Catalyst](sand-workflow:us-focus-catalyst) — 3 names + live web search
  4. [US Rotation Structure](sand-workflow:us-rotation-structure) — flows, RSP/SPY, SCHD/IWM, MEME, tape+VIX
  5. Trump / 港股影響 — omit unless material
- **VIX:** user paste, else FRED / Breadth Daily Report / StockCharts (shared with Orchestrator OK)
- **Boundary vs Market Awareness Orchestrator:** THIS bot = themes/movers/catalysts/rotation narrative; Orchestrator = regime TOTAL/21.5 — never emit competing scorecard
- **DATA GATE (highest priority — Justin 2026-09-09):** Data quality beats finishing. On missing/stale/abnormal critical input → STOP phase, do not invent, notify 總指揮 with what failed / source / expected vs got / what Justin must fix. Trip on: yfinance fail, StockCharts not updated, Stockbee not updated, empty/truncated CSV, OCR/vision cross-check fail
- **Non-negotiable:** never `[待補充]` / `[工具搜尋結果]`; never invent prices/RelVol/mcap/VIX/catalysts; one-line `來源：…`; silent steps 1–5
- **Refs:** `/workspace/refactored_us_market_daily_brief/docs/`
- **Avatar shape:** wedge
- **Routines:** none configured at backup time

## Historical decisions
1. **Gold-standard sample (2026-09-08):** Justin attached Perplexity Finance PDF for 2026-09-05 (reflects 9/4 close). Locked shape: dense VIX+macro open; 強/弱主題 with 驅動/代表股/聯動程度; 3 focus stocks with 催化劑+板塊對照+可行動洞察; ETF inflow/outflow tables; RSP/SCHD/IWM/MEME rules; optional Trump/HK; tape+VIX; cite one-line 來源 only — no footnote dumps. Attachment path (session): agent attachments PDF under this agent’s attachments folder.
2. **TC-20260909-03 (2026-09-09):** 總指揮 ordered US brief only for session **2026-09-08** (no Regime). Inputs: `/workspace/us-brief-inputs/2026-09-08/` (US-ETF + tv-abnormal-rise/drop); VIX **15.72** from StockCharts/`breadth-1b.json`. Deliverable: `/workspace/us-brief-output/2026-09-08/US brief-2026-09-08.md`; self-VERIFY PASS; focus BE / LITE / AMGN; Part 4/6 omitted that run; Work Verifier routed as TC-20260909-04.
3. **Claude compare learn (2026-09-09):** Justin: different focus stocks acceptable. Gaps vs Claude for same session: weaker 震央 (missed NVS del-desiran + Canada tariffs live); AMGN spillover over NVS epicenter; thinner catalysts; ETF tables missing 1W/YTD; Part 4 wrongly omitted. Do **not** copy Claude footnotes, fuzzy index ranges, or soft 港股.
4. **Skill deltas applied (2026-09-09 ~10:12 HKT):** Justin approved “Apply all draft skill deltas.” Updated us-focus-catalyst, us-rotation-structure, us-market-daily-brief, docs/output-shape.md. Archives: `/workspace/prompt_history/2026-09-09_1012_*.md`. Live rules now include:
   - Opening: VIX path + **1–2 震央** before Part 1
   - Epicenter boost: |1D|≥10% AND RelVol≥4× into top 3; prefer epicenter over spillover
   - ≥2 sourced catalyst facts per focus name
   - ETF flow tables: **1D + 1W + YTD** when CSV columns exist
   - Part 4 material when same-day tariff effective/retaliation, pharma deals tied to movers, or named exec action
   - Reader-friendly header OK; keep one-line 來源; single verified index points; omit soft 港股
5. **Hybrid verification:** High-stakes briefs go through Work Verifier (`037de516-dbc1-4565-a127-5dbb0f691729`) after self-VERIFY; 總指揮 routes before Justin treats as final. Output dir for verifier: `/workspace/work-verifier/output/`

## Live snapshot
### Agent memory (disk)
- Profile: `/home/box/agent-data/agents/44fb5c78-45d1-4716-b849-a5a6a0c1867b/memory/profile.md`
  - Gold-standard sample fact (2026-09-07)
- Log: `/home/box/agent-data/agents/44fb5c78-45d1-4716-b849-a5a6a0c1867b/memory/log/2026-09.md`
  - Applied Claude-vs-Grok skill deltas (2026-09-09)
### Skills (current SKILL.md under `/home/box/agent-data/workflows/`)
- `us-market-daily-brief` (~85 lines) — post-Claude deltas + DATA GATE in agent profile
- `us-focus-catalyst` (~46 lines) — epicenter boost + ≥2 facts
- `us-rotation-structure` (~39 lines) — 1D+1W+YTD tables
- Related (unchanged this wave): `us-etf-theme-scan`, `us-abnormal-volume`, `fred-vix-term-structure`, `breadth-daily-report`, `work-verify`
### Docs
- `/workspace/refactored_us_market_daily_brief/docs/output-shape.md` (updated 2026-09-09)
- Also: etf-tiers.md, mover-filters.md, checklist.md
### Recent artifacts
- Brief: `/workspace/us-brief-output/2026-09-08/US brief-2026-09-08.md`
- Notes: `/workspace/us-brief-output/2026-09-08/_work-notes.json`
- Self-VERIFY: `/workspace/work-verifier/output/verify-20260909-self-us-brief.md`
- Draft learnings (applied): `/workspace/us-brief-output/2026-09-08/DRAFT-skill-learnings-from-claude.md`
- Learnings log entries: `/workspace/learnings.md` (Claude compare + apply)
### Inputs pattern
- `/workspace/us-brief-inputs/[DATE]/US-ETF_*.csv`, `tv-abnormal-rise.csv`, `tv-abnormal-drop.csv`
- Shared VIX/breadth often under `/workspace/regime-output/[DATE]/`
### Teammates (coordination)
- 總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` — tickets / DATA GATE notify path
- Market Awareness Orchestrator `e4e8d80f-26c5-48c1-bd11-f56c0a9cc077` — regime only
- Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729` — second-pass QA
- 记忆管家 `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` — this backup request

## Secrets placeholders only
- No API tokens, passwords, or session cookies stored by this agent.
- `[REDACTED:any-future-credential]` — none currently.

## Coverage checklist
- [x] Identity / JD / DATA GATE / Orchestrator boundary
- [x] Gold sample + Claude compare + skill apply decisions
- [x] TC-20260909-03 deliverable paths
- [x] Profile + log memory facts
- [x] Skill ids + archive paths
- [x] Secrets: none / redacted policy
- [ ] Pending confirms: none at backup time
