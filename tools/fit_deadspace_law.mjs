// Fit the dead-space (mixing) law to results/deadspace_law_3d.csv (DC = 10 rows).
// x = L0/L (dead space), j = L0/d = x * L/d (jet formation: a stroke shorter than about one diameter
// does not shed a vortex ring that escapes).
// Forms:
//   old  eta = 0.59 (1 - exp(-(x/1.89)^1.76))                         (fitted at DC 8 on the buggy engine)
//   (a)  eta = m (1 - exp(-(x/x0)^n))                                  one curve
//   (c)  eta = m(L/d) (1 - exp(-(x/x0)^n)), m = mInf (1 - exp(-(L/d)/lam))
//   (d)  eta = m (1 - exp(-(x/x0)^n)) (1 - exp(-(j/k)^p))              dead space x jet formation
//   (e)  (d) x exp(-(L/d)/lam)                                         long-tube decline
// Run: node tools/fit_deadspace_law.mjs [maxLd]   (maxLd: only rows with L/d <= maxLd; default all; 3 = roadmap 1 set)
import fs from 'node:fs';
const maxLd = +process.argv[2] || Infinity;
const rows = fs.readFileSync(new URL('../results/deadspace_law_3d.csv', import.meta.url), 'utf8')
  .split('\n').filter(l => l && !l.startsWith('#') && !l.startsWith('L_over_d'))
  .map(l => l.split(',').map(Number)).filter(r => r[4] === 10 && r[5] === 300 && r[0] <= maxLd).map(([ld, , x, eta]) => ({ ld, x, eta }));
const sat = (v, v0, n) => 1 - Math.exp(-Math.pow(Math.max(v, 0) / v0, n));
const F = {
  old: (r) => 0.59 * sat(r.x, 1.89, 1.76),
  a: (r, [m, x0, n]) => m * sat(r.x, x0, n),
  c: (r, [mInf, lam, x0, n]) => mInf * (1 - Math.exp(-r.ld / lam)) * sat(r.x, x0, n),
  d: (r, [m, x0, n, k, p]) => m * sat(r.x, x0, n) * sat(r.x * r.ld, k, p),
  e: (r, [m, x0, n, k, p, lam]) => m * sat(r.x, x0, n) * sat(r.x * r.ld, k, p) * Math.exp(-r.ld / lam),
};
const rms = (f, p) => Math.sqrt(rows.reduce((a, r) => a + (f(r, p) - r.eta) ** 2, 0) / rows.length);
// Nelder-Mead on rms, parameters kept positive, several starts
function nm(f, p0) {
  const n = p0.length, cost = p => (p.some(v => v <= 0) ? 1e9 : rms(f, p));
  let S = [p0, ...p0.map((_, i) => p0.map((v, j) => (j === i ? v * 1.3 : v)))].map(p => ({ p, c: cost(p) }));
  for (let it = 0; it < 4000; it++) {
    S.sort((a, b) => a.c - b.c);
    const c = Array(n).fill(0); for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) c[j] += S[i].p[j] / n;
    const w = S[n], pt = (t) => c.map((v, j) => v + t * (w.p[j] - v));
    const r = { p: pt(-1) }; r.c = cost(r.p);
    if (r.c < S[0].c) { const e = { p: pt(-2) }; e.c = cost(e.p); S[n] = e.c < r.c ? e : r; }
    else if (r.c < S[n - 1].c) S[n] = r;
    else { const k = { p: pt(0.5) }; k.c = cost(k.p); if (k.c < w.c) S[n] = k; else S = S.map((s, i) => (i ? { p: s.p.map((v, j) => S[0].p[j] + 0.5 * (v - S[0].p[j])) } : s)).map(s => ({ p: s.p, c: cost(s.p) })); }
  }
  S.sort((a, b) => a.c - b.c); return S[0];
}
const best = (f, starts) => starts.map(s => nm(f, s)).sort((a, b) => a.c - b.c)[0];
const A = best(F.a, [[0.6, 1.9, 2], [0.7, 1.5, 1.5]]);
const C = best(F.c, [[0.66, 0.45, 1.9, 1.95], [0.7, 0.8, 1.8, 2]]);
const D = best(F.d, [[0.65, 1.9, 2, 1, 1.5], [0.7, 1.5, 1.5, 0.7, 2], [0.6, 2.2, 2.5, 1.2, 1]]);
const E = best(F.e, [[0.67, 1.7, 1.9, 1, 0.5, 60], [0.7, 1.6, 1.8, 0.8, 0.7, 40], [0.65, 1.9, 2, 1.2, 0.5, 100]]);
const D3 = [0.670, 1.691, 1.867, 0.998, 0.513];   // (d) as fitted on L/d <= 3 (roadmap 1, used by the pages)
const pct = v => (v * 100).toFixed(1), fx = (p, k = 3) => p.map(v => v.toFixed(k)).join(', ');
console.log(`points: ${rows.length}${isFinite(maxLd) ? ` (L/d <= ${maxLd})` : ''}`);
console.log(`old  rms ${pct(rms(F.old))} pts`);
console.log(`(a)  [m, x0, n] = [${fx(A.p)}]  rms ${pct(A.c)} pts`);
console.log(`(c)  [mInf, lam, x0, n] = [${fx(C.p)}]  rms ${pct(C.c)} pts`);
console.log(`(d)  [m, x0, n, k, p] = [${fx(D.p)}]  rms ${pct(D.c)} pts`);
console.log(`(d3) roadmap-1 (d) on these points  rms ${pct(rms(F.d, D3))} pts`);
console.log(`(e)  [m, x0, n, k, p, lam] = [${fx(E.p)}]  rms ${pct(E.c)} pts`);
console.log('\n L/d    x   L0/d  eta3D   old   (a)   (c)   (d)  (d3)   (e)');
rows.forEach(r => console.log(`${r.ld.toFixed(1).padStart(4)} ${r.x.toFixed(2).padStart(5)} ${(r.x * r.ld).toFixed(2).padStart(5)} ${pct(r.eta).padStart(6)} ${pct(F.old(r)).padStart(5)} ${pct(F.a(r, A.p)).padStart(5)} ${pct(F.c(r, C.p)).padStart(5)} ${pct(F.d(r, D.p)).padStart(5)} ${pct(F.d(r, D3)).padStart(5)} ${pct(F.e(r, E.p)).padStart(5)}`));
for (const [nm, f, p] of [['(d3)', F.d, D3], ['(e)', F.e, E.p]]) {
  console.log(`\n ${nm} at x = 0.5 / 1 / 1.5 / 2 / 3 / 4 / 8:`);
  for (const ld of [0.5, 0.75, 1, 1.5, 3, 10, 20, 30]) console.log(` L/d=${String(ld).padEnd(5)}` + [0.5, 1, 1.5, 2, 3, 4, 8].map(x => pct(f({ x, ld }, p)).padStart(6)).join(''));
}
