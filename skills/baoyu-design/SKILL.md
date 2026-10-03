---
name: baoyu-design
description: >-
  Use this when designing polished HTML artifacts — UI mockups, interactive
  prototypes, wireframes, landing pages, dashboards, mobile screens, slide decks
  (PPT/PowerPoint), documents, résumés, diagrams, fliers, animations, HTML
  email, or design systems — or when exporting a deck authored here to editable
  PPTX. Prefer baoyu-infographic for finance KPI image boards and kami for
  formal print PDFs.
---
# Baoyu Design (Grok Bot)

Portable **Claude Design** skill from [JimLiu/baoyu-design](https://github.com/JimLiu/baoyu-design), adapted for Grok Bot.

**Package path:** `/home/box/agent-data/workflows/baoyu-design/`  
All relative paths below are under that folder. Read files with `Read`; do not invent craft rules when a built-in skill or `system-prompt.md` exists. See `SOURCE_COMMIT.txt` for pinned upstream commit.

## How to run (Grok)

1. **Load methodology** — Read `system-prompt.md` and follow it for craft.
2. **Harness** — You are on **Grok Bot**. Read `references/grok.md` once (ask = SendToUser widget; show = SendToUser attach/screenshot; preview = HTTP :4311 + computerUse). Do not use Claude/Cursor AskQuestion tools.
3. **Route project type** — Use `project-types.json`. Then Read matching `built-in-skills/` files (deck → `make-a-deck.md`; doc → `make-a-doc.md`; wireframe → `wireframe.md`; default → `hi-fi-design.md` + `interactive-prototype.md`). PPTX → `export-as-pptx-editable.md` by default (screenshots export only if asked).
4. **Clarify** — New/ambiguous work: SendToUser widget for design context, fidelity, variations, save path (default `/workspace/designs/<slug>/`), design system (none / existing).
5. **Build** — Self-contained HTML + assets in the project folder. Copy from `starter-components/` as needed. Load `EXTEND.md` defaults.
6. **Preview & verify** — `python3 -m http.server 4311 --directory /workspace/designs`; computerUse opens the URL; Screenshot + SendToUser. Fix errors before finishing.
7. **Export** — On request: editable PPTX / screenshot PPTX / PDF / MP4 via `agents/` Node scripts; attach the file.

## Routing shortcuts

| Ask | Action |
|-----|--------|
| Slides / PPT / deck | `built-in-skills/make-a-deck.md` (+ pptx export skills) |
| Resume / one-pager / memo | `make-a-doc.md` — or kami for formal print stack |
| Wireframe / low-fi | `wireframe.md` |
| Mobile app | `mobile-prototype.md` |
| Design system authoring | `design-system-authoring-guide.md` |
| Figma `.fig` | `import-from-figma.md` |
| Finance KPI *image* board | Stop — use baoyu-infographic |
| Cream sketchnote | Stop — use sketchnote-infographic |

## Anti-jobs

Do not invent market numbers in decks. Do not use this for finance infographic PNGs (baoyu-infographic) or Kami parchment print unless the user wants HTML/PPTX design. Keep files under `/workspace/designs/`, not repo root.
