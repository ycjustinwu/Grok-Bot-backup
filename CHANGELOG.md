# Changelog

## 2026-10-26 full fleet bot backup
- Ingested MEMORY.md for all **40** registry bots (纳入=是). Prior MEMORY archived under `bots/<slug>/archive/2026-10-26.md`.
- Disk-stub dumps (SendToAgent unreachable): `stop`, `us-rs-sharpen` (profile/settings only).
- Newly added vs prior 21-bot backup (2026-10-03): article-analysis, career-coaching, etf-rs-cross, explainer-video, family-growth, feature-re-spec, hotel-compare, html-motion-studio, market-master-apps-script, north-star, researchy, restaurant-booking, second-brain, stop, trade-journal, us-rs-sharpen, us-swing-sim, x-monitor, youtube-analyzer-deep (19 new).
- shared-user-memory: left as-is (disk `/home/box/agent-data/user-memory/` still only Self Improver log + 總指揮/全富 profile facts from 2026-09; no fresher shared files).
- Secret scan: no plaintext live secrets; dumps already use `[REDACTED:…]` placeholders. Skills tree left unstaged.
- Tag: `backup-2026-10-26`.

## 2026-10-26 skills backup
- Refreshed **114** user-created skills from `/home/box/agent-data/workflows/` (folders with `SKILL.md`) into `skills/`, plus rewritten `skills/INDEX.md` (Asia/Hong_Kong).
- +30 vs 2026-10-03 (84): ambition-amplifier, article-analysis-report, article-ingest, feature-reverse-spec, gbrain-memory, hk-brief-getting-started, hk-ipo-research, hotel-hunter-{book,compare,intake}, html-motion-{brief,build,case-library,render}, jev-fleet-decisions, mm-gas-{intake,merge-charts,verify}, notion-db-lookup, notion-final-sync, tv-abnormal-volume-mcp, us-second-brain-{3-picks,notion-sync}, us-swing-rs-enhance, us-swing-session-overview, us-swing-sim-{open,reconcile,track}, x-signal-retrieval, youtube-analyzer-deep.
- Overwrote dirty `skills/verify-work-verifier/features/regime-market-awareness.md` from source (Intermediate Land 2026-10-23).
- Skipped: `kami-md2pdf` (no SKILL.md); managed-skills; plugins; `__pycache__` / node_modules / caches.
- Secret scan of copied skill files: no plaintext tokens/keys/passwords/oauth/private keys; no redactions required.
- No new fleet tag (same-day follow-up after `backup-2026-10-26`).

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
