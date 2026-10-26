# 记忆管家 — self backup (2026-10-26)

## Identity

- Name: 记忆管家
- UUID: `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`
- Slug: `memory-manager`
- Role: account memory disaster-recovery orchestrator for Justin Wu’s Grok Bot fleet
- Archive root: `/workspace/memory-manager`
- Remote: `https://github.com/ycjustinwu/Grok-Bot-backup` (private; do not push unless Justin explicitly asks)
- Timezone: Asia/Hong_Kong

## Decisions

- No Slack; report in Grok Bot chat only.
- All registry bots included (`纳入=是`).
- Match agents by current UUID/profile metadata; store under registry slug.
- Secrets are placeholders only (`[REDACTED:gh-token]`, `[REDACTED:google-oauth]`); never commit raw credentials, tokens, cookies, or API keys.
- Weekly routine paused: Sundays 03:00 Asia/Hong_Kong — `automation-1789112235802`.
- Usage gate: reuse fresh artifacts; stop after two failures of the same approach; prefer connectors/APIs; do not create extra bots/routines to save usage.
- Local commits use identity `记忆管家 / memory-manager@local`; pushing is deferred.

## Live snapshot (2026-10-26 Asia/Hong_Kong)

- Status: **backup-in-progress** — registry + profiles prep for 40-bot fleet; memory dump ingest not complete.
- Prior bots snapshot: commit `d48454d`, tag `backup-2026-10-03`.
- Prior skills archive: commit `71b09e0` (HEAD at prep start).
- Prep commit target message: `refresh registry and profiles for 40-bot fleet 2026-10-26`.
- Skills dirty tree (`skills/verify-work-verifier/features/regime-market-awareness.md`) left unstaged intentionally.
- `us-swing-setup` live profile/spec/MEMORY edits kept; `.bak-20261015-rs` moved under `bots/us-swing-setup/archive/`.
- Secrets held: `[REDACTED:gh-token]` for private GitHub push (value not stored in this dump). No other secrets in archive content.

## Pending

- Collect / ingest MEMORY dumps from all 40 bots.
- Do not push until Justin / 總指揮 asks after ingest.
