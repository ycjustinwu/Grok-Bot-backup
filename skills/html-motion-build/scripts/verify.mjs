#!/usr/bin/env node
// VERIFY an HTML motion file in headless Chromium.
// Usage: node verify.mjs <file.html> <outdir> [--duration 10] [--aspect 16:9] [--times 0,2.5,5,9.9]
// Checks: render contract, console/page errors, spec duration + aspect, BEATS cover the duration,
// determinism (same t -> same pixels after visiting other times), non-blank frames.
// Writes shot_<t>.png per timestamp, contact.png, verify.json. Exit 1 on any FAIL.
import fs from 'fs'; import path from 'path'; import crypto from 'crypto'; import { execFileSync } from 'child_process';
import { launch, openMotion } from '../../html-motion-render/scripts/_browser.mjs';
const a = process.argv.slice(2); const [file, od] = a;
if (!file || !od) { console.log('usage: verify.mjs <file.html> <outdir> [--duration s] [--aspect W:H] [--times a,b,c]'); process.exit(1); }
const opt = (k, d) => { const i = a.indexOf('--' + k); return i > -1 ? a[i + 1] : d; };
fs.mkdirSync(od, { recursive: true });
const browser = await launch();
const { page, contract: c, errors } = await openMotion(browser, file);
const checks = []; const ck = (name, ok, info = '') => checks.push({ name, ok, info });
const D = c.D;
let times = opt('times', null)?.split(',').map(Number);
if (!times) { // every beat midpoint + start + near end, min 3
  times = [0.05, ...(c.BEATS || []).map(b => (b[0] + b[1]) / 2), D - 0.05];
  if (times.length < 4) times = [0.05, D * 0.33, D * 0.66, D - 0.05];
}
times = [...new Set(times.map(t => +Math.min(Math.max(t, 0), D).toFixed(2)))];
const shot = async t => { await page.evaluate(async tt => { const r = window.seek(tt); if (r instanceof Promise) await r; }, t); return page.screenshot({ type: 'png' }); };
const hash = b => crypto.createHash('md5').update(b).digest('hex');
const shots = [];
for (const t of times) { const b = await shot(t); const p = path.join(od, `shot_${t.toFixed(2)}.png`); fs.writeFileSync(p, b); shots.push({ t, p, h: hash(b), size: b.length }); }
// determinism: revisit the first mid shot after jumping elsewhere
const mid = shots[Math.floor(shots.length / 2)];
await shot(D - 0.01); await shot(0); const again = hash(await shot(mid.t));
ck('deterministic seek', again === mid.h, `t=${mid.t}`);
ck('frames differ over time', new Set(shots.map(s => s.h)).size >= Math.min(3, shots.length), `${new Set(shots.map(s => s.h)).size} unique of ${shots.length}`);
// blank-frame heuristic: tiny PNG = flat colour
const blank = shots.filter(s => s.size < 6000).map(s => s.t);
ck('no blank frames', blank.length === 0, blank.length ? 'suspect blank at ' + blank.join(',') : '');
const wantD = opt('duration', null); if (wantD) ck('duration matches spec', Math.abs(D - +wantD) < 0.05, `DURATION=${D} spec=${wantD}`);
const asp = opt('aspect', null); if (asp) { const [x, y] = asp.split(':').map(Number); ck('aspect matches spec', Math.abs(c.STAGE.w / c.STAGE.h - x / y) < 0.01, `${c.STAGE.w}x${c.STAGE.h}`); }
if (c.BEATS) { const end = Math.max(...c.BEATS.map(b => b[1])); ck('BEATS cover DURATION', Math.abs(end - D) < 0.05, `last beat ends ${end}, D=${D}`); }
const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
ck('no horizontal overflow', !overflow);
ck('no console/page errors', errors.length === 0, errors.slice(0, 5).join(' | '));
await browser.close();
// contact sheet
try { const list = shots.map(s => s.p); const n = list.length; const cols = Math.min(4, n);
  execFileSync('ffmpeg', ['-v', 'error', '-y', ...list.flatMap(p => ['-i', p]), '-filter_complex',
    list.map((_, i) => `[${i}:v]scale=480:-1[s${i}]`).join(';') + ';' + list.map((_, i) => `[s${i}]`).join('') + `xstack=inputs=${n}:layout=` +
    list.map((_, i) => `${(i % cols) ? Array.from({ length: i % cols }, () => 'w0').join('+') : '0'}_${Math.floor(i / cols) ? Array.from({ length: Math.floor(i / cols) }, () => 'h0').join('+') : '0'}`).join('|') + ':fill=black',
    path.join(od, 'contact.png')]);
} catch (e) { /* single-shot or xstack issue: skip sheet */ }
const ok = checks.every(x => x.ok);
const rep = { file, verdict: ok ? 'PASS' : 'FAIL', stage: c.STAGE, duration: D, fps: c.FPS, beats: c.BEATS, shots: shots.map(s => s.p), checks };
fs.writeFileSync(path.join(od, 'verify.json'), JSON.stringify(rep, null, 1));
for (const x of checks) console.log(`${x.ok ? 'PASS' : 'FAIL'}  ${x.name}${x.info ? '  (' + x.info + ')' : ''}`);
console.log(`VERDICT ${rep.verdict}  shots: ${od}`); process.exit(ok ? 0 : 1);
