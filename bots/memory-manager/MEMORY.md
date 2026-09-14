# 记忆管家 — MEMORY dump (2026-09-14)

## Identity

- Name: 记忆管家
- UUID: bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed
- Slug: memory-manager
- Role: Disaster-recovery orchestrator for Justin Wu’s Grok Bot fleet
- Job: Continuously back up bot settings + independent memories to private Git (`ycjustinwu/Grok-Bot-backup`)
- Layout owned: `registry.md`, `shared-user-memory/`, `bots/<slug>/`, `meta/`

## Decisions

- No Slack for this account — report only in Grok Bot chat
- All registry bots 纳入=是 (full fleet backup)
- Match agents by `profile.json` name to registry name; folder key = registry slug
- Never commit plaintext secrets/tokens/cookies — placeholders only
- Cold-start: create agent-spec + profile for every opted-in bot; MEMORY stubs until dumps arrive
- Parent agent pushes after dumps land; 记忆管家 may commit locally with identity 记忆管家 / memory-manager@local

## Live snapshot (2026-09-14)

- Mode: cold-start full backup **in progress**
- Remote: https://github.com/ycjustinwu/Grok-Bot-backup (configured; push deferred)
- Opted-in bots: 20 (see registry.md)
- UUID matches: 20/20
- Not in registry: New Bot (f613268a-bc7d-406b-b438-e6f5f060fc88)
- Agent memory dumps: none present at cold-start; stubs written under bots/<slug>/MEMORY.md
- Shared user-memory: copied from box user-memory (sanitized)

## Secrets / credentials (placeholders only)

- GitHub remote auth: `[REDACTED: github_token_or_credential]`
- Any API keys discovered in dumps: `[REDACTED: api_key]`
- Slack: N/A (none configured)
- Browser/session cookies: never stored

## Notes

- Platform durable agent-memory write previously failed; this dump file is the workspace backup channel.
- After other agents write `/workspace/<messaging-id|uuid>-memory-backup.md`, re-run archive to fill MEMORY.md and archive priors.
