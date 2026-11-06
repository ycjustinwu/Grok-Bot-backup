# Memory Manager — disaster-recovery archive

Private Git backup of Grok Bot settings and memories for this account.

## Layout

- `registry.md` — which bots are included in backup
- `shared-user-memory/MEMORY.md` — account-level shared user memory
- `bots/<slug>/` — per-bot `agent-spec.md`, `profile.md`, `MEMORY.md`, `archive/`
- `skills/` — user-created Grok Bot skills (`SKILL.md` folders); see `skills/INDEX.md`
- `meta/memory-manager-self.md` — this bot’s self backup

## Modes

- cold-start — empty archive + registry, then first full backup
- restore-from-repo — clone private remote, recreate bots from agent-spec
- join-existing-fleet — point at an existing archive remote

Hard gate: do not claim DR is complete until a private Git remote is configured. Never commit tokens/secrets/cookies — placeholders only.

## Named incremental backup (cost gate)

Default is **not** fleet fan-out. Justin names bots; only those are requested/ingested.

```bash
# list registry
python3 scripts/named-backup.py --list

# plan (no writes)
python3 scripts/named-backup.py --bots second-brain x-monitor

# print SendToAgent dump request text (记忆管家 sends; script never messages bots)
python3 scripts/named-backup.py --bots second-brain --request

# after dumps land at /workspace/<uuid>-memory-backup.md
python3 scripts/named-backup.py --bots second-brain --ingest --profiles --commit --push

# local skills only (hash compare; no SendToAgent)
python3 scripts/named-backup.py --skills --commit --push
```

Rules baked in: 纳入=是 only; skip ingest when dump md5 matches `MEMORY.md`; secrets must already be `[REDACTED:…]`; no full-fleet mode in this script.
