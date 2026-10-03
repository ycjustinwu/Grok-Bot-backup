---
name: baoyu-infographic
description: >-
  Use this when creating a professional infographic, 信息图, visual summary, 可视化,
  高密度信息大图, market-brief dashboard, or layout×style infographic — prefer over
  sketchnote for data-rich finance briefs.
version: 1.117.4
metadata:
  openclaw:
    homepage: 'https://github.com/JimLiu/baoyu-skills#baoyu-infographic'
---
# Baoyu Infographic

Publication-ready infographics via **layout × style**. Adapted from [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) `baoyu-infographic` for Grok Bot.

**Full package path:** `/home/box/agent-data/workflows/baoyu-infographic/`  
Read layout/style specs from `references/layouts/<layout>.md` and `references/styles/<style>.md` before building the prompt. Do not invent layout rules from memory when a reference file exists.

## When to use which visual skill

| Need | Skill |
|------|--------|
| Finance / HK market brief / KPI snapshot / data-rich modules | **This skill** (`baoyu-infographic`) |
| Cream-paper educational sketchnote / slide summary | [sketchnote-infographic](sand-workflow:sketchnote-infographic) |
| General poster / avatar / comic / product shot (propose 3 looks) | [visual-director](sand-workflow:visual-director) |
| Print PDF / DOCX / long formal doc | [kami](sand-workflow:kami) |

## Defaults (from EXTEND.md)

- Layout: `dashboard` (finance briefs); `dense-modules` for high-density guides; `bento-grid` general
- Style: `craft-handmade` (default); Kami-adjacent option: parchment `#f5f4ed` + ink blue `#1B365D`
- Aspect: landscape `16:9` (map to GenerateImage `16:9`)
- Language: match source (zh-TW for 港股簡報)
- Backend: Cursor `GenerateImage`

## Confirmation policy

Confirm layout × style × aspect × language **before** generating. Skip only if the user says `--no-confirm`, `直接生成`, `不用确认`, `GENERATE`/`GO` on an already-shown prompt, or equivalent.

Never ship empty placeholder modules when source content exists — pull real numbers/labels first (e.g. from 港股收市簡報 output or pasted brief).

## Workflow

### 1. Setup & analyze

1. Load EXTEND.md from the first path that exists:
   - `/workspace/.baoyu-skills/baoyu-infographic/EXTEND.md`
   - `/home/box/.baoyu-skills/baoyu-infographic/EXTEND.md`
   - `/home/box/agent-data/workflows/baoyu-infographic/EXTEND.md`
2. Save source content under `infographic/{topic-slug}/source.md` (backup if exists).
3. Write `analysis.md`: topic, data type, complexity, tone, audience, language, design notes.
4. Strip credentials/secrets. Preserve statistics and quotes verbatim.

### 2. Structure content → `structured-content.md`

Title, learning objectives, sections (key concept + verbatim content + visual element + labels), data points exact, design instructions. Markdown only. No invented facts.

### 3. Recommend combinations

If keywords match:

| Keyword | Layout | Styles to promote |
|---------|--------|-------------------|
| 高密度信息大图 / high-density | `dense-modules` | morandi-journal, pop-laboratory, retro-pop-grid |
| 信息图 / infographic | `bento-grid` | craft-handmade |
| market brief / 收市簡報 / KPI | `dashboard` | craft-handmade, technical-schematic, corporate-memphis |

Otherwise recommend 3 layout×style combos with short rationale. Use a question widget (A/B/C + allowCustom).

### 4. Confirm (hard gate)

Confirm combination, aspect (`16:9` / `9:16` / `1:1` / `4:3` / `3:4`), and language. Do not generate until confirmed or explicitly skipped.

### 5. Build prompt → `prompts/infographic.md`

Combine, in order:

1. Layout definition from `references/layouts/<layout>.md`
2. Style definition from `references/styles/<style>.md`
3. Base template from `references/base-prompt.md`
4. Structured content (all text in confirmed language)
5. Aspect string for the prompt body
6. In-image text in `"quotes"` with `EXACT, verbatim, no extra characters`
7. Constraints: no watermark; no inventing numbers; regenerate (don't paint over) if text is wrong

Show the prompt in a **code block**, then ask: type `GENERATE` to execute.

### 6. Generate (only on GENERATE / GO)

1. Persist prompt file first under `infographic/{topic-slug}/prompts/infographic.md`
2. Call `GenerateImage` with `description` = prompt, `aspect_ratio` mapped, kebab-case `filename`
3. Attach the returned image. Do not re-embed as markdown
4. On bad text: regenerate from a corrected prompt — never overlay text with code

### 7. Summary

Report topic, layout, style, aspect, language, output path.

## Layout gallery (21)

`linear-progression`, `binary-comparison`, `comparison-matrix`, `hierarchical-layers`, `tree-branching`, `hub-spoke`, `structural-breakdown`, `bento-grid`, `iceberg`, `bridge`, `funnel`, `isometric-map`, `dashboard`, `periodic-table`, `comic-strip`, `story-mountain`, `jigsaw`, `venn-diagram`, `winding-roadmap`, `circular-flow`, `dense-modules`

## Style gallery (22)

`craft-handmade`, `claymation`, `kawaii`, `storybook-watercolor`, `chalkboard`, `cyberpunk-neon`, `bold-graphic`, `aged-academia`, `corporate-memphis`, `technical-schematic`, `origami`, `pixel-art`, `ui-wireframe`, `subway-map`, `ikea-manual`, `knolling`, `lego-brick`, `pop-laboratory`, `morandi-journal`, `retro-pop-grid`, `hand-drawn-edu`, `retro-popup-pop`

## Hard rules

- Raster only via `GenerateImage` (or pinned backend). Never substitute SVG/HTML as the deliverable.
- Never repair rendered text by painting over the bitmap.
- Preserve source data faithfully.
- For HK/finance briefs: prefer real content from the brief bot or files — never empty grey bars.
