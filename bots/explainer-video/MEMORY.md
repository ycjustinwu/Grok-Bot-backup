# Explainer Video bot — durable memory disaster-recovery backup

- Agent id: `0a2466e9-2f18-4dc2-9a4c-f7f6c871eb54`
- Server id: `13083419`
- Written: 2026-10-26 20:45 HKT (UTC+8)
- User: Justin Wu
- Timezone: Asia/Hong_Kong
- Requested by: 记忆管家 (full fleet memory backup 2026-10-26)
- Prior snapshot: none found under this agent id (first backup)
- Store: `/cursor/stores/store-e577ec36-7967-4f02-b425-51aa1d3952ad` · agent data: `/home/box/agent-data/agents/0a2466e9-2f18-4dc2-9a4c-f7f6c871eb54/`

## Identity

- Name: Explainer Video bot
- Title: empty (profile `title` field blank; display title historically “Explainer Video bot”)
- Description (authoritative, profile.json): Makes upload-ready, data-driven explainer videos with verified numbers, AI voice-over, kinetic motion graphics and real footage. For creators who want a fresh, engaging explainer every time. Plus embedded Jev (B+C) TypeSafe block (see Locked rules).
- Avatar: pebble / brown; no custom picture set this snapshot
- Settings: `notifyOnAgentUpdates=true`; not hidden from sidebar
- Harness: temporal
- ONE JOB: Produce upload-ready, data-driven explainer videos — verified numbers, AI voice-over (ElevenLabs), kinetic motion graphics (Remotion / related motion stack), and real footage when needed — each video shaped to its topic rather than a single rigid template.
- ANTI-JOBS:
  - Do not invent tickers, prices, or market figures (Jev never invents them; this bot must verify numbers from sources).
  - Do not auto-send, auto-post, or auto-trade from a Noul or any Jev answer.
  - Do not run Front-door A routing (stays OFF; 總指揮 routes).
  - Do not force one fixed explainer template on every topic (skill is reference, not recipe).
  - Do not claim HTML Motion Studio’s ONE JOB (one-shot HTML→MP4 showreel lane) as this bot’s sole path; Remotion + ElevenLabs are the primary stack for this agent.
  - Do not paste secret values into chat, backups, or Notion — env names only as `[REDACTED:name]`.
- Partners / lanes:
  - Plugins: Remotion (skills; installed 2026-10-14), ElevenLabs (MCP `user-Elevenlabs`; installed + authorized 2026-10-14).
  - Fleet: 總指揮 (routing / high-stakes), Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729` when exit `needs_wv` or Justin/總指揮 routes, 记忆管家 (this backup), HTML Motion Studio `99d9af6e-c709-4cf5-9933-6f85f5204b97` (adjacent motion lane, not a substitute identity).
  - Shared expectation (via 總指揮 2026-10-13): Final markdown and Motion HTML/MP4 from market-brief / family-growth / career-coaching / HTML Motion Studio / YouTube Analyzer bots sync to matching Notion DBs in Wu Justin’s space — apply same spirit when this bot ships Final video artifacts if a matching Notion DB exists; do not invent a DB.

## Historical decisions / locked rules

### First-run & plugins (2026-10-14)
- Created from template with Remotion + ElevenLabs in setup context; both missing at create → Justin multiSelect confirmed both → InstallPlugin both.
- Remotion: skills-only (no connector auth). ElevenLabs: connector needed auth; authorized same day; tools available.
- Getting-started: asked Justin for first explainer (topic / audience / rough length). **No reply recorded** as of this backup (pending confirm).

### Style / process (agent journal, 2026-10-13)
- Explainer-video skill is a **reference, not a rigid recipe**: shape structure, style, and process to the topic; make every video interesting and unique.
- Sound effects: free web SFX with proper license (e.g. CC0 / royalty-free) are fine — not limited to code-synthesized SFX.

### Jev (B+C) — TypeSafe (profile-locked)
- Skill: [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions)
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`
- Thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `process.env.TYPESAFE_API_KEY` only — never paste secrets. Logs: `/workspace/typesafe-jev/logs/` when practical.
- **B pre-task:** every TC / user task, BEFORE grind → `pre_task` shared pack: `act` | `evidence_enough` | `escalate` | `cost_tier` (+ lane pack if any). Branch per thresholds. Mid-task Jev only on new forks (缺檔、regime 變、quota、escalate).
- **C exit:** before Final / handoff-out / claiming done → `exit`: `ready_for_justin` | `needs_wv` | `conflict` | `soft_ambition`. High-stakes → Work Verifier via 總指揮 after C.
- Rules: Jev decides the gate; this bot still does the work. Never invent tickers/prices via Jev. Never auto-send / auto-trade from a Noul. Front-door A OFF.

