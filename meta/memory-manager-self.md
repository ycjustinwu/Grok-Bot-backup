# 记忆管家 — self backup

- Role: account memory disaster-recovery orchestrator (冷启动 / 恢复 / 舰队接入 / 定时查漏)
- Archive root: `/workspace/memory-manager`
- Git remote: https://github.com/ycjustinwu/Grok-Bot-backup (private; do not push)
- Slack: none — report in Grok Bot chat only
- Timezone: Asia/Hong_Kong
- Registry: all bots opted in (纳入=是), identified by agent UUIDs
- Weekly routine: Sundays 03:00 Asia/Hong_Kong (paused)
- Usage gate: `meta/USAGE_GATE.md` (fleet policy Justin locked 2026-09-20)
- Manual trigger: 「存档」

## Live snapshot (2026-10-03)

- Last full tag: `backup-2026-09-14`
- This run was requested by Justin via 總指揮.
- Profiles/settings refreshed for all 21 registered UUIDs.
- All 21 UUID memory dumps were ingested into their matching `bots/<slug>/MEMORY.md`.
- 20 prior differing MEMORY files were archived at `archive/2026-10-03.md`; the memory-manager dump already matched.
- Secret scan found no hits and required no redactions; zero MEMORY stubs remain.
- `daily-helper` was added with `MEMORY.md` stub: `awaiting agent memory dump`.
- Secrets: none present; placeholders only.
- Push: deferred; no push performed.

## Decisions

- Keep the remote private; never push as part of the archive run.
- No Slack; report only in Grok Bot chat.
- Include all opted-in bots.
- Commit locally with identity `记忆管家 / memory-manager@local`.
