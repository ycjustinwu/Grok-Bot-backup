---
name: teach
description: >-
  Use this when the user wants to learn a topic over multiple sessions in a
  dedicated teaching workspace with HTML lessons, RESOURCES.md, and learning
  records (/teach).
disable-model-invocation: true
argument-hint: What would you like to learn about?
---
# Teach

User-invoked (`/teach`). Stateful multi-session teaching workspace.

**Before teaching:** Read the full recipe at `/home/box/agent-data/workflows/teach/UPSTREAM.md` and the format files beside it (`MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`, `GLOSSARY-FORMAT.md`). Follow them.

## Workspace (default on Grok)

Prefer `/workspace/learnings/<topic-slug>/` (dedicated dir — not Justin's finance project folders) unless the user names another path. Create:

- `MISSION.md` — why learn this (interview first if missing)
- `RESOURCES.md` — vetted Knowledge + Wisdom sources (never trust parametric knowledge alone; WebSearch/WebFetch)
- `lessons/*.html` — short self-contained HTML lessons (`0001-…html`)
- `reference/*.html` — cheat-sheets / glossaries
- `learning-records/*.md` — ADR-style demonstrated learnings
- `assets/*` — shared CSS/components
- `NOTES.md` — preferences

## Philosophy (summary)

Knowledge from high-trust sources → Skills via interactive lessons → Wisdom from communities. Optimize for **storage strength** (retrieval, spacing, interleaving), not fluency illusion. Each lesson: one tangible win in the zone of proximal development; cite a primary source; remind the user to ask follow-ups.

Preview HTML via local HTTP server + computerUse, or attach files with SendToUser.

Source: mattpocock/skills `skills/productivity/teach`.
