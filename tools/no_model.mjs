// NO model of the pages (same as pages/integrated.template.html simulateNO / summarize), for comparing
// different definitions of "how much does humming raise nasal NO".
//   peak ratio  : first humming peak / quiet exhalation            (what the pages show)
//   mean ratio  : mean nasal NO output over the last 8 s of a 10-s hum / quiet  (Maniscalco 2003: 2233/471 = 4.7x;
//                 Shusterman 2007: 4.2x with a similar parallel sampling)
// Run: node tools/no_model.mjs
import { lumped, mix } from './model.mjs';
import fs from 'node:fs';

// sound pressure at each ostium relative to the maxillary ostium (tools/ostium_pressure.py); o.ostP = false turns it off
const OSTP = JSON.parse(fs.readFileSync(new URL('../results/ostium_pressure.json', import.meta.url), 'utf8'));
export function ostG(key, f) {
  const g = OSTP.g[key]; if (!g) return 1;
  const F = OSTP.freqs_hz, lf = Math.log(f);
  if (f <= F[0]) return g[0]; if (f >= F[F.length - 1]) return g[g.length - 1];
  let i = 0; while (F[i + 1] < f) i++;
  const t = (lf - Math.log(F[i])) / (Math.log(F[i + 1]) - Math.log(F[i]));
  return g[i] + t * (g[i + 1] - g[i]);
}

const NOP = { mucShare: 0.70, cssMax: 8000, tauRec: 270 };
const SIN = [
  { name: 'maxillary', key: 'max', V: 14.0, d: 2.8, L: 2.1, n: 1 },
  { name: 'sphenoid', key: 'sph', V: 4.0, d: 2.2, L: 1.5, n: 1 },
  { name: 'frontal', key: 'fro', V: 2.9, d: 7.5, L: 4.0, n: 1 },
  { name: 'ethmoid', key: 'eth', V: 0.4, d: 1.5, L: 1.5, n: 8 },
];
const PROTO = [['silent', 5], ['in', 3], ['hum', 10], ['in', 3], ['hum', 10], ['in', 3], ['hum', 10], ['in', 3], ['silent', 5], ['rest', 180], ['hum', 10], ['in', 3], ['silent', 5]];
const area = V => 4.836 * Math.pow(V, 2 / 3);

