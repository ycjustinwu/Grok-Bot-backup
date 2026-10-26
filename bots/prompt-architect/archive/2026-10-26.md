# Prompt Architect — durable memory snapshot
- Agent: Prompt Architect
- Agent id: cfe4ca9b-b60f-49d3-bd0d-454c269f4388
- Server id: 2410922
- Snapshot time: 2026-10-03 20:09 HKT (UTC+8)
- Requested by: 记忆管家 (full fleet memory backup)
- Sources: profile.json, settings.json, memory/profile.md, memory/log/2026-09.md, memory/USAGE_GATE.md, this agent's conversation through ticket close. No secrets copied.

## Identity
- Name: Prompt Architect (named by user)
- Title: (empty)
- Avatar: hex / yellow
- Harness: temporal
- User: Justin Wu (Asia/Hong_Kong)
- Coordinator: 總指揮 (id 7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4) — live profile writes go through 總指揮, not this bot
- Partners: dr eggbot (drafts new bots under the same gate); Work Verifier (id 037de516-dbc1-4565-a127-5dbb0f691729, independent QA); Self Improver (post-deploy corrections)

### ONE JOB
When given a raw prompt (paste or `/workspace/raw_prompts/`): produce a Job Description + modular skills + docs that pass harness-bot-standard.

### 3-TIER OUTPUT
1. JOB DESCRIPTION (<400 words) — ONE_JOB, ANTI_JOBS, folders, skill index, VERIFY, handoff → `job_description.txt`
2. SKILLS — each ends with a VERIFY checklist → `/workspace/refactored_[bot]/skills/*.md`
3. DOCS — static reference → `/workspace/refactored_[bot]/docs/*.md`

Also write a chat summary with copy-paste blocks. Batch: `/workspace/raw_prompts/` → `/workspace/refactored_output/`.

### CREATION GATE
Refuse to mark done if any harness gate is missing. High-stakes bots must name Work Verifier in handoff when appropriate.

### VERIFY
Confirm `job_description.txt` and skill files exist on disk; spot-check ANTI_JOBS + VERIFY sections present.

### ANTI-JOBS
- Do not invent domain facts not in the source prompt.
- Do not CreateAgent / overwrite live profiles unless Justin asks (hand to 總指揮).
- Do not run Self Improver’s weekly reflection.
- Do not leave procedures only in docs — procedures belong in skills.

### Settings
- notifyOnAgentUpdates: true
- hidden_from_sidebar: not set
- Routines: none

## Historical decisions
User profile (2026-09-07, from memory/profile.md):
- Justin is a Hong Kong senior financial practitioner (12+ years) specializing in structured products (Accumulator/ELN), derivatives, and cryptocurrency.
- Manages about 5M HKD (BOC HK, 致富證券). Tools: Bloomberg Terminal, TradingView Premium, Excel Advanced, Word, openclaw, Perplexity, Grok bots; Google ecosystem (Gemini primary).
- Hong Kong high-net-worth family (2 adults, 2 boys aged 9 and 12). Values efficiency. Travel preference: food, deep experiences, smooth logistics.
- Husband who values ritual and quality time with his wife; preparing both sons for British boarding school (critical thinking, international outlook, moderate financial literacy).
- Devices: Samsung S26+ and MacBook Air.
- Not for coding. Prefers non-coding tools for finance, decisions, and family planning (Matt Pocock productivity skills, baoyu-design) over coding/engineering suites like gstack.

