// Drive a page in Chrome, wait until a condition holds, then print selected DOM texts and the per-cycle log as JSON.
//
//   node test/run.mjs dist/verify-rounding.html --query "?autoE1" --until "document.getElementById('status').textContent.includes('完了')" --dump v1,t1
//   node test/run.mjs dist/sinus3d-integrated.html --query "?autorun&f=200&P0=150" --until "document.getElementById('st3s').textContent==='完了'" --dump st2v,st3v,cmp
//
// Options
//   --query  URL query (page switches: autorun / autoE1 / autoE2 / dbg / warm / cycles / dc / xs / rfs / f / P0 / d / muc / mucus / harm)
//   --until  JS expression polled every 2 s (default: wait --timeout seconds)
//   --timeout seconds (default 900)
//   --dump   comma-separated element ids whose innerText is returned
//   --shot   save a full-page screenshot
//   --headful    show the browser window (real GPU, easiest to trust)
//   --swiftshader  software WebGPU (Linux CI); also turns on --fake-canvas
//   --fake-canvas  render into an offscreen texture instead of the canvas (headless canvases may lose the device)
// Chrome is taken from CHROME_PATH, else the usual Windows / Linux install paths.
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import puppeteer from 'puppeteer-core';

const argv = process.argv.slice(2);
const opt = { query: '', until: '', timeout: 900, dump: '', shot: '', headful: false, swiftshader: false, fakeCanvas: false };
const file = argv.shift();
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === '--headful') opt.headful = true;
  else if (a === '--swiftshader') { opt.swiftshader = true; opt.fakeCanvas = true; }
  else if (a === '--fake-canvas') opt.fakeCanvas = true;
  else opt[a.replace(/^--/, '').replace(/-(\w)/g, (_, c) => c.toUpperCase())] = argv[++i];
}
const candidates = [process.env.CHROME_PATH,
  'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  '/usr/bin/google-chrome', '/usr/bin/chromium'].filter(Boolean);
const executablePath = candidates.find(p => fs.existsSync(p));
if (!executablePath) throw new Error('Chrome not found; set CHROME_PATH');
const args = ['--enable-unsafe-webgpu'];
if (opt.swiftshader) args.push('--no-sandbox', '--use-webgpu-adapter=swiftshader', '--enable-unsafe-swiftshader');
const browser = await puppeteer.launch({ executablePath, headless: opt.headful ? false : 'new', args });
const page = await browser.newPage();
await page.setViewport({ width: 1100, height: 900 });
const log = [];
page.on('console', m => { const t = m.text(); if (t.startsWith('cyc')) log.push(t); else console.error('console:', m.type(), t); });
page.on('pageerror', e => console.error('pageerror:', e.message));
if (opt.fakeCanvas) await page.evaluateOnNewDocument(() => {
  const orig = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (type, ...rest) {
    if (type !== 'webgpu') return orig.call(this, type, ...rest);
    const cv = this;
    const fake = {
      configure(cfg) { this.dev = cfg.device; this.fmt = cfg.format; this.tex = null; },
      getCurrentTexture() {
        if (!this.tex || this.tex.width !== cv.width || this.tex.height !== cv.height)
          this.tex = this.dev.createTexture({ size: [cv.width, cv.height], format: this.fmt, usage: GPUTextureUsage.RENDER_ATTACHMENT | GPUTextureUsage.COPY_SRC });
        return this.tex;
      },
    };
    window.__fake = fake;
    return fake;
  };
  // keep rAF from racing ahead of a slow (software) GPU queue
  const origRAF = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = cb => { const f = window.__fake; if (f && f.dev) { f.dev.queue.onSubmittedWorkDone().then(() => origRAF(cb)); return 0; } return origRAF(cb); };
});
const url = pathToFileURL(path.resolve(file)).href + opt.query;
await page.goto(url);
const t0 = Date.now();
let done = false;
while ((Date.now() - t0) / 1000 < +opt.timeout) {
  await new Promise(r => setTimeout(r, 2000));
  if (opt.until && await page.evaluate(opt.until).catch(() => false)) { done = true; break; }
}
const ids = opt.dump ? opt.dump.split(',') : [];
const dump = await page.evaluate(ids => Object.fromEntries(ids.map(id => [id, document.getElementById(id)?.innerText ?? null])), ids);
dump.err = await page.evaluate(() => document.getElementById('err')?.textContent ?? '');
if (opt.shot) await page.screenshot({ path: opt.shot, fullPage: true });
console.log(JSON.stringify({ url, done, seconds: Math.round((Date.now() - t0) / 1000), dump, cycles: log }, null, 1));
await browser.close();
