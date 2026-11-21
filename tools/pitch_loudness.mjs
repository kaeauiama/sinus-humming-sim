// Pitch x sound pressure: how much of each sinus is exchanged in 10 s of humming, with the page defaults
// (two compartments, weak harmonics n^-2, per-ostium pressure ratios, diffusion included). Dimensions are the
// fictional head of dist/hum-3d.html (literature means). Run: node tools/pitch_loudness.mjs
import { lumped } from './model.mjs';
import { ostG } from './no_model.mjs';

const DIM = { max: [12.75, 2.8, 2.1, null], sph: [4.0, 2.2, 1.5, 'sph'], fro: [2.9, 7.5, 4.0, 'fro'], eth: [0.4, 1.5, 1.5, 'eth'] };
const NAME = { max: 'maxillary', sph: 'sphenoid', fro: 'frontal', eth: 'ethmoid cell' };
const FN = 0.5, TAU = 40, T = 10;
function rates(k, f, P0) {
  const [V, d, L, g] = DIM[k], G = fr => (g ? ostG(g, fr) : 1);
  const r = lumped(V, d, L, f, P0 * G(f)); let kH = r.kH;
  for (let h = 2; h <= 6; h++) kH += lumped(V, d, L, f * h, P0 * h ** -2 * G(f * h)).kH;
  return { kH, kD: r.kD, x: r.x, f0: r.f0 };
}
function exch(k, t = T) {   // two compartments, as stepTwo() in the pages
  const a = 1 / TAU / (1 - FN), b = 1 / TAU / FN; let n = 1, fa = 1;
  for (let s = 0; s < t / 0.01; s++) { const dn = -(k / FN) * n + b * (fa - n), df = a * (n - fa); n += 0.01 * dn; fa += 0.01 * df; }
  return 1 - (FN * n + (1 - FN) * fa);
}
const pct = v => `${(v * 100).toFixed(0)}%`;
const FS = [100, 150, 200, 300], PS = [65, 130, 260, 520];
console.log(`exchanged in ${T} s of humming (two compartments, diffusion included); ceiling for infinitely fast exchange at the ostium: ${pct(1 - (1 - FN) * Math.exp(-T / TAU / (1 - FN)))} (near half at once, far half on ${TAU} s)`);
for (const k of Object.keys(DIM)) {
  const r0 = rates(k, 150, 130);
  console.log(`\n${NAME[k]} (resonance ${r0.f0.toFixed(0)} Hz, diffusion alone ${pct(exch(r0.kD))})`);
  console.log('  P0 (Pa) \\ f (Hz) ' + FS.map(f => String(f).padStart(14)).join(''));
  for (const P of PS) {
    const cells = FS.map(f => { const r = rates(k, f, P); return `${pct(exch(r.kH + r.kD)).padStart(5)} (x ${r.x.toFixed(2).padStart(4)})`; });
    console.log(`  ${String(P).padStart(7)}          ` + cells.map(c => c.padStart(14)).join(''));
  }
}
// time to reach half of the sinus at the defaults vs louder/higher
console.log('\nseconds of humming to exchange half of the maxillary sinus:');
for (const [f, P] of [[150, 130], [300, 130], [150, 260], [300, 260], [150, 520]]) {
  const r = rates('max', f, P); let t = 0; while (exch(r.kH + r.kD, t) < 0.5 && t < 600) t += 0.25;
  console.log(`  ${f} Hz, ${P} Pa: ${t >= 600 ? '> 600' : t.toFixed(1)} s`);
}
