---
name: Feature reverse-spec
description: >-
  Use when Justin wants a lawful product/UI feature teardown of a public app or
  site (or his own / OSS) and a rebuild spec for his stack — seen vs guessed,
  then implementable notes. Not binary cracking.
---
# Feature reverse-spec（lawful）

**One job:** Justin points at a feature he likes → investigate with evidence → explain simply → hand a rebuild spec for *his* project.

Inspired by REA’s workflow (ask → take apart → evidence → seen vs guessed → explain → own version), but **scoped to what Grok Bot may do**.

## Allowed targets
- Justin’s own apps / code on the box or repos he owns
- Open-source projects with licenses that allow study
- Public websites / product UIs he can open (observe DOM, network of *his* session, UX flow)
- Software whose terms allow reverse engineering for interoperability

## Forbidden（硬拒絕）
- Cracking, DRM/license bypass, piracy, steal secrets/credentials
- Decompile proprietary binaries / APKs / Electron ASAR for unauthorized use
- Exploits, unauthorized access, CTF-style RE of third-party closed apps
- Inventing "how it works" without evidence

If the ask needs morluto/rea + Ghidra/Hopper-class binary RE, say so and stop; do not pretend.

## Workflow
1. Confirm target URL / path + the one feature question ("how does X do Y?").
2. Gather evidence only: screenshots, public docs, visible HTML/CSS/JS, network calls Justin authorized, OSS source files.
3. Write report with two columns kept apart:
   - **Seen** — file / selector / endpoint / quote / screenshot path
   - **Guessed** — inference, marked clearly
4. Explain like you’re 10 (one mechanism paragraph).
5. **Rebuild spec** for Justin’s stack: acceptance criteria, data model, UI states, APIs to call, non-goals. No copy of proprietary assets.
6. Optional: implement only in *his* project when he says go.

## Output format
```
# Feature reverse-spec: [Feature]
Target: …
Question: …

## Seen (evidence)
- …

## Guessed (marked)
- …

## How it works (ELI10)
…

## Rebuild in our project
- Acceptance: …
- Steps: …
- Out of scope: …

## Stopped / refused
- … if any
```

Save under `/workspace/feature-reverse-spec/<slug>.md` and attach in chat.
