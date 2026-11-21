// Fit the lumped model to Fig. 6 of Maniscalco et al. 2003 (Eur Respir J 22:323): fraction of syringe gas
// exchanged by one 10-s human hum (0.2 L/s, 15 mL, 1 cmH2O), read from the figure, versus tip diameter.
// The tip LENGTH is not reported. Questions: (A) can one length for all tips reproduce Fig. 6?
// (B) if each tip has its own length, what lengths would be needed, and are they plausible?
// Run: node tools/syringe_fig6_fit.mjs          (refit mixing law; tips are L/d 9-30, beyond its tested range)
//      LAW=old node tools/syringe_fig6_fit.mjs  (the old soft law, as first recorded in results/syringe_fig6_fit.md)
import { lumped as lumpedModel, mix, mixOld } from './model.mjs';
const LAW = process.env.LAW === 'old' ? mixOld : mix;
console.log(`mixing law: ${process.env.LAW === 'old' ? 'old soft law' : 'refit 2026-11-21'}`);
const lumped = (V, d, Lmm, f, P0) => lumpedModel(V, d, Lmm, f, P0, LAW);
const V = 15, T = 10;
const DS = [0.8, 1.29, 1.9, 2.1, 4.0];
const FIG6 = [6, 50, 75, 81, 97];          // % exchanged after one 10-s hum, digitised (±2 points)
const ex = (d, L, f, P0) => 100 * (1 - Math.exp(-lumped(V, d, L, f, P0).kH * T));
const fmt = a => a.map(v => v.toFixed(0).padStart(3)).join(' ');

// (0) the paper says the standard system (15 mL, 1.9 mm) resonates at 200 Hz -> implied tip length in this model
{ let lo = 0.1, hi = 100; for (let i = 0; i < 60; i++) { const m = (lo + hi) / 2; if (lumped(V, 1.9, m, 200, 100).f0 > 200) lo = m; else hi = m; }
  console.log(`(0) f0 = 200 Hz at 15 mL / 1.9 mm needs L = ${lo.toFixed(1)} mm here (L_e = L + 1.7 r)`); }

// (A) one length for all tips
for (const f of [130, 150]) {
  let best = null;
  for (let L = 0.5; L <= 80; L += 0.5) for (let lp = 1.3; lp <= 3.6; lp += 0.01) {
    const P0 = 10 ** lp, e = DS.map(d => ex(d, L, f, P0));
    const sse = e.reduce((a, v, i) => a + (v - FIG6[i]) ** 2, 0);
    if (!best || sse < best.sse) best = { L, P0, e, sse };
  }
  console.log(`(A) f=${f} Hz best single length: L=${best.L} mm P0=${best.P0.toFixed(0)} Pa  model ${fmt(best.e)}  vs Fig.6 ${fmt(FIG6)}  rms ${Math.sqrt(best.sse / 5).toFixed(1)} pts`);
  DS.forEach(d => { const r = lumped(V, d, best.L, f, best.P0);
    console.log(`     d=${d} f0=${r.f0.toFixed(0)} L0=${r.L0mm.toFixed(1)}mm L0/L=${r.x.toFixed(2)} eta=${r.eta.toFixed(2)} Vin=${r.Vin_uL.toFixed(1)}uL Re=${r.Re.toFixed(0)}`); });
}

// (B) each tip its own length: for a given P0, which L reproduces each Fig. 6 point? (all roots on 0.2..300 mm)
function roots(d, f, P0, target) {
  const out = []; let pL = 0.2, pv = ex(d, pL, f, P0) - target;
  for (let L = 0.25; L <= 300; L *= 1.01) { const v = ex(d, L, f, P0) - target;
    if (Math.sign(v) !== Math.sign(pv)) { let a = pL, b = L; for (let i = 0; i < 50; i++) { const m = (a + b) / 2;
      if (Math.sign(ex(d, m, f, P0) - target) === Math.sign(pv)) a = m; else b = m; } out.push(((a + b) / 2).toFixed(1)); }
    pL = L; pv = v; }
  const lo = ex(d, 0.2, f, P0), hi = ex(d, 300, f, P0);
  return out.length ? out.join(' or ') : `none (range ${Math.min(lo, hi).toFixed(0)}-${Math.max(lo, hi).toFixed(0)}%)`;
}
for (const f of [150]) for (const P0 of [150, 250, 400, 600, 1000]) {
  console.log(`(B) f=${f} P0=${P0}: ` + DS.map((d, i) => `${d}mm->${roots(d, f, P0, FIG6[i])}`).join(' | '));
}

// (C) two lengths: the four tips 0.8-2.1 mm share one length L, the 4.0 mm opening has its own L4 (3 parameters, 5 points)
for (const f of [130, 150]) {
  let best = null; const grid = [];
  for (let L = 1; L <= 80; L += 0.5) for (let L4 = 0.5; L4 <= 10; L4 += 0.5) for (let lp = 1.5; lp <= 3.3; lp += 0.01) {
    const P0 = 10 ** lp, e = DS.map(d => ex(d, d === 4 ? L4 : L, f, P0));
    const sse = e.reduce((a, v, i) => a + (v - FIG6[i]) ** 2, 0);
    grid.push({ L, L4, P0, sse });
    if (!best || sse < best.sse) best = { L, L4, P0, e, sse };
  }
  console.log(`(C) f=${f} Hz best: L=${best.L} mm, L4=${best.L4} mm, P0=${best.P0.toFixed(0)} Pa  model ${fmt(best.e)}  vs Fig.6 ${fmt(FIG6)}  rms ${Math.sqrt(best.sse / 5).toFixed(1)} pts`);
  DS.forEach(d => { const r = lumped(V, d, d === 4 ? best.L4 : best.L, f, best.P0);
    console.log(`     d=${d} L/d=${((d === 4 ? best.L4 : best.L) / d).toFixed(1)} f0=${r.f0.toFixed(0)} L0=${r.L0mm.toFixed(1)}mm L0/L=${r.x.toFixed(2)} L0/d=${(r.L0mm / d).toFixed(1)} eta=${r.eta.toFixed(2)} Vin=${r.Vin_uL.toFixed(1)}uL Re=${r.Re.toFixed(0)}`); });
  // how well determined: parameter ranges with rms within 1 point of the best
  const ok = grid.filter(g => Math.sqrt(g.sse / 5) <= Math.sqrt(best.sse / 5) + 1);
  const rng = k => `${Math.min(...ok.map(g => g[k])).toFixed(0)}-${Math.max(...ok.map(g => g[k])).toFixed(0)}`;
  console.log(`     rms within +1 pt: L ${rng('L')} mm, L4 ${rng('L4')} mm, P0 ${rng('P0')} Pa`);
  // frequency response of the 1.9 mm tip with these parameters (the paper's frequency data change the sound source too)
  const fr = [120, 130, 150, 200, 450].map(ff => `${ff}Hz ${ex(1.9, best.L, ff, best.P0).toFixed(0)}%`).join(', ');
  console.log(`     1.9 mm, same P0, other frequencies: ${fr}`);
}
