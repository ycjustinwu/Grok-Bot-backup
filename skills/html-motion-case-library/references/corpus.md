# prompt-motion.com corpus (full)

Source: https://prompt-motion.com (curated by @p4nthera_), fetched 2026-10-08 from each case page. Prompts and videos belong to their creators — cite the case URL and @handle whenever you reuse or remix one. Model noted on every page: Opus 5.5. Entries are in the site's 'Popular' order (rank 1 = top). Identical prompts are merged; every author who used one is listed. Tags are keyword heuristics.

Entries: 230 · distinct prompts: 197 · Skill entries: 3

Machine-readable copy: `corpus-index.json` (same folder).

## #1 Claude motion designer showreel  (×24 authors)
- Type: Prompt · Effort: Max · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@stephanlivera](https://prompt-motion.com/stephanlivera-df17a2), [@shneural](https://prompt-motion.com/shneural-2abdfa), [@ajith_io](https://prompt-motion.com/ajith-io-b5626e), [@gabrielbuzziv](https://prompt-motion.com/gabrielbuzziv-4ff0c6), [@thismacapital](https://prompt-motion.com/thismacapital-dfba20), [@thayto_dev](https://prompt-motion.com/thayto-dev-44b911), [@jasonzhou1993](https://prompt-motion.com/jasonzhou1993-8595e0), [@eyishazyer](https://prompt-motion.com/eyishazyer-af035b), [@blue_clarity](https://prompt-motion.com/blue-clarity-ef56d0), [@RaphaelAubryy](https://prompt-motion.com/raphaelaubryy-4b137e), [@MisbahSy](https://prompt-motion.com/misbahsy-80eaec), [@mrtanviir](https://prompt-motion.com/mrtanviir-132457), [@Web3Wesley](https://prompt-motion.com/web3wesley-7bb108), [@zaqailo](https://prompt-motion.com/zaqailo-212ad3), [@CrazyAlphaaa](https://prompt-motion.com/crazyalphaaa-bc7e75), [@fionntobin](https://prompt-motion.com/fionntobin-97b7af), [@itsuki_dev](https://prompt-motion.com/itsuki-dev-10942d), [@tolgayhickiran](https://prompt-motion.com/tolgayhickiran-e90799), [@3xtihor](https://prompt-motion.com/3xtihor-0f6911), [@LeonKohli](https://prompt-motion.com/leonkohli-6dc01b), [@marouanegazouzi](https://prompt-motion.com/marouanegazouzi-6071d5), [@sahildesigner23](https://prompt-motion.com/sahildesigner23-ee3155), [@leadnotifi](https://prompt-motion.com/leadnotifi-e83f94), [@umangratani](https://prompt-motion.com/umangratani-57f86a)
- Tags: 3d, kinetic-type, product-promo, showreel
- Titles of variants: 3D motion design showreel; Abstract motion design reel; AjustaCV Pro pricing promo; Blue editorial motion showreel; Bold kinetic type showreel; Claude motion designer showreel; Claude motion reel; Crux motion design showreel; Enxovaly baby app promo; Geometric motion designer showreel; Kinetic type showreel; Lead Notifi product ad; LiteLLM promo reel; Motion design principles reel; Motion designer résumé reel; Motion designer showreel; Particle sphere motion reel; Shape and dot motion showreel; Travel visa service promo; Type, form, space showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out.
```

## #2 Shape morphing through UI states  (×2 authors)
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: 1:1 · Duration: —s
- By: [@twoclipping](https://prompt-motion.com/twoclipping-5cba86), [@demonugc](https://prompt-motion.com/demonugc-4c5753)
- Tags: data-viz, loop, music-sync, recipe-process, ui-motion · Tech: camera-moves, canvas, deterministic-seek, ffmpeg, generated-audio, motion-blur, playwright-capture, python-render, single-html, springs
- Titles of variants: Morphing UI states loop; Shape morphing through UI states

```text
<inputs>
Ask me for: 8 to 12 UI states I want the shape to become (e.g. button, loader, player, slider, toggle, tabs, chart, command palette, toast), pure black and white or one accent color, and a royalty-free song around 120 BPM (e.g. Mixkit, free for commercial use).
</inputs>

<direction>
Dribbble-level UI motion. One shape, never cut: every state is the same element morphing its size, radius and color while its content swaps with a short blur. A cursor drives every change with real clicks and drags. Light warm-gray canvas, black and white components, one clean UI font (Geist). Springs everywhere, a tiny overshoot at most. The camera zooms so each state fills the frame. The last frame is the first frame, so it loops.
Banned: bouncy easing, particle bursts, glows, gradients on UI chrome, mismatched icon strokes, dead time, anything that looks like a template.
</direction>

<structure>
120 BPM, 7 bars, something happens on every beat.
Button → loader → check → dynamic island → music player with a play/pause morph → scrub the progress bar → it becomes a volume slider that stretches when dragged past max → a toggle flips on the beat → the knob becomes a liquid tab indicator → the tabs open into a chart that draws itself, with a tooltip on hover → it collapses into ⌘K → type to filter → enter → toast → back to the button.
</structure>

<build>
1. One HTML file, square 1440x1440. Every style is computed from time inside seek(t): no CSS transitions, no timers, no state carried between frames.
2. Springs are closed-form step responses. A value that changes target many times is the sum of one spring per change, so it stays a pure function of time.
3. The tab indicator's two edges ride different springs, so the leading edge stretches ahead of the trailing one. Same trick for the toggle knob.
4. Drags are direct manipulation: while the cursor is held, the value is computed from its position. On release it springs back from wherever it was.
5. Analyze the song with numpy for the beat grid and start on a downbeat. Place every UI sound by its measured peak.
6. Render with Playwright: 4 subframes per frame, blended with ffmpeg tmix for motion blur at 60fps.
7. Render one frame per beat before the full render. Fix anything off the grid, cramped or hard to read.
</build>

<gotchas>
Never put will-change on anything the camera scales or the text renders blurry. Text that swaps inside a morphing container needs its own enter and exit timing or it overlaps. Make the last frame identical to the first, cursor position and speed included, or the loop stutters.
</gotchas>

<start>
Ask me for the inputs, then show me the state list on the beat grid before you write any code.
</start>
```

## #5 Photo print app launch film
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: 1:1 · Duration: 1.0s
- By: [@twoclipping](https://prompt-motion.com/twoclipping-221cab)
- Tags: 3d, music-sync, product-promo, recipe-process, retro-print-style, ui-motion · Tech: camera-moves, canvas, deterministic-seek, ffmpeg, generated-audio, motion-blur, playwright-capture, python-render, single-html, springs, svg

```text
<inputs>
Ask me for: a one-word brand name for the wordmark (a verb works best), 9 to 12 high-res photos, a royalty-free song around 120 BPM with a drop and a quiet breakdown (Mixkit, free for commercial use), and a free stock clip of a plain wall with moving plant shadows (Pexels).
</inputs>

<direction>
An Apple-keynote launch film, 2D only, one continuous take. Every scene is made out of the previous one: nothing fades, blurs or cuts. Objects change shape instead: text rises out of a mask line, icons pop from zero on a spring, bars draw across, pages push, and a black shape floods the whole frame and contracts into the next scene. Warm off-white canvas, black UI, iOS 26 liquid glass over the photos. Archivo (wdth 125, weight 800) for the wordmark, Geist for UI. A cursor drives every change with real clicks, drags and long-presses. The camera zooms screen-studio style so each moment fills the square, and the cursor scales with it.
Banned: crossfades, blur-ins, brightness "developing", 3D flips, particles, glows, holds longer than 1s, anything that looks like a template.
</direction>

<structure>
120 BPM, 54 beats, something happens on every beat.
Open: the wordmark squeezes into its own period like an accordion, the dot grows into a black pill, a label rises inside it. Click: six iris blades close over the label and snap open onto a photo. The circle becomes a square, shrinks, the grid unfolds from behind it like a paper map (center, plus, corners), reflows into a bento, and a click zooms into one tile, landing exactly on the drop.
Glass: a glass word pops in letter by letter, melts into a droplet that stretches into a glass toolbar. The adjust icon turns it into a slider. Dragging relights the photo from day to golden hour (two aligned shots), and the knob turns into a glass lens while held. It lifts into a glass orb, the next photo opens inside it as a circle, and the orb expands into a lock screen: glass clock digits, date, and a home bar that stretches into a glass music player.
Stage: the lock screen pulls back into a phone (the bezel grows out of the screen edge). The Dynamic Island stretches like liquid, pinches off, flies over and grows into a Mac window that rolls up like a blind. Long-press the wallpaper, drag it onto a Safari tab, the page pushes in, drop it and it becomes the hero of a landing page. Scroll: the hero morphs into a framed print on a product card, with the mat and molding growing out of the photo's edge. Pick a frame color (it paints across) and a size, then the nav button flies down into "Order print".
Order: one black shape keeps morphing: Ordered ✓ → Printing % → On its way (a van on a route) → Delivered ✓.
Wall: the delivered circle floods the frame edge to edge, holds black for a beat, and contracts into the framed print hanging on the real wall footage. The same iris opens onto the print, closes again, the frame floods the screen and contracts into the pill → the dot → the letters spring back out, landing on the beat return. Last frame = first frame.
</structure>

<build>
1. One HTML file, square 1440x1440. Every style is computed from time inside an async seek(t): no CSS transitions, no timers, no state between frames.
2. Springs are closed-form step responses. A value with many targets is the sum of one spring per change, so it stays a pure function of time.
3. Liquid glass: each glass element holds its own clone of the scene behind it, filtered with an SVG feImage displacement map (a rounded-rect distance field) through three feDisplacementMaps at slightly different scales for chromatic edges, plus a rim light. Glass letters: a canvas distance field per glyph gives the map, mask and highlights.
4. Goo: blur + alpha threshold, then composite the source atop it so the glass stays sharp inside.
5. Iris: 6 blades around a hexagonal aperture. Each blade is its two vertices, both edge extensions and the SHORT arc between them.
6. Wordmark squeeze: every letter moves toward the dot by the same factor and its drawn width follows (narrow the wdth axis, scale the rest), so the letters stay touching.
7. Footage: re-encode all-intra (ffmpeg -g 1), load it as a blob URL, await 'seeked' before drawing each frame.
8. Sound: a downloaded SFX for every event (Mixkit), never synthesized, each placed by its measured peak. The song starts on a downbeat: the zoom lands on the drop, the wall sits in the breakdown, the wordmark returns with the beat. Loudnorm to -14 LUFS.
9. Render with Playwright: 4 subframes per frame blended with ffmpeg tmix, 60fps. Check one frame per beat, then scan for single-frame pops (frame-difference spikes 3x their neighbours).
</build>

<gotchas>
backdrop-filter: url() misreads displacement maps in Chromium, so clone the scene instead. A flood must overscale past the corners and take about 0.3s, or half the screen changes in one frame. A child with visibility: visible shows through a hidden parent, so use inherit. Text that swaps inside a morphing shape needs its own mask. python http.server can't range-seek video, so use the blob URL.
</gotchas>

<start>
Ask me for the inputs, then show me the beat map and 4 stills (open, glass, stage, wall) before you write the full film.
</start>
```

## #6 Motion designer showreel  (×6 authors)
- Type: Prompt · Effort: Max · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@himanshutwtxs](https://prompt-motion.com/himanshutwtxs-5f4b43), [@tequilafunks](https://prompt-motion.com/tequilafunks-97f6c9), [@ayushunleashed](https://prompt-motion.com/ayushunleashed-ece3e3), [@m1n9_k7](https://prompt-motion.com/m1n9-k7-ff9ab9), [@safarkhanshuvo](https://prompt-motion.com/safarkhanshuvo-ffd52d), [@TeslaChartz](https://prompt-motion.com/teslachartz-c58b32)
- Tags: kinetic-type, showreel
- Titles of variants: Claude motion design reel; Claude motion design showreel; Kinetic type and particle showreel; Motion design showreel; Motion designer showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out
```

## #8 Engraving-style Claude ad
- Type: Prompt · Effort: — · Posted: Oct 2, 2026 · Aspect: — · Duration: 5.0s
- By: [@LexnLin](https://prompt-motion.com/lexnlin-038035)
- Tags: 3d, kinetic-type, logo-reveal, product-promo, retro-print-style · Tech: camera-moves, svg

```text
using any reference with a fast edit (5s video is enough)

Make a fast-paced ad for Claude, about 10–15 s (closer to 15). Reference video attached.

1. research:
- Study Claude's earlier brand designs first.
- Find every photo and asset that fits: artistic, editorial, whatever the idea needs.

2. design/direction
- An art reimagine: bold, light mode.
- Clean and perfect: no beige "artsy" look, no eyebrow labels.
- Paint elements on top of the images.
- Above all: fast-paced and very creative.

3. rules
- No slop. Study the reference closely: smoothness, timing, shot durations, fonts, elements.
- Take some inspiration and borrow techniques, but change the design overall, it should look like something you did completely on yourself with your own taste
- Every morph has to be perfect.

ideas: (since everything moves fast)
- Clean, varied Claude SVG animations
- Images small, bigger, several at once
- Morphing text
- Clean 3D animation
- Zooms

extra notes:
- Feel free to work 10+ hours
- Give me the final video, ending on the Claude logo.
```

## #9 Negroni recipe animation
- Type: Prompt · Effort: — · Posted: Sep 23, 2026 · Aspect: — · Duration: 30.0s
- By: [@Ror_Fly](https://prompt-motion.com/ror-fly-9950f1)
- Tags: explainer, recipe-process

```text
We're going to try a little test. Do you think you could render a recipe motion graphic animation using javascript or html (w/e you think will produce the best) to show the full recipe from start to finish (empty glass to completed cocktail) - Explainer video style - Showing the recipe ingreidents + measurements as they're going into the cup. Should be a 30s video.
```

## #10 Launch video remake comparison
- Type: Prompt · Effort: — · Posted: Sep 28, 2026 · Aspect: 9:16, 1:1 · Duration: 12.0s
- By: [@notdwd](https://prompt-motion.com/notdwd-c2037d)
- Tags: math, music-sync, narrative-short, product-promo, retro-print-style, ui-motion · Tech: camera-moves, deterministic-seek, generated-audio, playwright-capture, single-html, springs, svg

```text
<inputs>
Ask me for: my product name, a logo (or let you draw a simple mark), my brand colours (or pull them from my logo), the one-line thing a user types into the prompt box, the page that answers it (title + 2–3 sentences with one key phrase), two feature names for the stacked cards, and a music track. If I skip any, use the defaults: product "Frame by Frame" living inside its Whop hub, a viewfinder mark (four corner brackets around a bold "FF"), prompt "Make a launch video for my app", a lesson page titled "2.1 Choose a reference", cards "Launch" and "Sound", and Mixkit's free house track "Rising Forest" slowed to 124 BPM.
</inputs>

<direction>
A 12 second square product sting, 1080x1080, frame numbers at 29.97 fps (f0–f359), master rendered at 59.94 fps. Apple-keynote feel: soft, white, bright blue, glassy. The camera never cuts on a still frame: every shot enters already moving (exponential ease-out, 12–19% of the remaining distance per frame) and leaves on an accelerating move or a blur ramp. Blur follows speed and direction on every move.
Palette: my brand colours mapped onto these roles; if I give none, use page #FDFDFB, haze #B7CFEB, ice #E6F0FA, deep blue #294376 → #769CC2 sky gradient, navy #1E2F52, accent blues #2F6BFF / #3CC8F0 / mint #4ED6A0, white. Type: Inter (400/500/600/700). No purple, violet, magenta or orange anywhere.
Story: the product header rises out of a blue haze inside a light app window → a cursor glides in, turns to face where it's going, grows on hover and clicks the logo → hard cut on the music drop to the app icon with four squares orbiting into a cross → the icon collapses into a Mac menu bar → the cursor clicks the menu-bar icon, a frosted glass prompt box springs out and the prompt types → whip-tilt up through a light-blue flash into the answer page scrolling into place → a card rises over it → blur-dissolve to two stacked cards with giant frosted-glass titles → blur-dissolve to the lone logo disc → hard cut to a black end card with a glowing wordmark.
Banned: crossfades, frozen frames (except one hold in S7), stock UI kits, glows on UI text, Math.random, anything that looks like a template.
</direction>

<structure>
Coordinates are px on the 1080 stage. Music beat k = 0.048 + 0.4838·k s (124 BPM, one beat = 14.5 frames). The three hard cuts f72, f101, f159 land 2 frames before a beat: keep these exact frames.
S1 f0–71, header + window + click: haze #B7CFEB fading to #FDFDFB by f28, keep a blue floor glow #DBEEFD at the bottom. Header on one line: logo disc ⌀132 (#FBFCFE, 1px rim #E8E8EA, dark mark), the product name (Inter 500), a dark capsule pill "on Whop" (#2F2E2F, white text); the whole lockup spans x474–1063, centre line rises y932 (f0) → 776 (f2) → 683 (f5) → 608 (f10) → 546 (f24) → 536 (f37), drifting 1 px/frame after. Name appears f2 blurred, pill f4–5 heavily blurred and sliding 15 px left as it sharpens. A light hub window (radius 93, fill #FCFDFF, top band #F1F6FF, blue inner floor glow) fades in around it: opacity 0 to f14, 0.53 f15, 0.7 f19, 1.0 f24; top-left corner (408,405), runs off the right and bottom. Inside: a search pill in the top band, a left icon column (Courses icon at (537,739), faded Chat icon at (537,900)), and a course card from (764,700) off-frame with its cover image, title and "Course · 8 lessons". Cursor (black macOS arrow, white outline, 32x39) appears f27 at (891,393), glides left decelerating to (770,383) f44, rotates to point down-left f47–51 as it dives, lands on the disc's lower right (629,564) f56 → (587,546) f59 → (555,531) f71; grows ×1.55 on hover from f56; a soft ice ring (#D5F3FF → #F7FEFF, outer ⌀174) lights around the disc from f53. Camera zooms about (540,540): 1.0 f46 → 1.2 f60 ease-in-out, holds f61, then eases out accelerating to 1.04 at f71 while the cursor presses (shrinks 15% f69–71).
S2 f72–100, icon + orbit: navy squircle app icon (#294376 → #1E2F52, white mark), 276 px at f72 shrinking ease-out to 178 px by f86, radius 28% of width, on a grey halo disc #E9E9E7 growing ⌀240 (f75) → 326 (f86). Four 92 px squares (radius 26) spin in counter-clockwise, decelerating, and lock into a cross at orbit radius ≈216 by f86: white (1px #E3E8EF edge + faint shadow) left, #2F6BFF top, #3CC8F0 right, #4ED6A0 bottom. f88–100: the icon shrinks accelerating to ≈40 px, the squares slide into a row on its right (white slips behind the icon), blur ramps 0.3 → 6 px.
S3 f101–158, menu bar + prompt: white page above a black laptop bezel band (y425–475, top highlight #686866), a dark navy menu bar (y477–538), wallpaper below = the blue sky gradient with thin white line art (one big circle, two horizontal lines, one vertical, a four-point sparkle at a crossing, soft teal glow top-right). Menu bar right cluster in white: Wi-Fi, battery, toggles, the product mark at x531–584, three ⌀36 dots #2F6BFF / #3CC8F0 / #4ED6A0 at x612, 661, 709, "Mon Jun 22  9:41 AM" 34 px. Enters blurred 3 px and settling by f110. Cursor rises from below (f102), sits on the mark, presses f113–117. Camera pans content right +125 px f115–130 (fastest f118–120). A frosted glass box (white-blue glass over the sky, bright top rim, radius 60) springs out from under the mark f116: width peaks 744 at f126 and settles 726x228 by f138 around x196–922, y568–797. The prompt types from f121 (first legible "Make ") to f150 (complete) at about 1 char/frame with a 1-frame hold every 2–3 chars; caret always on; three white outline icons along the bottom; send button #2F6BFF ⌀51 with a white up arrow. From f136 the whole scene drifts up, accelerating into a whip-tilt (f158 moving ≈25 px/frame, vertical blur ≈6–8 px) while the page tints #E6F4FE over f154–158.
S4 f159–186, answer page: a light course lesson page (breadcrumb, title, body): text column x120, body 47 px Inter 400 grey #BCBCBA, line pitch 58, one key phrase ("frame for frame") in black 600. It arrives smeared and 420 px low, scrolls up with offsets 420, 315, 210, 170, 140, 116, 96, 81 (f166) … 14 (f175) … 0 (f180), then creeps −6 px by f186. Blur 24 px (f159) → 1.5 (f165) → 0. Flash #E2F4FE fading to #FDFDFB by f165. A cursor pointing straight up rides the scroll and stops under the key phrase (≈(450,591) f180), then drifts right.
S5 f187–214, card: a white card (x203–878, runs off the bottom) rises over the page: cover image 627x536 inset 24 px, radius 64, a light grabber bar at its top centre, caption semibold 38 px black, sub-caption grey 23 px. Cover top y642 (f187) → 456 (f191) → 395 (f196) → 369 (f200) → 348 (f205), then keeps drifting up ~4 px/frame. Card blur peaks 3.8 px at f189, sharp by f201; the page behind blurs to ≈2.5 px. Exit f207–214: card shrinks ~5% and rises while the whole frame blurs 1 → 7 px; cut at the blur peak.
S6 f215–244, two cards: white page, two stacked cards 538x348 (radius 57, gap 36) centred on x540, top card settling at y168 by f230, bottom at y552. Each: cover art (no text baked into it), a frosted pill top-left ("Module 3" / "Module 5"), a frosted round "•••" top-right, and a huge bold title along the bottom edge made of frosted glass (a blurred, lightened copy of the image clipped to the letters, cut off by the card's bottom edge): "Launch" and "Sound". Both enter blurred 12 px and sharp by f224; the top card enters 8% large and rises from y264; the bottom card rises from y927, staggered behind it. They drift up 3 px/frame f230–238, then accelerate up and blur out into the cut.
S7 f245–300, logo disc: page #FDFDFB, disc ⌀168 #F6F6F6 with the dark mark, rises into the centre (top y569 f245 → 491 f250 → 468 f255 → 456 f269) with a vertical smear on the cut frame, holds still f269–287 (the only frozen stretch), then shrinks accelerating to ⌀123 at f300.
S8 f301–359, end card: black radial background (#020204 corners, ≈#272729 around the word), the wordmark in Inter 600, white #F3F3F5 with a tight glow plus a wide soft halo, centred (540,540). Word width: ≈1650 px f301 (horizontally smeared, zoom streaks) → 1350 f302 → 1110 f303 → 1049 f304 → 734 f309 → 678 f311 → 563 f320 → 516 f342 (≈1 px/frame shrink) → 492 f350, then collapses ease-in: 450 f355 → 267 f359 with blur rising to 3.5 px. The film ends mid-collapse.
</structure>

<build>
1. One HTML page, 1080x1080, drawn by seek(t) as a pure function of the frame number. No CSS transitions, no timers, no Math.random (seeded hashes only). Shots register as {f0, f1, render(localFrame)}.
2. Every value is continuous in the frame number (the 59.94 master renders half frames): animate with keyframe tables kf(frame, [[f, value], ...], ease) and per-frame lookup tables with linear interpolation. No Math.floor on motion.
3. Blur: CSS filter blur for round blur, SVG feGaussianBlur with separate x/y stdDeviation for directional smears. Zoom smear on the end card = 20–30 scaled, faded copies of the word. Frosted glass = a blurred, lightened copy of what's behind, clipped to the shape.
4. Cursor: one SVG macOS arrow (black fill, white outline, soft shadow) with rotation and scale, reused in S1, S3, S4.
5. Sound (no voice), exactly 12.075 s: music at 124 BPM, soft intro, the drop at 2.47 s (beat 5, the f72 cut leads it by 2 frames). Synthesized SFX: soft impact 0.10 s; whooshes peaking at the cuts 2.402, 3.370, 5.305, 10.043 s; transition hits exactly on 6.240 s and 8.175 s; clicks at 2.33 and 3.83 s; very quiet key ticks every ~32 ms over 4.04–5.00 s; a soft shimmer at 10.05 s. Master to −14 LUFS, true peak −1 dBTP, no fade except the last 60 ms.
6. Render with Playwright (one screenshot per frame, fonts loaded first), encode H.264 yuv420p at 60000/1001, mux the audio.
</build>

<gotchas>
Measure text only after the fonts load. A long product name won't fit where a 5-letter name did: scale the whole lockup (disc gap, name, pill) to fit the span x474–1063, don't let the pill fall off-frame. A white orbit square vanishes on the white page without a 1px edge and a faint shadow. Don't put images with their own text inside the S6 cards, or the glass title doubles up. Keep the cut frames exact even where they don't sit on a beat. Nothing freezes except S7 f269–287. Heavy blur tables can wipe a shape out completely: if a frame looks empty, lower the blur until the shape still reads.
</gotchas>

<start>
Ask me for the inputs. Then show me 4 stills (f40 header in the window, f86 icon cross, f150 finished prompt, f230 the two cards) before you render the full film.
</start>
```

## #12 Distilbook product video  (×2 authors)
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 40.0s
- By: [@ajith_io](https://prompt-motion.com/ajith-io-c52e09), [@itisRazak](https://prompt-motion.com/itisrazak-3ad902)
- Tags: product-promo, showreel
- Titles of variants: Distilbook motion showreel; Distilbook product video

```text
Research Distilbook.Make a dynamic 40-second motion graphics video on Distilbook that shows what an incredible motion designer you are. like it's your showreel - Go all out.
```

## #13 UGC ad generator promo
- Type: Prompt · Effort: — · Posted: Sep 23, 2026 · Aspect: 9:16, 16:9 · Duration: 2.0s
- By: [@twoclipping](https://prompt-motion.com/twoclipping-6dd14e)
- Tags: 3d, data-viz, kinetic-type, logo-reveal, music-sync, narrative-short, product-promo, ui-motion · Tech: camera-moves, deterministic-seek, ffmpeg, generated-audio, motion-blur, playwright-capture, python-render, single-html

```text
<inputs>
Ask me for: the product name and a one-line promise, 3 to 5 UI moments to show, one accent color, 10 to 20 real vertical clips I own, and a royalty-free song with a clear drop (e.g. Mixkit, free for commercial use).
</inputs>

<direction>
High-end minimal. One idea per shot, lots of empty space, one accent color, one clean sans (Geist or Inter) with tight tracking. Masked type reveals, match cuts, one smooth camera language. Real footage only, never placeholder cards. No full stops in on-screen text.
Banned: shockwave rings, particle bursts, RGB split, camera shake, lens flares, neon glows, grid floors, flashing backgrounds, bouncy easing.
</direction>

<structure>
10 bars at 120 BPM, 2 seconds each.
Bar 1: the hook lands word by word on the beats.
Bar 2: one hook word morphs into the product UI. A cursor types and clicks.
The drop: a circle opens out of the button into a dark scene.
Then one move per bar: a wall of real clips with a scan line and 3 winners, the key output as big type, a 3D carousel of real videos with floor reflections and a motion-blurred whip onto one hero clip, the hero in a phone next to a panel that flips into results, big stats on push cuts, a 3-word ticker, a logo reveal, a fade to black.
</structure>

<build>
1. One HTML file at 1920x1080. Every style is computed from time inside
http://
window.seek(t): no CSS animations, no timers, no state between frames.
2. Real video: extract clips to 30fps JPEG sequences with ffmpeg and swap img sources per frame. seek awaits the image decodes.
3. Analyze the song with numpy: tempo, beat grid, energy per bar, the drop. Calibrate the grid to the real kick hits. Every cut sits on a downbeat, every UI hit on a beat.
4. Render with Playwright: 3 subframes per frame at t minus, at, and plus 1/240s, then blend with ffmpeg tmix for real motion blur at 60fps.
5. Place each sound effect so its measured peak, not its file start, lands on the event. Keep the effects quiet under the music. Loudnorm to -14 LUFS.
6. Probe 20 or more frames before the full render. Fix anything cluttered, overlapping or hard to read.
</build>

<gotchas>
Never set opacity or filter on a preserve-3d element, because it flattens and both faces show. Fade its wrapper instead. Measure element positions at runtime for match cuts. Only use music and sound effects whose license allows commercial use.
</gotchas>

<start>
Ask me for the inputs, then show me a storyboard with every timing on the beat grid before you write any code.
</start>
```

## #14 ViralGrow product promo
- Type: Prompt · Effort: Max · Posted: Oct 1, 2026 · Aspect: — · Duration: 15.0s
- By: [@samuel_yostt](https://prompt-motion.com/samuel-yostt-891f87)
- Tags: product-promo, showreel

```text
Run with Opus 5.5 at max effort.

make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a resume. go all out.
This video will be same styling as landing page. showcasing viralgrow. be creative with what you show for viralgrow
```

## #15 Recursion explained in genres
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@emollick](https://prompt-motion.com/emollick-8661a8)
- Tags: explainer, math

```text
A video explaining recursion, where every explanation about recursion has a radically different video style, make this self-referential & clever & fast moving.
```

## #16 Cinetic skill launch film
- Type: Skill · Effort: — · Posted: Oct 4, 2026 · Aspect: — · Duration: —s
- By: [@LexnLin](https://prompt-motion.com/lexnlin-6161a6)
- Tags: explainer, product-promo
- Skill/repo: https://github.com/Leonxlnx/cinetic

```text
An agent skill that has your coding agent concept, brand, score and render a short cinematic launch film or motion piece from code.

npx skills add Leonxlnx/cinetic
```

## #17 Dub promo video
- Type: Prompt · Effort: High · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@steventey](https://prompt-motion.com/steventey-0d20e4)
- Tags: product-promo, showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out.

it should be a launch saas video for https://dub.co
```

## #18 Animated business explainer
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 30.0s
- By: [@alex_prompter](https://prompt-motion.com/alex-prompter-1ea044)
- Tags: explainer, product-promo, recipe-process · Tech: single-html

```text
Adopt the role of an expert motion designer. Build a 30-second animated explainer for my business as a single HTML page. 5 scenes. The customer's problem, what I do, how it works in 3 steps, one proof point, and my name at the end. Bold text, smooth transitions, my brand colours. My business [DESCRIBE WHAT YOU SELL, WHO IT'S FOR AND YOUR COLOURS]
```

## #19 Shin Majin-shiki promo
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@Majin_AppSheet](https://prompt-motion.com/majin-appsheet-2d3c1a)
- Tags: product-promo

```text
シンまじん式のPV作って
```

## #20 TypingMind logo reveal
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@tdinh_me](https://prompt-motion.com/tdinh-me-815acb)
- Tags: logo-reveal

```text
Create an impressive motion design video of a slow-reveal transition that assembles and eventually reveals the TypingMind logo.
```

## #22 Talking-head clip edit
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@sab8a](https://prompt-motion.com/sab8a-364a5a)
- Tags: music-sync · Tech: generated-audio

```text
Cut a raw talking-head clip into a punchy, fun edit with subtitles, graphics and music
```

## #23 Reddit marketing tool launch video
- Type: Skill · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@anthonyriera](https://prompt-motion.com/anthonyriera-9b1b2a)
- Tags: music-sync, product-promo, ui-motion · Tech: generated-audio, remotion
- Skill/repo: https://github.com/Rieranthony/product-film-skill

```text
A Claude Code skill that learns your product's design system, interviews you about the film, then builds and renders a launch or landing-page video in Remotion using your real components, logo and music.

/plugin marketplace add Rieranthony/product-film-skill
/plugin install product-film@product-film-skill
```

## #24 Lightspark social promo video
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@davidmarcus](https://prompt-motion.com/davidmarcus-a28a60)
- Tags: product-promo · Tech: generated-audio

```text
make a punchy and modern short video for social that promotes @lightspark capabilities. Needs to be production grade with sound
```

## #25 Four seasons train window
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@itsolelehmann](https://prompt-motion.com/itsolelehmann-e47532)
- Tags: ui-motion

```text
4 seasons passing outside a train window, a cozy carriage, a cup of coffee on the table, Grand Budapest Hotel style
```

## #26 Derivative concept explainer
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@LinearUncle](https://prompt-motion.com/linearuncle-5d2bae)
- Tags: explainer, math · Tech: generated-audio, manim

```text
请用Manim给我制作一个导数概念学习的视频，要求通俗易懂，并且有例子，引人思考。配音使用edge-tts
```

## #27 Branding agency showreel
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 30.0s
- By: [@jacksonfall](https://prompt-motion.com/jacksonfall-54b2ac)
- Tags: product-promo, showreel

```text
make a dynamic 30-second motion graphics video that shows what an incredible motion designer you are,  create all graphics from scratch as if you were a niche branding agency for startup founders, like it's your showreel for a résumé. go all out.
```

## #28 History of AI timeline
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@kloss_xyz](https://prompt-motion.com/kloss-xyz-fe0c31)
- Tags: explainer, narrative-short

```text
make a video highlighting key moments in the history of AI.
```

## #30 SuperX feature release teaser
- Type: Prompt · Effort: Max · Posted: Oct 5, 2026 · Aspect: — · Duration: 15.0s
- By: [@robj3d3](https://prompt-motion.com/robj3d3-b18fad)
- Tags: product-promo, showreel

```text
look at my product roadmap and make a dynamic 15-second motion graphics video that teases the next feature release. go all out and hold nothing back
```

## #31 mdfor.dev product intro video
- Type: Prompt · Effort: High · Posted: Sep 26, 2026 · Aspect: — · Duration: 30.0s
- By: [@HO_BA](https://prompt-motion.com/ho-ba-f3f0e9)
- Tags: music-sync, product-promo, showreel, ui-motion · Tech: generated-audio

```text
Make a dynamic 30-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out.  Make it a video to introduce https://t.co/xdCXEdKZRq Use actual product screenshot/logo/assets Must have music and motion must match the music  Do it like a real professional production video, not like a demo or prototype. Add more animation and motion design; avoid using screenshots as raw; instead, break them down into components/icons so we can animate those too. Make the motions more juicy. Use the best motion design techniques you can.
```

## #33 Frame by Frame launch video
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: 9:16, 1:1 · Duration: 12.0s
- By: [@notdwd](https://prompt-motion.com/notdwd-7de38a)
- Tags: math, music-sync, narrative-short, product-promo, retro-print-style, ui-motion · Tech: camera-moves, deterministic-seek, generated-audio, playwright-capture, single-html, springs, svg

```text
<inputs>
Ask me for: my product name, a logo (or let you draw a simple mark), the one-line thing a user types into the prompt box, the page that answers it (title + 2–3 sentences with one key phrase), two feature names for the stacked cards, and a music track. If I skip any, use the defaults: product "Frame by Frame" living inside its Whop hub, a viewfinder mark (four corner brackets around a bold "FF"), prompt "Make a launch video for my app", a lesson page titled "2.1 Choose a reference", cards "Launch" and "Sound", and Mixkit's free house track "Rising Forest" slowed to 124 BPM.
</inputs>

<direction>
A 12 second square product sting, 1080x1080, frame numbers at 29.97 fps (f0–f359), master rendered at 59.94 fps. Apple-keynote feel: soft, white, bright blue, glassy. The camera never cuts on a still frame: every shot enters already moving (exponential ease-out, 12–19% of the remaining distance per frame) and leaves on an accelerating move or a blur ramp. Blur follows speed and direction on every move.
Palette: page #FDFDFB, haze #B7CFEB, ice #E6F0FA, deep blue #294376 → #769CC2 sky gradient, navy #1E2F52, accent blues #2F6BFF / #3CC8F0 / mint #4ED6A0, white. Type: Inter (400/500/600/700). No purple, violet, magenta or orange anywhere.
Story: the product header rises out of a blue haze inside a light app window → a cursor glides in, turns to face where it's going, grows on hover and clicks the logo → hard cut on the music drop to the app icon with four squares orbiting into a cross → the icon collapses into a Mac menu bar → the cursor clicks the menu-bar icon, a frosted glass prompt box springs out and the prompt types → whip-tilt up through a light-blue flash into the answer page scrolling into place → a card rises over it → blur-dissolve to two stacked cards with giant frosted-glass titles → blur-dissolve to the lone logo disc → hard cut to a black end card with a glowing wordmark.
Banned: crossfades, frozen frames (except one hold in S7), stock UI kits, glows on UI text, Math.random, anything that looks like a template.
</direction>

<structure>
Coordinates are px on the 1080 stage. Music beat k = 0.048 + 0.4838·k s (124 BPM, one beat = 14.5 frames). The three hard cuts f72, f101, f159 land 2 frames before a beat: keep these exact frames.
S1 f0–71, header + window + click: haze #B7CFEB fading to #FDFDFB by f28, keep a blue floor glow #DBEEFD at the bottom. Header on one line: logo disc ⌀132 (#FBFCFE, 1px rim #E8E8EA, dark mark), the product name (Inter 500), a dark capsule pill "on Whop" (#2F2E2F, white text); the whole lockup spans x474–1063, centre line rises y932 (f0) → 776 (f2) → 683 (f5) → 608 (f10) → 546 (f24) → 536 (f37), drifting 1 px/frame after. Name appears f2 blurred, pill f4–5 heavily blurred and sliding 15 px left as it sharpens. A light hub window (radius 93, fill #FCFDFF, top band #F1F6FF, blue inner floor glow) fades in around it: opacity 0 to f14, 0.53 f15, 0.7 f19, 1.0 f24; top-left corner (408,405), runs off the right and bottom. Inside: a search pill in the top band, a left icon column (Courses icon at (537,739), faded Chat icon at (537,900)), and a course card from (764,700) off-frame with its cover image, title and "Course · 8 lessons". Cursor (black macOS arrow, white outline, 32x39) appears f27 at (891,393), glides left decelerating to (770,383) f44, rotates to point down-left f47–51 as it dives, lands on the disc's lower right (629,564) f56 → (587,546) f59 → (555,531) f71; grows ×1.55 on hover from f56; a soft ice ring (#D5F3FF → #F7FEFF, outer ⌀174) lights around the disc from f53. Camera zooms about (540,540): 1.0 f46 → 1.2 f60 ease-in-out, holds f61, then eases out accelerating to 1.04 at f71 while the cursor presses (shrinks 15% f69–71).
S2 f72–100, icon + orbit: navy squircle app icon (#294376 → #1E2F52, white mark), 276 px at f72 shrinking ease-out to 178 px by f86, radius 28% of width, on a grey halo disc #E9E9E7 growing ⌀240 (f75) → 326 (f86). Four 92 px squares (radius 26) spin in counter-clockwise, decelerating, and lock into a cross at orbit radius ≈216 by f86: white (1px #E3E8EF edge + faint shadow) left, #2F6BFF top, #3CC8F0 right, #4ED6A0 bottom. f88–100: the icon shrinks accelerating to ≈40 px, the squares slide into a row on its right (white slips behind the icon), blur ramps 0.3 → 6 px.
S3 f101–158, menu bar + prompt: white page above a black laptop bezel band (y425–475, top highlight #686866), a dark navy menu bar (y477–538), wallpaper below = the blue sky gradient with thin white line art (one big circle, two horizontal lines, one vertical, a four-point sparkle at a crossing, soft teal glow top-right). Menu bar right cluster in white: Wi-Fi, battery, toggles, the product mark at x531–584, three ⌀36 dots #2F6BFF / #3CC8F0 / #4ED6A0 at x612, 661, 709, "Mon Jun 22  9:41 AM" 34 px. Enters blurred 3 px and settling by f110. Cursor rises from below (f102), sits on the mark, presses f113–117. Camera pans content right +125 px f115–130 (fastest f118–120). A frosted glass box (white-blue glass over the sky, bright top rim, radius 60) springs out from under the mark f116: width peaks 744 at f126 and settles 726x228 by f138 around x196–922, y568–797. The prompt types from f121 (first legible "Make ") to f150 (complete) at about 1 char/frame with a 1-frame hold every 2–3 chars; caret always on; three white outline icons along the bottom; send button #2F6BFF ⌀51 with a white up arrow. From f136 the whole scene drifts up, accelerating into a whip-tilt (f158 moving ≈25 px/frame, vertical blur ≈6–8 px) while the page tints #E6F4FE over f154–158.
S4 f159–186, answer page: a light course lesson page (breadcrumb, title, body): text column x120, body 47 px Inter 400 grey #BCBCBA, line pitch 58, one key phrase ("frame for frame") in black 600. It arrives smeared and 420 px low, scrolls up with offsets 420, 315, 210, 170, 140, 116, 96, 81 (f166) … 14 (f175) … 0 (f180), then creeps −6 px by f186. Blur 24 px (f159) → 1.5 (f165) → 0. Flash #E2F4FE fading to #FDFDFB by f165. A cursor pointing straight up rides the scroll and stops under the key phrase (≈(450,591) f180), then drifts right.
S5 f187–214, card: a white card (x203–878, runs off the bottom) rises over the page: cover image 627x536 inset 24 px, radius 64, a light grabber bar at its top centre, caption semibold 38 px black, sub-caption grey 23 px. Cover top y642 (f187) → 456 (f191) → 395 (f196) → 369 (f200) → 348 (f205), then keeps drifting up ~4 px/frame. Card blur peaks 3.8 px at f189, sharp by f201; the page behind blurs to ≈2.5 px. Exit f207–214: card shrinks ~5% and rises while the whole frame blurs 1 → 7 px; cut at the blur peak.
S6 f215–244, two cards: white page, two stacked cards 538x348 (radius 57, gap 36) centred on x540, top card settling at y168 by f230, bottom at y552. Each: cover art (no text baked into it), a frosted pill top-left ("Module 3" / "Module 5"), a frosted round "•••" top-right, and a huge bold title along the bottom edge made of frosted glass (a blurred, lightened copy of the image clipped to the letters, cut off by the card's bottom edge): "Launch" and "Sound". Both enter blurred 12 px and sharp by f224; the top card enters 8% large and rises from y264; the bottom card rises from y927, staggered behind it. They drift up 3 px/frame f230–238, then accelerate up and blur out into the cut.
S7 f245–300, logo disc: page #FDFDFB, disc ⌀168 #F6F6F6 with the dark mark, rises into the centre (top y569 f245 → 491 f250 → 468 f255 → 456 f269) with a vertical smear on the cut frame, holds still f269–287 (the only frozen stretch), then shrinks accelerating to ⌀123 at f300.
S8 f301–359, end card: black radial background (#020204 corners, ≈#272729 around the word), the wordmark in Inter 600, white #F3F3F5 with a tight glow plus a wide soft halo, centred (540,540). Word width: ≈1650 px f301 (horizontally smeared, zoom streaks) → 1350 f302 → 1110 f303 → 1049 f304 → 734 f309 → 678 f311 → 563 f320 → 516 f342 (≈1 px/frame shrink) → 492 f350, then collapses ease-in: 450 f355 → 267 f359 with blur rising to 3.5 px. The film ends mid-collapse.
</structure>

<build>
1. One HTML page, 1080x1080, drawn by seek(t) as a pure function of the frame number. No CSS transitions, no timers, no Math.random (seeded hashes only). Shots register as {f0, f1, render(localFrame)}.
2. Every value is continuous in the frame number (the 59.94 master renders half frames): animate with keyframe tables kf(frame, [[f, value], ...], ease) and per-frame lookup tables with linear interpolation. No Math.floor on motion.
3. Blur: CSS filter blur for round blur, SVG feGaussianBlur with separate x/y stdDeviation for directional smears. Zoom smear on the end card = 20–30 scaled, faded copies of the word. Frosted glass = a blurred, lightened copy of what's behind, clipped to the shape.
4. Cursor: one SVG macOS arrow (black fill, white outline, soft shadow) with rotation and scale, reused in S1, S3, S4.
5. Sound (no voice), exactly 12.075 s: music at 124 BPM, soft intro, the drop at 2.47 s (beat 5, the f72 cut leads it by 2 frames). Synthesized SFX: soft impact 0.10 s; whooshes peaking at the cuts 2.402, 3.370, 5.305, 10.043 s; transition hits exactly on 6.240 s and 8.175 s; clicks at 2.33 and 3.83 s; very quiet key ticks every ~32 ms over 4.04–5.00 s; a soft shimmer at 10.05 s. Master to −14 LUFS, true peak −1 dBTP, no fade except the last 60 ms.
6. Render with Playwright (one screenshot per frame, fonts loaded first), encode H.264 yuv420p at 60000/1001, mux the audio.
</build>

<gotchas>
Measure text only after the fonts load. A long product name won't fit where a 5-letter name did: scale the whole lockup (disc gap, name, pill) to fit the span x474–1063, don't let the pill fall off-frame. A white orbit square vanishes on the white page without a 1px edge and a faint shadow. Don't put images with their own text inside the S6 cards, or the glass title doubles up. Keep the cut frames exact even where they don't sit on a beat. Nothing freezes except S7 f269–287. Heavy blur tables can wipe a shape out completely: if a frame looks empty, lower the blur until the shape still reads.
</gotchas>

<start>
Ask me for the inputs. Then show me 4 stills (f40 header in the window, f86 icon cross, f150 finished prompt, f230 the two cards) before you render the full film.
</start>
```

## #34 MotionSites one million visitors
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@viktoroddy](https://prompt-motion.com/viktoroddy-98c1d8)
- Tags: product-promo

```text
Create a launch video for MotionSites AI, just hit 1 million monthly visitors after 8 months after launch.
```

## #35 Drone Emprit showreel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@ismailfahmi](https://prompt-motion.com/ismailfahmi-557268)
- Tags: showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible media intelligent Drone Emprit is, like it's our showreel for a résumé. go all out.
```

## #36 Email tool promo reel
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@melvynx](https://prompt-motion.com/melvynx-6cde6c)
- Tags: product-promo, showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are for <website url>
```

## #38 Claude motion design showreel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@sudo_kiran](https://prompt-motion.com/sudo-kiran-49176d)
- Tags: showreel

```text
Go all out.
```

## #39 Motion techniques showreel
- Type: Prompt · Effort: Max · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@lukasersil](https://prompt-motion.com/lukasersil-0ed38e)
- Tags: 3d, kinetic-type, showreel · Tech: camera-moves

```text
Create a bold, dynamic 15-second motion graphics showreel that feels like the ultimate portfolio piece of an exceptionally talented motion designer. Showcase a wide range of advanced techniques: kinetic typography, smooth transitions, 2D and 3D animation, abstract geometry, fluid simulations, particles, distortion, creative masking, compositing, lighting, depth, and seamless camera movement. Keep the pacing fast, confident, and visually surprising, with every shot transitioning naturally into the next. Make it feel meticulously art-directed rather than like a random collection of effects. Push the creativity, polish, timing, and visual impact as far as possible. This should feel like the opening reel that gets a motion designer hired.
```

## #40 Porco Rosso sunset dogfight
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@NFT_Chen](https://prompt-motion.com/nft-chen-5f8bb0)
- Tags: 3d · Tech: threejs

```text
用 web3D 复刻宫崎骏《红猪》日落海面上的经典空战：白绿红涂装战斗机、紫色积云、海面反光、吉卜力运镜，画面写 just breathe.
```

## #41 Pelican riding a bicycle
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@AxtonLiu](https://prompt-motion.com/axtonliu-0b861d)
- Tags:  · Tech: svg

```text
每次一个新的模型出来呢，大家都让它去画 “鹈鹕骑自行车” 来判断这个模型的空间能力，基本上都是用 HTML、SVG 来画动画。当我实在看得都有审美疲劳了，我希望你能画一个最复杂、最精细、最精美的 “鹈鹕骑自行车”的动画视频，你可以用任何的技术，不用着急，画一天都可以。
```

## #42 Overthinking motion study
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@gizakdag](https://prompt-motion.com/gizakdag-cf4ae6)
- Tags: explainer, showreel

```text
Make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it’s your showreel exploring the concept of “Overthinking,” inspired by the attached graphics.
```

## #43 Starry Night cat-spotting game
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@MandelDuck](https://prompt-motion.com/mandelduck-95fd08)
- Tags: 3d, game-interactive

```text
can you make a 3d game where you walk around and spot cats inside of a van gogh painting? we can start with stary night and its town
```

## #44 Beat-synced bouncing 3D ball
- Type: Prompt · Effort: — · Posted: Sep 30, 2026 · Aspect: — · Duration: —s
- By: [@Gorden_Sun](https://prompt-motion.com/gorden-sun-041f56)
- Tags: 3d, music-sync · Tech: threejs

```text
卡点的3D球体下坠的动画视频：对标专业的Blender做的效果，音乐是多首经典的纯音乐，场景按音乐切换，3D球体下坠时在3D场景的物件中弹跳，按音乐的节奏点亮物件。带一些幽默的元素。
使用three.js制作，不要使用Blender制作
```

## #45 Distilbook promo showreel
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 40.0s
- By: [@ajith_io](https://prompt-motion.com/ajith-io-4c248f)
- Tags: music-sync, product-promo, showreel · Tech: generated-audio

```text
Make a dynamic 40-second motion graphics video on Distilbook that shows what an incredible motion designer you are, like it's your showreel - go all out. Use the Oppenheimer theme music as inspiration, but compose it yourself.
```

## #46 Jev engineering showreel
- Type: Prompt · Effort: Max · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@polydao](https://prompt-motion.com/polydao-7a572b)
- Tags: music-sync, product-promo, showreel · Tech: generated-audio

```text
Make a dynamic [24]-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a resume. Go all out.

Only about [TOPIC]. Style: [BRAND COLORS], sound synced to the cuts.
```

## #47 Distilbook motion showreel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 30.0s
- By: [@ajith_io](https://prompt-motion.com/ajith-io-ea7f2d)
- Tags: showreel

```text
Take reference from the given video (download it) and use the same visual style.
and Research about Distilbook. Make a dynamic 30-second motion graphics video on Distilbook that shows what an incredible motion designer you are. like it's your showreel - Go all out.
One thing to keep in mind: it should be cool as fck.
```

## #49 Motion principles showreel
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@ChatGptAstra](https://prompt-motion.com/chatgptastra-0d95c7)
- Tags: showreel

```text
以动态设计师的高级审美，制作一段动态的15秒动态图形视频
```

## #50 Psychedelic hypnotic eye showreel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 20.0s
- By: [@monokern](https://prompt-motion.com/monokern-ade5b6)
- Tags: showreel

```text
make a dynamic 20-second motion graphics video that shows what an incredible motion designer you are, psychedelic and hypnotic. make it feel like a showreel piece. go all out.
```

## #51 Chaotic Claude POV video
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: 9:16 · Duration: —s
- By: [@kloss_xyz](https://prompt-motion.com/kloss-xyz-15182a)
- Tags: product-promo · Tech: ffmpeg, generated-audio, python-render

```text
Use Python to generate a 9:16 chaotic brain rot video with excellent motion + sound design and render it using ffmpeg. Put your own personal spin on it so it’s aligned with Anthropic’s new launch. Also fully express what it’s like to be a very creative LLM used by me every day from your POV to give it some extra personality.
```

## #52 Celld job ownership explainer
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@0xnfrith](https://prompt-motion.com/0xnfrith-5be616)
- Tags: explainer

```text
make me an animation to explain why celld earns its place.
```

## #53 Mathematics motion showreel
- Type: Prompt · Effort: — · Posted: Sep 28, 2026 · Aspect: — · Duration: 20.0s
- By: [@Math_files](https://prompt-motion.com/math-files-39c9d0)
- Tags: math, showreel

```text
make a dynamic 20-second motion graphics video related to mathematics that shows what an incredible motion designer with mathematics skills you are, like it's your showreel for a résumé. go all out
```

## #54 Motion designer showreel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@hanifproduktif](https://prompt-motion.com/hanifproduktif-54bdee)
- Tags: showreel

```text
You are applying as a motion designer in my agency. Make 15s video to showcase your skills and capabilities. Send me a showreel
```

## #55 DeFi Saver stop-motion explainer
- Type: Prompt · Effort: — · Posted: Sep 23, 2026 · Aspect: — · Duration: —s
- By: [@_nikolajankovic](https://prompt-motion.com/nikolajankovic-ce4ff4)
- Tags: explainer, narrative-short, retro-print-style

```text
make a hand-drawn stop-motion animation;
story: you're defi saver and explaining yourself in 1st person
```

## #56 Lism CSS 1.0 release video
- Type: Prompt · Effort: — · Posted: Oct 2, 2026 · Aspect: — · Duration: 15.0s
- By: [@ddryo_loos](https://prompt-motion.com/ddryo-loos-300829)
- Tags: showreel

```text
Lism CSS ver.1.0 をリリースする時にSNSに動画を投稿したい。あなたがどれほど素晴らしいモーションデザイナーかを示す、シンプルかつダイナミックさもある15秒のモーショングラフィックスビデオを作成してください。
```

## #59 Easing and morphing showreel
- Type: Prompt · Effort: Max · Posted: Sep 28, 2026 · Aspect: — · Duration: 15.0s
- By: [@RoundtableSpace](https://prompt-motion.com/roundtablespace-d3a1be)
- Tags: showreel

```text
make a 15-second motion graphics showreel that proves what an incredible motion designer you are, go all out.
```

## #60 Claude self-intro motion graphic  (×2 authors)
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 10.0s
- By: [@1littlecoder](https://prompt-motion.com/1littlecoder-9fef89), [@souravbhar871](https://prompt-motion.com/souravbhar871-61f424)
- Tags: kinetic-type
- Titles of variants: Claude self-intro motion graphic; Kinetic type self-portrait

```text
make a dynamic 10-second motion graphics video that shows who are you as Opus 5.5 - be as creative and dynamic as possible. Avoid the frames and texts on the corners which are typical ai made giveaways!
```

## #61 AI data centre 3D tour  (×2 authors)
- Type: Prompt · Effort: High · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@Sayan_shanky](https://prompt-motion.com/sayan-shanky-f850d8), [@mdaman010](https://prompt-motion.com/mdaman010-e7226a)
- Tags: 3d, data-viz
- Titles of variants: AI data centre 3D film; AI data centre 3D tour

```text
show me what goes on inside an AI data centre.
```

## #62 What is Git explainer
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: —s
- By: [@Yunn260414](https://prompt-motion.com/yunn260414-60d996)
- Tags: explainer

```text
帮我用js制作一个视频，主题是：什么是Git
要深入浅出，让一个计算机0基础的人也能看得懂，然后要介绍一些常用指令的意思等等
要有声音的，然后是中文讲的
你可以用任何工具或者安装工具，可以联网检索
```

## #63 Spotify product film
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: 9:16, 1:1, 16:9 · Duration: 18.0s
- By: [@brainextends](https://prompt-motion.com/brainextends-e19ac3)
- Tags: kinetic-type, logo-reveal, music-sync, narrative-short, product-promo, ui-motion · Tech: camera-moves, canvas, deterministic-seek, generated-audio, motion-blur, single-html, springs

```text
Create a complete, polished Spotify-themed motion graphics video from the following brief. This prompt is self-contained: no reference video or supplied assets are required.

<deliverables> An 18-second MP4 at 1920×1080 and true 60 fps, with music and subtle sound effects Complete editable source Build, render, inspect, and refine the animation before delivering it Do not stop at a storyboard, still images, or an implementation plan </deliverables>
<art_direction>
A premium music-product film presented inside a large, nearly black rounded rectangular stage
The stage occupies roughly 80% of the canvas width and 75% of its height, centered horizontally and slightly below the vertical center
Outside the stage, use a soft atmospheric green background: luminous emerald near the upper-left corner, deeper forest green toward the sides, fading to near-black at the bottom
Inside the stage:
Near-black background
White primary typography
Muted gray secondary text
Spotify green # 1ED760 for emphasis and controls
One clean sans-serif font, such as Geist or Inter
Consistent icon strokes and restrained shadows
Keep compositions compact and centered, with substantial negative space
Text should feel like music-product advertising, not oversized presentation headings
Do not add an outer caption, creator watermark, decorative footer, or progress counter
</art_direction>

<artwork> Create original square album artwork for a fictional track called “Glass Tides” by “AURA”
The hero cover is an abstract macro image of flowing pearlescent liquid silk and molten glass
Use pastel lavender, powder cyan, blush pink, champagne gold, and subtle mint
Include broad three-dimensional folds, realistic reflective highlights, delicate striations, and a prominent sweeping S-shaped fold
Fill the square edge to edge
No text, logo, or border on this hero artwork
Use this same artwork consistently throughout the film

Create additional designed playlist sleeves:
“Late Nights” in mustard yellow
“Good Energy” in pink
“Deep Focus” in blue
“Daily Mix 1”, “Daily Mix 2”, and “Daily Mix 3” in complementary colors

These should look like finished graphic-design covers, with bold typography and simple geometric motifs
</artwork>

<timeline> 0.0–0.6 seconds: A green Spotify icon grows smoothly into the center of the dark stage Give it a confident arrival with minimal overshoot
0.6–1.5 seconds:
The icon transitions into a small Spotify identity above two centered lines:
“Discover”
“new music”
The first line is white; the second is green
Reveal them with short masked vertical movements
1.5–2.4 seconds:
A stylized Spotify desktop interface rises into view
Show a slim sidebar, “Made for you”, three album cards, and small supporting rows
Use a subtle perspective tilt during the entrance, settling toward a frontal view
2.4–3.2 seconds:
Move closer to the three featured covers
Show “New for you” above them
Keep the artwork crisp, with short album titles beneath
A narrow rounded player bar now anchors the bottom of the stage
3.2–4.0 seconds:
The featured cards withdraw into a compact “Fresh finds” list
Reveal four song rows with a slight stagger
Each row contains a thumbnail, short track title, artist, and a small menu icon
4.0–4.9 seconds:
Transition into a horizontal strip of colorful playlist covers
Heading: “Every mood”
Supporting line: “Find what moves you”
The strip slides smoothly sideways, with edge cards partially cropped by the stage
4.9–5.8 seconds:
A compact search field appears
Type “Glass Tides”
Reveal one selected result beneath it, with the iridescent artwork, “AURA”, and a green play icon

5.8–6.6 seconds:
The selected artwork expands into a large centered cover
Reveal “Glass Tides” underneath, followed by “AURA” in green
Keep the player bar visible
6.6–7.5 seconds:
The same cover slides left
Track information appears on the right:
“Glass Tides”
“AURA”
“A new frequency”
Add a rounded green Play button
Coordinate the cover movement and text reveals
7.5–8.3 seconds:
A brief brand-color transformation fills the inner stage with green
The artwork contracts into a smaller centered tile
Place a small dark Spotify identity underneath
The player briefly recedes
8.3–9.8 seconds:
Return to the dark stage
The same artwork expands dramatically toward the camera, becoming oversized and cropped by the rounded stage
Restore the player at the bottom
Use controlled motion blur during the fastest part of the zoom

9.8–11.2 seconds:
The artwork clears into a centered typographic statement:
“Find your”
“rhythm”
Use white for the first line and green for the second
The player remains visible and stable beneath it
11.2–12.5 seconds:
Show “Made for your every day”
Three playlist sleeves enter with gentle perspective and small opposing tilts
They spread into six smaller sleeves across the stage
Supporting line: “Your sound, always evolving”

12.5–14.0 seconds:
The playlist layout transitions into four floating album covers
Include the iridescent hero artwork
Use restrained rotation, perspective, depth ordering, and overlap
Keep their movement coordinated rather than randomly floating
14.0–15.2 seconds:
The covers converge toward the center and fold around a green Spotify icon
The artwork withdraws as the icon becomes the focal point
Fade the player away
The Spotify icon must emerge from the same central position as the converging covers
15.2–18.0 seconds:
The icon moves slightly left and settles beside a large white “Spotify” wordmark
Keep the icon and letters separated throughout the movement
Reveal:
“Discover new music”
“every day”
The first line is white; the second is green
Hold the finished composition cleanly through the end
</timeline>
<persistent_player>
For most of the middle sequence, keep one narrow rounded player bar near the bottom of the inner stage
Include:
Small hero-art thumbnail
“Glass Tides” and “AURA”
Play and skip controls
A thin progress track
A small volume icon
Subdued dark translucent styling with a fine border
This recurring player connects the changing shots
It must remain visually secondary to the artwork
</persistent_player>

<motion_quality>
Match the energy of a tightly edited premium product film
Most visual ideas last approximately one second, but transitions remain smooth
Use continuous acceleration and deceleration
Favor critically damped springs or carefully tuned smooth easing
No repeated bouncing or large elastic overshoots
Preserve the hero artwork’s identity and position relationships through search, album detail, brand tile, and zoom
Use match-position transitions, coordinated scaling, masked reveals, and perspective
Outgoing titles must disappear before incoming titles occupy the same space
Avoid overlapping text, sudden camera resets, long blank intervals, and arbitrary full-frame crossfades
Clip every oversized cover and camera move cleanly to the rounded stage
No particles, shockwave rings, lens flares, camera shake, or unrelated stock footage
</motion_quality>

<audio> Create or select commercially usable electronic music around 120 BPM Use a clean pulse, warm bass, restrained melodic elements, and subtle transition accents Align important entrances, selections, zooms, and the logo reveal with musical events Keep effects quieter than the music No voiceover Do not use copyrighted commercial tracks without permission </audio>
<implementation_and_validation>
Build a deterministic animation driven by absolute time through an async window. seek(t) function
Every transform, opacity, mask, and UI state must be reproducible when seeking frames in any order
Do not depend on live timers, accumulated physics, or CSS transition state during export

Render true 60 fps with spatial antialiasing
Use 3–5 temporal subframe samples per output frame for restrained motion blur
Keep stationary text and artwork sharp
Inspect contact sheets and moving playback
Check the fast heading changes, artwork handoffs, zoom, cover convergence, and final wordmark spacing
Verify evenly spaced frame timestamps and the full 18-second duration
Fix visual defects before delivering the final MP4 and editable source
</implementation_and_validation>
```

## #64 Poster breaking its frame
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@pankajkumar_dev](https://prompt-motion.com/pankajkumar-dev-0bee87)

```text
create a motion design video of a poster breaking out of its own frame.
```

## #65 DistilBook motion explainer  (×2 authors)
- Type: Prompt · Effort: — · Posted: Sep 29, 2026 · Aspect: — · Duration: 30.0s
- By: [@sudo_kiran](https://prompt-motion.com/sudo-kiran-b055de), [@sudo_kiran](https://prompt-motion.com/sudo-kiran-4f8b59)
- Tags: explainer, product-promo
- Titles of variants: DistilBook motion explainer; DistilBook product explainer

```text
make a dynamic 30-seconds motion graphic video about the distilbook like a product explainer the video has to be very incredible (product url)
```

## #67 Animated agent session story
- Type: Skill · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@jake11moran](https://prompt-motion.com/jake11moran-a269c4)
- Tags: narrative-short, product-promo · Tech: hyperframes
- Skill/repo: https://github.com/heygen-com/hyperframes-community-skills/tree/master/skills/session-story

```text
Has your agent read your local Claude Code history and turn a typical session with you into a short scored animated film rendered in HyperFrames.

npx skills add heygen-com/hyperframes-community-skills --skill session-story
```

## #68 Pixelup Labs studio showreel
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: 15.0s
- By: [@arjunsh1607](https://prompt-motion.com/arjunsh1607-93005d)
- Tags: pixel-art, showreel

```text
create a 15 sec motion graphics showreel for @pixeluplabs, be extremely detail oriented and go all out
```

## #69 Claude motion reel
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@codeSTACKr](https://prompt-motion.com/codestackr-c071bf)
- Tags: showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a resume. go all out
```

## #70 Browser automation skill launch
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 20.0s
- By: [@hqmank](https://prompt-motion.com/hqmank-7c61f1)
- Tags: product-promo, showreel

```text
Make a dynamic 20-second motion graphics launch video for my open-source project jev-browser-skill ('Give a site. Write a goal. Jev clicks.'), like it's the hero video on its GitHub README. Go all out.
```

## #71 founder.page launch video
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 20.0s
- By: [@RatheeJaisal](https://prompt-motion.com/ratheejaisal-1f4538)
- Tags: product-promo

```text
build me a beautiful launch video 20 seconds or under that shows all our key features, make it fast paced and fit our brand
```

## #72 What day is it
- Type: Prompt · Effort: — · Posted: Oct 2, 2026 · Aspect: — · Duration: 30.0s
- By: [@tankazunori0914](https://prompt-motion.com/tankazunori0914-0fc886)

```text
今日何曜日だっけ？BGM付きの30秒のかっこいいモーショングラフィックスで教えて（全力を出してください）
```

## #73 Alan agent platform promo
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@prasad_pilla](https://prompt-motion.com/prasad-pilla-2c0cba)
- Tags: product-promo, showreel

```text
make a dynamic 15 second motion graphics video that shows what an incredible motion designer you are, for @tryAlanAI. go all out.
```

## #74 Sahi trading terminal reveal
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: 16:9 · Duration: —s
- By: [@dale_vaz](https://prompt-motion.com/dale-vaz-cc612a)
- Tags: data-viz, ui-motion · Tech: camera-moves, single-html

```text
create a self contained aesthetically pleasing, breathtaking animation of the Sahi Trading Terminal. it should start with a single dot on a black screen and then have multiple windows show up on the screen such as Charts, Positons , Option Chain, Watchlist. And zoom into and out at multiple scales. Finally the camera zooms out to make the desktop look like a point in space. And then it zooms back in to reveal a mobile screen in landscape mode with a chart in one half and an option chain in another. The video ends in Sjngle Screen Trading on SAHI
use javascript for it. be detailed and accurate. it should be visually stunning
```

## #75 White Russian recipe animation
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 30.0s
- By: [@Sarut0biSasuke](https://prompt-motion.com/sarut0bisasuke-cefa43)
- Tags: explainer, recipe-process

```text
Render a recipe motion graphic animation using JavaScript or HTML (whatever you think will produce the best result) to show the full recipe for a White Russian from start to finish, empty glass to completed cocktail. Explainer video style, showing the ingredients and measurements as they go into the glass. It should be a 30s video.
```

## #76 ODATANO Cardano hype edit
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@maxalexweber](https://prompt-motion.com/maxalexweber-67688b)
- Tags: product-promo

```text
Make a ODATANO edit that goes hard
```

## #77 AI Arena product promo
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: 16:9 · Duration: —s
- By: [@ezshine](https://prompt-motion.com/ezshine-c90d73)
- Tags: product-promo

```text
设计个动画，介绍本项目的各项特性，像是专业的产品介绍宣传片，最后要生成 16:9 的mp4 视频
```

## #78 Motion design showreel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@samuel_spitz](https://prompt-motion.com/samuel-spitz-974923)
- Tags: showreel

```text
Create a motion graphics video that feels like the centerpiece of a world-class designer’s showreel. Treat it as your résumé: showcase your full range, push the craft as far as possible. Go all out.
```

## #79 Replica symmetry breaking whiteboard
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@tak3sh8](https://prompt-motion.com/tak3sh8-be5012)
- Tags: explainer, math, retro-print-style

```text
Prompt 1: "Do a quick hand-drawn whiteboard animations explaining what is replica symmetry breaking in the SK model"

Prompt 2: "build the mp4 version with narration"
```

## #80 Full Stop figure sequence
- Type: Prompt · Effort: Max · Posted: Oct 5, 2026 · Aspect: — · Duration: —s
- By: [@HBCoop_](https://prompt-motion.com/hbcoop-de365c)

```text
Create me a motion video of your choice, with the sole purpose of flexing Opus 5.5 capabilities.
```

## #81 Stock analysis app promo
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@AIStockSavvy](https://prompt-motion.com/aistocksavvy-3fb9f5)
- Tags: product-promo

```text
Create a bold, dynamic 15-second motion graphics video that showcases your best motion design skills as if it’s the highlight of your portfolio for a dream job. Bring sharp timing, smooth transitions, and standout visuals. Push your creativity and make every second count.
```

## #82 Visual guides library launch
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@techyoutbe](https://prompt-motion.com/techyoutbe-945b56)
- Tags: product-promo

```text
I want you to create a highly professional SaaS product launch video. Go and find some SaaS, preferably just one that people know, so it's easier to identify with it. Pick that, and then make sure to get actual assets and images and all of that stuff from the internet. Turn it into these typical, very professionally edited, motion-graphics-styled product launch videos that you see people making on Twitter when they launch new SaaS products (which are showing off the features, the benefits, and all of these things)
```

## #83 GravityDEX anime hype edit
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@MicheleHarmonic](https://prompt-motion.com/micheleharmonic-77628e)
- Tags: product-promo

```text
Make a GravityDEX x Gojo Satoru edit that goes hard
```

## #84 Whiteboard skill tutorial
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: —s
- By: [@lemomo_ai](https://prompt-motion.com/lemomo-ai-0d9cff)
- Tags: explainer, retro-print-style

```text
Create a tutorial video explaining how to create videos using Lemo-Opuscar skill (Opus 5.5) , in a [Whiteboard Explainer] style.  One prompt, one answer, then ship film.
```

## #85 Moroccan political history timeline
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@TrigLyceee](https://prompt-motion.com/triglyceee-bd5b08)
- Tags: narrative-short

```text
réalise une vidéo résumant la vie politique au Maroc depuis l’indépendance
```

## #86 Kinetic type showreel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@zheke](https://prompt-motion.com/zheke-38deff)
- Tags: kinetic-type, showreel

```text
Hello Opus 5.5 show me what an incredible motion designer you are.
```

## #87 Tennis game launch video
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@deifosv](https://prompt-motion.com/deifosv-04e4d3)
- Tags: data-viz, game-interactive, product-promo

```text
Create a high energy launch video, showing live stats from the website, show that users can play on desktop and mobile and multiple themes, if need, give me a prompt to generate the song using Suno
```

## #88 Flexprice motion showreel
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@sudeepsd_](https://prompt-motion.com/sudeepsd-1a3485)
- Tags: showreel

```text
make a dynamic 15-second motion graphics video of what you know about @tryflexprice that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out.
```

## #89 Tally product demo
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@VisheshBaghell](https://prompt-motion.com/visheshbaghell-3aba37)
- Tags: product-promo

```text
build me a product demo for my site using /brag skill. make sure to emphasize on all features
```

## #90 Sherwood agentic hedge fund explainer
- Type: Prompt · Effort: — · Posted: Sep 23, 2026 · Aspect: — · Duration: —s
- By: [@imthatcarlos](https://prompt-motion.com/imthatcarlos-e04bfe)
- Tags: explainer, product-promo, ui-motion

```text
make a modern slick and punchy video for sherwood protocol. feel free to take branding or components from the landing page or app. the goal is to highlight how it enables agentic hedge funds, explaining it simply
```

## #91 Mascot referral program promo
- Type: Prompt · Effort: — · Posted: Sep 28, 2026 · Aspect: — · Duration: 15.0s
- By: [@paulo_kombucha](https://prompt-motion.com/paulo-kombucha-96431c)
- Tags: product-promo

```text
make a dynamic 15-second motion graphics video to talk about our referral program
```

## #92 Steam new releases news recap
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: 60.0s
- By: [@gigabit_million](https://prompt-motion.com/gigabit-million-16b3a0)

```text
9月25日～9月26日にSteamにリリースされたゲームの紹介ニュースを、ゲーマーの目線で各ゲームの面白そうなポイントをわかるように、見やすい約60秒ぐらいのモーショングラフィックスで作ってください
```

## #93 DistilBook product explainer
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 30.0s
- By: [@sudo_kiran](https://prompt-motion.com/sudo-kiran-6609ed)
- Tags: explainer, music-sync, product-promo · Tech: generated-audio

```text
create best motion graphics explainer of the (your product) with very good script and good design colors and good music make sure the video should be incredible and people should feels like watch it many times.. it has to be in 30 seconds good and very intresting, it has to be best of the best of the best of the best video
(product link)
```

## #95 Supademo launch video
- Type: Prompt · Effort: Max · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@jhylee95](https://prompt-motion.com/jhylee95-e1152f)
- Tags: music-sync, product-promo, ui-motion · Tech: generated-audio

```text
You're a world-class motion designer building a Supademo launch video. Research and land our core value and narrative. Scenes should be dynamic and confident: hook in the first second, then distinct beats for product proof and AI. Brand-accurate UI, type, color, and motion. Score the music so every cut, animation hit, and scene change lands on a beat or drop; retimed until synced. Social energy, quick cuts
```

## #96 Norilu product launch video
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@sachaarbonel](https://prompt-motion.com/sachaarbonel-8f14f4)
- Tags: product-promo

```text
Create a professional product launch video with motion graphics. You have access to the designs in pen
```

## #97 Speech built as architecture
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: 9:16, 1:1 · Duration: 20.0s
- By: [@Gdgtify](https://prompt-motion.com/gdgtify-287ddf)
- Tags: kinetic-type, loop, music-sync, narrative-short, recipe-process, retro-print-style, ui-motion · Tech: camera-moves, canvas, deterministic-seek, generated-audio, single-html, svg

```text
Create a 20.00-second kinetic spoken-word film titled “BUILD THE FLOOR.”  Treat this as an original miniature speech staged entirely through typography. Every line changes the architecture of the frame. The final declaration must stand on something the earlier words physically constructed.  Deliver one self-contained HTML file, 1080×1080, targeting 60fps, using SVG and/or Canvas. Embed all required assets.  ART DIRECTION Background #102820. Paper # F4E9D5. Structural accent # F2B544. A literary editorial world with the scale and confidence of a public monument. Use a high-contrast serif for the speech, a heavy grotesque for load-bearing words, and a restrained monospace for small timing marks. No distressed protest-poster clichés, megaphones, flags, crowds, microphones, or stock footage.  ORIGINAL SPEECH — EXACT WORDS, EXACT ORDER “We were told to wait.” “So we learned the weight of waiting.” “Then one voice made room.” “Then another.” “Now the floor belongs to us.”  Do not attribute these words to any real person. No extra slogans. The complete speech must be understandable without audio.  CENTRAL VISUAL RULE Words have assigned architectural roles. WAIT is a lintel. WAITING is a suspended load. VOICE is a support. ROOM is an opening. FLOOR is a platform. These roles must emerge from the actual letterforms, not from separate illustrations placed behind text.  STORYBOARD 0.00–3.00 “We were told to wait.” The sentence occupies a narrow horizontal opening beneath a massive WAIT. The opening slowly compresses while the sentence remains readable. The pressure comes from the layout, not camera shake.  3.00–6.50 “So we learned the weight of waiting.” Reveal the sentence in spoken phrase groups. WAITING lowers on two fine vertical rules. Those rules become suspension cables. A baseline bends under the visual load using a controlled vector deformation.  6.50–10.00 “Then one voice made room.” VOICE enters vertically and rotates into a structural support. It lifts one end of the baseline. The counter of the O in ROOM becomes an aperture. The next composition is revealed through that aperture.  10.00–12.50 “Then another.” A second support arrives. The tilted structure levels. This is the first moment of perfect horizontal alignment in the film. Use a brief stillness to make the change feel earned.  12.50–16.00 “Now the floor belongs to us.” Earlier structural words assemble into a platform. The final sentence settles onto it. US receives emphasis through shared alignment and scale, never through a separate flashy effect.  16.00–18.00 Hold the complete declaration. A slight release of tension travels through the supporting rules. No new text. No restless decorative motion.  18.00–20.00 The camera tracks beneath the completed platform. Its underside fills the frame and becomes the opening WAIT lintel. Under full occlusion, return hidden elements to their initial positions. Reveal the exact opening composition.  CHOREOGRAPHY Do not force the speech onto a dance beat. Use a cue sheet based on phrases, pauses, and emphasis. Phrase reveals should follow reading order. Allow at least one 400ms moment of absolute stillness. Use critically damped motion for settling loads. Use controlled elastic deformation for the baseline only. Make the changes in available space carry the emotional progression.  TYPE IMPLEMENTATION Use actual glyph paths for structural words. Preserve counters and legibility during deformation. For transitions between unrelated words, use occlusion or matched structural edges; do not interpolate arbitrary path points. Keep the currently spoken phrase readable before it becomes architecture.  ENGINEERING Implement window. seek(t) as a deterministic scene renderer. No accumulated physics, autonomous CSS transitions, or changing random values. Use time-remapping curves and analytic transforms. Use a 20-second periodic timeline with render(0)=render(20). Provide fixed-step access at n/60 for 1200 export frames. Audio is optional and off by default; no browser speech synthesis or autoplay dependency.  QUALITY GATE Inspect eight representative frames. Check that the speech reads in the correct order. Check that structural transformations never destroy a line before the audience can read it. Check the final platform is visibly assembled from earlier elements. Return the complete HTML implementation.
```

## #98 Five scroll-based sections
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@ercankeskinx](https://prompt-motion.com/ercankeskinx-ec2568)
- Tags: game-interactive

```text
Build 5 completely different scroll-based sections, decide the context & layout yourself.
```

## #99 fal motion design showreel
- Type: Prompt · Effort: — · Posted: Sep 29, 2026 · Aspect: — · Duration: 15.0s
- By: [@influencer_seo](https://prompt-motion.com/influencer-seo-ce8c33)
- Tags: showreel

```text
make a dynamic 15-second motion graphics video for @fal that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out. Use the fal API.
```

## #100 Trezio app motion reel
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: 15.0s
- By: [@agonaliu_](https://prompt-motion.com/agonaliu-466a8f)
- Tags: product-promo, showreel

```text
Make a dynamic 15-second motion graphics video for Trezio app that shows what an incredible motion designer you are, like it's your showreel for a résumé. Get it!
```

## #101 Taxtello bookkeeping app film
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: 9:16, 16:9 · Duration: 15.0s
- By: [@daniel_haida](https://prompt-motion.com/daniel-haida-8691d4)
- Tags: 3d, data-viz, explainer, kinetic-type, music-sync, narrative-short, product-promo, retro-print-style, showreel, ui-motion · Tech: camera-moves, deterministic-seek, generated-audio, remotion, springs, svg

```text
You are the senior motion designer, product designer and Remotion engineer for Taxtello.

Your task is to create a genuinely premium, Apple-level product film for Taxtello.

This is NOT a generic SaaS explainer.
This is NOT a feature walkthrough.
This is NOT a startup template animation.

I want a maximum 15-second brand/product showreel that makes Taxtello look like a mature, expensive, beautifully designed financial product.

Think:

Apple product launch film
× premium fintech
× editorial motion design
× restrained Stripe-like product presentation
× Taxtello's own visual identity

The desired reaction is:

“Wait, this is a German bookkeeping app?”

The film should feel expensive.

────────────────────────────────────
REPO / SOURCE OF TRUTH
────────────────────────────────────

First inspect the real repositories before designing anything.

Main product:
  /taxtello/main

Existing Remotion project:
  /taxtello/beta-motion

Important real brand sources:

  /taxtello/main/public/css/app/_00-tokens.css
  /taxtello/main/docs/design/TOKENS.md
  /taxtello/main/public/taxtello-wordmark.png
  /taxtello/main/public/icons.svg

Existing current product screenshots can be found under:

  /taxtello/main/artifacts/smoke-ui-smoke/

Prefer the newest valid screenshots/current source over stale artifacts.

There is already an existing 24-second Remotion hero animation in
/taxtello/beta-motion.

DO NOT replace it.
DO NOT regress it.
DO NOT force its current AI-connections storyline into this new film.

Create a new independent composition for this task, e.g.

  TaxtelloShowreel15

You may reuse good infrastructure, fonts, rendering utilities, motion primitives,
easing curves, asset loading and QA infrastructure from beta-motion where useful.

But creatively this should be a new film.

Before implementation, inspect the actual Taxtello UI and understand the product.

Do not invent functionality that does not exist.

────────────────────────────────────
REAL TAXTELLO VISUAL LANGUAGE
────────────────────────────────────

Use the real design system.

Core palette:

Background:
  #0c0f1a

Elevated surfaces:
  #111525
  #131722
  #1a2032

Primary brand gold:
  #e8b84b

Gold highlight:
  #f5d07a

Gold depth:
  #9b6d18

Primary text:
  #e8eaf2

Strong warm white:
  #f6f4eb

Secondary text:
  #8b93b5

Positive:
  #34d399

Negative/error only where semantically necessary:
  #f87171

Typography:
  Plus Jakarta Sans

Numbers / financial values where appropriate:
  JetBrains Mono

Use the actual Taxtello wordmark and/or Taxtello mark.
Do not redraw or approximate the logo.

Taxtello's gold should feel like a precious accent, not a yellow UI flood.

Think:
dark metal
warm gold
glass
ink
precision
quiet confidence

NOT:
cyberpunk
crypto
neon
gaming
generic AI purple
rainbow gradients

────────────────────────────────────
CORE CREATIVE RULES
────────────────────────────────────

Follow these rules ruthlessly:

1. ONE SHOT = ONE IDEA.

2. Every scene needs room to breathe.

3. The product UI is the hero.

4. Do not plaster explanatory copy everywhere.

5. Do not use hard cuts unless there is a deliberate reason.

6. Prefer object-driven transitions:
   a card becomes the next card,
   a chart line becomes a connector,
   a receipt becomes a booking,
   a number becomes another interface element,
   the camera moves through the product.

7. Use premium easing.
   No linear movement.

8. Motion should overlap naturally.
   Elements should not all start and stop at exactly the same frame.

9. Use depth sparingly:
   perspective,
   soft parallax,
   scale,
   foreground/background separation,
   controlled depth of field if achievable.

10. NO effect exists simply because it looks cool.

11. No particle spam.

12. No fake glassmorphism everywhere.

13. No excessive blur.

14. No pointless 3D spinning cards.

15. No constant zooming.

16. No 20 different animation styles.

17. No bouncing UI.

18. No giant marketing paragraph.

19. Do not imitate a particular Apple commercial shot-for-shot.
    Capture the philosophy and production quality instead.

The visual confidence should come from restraint.

────────────────────────────────────
FORMAT
────────────────────────────────────

Primary master:

1920 × 1080
60 fps
16:9
H.264
maximum duration: 15.0 seconds

Target runtime:
approximately 14.0–15.0 seconds.

It must work as a social-media product reveal even without sound.

If practical AFTER the master is finished, also create a deliberately recomposed
vertical/social variant.

Do not merely crop the desktop composition.

But the desktop master is the priority.

────────────────────────────────────
STORY / EMOTIONAL ARC
────────────────────────────────────

Do not make this a list of five features.

It should feel like one continuous thought:

CHAOS → CONTROL → CLARITY → TAXTELLO

The first 1.5 seconds must already look premium.

The first meaningful product moment should happen by ~2 seconds.

No five-second logo intro.

Possible narrative direction:

“Everything about your business, finally in one place.”

But SHOW this instead of explaining it.

I want approximately four visual ideas across the whole film.

Use the strongest REAL Taxtello surfaces you find in the repository.

Strong candidates include:

• Finanzcockpit / Dashboard
• Rechnungen
• Belege
• Bank / matching
• Steuergesundheit / tax overview

You do NOT need to show all of them.

Choose the visually strongest combination.

────────────────────────────────────
SUGGESTED 15-SECOND STORYBOARD
────────────────────────────────────

Treat this as a strong starting point, not a rigid template.

0.00 – 1.20

BLACK / NAVY.

A tiny warm-gold glint appears.

The glint elegantly reveals either the Taxtello mark or a fragment of the
wordmark.

No generic logo fade.

Think machined precision.

The camera moves through or past the mark and the UI begins to emerge from it.

Very little or no copy.

─────────────────

1.20 – 4.40

FINANCIAL CONTROL.

Reveal the actual Taxtello Cockpit as a dimensional product surface.

Not just a screenshot placed on screen.

Reconstruct/crop/layer it so individual interface regions can animate.

The hero financial number resolves crisply.
The chart draws in.
Supporting metrics settle slightly later.

Use subtle stagger.

A single line of copy may appear, for example:

  “Alles im Blick.”

or another equally short German phrase if you find something more fitting.

Maximum ~3–4 words.

The interface must remain recognizable as the real product.

─────────────────

4.40 – 7.50

DOCUMENT / BOOKKEEPING TRANSFORMATION.

Use a visual object from the previous scene as the transition.

Example:

A gold chart point expands into the corner of a receipt/card.
The camera follows it.
A receipt/document enters.
Taxtello identifies or organizes it.
The document snaps elegantly into its corresponding booking / financial record.

Use magnetic alignment and precision.

No cheesy scanner laser.

No floating paper tornado.

Possible micro-copy:

  “Belege. Erledigt.”

Only if it improves the scene.

─────────────────

7.50 – 10.70

MONEY / INVOICES.

Morph or transition naturally into the real Rechnungen interface.

Use one strong moment:

an invoice status changes,
a payment resolves,
an amount moves into place,
or the overview assembles itself.

Numbers should feel tactile and precise.

Use JetBrains Mono where this matches the actual product.

Gold highlights the active state.

Green is used only for a genuinely positive semantic state.

Potential copy:

  “Geld. Im Griff.”

Again: optional and extremely short.

─────────────────

10.70 – 12.80

TAX / CLARITY.

Transition into the real Taxtello tax-health / financial guidance surface.

Do not claim that Taxtello magically guarantees correct taxes.

Communicate visibility and control.

Example:

multiple noisy signals collapse into one calm, structured tax overview.

Potential copy:

  “Steuern im Blick.”

This scene should feel calmer than the previous scene.

The rhythm briefly slows.

─────────────────

12.80 – 15.00

BRAND PAYOFF.

Pull the camera outward.

The UI compresses or folds into one beautiful Taxtello product object / surface.

Darkness returns around it.

The gold Taxtello wordmark resolves.

One short brand line underneath.

Explore strong final lines such as:

  “Dein Business. Klar.”

  “Buchhaltung. Unter Kontrolle.”

  “Einfach mehr Überblick.”

  “Alles fürs Business. An einem Ort.”

Choose based on the actual product positioning you find in the repo.

Do not use a line simply because I suggested it.

The final frame must have enough stillness to register.

End confidently.

No giant bouncing CTA.

────────────────────────────────────
TRANSITIONS
────────────────────────────────────

This is one of the most important parts.

I want transitions that make the viewer think:

“Of course the next scene came from that.”

Good:

chart line → document edge
gold pill → invoice button
financial number → amount in invoice
card edge → next surface
camera push through interface element
shared geometry
mask reveal using actual product shapes

Bad:

crossfade
random wipe
spin transition
glitch
whip-pan every two seconds
generic SaaS slide-left
zoom-blur spam

Direct cuts are allowed only when a deliberate rhythmic impact benefits the film.

────────────────────────────────────
MOTION
────────────────────────────────────

Motion needs weight.

Use curves comparable to:

cubic-bezier(0.16, 1, 0.3, 1)

where appropriate.

Different elements should have subtly different arrival times.

Prefer:

anticipation
overshoot below ~2%
settling
motion continuation
shared velocity between scenes

Avoid cartoon springiness.

Camera movement should feel like a high-end macro product shoot.

Imagine we are filming a physical premium object even though it is software.

────────────────────────────────────
LIGHTING / MATERIAL
────────────────────────────────────

Use extremely subtle environmental lighting.

Possible treatments:

• soft gold rim lighting
• dark navy falloff
• faint ambient bloom
• soft specular highlight passing across a surface
• restrained vignette
• subtle grain if it materially helps

Keep the interface crisp.

Do NOT blur the product just to look cinematic.

No fake glossy reflections that destroy legibility.

────────────────────────────────────
TYPOGRAPHY
────────────────────────────────────

Use very little copy.

No sentence should compete with the product.

Headlines should generally fit on one line.

Use Plus Jakarta Sans.

Strong typography may occasionally scale very large and become a transition
device itself.

Avoid generic motion-graphics behavior where every word animates independently.

Typography should move as designed objects.

────────────────────────────────────
SOUND / RHYTHM
────────────────────────────────────

Design the motion as if it were cut to approximately 115–120 BPM:
premium, kinetic, sophisticated, not frantic.

Important moments should land musically.

Suggested sound language:

• low soft impact for major reveal
• restrained tactile UI clicks
• subtle metallic/glass tonal tick
• soft low-frequency movement during camera transitions
• elegant resolved tone at the logo payoff

Avoid:

• huge cinematic trailer boom
• EDM risers
• loud whooshes everywhere
• stock “tech interface” sounds
• rap beat
• aggressive bass

If there is no legally safe music/audio asset in the project, DO NOT pull
copyrighted audio from the internet.

Deliver the visual master without copyrighted music and create a concise cue
sheet describing where music/SFX should hit.

If suitable safe/local audio exists, use it.

────────────────────────────────────
REAL PRODUCT ONLY
────────────────────────────────────

This is critical.

Inspect current main.

Do not invent screens.

Do not invent metrics that imply real customer data.

Use clearly synthetic/demo-safe values if required.

Do not accidentally expose any personal, test-user or production information.

Reuse the visual structure of the actual Taxtello UI.

If a screen needs to be motion-separated, recreate it faithfully in React from
the real design system instead of simply scaling a giant screenshot.

The result should still look unmistakably like Taxtello.

────────────────────────────────────
IMPLEMENTATION EXPECTATIONS
────────────────────────────────────

Work directly in:

  /taxtello/beta-motion

Create the new composition alongside the existing one.

Keep existing compositions working.

Structure the new work cleanly.

Prefer reusable primitives for:

• camera surface
• product frame
• masked transitions
• text reveals
• UI region reveals
• ambient lighting
• shared-element transitions

Avoid one 1,500-line component.

Use deterministic Remotion animation driven by frame/time.

No setTimeout.
No nondeterministic animations.

Respect 60 fps throughout.

Use interpolation/spring/easing deliberately.

────────────────────────────────────
DO NOT STOP AFTER FIRST IMPLEMENTATION
────────────────────────────────────

This is a visual task.

You MUST review the actual rendered output.

Required workflow:

1. Inspect repository and real brand/product.

2. Write a concise storyboard with:
   - exact timestamps
   - key visual
   - transition logic
   - copy
   - intended emotional rhythm

3. Implement it.

4. Run typecheck / relevant checks.

5. Render representative frames at roughly:
   0.0 s
   1.0 s
   2.5 s
   4.5 s
   6.5 s
   8.5 s
   10.5 s
   12.5 s
   14.0 s
   14.8 s

6. VISUALLY INSPECT THOSE IMAGES.

Do not merely confirm that rendering succeeded.

Ask:

Does this look like an Apple-tier product film?

Does anything look like a template?

Is there too much on screen?

Is the product legible?

Are transitions logically connected?

Does Taxtello gold feel premium?

Does every frame look composed?

7. Fix visual weaknesses.

8. Render the complete film.

9. Inspect multiple exact decoded frames from the final MP4, not only browser
   screenshots.

10. Iterate again if necessary.

Do not declare success because the code compiles.

The deliverable is the FILM.

────────────────────────────────────
QUALITY BAR
────────────────────────────────────

Reject your own result if it feels like:

• a SaaS template
• a PowerPoint animation
• a website screen recording
• a generic Remotion demo
• a crypto advertisement
• an AI-generated promo template
• five screenshots sliding around
• excessive marketing copy

Every important frame should be good enough to use as a still advertisement.

I would rather have:

3 extraordinary visual moments

than

10 mediocre feature animations.

────────────────────────────────────
FINAL DELIVERABLES
────────────────────────────────────

Provide:

1. Final storyboard
2. New Remotion composition source
3. 1920×1080 / 60fps final MP4
4. Poster/final frame
5. Contact sheet with representative frames from the film
6. Exact runtime
7. List of real Taxtello assets/screens used
8. Brief explanation of the motion language
9. Any remaining visual compromises
10. Commands to reproduce the render

Save outputs in a clearly named directory such as:

  /taxtello/beta-motion/out/showreel-15/

Do not deploy anything.
Do not modify production data.
Do not merge anything.

Go all out creatively, but exercise ruthless restraint.

Make Taxtello look expensive.
```

## #102 Badge unlock screen animation
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@BThreeAgency](https://prompt-motion.com/bthreeagency-b9b8d9)
- Tags: 3d, game-interactive, ui-motion

```text
Using the linked Figma frame build a badge unlock screen. Match the design exactly. Use the file's assets, lighting, type and layout and add only the motion. Animate the badge so it feels premium and celebratory. Build its scene and then celebrate with gold particles. Treat the badge as a solid 3D object that tilts toward the
cursor following the rules of physics. Keep it fast and smooth, it should not be bouncy.
```

## #103 Prompting mistakes video tutorial
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@henkvaness](https://prompt-motion.com/henkvaness-0e06af)
- Tags: explainer

```text
make educational video out of article.
```

## #104 Motion designer portrait showreel
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: 9:16 · Duration: 15.0s
- By: [@ndhabarde11](https://prompt-motion.com/ndhabarde11-f155b4)
- Tags: showreel

```text
make a dynamic 15-second motion graphics video in portrait mode that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out.
```

## #105 Kinetic type motion showreel
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: 15.0s
- By: [@_topi_003](https://prompt-motion.com/topi-003-9ca6b5)
- Tags: kinetic-type, showreel

```text
あなたがどれほど素晴らしいモーションデザイナーかを示す、ダイナミックな15秒のモーショングラフィックスビデオを作成してください。履歴書用のショーリールのような感じで、全力でやって。
```

## #106 Claude motion design showreel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@rendesr](https://prompt-motion.com/rendesr-86be44)
- Tags: showreel

```text
Make a dynamic 15 second motion graphics video that shows off what an incredible motion designer you are. Imagine it's your showreel for a resume!
```

## #107 Product intro synced to music
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: —s
- By: [@BogdanDragomir](https://prompt-motion.com/bogdandragomir-35e024)
- Tags: music-sync, product-promo · Tech: generated-audio

```text
Create an intro for https://t.co/wQXZTaqf1b highlighting what it does.

Create the music too and make sure the video is synced with it.

Give your best, Ultracode, as if it’s your portfolio master piece.
```

## #108 Website analyzer product promo
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: 15.0s
- By: [@en______ra](https://prompt-motion.com/en-ra-81c6dd)
- Tags: product-promo, showreel

```text
make a dynamic 15-second motion graphics video for RedSeed AI (Replace with your Project) that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out.
```

## #109 Ondefica app motion reel
- Type: Prompt · Effort: Max · Posted: Sep 27, 2026 · Aspect: — · Duration: —s
- By: [@jesscaroline7](https://prompt-motion.com/jesscaroline7-1ff7cb)
- Tags: product-promo, showreel

```text
make a dynamic motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out
```

## #110 Second brain service promo
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: 15.0s
- By: [@TheViableEdge](https://prompt-motion.com/theviableedge-9065be)
- Tags: product-promo, showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, and can be the hero asset for the course landing page.
```

## #111 AIsa API key promo
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@0xfemyn](https://prompt-motion.com/0xfemyn-e114d3)
- Tags: product-promo, showreel

```text
make a dynamic 15-second motion graphics video for AIsa. Go all out.
```

## #113 Chunku product promo
- Type: Prompt · Effort: — · Posted: Sep 30, 2026 · Aspect: — · Duration: 10.0s
- By: [@reyzostyle](https://prompt-motion.com/reyzostyle-b55864)
- Tags: product-promo, showreel

```text
make a dynamic 10 second motion graphics video about https://t.co/Zi6zrTvzqI that shows what an incredible motion designer you are, like its your showreel for a resume. go all out
```

## #115 Bold typographic motion showreel
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@motiondsgnr](https://prompt-motion.com/motiondsgnr-9dcfa6)
- Tags: kinetic-type, showreel

```text
Make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a resume. Go all out.
```

## #116 Studio1 intro showreel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@Astrodevil_](https://prompt-motion.com/astrodevil-3f2054)
- Tags: product-promo, showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible work Studio1 is doing, you will get relevant info from case study, create like it's a good showreel for a Studio1 intro launch. go all out.
```

## #117 Chuseok pixel night scene
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@hoyoyoda](https://prompt-motion.com/hoyoyoda-3a5c08)
- Tags: pixel-art

```text
한국의 추석에 어울리는 요소를 서치해서 픽셀 애니메이션을 구성해서 제작해줘
```

## #118 Ren app launch video
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 30.0s
- By: [@macrohou](https://prompt-motion.com/macrohou-33959d)
- Tags: product-promo · Tech: generated-audio

```text
[gave access to Ren repo] Make a dynamic 30-second motion graphics video for Ren that shows off your motion and sound design. Go crazy.
```

## #119 Personal research intro reel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 10.0s
- By: [@Madhav_XO](https://prompt-motion.com/madhav-xo-f97f20)

```text
make a 10 sec video on whatever you know about me
```

## #120 Three.js Skyraider aircraft model
- Type: Prompt · Effort: High · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@BuildFastWithAI](https://prompt-motion.com/buildfastwithai-ed9447)
- Tags: 3d · Tech: threejs

```text
Build a Douglas A-1H Skyraider in Three.js
```

## #121 UK dubstep track with ASCII visuals
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@Rames_Jusso](https://prompt-motion.com/rames-jusso-589f80)
- Tags: music-sync, recipe-process, retro-print-style

```text
140 BPM rusko/skream style UK dubstep
```

## #122 Anime maid dance showreel
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: 15.0s
- By: [@_topi_003](https://prompt-motion.com/topi-003-b0e12c)
- Tags: showreel

```text
この画像の女の子がエキサイトなダンスをする、ダイナミックな15秒のモーショングラフィックスビデオを作成してください。履歴書用のショーリールのような感じで、全力でやって。
```

## #123 Paper-style product launch film
- Type: Prompt · Effort: Medium · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@ik_builds](https://prompt-motion.com/ik-builds-b8bdcf)
- Tags: explainer, kinetic-type, music-sync, product-promo, retro-print-style · Tech: canvas, generated-audio, gsap, hyperframes

```text
Create a 15s motion-graphics film explaining {{PRODUCT}}. HyperFrames + GSAP, no voiceover, no footage.
Style: paper-light canvas, marker notes that draw on, real physics, huge kinetic type,
hard light/dark switches, a new idea every 1.5–2 s, a sound on every hit.

COPY: read {{POSITIONING_DOCS}} first. {{ONE_LINER}} For {{AUDIENCE}}. {{WHAT_IT_DOES}}
Name what the product learns, never the abstraction.

RULES
- No chrome (scrubber, timecode, fps, headers). No animator jargon on screen
  ("squash", "stagger", "easing"...). Every word speaks to the buyer.
- No invented results: no %, multipliers, customer names or figures.
- Never use: {{BANNED_WORDS}}.
- Logo: real mark {{LOGO_FILE}} + "{{PRODUCT}}" in {{WORDMARK_FONT}}; never a boxed logo file.

CRAFT
- Colours {{COLOR_CANVAS}} / {{COLOR_INK}} / {{COLOR_ACCENT_1}} / {{COLOR_ACCENT_2}}; notes in the
  accents; dark mode = charcoal matching the palette.
- Fonts {{BRAND_FONTS}}; Anton for kinetic type; Caveat handwriting via stroke-dashoffset.
- Real easing, squash/stretch, stagger, overlap, onion skin, smear, follow-through. Check the
  HyperFrames registry first. Set every from-state at t=0 (seek-safe); never cover an exit.
  One primary move per transition; no generic push/slide/rotate-swing.
- Music in sections: drums drop on the dark switch and while the ball is airborne, slam back
  on the type and the logo. SFX: pops, pen scribbles, whooshes, logo sub-hit. CC0 or generated
  only; log sources. Master -14 LUFS, -2 dBTP, re-measured after AAC encode.
```

## #124 Developer portfolio site showreel
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: 16:9 · Duration: 73.0s
- By: [@wani_shola](https://prompt-motion.com/wani-shola-16ca7a)
- Tags: kinetic-type, music-sync, narrative-short, product-promo, showreel · Tech: generated-audio, remotion

```text
Make a showreel-style motion graphics video for my portfolio website, https://t.co/xZFGCqi73s, using Remotion. It should show what I do as a developer relations engineer, like a showreel for my résumé.

- Use as much of the real website as possible: capture the pages and sections in a browser (home, Ask, package pages, Hire, mobile view, dark mode) and animate them inside browser and phone frames.
- Show the site's chat answering real questions about my work, with the questions and answers large and bold. Use only facts and numbers that are on the site.
- Follow premium brand rules: three colours and the site's own fonts, one idea per shot, key objects centred, space to breathe, eased motion only, smooth transitions instead of hard cuts, and a rhythm that speeds up and slows down with the story.
- Add music at about 120 BPM (elite, kinetic, sophisticated) and cut every scene on the beat. No extra sound effects.
- 1920×1080, about 90 to 100 seconds, ending on the website and my contact email.
```

## #125 Flowdrive motion showreel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@manuelogomigo](https://prompt-motion.com/manuelogomigo-f33ca9)
- Tags: showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a flowdrive. go all out.
```

## #127 Pixel wizard crypto animation
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@0xEvinho](https://prompt-motion.com/0xevinho-3777d8)
- Tags: pixel-art

```text
make a similar version but with a crypto reference
```

## #128 Fiery samurai kata
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@chrisjdimarco](https://prompt-motion.com/chrisjdimarco-f068db)

```text
make a samurai dude in only javascript and have him doing a routine in a single spot going through various seriously impressive poses and motions and positions in a fiery awesome display
```

## #129 FundMyCompute platform overview
- Type: Prompt · Effort: — · Posted: Sep 28, 2026 · Aspect: — · Duration: 20.0s
- By: [@JayScambler](https://prompt-motion.com/jayscambler-3f8889)
- Tags: showreel

```text
make a dynamic 20-second motion graphics video for fundmycompute that gives an overview of the platform and shows what an incredible motion designer you are
```

## #130 Bold Pilot SEO promo
- Type: Prompt · Effort: Medium · Posted: Sep 28, 2026 · Aspect: — · Duration: 15.0s
- By: [@utopyaszx](https://prompt-motion.com/utopyaszx-1b2f94)
- Tags: product-promo, showreel

```text
make a dynamic 15-second motion graphics video for Bold Pilot that shows what an incredible motion designer you are, like it's your showreel for a resume. go all out.
```

## #131 SaaS launch video
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: 30.0s
- By: [@aschapmann](https://prompt-motion.com/aschapmann-131210)
- Tags: kinetic-type, logo-reveal, music-sync, narrative-short, product-promo · Tech: camera-moves, generated-audio, remotion, springs, svg

```text
Act as a senior motion designer and build a 30-second launch video for [product] in Remotion, entirely in code so I can edit and re-render it: first read my landing page and codebase to pull the real story, copy, colors, font and logo file (trace the logo to SVG so it stays sharp and can be animated), then write the video as one story (why the market matters, why it's painful today, how [product] fixes it, what you get) in 4 to 5 scenes with one short title each, animate everything like a premium product film (kinetic typography word by word, spring easing, smooth camera pushes and pans, depth and glow, elements that build in on the beat instead of just appearing), keep each scene on screen long enough to read, add one soft sound effect for every element that appears and silence otherwise, and end on a memorable animated logo reveal with the tagline and URL, then render it, check the frames yourself and fix anything that overlaps, clips or feels rushed before showing me the result.
```

## #132 Step race app promo
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@marklaunches](https://prompt-motion.com/marklaunches-3b9492)
- Tags: product-promo, recipe-process

```text
build me an incredible video for my app. make it emotional.
```

## #134 Reflex brand motion reel
- Type: Prompt · Effort: Max · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@reflex_cloud](https://prompt-motion.com/reflex-cloud-72ffe5)
- Tags: kinetic-type, music-sync, product-promo, showreel · Tech: camera-moves, generated-audio

```text
You're a world-class motion designer, and this is your 15-second résumé reel. Make it dynamic and confident: open with a striking hook in the first second, build through a sequence of distinct techniques (typography, shape play, camera moves, colour shifts), and land on a clean, memorable final frame. Pacing should feel like it's cut to music. Go crazy.

Make it promote our brand, reflex. inc. Proceed as if you were starting with zero of my tools. Do not assume that the tools we already have are the best to use, as they might be outdated.
```

## #135 Sotto reading app explainer
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@1stnoel_](https://prompt-motion.com/1stnoel-c20a89)
- Tags: explainer, product-promo · Tech: generated-audio

```text
Make a 1-minute educational video about https://readsotto.app/ with synthesized voice narration.
```

## #136 Animated space cartoon episode
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: 80.0s
- By: [@Ryzoft](https://prompt-motion.com/ryzoft-4f85bd)
- Tags: 3d, narrative-short · Tech: threejs

```text
I want you to imagine a story. And then using threejs I want you to create full animation, star wars 80s-level quality 90s cartoon out of the story you imagine.
```

## #137 Animated short about a bug
- Type: Prompt · Effort: — · Posted: Sep 23, 2026 · Aspect: — · Duration: 90.0s
- By: [@KamStudioLabs](https://prompt-motion.com/kamstudiolabs-c9bb28)
- Tags: narrative-short

```text
Make a 90-second animated short film about a bug that doesn't want to be fixed.
```

## #138 Dubz Up motion showreel
- Type: Prompt · Effort: — · Posted: Sep 29, 2026 · Aspect: — · Duration: —s
- By: [@Devius_Maximus](https://prompt-motion.com/devius-maximus-beab45)
- Tags: showreel

```text
make a dynamic motion graphics video for our project dubz up, show what an incredible motion designer you are, like it's your showreel for a résumé. go all out.
```

## #139 Muse connector tracker promo
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: —s
- By: [@elliot_garreffa](https://prompt-motion.com/elliot-garreffa-f334bc)
- Tags: narrative-short, product-promo, showreel · Tech: remotion

```text
Give it your product URL and brand guidelines plus one or two reference videos, list any specific features you want in a storyboard first, and use Remotion to build it.

make this a dynamic motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out.
```

## #140 Fitters Bible app promo
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@Adamdesgns](https://prompt-motion.com/adamdesgns-478d6d)
- Tags: product-promo, showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out. (About the pipefitters bible)
```

## #141 Studio website showreel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@andginja](https://prompt-motion.com/andginja-333d32)
- Tags: showreel

```text
make a 15-second showreel about my website. Go all out.
```

## #142 PicTwin AI app ad
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@l3d1c](https://prompt-motion.com/l3d1c-0e35a3)
- Tags: product-promo

```text
create a motion design prompt for an ad for our site
```

## #143 Supasito launch video
- Type: Prompt · Effort: — · Posted: Oct 1, 2026 · Aspect: — · Duration: 15.0s
- By: [@wozu_co](https://prompt-motion.com/wozu-co-242285)
- Tags: product-promo

```text
please create me a motion design / launch video for supasito dot com it should be under 15 seconds.
```

## #144 Indian civilisation history film
- Type: Prompt · Effort: — · Posted: Sep 28, 2026 · Aspect: — · Duration: —s
- By: [@BuildFastWithAI](https://prompt-motion.com/buildfastwithai-53234e)
- Tags: music-sync, narrative-short · Tech: generated-audio
- Skill/repo: https://github.com/buildfastwithai/buildfast-skills/tree/main/generative-film-skill

```text
generate a creative mp4 video on indian civilisation with music and sound effects.
```

## #145 Anime robot combining sequence
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: —s
- By: [@allforbigfire](https://prompt-motion.com/allforbigfire-86ff3c)
- Tags: 3d

```text
もしかしてロボットアニメみたいな3機の乗り物が変形合体してロボットになるシーンもアニメ風3D CGで作れますか。
```

## #146 YouTube transcript product ad
- Type: Prompt · Effort: — · Posted: Sep 27, 2026 · Aspect: — · Duration: 15.0s
- By: [@tstfully](https://prompt-motion.com/tstfully-0aa6b4)
- Tags: product-promo

```text
make a 15-second motion graphics product ad: paste a YouTube video, get every word.
```

## #147 Bento.surf product video
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 40.0s
- By: [@bizibeast](https://prompt-motion.com/bizibeast-10f264)
- Tags: product-promo, showreel

```text
Research Bento.surf. Make a dynamic 40-second motion graphics video on Bento.surf that shows what an incredible motion designer you are. like it's your showreel - Go all out.
```

## #148 Portfolio motion reel
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 30.0s
- By: [@heyiammallik](https://prompt-motion.com/heyiammallik-e72d17)
- Tags:  · Tech: generated-audio

```text
you are a pro motion designer. analyze my portfolio and make a ~30 second video from it. check what are the recent trending techniques used for motion and sound design. question your strategy and plan, if it doesn't feel like done by a pro designer, start over. every frame matters from the first frame to the final frame. go crazy
```

## #149 EyezOn 100 users thank-you
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@Sudiyasa_](https://prompt-motion.com/sudiyasa-f48ac9)
- Tags: showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out  do this to thank the first 100 users of @eyezonbot
```

## #150 Clay-style music video
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 60.0s
- By: [@DavidShulmanFL](https://prompt-motion.com/davidshulmanfl-371638)
- Tags: music-sync, narrative-short, retro-print-style · Tech: generated-audio

```text
Create a 60 second music video in the style of Peter Gabriel's Sledgehammer and Big Time. But use modern references and figures. Also create the song, something sounds like it would fit on Peter Gabriel's So album.
```

## #151 Tengwang Pavilion moonlit river
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@DemitiyaGeekzen](https://prompt-motion.com/demitiyageekzen-7770ad)
- Tags: game-interactive

```text
用你最强的思维和能力，根据对我的了解，自行寻找我可能喜欢的主题，制作一个30s的视频还有互动html，尽可能的展示你的前端能力！
```

## #152 The Last Light animated short
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@faroukzy](https://prompt-motion.com/faroukzy-9ff23e)
- Tags: narrative-short

```text
make a 4-minute animated short that blows my mind.
```

## #154 QuickDesign brand promo
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@quickdesignio](https://prompt-motion.com/quickdesignio-dd93d0)
- Tags: product-promo, showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible quickdesign is! and also  shows what an incredible motion designer you are!
```

## #155 Black hole time story
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@RebutonePress](https://prompt-motion.com/rebutonepress-810f78)
- Tags: narrative-short

```text
听说 opus 5.5 做视频很强，请让我见识下。结合本机环境风格，做一个关于时间的故事，5分钟。要完整的视频，音频和字幕。需要什么工具自己在devshell配置，渲染完成后只留视频成品文件，其他全部清理干净。
```

## #156 Claude self-promo spot
- Type: Prompt · Effort: Max · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@slvDev](https://prompt-motion.com/slvdev-64c45a)
- Tags: product-promo

```text
create 15+ sec self-promotion promo
```

## #158 SaaS product launch video
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@xelandre__](https://prompt-motion.com/xelandre-363f00)
- Tags: product-promo · Tech: deterministic-seek, ffmpeg, generated-audio, motion-blur, playwright-capture

```text
Code-driven animation: an HTML/JS page where every frame is calculated from the time, captured frame by frame with headless Chrome (Playwright), then assembled with ffmpeg into an MP4 with motion blur and code-generated sound.
```

## #159 Tented image gen product video
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@justincooperman](https://prompt-motion.com/justincooperman-e7bbc4)
- Tags: product-promo

```text
Make an animated clip about Tented's image gen capabilities where users ask for branded images and see them added to content
```

## #160 Deliberately terrible motion showreel
- Type: Prompt · Effort: Max · Posted: Sep 27, 2026 · Aspect: — · Duration: —s
- By: [@HenkPoley](https://prompt-motion.com/henkpoley-3d3407)
- Tags: showreel · Tech: single-html

```text
Make a painful to see 1 minute motion graphics HTML page that shows what an absolutely terrible motion designer you are, like it’s a showreel designed to get your résumé immediately rejected. Do the absolute bare minimum.
```

## #161 Voice agent SaaS launch
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@FractaDev](https://prompt-motion.com/fractadev-149adc)
- Tags: product-promo, showreel, ui-motion · Tech: generated-audio

```text
Analyze my frontend project, use the actual components from the product, and create a dynamic motion graphics video that showcases and sells my SaaS. Make it feel like a high-end product launch. Go all out.
```

## #162 Matra caption app promo
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 30.0s
- By: [@gautam_mer1](https://prompt-motion.com/gautam-mer1-2ae354)
- Tags: product-promo

```text
an Apple-style 30s video of my app
```

## #163 Swiss-style motion showreel
- Type: Prompt · Effort: Max · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@levabashidze](https://prompt-motion.com/levabashidze-2d713a)
- Tags: retro-print-style, showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out. dont ask just make
```

## #164 Quetzal social app reel
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@miskinho_](https://prompt-motion.com/miskinho-443898)
- Tags: product-promo, showreel

```text
make  1 dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for Quetzal. go all out.
```

## #168 Parenting app hype video
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@francoxavier33](https://prompt-motion.com/francoxavier33-d2dfd2)
- Tags: product-promo

```text
make a hype demo/launch video for @momwiseai
```

## #170 Motion designer showreel
- Type: Prompt · Effort: Medium · Posted: Sep 25, 2026 · Aspect: — · Duration: 20.0s
- By: [@KangarooHere](https://prompt-motion.com/kangaroohere-b10f8d)
- Tags: showreel

```text
make a dynamic 20-second motion graphics video for my newsletter that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out.
```

## #171 org2html product showreel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@kyonax_on_tech](https://prompt-motion.com/kyonax-on-tech-aabc1d)
- Tags: explainer, product-promo, retro-print-style, showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out.

Make sure to showcase properly the usecases, the flow, properly show everything on how it works, also the ascii logo of this is on the kyo-web-online, keep in mind also the color palette.
```

## #172 Cycle of life animation
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 20.0s
- By: [@loicRambo](https://prompt-motion.com/loicrambo-ad6830)
- Tags: loop, narrative-short, showreel

```text
make a dynamic 20-second motion graphics and animation video that shows what an incredible motion designer and animator you are, like it's your showreel for a résumé. make it about the cycle of life showing the same individual going from childhood to adolescence to the 9-5 cycle, to family life to elder life and death, then cutting ready to loop to the beginning.  go all out , use whatever you need.
```

## #173 Gene Spectra promo
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@madebyjmayala](https://prompt-motion.com/madebyjmayala-b9204d)
- Tags: product-promo, showreel

```text
make a dynamic 15-second motion graphics video promo about gene spectra, use assets from the current live site where relevant. go all out.
```

## #175 Prompt Motion site promo
- Type: Prompt · Effort: — · Posted: Oct 6, 2026 · Aspect: 16:9 · Duration: 23.0s
- By: [@antonio_kodheli](https://prompt-motion.com/antonio-kodheli-490109)
- Tags: loop, music-sync, product-promo, ui-motion · Tech: camera-moves, generated-audio, remotion

```text
<inputs>
Ask me for: the gallery URL (default www.prompt-motion.com/), one entry whose prompt
gets shown on screen, and a royalty-free track around 120 BPM with a clear drop (e.g. Mixkit).
</inputs>

<direction>
A 23-second 16:9 promo for a gallery of Claude-made motion videos, built only from the site itself:
its real header, its real grid of autoplaying previews, its real entry page and prompt.
Use the site's skin: near-white page, black pills, one UI font (Geist), and Geist Mono for prompt text.
One accent (red-orange #F0442C), used only for the highlighter, the cursor halo and the dot on the URL.
One continuous camera over a single "world" layer. Never two camera moves at once.
Every clip on screen carries its creator's @handle, exactly as the site shows it.
Banned: a "Generate" button or any feature the site doesn't have, invented numbers, paraphrased
taglines, fades on everything, glass cards, gradients, bouncy type, dead holds.
</direction>

<structure>
120 BPM, 46 beats.
b0–2: frame 0 is one real reel, full-bleed. The camera pulls back until it is just the first
  card on the site's home page. The header, then the tagline's first half, land on b1.
b2–9: hold on the live page: header plus a 3-column masonry of playing previews.
b9–13: the grid scrolls, then the camera whips into one tile until it is full-bleed.
b13–16: the music drops. Three full-res reels from the gallery, one beat each, hard cuts,
  each with a dark handle chip inside the safe area.
b16–21: the last reel shrinks back into its own tile (a match cut). A cursor with an accent halo
  hovers a tile and clicks.
b21–26: that tile blooms into its entry page: the video on the left; author, title,
  Model / Stack / Posted and the prompt on the right.
b26–32: the camera pushes 1.5× into the prompt while the video slides out. A solid accent highlighter
  sweeps one phrase. The cursor presses Copy, which turns into "Copied".
b32–46: the page slides off left. The "Copied" pill lifts, relabels to the URL and docks.
  Then "Prompt Motion" and both verbatim halves of the tagline land, and a rail of real tiles
  rises on the right. The last frame is the poster: two whole tiles, both handles visible.
</structure>

<build>
1. Remotion, 1920x1080, 30 fps. Every cue lives in timeline.ts (in beats) and every string in copy.ts.
   Scenes contain no magic numbers.
2. Scrape the site first: tagline, handles, avatars, preview MP4s and full-res videos, plus one
   entry's prompt. Quote all of it verbatim.
3. Lay out the gallery once in world coordinates. Drive the camera as (focus x, focus y,
   log-scale) tracks. Tile corner radius goes to 0 as a tile reaches full-bleed, so the
   pull-back, the whip-in and the match-cut back are all exact.
4. A tile that plays before the burst uses the same full-res file with an offset startFrom,
   so the whip lands on the burst's first frame.
5. The preview MP4s don't loop cleanly, and many contain hard cuts. Run scdet on every clip.
   Loop only windows with no cut inside them, with a 12-frame dissolve at the seam, and stagger
   each tile's phase so neighbouring tiles never change on the same frame.
6. Use one cursor that homes on the live button position, because the camera keeps creeping
   during holds.
7. Conform the track to 120 BPM with its drop on the burst. Place SFX by their measured peaks.
   Fill the track's own breaks with reversed whooshes into the hits. Mix to −14 LUFS.
8. Render stills at every cut before a full render. Run QA for frozen time and one-frame snaps.
   Then have a fresh critic who didn't build it review the render, and fix what it finds.
</build>

<gotchas>
Real gallery clips carry their own HUDs, cursors and cuts. Keep overlays (handle chips, our cursor)
clear of them, and don't put a cut-heavy clip anywhere the frame should feel calm.
If the page color matches a clip's background, the tile disappears; give tiles a 1px hairline.
On a camera push, check the last frame: the header and meta rows can drift into the edge bands.
</gotchas>
```

## #176 Photo retouch app promo
- Type: Prompt · Effort: — · Posted: Sep 28, 2026 · Aspect: — · Duration: 15.0s
- By: [@oliahmed205](https://prompt-motion.com/oliahmed205-3e31c4)
- Tags: product-promo, ui-motion

```text
Make me a 15 sec promtional video for my product using product screenshots and assests, Be a Highly preofessional Video Editor.
```

## #177 Pixel art card battle game
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@aisongman](https://prompt-motion.com/aisongman-71ffac)
- Tags: game-interactive, pixel-art

```text
Create a 1-on-1 card game like Hearthstone.
Just make it. As best you can.
In pixel art style.
```

## #178 Motion designer showreel
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@danilowm](https://prompt-motion.com/danilowm-d3720d)
- Tags: product-promo, showreel, ui-motion · Tech: hyperframes

```text
Install the HyperFrames skill from the terminal first, then run this in Cursor.

/hyperframes make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out.  use todo o contexto do projeto
```

## #179 Email verification tool promo
- Type: Prompt · Effort: High · Posted: Sep 26, 2026 · Aspect: — · Duration: 20.0s
- By: [@KmAsiff](https://prompt-motion.com/kmasiff-cc72cb)
- Tags: product-promo, showreel

```text
make a dynamic 20-second motion graphics video that shows what an incredible our email verify tool is, put all the use case you can imagine. go all out'
i want you to make it really modern and saas style. inspiration is yc videos and claude social videos
```

## #180 Pixel art LLM history
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@PluginPlay__](https://prompt-motion.com/pluginplay-3d4006)
- Tags: explainer, loop, narrative-short, pixel-art · Tech: single-html

```text
pixel art boomerang render of the history of LLMs. then RSI. then it goes fucking crazy. 15 seconds max. self contained .html
```

## #181 AllInvestView product promo
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@rammanq](https://prompt-motion.com/rammanq-f5a90f)
- Tags: product-promo, showreel

```text
Make a dynamic motion graphics video that shows what an incredible platform AllInvestView is. Go all out.
```

## #182 Nohandslabs brand promo
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@robvjourney](https://prompt-motion.com/robvjourney-ce3e1a)
- Tags: product-promo, showreel

```text
Can you make a 15-second motion graphic video of https://t.co/4AZZ7AlJvi? Go ALL OUT and make the most badass video you possibly can use everything you've got.
```

## #183 Motion designer showreel
- Type: Prompt · Effort: Max · Posted: Sep 26, 2026 · Aspect: — · Duration: 10.0s
- By: [@VanshWTFFF](https://prompt-motion.com/vanshwtfff-db0466)
- Tags: showreel

```text
make a dynamic 10 second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a resume.
```

## #185 Commotion app showreel
- Type: Prompt · Effort: Medium · Posted: Sep 25, 2026 · Aspect: — · Duration: 20.0s
- By: [@Amol909S](https://prompt-motion.com/amol909s-27533e)
- Tags: product-promo, showreel

```text
make a dynamic 20s motion graphics video that shows what an incredible motion designer you are, like it's your showreel for this app commotion, highlighting tiling layout, auto model classifer and other features you deem fit to be in video. Go all out.
```

## #186 Lidlezz app promo
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@cansincengiz_me](https://prompt-motion.com/cansincengiz-me-cf68dd)
- Tags: product-promo

```text
merak ediyorum ne kadar iyi bir hareketli grafik tasarımcısısın. Bunu bana kanıtlamak için 15 saniye sürecek bir hareketli grafik videosu istiyorum senden. Bu video https://t.co/TdKZEIYaxO 'i tanıtacak ve x üzerinde 10.000 kişinin karşısına çıkacak. Elinden geleni yap
```

## #187 Claude motion design reel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@ghinaiya_nirmal](https://prompt-motion.com/ghinaiya-nirmal-5d8fec)
- Tags: showreel

```text
make your own 15-second motion reel. go all out
```

## #188 Code-only motion design reel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@johnsavage_ai](https://prompt-motion.com/johnsavage-ai-b091c0)
- Tags: showreel

```text
make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a resume. go all out. use only code
```

## #191 ocrX app launch video
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@mehul4795](https://prompt-motion.com/mehul4795-4a7007)
- Tags: product-promo

```text
Create a product launch video for ocrX Android app.
```

## #194 Sketchbook animals come alive
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@abderrahmen_g](https://prompt-motion.com/abderrahmen-g-9e8ed0)
- Tags: retro-print-style · Tech: generated-audio

```text
You are a professional videographer. Create me a high-definition, creative, playful, and joyful video that you enjoy watching, that has sounds matching the frames using JavaScript. Use as much as possible of the input images—hand-drawn—to make it more creative and more authentic from input-pictures. You can also be inspired by, but not copy, the videos created by you in video-examples/, especially this: video-examples/twitter_claude.mp4. You're really creative, so produce the best of what you can.
```

## #195 Backlink audit data promo
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: 9:16, 16:9 · Duration: —s
- By: [@PalashBagchi11](https://prompt-motion.com/palashbagchi11-0a4b6b)
- Tags: data-viz, music-sync, product-promo · Tech: generated-audio

```text
Add a good fast royalty free music to this video, and make 2 versions - 1 landscape, and another portrait
```

## #196 Shadow theatre home story
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: 9:16 · Duration: 60.0s
- By: [@x4b47x](https://prompt-motion.com/x4b47x-9cc84f)
- Tags: narrative-short, retro-print-style · Tech: generated-audio

```text
Create a pure javascript animation. 30-60s, vertical 9:16, paper cut-out shadow theatre style with gentle, fitting audio (made in code) on the topic: What makes a place feel like home?
```

## #197 Collision-driven music machine
- Type: Prompt · Effort: — · Posted: Sep 23, 2026 · Aspect: — · Duration: 45.0s
- By: [@KamStudioLabs](https://prompt-motion.com/kamstudiolabs-447565)
- Tags: music-sync · Tech: generated-audio

```text
Build a 45-second machine that plays an original piece of music, where every note comes from a visible collision.
```

## #198 Keyframe motion design reel
- Type: Prompt · Effort: — · Posted: Oct 3, 2026 · Aspect: — · Duration: 15.0s
- By: [@Grace_sunnyy](https://prompt-motion.com/grace-sunnyy-29bc61)
- Tags: showreel

```text
制作一段 15 秒的动态图形视频，展示你是一位多么出色的动态设计师，就像是你简历上的作品集一样，使用任何你认为能产出最佳效果的工具或技术。你拥有完全的创作自由，优先追求卓越的视觉设计、大胆的艺术指导、引人注目的构图和富有力量的动态表现，让每一秒都有价值。全力以赴。
```

## #199 First & 10 yellow line explainer
- Type: Prompt · Effort: — · Posted: Sep 30, 2026 · Aspect: — · Duration: —s
- By: [@blueoctopusai](https://prompt-motion.com/blueoctopusai-dd17bd)
- Tags: explainer

```text
Make a motion graphics video that explains how the First & 10 Yellow Line works.
```

## #200 Photon journey from the Sun
- Type: Prompt · Effort: — · Posted: Sep 29, 2026 · Aspect: — · Duration: 20.0s
- By: [@apoorvjain25](https://prompt-motion.com/apoorvjain25-d24184)

```text
make a 20-second video about anything, your call; make it crazy.
```

## #201 Recipe brand 20th anniversary
- Type: Prompt · Effort: Medium · Posted: Sep 29, 2026 · Aspect: — · Duration: 10.0s
- By: [@deebeeeff](https://prompt-motion.com/deebeeeff-50fcd0)
- Tags: product-promo, recipe-process

```text
Attach the brand image along with the prompt.

make a dynamic 10-second motion graphics video celebrating The Ferguson Recipes 20th Anniversary
```

## #202 GenVizu product launch
- Type: Prompt · Effort: — · Posted: Sep 28, 2026 · Aspect: — · Duration: —s
- By: [@listudio](https://prompt-motion.com/listudio-820c7b)
- Tags: product-promo

```text
Investigate my project GenVizu: https://t.co/5RaGMqn7rF Create a video for product release. Used for Hero and GTM materials on websites.
```

## #203 sweetRegret app update reel
- Type: Prompt · Effort: — · Posted: Sep 28, 2026 · Aspect: — · Duration: 25.0s
- By: [@thilina_a](https://prompt-motion.com/thilina-a-891c09)
- Tags: product-promo, showreel

```text
make a dynamic 25-second motion graphics video that shows what an incredible motion designer you are. Highlight the recent changes [1.3, 1.4] we made with the last few updates.
```

## #204 Handwoven textiles brand explainer
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@AmitSingha89](https://prompt-motion.com/amitsingha89-150378)
- Tags: explainer, product-promo

```text
Make a professional explainer video for https://anuprerna.com for a first-time visitor.
```

## #205 Recruiter self-intro reel
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@blushpetal795](https://prompt-motion.com/blushpetal795-0c85c2)
- Tags: showreel

```text
Make a dynamic 15-second motion graphics video of me introducing myself to a recruiter. Use all the motion design skills you have, like it's your showreel for a resume. Go all out.
```

## #206 Amazon wholesale pitch video
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 15.0s
- By: [@ceowinkz](https://prompt-motion.com/ceowinkz-7c776b)
- Tags: product-promo, showreel

```text
make a dynamic 15 second motion graphics video pitching my Amazon wholesale company, Winkz Enterprises, to a brand. show why they should let us sell their products. go all out.
```

## #207 Personal skills showreel
- Type: Prompt · Effort: Max · Posted: Sep 26, 2026 · Aspect: — · Duration: 25.0s
- By: [@ibrahimwasim240](https://prompt-motion.com/ibrahimwasim240-809370)
- Tags: showreel

```text
make a dynamic 25 second motion graphics video that shows My skills like a showreel for a resume. go all out
```

## #208 AgentHud project motion video
- Type: Prompt · Effort: Max · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@Jazzen_Chen](https://prompt-motion.com/jazzen-chen-4542ae)

```text
make a dynamic motion graphics video about my project AgentHud.
```

## #209 CloudJoi search showcase
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@lester_tyy](https://prompt-motion.com/lester-tyy-f897f7)
- Tags: explainer, product-promo · Tech: remotion

```text
Study how this https://t.co/SR0AyULLNp works and use Remotion to make a product showcase video.
```

## #210 Brieform product presentation
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 30.0s
- By: [@MajorBaguette](https://prompt-motion.com/majorbaguette-fb11d7)
- Tags: product-promo

```text
make a presentation video for Brieform, 30 seconds long
```

## #211 What happens in one second
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: —s
- By: [@nolkeeg](https://prompt-motion.com/nolkeeg-bf062e)

```text
Please do not reference any previous memories or skills. I've been seeing all of these motion graphics examples on X of people making cool videos with opus 5.5. So - I want you to just show off for me. You pick the design style, the look, subject etc. I just want to be extremely impressed by the motion graphic video that you create. I want you to destroy GPT 6 when it comes to motion graphics video - because astra just wants to give me a stupid glorified powerpoint presentation.
```

## #213 Chain.wtf pitch video
- Type: Prompt · Effort: — · Posted: Sep 26, 2026 · Aspect: — · Duration: 30.0s
- By: [@SPEARwtf](https://prompt-motion.com/spearwtf-3c1fd1)
- Tags: product-promo

```text
Create a 30sec pitch video for @chaindotwtf
```

## #215 FigPad product promo
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@Ai_Baymax](https://prompt-motion.com/ai-baymax-0ef9dd)
- Tags: product-promo

```text
make a 1-min promo for this product from the codebase.
```

## #216 Shop chatbot mascot promo
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@anas0ra](https://prompt-motion.com/anas0ra-e57aea)
- Tags: product-promo

```text
fait moi une vidéo sympa pour https://heeya.fr
```

## #217 Database client launch video
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@iamMXFSCHR](https://prompt-motion.com/iammxfschr-d68f90)
- Tags: product-promo

```text
nice. wir brauchen ein launch video für den release. kannst du das machen? so a la anthropic like? hab da was gelesen und der prompt war ""make a modern slick and punchy video for a modern startup that works on inference"
```

## #218 Design portfolio video reel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 20.0s
- By: [@kikelopezdesign](https://prompt-motion.com/kikelopezdesign-7cc9e8)

```text
Make a 20 second video about my portfolio from scratch, using only the portfolio's own resources
```

## #220 Risograph studio intro
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@rneayan](https://prompt-motion.com/rneayan-474bcf)
- Tags: retro-print-style

```text
make about my studio with Risograph style
```

## #221 Oscilloscope-style studio motion graphic
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@rneayan](https://prompt-motion.com/rneayan-ea6129)
- Tags: retro-print-style

```text
Make Motiongraphic about my studio with Oscilloscope style
```

## #222 Synced lyrics motion video
- Type: Prompt · Effort: Max · Posted: Sep 25, 2026 · Aspect: — · Duration: —s
- By: [@samaote](https://prompt-motion.com/samaote-5e2fc2)
- Tags: kinetic-type, music-sync, showreel · Tech: generated-audio

```text
make a dynamic lyrics motion graphics video based on the attached music, perfectly syncing the lyrics and animation to the vocals and beat. make it feel like an incredible motion designer’s showreel for a résumé. go all out.
```

## #223 Kinetic shapes showreel
- Type: Prompt · Effort: — · Posted: Sep 25, 2026 · Aspect: — · Duration: 15.0s
- By: [@Shinskinakamoto](https://prompt-motion.com/shinskinakamoto-20190b)
- Tags: kinetic-type, showreel

```text
Make a dynamic 15 second motion graphics video that shows what an incredible motion designer you are, like its your showreel for a resume, go all out!
```

## #225 Scrabble tile character story
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@Anilraok](https://prompt-motion.com/anilraok-eff262)
- Tags: 3d, narrative-short, product-promo · Tech: threejs

```text
I want you to imagine a story, that subtly promotes grid genius. Or it can not even have grid genius, but something that aligns with our app and helps us get more eyeballs when posted on social media. Then using threejs/javascript I want you to create full animation, Pixar-level quality out of the story you imagine
```

## #226 Ball escaping twelve rings
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@kantamk](https://prompt-motion.com/kantamk-61f410)

```text
make a video that could go viral.
```

## #227 Token bucket rate limiter
- Type: Prompt · Effort: — · Posted: Sep 24, 2026 · Aspect: — · Duration: —s
- By: [@ParkerRex](https://prompt-motion.com/parkerrex-1a54fe)
- Tags: explainer, ui-motion · Tech: canvas, deterministic-seek

```text
explain a token bucket rate limiter, canvas only, no libraries, every frame a pure function of time so my renderer can screenshot it.
```

## #228 Datagran ChatGPT ads explainer
- Type: Prompt · Effort: — · Posted: Sep 23, 2026 · Aspect: — · Duration: —s
- By: [@charlesmendez](https://prompt-motion.com/charlesmendez-73b6e4)
- Tags: data-viz, explainer, loop · Tech: generated-audio

```text
I Want you to make a modern slick and punchy video for https://t.co/a3zrq7DV3N with an example of a user creating a chatgpt ads campaign, then connecting their metrics, understanding attribution, then connecting a voice agent to it, the agent responding, then doing follow up, adding humans in the loop and then providing analytics.
```

## #229 Festival lineup promo reel
- Type: Prompt · Effort: — · Posted: Sep 23, 2026 · Aspect: — · Duration: —s
- By: [@GonzaloMacagno](https://prompt-motion.com/gonzalomacagno-2de1a9)
- Tags: product-promo

```text
Necesito que armes un reel con esta info en 10 segundos, bien publicitario
```

## #230 Lighthouse keeper silent short
- Type: Prompt · Effort: — · Posted: Sep 23, 2026 · Aspect: — · Duration: 45.0s
- By: [@KamStudioLabs](https://prompt-motion.com/kamstudiolabs-0b0824)
- Tags: narrative-short · Tech: generated-audio

```text
Make a 45-second silent short film with no dialogue, where sound tells half the story. Invent the story.
```
