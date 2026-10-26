---
name: html-motion-build
description: >-
  Use this to build seekable HTML from a director brief — follow the one-shot
  for craft; only enforce pure-time seek and verify so it can become MP4.
---
# HTML motion build

**One job:** build `<name>.html` that **achieves** the brief's one-shot look — showreel craft, not title cards.
**Director rule:** obey ONE-SHOT + **CANVAS** in the brief. Override starter chrome. Starter ships a placeholder — **replace** `--bg` with brief CANVAS; shipping house-black when the case was paper/cream/colour is a fail.

## Hard cage only (recording)
```js
window.STAGE; window.DURATION; window.FPS=60;
window.seek = t => { render(t); }; // never return a GSAP timeline
window.__ready = Promise; window.BEATS; // cover 0→DURATION
```
Motion only from `render(t)` / paused GSAP seek — no CSS animations, no unseeded random, no timers. Fonts preloaded.

## Steps
1. `cp …/html-motion-build/assets/starter.html` then replace look + CANVAS.
2. Implement the one-shot. Prefer storytelling over packing every number.
3. **Beat hygiene (Justin fail to avoid):** adjacent beats must not overlap on screen. Finish exit of beat N before beat N+1 copy is readable; designed hold after resolve; no stacked titles from two slides at once.
4. verify.mjs until PASS; Read contact + ≥3 shots + **transition frames** between beats. If KPI deck, accidental black terminal, or **overlapping slides**, redesign — don't ship.

```bash
node /home/box/agent-data/workflows/html-motion-build/scripts/verify.mjs <html> <dir>/verify --duration <D> --aspect <W:H>
```

## VERIFY
- [ ] PASS + matches one-shot energy and brief CANVAS
- [ ] Hook + final designed; no invented facts
- [ ] No mid-transition double-text / overlapping slides

→ html-motion-render