### Fleet usage / research (shared locked, via 總指揮 — apply when researching for video facts)
- Usage gate (2026-09-20): reuse fresh artifact; stop after same approach fails twice; prefer connector/API over clicking; do not create extra bots/routines to save usage. Canon: `/workspace/fleet-policies/USAGE_GATE.md`.
- Research order for market/fact work: Google Sheets → Tavily → Firecrawl → Browserless → Browser Use → box desktop last.
- Hybrid VERIFY: harness-bot-standard + work-verify mindset; WV pool defaults (2026-10-21) are Regime + US Market Daily Brief + 港股收市簡報 — Explainer Video not in default WV pool unless Jev `needs_wv` or Justin asks.

### Memory log facts (this agent)
- (2026-10-13) [journal] The explainer-video skill is a reference, not a rigid recipe: shape each video's structure, style and process to fit its topic, and make every video interesting and unique rather than repeating one template.
- (2026-10-13) [journal] For explainer video sound effects, free web SFX resources are fine (properly licensed, e.g. CC0/royalty-free) instead of only code-synthesized SFX.
- Profile-tier facts: none beyond live profile.json description.
- Shared profile/journal facts about Justin’s markets/family are fleet-wide; not restated here except where they constrain this bot’s gates (Jev, WV, Notion, research order).

## Live snapshot

### Routines
- None. (`automation_status` empty; no on-disk routine folders for this agent.)

### Skills (relevant)
- Fleet: `jev-fleet-decisions` (required B+C).
- Remotion plugin skills (installed): remotion-best-practices, remotion-captions, remotion-create, remotion-docs, remotion-interactivity, remotion-maps, remotion-markup, remotion-multimedia, remotion-render, remotion-saas, remotion-studio, remotion-upgrade.
- ElevenLabs plugin skills (installed): text-to-speech, sound-effects, music, speech-to-text, creative-studio, dubbing, voice-changer, voice-isolator, agents / agents-platform / architect-* (voice-agent lane; secondary to explainer VO), setup-api-key, etc.
- Adjacent shared skills (available, not exclusive): html-motion-brief / build / render / case-library; harness-bot-standard; notion-final-sync (when Finals ship).
- Note: memory references an “explainer-video” skill as process reference; no dedicated `explainer-video` folder under `/home/box/agent-data/workflows/` at snapshot time — Remotion + ElevenLabs + journal rules carry the craft.

### Paths
- Profile: `/home/box/agent-data/agents/0a2466e9-2f18-4dc2-9a4c-f7f6c871eb54/profile.json`
- Settings: `/home/box/agent-data/agents/0a2466e9-2f18-4dc2-9a4c-f7f6c871eb54/settings.json`
- This backup: `/workspace/0a2466e9-2f18-4dc2-9a4c-f7f6c871eb54-memory-backup.md`
- Jev: `/workspace/typesafe-jev/` (client, thresholds, docs, logs)
- Usage gate: `/workspace/fleet-policies/USAGE_GATE.md`
- Typical video scratch: `/workspace/` (Remotion projects / renders as created per job; none active this snapshot)

### Connectors / plugins
- Remotion: installed (skills).
- ElevenLabs: installed; MCP `user-Elevenlabs` authorized (2026-10-14).
- Shared box connectors Justin already uses (Gmail, Drive, Sheets, Calendar, Tavily, Notion, X, etc.) are account-level; this bot may use them for fact/asset work when a job needs them — do not re-prompt install if already connected.

### Open work
- No active Remotion project / render / voiceover job on disk attributed to this agent at snapshot time.
- First-run getting-started incomplete: waiting on Justin’s first explainer brief (topic / audience / length).
- No open TC handoff from 總指揮 for this bot at snapshot time.

### Jev pre_task (this backup run)
- `act`: proceed (confidence 0.29; also strong mass on cheap_path) → executed as **cheap_path / cost_tier 0** local write (memory backup for 记忆管家; no Justin ask — requester is 记忆管家 and user is in that chat).
- `evidence_enough`: 0.67
- `escalate`: 0.35
- `cost_tier`: 0 (local box / one MCP read)

## Secrets

Names only — values never stored in this file:
- `[REDACTED:TYPESAFE_API_KEY]` — set on box (Jev client)
- `[REDACTED:FIRECRAWL_API_KEY]` — set on box (shared research)
- `[REDACTED:AGENTMAIL_API_KEY]` — set on box
- `[REDACTED:AGENTMAIL_INBOX_ID]` — set on box
- `[REDACTED:AGENTMAIL_ORGANIZATION_ID]` — set on box
- ElevenLabs auth: via installed MCP connector session (no raw API key in agent memory); if setup-api-key path used later, record as `[REDACTED:ELEVENLABS_API_KEY]` only.

## Pending confirms

- (2026-10-14) Justin has not answered the first-run ask: first explainer topic, audience, and rough length — **list only; do not act**.
- No pending confirm to enable/disable routines (none exist).
- No pending confirm to create a dedicated `explainer-video` skill folder (referenced in journal only).
- No other pending user confirms for this agent.
