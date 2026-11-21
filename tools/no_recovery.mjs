// Recovery of the humming NO peak with the rest interval, measured the way Menzel 2005 did (peak height of a hum
// vs the time since the previous hum, fitted with 1 - exp(-dt/tau)), in the NO model (store and older versions).
// Also Maniscalco 2003's 1-min and 3-min interval series (mean of last 8 s), hum k+1 / hum k.
// Run: node tools/no_recovery.mjs
import { simulate } from './no_model.mjs';

const segs = out => { const s = []; let cur = null; out.forEach(p => { if (!cur || cur.type !== p.type) { cur = { type: p.type, pts: [] }; s.push(cur); } cur.pts.push(p); }); return s; };
const peak = seg => Math.max(...seg.pts.map(p => p.c));
const last8 = seg => { const t = seg.pts.slice(Math.round(seg.pts.length * 0.2)); return t.reduce((a, p) => a + p.c, 0) / t.length; };
const DTS = [5, 15, 30, 60, 120, 180, 300, 600, 1200];
function recovery(o) {
  // rested hum, then after dt another hum; both preceded by a 5-s inhalation
  return DTS.map(dt => {
    const proto = [['silent', 10], ['in', 5], ['hum', 10], ['rest', Math.max(0.05, dt - 5)], ['in', 5], ['hum', 10]];
    const h = segs(simulate({ ...o, proto })).filter(s => s.type === 'hum');
    return { dt, peak: peak(h[1]) / peak(h[0]), mean: last8(h[1]) / last8(h[0]) };
  });
}
function fitTau(rows, key) {   // least squares of 1 - exp(-dt/tau) on the recovered fraction above the immediate value
  let best = null; const r0 = rows[0][key];
  for (let tau = 5; tau <= 1200; tau *= 1.02) {
    const e = rows.reduce((a, r) => a + ((r[key] - r0) / (1 - r0) - (1 - Math.exp(-(r.dt - rows[0].dt) / tau))) ** 2, 0);
    if (!best || e < best.e) best = { tau, e };
  }
  return best.tau;
}
const base = { f: 150, harm: 2, P0: 130, mucShare: 0.5, phi: 1, fn: 0.5, tauInt: 40 };
const STORE = { f: 150, harm: 2, P0: 180, mucShare: 0.7, phi: 1, tauRec: 120, store: { sigma: 0.6, tauEx: 24 } };   // pages since 2026-11-22
for (const [lab, o] of [['one-box air + mucosal store (pages since 2026-11-22)', STORE],
                        ['two compartments, tauRec 270 s (pages 2026-11-21)', { ...base, tauRec: 270 }],
                        ['two compartments, tauRec 600 s', { ...base, tauRec: 600 }],
                        ['two compartments, tauRec 120 s', { ...base, tauRec: 120 }],
                        ['one compartment, 200 Pa, tauRec 120 s', { ...base, P0: 200, fn: 1, tauRec: 120 }],
                        ['one compartment, 100 Pa, tauRec 270 s (original pages)', { ...base, P0: 100, harm: 0, fn: 1, mucShare: 0.7, tauRec: 270 }]]) {
  const rows = recovery(o);
  console.log(`\n${lab}`);
  console.log('  dt (s)      ' + rows.map(r => String(r.dt).padStart(6)).join(''));
  console.log('  peak ratio  ' + rows.map(r => (r.peak * 100).toFixed(0).padStart(5) + '%').join(''));
  console.log('  mean ratio  ' + rows.map(r => (r.mean * 100).toFixed(0).padStart(5) + '%').join(''));
  console.log(`  apparent recovery time constant from peaks (Menzel's way): ${(fitTau(rows, 'peak') / 60).toFixed(1)} min; from means: ${(fitTau(rows, 'mean') / 60).toFixed(1)} min`);
}
console.log('\nMenzel 2005: 4.5 +- 3.2 min (peaks). Maniscalco 2003: 3-min intervals alike (< 15 % variability), 1-min intervals ~70 % variability.');
