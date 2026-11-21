// Ostium diameter sweep of the lumped model: maxillary 14 mL, L = 2.1 mm, 150 Hz, 100 Pa.
// Run: node tools/ostium_sweep.mjs   (results/ostium_sweep_lumped.md)
import { lumped, mixOld } from './model.mjs';
console.log('d(mm)  f0   Vin(uL)  L0(mm)  x     L/d   u(m/s)  Re    eta   eta_old  tauH(s)  tauH_old(s)  tauD(s)');
for (const d of [0.8, 1.2, 1.6, 2, 2.8, 4, 5, 7]) {
  const r = lumped(14, d, 2.1, 150, 100), o = lumped(14, d, 2.1, 150, 100, mixOld);
  console.log([d.toFixed(1).padStart(4), r.f0.toFixed(0).padStart(5), r.Vin_uL.toFixed(1).padStart(8), r.L0mm.toFixed(2).padStart(7),
    r.x.toFixed(2).padStart(5), r.ld.toFixed(2).padStart(5), r.u.toFixed(2).padStart(7), r.Re.toFixed(0).padStart(5),
    r.eta.toFixed(2).padStart(5), o.eta.toFixed(2).padStart(8), (1 / r.kH).toFixed(1).padStart(8), (1 / o.kH).toFixed(1).padStart(12),
    (1 / r.kD).toFixed(0).padStart(8)].join(' '));
}
