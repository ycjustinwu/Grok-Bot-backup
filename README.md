# Memory Manager — disaster-recovery archive

Private Git backup of Grok Bot settings and memories for this account.

## Layout

- `registry.md` — which bots are included in backup
- `shared-user-memory/MEMORY.md` — account-level shared user memory
- `bots/<slug>/` — per-bot `agent-spec.md`, `profile.md`, `MEMORY.md`, `archive/`
- `meta/memory-manager-self.md` — this bot’s self backup

## Modes

- cold-start — empty archive + registry, then first full backup
- restore-from-repo — clone private remote, recreate bots from agent-spec
- join-existing-fleet — point at an existing archive remote

Hard gate: do not claim DR is complete until a private Git remote is configured. Never commit tokens/secrets/cookies — placeholders only.