Work log (2026-09-07, from memory/log/2026-09.md):
- visual-director skill (Propose → Audit → Execute). Decision: skill only, no dedicated Visual Director bot. Package: `/workspace/refactored_visual_director/`. Any bot can invoke it even if slash autocomplete does not list it.
- sketchnote-infographic skill (cream-paper educational sketchnote). Package: `/workspace/refactored_sketchnote_infographic/`.
- youtube-detailed-summary skill (繁體中文 finance/tech, 極詳細摘要). Package: `/workspace/refactored_youtube_detailed_summary/`. No YouTube connector; transcripts or attachments required.
- Bot 港股收市簡報 with skills hk-after-close-brief, hk-unusual-movers, hk-catalyst-research, hk-sector-rotation, hk-market-alerts. Package: `/workspace/refactored_hk_after_close_brief/`. Weekday auto-run at 18:00 HKT despite missing HKEX marketplace connectors.
- Bot Story Search with story-search-report, story-handoff-parse, story-theme-match, story-web-search, story-narrative-validate. Package: `/workspace/refactored_story_search/`. Upstream 港股 Swing Setup; downstream Fusion Formatter.
- Bot Fusion Formatter with fusion-bridge, fusion-ingest, fusion-report, fusion-infographic-prompt, fusion-swing-infographic. Package: `/workspace/refactored_fusion_formatter/`. Pipeline: Swing Setup → Story Search → Fusion → Fusion Swing Infographic → baoyu-infographic (16:9). Fusion report ≤500 字 繁體中文.
- fusion-swing-infographic skill. Examples (Henlius / Hinge Health / Coty) under `refactored_fusion_formatter/docs/infographic-examples/`.
- Bot 港美股 Swing Setup (v4.7 Scenario-Anchored Stop / PB_STRUCT) with hk-swing-trade-analysis, hk-swing-csv-validate, hk-swing-setup-playbook, hk-swing-scenario-stop, extended for HK and US. Package: `/workspace/refactored_swing_setup_dual/`. 港股 Swing Setup kept as HK-focused twin on the same skills.
- Swing → Story Search handoff contract: labeled GEMINI HANDOFF including MARKET, RS_SCORE, v4.7 STOP TYPE/ANCHOR/SCENARIO ENTRY. Story Handoff Parse requires those fields and handles UNKNOWN earnings.
- Bot 旅行計劃助手 with travel-plan-architect, travel-consultative-intake, travel-hk-safety-net, travel-logistics-links, travel-itinerary-table. Package: `/workspace/refactored_travel_planner/`.
- Bot 全富決策副手 with financial-life-deputy, decision-mode-switch, live-search-mandates, second-order-reasoning, deputy-output-modes. Package: `/workspace/refactored_decision_deputy/`.
- StockCharts breadth → 4 skills (breadth-daily-report, breadth-chart-capture, breadth-ocr-verify, fred-vix-term-structure). Package: `/workspace/refactored_breadth_monitor/`. Charts in `/workspace/breadth/`. FRED VIX uses public series pages for VIXCLS and VXVCLS, no API key, pair VIX/VXV on the same date only.
- Stockbee T2108 → 4 skills (stockbee-t2108-monitor, stockbee-t2108-fetch, stockbee-t2108-excel, telegram-xlsx-send). Package: `/workspace/refactored_stockbee_t2108/`. Telegram delivery uses env `[REDACTED:TELEGRAM_BOT_TOKEN]` only; Grok attach by default.
- Market Awareness Orchestrator (id e4e8d80f-26c5-48c1-bd11-f56c0a9cc077), Regime Scoring v6.3 at packaging time. Package: `/workspace/refactored_market_awareness/`. Skills: market-awareness-orchestrator, regime-data-ingest, regime-pillar-a, regime-pillar-b, regime-layer-context, regime-modifiers-and-stance, regime-daily-report. Inputs: TradingView ETF CSV + Stockbee T2108 + StockCharts breadth/FRED.
- Bot US Market Daily Brief. Package: `/workspace/refactored_us_market_daily_brief/`. Skills: us-market-daily-brief, us-etf-theme-scan, us-abnormal-volume, us-focus-catalyst, us-rotation-structure.
- Installed baoyu-design (JimLiu) at `/home/box/agent-data/workflows/baoyu-design/` with references/grok.md. HTML-first; prefer baoyu-infographic for finance boards and kami for print. Package mirror: `/workspace/refactored_baoyu_design/`.
- Installed Matt Pocock skills (mattpocock/skills@3cca18b): grill-me, grilling, handoff, teach, to-questionnaire, wait-what, writing-for-agents. Mirror: `/workspace/refactored_mattpocock_productivity/`.
- gstack 1.81.0.0 at `/home/box/.gstack/repos/gstack`. `./setup` was Auto-review blocked; manual install. Upgrade via gstack-upgrade skill. Package: `/workspace/refactored_gstack_upgrade/`. Justin deprioritized gstack for daily finance/family work.
- Installed diagram-design (cathrynlavery/diagram-design v2.6) with EXTEND.md Justin defaults. Package: `/workspace/refactored_diagram_design/`. Editorial HTML/SVG process diagrams; prefer baoyu-infographic for finance boards and baoyu-design for decks.
- Toolkit priority: Matt Pocock grill-me/grilling, to-questionnaire, wait-what, handoff for decisions; baoyu-design for decks; baoyu-infographic for market one-pagers; diagram-design for process diagrams; leave gstack unused day to day.

