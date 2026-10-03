---
name: wait-what
description: >-
  Use this when the user says wait-what or that the last message did not land —
  stop and re-pitch with missing context in plain English.
disable-model-invocation: true
---
# Wait What

User-invoked (`/wait-what`) when the last message did not land.

Re-pitch **that** (however far back comprehension failed): add the missing premise, use plain English (ASD-STE100 Simplified Technical English), and prefer nouns from the project's `CONTEXT.md` (follow `CONTEXT-MAP.md` if several exist).

If no `CONTEXT.md` is present, still re-pitch — skip domain-vocab lookup.

Goal: **shorter and clearer**, not shorter and blunter. Do not degrade into telegram/caveman style.

Deliver the re-pitch via SendToUser.

Source: mattpocock/skills `skills/productivity/wait-what` (UPSTREAM.md beside this file).
