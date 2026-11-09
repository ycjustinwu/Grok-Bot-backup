# Memory Manager — disaster-recovery archive

Private Git backup of Grok Bot settings and memories for this account.

## Layout

- `registry.md` — which bots are included in backup
- `shared-user-memory/MEMORY.md` — account-level shared user memory
- `bots/<slug>/` — per-bot `agent-spec.md`, `profile.md`, `MEMORY.md`, `archive/`
- `skills/` — user-created Grok Bot skills (`SKILL.md` folders); see `skills/INDEX.md`
- `specs/` — package/spec mirrors (e.g. `specs/swing-package-2026-11-09/`)
- `meta/memory-manager-self.md` — this bot’s self backup

## Modes

- cold-start — empty archive + registry, then first full backup
- restore-from-repo — clone private remote, recreate bots from agent-spec
- join-existing-fleet — point at an existing archive remote

Hard gate: do not claim DR is complete until a private Git remote is configured. Never commit tokens/secrets/cookies — placeholders only.

## Named incremental backup (cost gate)

Default is **not** fleet fan-out. Justin names bots; only those are requested/ingested.

### Layout per bot

- `bots/<slug>/MEMORY.md` — current snapshot (whole-file replace on ingest)
- `bots/<slug>/archive/<YYYY-MM-DDTHHMMSS>.md` — prior versions (immutable)
- `bots/<slug>/VERSIONS.md` — append-only index (`vN`, md5, lines, archive path)
- `meta/backup-runs/<run-id>.md` — per-run log
- `CHANGELOG.md` — newest-first human summary
- optional git tag: `backup-<slug>-<date>` (one bot) or `backup-named-<run-id>`

### Commands

```bash
python3 scripts/named-backup.py --list
python3 scripts/named-backup.py --bots second-brain x-monitor          # plan
python3 scripts/named-backup.py --bots second-brain --request          # dump text for SendToAgent
python3 scripts/named-backup.py --bots second-brain --ingest --profiles --tag --commit --push
python3 scripts/named-backup.py --skills --commit --push               # local skills only
```

Rules: `纳入=是` only; skip when dump md5 matches `MEMORY.md`; secrets must be `[REDACTED:…]`; no full-fleet mode in this script.
