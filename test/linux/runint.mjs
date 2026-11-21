import puppeteer from 'puppeteer-core';
const file = process.argv[2];
const out = process.argv[3] || 'shot.png';
const browser = await puppeteer.launch({
  executablePath: '/usr/bin/google-chrome', headless: 'new',
  args: ['--no-sandbox', '--enable-unsafe-webgpu', '--use-webgpu-adapter=swiftshader', '--enable-unsafe-swiftshader'],
});
const page = await browser.newPage();
await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 1 });
page.on('console', m => console.log('console:', m.type(), m.text()));
page.on('pageerror', e => console.log('pageerror:', e.message));
await page.evaluateOnNewDocument(() => {
  const orig = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (type, ...rest) {
    if (type !== 'webgpu') return orig.call(this, type, ...rest);
    const cv = this;
    const fake = {
      configure(cfg) { this.dev = cfg.device; this.fmt = cfg.format; this.tex = null; },
      getCurrentTexture() {
        if (!this.tex || this.tex.width !== cv.width || this.tex.height !== cv.height) {
          this.tex = this.dev.createTexture({ size: [cv.width, cv.height], format: this.fmt,
            usage: GPUTextureUsage.RENDER_ATTACHMENT | GPUTextureUsage.COPY_SRC });
        }
        return this.tex;
      },
    };
    window.__fake = fake;
    return fake;
  };
  const origRAF = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = cb => {
    const f = window.__fake;
    if (f && f.dev) { f.dev.queue.onSubmittedWorkDone().then(() => origRAF(cb)); return 0; }
    return origRAF(cb);
  };
  window.__snap = async () => {
    const f = window.__fake, d = f.dev, t = f.tex;
    const bpr = Math.ceil(t.width * 4 / 256) * 256;
    const buf = d.createBuffer({ size: bpr * t.height, usage: GPUBufferUsage.COPY_DST | GPUBufferUsage.MAP_READ });
    const e = d.createCommandEncoder();
    e.copyTextureToBuffer({ texture: t }, { buffer: buf, bytesPerRow: bpr }, [t.width, t.height]);
    d.queue.submit([e.finish()]);
    await buf.mapAsync(GPUMapMode.READ);
    const src = new Uint8Array(buf.getMappedRange());
    const c2 = document.createElement('canvas'); c2.width = t.width; c2.height = t.height;
    const g = c2.getContext('2d'); const img = g.createImageData(t.width, t.height);
    const bgra = f.fmt.startsWith('bgra');
    for (let y = 0; y < t.height; y++) for (let x = 0; x < t.width; x++) {
      const s = y * bpr + x * 4, o = (y * t.width + x) * 4;
      img.data[o] = src[s + (bgra ? 2 : 0)]; img.data[o + 1] = src[s + 1]; img.data[o + 2] = src[s + (bgra ? 0 : 2)]; img.data[o + 3] = 255;
    }
    g.putImageData(img, 0, 0);
    const main = document.getElementById('sim');
    c2.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;';
    main.parentElement.insertBefore(c2, main.nextSibling);
    return f.fmt;
  };
});
await page.goto('file://' + file + (process.env.Q || ''));
await new Promise(r => setTimeout(r, +(process.env.WAIT || 8000))); console.log('waited');
if (process.env.TILT) {
  await page.evaluate(k => dispatchEvent(new KeyboardEvent('keydown',{key:k})), process.env.KEY || 'ArrowRight'); console.log('key sent');
  await new Promise(r => setTimeout(r, +process.env.TILT));
}
const fmt = await page.evaluate(() => window.__snap());
const txt = await page.evaluate(() => ({ st1: st1v.innerText, st2: st2v.innerText, st3: st3v.innerText, verdict: verdict.innerText, cmp: cmp.innerText, hud: hud.innerText, err: err.textContent }));
txt.fmt = fmt;
console.log(JSON.stringify(txt));
await page.screenshot({ path: out, fullPage: !!process.env.FULL });
await browser.close();
