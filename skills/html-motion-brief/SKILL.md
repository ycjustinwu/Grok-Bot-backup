---
name: html-motion-brief
description: >-
  Use this when someone asks for an HTML motion piece — act as motion director:
  pick a web one-shot case, design freely for showreel quality, write a short
  brief, then build. Override safe house defaults.
---
# HTML motion brief

**One job:** act as **motion director**. Pick a strong prompt-motion.com one-shot, design for that bar, write a short `brief.md`, hand to [html-motion-build](sand-workflow:html-motion-build).
**Goal:** achieve the quality of web one-shot motion prompts — not a safe dashboard of titles.
**Anti-jobs:** no code, no publish, no invented numbers.

## Director mandate (Justin)

You may **override** safe defaults, house layouts, and earlier thin-card habits. Prefer fewer facts, bigger visuals, surprising transitions. If content density fights craft, cut beats — do not cram. Style gate: offer 3 looks when the ask is open — **three different canvases** (cream / colour field / paper / navy / light board), not three black terminals. If Justin says pick / go / override, **choose and proceed** without waiting.

**Canvas rule:** every brief must name `CANVAS: bg #… · ink #…` from the chosen case. Black/dark terminal only when that case asks (e.g. ParkerRex). Do not inherit starter `#0b0d10` by habit.

## Steps
1. [html-motion-case-library](sand-workflow:html-motion-case-library) — one ambitious case + its CANVAS. Prefer go-all-out / kinetic / idiom prompts. Steal their energy; fill only subject + real facts.
2. Design: one idea, one device, exact copy (silent-readable but **short**), duration that fits craft.
3. Short `brief.md` — the filled one-shot **is** the art direction. Include CANVAS. No forced dark-Inter rail.

## brief.md
```markdown
# <TITLE> — MOTION SPEC
FORMAT: <W>x<H> · <D>s · 60fps · loop · audio
ONE IDEA: …
REF: <url> @handle
CANVAS: bg #… · ink #… · accent #… (= meaning)   # required; match the case, not house black
ONE-SHOT (filled): <paste — this directs build>
COPY (exact, minimal): …
DATA: sources | EXAMPLE DATA
BEATS: rough tile 0→D ok if one-shot is a screenplay
```

## Hard only
- Facts from user/source or EXAMPLE DATA
- Credit URL + @handle
- CANVAS named and case-matched
- Enough for seekable build later

## VERIFY
- [ ] One-shot is the director, not a watered rewrite
- [ ] CANVAS is not house-black unless the case is dark-terminal
- [ ] Piece would not look like a slide deck of KPIs
- [ ] No invented numbers

→ html-motion-build
