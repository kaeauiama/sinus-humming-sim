// NO model rebuilt after the long 3D runs (2026-11-22): the sinus air is one well-mixed box; the slow part the in-vivo
// data need sits in a mucosal store (tools/no_model.mjs o.store). Same targets and cost as tools/no_calibrate2.mjs
// (Maniscalco 2003 Fig. 3 sequence and tail, mean ratio, Menzel washout, quiet drop, 3-min recovery, Menzel refill
// prior on the slowest time constant, mucosal share >= 50 %). Run: node tools/no_calibrate3.mjs [fine]
import { simulate, storeSlowTau, maxRates } from './no_model.mjs';

const REPEAT = [['silent', 10], ...Array.from({ length: 5 }, () => [['in', 5], ['hum', 10]]).flat(), ['in', 3], ['silent', 10]];
const RECOV = [['silent', 10], ['in', 5], ['hum', 10], ['in', 5], ['rest', 170], ['in', 5], ['hum', 10]];
const segs = out => { const s = []; let cur = null; out.forEach(p => { if (!cur || cur.type !== p.type) { cur = { type: p.type, pts: [] }; s.push(cur); } cur.pts.push(p); }); return s; };
const last8 = seg => { const t = seg.pts.slice(Math.round(seg.pts.length * 0.2)); return t.reduce((a, p) => a + p.c, 0) / t.length; };
function washout(seg) {
  const c = seg.pts.map(p => p.c); let ip = 0; c.forEach((v, i) => { if (v > c[ip]) ip = i; });
  const end = c[c.length - 1], th = end + (c[ip] - end) / Math.E;
  for (let i = ip; i < c.length; i++) if (c[i] <= th) return (i - ip) * 0.05;
  return Infinity;
}
function metrics(o) {
  const a = segs(simulate({ ...o, proto: REPEAT })), quiet = last8(a[0]);
  const hums = a.filter(s => s.type === 'hum'), sil = a.filter(s => s.type === 'silent'), m = hums.map(last8);
  const h1 = hums[0].pts, at = t => h1[Math.min(h1.length - 1, Math.round(t / 0.05))].c;
  const b = segs(simulate({ ...o, proto: RECOV })).filter(s => s.type === 'hum').map(last8);
  const peak = Math.max(...h1.map(p => p.c)) / quiet;
  return { ratio: m[0] / quiet, peak, s2: m[1] / m[0], s3: m[2] / m[0], s5: m[4] / m[0], tail: at(10 - 0.05) / at(2),
           wash: washout(hums[0]), drop: 1 - last8(sil[1]) / quiet, recov3: b[1] / b[0] };
}
const TARGET = { ratio: [4.5, 0.5], s2: [0.49, 0.1], s3: [0.40, 0.1], s5: [0.27, 0.08], tail: [0.34, 0.12], wash: [3.0, 1.2], drop: [0.32, 0.15], recov3: [0.92, 0.12] };
const slowOf = o => (o.store ? storeSlowTau(o) : o.tauRec);
const cost = (r, o) => Object.entries(TARGET).reduce((s, [k, [mu, sd]]) => s + ((r[k] - mu) / sd) ** 2, 0)
  + ((slowOf(o) - 270) / 190) ** 2 + (o.mucShare < 0.5 ? ((0.5 - o.mucShare) / 0.05) ** 2 : 0);
const exch10 = o => { const r = maxRates(o); return 1 - Math.exp(-10 * (r.kH + r.kD)); };
const fmt = r => `ratio ${r.ratio.toFixed(1)}x (peak ${r.peak.toFixed(0)}x)  hums 2/3/5 ${[r.s2, r.s3, r.s5].map(v => (v * 100).toFixed(0)).join('/')}%  tail ${r.tail.toFixed(2)}  washout ${r.wash.toFixed(1)} s  drop ${(r.drop * 100).toFixed(0)}%  3-min ${(r.recov3 * 100).toFixed(0)}%`;
const base = { f: 150, harm: 2, etaMx: null, phi: 1 };
const lab = o => o.store ? `P0 ${String(o.P0).padStart(3)} store sigma ${o.store.sigma} tauEx ${o.store.tauEx} s tauRec ${o.tauRec} s (slow ${slowOf(o).toFixed(0)} s) mucosa ${o.mucShare}`
  : `P0 ${o.P0} fn ${o.fn ?? 1} tauInt ${o.tauInt ?? '-'} tauRec ${o.tauRec} mucosa ${o.mucShare}`;

console.log('targets: ratio 4.2-4.7x, hums 2/3/5 = 49/40/27 %, tail 0.34, washout 3.0 s, drop 32 %, 3-min ~complete, slow time ~270 s');
for (const o of [{ ...base, P0: 130, tauRec: 270, mucShare: 0.5, fn: 0.5, tauInt: 40 }, { ...base, P0: 200, tauRec: 120, mucShare: 0.5 }]) {
  const r = metrics(o); console.log(`  ${o.fn ? 'pages now (two air compartments)' : 'one box, no store            '}: cost ${cost(r, o).toFixed(1)} | ${fmt(r)}`);
}
const res = [];
const FINE = process.argv.includes('fine');
const G = FINE ? { P0: [140, 160, 180, 200, 230], sigma: [0.3, 0.45, 0.6, 0.8, 1, 1.5], tauEx: [8, 12, 16, 24, 32, 64], tauRec: [60, 90, 120, 150, 270], mucShare: [0.6, 0.7, 0.8] }
  : { P0: [130, 160, 200, 250, 320], sigma: [0.3, 0.6, 1, 1.5, 2.5, 4], tauEx: [0.5, 1, 2, 4, 8, 16], tauRec: [90, 150, 270, 450], mucShare: [0.5, 0.6, 0.7] };
for (const P0 of G.P0) for (const sigma of G.sigma) for (const tauEx of G.tauEx)
  for (const tauRec of G.tauRec) for (const mucShare of G.mucShare) {
    const o = { ...base, P0, tauRec, mucShare, store: { sigma, tauEx } }, r = metrics(o);
    res.push({ o, r, c: cost(r, o) });
  }
res.sort((x, y) => x.c - y.c);
console.log(`\nbest 12 of ${res.length} (one-box air + mucosal store):`);
res.slice(0, 12).forEach(({ o, r, c }) => console.log(`  cost ${c.toFixed(1).padStart(5)} | ${lab(o)} | ${fmt(r)} | air exchanged in 10 s ${(exch10(o) * 100).toFixed(0)}%`));
// how well each parameter is pinned: best cost for each value
for (const key of ['P0', 'sigma', 'tauEx', 'tauRec', 'mucShare']) {
  const vals = [...new Set(res.map(x => key === 'sigma' || key === 'tauEx' ? x.o.store[key] : x.o[key]))];
  console.log(`  best cost by ${key}: ` + vals.map(v => { const b = res.find(x => (key === 'sigma' || key === 'tauEx' ? x.o.store[key] : x.o[key]) === v); return `${v}: ${b.c.toFixed(1)}`; }).join(', '));
}
