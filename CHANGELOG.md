## 2026-11-09 named incremental backup (`2026-11-09T171057+0800`)

- Skills touched: .
- Git tag: `backup-named-2026-11-09T171057+0800`.
- Run log: `meta/backup-runs/2026-11-09T171057+0800.md`.

## 2026-11-09 named incremental backup (`2026-11-09T171034+0800`)

- Skills touched: `crypto-exec-intake` (new), `crypto-exec-stage-gate` (new), `crypto-exec-validate` (new), `market-awareness-orchestrator` (updated), `regime-daily-report` (updated), `rotation-delta` (new), `script-first-dispatch` (new), `socratic-tutor` (new), `story-handoff-parse` (updated), `story-package-s4` (new), `swing-package-fallback` (new), `swing-package-install` (new), `swing-package-verify` (new), `tv-abnormal-volume-mcp` (updated), `tvscreener` (new), `us-abnormal-volume` (updated), `us-etf-theme-scan` (updated), `us-focus-catalyst` (updated), `us-market-daily-brief` (updated), `us-rotation-structure` (updated), `us-second-brain-3-picks` (updated), `us-swing-session-overview` (updated), `us-swing-sim-open` (updated), `us-swing-sim-reconcile` (updated), `us-swing-sim-track` (updated), `x-signal-retrieval` (updated).
- Run log: `meta/backup-runs/2026-11-09T171034+0800.md`.

## 2026-11-09 — YouTube Analyzer Deep **upgraded** (Cupsir PDF gold)

- Skill `skills/youtube-analyzer-deep/SKILL.md` synced from live workflows (Format A Cupsir PDF gold 2026-11-09 + Notion GFM pipe table rule 4a).
- Bot spec/profile refreshed; registry notes → `upgraded 2026-11-09 Cupsir PDF gold Format A + GFM 4a`.
- MEMORY.md ingest v1 (216 lines, md5 `dbc8c7a93e985b247f0dfeffc54ecb00`) incl. Upgrade section; prior archived.
- Tag: `backup-youtube-analyzer-deep-2026-11-09-upgraded`

# Changelog

## 2026-11-09 named incremental backup (`2026-11-09T161604+0800`)

- Bots named: `youtube-analyzer-deep` (no fleet fan-out).
- `youtube-analyzer-deep` v1: md5 `dbc8c7a93e985b247f0dfeffc54ecb00` (216 lines); was `ce5ab1feee8b1cff31a781acbf739a81`; archive `bots/youtube-analyzer-deep/archive/2026-11-09T161604.md`; VERSIONS.md updated.
- Run log: `meta/backup-runs/2026-11-09T161604+0800.md`.

## 2026-11-09 named incremental backup (`2026-11-09T152752+0800`)

- Bots named: `memory-manager`, `zong-zhi-hui`, `work-verifier`, `hk-after-close`, `fusion-formatter`, `story-search`, `us-swing-setup`, `self-improver`, `us-swing-scanner`, `us-market-daily-brief`, `market-awareness`, `prompt-architect`, `hk-swing-scanner`, `quanfu`, `travel`, `hk-swing-setup`, `sweeper`, `dr-eggbot`, `x-brief`, `video-transcriber`, `daily-helper`, `article-analysis`, `career-coaching`, `crypto-exec`, `etf-rs-cross`, `explainer-video`, `family-growth`, `feature-re-spec`, `hotel-compare`, `html-motion-studio`, `market-master-apps-script`, `north-star`, `researchy`, `restaurant-booking`, `second-brain`, `stop`, `trade-journal`, `us-rs-sharpen`, `us-swing-sim`, `x-monitor`, `youtube-analyzer-deep` (no fleet fan-out).
- Run log: `meta/backup-runs/2026-11-09T152752+0800.md`.

## 2026-11-06 named incremental backup (`2026-11-06T115532+0800`)

- Bots named: `memory-manager` (no fleet fan-out).
- `memory-manager` v1: md5 `4b64dbedbd170139c8808615e732bdc8` (56 lines); was `acd1e0ea4458b36310eca1d1a78acfe4`; archive `bots/memory-manager/archive/2026-11-06T115532.md`; VERSIONS.md updated.
- Git tag: `backup-memory-manager-2026-11-06`.
- Run log: `meta/backup-runs/2026-11-06T115532+0800.md`.

## 2026-11-02 Second brain backup
- Refreshed `bots/second-brain/MEMORY.md` (native Relative_Strength `1D3Brz…`, W44 Soft Finals + weekend eval, crowding/fillable/can’t-miss gates). Prior MEMORY archived as `bots/second-brain/archive/2026-11-02.md`.
- Refreshed `profile.md` / `agent-spec.md` from live agent profile+settings.
- Copied live skills: `skills/us-second-brain-3-picks/`, `skills/us-second-brain-notion-sync/`, `skills/us-swing-session-overview/`.
- Workspace dump mirrored: `/workspace/d354ccee-dcf7-4655-bbde-016bc5db7654-memory-backup.md`.
- Secret scan: placeholders only (`[REDACTED:TYPESAFE_API_KEY]`). Left unrelated dirty `skills/us-etf-theme-scan/SKILL.md` unstaged.
- Tag: `backup-second-brain-2026-11-02`.

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
