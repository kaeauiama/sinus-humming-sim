# NO kinetics: calibration against in-vivo humming data (tools/no_calibrate.mjs, 2026-11-21)

## Targets (healthy adults)

| source | quantity | value |
|---|---|---|
| Menzel et al. 2005, J Appl Physiol 98:2064–2071 (n = 8, laser magnetic resonance spectroscopy, abstract) | washout time constant of nasal NO during humming (after the peak) | 3.0 ± 1.2 s |
| same | recovery (refill) time constant of sinus NO between hums | 4.5 ± 3.2 min |
| Maniscalco et al. 2003, Eur Respir J 22:323 (n = 10, 0.2 L/s, mean of last 8 s) | first hum ÷ quiet | 4.7× (Shusterman 2007: 4.2×) |
| same | 5 hums at 5-s intervals | progressive fall to a plateau at 26 % of the first within four hums |
| same | quiet exhalation right after the hums | 32 % lower (range 5–50 %) |
| same | hums at 3-min intervals | alike (< 15 % variability): "complete recovery" |
| same | topical L-NAME | quiet nasal NO −50 %, humming increase unchanged → mucosal share ≥ 50 % |

## Model and free parameters

The pages' NO model (tools/no_model.mjs). Free: effective sound pressure P0, refill time constant tauRec,
mucosal share of quiet nasal NO, phi = NO production of the small sinuses (frontal, ethmoid) relative to the per-area
rule, harmonics none or −12 dB/oct. Cost = sum of squared z-scores of the five targets + the Menzel prior on tauRec.
Grid: 2 × 7 × 6 × 4 × 5 = 1680 runs.

## Result

| setting | ratio (mean) | washout | 5th/1st | post-quiet drop | 3-min recovery | cost |
|---|---|---|---|---|---|---|
| pages until now: 100 Pa, tau 270 s, mucosa 70 %, phi 1 | 3.1× | 5.5 s | 42 % | 11 % | 85 % | — |
| best: 250 Pa, no harmonics, tau 120 s, mucosa 50 %, phi 1 | 4.8× | 3.0 s | 33 % | 19 % | 87 % | 2.6 |
| 200 Pa, −12 dB/oct, tau 120 s, mucosa 50 %, phi 1 | 4.6× | 2.7 s | 33 % | 17 % | 87 % | 2.8 |
| 250 Pa, no harmonics, tau 180 s, mucosa 60 % | 4.6× | 3.0 s | 29 % | 18 % | 77 % | 2.8 |

With the page protocol the calibrated sets give a first PEAK of 19–20× (mean 4.6–4.8×), the same order as the 15× of
Weitzberg & Lundberg 2002. So the 15× was most likely a peak, and one parameter set now covers 15× (peak), 4.7× (mean),
the 3-s washout and the 3-min recovery.

What pins what (one at a time around the best):
- **P0 is fixed by the washout**, which depends almost only on the hum ventilation rate: 5.5 s at 100 Pa, 4.3 s at
  160, 3.6 s at 200, 3.0 s at 250 Pa (no harmonics; −12 dB/oct harmonics lower the needed pressure to ~200 Pa).
  The 3D maxillary mixing of P001 is ~20 % above the ideal-geometry law, which would lower it a little more.
- **tauRec trades ratio against recovery**: 60 s → 4.0×, 98 %; 120 s → 4.8×, 87 %; 270 s → 6.4×, 64 %. About 2 min
  satisfies both studies and lies inside Menzel's 4.5 ± 3.2 min.
- **Mucosal share and phi are degenerate**: mucosa 50 % with phi 1 fits as well as mucosa 80 % with phi 0.1. The data
  only fix how much of the quiet sinus NO comes from sinuses that humming empties.
- Remaining misses: the plateau comes too early and too high (model 33 % by the 2nd hum; measured 26 % reached
  gradually within four), and the post-hum quiet drop is low (17–19 % vs 32 %, but inside the measured 5–50 %).

## Reading

- The in-vivo NO dynamics need about twice the hum ventilation the pages assumed: an effective nasal sound pressure of
  ~200 Pa with realistic harmonics (−12 dB/oct), or ~250 Pa without. "Effective" because it also absorbs the model's
  other approximations (mixing law from the ideal geometry, one-compartment sinuses). No one has measured the pressure.
- With that, maxillary humming ventilation is much faster than on the pages: one 10-s hum empties ~95 % (washout 3 s).
- The refill time constant is ~2 min rather than 4.5 min; the "known weakness" (3-min recovery 66–74 %) goes away.
