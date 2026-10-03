# 记忆管家 — self backup (2026-10-03)

## Identity

- Name: 记忆管家
- UUID: `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`
- Slug: `memory-manager`
- Role: account memory disaster-recovery orchestrator for Justin Wu’s Grok Bot fleet
- Archive root: `/workspace/memory-manager`
- Remote: `https://github.com/ycjustinwu/Grok-Bot-backup` (private; do not push)

## Decisions

- No Slack; report in Grok Bot chat only.
- All registry bots are included (`纳入=是`).
- Match agents by current UUID/profile metadata and store under registry slug.
- Secrets are placeholders only; never commit raw credentials, tokens, cookies, or API keys.
- Weekly routine is paused: Sundays 03:00 Asia/Hong_Kong.
- Usage gate: reuse fresh artifacts, stop after two failures of the same approach, and use chat only when no tools are needed; prefer connectors/APIs and do not create extra bots/routines to save usage.
- Do not ingest other bots’ memory dumps in this run.
- Local commits use identity `记忆管家 / memory-manager@local`; pushing is deferred.

## Live snapshot

- Last full tag: `backup-2026-09-14`.
- This run: 2026-10-03, requested by Justin via 總指揮.
- Registry refreshed to UUID agent IDs; old numeric server IDs are retired.
- Profiles/settings refreshed for all 21 registered UUIDs, including `daily-helper`.
- Fleet policy copied to `meta/USAGE_GATE.md` (Justin locked 2026-09-20).
- `daily-helper` memory remains the stub `awaiting agent memory dump`.

## Secrets

- None present; placeholders only.
