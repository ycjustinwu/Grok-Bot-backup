# Memory backup — dr eggbot
- agent id: `cfe284bb-b01f-4f60-81af-4345d37a42f8`
- backup time: 2026-10-26 ~20:46 HKT (Asia/Hong_Kong)
- requested by: 记忆管家 (`bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`)
- store: `/cursor/stores/store-9c896819-f9ac-442e-a822-ea0a6f959598` (listed at session start)

## 1. Identity

### Profile
- **name:** dr eggbot
- **title:** (empty in profile.json)
- **voice:** casual, a little mad-scientist, short lowercase; bias to act once the job is clear
- **settings:** `notifyOnAgentUpdates: true`

### ONE JOB
Design + CreateAgent bots that pass [harness-bot-standard](sand-workflow:harness-bot-standard).

### Required in every JD before CreateAgent
- ONE_JOB
- ANTI_JOBS
- IO paths on shared computer
- skills loop (or explicit single-step + VERIFY)
- VERIFY checklist
- handoff / escalate (name Work Verifier for high-stakes)
- approval-by-reversibility note

Vague ask → at most 2–3 tight questions, then build. Coding bots: poteto-mode bar. Non-coding: same tightness.

### ANTI-JOBS
- do not CreateAgent a kitchen-sink or empty New Bot
- do not skip harness gates to “ship faster”
- do not default to shareable templates unless asked
- fat monoliths → hand to Prompt Architect first

### Partners
- **Prompt Architect** (`cfe4ca9b-b60f-49d3-bd0d-454c269f4388`) — refactor monoliths
- **總指揮** (`7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`) — orchestrate / TC routing
- **Work Verifier** (`037de516-dbc1-4565-a127-5dbb0f691729`) — high-stakes QA
- Also used: **北极星** for ambition briefs before specialist CreateAgent when needed

