// How robust are the frontal / ethmoid conclusions to their (assumed) drainage dimensions?
// Diffusion time tau_D = V L_e / (D A) and humming ventilation (two compartments, 130 Pa at the maxillary ostium times
// the ostium pressure ratio, weak harmonics, 150 Hz) over plausible ranges. Run: node tools/small_sinus_sensitivity.mjs
import { lumped, mix } from './model.mjs';
import { ostG } from './no_model.mjs';
const P0 = 130, f = 150, HARM = 2, fn = 0.5, tauInt = 40;
function exch2(k, T) {   // two-compartment washout, whole-sinus fraction exchanged in T s
  const b = 1 / tauInt / fn, a = 1 / tauInt / (1 - fn); let n = 1, fa = 1; const h = 0.01;
  for (let i = 0; i < T / h; i++) { const dn = -(k / fn) * n + b * (fa - n), df = a * (n - fa); n += h * dn; fa += h * df; }
  return 1 - (fn * n + (1 - fn) * fa);
}
function rates(key, V, d, L) {
  const r = lumped(V, d, L, f, P0 * ostG(key, f));
  let kH = r.kH;
  for (let h = 2; h <= 6; h++) { const q = lumped(V, d, L, f * h, P0 * Math.pow(h, -HARM) * ostG(key, f * h)); kH += q.kH; }
  return { x: r.x, eta: r.eta, kH, kD: r.kD, tauD: 1 / r.kD };
}
const show = (lab, key, V, d, L) => { const r = rates(key, V, d, L);
  console.log(`${lab.padEnd(34)} L0/L ${r.x.toFixed(2).padStart(5)}  eta ${(r.eta * 100).toFixed(1).padStart(5)}%  diffusion tau ${r.tauD.toFixed(0).padStart(5)} s  ` +
    `5 s: hum+diff ${(exch2(r.kH + r.kD, 5) * 100).toFixed(0).padStart(3)}% vs diff ${(exch2(r.kD, 5) * 100).toFixed(0).padStart(3)}%  | 60 s diff only ${(exch2(r.kD, 60) * 100).toFixed(0)}%`); };
console.log('frontal sinus, V 2.9 mL (pages: d 7.5 mm, L 4 mm):');
for (const [d, L] of [[7.5, 4], [5, 4], [5, 10], [4, 15], [3, 20]]) show(`  d ${d} mm, L ${L} mm`, 'fro', 2.9, d, L);
console.log('\nethmoid cell (pages: V 0.4 mL, d 1.5 mm, L 1.5 mm):');
for (const [V, d, L] of [[0.4, 1.5, 1.5], [0.4, 1.0, 1.5], [0.4, 1.0, 3.0], [0.8, 1.5, 3.0], [0.2, 2.5, 1.0]]) show(`  V ${V} mL, d ${d} mm, L ${L} mm`, 'eth', V, d, L);
console.log('\nsphenoid (pages: V 4 mL, d 2.2 mm, L 1.5 mm):');
for (const [V, d, L] of [[4, 2.2, 1.5], [4, 3.0, 1.5], [4, 1.5, 1.5], [8, 2.2, 1.5], [2, 2.2, 3.0]]) show(`  V ${V} mL, d ${d} mm, L ${L} mm`, 'sph', V, d, L);
