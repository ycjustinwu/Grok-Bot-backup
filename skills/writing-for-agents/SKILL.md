---
name: writing-for-agents
description: >-
  Use this when creating or editing agent-facing documents — skills, AGENTS.md,
  CLAUDE.md, specs, tickets, or runtime prompts — to prune no-ops and write
  predictable process.
---
# Writing For Agents

Reference for writing any document an **agent** reads: skills, `AGENTS.md` / `CLAUDE.md`, specs, tickets, runtime prompts, READMEs. Default move is **deletion**, not explanation (cut no-ops the model already knows).

**Before editing:** Read the full reference at `/home/box/agent-data/workflows/writing-for-agents/UPSTREAM.md`. When the document is a skill, also read `SKILL-MECHANICS.md` in the same folder.

## Levers (summary)

- **Context pointers** — wording that triggers reaching out-of-context material (skill descriptions, AGENTS.md lines)
- **Two loads** — context load (always-on tokens) vs cognitive load (human as index)
- **Information hierarchy / progressive disclosure**
- **Completion criteria** + legwork against premature completion
- **Leading words** from pretraining that anchor process
- **Pruning** — single source of truth; kill duplication, sediment, sprawl

Model-invoked when creating/editing skills or AGENTS/CLAUDE.md; user-invoked (`/writing-for-agents`) for any other agent-facing doc.

On Grok: prefer [skill-authoring](sand-workflow:skill-authoring) mechanics for `update_state` skill writes; use this skill for the *writing craft*.

Source: mattpocock/skills `skills/productivity/writing-for-agents` (renamed from writing-great-skills in v1.1).
