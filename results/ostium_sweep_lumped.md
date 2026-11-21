# Ostium diameter sweep, lumped model (tools/ostium_sweep.mjs). Maxillary 14 mL, L = 2.1 mm, 150 Hz, 100 Pa.

Updated 2026-11-21 to the refit mixing law (results/deadspace_law_fit.md); the old soft-law values are kept for comparison.
With the long-tube factor (commit eafe134) the "new" columns move by ≤ 0.01 in η: humming tau 13.0 / 6.6 / 6.2 / 7.3 /
15.4 / 64 / 183 / 978 s for d = 0.8 / 1.2 / 1.6 / 2.0 / 2.8 / 4.0 / 5.0 / 7.0 mm (table below is the eee38fa run).

| d (mm) | stroke L0 | L0/L | L/d | peak u | Re | eta (new) | eta (old) | humming tau (new) | humming tau (old) | diffusion tau |
|---|---|---|---|---|---|---|---|---|---|---|
| 7.0 | 0.5 mm | 0.25 | 0.30 | 0.3 m/s | 117 | 0 % | 2 % | 1017 s | 269 s | 146 s |
| 5.0 | 1.1 mm | 0.50 | 0.42 | 0.5 m/s | 166 | 2 % | 5 % | 188 s | 82 s | 226 s |
| 4.0 | 1.7 mm | 0.80 | 0.53 | 0.8 m/s | 210 | 7 % | 12 % | 65 s | 39 s | 306 s |
| 2.8 (P001) | 3.5 mm | 1.67 | 0.75 | 1.7 m/s | 309 | 28 % | 33 % | 15 s | 13 s | 509 s |
| 2.0 | 7.2 mm | 3.45 | 1.05 | 3.4 m/s | 455 | 56 % | 56 % | 7.3 s | 7.4 s | 847 s |
| 1.6 | 11.7 mm | 5.6 | 1.31 | 5.5 m/s | 588 | 63 % | 59 % | 6.3 s | 6.7 s | 1205 s |
| 1.2 | 18.8 mm | 8.9 | 1.75 | 8.9 m/s | 708 | 66 % | 59 % | 6.7 s | 7.4 s | 1931 s |
| 0.8 | 21.8 mm | 10.4 | 2.63 | 10 m/s | 548 | 67 % | 59 % | 12.8 s | 14.4 s | 3871 s |

- Volume per cycle ≈ V·P0/(γ p_atm) ≈ 0.02 mL, nearly independent of d (well below resonance), so stroke ∝ 1/d².
  Below 1.2 mm the jet loss and viscosity cut the volume itself (11 µL at 0.8 mm).
- Best for humming stays at 1.2–1.6 mm (tau ≈ 6.3–6.7 s). The new law makes wide ostia much worse:
  at 4–5 mm the stroke is shorter than one diameter, and humming adds little to diffusion (5 mm: 188 s vs 226 s).
- Caveats: the law was measured for L0/L ≤ 4 and Re = 300; the 0.8–1.6 mm rows (L0/L 5.6–10, Re 550–710) are on its
  saturated plateau by extrapolation.
- Impedance at 2.8 mm: compliance ≈ 100 %, jet loss ≈ 2 %, oscillatory wall friction ≈ 0.5 %; Stokes layer 0.19 mm, Womersley ≈ 11.
