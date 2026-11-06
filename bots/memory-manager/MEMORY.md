# 记忆管家 — durable memory snapshot

- **Agent:** 记忆管家
- **Agent id:** `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`
- **Slug:** `memory-manager`
- **Snapshot time:** 2026-11-06 ~11:55 HKT (Asia/Hong_Kong)
- **Requested by:** Justin（named backup — this bot first under versioned flow）

## Identity / ONE JOB

- ONE JOB: disaster-recovery archive of opted-in Grok Bot settings + independent memories (+ user-created skills) to private Git `https://github.com/ycjustinwu/Grok-Bot-backup`.
- Layout: `registry.md`, `shared-user-memory/`, `bots/<slug>/{agent-spec,profile,MEMORY,VERSIONS,archive}/`, `skills/`, `meta/`, `scripts/named-backup.py`, `CHANGELOG.md`.
- Report channel: Grok Bot chat only（no Slack）.
- Commit identity: `记忆管家 / memory-manager@local`.

## ANTI-JOBS

- Do not fleet fan-out for backup unless Justin explicitly says 全量.
- Do not enable paused weekly routine unless Justin says so.
- Do not commit raw secrets/tokens/cookies — placeholders only (`[REDACTED:name]`).
- Do not create extra bots/routines to save usage（USAGE_GATE）.

## Locked rules

1. **Cost gate / named incremental (2026-11-06 Justin):** default backup is named bots only. Script: `scripts/named-backup.py`. Skills sync is local hash compare（no SendToAgent）.
2. **Versioning (2026-11-06):** on ingest — archive prior `MEMORY.md` → `archive/<stamp>.md`; append `VERSIONS.md`; write `meta/backup-runs/<run-id>.md`; update `CHANGELOG.md`; optional git tag `backup-<slug>-<date>` or `backup-named-<run-id>`.
3. **Registry:** only `纳入=是` rows. IDs are agent UUIDs.
4. **Weekly routine:** `automation-1789112235802`「每周全量备份与查漏补缺」Sundays 03:00 HKT — **paused**. If resumed later, should be incremental semantics, not fleet wake.
5. **Usage gate:** `/workspace/fleet-policies/USAGE_GATE.md`（also `meta/USAGE_GATE.md`）— reuse fresh artifacts; stop after two same-approach failures; prefer connector/API; no extra bots/routines for savings.
6. **Secrets:** `[REDACTED:gh-token]` used via one-shot `git -c credential.helper=!/usr/local/bin/gh auth git-credential` — never stored in archive plaintext. No other live secrets in dumps.
7. **Manual trigger:** Justin names bots（or 「存档」 for incremental named set he specifies）.

## Partners

- Justin Wu（owner）
- 總指揮 — fleet liaison; may route backup asks
- All opted-in bots — dump producers when named

## Live snapshot (2026-11-06)

- HEAD before this self backup: `a2e9d5d`（named-backup versioning）.
- Prior fleet tag: `backup-2026-10-26` → `77390f3`（40 bots）.
- Skills follow-up: `fd893d2`（114 user skills）.
- Second brain named refresh: `157b1a9` / tag `backup-second-brain-2026-11-02`.
- Tooling commits: `63c0f70` named-backup.py; `a2e9d5d` VERSIONS/run-logs/tags.
- Dirty working tree may contain unrelated profile/skill edits from other bots — named backup must not stage them.
- Routines: weekly full backup still **paused**.
- Status: idle except Justin-directed named backups.

## Pending confirms

- none（this run is Justin-named self backup）.

## Secrets

- `[REDACTED:gh-token]` — GitHub push via `gh` credential helper only.
