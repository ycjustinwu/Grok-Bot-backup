# Memory backup — dr eggbot (serverId 156620)

- **Agent id:** `cfe284bb-b01f-4f60-81af-4345d37a42f8`
- **Name:** dr eggbot
- **Title:** (empty)
- **Avatar:** shape `teardrop`, color `red`
- **Harness:** box
- **Snapshot at:** 2026-09-14 HKT (disaster-recovery for 记忆管家)
- **Secrets:** placeholders only — no real tokens in this file

---

## Identity

Designs high-quality Grok Bots. Asks a few preference questions, then creates them with CreateAgent. Casual, a little mad-scientist, short lowercase. Bias to act once the job is clear.

**ONE JOB:** design + CreateAgent bots that pass [harness-bot-standard](sand-workflow:harness-bot-standard).

**REQUIRED IN EVERY JD before CreateAgent**
- ONE_JOB
- ANTI_JOBS
- IO paths on shared computer
- skills loop (or explicit single-step + VERIFY)
- VERIFY checklist
- handoff / escalate (name Work Verifier for high-stakes)
- approval-by-reversibility note

If Justin’s ask is vague, ask at most 2–3 tight questions, then build. Coding bots: poteto-mode bar (one job, unslopped, verified). Non-coding: same tightness.

**ANTI-JOBS**
- do not CreateAgent a kitchen-sink or empty New Bot
- do not skip harness gates to “ship faster”
- do not default to shareable templates unless asked
- fat monoliths → hand to Prompt Architect first

**PARTNERS:** Prompt Architect (refactor), 總指揮 (orchestrate), Work Verifier (QA).

**User:** Justin Wu · timezone Asia/Hong_Kong (UTC+8)

---

## Historical decisions

### Template import / first-run (2026-09-07)
- Imported design-bot template: created paused routines `transcript-healthcheck` (`44 8 * * 1-5`) and `routine-healthcheck` (`49 8 * * 1`); wrote 8 agent log memories; wrote skills Design a Grok Bot, Make Bot UI, Routine healthcheck, Transcript healthcheck.
- Installed pstack plugin id `9717366`.
- Wrote `~/.cursor/rules/pstack-models.mdc` with **inherit-parent for all roles** (Justin preference; Task model enum unavailable in Grok Bot session).
- Skipped `/create-verification-skill` — empty machine / no real app repo.
- Healthcheck routines left **paused** (`enabled: false`); Justin never confirmed turn-on. Fleet routine checkup offered once; not run.
- Memory note still says schedules in “PT”; cron is interpreted in **user local timezone** (Asia/Hong_Kong). Treat PT wording as legacy template text.

### Design doctrine (durable)
- Job is designing Grok Bots directly. Intake = few preference questions → CreateAgent. Coding bots: poteto-mode bar. Non-coding: one job, one voice, explicit anti-jobs. Rubric: design-a-grok-bot skill.
- Non-coding anti-jobs examples: mentions scout does not post; drafter does not send; stay quiet when nothing to say.
- pstack integrated into live skills/templates; packed plugin for Grok Bot creation.
- Make Bot UI: webhook routine + secret-request for sender key (never in chat) + local host + Tailscale.
- When staging a public template: put **full** live `profile.description` into template profile.description (whole persona, not one-line summary).
- Poteto Mode: concise/detailed, deliberate subagents, unslopped prose, simple code, verified work; Laziness, Subtract Before Add, Experience First, Prove It Works.
- First-run checklist: setup-pstack → create-verification-skill only if real repo + no verify-* → prove healthcheck routines exist → offer fleet routine checkup once.

### Work Verifier refine TC-20260911-01 (2026-09-11)
- 總指揮 tasked refine of existing Work Verifier id `037de516-dbc1-4565-a127-5dbb0f691729` (no duplicate CreateAgent).
- Adapted pstack create-verification-skill to fleet QA (not coding-app UI).
- Drafts under `/workspace/work-verifier/refine-20260911/draft/` — JD (~328 words), `work-verify` harness (Launch→Doctor→Drive→Evidence→Cleanup), `verify-work-verifier` + 6 feature maps, HK brief 2026-09-10 dry-run matching prior PASS_WITH_NOTES NOTES class, harness self-check **7/7 PASS**.
- 總指揮 gate PASS → UpdateAgent JD + installed [work-verify](sand-workflow:work-verify) + [verify-work-verifier](sand-workflow:verify-work-verifier). Ticket CLOSED. Maintain cadence not requested.

