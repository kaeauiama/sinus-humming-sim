# Numerical floor and grid resolution (dist/verify-rounding.html, commit 47686d7, 2026-11-21)

Run in the desktop app's built-in browser (NVIDIA Ampere, localhost). Idealized geometry of experiment 1:
sphere cavity (Rc = 3.2d) + sharp-edged cylindrical ostium, L = 0.8d, nasal channel, Re = 300, cross-flow 0.12·UPEAK.
The engine is the same as for results/rounding_e1.csv; 47686d7 only adds the control mode to the page.

## 1. No drive (`?autoC`, DC = 10)

Drive amplitude held at 0, same period T as the driven run at that L0/L. "Lost" = what the sinus loses per period,
divided by the inflow a driven run would have (L0·A), i.e. in the units of eta. Cycles 5–10.

| period of | T (steps) | lost per period | per cycle | diffusion-only estimate |
|---|---|---|---|---|
| L0/L = 1 | 314 | 0.8 % | 0.8 0.8 0.8 0.9 0.8 0.9 | 0.8 % |
| L0/L = 2 | 628 | 0.9 % | 0.9 0.9 0.9 0.9 0.9 0.9 | 0.8 % |
| L0/L = 4 | 1257 | 0.8 % | 0.9 0.9 0.8 0.8 0.8 0.8 | 0.8 % |

Diffusion-only estimate: D·T / ((L + (π/2)·r)·L0) with D = ν/0.8 (the engine's scalar diffusivity); it equals
π·d/(0.8·Re·(L + 1.57r)) and does not depend on L0/L. At rest the measured loss is the physical diffusion and nothing
else: no numerical leak of the non-conservative scalar scheme, no extra exchange from the cross-flow.
(Coarse check at DC = 4: 0.6–0.9 % vs estimate 0.9–1.4 %.)

## 2. Grid resolution, driven (`?autoE1&rfs=0&xs=...&dc=...`)

| DC (cells across d) | L0/L target | achieved | eta 3D | soft law at achieved |
|---|---|---|---|---|
| 7 | 1 | 0.99 | **20 %** | 16 % |
| 10 | 1 | 1.03 | **11 %** | 17 % |
| 14 | 1 | 1.07 | **11 %** | 18 % |
| 7 | 2 | 2.10 | 38 % | 41 % |
| 10 | 2 | 1.83 | 35 % | 36 % |
| 7 | 4 | 3.89 | 52 % | 57 % |
| 10 | 4 | 4.17 | 55 % | 58 % |

(DC = 10 rows from rounding_e1.csv; Lc = round(0.8·DC) gives L/d = 0.86 / 0.80 / 0.79.)

- At L0/L = 1, eta is converged from DC = 10 on (11 % at 10 and 14). DC = 7 nearly doubles it (20 %).
  The 3D value below the soft law at L0/L = 1 (11 vs 17–18 %) is therefore real, not a resolution artefact.
- At L0/L = 2 and 4, DC = 7 is within 3 points of DC = 10.
- Consequences: the soft law was fitted with DC = 8 (pages/dlaw.template.html) on the engine with the amplitude
  bug, so its low-L0/L end was probably inflated by both. Re-fit (roadmap 1) and the long-tube runs (roadmap 2) need
  DC ≥ 10. The P001 runs have the ostium on few cells (E2 on the 0.4 mm grid: 2.0 / 2.8 / 4.0 mm = 5 / 7 / 10 cells;
  the integrated result quoted in findings, 31 % vs 34 %, was on the 0.8 mm grid: 2.8 mm = 3.5 cells), so their
  values near L0/L ≈ 1 may be too high.
