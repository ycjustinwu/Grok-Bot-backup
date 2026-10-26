---
name: html-motion-render
description: >-
  Use this to record a seekable HTML motion piece to MP4 (and optional GIF) on
  the box — headless Chromium frame-step capture piped to ffmpeg, then probe the
  file and look at extracted frames before delivering.
---
# HTML motion render

**One job:** turn a verified `<name>.html` (render contract from [html-motion-build](sand-workflow:html-motion-build)) into `<name>.mp4` (+ optional `.gif`) and prove the file is right.
**Anti-jobs:** no design edits beyond fixing a render bug; no uploading, posting or sharing the file anywhere.
**IO:** in = `<project>/<name>.html`. Out = `<project>/<name>.mp4`, `<name>.render.json`, `<project>/probe/` (probe.json, frame PNGs, contact.png), optional `<name>.gif`.

Scripts live in `/home/box/agent-data/workflows/html-motion-render/scripts/` (call it `S`).

## Steps

1. **Tools.** `bash $S/ensure-tools.sh` → prints `CHROME=` and `TOOLS=`. It finds Chrome/Chromium, installs `playwright-core` into `~/.local/share/html-motion-tools` if missing, and needs `ffmpeg`/`ffprobe`. Done when both lines print.
2. **Render.**
   ```bash
   node $S/render.mjs <name>.html <name>.mp4 [--fps 60] [--subframes 1] [--start 0 --end D] [--crf 16] [--gif <name>.gif --gif-fps 25 --gif-width 960] [--audio track.wav]
   ```
   - For each frame i it calls `seek(i/fps)`, screenshots the stage at 1:1, pipes JPEGs to ffmpeg → H.264, yuv420p, TV range, BT.709, faststart.
   - fps: 60 for UI/text/camera moves; 30 only for slow pieces. GIF at 25 fps (GIF delays are whole hundredths).
   - Motion blur: `--subframes 6`–`8` for fast moves (3 shows stepped ghost copies). Costs N× capture time.
   - Speed reference: 10 s × 60 fps at 1920×1080 ≈ 35–45 s on the box.
   - Exit 3 = page errors during render (listed in `.render.json`); fix the HTML, re-render.
3. **Probe.** `bash $S/probe.sh <name>.mp4 <project>/probe <t1> <t2> <t3>` (pick beat mid-points; defaults 10/50/90 %). Prints duration, size, fps, frame count, codec, pix_fmt, range, audio; writes `frame_<t>.png` + `contact.png`.
4. **Deliver.** Attach the MP4 (and GIF if asked) plus the HTML; give the box paths.

## VERIFY (all must hold before delivery)
- [ ] `render.json` → `errors: []`
- [ ] duration = spec ± 1 frame; frames = duration × fps
- [ ] size = STAGE (even numbers), codec h264, pix yuv420p, range tv
- [ ] Read `contact.png` and ≥ 3 frame PNGs: each matches its beat, text sharp, colours not washed out (washed-out blacks = range bug), no white flash or blank frame at start/end
- [ ] loops: first and last frame match
- [ ] audio (if any): `audio=yes`, licence noted

## Handoff / escalate
Report paths + the probe line. If Chrome or ffmpeg cannot be installed, stop and report the exact error; deliver the HTML alone with that note. Publishing, uploading or posting the video needs the user's explicit go-ahead.