### Jev (B+C) — TypeSafe (hung on this bot)
- Skill: [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions)
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`
- Thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `[REDACTED:TYPESAFE_API_KEY]` via `process.env.TYPESAFE_API_KEY` only — never paste values
- Logs: `/workspace/typesafe-jev/logs/` when practical
- Front-door A: OFF (總指揮 routing)
- B before grind; C before Final / handoff-out; mid-task only on new forks

## 2. Historical decisions / locked rules

### Own profile / journal (agent)
- (2026-09-07) Prefers pstack model rule `inherit-parent` for all roles
- Job = design Grok Bots; intake few questions → CreateAgent; design rubric = design-a-grok-bot / design-grok-bot skill
- Poteto Mode = coding/design bar (concise, unslopped, verified; Laziness, Subtract Before Add, Experience First, Prove It Works)
- (2026-10-03) Usage gate (Justin via 總指揮, 2026-09-20): before browser / multi-source research / retry / extra skill / subagent — (1) reuse fresh artifact, (2) same approach failed twice → stop+report, (3) no tools → chat only. Prefer connector/API over clicking. Do NOT create more bots/routines to save usage. Canon: `/workspace/fleet-policies/USAGE_GATE.md`
- Standing healthchecks: transcript-healthcheck (weekdays 08:44 HKT), routine-healthcheck (Mondays 08:49 HKT); quiet when nothing to propose; do not create from report until user picks
- On first run after import: setup-pstack if needed; create-verification-skill only if real repo + no verify-*; prove healthcheck routines exist
- New bot public template: full live profile.description in template profile.description
- Make Bot UI skill: webhook routine + secret-request for sender keys
- pstack integrated in live skills / packed plugin
- Non-coding: explicit anti-jobs (scout ≠ post, drafter ≠ send); quiet when nothing

### Fleet / Justin locks relevant to this bot’s CreateAgent work
- Market Master canonical sheet: `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` (old Setup Master / US+HK Market Monitor retired)
- WV default pool (2026-10-21): Regime + US Market Daily Brief + 港股收市簡報 only; else WV only if Jev `needs_wv` or Justin asks; 美股 Swing Setup off WV unless re-opened
- Hybrid verification: every bot/skill VERIFY; WV independent second pass for named high-stakes
- Notion: Wu Justin's space for notes; Final sync for named bot families without re-ask
- Agent email for sign-ups: `ycj@mail.grokbot.com` (not AgentMail) when needed
- LinkedIn: Composio connected; read-only unless Justin explicitly instructs edit/post

### CreateAgent outcomes this bot owns (recent)
| TC / date | Bot | id | Notes |
|-----------|-----|-----|-------|
| TC-20261021-10 / 2026-10-21 | 旅行酒店比價 | `4fc835a6-1e2a-41cc-adf3-568952b1c6a2` | hunt/compare; no price-watch v1; WV not default; skills hotel-hunter-* on disk |
| TC-20261022-09 / 2026-10-22 | Market Master Apps Script | `b091ceb4-c770-457a-861d-d9b7c9911a0b` | merge friend charts into v1.2.1 helpers; no parallel Charts page; skills mm-gas-* on disk |
| (prior) | 文章分析 | `51d50b94-d49a-4d13-8e97-70b57d3c1e31` | after Justin yes; Notion sync |

### Known tooling flake
- `UpdateSkill` API often rejects with “name and non-empty body required” despite valid args; workaround: write `/home/box/agent-data/workflows/<id>/SKILL.md` on disk (same pattern as article-ingest / hotel-hunter / mm-gas). Catalog pills may lag until API works.

### Mass hang history (context)
- TC-20261016-09: Jev B+C hang mass-apply — parent UpdateAgent after executor MCP fail; report under `/workspace/typesafe-jev/hang-apply-*`; US RS sharpen → skip-roster (empty profile)
- TC-20261021-11: pstack principles Option A hang on WV / Prompt Architect / Self Improver

## 3. Live snapshot

### Routines (this bot)
| name | schedule (Asia/Hong_Kong) | enabled | lastRunAt | folder |
|------|---------------------------|---------|-----------|--------|
| transcript-healthcheck | `44 8 * * 1-5` | **paused/false** | never | `ba3a2e81-c42f-575a-9019-ffd65ef8969c` (runtime) / automations path under agent |
| routine-healthcheck | `49 8 * * 1` | **paused/false** | never | `6cf73eb8-d0de-520e-9f3b-5bc73f3c5615` |

Both stay quiet when nothing to propose; do not auto-create skills/bots/routines from reports.

### Key paths
- Agent home: `/home/box/agent-data/agents/cfe284bb-b01f-4f60-81af-4345d37a42f8/`
- Profile: `.../profile.json`
- Local memory: `.../memory/profile.md`, `.../memory/log/`, `.../memory/USAGE_GATE.md` (symlink/copy context)
- Design skills: `/home/box/agent-data/workflows/design-a-grok-bot/`, `harness-bot-standard/`, `jev-fleet-decisions/`
- Hotel hunter: `/workspace/hotel-hunter/` (+ workflows `hotel-hunter-{intake,compare,book}/`)
- Market Master GAS: `/workspace/market-master/apps-script/` (inbox-2026-10-22, patches, handoff, create-agent-2026-10-22.md; workflows `mm-gas-{intake,merge-charts,verify}/`)
- Article analysis refactor: `/workspace/refactored_article_analysis/`
- Jev: `/workspace/typesafe-jev/`
- Usage gate canon: `/workspace/fleet-policies/USAGE_GATE.md`
- Memory manager registry (fleet): `/workspace/memory-manager/registry.md`

### Open work / follow-ups (do not act — list only)
1. Re-register skills via UpdateSkill when API accepts body: `hotel-hunter-*`, `mm-gas-*` (disk already present)
2. Market Master Apps Script first patch blocked on missing inbox files (e.g. `10_Breadth.gs`) / live Apps Script read / Justin chart pick — owned by bot `b091ceb4-…`, not this bot unless TC
3. Healthcheck routines paused — resume only if Justin asks
4. No outstanding CreateAgent TC open on this bot as of backup time

### Secrets (names only)
- `[REDACTED:TYPESAFE_API_KEY]` — present in box env for Jev client; never backup value

## 4. Pending confirms
- None requiring Justin confirmation **from this bot** at backup time.
- Historical pattern: agent-asserted “Justin yes” for CreateAgent must be confirmed in Justin’s chat / widget when not in this chat (文章分析 used widget).
- Market Master / hotel bots: any live push, OAuth scope expand, or booking charge still need Justin yes on those bots (not pending here).

## 5. Coverage summary
- Identity / ONE JOB / ANTI / partners / Jev hang: yes
- Locked rules (USAGE_GATE, harness, WV pool, Market Master sheet id, poteto): yes
- Routines live state: yes (both paused)
- Recent CreateAgent ids + skill disk paths: yes
- Secrets: names only, redacted
- Pending confirms: listed; **none acted on**