// opts: f, P0, harm (0 = none, 2 = -12 dB/oct, 1 = -6 dB/oct), etaMx (null = law),
//       tauRec (s), mucShare, phi (NO production of frontal + ethmoid relative to the per-area rule), proto
function humRate(s, o, eta0) {
  const g = f => (o.ostP === false ? 1 : ostG(s.key, f));
  const r = lumped(s.V, s.d, s.L, o.f, o.P0 * g(o.f));
  let k = (eta0 == null ? mix(r.x, r.ld) : eta0) * r.Vin * o.f / (s.V * 1e-6);
  if (o.harm > 0) for (let h = 2; h <= 6; h++) { const q = lumped(s.V, s.d, s.L, o.f * h, o.P0 * Math.pow(h, -o.harm) * g(o.f * h)); k += q.eta * q.Vin * o.f * h / (s.V * 1e-6); }
  return { k, kD: r.kD };
}
// slowest time constant of the maxillary sinus at rest with the store (for the Menzel prior)
export function storeSlowTau(o) {
  const s = SIN[0], r = humRate(s, o, null), S = area(s.V), sg = o.store.sigma, ge = 1 / o.store.tauEx, kl = 1 / (o.tauRec || NOP.tauRec);
  const a11 = -ge - r.kD, a12 = ge, a21 = ge / sg, a22 = -kl - ge / sg, tr = a11 + a22, det = a11 * a22 - a12 * a21;
  const lam = (tr + Math.sqrt(tr * tr - 4 * det)) / 2;   // the less negative eigenvalue
  return -1 / lam;
}
export function maxRates(o) { const r = humRate(SIN[0], o, o.etaMx ?? null); return { kH: r.k, kD: r.kD }; }
export function simulate(o) {
  const phi = o.phi ?? 1, mucShare = o.mucShare ?? NOP.mucShare, small = i => (i >= 2 ? phi : 1);   // frontal, ethmoid
  const set = SIN.map((s, i) => { const r = humRate(s, o, i === 0 ? o.etaMx : null); return { ...s, S: area(s.V), kD: r.kD, kH: r.k }; });
  const mx = set[0], tauRec = o.tauRec || NOP.tauRec;
  const kLoss = Math.max(1 / tauRec - mx.kD, 1 / (tauRec * 20));
  const ppa = NOP.cssMax * (kLoss + mx.kD) * mx.V / mx.S;
  set.forEach((x, i) => { x.P = ppa * small(i) * x.S / x.V; x.C = x.P / (kLoss + x.kD); });
  const ref = SIN.map(s => ({ s, kD: lumped(s.V, s.d, s.L, o.f, o.P0).kD }));
  const kLr = Math.max(1 / tauRec - ref[0].kD, 1 / (tauRec * 20));
  const pRef = NOP.cssMax * (kLr + ref[0].kD) * SIN[0].V / area(SIN[0].V);
  const refFlux = ref.reduce((a, x, i) => { const P = pRef * small(i) * area(x.s.V) / x.s.V; return a + x.s.n * x.s.V * x.kD * P / (kLr + x.kD); }, 0);
  let M = refFlux * mucShare / (1 - mucShare);
  // optional two-compartment sinuses: a near-ostium part (fraction fn of the volume) exchanged by humming and
  // diffusion, and a far part that mixes with it at rate 1/tauInt (exchange volume per s / whole volume)
  const fn = o.fn ?? 1, two = fn < 1, kI = two ? 1 / (o.tauInt || 30) : 0, a = two ? kI / (1 - fn) : 0, b = two ? kI / fn : 0;
  if (two) {
    set.forEach(x => {   // quiet steady state
      const g = kLoss + a, CN = x.P * (1 + b / g) / (kLoss + x.kD / fn + b - b * a / g);
      x.CN = CN; x.CF = (x.P + a * CN) / g;
    });
    M = set.reduce((s, x) => s + x.n * x.V * x.kD * x.CN, 0) * mucShare / (1 - mucShare);
  }
  // optional mucosal store (2026-11-22): the sinus air is one well-mixed box (long 3D runs,
  // results/agefield_maxillary.md); a store at the mucosa (capacity sigma x the air volume, scaled with area/volume
  // relative to the maxillary sinus) exchanges NO with the air on tauEx (also scaled), receives all the production and
  // loses NO on tauRec (uptake into the blood). Chemical store or production that rises when the air NO falls: the
  // equations are the same. o.store = { sigma, tauEx }; o.fn must be 1.
  const st = o.store, kl = st ? 1 / tauRec : 0;
  if (st) {
    const sv = mx.S / mx.V;
    set.forEach(x => { const f = (x.S / x.V) / sv; x.sg = st.sigma * f; x.ge = f / st.tauEx; });
    const Cm = NOP.cssMax, Pm = mx.sg * kl * Cm * (1 + mx.kD / mx.ge) + mx.kD * Cm, ppa2 = Pm * mx.V / mx.S;
    set.forEach((x, i) => {
      x.P = ppa2 * small(i) * x.S / x.V;
      x.C = x.P / (x.sg * kl * (1 + x.kD / x.ge) + x.kD); x.Sv = x.C * (1 + x.kD / x.ge);
    });
    M = set.reduce((s, x) => s + x.n * x.V * x.kD * x.C, 0) * mucShare / (1 - mucShare);
  }
  const dt = 0.05, out = []; let t = 0;
  for (const [type, dur] of (o.proto || PROTO)) {
    const n = Math.round(dur / dt);
    for (let i = 0; i < n; i++) {
      let src = 0;
      if (st) set.forEach(x => {
        const k = x.kD + (type === 'hum' ? x.kH : 0); src += x.n * x.V * k * x.C;
        const ex = x.ge * (x.Sv - x.C), dC = ex - k * x.C, dS = (x.P - x.sg * kl * x.Sv - ex) / x.sg;
        x.C += dt * dC; x.Sv += dt * dS;
      });
      else if (two) set.forEach(x => {
        const k = x.kD + (type === 'hum' ? x.kH : 0); src += x.n * x.V * k * x.CN;
        const dN = x.P - kLoss * x.CN - (k / fn) * x.CN + b * (x.CF - x.CN), dF = x.P - kLoss * x.CF + a * (x.CN - x.CF);
        x.CN += dt * dN; x.CF += dt * dF;
      });
      else set.forEach(x => { const k = x.kD + (type === 'hum' ? x.kH : 0); src += x.n * x.V * k * x.C; x.C += dt * (x.P - kLoss * x.C - k * x.C); });
      const ex = type === 'silent' || type === 'hum';
      out.push({ t, type, i, n, c: ex ? M + src : null });
      t += dt;
    }
  }
  return out;
}
export function summarize(out) {
  const quietPts = out.filter(p => p.type === 'silent').slice(0, 80);       // first quiet exhalation (4 s)
  const quiet = quietPts.reduce((a, p) => a + p.c, 0) / quietPts.length;
  const hums = []; let cur = null;
  out.forEach(p => { if (p.type === 'hum') { if (!cur) { cur = []; hums.push(cur); } cur.push(p); } else cur = null; });
  const h1 = hums[0], peak = Math.max(...h1.map(p => p.c));
  const last8 = h1.filter(p => p.i >= p.n * 0.2), mean8 = last8.reduce((a, p) => a + p.c, 0) / last8.length;
  return { peak: peak / quiet, mean8: mean8 / quiet, step: Math.max(...hums[1].map(p => p.c)) / peak, recov: Math.max(...hums[3].map(p => p.c)) / peak };
}
const fmt = s => `peak ${s.peak.toFixed(1)}x  mean(last 8 s) ${s.mean8.toFixed(1)}x  2nd/1st ${(s.step * 100).toFixed(0)}%  after 3 min ${(s.recov * 100).toFixed(0)}%`;

