---
name: gstack-upgrade
version: 1.1.0
description: >-
  Use this when upgrading or updating gstack (Garry Tan's agent skill factory)
  to the latest version — detect install type, run upgrade, show what's new.
triggers:
  - upgrade gstack
  - update gstack version
  - get latest gstack
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---
# Gstack Upgrade

Upgrade [garrytan/gstack](https://github.com/garrytan/gstack) to the latest version and show what's new. Use when asked to upgrade/update gstack or "get latest gstack".

**Full upstream recipe:** Read `/home/box/agent-data/workflows/gstack-upgrade/UPSTREAM.md` and follow it (migrations under `/home/box/agent-data/workflows/gstack-upgrade/migrations/`).

## Grok Bot adaptations

- AskUserQuestion → SendToUser **widget** (options: Yes upgrade now / Always keep me up to date / Not now / Never ask again).
- Primary install paths to detect (in order):
  1. `$HOME/.claude/skills/gstack` (Claude global)
  2. `$HOME/.gstack/repos/gstack` (gstack repo clone)
  3. `/home/box/agent-data/workflows/gstack` (Grok vendored monorepo, if present)
  4. Project-local `.claude/skills/gstack` or `.agents/skills/gstack`
- If **none** found: do **not** invent an upgrade. Tell Justin gstack is not installed, and offer to clone into `$HOME/.gstack/repos/gstack` then run `./setup` (or install selected skills into workflows).
- Bash → Shell on the box. Destructive `git reset --hard` requires an explicit widget confirm listing dirty files / unpushed commits.
- After upgrade, summarize CHANGELOG highlights since `OLD_VERSION` via SendToUser.

## Anti-jobs

Do not run upgrade against unrelated repos. Do not delete a stale `.bak` without Justin inspecting it. Do not auto-upgrade unless `GSTACK_AUTO_UPGRADE=1` or config `auto_upgrade` is true.

Package: `/home/box/agent-data/workflows/gstack-upgrade/` (SOURCE.txt, UPSTREAM.md, migrations/).
