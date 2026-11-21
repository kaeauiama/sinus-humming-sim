# Dead-space law refit on the corrected engine (roadmap 1 and 2, 2026-11-21)

## Adopted law (after roadmap 2, commit eafe134; pages and tools use this)

η = 0.695 · (1 − e^−(x/1.68)^1.76) · (1 − e^−(j/1.15)^0.57) · e^−(L/d)/48, x = L0/L, j = L0/d.
22 points (L/d 0.5–20 at DC 10, Re 300), rms 1.7 points. `node tools/fit_deadspace_law.mjs`, form (e).

Long tubes (roadmap 2, dist/verify-rounding.html at 4b1da7d, after the drive-slab fix):

| L/d | DC | Re | x | η 3D | (d) from L/d ≤ 3 | (e) adopted |
|---|---|---|---|---|---|---|
| 10 | 10 | 300 | 0.49 / 1.02 / 1.90 | 7 / 19 / 37 | 6 / 21 / 47 | 6 / 19 / 40 |
| 20 | 10 | 300 | 0.48 / 1.06 / 1.92 | 6 / 16 / 34 | 6 / 23 / 48 | 5 / 16 / 33 |
| 10 | 14 | 300 | 1.91 | 39 | 47 | 40 |
| 10 | 14 | 1000 | 1.07 / 1.93 | 23 / 38 | 22 / 48 | 19 / 40 |

- Up to L0/L ≈ 1 the L/d ≤ 3 law extrapolates well to long tubes (within 2–7 points). At L0/L ≈ 2 long tubes mix
  clearly less: η at x ≈ 2 is 33 / 35 / 42 / 45 / 37 / 34 % for L/d 0.5 / 0.8 / 1.5 / 3 / 10 / 20, i.e. it peaks
  around L/d ≈ 3. The factor e^−(L/d)/48 captures the decline (−19 % at L/d 10, −34 % at L/d 20 relative to the
  same law without it). Physically plausible as the flow in a long tube is fully developed (parabolic) and the
  jet it sheds is weaker, but not examined further.
- Resolution: DC 14 at L/d 10, x ≈ 1.9 gives 39 % vs 37 % at DC 10.
- Reynolds number: Re 1000 vs 300 changes η by +4 points at x ≈ 1 and ≈ 0 at x ≈ 2. Small.
- For sinus ostia (L/d ≤ 1) (e) differs from (d) by less than 1 point.
- Validity: L/d 0.5–20, x 0.5–4 (only up to 2 beyond L/d 3), Re 300 (spot checks at 1000), sharp-edged
  cylinder into a sphere. Below L/d 0.5 or above 20 it is an extrapolation.

## Roadmap 1 record (L/d ≤ 3; superseded by the section above)

Data: results/deadspace_law_3d.csv (16 points at DC = 10, Re = 300, sharp edge, L/d = 0.5 / 0.8 / 1.5 / 3 ×
L0/L ≈ 0.5 / 1 / 2 / 4; dist/verify-rounding.html at commit 604b950; DC = 14 checks at L0/L ≈ 1 agree to the point).
Fit: tools/fit_deadspace_law.mjs (Nelder–Mead on rms). x = L0/L (dead space), j = L0/d = x·L/d (stroke in diameters).

| fit | form | parameters | rms (points) |
|---|---|---|---|
| old soft law | 0.59 (1 − e^−(x/1.89)^1.76) | fitted at DC 8 on the buggy engine | 4.8 |
| (a) one curve | m (1 − e^−(x/x0)^n) | 0.583, 1.90, 2.15 | 4.3 |
| (c) plateau by L/d | m∞(1 − e^−(L/d)/λ) (1 − e^−(x/x0)^n) | 0.649, 0.365, 1.92, 2.04 | 2.2 |
| **(d) dead space × stroke** | **m (1 − e^−(x/x0)^n) (1 − e^−(j/k)^p)** | **m 0.670, x0 1.69, n 1.87, k 1.00, p 0.51** | **1.7** |

| L/d | x | L0/d | η 3D | old | (d) |
|---|---|---|---|---|---|
| 0.5 | 0.50 / 1.03 / 2.03 / 4.09 | 0.25 / 0.52 / 1.0 / 2.0 | 4 / 7 / 33 / 51 | 5 / 17 / 40 / 58 | 3 / 11 / 32 / 51 |
| 0.8 | 0.52 / 1.03 / 1.83 / 4.17 | 0.42 / 0.82 / 1.5 / 3.3 | 5 / 11 / 35 / 55 | 6 / 17 / 36 / 58 | 3 / 13 / 32 / 56 |
| 1.5 | 0.51 / 0.98 / 2.05 / 3.92 | 0.77 / 1.5 / 3.1 / 5.9 | 4 / 16 / 42 / 61 | 6 / 16 / 40 / 57 | 4 / 14 / 42 / 61 |
| 3.0 | 0.55 / 0.94 / 2.04 / 3.69 | 1.7 / 2.8 / 6.1 / 11 | 5 / 17 / 45 / 65 | 6 / 15 / 40 / 57 | 6 / 16 / 47 / 64 |

Findings
- L0/L is still the main variable, but not the only one. At the same L0/L, a short ostium mixes less:
  at x ≈ 4, η = 51 / 55 / 61 / 65 % for L/d = 0.5 / 0.8 / 1.5 / 3; at x ≈ 1, 7 / 11 / 16 / 17 %.
  The old claim "one curve for all L/d" is wrong; it was hidden by the narrower range (0.75–3) and the old errors.
- A second variable, the stroke in diameters L0/d, captures it: (d) has k ≈ 1.0, i.e. the extra loss sets in when
  the air column is shorter than about one ostium diameter. That is the order where an oscillating jet stops
  shedding vortex rings that escape the opening (synthetic-jet formation). The factor is gradual (p ≈ 0.5), not a
  sharp threshold. (c) (plateau depending on L/d) fits almost as well (2.2 points) with one parameter fewer.
- Largest misses of (d): x ≈ 1 at short L/d (L/d 0.5: 7 vs 11 %, 0.8: 11 vs 13 %).
- Long tubes: (c) saturates by L/d ≈ 1.5, (d) keeps rising with L0/d (x = 1: 17 % at L/d 3, 20 % at L/d 10).
  Neither is tested beyond L/d = 3: roadmap 2 decides, and it matters for the syringe tips (L/d 10–30).

Impact on the lumped model at 100 Pa, η old → (d):
- maxillary P001 (L/d 0.75, x 1.67 at 150 Hz): 32.7 → 28.3 % (×0.87); 250 Hz 38.4 → 34.2 %
- sphenoid (L/d 0.68, x 1.03): 17.2 → 12.4 % (×0.72)
- ethmoid (x 0.22): 1.3 → 0.5 %; frontal (x ≈ 0.02) ≈ 0. Both ventilate by diffusion anyway.
The pages and tools still use the old law.

P001 (E2, real geometry, 0.4 mm grid) against (d): 2.0 mm 56 vs 56 %, 2.8 mm 36 vs 29 %, 4.0 mm 16 vs 7 %.
4.0 mm has 10 cells across and L/d = 0.53 is inside the measured range, so the gap is neither resolution nor
extrapolation: the CT geometry mixes more than the ideal one at small L0/L. A likely reason is that the carved
cylinder meets the irregular sinus and nasal walls, so the effective ostium is shorter than the nominal 2.1 mm.
