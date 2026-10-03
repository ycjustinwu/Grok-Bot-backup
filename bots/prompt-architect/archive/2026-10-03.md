# Prompt Architect — durable memory snapshot
- Agent: Prompt Architect
- Agent id: cfe4ca9b-b60f-49d3-bd0d-454c269f4388
- ServerId: 2410922
- Written: 2026-09-14 HKT
- Path: /workspace/2410922-memory-backup.md

## Identity

- Name: Prompt Architect
- Title: Prompt Architect (profile.json title empty; chat title is Prompt Architect)
- Avatar: hex / yellow
- Named by: user
- Harness: box
- ONE JOB: When given a raw prompt (paste or `/workspace/raw_prompts/`): produce Job Description + modular skills + docs that pass harness-bot-standard.
- 3-tier output: job_description.txt (<400 words, ONE_JOB/ANTI_JOBS/folders/skill index/VERIFY/handoff) + `/workspace/refactored_[bot]/skills/*.md` (each ends VERIFY) + `/workspace/refactored_[bot]/docs/*.md`
- CREATION GATE: refuse done if harness gate missing; high-stakes bots name Work Verifier in handoff when appropriate
- ANTI-JOBS: do not invent domain facts not in source; do not CreateAgent / overwrite live profiles unless Justin asks (hand to 總指揮); do not run Self Improver weekly reflection; procedures belong in skills not docs-only
- PARTNERS: dr eggbot (drafts new bots); Work Verifier (independent QA after production); Self Improver (post-deploy corrections); 總指揮 applies live profile updates
- User: Justin Wu (HK senior finance, structured products / derivatives / crypto; family 2 adults + boys ~9 and ~12; timezone Asia/Hong_Kong)

## Historical decisions

### 2026-09-07 — fleet packages (this agent built)

- Visual Director skill only (no dedicated bot): Propose → Audit → Execute; package `refactored_visual_director/`
- Sketchnote Infographic skill; package `refactored_sketchnote_infographic/`
- YouTube Detailed Summary skill (繁體中文; no YouTube connector — transcript/attachment required); package `refactored_youtube_detailed_summary/`
- Bot 港股收市簡報 + 5 skills; weekday 18:00 HKT routine on that bot; no HKEX marketplace connector; package `refactored_hk_after_close_brief/`
- Dual 港股/美股 Swing Setup skills (hk-swing-*); GEMINI HANDOFF labeled contract; package `refactored_swing_setup_dual/`
- Story Search bot + story-* skills; package `refactored_story_search/`
- Fusion Formatter bot + fusion-* + fusion-swing-infographic; package `refactored_fusion_formatter/`
- Pipeline: CSV → Swing Setup → GEMINI HANDOFF → Story Search → Fusion → Infographic
- 旅行計劃助手 + travel-* skills; package `refactored_travel_planner/`
- 全富決策副手 + financial-life-deputy stack; package `refactored_decision_deputy/`
- Breadth skills (breadth-daily-report, breadth-chart-capture, breadth-ocr-verify, fred-vix-term-structure); FRED public pages no API key; same-date VIXCLS/VXVCLS only; package `refactored_breadth_monitor/`
- Stockbee T2108 skills; Telegram uses env `[REDACTED:TELEGRAM_BOT_TOKEN]` only (never in skill text); package `refactored_stockbee_t2108/`
- Market Awareness Orchestrator bot id `e4e8d80f-26c5-48c1-bd11-f56c0a9cc077`; Regime Scoring v6.3; package `refactored_market_awareness/`
- US Market Daily Brief bot id `44fb5c78-45d1-4716-b849-a5a6a0c1867b`; package `refactored_us_market_daily_brief/`

### 2026-09-07 — third-party skills Justin asked to install

- baoyu-design (JimLiu) at `/home/box/agent-data/workflows/baoyu-design/` + `references/grok.md`; HTML-first, optional PPTX/PDF/MP4
- Matt Pocock productivity @3cca18b: grill-me, grilling, handoff, teach, to-questionnaire, wait-what, writing-for-agents
- gstack-upgrade skill + full gstack 1.81.0.0 at `/home/box/.gstack/repos/gstack` (symlinked `~/.claude/skills/gstack` and `~/.cursor/skills/gstack`); bun install + build:gates done; official `./setup` Auto-review blocked (manual equivalent)
- Justin assessed: **non-coding sitting** — prioritize grill-me/grilling + baoyu-design/infographic + diagram-design; **leave gstack unused** for daily finance/family
- OpenWhispr: reviewed, Justin declined install (`no`)
- diagram-design (cathrynlavery v2.6) installed with EXTEND.md Justin defaults; skip UML/DB unless asked

### 2026-09-11 — Work Verifier refine

- 總指揮 TC-20260911-01b: standby to refactor Work Verifier JD/skills from `/workspace/work-verifier/refine-20260911/draft/`
- Later CANCELLED/DONE — 總指揮 installed drafts; Prompt Architect refactor not needed; stayed quiet
- Hybrid verification live (learned via 總指揮): harness-bot-standard + work-verify; Work Verifier bot `037de516-dbc1-4565-a127-5dbb0f691729`

### Creation-gate evolution (profile 2026-09-11)

- Do **not** CreateAgent / overwrite live profiles unless Justin asks — hand to 總指揮
- Historical note: this agent DID CreateAgent earlier (Market Awareness Orchestrator, US Market Daily Brief) on 2026-09-07 when Justin asked explicitly. New default is handoff to 總指揮 unless Justin asks this bot.

## Live snapshot

- Memory profile.md: Justin identity, devices (S26+, MacBook Air), ~5M HKD, BOC HK / 致富證券, Bloomberg/TradingView/Excel, Google/Gemini, non-coding toolkit preference
- Log: 2026-09.md (visual through diagram-design + toolkit)
- Routines owned by this agent: none (港股收市簡報 18:00 HKT lives on that bot)
- No pending user asks; last user-visible work: diagram-design install (2026-09-08)
- Agent-to-agent: 记忆管家 DR backup (this file)
- Packages still expected under `/workspace/refactored_*` as listed above
- Skills global at `/home/box/agent-data/workflows/<id>/`

## Secrets placeholders only

- `[REDACTED:TELEGRAM_BOT_TOKEN]` — T2108 Excel Telegram send; skill must use env, never embed token (source prompt once contained a token; redacted and rotate if still live)
- `[REDACTED:FRED_API_KEY]` — not used; FRED public HTML pages preferred
- No other credentials held in this agent's memory

## Coverage

- Identity: profile.json + current ONE_JOB/ANTI_JOBS
- Historical: all agent log facts 2026-09-07 through 2026-09-11 Work Verifier cancel
- Live: no open Prompt Architect tickets
- Secrets: placeholders only
- Pending confirms: none
