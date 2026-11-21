// Two-compartment sinuses vs the in-vivo humming data (results/no_kinetics_2compartment.md).
// Extra targets read from Maniscalco 2003 Fig. 3 (one subject's tracings, 5 hums at 5-s intervals, digitised):
//   hum 1 peaks at ~1.2 s, falls to ~2/3 within ~1.5 s, then declines slowly: c(10 s)/c(2 s) = 0.34;
//   mean of last 8 s relative to hum 1: hum 2 ~0.49, hum 3 ~0.40, hums 4-5 ~0.3 (text: plateau 26 %)
// Plus the earlier targets (tools/no_calibrate.mjs): mean ratio 4.2-4.7x, Menzel washout 3.0 +- 1.2 s, quiet drop
// after the hums 32 % (5-50), 3-min recovery ~complete, Menzel refill 4.5 +- 3.2 min, mucosal share >= 50 %.
// Run: node tools/no_calibrate2.mjs
import { simulate } from './no_model.mjs';

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
  return { ratio: m[0] / quiet, s2: m[1] / m[0], s3: m[2] / m[0], s5: m[4] / m[0], tail: at(10 - 0.05) / at(2),
           wash: washout(hums[0]), drop: 1 - last8(sil[1]) / quiet, recov3: b[1] / b[0] };
}
const TARGET = { ratio: [4.5, 0.5], s2: [0.49, 0.1], s3: [0.40, 0.1], s5: [0.27, 0.08], tail: [0.34, 0.12], wash: [3.0, 1.2], drop: [0.32, 0.15], recov3: [0.92, 0.12] };
const cost = (r, o) => Object.entries(TARGET).reduce((s, [k, [mu, sd]]) => s + ((r[k] - mu) / sd) ** 2, 0)
  + ((o.tauRec - 270) / 190) ** 2 + (o.mucShare < 0.5 ? ((0.5 - o.mucShare) / 0.05) ** 2 : 0);
const fmt = r => `ratio ${r.ratio.toFixed(1)}x  hums 2/3/5 ${[r.s2, r.s3, r.s5].map(v => (v * 100).toFixed(0)).join('/')}%  tail ${r.tail.toFixed(2)}  washout ${r.wash.toFixed(1)} s  drop ${(r.drop * 100).toFixed(0)}%  3-min ${(r.recov3 * 100).toFixed(0)}%`;
const base = { f: 150, harm: 2, etaMx: null };
console.log('targets: ratio 4.2-4.7x, hums 2/3/5 = 49/40/27 %, tail c(10)/c(2) 0.34, washout 3.0 s, drop 32 %, 3-min ~complete');
const one = { ...base, P0: 200, tauRec: 120, mucShare: 0.5, phi: 1 };
const r1 = metrics(one); console.log(`\none compartment, calibrated (200 Pa, tau 120 s, mucosa 50 %): cost ${cost(r1, one).toFixed(1)}\n  ${fmt(r1)}`);
const res = [];
for (const P0 of [130, 160, 200, 250, 320]) for (const tauRec of [60, 90, 120, 180, 270]) for (const mucShare of [0.5, 0.6, 0.7])
  for (const phi of [1, 0.3]) for (const fn of [1, 0.5, 0.3, 0.2]) for (const tauInt of (fn < 1 ? [5, 10, 20, 40, 80] : [0])) {
    const o = { ...base, P0, tauRec, mucShare, phi, fn, tauInt }, r = metrics(o);
    res.push({ o, r, c: cost(r, o) });
  }
res.sort((x, y) => x.c - y.c);
const lab = o => `P0 ${String(o.P0).padStart(3)} tau ${String(o.tauRec).padStart(3)} s mucosa ${o.mucShare} phi ${o.phi} fn ${o.fn} tauInt ${o.tauInt} s`;
console.log('\nbest 10 overall:');
res.slice(0, 10).forEach(({ o, r, c }) => console.log(`  cost ${c.toFixed(1).padStart(5)} | ${lab(o)} | ${fmt(r)}`));
const b1 = res.filter(x => x.o.fn === 1)[0];
console.log(`\nbest one-compartment: cost ${b1.c.toFixed(1)} | ${lab(b1.o)} | ${fmt(b1.r)}`);
