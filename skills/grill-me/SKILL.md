---
name: grill-me
description: >-
  Use this when the user wants a relentless interview to sharpen a loose plan,
  design, product idea, or decision (/grill-me). Stateless — no files written.
  Runs the grilling interview loop.
disable-model-invocation: true
---
# Grill Me

User-invoked (`/grill-me`). Prefer a fresh conversation. Stateless: write **no** workspace files.

1. Read and follow [grilling](sand-workflow:grilling) — full path `/home/box/agent-data/workflows/grilling/SKILL.md`.
2. Ask in **rounds** (whole frontier each round). Wait for answers before the next round.
3. On Grok: ask in chat (or a widget when options are short); keep the `❓` / `➡️` round format from grilling.
4. Stop on **ungrillable** questions (need a prototype to react to) — say so instead of endless rephrasing.
5. Do not act on the plan until the user confirms shared understanding.

Source: mattpocock/skills `skills/productivity/grill-me` (see SOURCE.txt).
