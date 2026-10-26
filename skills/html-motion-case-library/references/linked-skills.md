# Skills linked from prompt-motion.com (read 2026-10-08)

Summaries only; read the repos for the real text. Licences as stated in each repo.

| Case | Skill / repo | Licence | Engine | Use it for |
|---|---|---|---|---|
| [Cinetic skill launch film](https://prompt-motion.com/lexnlin-6161a6) @LexnLin | https://github.com/Leonxlnx/cinetic (`npx skills add Leonxlnx/cinetic`) | MIT | Remotion 4 / HyperFrames (HTML+GSAP) | Launch films, stings, UI walkthroughs with a measured review loop |
| [Reddit marketing tool launch video](https://prompt-motion.com/anthonyriera-9b1b2a) @anthonyriera | https://github.com/Rieranthony/product-film-skill | MIT | Remotion | Product films built from the product's real components |
| [Animated agent session story](https://prompt-motion.com/jake11moran-a269c4) @jake11moran | https://github.com/heygen-com/hyperframes-community-skills/tree/master/skills/session-story | Apache-2.0 | HyperFrames | A scored film of an agent's session history |
| [Indian civilisation history film](https://prompt-motion.com/buildfastwithai-53234e) @BuildFastWithAI | https://github.com/buildfastwithai/buildfast-skills (generative-film, html-animation-skill, motion-studio) | MIT | pycairo+numpy / Canvas HTML / own engine | Code-drawn films with synth score; canvas documentaries; 51-style motion studio |

## Craft worth reusing (paraphrased)
- **cinetic — formats:** launch 20–45 s, product/feature 8–30 s, loop 4–15 s in whole bars, logo sting 3–8 s, UI walkthrough 20–90 s; 60 fps whenever UI, text or camera moves; GIF at 25 fps.
- **cinetic — five laws:** one product-specific idea; one story device that never blinks out at a cut; one accent with one meaning (≈ ≤ 8 % of pixels); one house motion system (~3 easing characters); verify by measurement.
- **cinetic — easing tokens:** out `.16,1,.3,1` (arrivals), in `.7,0,.84,0` (snap out), inOut `.87,0,.13,1` (whips), smooth `.65,0,.35,1` (fades), cam `.48,.1,0,.9`. Entrances decay, exits accelerate; scale/zoom interpolated in log space; overshoot only on true landings (≤ 2 per film).
- **cinetic — engine rules:** everything a function of frame/time; no CSS transitions/keyframes; seeded random; transform-only placement; no `will-change` where blur animates; fonts loaded before measuring; GSAP `fromTo` not `from`, one paused timeline.
- **cinetic — timing:** text holds ≥ 36 f + 6 f/word at 60 fps; nothing static > 48 f except one designed hold; transitions: 6–8 types, ≤ 2 uses each, no crossfade by default.
- **html-animation-skill (canvas documentary):** classic `<script>` so `seek()` is on `window`; scene functions deterministic in local time; keyframes as spline data; verify every named beat by screenshot after computing absolute times; listen for pageerror.
- **motion-studio:** brief → concept → storyboard → visual system → build → preview → render → QC → fix; transition table by intent (match cut, push, mask wipe, iris, whip, zoom); vary transition types; save the biggest for the payoff.
- **generative-film:** beat grid first (e.g. 96 BPM), music before picture, test frames → contact sheet → fix before full render.