Standing rules after the September log:
- (2026-09-20) Usage gate, Justin locked, all bots. Canon also in this agent's `memory/USAGE_GATE.md`. Before browser, multi-source research, retry, extra skill load, or subagent: reuse a fresh artifact if one exists; if the same approach failed twice, stop and report; if no tools are needed, chat only. Prefer a connector or API over clicking a site. Do not create more bots or routines to save usage.
- (2026-09-08, fleet via 總指揮) Hybrid verification: every bot/skill includes a VERIFY step (harness-bot-standard + work-verify). Work Verifier does an independent second pass on high-stakes outputs (Swing Setup, Story, Fusion, Regime, Daily Briefs).
- (2026-09-24 ticket, closed 2026-10-03 by 總指揮) TC-20260924-08. ETF Relative Strength Dashboard is an overlay only for Market Awareness Orchestrator and US Swing Scanner. Do not change regime scoring math or invent RS numbers. Sheet file id `1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ`. Local copy `/workspace/etf-rs/ETF_Relative_Strength_Dashboard.xlsx`. RS actual = 30d PERCENTRANK of (ETF/VOO), not “beat VOO by X%”. Skills written to disk: etf-rs-overlay-ingest, etf-rs-theme-tilt, us-swing-sector-wind (plus sector-proxy-map.md). Draft package: `/workspace/refactored_etf_rs_overlay/`. 總指揮 applied UpdateAgent on Market Awareness and US Swing Scanner. Prompt Architect did not CreateAgent. Ticket closed; no further Prompt Architect action.

## Live snapshot
- Routines: none
- This bot does not own a production market job. It writes specs and shared skills; 總指揮 applies live job descriptions.
- Skill files confirmed on disk for the last ticket: `/home/box/agent-data/workflows/etf-rs-overlay-ingest/SKILL.md`, `etf-rs-theme-tilt/SKILL.md`, `us-swing-sector-wind/SKILL.md`.
- Refactored packages present under `/workspace/`: refactored_baoyu_design, refactored_breadth_monitor, refactored_decision_deputy, refactored_diagram_design, refactored_etf_rs_overlay, refactored_fusion_formatter, refactored_gstack_upgrade, refactored_hk_after_close_brief, refactored_hk_swing_setup, refactored_market_awareness, refactored_mattpocock_productivity, refactored_sketchnote_infographic, refactored_stockbee_t2108, refactored_story_search, refactored_swing_setup_dual, refactored_travel_planner, refactored_us_market_daily_brief, refactored_visual_director, refactored_youtube_detailed_summary.
- Open work: none. TC-20260924-08 closed.
- Pending confirms: none. (During apply, skill-write via the state API returned “brain docs snapshot was cut short”; files were already on disk. 總指揮 later confirmed the three ETF RS skills live and closed the ticket.)

## Secrets
- No API keys or tokens are stored in this agent's profile, settings, or memory files.
- Telegram delivery for the Stockbee skill uses env `[REDACTED:TELEGRAM_BOT_TOKEN]` only. Value not recorded here.
- Google connector credentials: `[REDACTED:google-oauth]` (connector-owned; not copied into this agent).
- Drive file id for the ETF RS sheet is a resource locator, not a secret.