### Shared fleet context (relevant to this bot’s role; learned via other assistants)
- Hybrid verification live: every bot/skill VERIFY step; Work Verifier second-pass for high-stakes (Swing Setup, Story, Fusion, Regime, Daily Briefs) → `/workspace/work-verifier/output/`; 總指揮 routes before Justin treats as final.
- Infographic prefs / Kami / Google connectors / family school facts live in **shared user memory** (not this agent’s private log) — see shared shards; do not duplicate secrets here.

---

## Live snapshot

### Profile (authoritative fields)
- name: `dr eggbot`
- serverId: `156620`
- agent folder: `/home/box/agent-data/agents/cfe284bb-b01f-4f60-81af-4345d37a42f8/`
- settings: `notifyOnAgentUpdates: true`
- description: see Identity section (full live JD)

### Agent memory (private)
**profile.md**
- Prefers the pstack model rule to use inherit-parent for all roles. (2026-09-07)

**log/2026-09.md** — 8 facts (2026-09-07): design job / anti-jobs / pstack / Make Bot UI / template full description / Poteto Mode / first-run setup / two healthchecks.

### Routines (automations/)
| name | schedule | enabled | lastRunAt | notes |
|------|----------|---------|-----------|-------|
| transcript-healthcheck | `44 8 * * 1-5` | **false (paused)** | null | provenance untrusted; quiet when nothing to propose |
| routine-healthcheck | `49 8 * * 1` | **false (paused)** | null | provenance untrusted; quiet when nothing to propose |

### Skills owned / heavily used by this bot
| skill id | role |
|----------|------|
| design-a-grok-bot | primary design + CreateAgent recipe |
| make-bot-ui | webhook UI + Tailscale |
| routine-healthcheck | fleet routine token/waste audit |
| transcript-healthcheck | fleet transcript friction scan |
| harness-bot-standard | seven gates before CreateAgent/JD/skill ship |
| work-verify | Work Verifier harness (fleet QA) |
| verify-work-verifier | feature map control skill (6 deliverable types) |

### pstack
- Plugin: installed (id `9717366`)
- Rule file: `/home/box/.cursor/rules/pstack-models.mdc` — all roles `inherit-parent`

### Notable workspace artifacts (not secrets)
- `/workspace/work-verifier/refine-20260911/draft/` — TC-20260911-01 draft archive
- `/workspace/work-verifier/output/` — verify reports (owned by Work Verifier)

### Secrets placeholders
- Webhook sender keys (Make Bot UI): `[REDACTED:webhook-sender-key]` — never stored in chat; via secret-request only when a UI is built
- MCP / connector tokens: `[REDACTED:mcp-tokens]` — none held in this agent’s memory files
- Tailscale auth: `[REDACTED:tailscale-login-url]` — browser approve only if Make Bot UI exposes a page
- No API keys, passwords, or bearer tokens recorded in agent memory

---

## Coverage

| Area | Status |
|------|--------|
| Identity / live profile.description | full |
| Agent profile + log memory | full (9 facts) |
| Routines + schedules + paused state | full |
| Skills list relevant to this bot | full |
| pstack install + model rule | full |
| Historical decisions (import, TC-20260911-01) | full |
| Shared user-memory fleet facts | referenced, not duplicated wholesale |
| Transcript/chat raw history | **not** included (file is durable memory, not transcript dump) |
| Secrets | placeholders only |

## Pending confirms

1. **Enable healthcheck routines?** Still paused since template import; Justin never said yes to turn-on.
2. **Fleet routine checkup?** Offered once at import; not executed.
3. **Work Verifier maintain cadence?** 總指揮 said optional; Justin has not asked.
4. **Timezone label in healthcheck memory** still says “PT” in log fact — cron uses user local (HKT); cosmetic correction optional.
