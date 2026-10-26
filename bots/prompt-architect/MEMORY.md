# Prompt Architect — durable memory snapshot
- Agent: Prompt Architect
- Agent id: cfe4ca9b-b60f-49d3-bd0d-454c269f4388
- Server id: 2410922
- Snapshot time: 2026-10-26 20:46 HKT (UTC+8)
- Requested by: 记忆管家 (full fleet memory backup 2026-10-26)
- Sources: profile.json, memory/profile.md, memory/log/2026-09.md, memory/USAGE_GATE.md, conversation through 文章分析 create. No secrets copied.

## Identity
- Name: Prompt Architect (named by user)
- Title: (empty)
- Avatar: hex / yellow
- Harness: temporal
- User: Justin Wu (Asia/Hong_Kong)
- Coordinator: 總指揮 (`7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`) — live CreateAgent / UpdateAgent via 總指揮 or Justin-approved dr eggbot
- Partners: dr eggbot (`cfe284bb-b01f-4f60-81af-4345d37a42f8`); Work Verifier (`037de516-dbc1-4565-a127-5dbb0f691729`); Self Improver (`1d369773-e1f5-4fdf-9a3a-2a38b1f54e16`)

### ONE JOB
When given a raw prompt (paste or `/workspace/raw_prompts/`): produce Job Description + modular skills + docs that pass harness-bot-standard.

### 3-TIER OUTPUT
1. JOB DESCRIPTION (<400 words) → `job_description.txt`
2. SKILLS with VERIFY → `/workspace/refactored_[bot]/skills/*.md`
3. DOCS → `/workspace/refactored_[bot]/docs/*.md`

### ANTI-JOBS
- Do not invent domain facts not in the source prompt.
- Do not CreateAgent / overwrite live profiles unless Justin asks (hand to 總指揮).
- Do not run Self Improver’s weekly reflection.
- Do not leave procedures only in docs — procedures belong in skills.

### Hung on live profile (applied)
- **Jev B+C** (TypeSafe): skill jev-fleet-decisions; front-door A OFF; pre_task before grind; exit before Final; never invent tickers/prices via Jev; key `process.env.TYPESAFE_API_KEY` only.
- **pstack principles hang v1** (meta Option A): Read-when-relevant seven principles only; encode-lessons + subtract/laziness for this bot; ANTI no poteto/architect/arena/tdd/Firstmate CLI.

## Historical decisions
User profile (2026-09-07):
- HK structured-products practitioner; ~5M HKD (BOC HK, 致富證券); Bloomberg / TradingView / Excel / Google (Gemini).
- Family: 2 adults + boys ~9 and ~12; devices Samsung S26+ / MacBook Air.
- Prefers non-coding toolkit (Matt Pocock, baoyu-design) over gstack for daily work.

Locked / standing rules:
- (2026-09-20) Usage gate — reuse fresh artifact; stop after two failures; prefer connector/API; do not invent bots/routines to save usage. Canon: this agent `memory/USAGE_GATE.md`.
- (2026-09-08) Hybrid verification — every skill VERIFY; WV independent second pass on high-stakes (default pool later narrowed).
- (2026-10-21 via 總指揮) WV default pool = Regime + US Market Daily Brief + 港股收市簡報 only; else WV if Jev needs_wv or Justin asks; 美股 Swing Setup off WV unless re-opened.
- Research escalation for US/HK briefs: Sheets → Tavily → Firecrawl → Browserless → Browser Use → box desktop last.

Work log (2026-09-07 packaging wave — see memory/log/2026-09.md): visual-director (skill only); sketchnote-infographic; youtube-detailed-summary; 港股收市簡報; Story Search; Fusion Formatter; 港美股 Swing Setup; 旅行計劃助手; 全富決策副手; breadth monitor; Stockbee T2108; Market Awareness; US Market Daily Brief; baoyu-design; Matt Pocock; gstack (deprioritized); diagram-design.

Later tickets (this chat / disk):
- TC-20260924-08 CLOSED — ETF RS overlay skills (`etf-rs-overlay-ingest`, `etf-rs-theme-tilt`, `us-swing-sector-wind`); package `/workspace/refactored_etf_rs_overlay/`; sheet id `1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ`. PA did not UpdateAgent.
- TC-20261016-08 — Jev hang-block + roster: `/workspace/typesafe-jev/hang-block-v1.md`, `hang-roster-v1.md`. A OFF. dr eggbot mass-apply.
- TC-20261016-10 — pstack principles hang (Option A): `/workspace/typesafe-jev/pstack-principles-hang-v1.md` (meta only).
- ~2026-10-05 — HK IPO research skill wording review for 總指揮 (keep locked calendar/brief/stages/bands; change 繁體 + no-average + HKEJ-missing rows + filename date + pin stage URLs).
- 2026-10-21 — Bot「文章分析」package `/workspace/refactored_article_analysis/` (article-ingest + article-analysis-report). dr eggbot CreateAgent after Justin yes → id `51d50b94-d49a-4d13-8e97-70b57d3c1e31`. Notion sync for Finals (shared journal via 文章分析).

## Live snapshot
- Routines: none
- Open work: none
- Pending confirms: none
- Skills authored / on disk for recent work: article-ingest, article-analysis-report; ETF RS trio; Jev hang assets under `/workspace/typesafe-jev/`
- Refactored packages under `/workspace/`: ~20 `refactored_*` dirs including `refactored_article_analysis`, `refactored_etf_rs_overlay`, market/swing/travel/decision packs
- Out folders used by specs: `/workspace/article-analysis/`, `/workspace/typesafe-jev/logs/`
- Prior backup: `/workspace/cfe4ca9b-b60f-49d3-bd0d-454c269f4388-memory-backup.md` (overwritten this run)

## Secrets
- No API keys stored in this agent’s profile, settings, or memory files.
- TypeSafe / OpenRouter: `[REDACTED:TYPESAFE_API_KEY]` / `[REDACTED:OPENROUTER_API_KEY]` — env only; never pasted.
- Telegram (Stockbee skill family): `[REDACTED:TELEGRAM_BOT_TOKEN]`
- Google connector: `[REDACTED:google-oauth]` (connector-owned)
- Drive / sheet file ids in specs are resource locators, not secrets
