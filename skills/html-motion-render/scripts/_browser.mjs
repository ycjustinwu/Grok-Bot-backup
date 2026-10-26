// Shared: launch headless Chromium via playwright-core from the tools dir.
import { createRequire } from 'module';
import { execSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
const here = path.dirname(fileURLToPath(import.meta.url));
export function env() {
  const out = execSync(`bash "${here}/ensure-tools.sh"`, { encoding: 'utf8' });
  const kv = Object.fromEntries(out.trim().split('\n').map(l => l.split('=')));
  return kv;
}
export async function launch() {
  const { CHROME, TOOLS } = env();
  const require = createRequire(path.join(TOOLS, 'package.json'));
  const { chromium } = require('playwright-core');
  return chromium.launch({ executablePath: CHROME, headless: true,
    args: ['--no-sandbox', '--force-color-profile=srgb', '--hide-scrollbars', '--disable-gpu-vsync', '--font-render-hinting=none'] });
}
export function toUrl(p, q) {
  const u = p.startsWith('http') ? p : 'file://' + path.resolve(p);
  return u + (u.includes('?') ? '&' : '?') + q;
}
// Open page in render mode, wait for fonts + contract, collect errors.
export async function openMotion(browser, file, extraQuery = 'render=1') {
  const errors = [];
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  page.on('requestfailed', r => errors.push('requestfailed: ' + r.url()));
  await page.goto(toUrl(file, extraQuery), { waitUntil: 'load', timeout: 60000 });
  const c = await page.evaluate(async () => {
    if (window.__ready) await window.__ready;
    return { seek: typeof window.seek, D: window.DURATION, FPS: window.FPS, STAGE: window.STAGE, BEATS: window.BEATS || null };
  });
  if (c.seek !== 'function' || !(c.D > 0) || !c.STAGE) throw new Error('Render contract missing: need window.seek(t), window.DURATION, window.STAGE {w,h}. Got ' + JSON.stringify(c));
  await page.setViewportSize({ width: c.STAGE.w, height: c.STAGE.h });
  await page.evaluate(() => { window.seek(0); }); // never return seek()'s value: a GSAP timeline is a thenable and would hang evaluate
  return { page, contract: c, errors };
}
