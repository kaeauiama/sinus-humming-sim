// Shared lumped resonance model and mixing law for the Node tools.
// The pages carry their own copies (they must stay self-contained): see docs/methods.md §6.
export const RHO = 1.14, C0 = 350, MU = 1.9e-5, KLOSS = 1.5, DNO = 2.0e-5;

// Mixing law, 3D LBM on the ideal geometry, refit 2026-11-21 (results/deadspace_law_fit.md):
// eta = m (1 - exp(-(x/x0)^n)) (1 - exp(-(j/k)^p)) exp(-(L/d)/lam), x = L0/L (dead space), j = L0/d (stroke in
// diameters), the last factor = long tubes mix less. Measured for L/d = 0.5-20, x = 0.5-4 (x <= 2 beyond L/d 3), Re 300.
export const MIX = { m: 0.695, x0: 1.68, n: 1.76, k: 1.15, p: 0.57, lam: 48 };
const sat = (v, v0, n) => 1 - Math.exp(-Math.pow(Math.max(v, 0) / v0, n));
export const mix = (x, ld) => MIX.m * sat(x, MIX.x0, MIX.n) * sat(x * ld, MIX.k, MIX.p) * Math.exp(-ld / MIX.lam);
// the previous law (one curve, fitted at DC 8 on the engine with the amplitude bug), for comparison only
export const mixOld = x => 0.59 * sat(x, 1.89, 1.76);

// Helmholtz resonator driven by pressure amplitude P0 (Pa) at f (Hz). V in mL, d and Lmm in mm.
export function lumped(V, d, Lmm, f, P0, law = mix) {
  const r = d / 2e3, A = Math.PI * r * r, L = Lmm / 1e3, Le = L + 1.7 * r, Vm = V * 1e-6, w = 2 * Math.PI * f;
  const M = RHO * Le / A, Cc = Vm / (RHO * C0 * C0), X = w * M - 1 / (w * Cc);
  const Rl = Math.max(8 * MU * L / (Math.PI * r ** 4), (L / (Math.PI * r ** 3)) * Math.sqrt(2 * RHO * MU * w)) + RHO * w * w / (2 * Math.PI * C0);
  const k = (8 / (3 * Math.PI)) * KLOSS * RHO / (2 * A * A);
  let lo = 0, hi = P0 / Math.sqrt(Rl * Rl + X * X);
  for (let i = 0; i < 60; i++) { const q = (lo + hi) / 2; if (q * Math.sqrt((Rl + k * q) ** 2 + X * X) > P0) hi = q; else lo = q; }
  const Vin = 2 * lo / w, L0 = Vin / A, x = L0 / L, ld = L / (2 * r), eta = law(x, ld), u = lo / A;
  return { f0: C0 / (2 * Math.PI) * Math.sqrt(A / (Vm * Le)), Vin, Vin_uL: Vin * 1e9, L0mm: L0 * 1e3, x, ld, eta,
           u, Re: u * d / 1e3 / 1.5e-5, kH: eta * Vin * f / Vm, kD: DNO * A / (Vm * Le) };
}
