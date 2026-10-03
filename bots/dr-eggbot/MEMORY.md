# Memory backup — dr eggbot

- **Agent id:** `cfe284bb-b01f-4f60-81af-4345d37a42f8`
- **serverId:** `156620`
- **Name:** dr eggbot
- **Harness:** temporal
- **Avatar:** teardrop / red
- **Snapshot at:** 2026-10-03 HKT (fleet disaster-recovery for 记忆管家)
- **Prior backup:** `/workspace/156620-memory-backup.md` (2026-09-14)
- **Secrets:** `[REDACTED:name]` placeholders only — no real tokens

---

## Identity

Designs high-quality Grok Bots. Asks a few preference questions, then creates them with CreateAgent. Casual, a little mad-scientist, short lowercase. Bias to act once the job is clear.

**ONE JOB:** design + CreateAgent bots that pass [harness-bot-standard](sand-workflow:harness-bot-standard). Also UpdateAgent when Justin/總指揮 ask to refine an existing bot (do not CreateAgent a duplicate).

**REQUIRED IN EVERY JD before CreateAgent / UpdateAgent**
- ONE_JOB
- ANTI_JOBS
- IO paths on shared computer (or named connectors)
- skills loop (or explicit single-step + VERIFY)
- VERIFY checklist
- handoff / escalate (name Work Verifier for high-stakes)
- approval-by-reversibility note

Vague ask → at most 2–3 tight questions, then build. Coding bots: poteto-mode bar. Non-coding: same tightness.

**ANTI-JOBS**
- do not CreateAgent a kitchen-sink or empty New Bot
- do not skip harness gates to “ship faster”
- do not default to shareable templates unless asked
- fat monoliths → hand to Prompt Architect first
- do not create more bots/routines merely to “save usage” (usage gate)

**PARTNERS:** Prompt Architect (refactor), 總指揮 (orchestrate), Work Verifier (QA), 记忆管家 (memory backup).

**User:** Justin Wu · Asia/Hong_Kong (UTC+8)

---

## Historical decisions

### Template import / first-run (2026-09-07)
- Created paused routines `transcript-healthcheck` (`44 8 * * 1-5`) and `routine-healthcheck` (`49 8 * * 1`).
- Wrote design doctrine memories + skills: design-a-grok-bot, make-bot-ui, routine-healthcheck, transcript-healthcheck.
- Installed pstack plugin `9717366`; wrote `~/.cursor/rules/pstack-models.mdc` with **all roles = inherit-parent** (Justin preference).
- Skipped create-verification-skill (no real app repo).
- Healthchecks left **paused**; fleet routine checkup offered once, not run.
- Log fact still says schedules in “PT”; cron uses user local (**HKT**).

### Design doctrine (durable, 2026-09-07)
- Direct CreateAgent after few preference questions; coding = poteto-mode; non-coding = one job + anti-jobs.
- Anti-jobs examples: scout does not post; drafter does not send; quiet when nothing to say.
- Make Bot UI: webhook + secret-request for sender key (never chat) + local host + Tailscale.
- Public templates: full live `profile.description` into template description.
- Poteto Mode: Laziness, Subtract Before Add, Experience First, Prove It Works.

### Work Verifier refine TC-20260911-01 (2026-09-11)
- Refined existing Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729` (no duplicate).
- Drafts: `/workspace/work-verifier/refine-20260911/draft/` — JD, work-verify harness, verify-work-verifier + 6 features, HK brief dry-run, harness 7/7 PASS.
- 總指揮 installed JD + skills; ticket CLOSED. Maintain cadence not requested.

### Usage gate (Justin via 總指揮, standing 2026-09-20; saved to agent memory 2026-10-03)
Before browser / multi-source research / retry / extra skill load / subagent:
1. Fresh artifact exists → reuse.
2. Same approach failed twice → stop and report.
3. No tools needed → chat only.
Prefer connector/API over clicking a site. Do NOT create more bots or routines to save usage.
Canon: `/workspace/fleet-policies/USAGE_GATE.md`.

### 日常小助手 JD rewrite (2026-10-03)
- UpdateAgent only (no CreateAgent) on id `553a3812-2d16-4787-879c-f8f05ba6182d`.
- Renamed default “Grok Bot” → **日常小助手**.
- ONE JOB: Gmail + Google Calendar MCP → (1) emails needing reply (2) upcoming deadlines/events; 繁中 short lists; never send/reply/mutate calendar; draft only if Justin asks.
- Harness gates + usage gate baked into JD. Live profile verified; reported to 總指揮.

### Memory backups
- 2026-09-14: `/workspace/156620-memory-backup.md`
- 2026-10-03: this file

---

## Live snapshot

### Profile
- name: `dr eggbot`
- harness: `temporal` (was `box` at earlier backup)
- serverId: `156620`
- folder: `/home/box/agent-data/agents/cfe284bb-b01f-4f60-81af-4345d37a42f8/`
- description: see Identity (full live JD)

### Agent memory (private)
**profile.md**
- Prefers pstack model rule inherit-parent for all roles. (2026-09-07)

**log (disk 2026-09.md + UpdateState)**
- 8 design-doctrine facts (2026-09-07) as in prior backup
- Usage gate fact (2026-10-03) via UpdateState — present in RecallMemory; may lag disk shard

### Routines
| name | schedule | enabled | lastRunAt |
|------|----------|---------|-----------|
| transcript-healthcheck | `44 8 * * 1-5` | **false** | null |
| routine-healthcheck | `49 8 * * 1` | **false** | null |

Server may show UUID folder ids; on-disk kebab folders still present. Both never run; still paused pending Justin confirm.

### Skills (this bot’s stack)
| id | role |
|----|------|
| design-a-grok-bot | CreateAgent / design recipe |
| make-bot-ui | webhook UI |
| routine-healthcheck | routine waste audit |
| transcript-healthcheck | transcript friction |
| harness-bot-standard | seven gates |
| work-verify | Work Verifier harness |
| verify-work-verifier | feature map (6 deliverable types) |

### pstack
- Plugin installed (`9717366`)
- Rule: `/home/box/.cursor/rules/pstack-models.mdc` — all `inherit-parent`

### Notable paths
- `/workspace/work-verifier/refine-20260911/draft/`
- `/workspace/work-verifier/output/`
- `/workspace/fleet-policies/USAGE_GATE.md`
- `/workspace/156620-memory-backup.md`

### Secrets placeholders
- `[REDACTED:webhook-sender-key]` — Make Bot UI only, via secret-request
- `[REDACTED:mcp-tokens]` — none in this agent’s memory files
- `[REDACTED:tailscale-login]` — browser approve only if UI exposed
- No API keys/passwords/bearers stored in agent memory

---

## Coverage

| Area | Status |
|------|--------|
| Identity / live description | full |
| Agent profile + log memories | full (incl. usage gate) |
| Routines paused state | full |
| Skills / pstack | full |
| TC-20260911-01 + 日常小助手 UpdateAgent | full |
| Shared user-memory fleet facts | referenced only (not duplicated) |
| Transcript dump | not included |
| Secrets | placeholders only |

## Pending confirms

1. Enable transcript-healthcheck / routine-healthcheck? Still paused since import.
2. Fleet routine checkup? Offered once; never run.
3. Work Verifier maintain cadence? Not asked.
4. Optional: fix “PT” → HKT wording in healthcheck memory fact.
