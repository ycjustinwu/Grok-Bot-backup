# Changelog

## 2026-09-14
- Cold-start scaffold: standard archive layout created on shared computer.

## 2026-09-14 (later)
- Connected private remote `ycjustinwu/Grok-Bot-backup` and pushed cold-start archive.
- `gh` authenticated as ycjustinwu (scopes: repo, read:org, gist).

## 2026-09-14 cold-start full backup

- Archived all 20 registry bots: agent-spec.md + profile.md (from profile.json/settings.json)
- Ingested agent memory dumps into bots/<slug>/MEMORY.md (19 dumps)
- Shared user-memory gathered from /home/box/agent-data/user-memory/
- Self dump written; meta snapshot updated; secret scan clean
- Extra agent not in registry: New Bot (f613268a-…) — not archived
- Push deferred until parent confirms dumps clean

## 2026-09-14 quanfu late ingest

- Ingested 全富決策副手 (quanfu / 2410937) memory dump; fleet now 20/20.
- Secret scan clean.

## 2026-09-14 full fleet backup
- Ingested MEMORY.md for all 20 opted-in bots (0 stubs).
- Secret scan: no plaintext hits.
- Tag: `backup-2026-09-14`.
- Slack: none (in-chat reports only).
- Extra agent not in registry: New Bot (`f613268a-…`) — not archived.

## 2026-10-03
- Full fleet backup: 21/21 MEMORY dumps ingested (added 日常小助手). Registry ids switched to agent UUIDs. Usage gate copied to meta/USAGE_GATE.md. Secret scan clean. Prior MEMORY archived under archive/2026-10-03.md.

## 2026-10-03 skills backup
- Archived 84 user-created skills from `/home/box/agent-data/workflows/` (folders with `SKILL.md`) into `skills/`, plus `skills/INDEX.md`.
- Skipped: `kami-md2pdf` (no SKILL.md); `kami/scripts/__pycache__` (cache). Did not copy managed-skills or plugins.
- Secret scan of copied skill files: no tokens, API keys, passwords, oauth secrets, private keys, or cookies. No redactions.