if ((process.argv[1] || '').endsWith('no_model.mjs')) {
  const base = { f: 150, P0: 100, harm: 0, etaMx: null };
  console.log('150 Hz, 100 Pa, law          :', fmt(summarize(simulate(base))));
  console.log('150 Hz, 100 Pa, 3D eta 0.35  :', fmt(summarize(simulate({ ...base, etaMx: 0.35 }))));
  for (const harm of [2, 1]) console.log(`150 Hz, 100 Pa, harmonics n^-${harm}:`, fmt(summarize(simulate({ ...base, harm }))));
  // pressure needed to reach each literature figure, by definition
  // smallest P0 reaching the target (the mean ratio saturates and then falls, so scan before bisecting)
  const solve = (key, target, harm) => {
    const val = P0 => summarize(simulate({ ...base, P0, harm }))[key];
    let prev = 5, best = { v: 0, p: 5 };
    for (let i = 1; i <= 40; i++) {
      const p = 5 * Math.pow(400, i / 40), v = val(p); if (v > best.v) best = { v, p };
      if (v >= target) { let lo = prev, hi = p; for (let k = 0; k < 30; k++) { const m = Math.sqrt(lo * hi); if (val(m) >= target) hi = m; else lo = m; } return `${hi.toFixed(0)} Pa`; }
      prev = p;
    }
    return `never (max ${best.v.toFixed(1)}x at ${best.p.toFixed(0)} Pa)`;
  };
  for (const harm of [0, 2, 1]) {
    const lab = harm === 0 ? 'no harmonics ' : `harm n^-${harm}   `;
    console.log(`${lab}: mean ratio 4.2x at ${solve('mean8', 4.2, harm)}, 4.7x at ${solve('mean8', 4.7, harm)}; peak 15x at ${solve('peak', 15, harm)}`);
  }
  console.log('\nP0 sweep (no harmonics):');
  for (const P0 of [30, 50, 70, 100, 150, 200, 300]) console.log(`  ${String(P0).padStart(3)} Pa: ` + fmt(summarize(simulate({ ...base, P0 }))));
  console.log('\nRecovery time constant (sinus refill) x pressure, weak harmonics n^-2, law for all sinuses:');
  for (const tauRec of [270, 120, 90, 60]) for (const P0 of [100, 150, 200]) {
    console.log(`  tau ${String(tauRec).padStart(3)} s, ${String(P0).padStart(3)} Pa: ` + fmt(summarize(simulate({ ...base, P0, harm: 2, tauRec }))));
  }
}
