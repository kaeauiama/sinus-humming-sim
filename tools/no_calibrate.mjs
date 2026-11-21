// Calibrate the NO model against the in-vivo humming data (results/no_kinetics_calibration.md).
// Targets (healthy adults):
//   Menzel 2005 (J Appl Physiol 98:2064, n = 8): washout time constant during humming 3.0 +- 1.2 s;
//                                              recovery (refill) time constant 4.5 +- 3.2 min
//   Maniscalco 2003 (Eur Respir J 22:323, n = 10, 0.2 L/s, means over the last 8 s of 10-s exhalations):
//     first hum / quiet = 4.7x (Shusterman 2007: 4.2x); 5 hums at 5-s intervals -> plateau at 26 % of the first
//     within four hums; quiet exhalation right after the hums 32 % lower (range 5-50 %); with 3-min intervals the hums
//     are alike (< 15 % variability, "complete recovery"); topical L-NAME halves quiet nasal NO (mucosal share >= 50 %)
// Free: effective sound pressure P0, refill time constant tauRec, mucosal share, phi (NO production of the small
// sinuses = frontal + ethmoid, relative to the per-area rule), harmonics none / -12 dB/oct.
// Run: node tools/no_calibrate.mjs
import { simulate } from './no_model.mjs';

const REPEAT = [['silent', 10], ...Array.from({ length: 5 }, () => [['in', 5], ['hum', 10]]).flat(), ['in', 3], ['silent', 10]];
const RECOV = [['silent', 10], ['in', 5], ['hum', 10], ['in', 5], ['rest', 170], ['in', 5], ['hum', 10]];
const segs = out => { const s = []; let cur = null; out.forEach(p => { if (!cur || cur.type !== p.type) { cur = { type: p.type, pts: [] }; s.push(cur); } cur.pts.push(p); }); return s; };
const last8 = seg => { const t = seg.pts.slice(Math.round(seg.pts.length * 0.2)); return t.reduce((a, p) => a + p.c, 0) / t.length; };
function washout(seg) {   // time from the peak until (c - c_end) falls to 1/e of (c_peak - c_end)
  const c = seg.pts.map(p => p.c); let ip = 0; c.forEach((v, i) => { if (v > c[ip]) ip = i; });
  const end = c[c.length - 1], th = end + (c[ip] - end) / Math.E;
  for (let i = ip; i < c.length; i++) if (c[i] <= th) return (i - ip) * 0.05;
  return Infinity;
}
export function metrics(o) {
  const a = segs(simulate({ ...o, proto: REPEAT })), quiet = last8(a[0]);
  const hums = a.filter(s => s.type === 'hum'), sil = a.filter(s => s.type === 'silent');
  const m = hums.map(last8);
  const b = segs(simulate({ ...o, proto: RECOV })).filter(s => s.type === 'hum').map(last8);
  return { ratio: m[0] / quiet, plateau: m[4] / m[0], fourth: m[3] / m[0], drop: 1 - last8(sil[1]) / quiet, recov3: b[1] / b[0], wash: washout(hums[0]) };
}
const TARGET = { wash: [3.0, 1.2], ratio: [4.5, 0.5], plateau: [0.26, 0.08], drop: [0.32, 0.15], recov3: [0.92, 0.12] };
const cost = (r, o) => Object.entries(TARGET).reduce((a, [k, [mu, sd]]) => a + ((r[k] - mu) / sd) ** 2, 0)
  + ((o.tauRec - 270) / 190) ** 2 + (o.mucShare < 0.5 ? ((0.5 - o.mucShare) / 0.05) ** 2 : 0);
const fmt = r => `ratio ${r.ratio.toFixed(1)}x  washout ${r.wash.toFixed(1)} s  5th/1st ${(r.plateau * 100).toFixed(0)}% (4th ${(r.fourth * 100).toFixed(0)}%)  post-quiet drop ${(r.drop * 100).toFixed(0)}%  3-min recovery ${(r.recov3 * 100).toFixed(0)}%`;

const base = { f: 150, harm: 0, etaMx: null };
console.log('targets: ratio 4.2-4.7x, washout 3.0 +- 1.2 s, 5th/1st 26 %, post-quiet drop 32 % (5-50), 3-min recovery ~ complete; tauRec 4.5 +- 3.2 min; mucosa >= 50 %');
console.log('\ncurrent pages (100 Pa, tau 270 s, mucosa 70 %, phi 1):\n  ' + fmt(metrics({ ...base, P0: 100, tauRec: 270, mucShare: 0.7, phi: 1 })));
const res = [];
for (const harm of [0, 2]) for (const P0 of [80, 100, 130, 160, 200, 250, 320]) for (const tauRec of [60, 90, 120, 180, 270, 400])
  for (const mucShare of [0.5, 0.6, 0.7, 0.8]) for (const phi of [1, 0.5, 0.25, 0.1, 0.03]) {
    const o = { ...base, harm, P0, tauRec, mucShare, phi }, r = metrics(o);
    res.push({ o, r, c: cost(r, o) });
  }
res.sort((x, y) => x.c - y.c);
console.log('\nbest 12 (cost = sum of squared z-scores):');
res.slice(0, 12).forEach(({ o, r, c }) => console.log(`  cost ${c.toFixed(1).padStart(5)} | harm ${o.harm ? '-12dB' : 'none '} P0 ${String(o.P0).padStart(3)} tau ${String(o.tauRec).padStart(3)} s mucosa ${o.mucShare} phi ${String(o.phi).padEnd(4)} | ${fmt(r)}`));
// what each parameter does around the best
const b = res[0].o;
console.log('\none at a time around the best:');
for (const [k, vals] of [['P0', [100, 130, 160, 200, 250]], ['tauRec', [60, 120, 270, 400]], ['mucShare', [0.5, 0.7, 0.8]], ['phi', [1, 0.25, 0.03]]])
  for (const v of vals) console.log(`  ${k} = ${String(v).padEnd(4)}: ` + fmt(metrics({ ...b, [k]: v })));
