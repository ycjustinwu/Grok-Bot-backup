#!/usr/bin/env node
// Frame-step recorder: seeks a deterministic HTML motion piece to t=i/fps, screenshots each frame,
// pipes to ffmpeg -> H.264 MP4 (yuv420p, faststart). Optional motion blur via sub-frames + tmix, optional GIF.
// Usage: node render.mjs <file.html> <out.mp4> [--fps 60] [--subframes 1] [--start 0] [--end D]
//        [--crf 16] [--gif out.gif --gif-fps 25 --gif-width 960] [--audio track.wav] [--quality 92]
import { spawn } from 'child_process';
import fs from 'fs';
import { launch, openMotion } from './_browser.mjs';
const a = process.argv.slice(2);
if (a.length < 2 || a.includes('--help')) { console.log(fs.readFileSync(new URL(import.meta.url)).toString().split('\n').slice(1,5).join('\n')); process.exit(a.length<2?1:0); }
const [file, out] = a;
const opt = (k, d) => { const i = a.indexOf('--' + k); return i > -1 ? a[i + 1] : d; };
const browser = await launch();
const { page, contract, errors } = await openMotion(browser, file);
const fps = +opt('fps', contract.FPS || 60), sub = Math.max(1, +opt('subframes', 1));
const t0 = +opt('start', 0), t1 = +opt('end', contract.D);
const n = Math.round((t1 - t0) * fps);
const { w, h } = contract.STAGE;
const q = +opt('quality', 92), crf = opt('crf', '16');
// JPEG frames are full-range; convert to TV range BT.709 yuv420p so players show correct blacks/colours.
const vf = [`scale=${w - (w % 2)}:${h - (h % 2)}:in_range=pc:out_range=tv:out_color_matrix=bt709`, 'format=yuv420p'];
if (sub > 1) vf.unshift(`tmix=frames=${sub}`, `select='not(mod(n\\,${sub}))'`, `setpts=N/(${fps}*TB)`);
const audio = opt('audio', null);
const args = ['-y', '-hide_banner', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps * sub), '-i', '-'];
if (audio) args.push('-i', audio);
args.push('-vf', vf.join(','), '-r', String(fps), '-c:v', 'libx264', '-preset', 'medium', '-crf', crf, '-pix_fmt', 'yuv420p',
  '-color_range', 'tv', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-movflags', '+faststart');
if (audio) args.push('-c:a', 'aac', '-b:a', '192k', '-shortest');
args.push(out);
const ff = spawn('ffmpeg', args, { stdio: ['pipe', 'inherit', 'inherit'] });
const started = Date.now();
for (let i = 0; i < n; i++) {
  for (let s = 0; s < sub; s++) {
    // sub-frames spread across the shutter interval centred on the frame time
    const t = t0 + (i + (sub > 1 ? (s - (sub - 1) / 2) / sub * 0.5 : 0)) / fps;
    // GSAP timelines are thenables that never resolve while paused: only await real Promises.
    await page.evaluate(async tt => { const r = window.seek(Math.max(0, tt)); if (r instanceof Promise) await r; }, t);
    const buf = await page.screenshot({ type: 'jpeg', quality: q });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  if (i % Math.max(1, Math.round(fps)) === 0) process.stderr.write(`\rframe ${i}/${n}`);
}
ff.stdin.end();
const code = await new Promise(r => ff.on('close', r));
await browser.close();
process.stderr.write(`\rframes ${n} in ${((Date.now() - started) / 1000).toFixed(1)}s\n`);
if (code !== 0) { console.error('ffmpeg failed'); process.exit(2); }
const gif = opt('gif', null);
if (gif) {
  const gf = opt('gif-fps', '25'), gw = opt('gif-width', String(Math.min(960, w)));
  await new Promise((res, rej) => spawn('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-i', out, '-vf',
    `fps=${gf},scale=${gw}:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=sierra2_4a`, gif],
    { stdio: 'inherit' }).on('close', c => c ? rej(new Error('gif failed')) : res()));
}
const report = { file, out, gif, fps, subframes: sub, frames: n, stage: contract.STAGE, duration: t1 - t0, errors };
fs.writeFileSync(out.replace(/\.mp4$/, '') + '.render.json', JSON.stringify(report, null, 1));
console.log(JSON.stringify(report));
if (errors.length) { console.error('PAGE ERRORS during render:', errors); process.exit(3); }
