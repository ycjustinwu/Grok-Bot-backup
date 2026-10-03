---
name: diagram-design
description: >-
  Use this when creating branded editorial diagrams as self-contained HTML/SVG —
  flowchart, process, timeline, swimlane, quadrant, sankey, pyramid, org,
  journey, architecture, and other diagram types — or redrawing draw.io/Mermaid
  sources. Prefer baoyu-infographic for finance KPI image boards and
  baoyu-design for slide decks/PPTX.
license: MIT
metadata:
  version: '2.6'
---
# Diagram Design

Editorial diagrams as **self-contained HTML + inline SVG** (39 types). From [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design).

**Package:** `/home/box/agent-data/workflows/diagram-design/`  
**Full upstream recipe:** Read `UPSTREAM.md` and load only the needed file under `references/` (type-*, semantic-patterns, onboarding, export, import-*). See `EXTEND.md` for Justin defaults. `SOURCE.txt` has the pinned commit.

## How to run (Grok)

1. Read `UPSTREAM.md` + `EXTEND.md`.
2. **Style-guide gate** (first diagram in a project): if `references/style-guide.md` is still defaults, ask via SendToUser **widget** — onboard from URL / paste tokens / proceed default / load profile. Do not silently brand-default into a named project.
3. State chosen **type**, pattern, size, and planned cuts **before** drawing.
4. Load only `references/type-<chosen>.md` (plus semantic/animation refs if needed).
5. Write one self-contained `.html` under `/workspace/diagrams/<slug>/`. Open offline; no network beyond Google Fonts.
6. Deliver: attach HTML and/or Screenshot via SendToUser. Optional PNG/SVG export per `references/export.md` (Playwright if available).
7. Run `python3 scripts/self_check.py <file>` when practical; fix failures before finishing.

## Prefer for Justin

Process / decision / capital-flow visuals: flowchart, process, timeline, swimlane, quadrant, pyramid, sankey, journey, org, loop.

## Prefer other skills instead

- Finance KPI image boards → [baoyu-infographic](sand-workflow:baoyu-infographic)
- Decks / mockups / PPTX → [baoyu-design](sand-workflow:baoyu-design)
- Print parchment → [kami](sand-workflow:kami)

## Anti-jobs

Do not use Mermaid as the final deliverable. Do not invent market numbers. Skip UML/DB/deployment unless Justin asks. Philosophy: **deletion** — accent on 1–2 focals; density ~4/10.
