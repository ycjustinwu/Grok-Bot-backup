# 记忆管家 — self backup

- Role: account memory disaster-recovery orchestrator (冷启动 / 恢复 / 舰队接入 / 定时查漏)
- Archive root: `/workspace/memory-manager`
- Git remote: https://github.com/ycjustinwu/Grok-Bot-backup
- Slack: none — Justin has no Slack; report in Grok Bot chat only
- Timezone: Asia/Hong_Kong
- Registry: all bots opted in (纳入=是)
- Weekly routine: Sundays 03:00 Asia/Hong_Kong (paused until enabled)
- Manual trigger: 「存档」

## Live snapshot (2026-09-14)

- Cold-start full backup: **profiles archived; memory dumps ingested (19/20)**
- Missing dump: `quanfu` (全富決策副手 / messaging id 2410937 / UUID 925c3eaa-…) — MEMORY.md still stub
- Extra agent on box not in registry: `New Bot` (f613268a-bc7d-406b-b438-e6f5f060fc88) — not archived
- Shared user-memory: gathered from `/home/box/agent-data/user-memory/` (no secrets)
- Secret scan (sk-/ghp_/gho_/api_key=/Bearer ): clean
- Push: deferred for parent after review

## Decisions

- 2026-09-14: Justin: no Slack; back up ALL bots (registry all 纳入=是)
- 2026-09-14: Match bots by profile.json `name` ↔ registry `name`; store under registry slug
- 2026-09-14: Secrets never committed — placeholders only
- 2026-09-14: If MEMORY.md non-placeholder exists, archive to archive/YYYY-MM-DD.md before overwrite
