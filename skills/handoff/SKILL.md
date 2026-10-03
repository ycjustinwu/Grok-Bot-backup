---
name: handoff
description: >-
  Use this when compacting the current conversation into a handoff document for
  another agent, harness, directory, or colleague to pick up (/handoff).
argument-hint: What will the next session be used for?
disable-model-invocation: true
---
# Handoff

Compact the current conversation into a **handoff document** so a fresh agent (or colleague) can continue. User-invoked (`/handoff`).

1. If the user passed a focus note, tailor the doc to that next session.
2. Write markdown to `/tmp/handoff-<slug>.md` (OS temp on the box) — **not** into the project workspace unless asked.
3. Include: live thread (in flight / why / next), and a **suggested skills** section naming sand-workflow skills the next agent should run.
4. **Do not** copy specs, plans, ADRs, issues, commits, diffs — reference by path or URL only.
5. Redact API keys, passwords, and PII.
6. Attach the file via SendToUser so Justin can download or paste into another bot.

Prefer `/compact`-style stay-in-thread when nothing is travelling. Use handoff when swapping harness, directory, colleague, or forking a side task.

Full upstream text: `/home/box/agent-data/workflows/handoff/UPSTREAM.md`.
Source: mattpocock/skills `skills/productivity/handoff`.
