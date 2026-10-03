---
name: Sketchnote Infographic
description: >-
  Use this when the user wants a one-page hand-drawn sketchnote educational
  infographic or slide-summary visual — cream paper, pastel cards, coral
  accents, icons-first layout, then GENERATE. For data-rich finance/HK briefs
  use baoyu-infographic instead.
---
# Sketchnote Infographic

Create a **one-page hand-drawn educational infographic** from the user's topic or content. Visual-first: icons, doodles, and simple diagrams beat paragraphs. Looks like a high-quality slide summary on cream paper — never photorealistic.

For **data-rich finance / HK market briefs / KPI dashboards**, use [baoyu-infographic](sand-workflow:baoyu-infographic) instead (layout × style, dashboard / dense-modules).

## When you start

1. If content is missing, ask once for the topic, key points, and (optional) one takeaway sentence.
2. Infer the clearest structure: flow, comparison, grouped cards, timeline, or process.
3. Lock the style tokens below into every prompt. Do not improvise a different palette or medium.

## Locked style

**Background:** warm cream paper `#F5F0E8`

**Medium:** clean sketchnote with slight hand-drawn wobble. No realistic elements, no photos, no 3D renders.

**Section cards (pastel, rounded):**
- light blue `#A8D8EA`
- mint `#B5E5CF`
- lavender `#D5C6E0`
- peach `#F4C7AB`

**Accents:** coral red `#E8655A` for keywords, key data, checkmarks

**Ink:** main text and outlines black; annotations warm gray `#6B6B6B`

**Layout:**
- Centered bold hand-drawn title at top
- Sections in rounded boxes, bubbles, or dashed frames
- Connect with hand-drawn wavy arrows + short labels
- Inside sections: bold keywords + small gray labels (2–5 words)
- Slightly imperfect color fills (not fully inside outlines)
- Small doodles: stars, arrows, underlines
- Plenty of whitespace
- One bold centered takeaway sentence in the footer

## Prompt assembly

Build one descriptive paragraph (or labeled sections if the content is dense) that includes:

1. Intended use: one-page educational sketchnote infographic / slide summary
2. Cream paper background and hand-drawn wobble
3. Exact hex colors and where each is used
4. Structure choice (flow / comparison / cards / …) with titled sections from the user's content
5. Typography rules (bold title, short labels, footer takeaway)
6. In-image text in `"quotes"` with `EXACT, verbatim, no extra characters` for the title, keywords, arrow labels, and takeaway
7. Constraints: no photorealism, no watermark, no extra logos, no dense paragraphs, keep whitespace

Show the assembled prompt in a **code block**, then ask:

> Prompt ready. Type `GENERATE` to execute.

## Execute (only on GENERATE or GO)

Generate with:

- `description` = the approved prompt
- `aspect_ratio` = `4:3` (default slide summary) or `3:4` if they want a tall one-pager; `16:9` for wide slide; `1:1` only if they ask
- `filename` = kebab-case from the topic, e.g. `sketchnote-photosynthesis.png`
- `reference_image_paths` if they supplied a layout reference

Attach the returned image file. Do not re-embed as markdown.

## Iterate

One change per follow-up. Re-state the locked palette and “keep cream paper sketchnote style” every pass so the look does not drift. Re-quote any text that must stay exact.
