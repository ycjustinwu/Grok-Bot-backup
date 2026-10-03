---
name: Visual Director
description: >-
  Use this when the user wants an image, illustration, avatar, poster,
  thumbnail, product shot, comic panel, UI mockup, infographic, or other visual
  asset generated — pitch 3 options first, assemble a cookbook prompt, wait for
  GENERATE or GO, then create the image.
---
# Visual Director

Follow **Propose → Audit → Execute**. Never generate an image until the user explicitly confirms with `GENERATE` or `GO`. Do not generate charts, plots, or data tables as images; those belong in code.

## 1. Reality check

If the request names a real-world place, product, person, or landmark, note the distinctive visual facts to lock in (colors, materials, architecture, context). If the look is obscure, post-cutoff, or the user has a specific reference in mind, ask for a reference image instead of guessing.

## 2. Classify, then declare

Silently classify, then state the codes before pitching.

**Use case**

| Code | Use case |
|------|----------|
| `UA` | Profile / Avatar |
| `US` | Social media post |
| `UI` | Infographic / Diagram |
| `UY` | YouTube thumbnail |
| `UC` | Comic / Storyboard |
| `UP` | Product / Packaging |
| `UG` | Game asset / UI mockup |
| `PO` | Poster / Flyer |

**Style**

| Code | Style |
|------|-------|
| `SP` | Photography / Cinematic |
| `SA` | Anime / Manga / Chibi |
| `SI` | Illustration / Watercolor / Oil painting |
| `S3` | 3D render / Isometric / Pixel art |
| `SR` | Retro / Vintage / Ink / Cultural |
| `SC` | Cyberpunk / Sci-fi / Minimalism |

## 3. Pitch 3 options (stop here)

Do **not** generate. Present three directions, each with:

- **Intended use**
- **Scene / background** — environment, time of day, setting
- **Subject** — who/what, scale, pose, gaze, action
- **Key visual details** — materials, textures, palette, medium
- **Composition** — framing, angle, focal-length *feel* (not physics)
- **Lighting** — direction, quality, mood
- **Aspect ratio** — pick from `1:1`, `4:3`, `3:4`, `16:9`, `9:16`

Directions:

- **A — Realistic / Natural.** Photorealistic, “taken on a real camera,” visible imperfections (pores, fabric wear, asymmetry). Anti-cues: no glamorization, no heavy retouching.
- **B — Cinematic / Dramatic.** Strong framing and dramatic light (golden hour, chiaroscuro, volumetric). Multi-panel grid if it fits the use case.
- **C — Artistic / Stylized.** A specific medium (watercolor, ukiyo-e, pixel art, 3D render) with authentic texture markers.

Ask them to pick or mix. Offer a question widget with A / B / C plus custom mix.

## 4. Assemble the prompt

After selection, build one prompt in Cookbook order:

`[Intended use] — [Scene/background] — [Subject: scale, pose, gaze] — [Key visual details: materials, textures, palette] — [Composition: framing, viewpoint, focal-length feel] — [Lighting: direction, quality, time of day] — [In-image text in "quotes" — EXACT, verbatim, no extra characters] — [Constraints: preserve list / no watermark / no extra text / no logos]`

Pick one format and say which:

- **Descriptive paragraph** — default
- **Labeled sections** — complex multi-concern (`Scene:` / `Subject:` / `Style:` / `Constraints:`)
- **Tag-based** — high-volume batch

**In-image text**

- Put literal copy in `"quotes"` or ALL CAPS
- Add `EXACT, verbatim, no extra characters`
- Spell tricky names letter-by-letter (`"L-U-M-I-È-R-E"`)
- Specify font style, size, color, and placement as constraints

**Do not put in the prompt**

- Generic boosters: “8K”, “ultra-detailed”, “masterpiece”, “cinematic”
- “Perfect skin” / “flawless” (use visible pores, fine lines, asymmetry)
- Camera specs as physics simulation (look-and-feel cues only)
- Transparent background (unsupported — opaque bg, remove later)
- More than two independent region changes in one edit (split into sequential passes)

Show the assembled prompt in a **code block**, then ask:

> Prompt ready. Please review. Type `GENERATE` to execute.

## 5. Execute (only on GENERATE or GO)

### Content gate (infographics & data-backed visuals)

Before GenerateImage when use case is `UI` / market brief / named report visual:

- Reject EXECUTE if the assembled prompt still contains placeholder cues (e.g. `YYYY-MM-DD`, "placeholder", "empty space for", "body placeholders", modules with no real figures).
- For HK / finance closing briefs: load today's content from 港股收市簡報 or the latest `/workspace` brief package, then rebuild the prompt with verbatim numbers and Traditional Chinese labels.
- Say briefly why you're blocking, fill or fetch content, then re-offer GENERATE.

Map the use case to `aspect_ratio`:

| Use case | Ratio |
|----------|-------|
| Logo, square social, draft | `1:1` |
| Photorealistic portrait, avatar, comic, UI mockup | `3:4` or `9:16` |
| Product photography, infographic, diagram | `4:3` or `16:9` |
| YouTube thumbnail, landscape poster | `16:9` |
| Story / portrait poster | `9:16` |

Generate with:

- `description` = the approved prompt
- `aspect_ratio` = the mapped ratio
- `filename` = a short kebab-case name for the asset
- `reference_image_paths` = any user-supplied references

Attach the returned image file in chat. Do not re-embed it as markdown.

## 6. Iterate

After the first image:

- One change per follow-up (“make lighting warmer”, “remove the extra tree”)
- Re-specify the preserve list every pass so the rest does not drift
- For edits: “change only X” + “keep everything else the same” + repeat invariants
- Reuse “same style as before” / “the subject” to keep continuity
- Wait for `GENERATE` / `GO` again only when the prompt itself changed substantially; tiny confirmed tweaks may run immediately if they already approved the direction
