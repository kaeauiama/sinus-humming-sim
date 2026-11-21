# Population × humming strategy, lumped model (tools/population_pitch.py)

4000 sampled geometries per sinus, 10 s of humming. Numbers are medians of the fraction of sinus air exchanged.

## Current (2026-11-21, same model as the pages): two compartments, 130 Pa at the maxillary ostium, ostium ratios

| strategy (10 s) | maxillary, no harmonics | maxillary, −12 dB/oct | sphenoid, no harmonics | sphenoid, −12 dB/oct | sphenoid without ostium ratio, −12 dB/oct |
|---|---|---|---|---|---|
| 120 Hz | 33 % | 38 % | 43 % | 44 % | 25 % |
| 150 Hz | 39 % | 46 % | 47 % | 50 % | 31 % |
| 200 Hz | 49 % | 56 % | 53 % | 57 % | 41 % |
| 300 Hz | 61 % | 64 % | 63 % | 65 % | 56 % |

- The whole-sinus exchange in 10 s is capped near two thirds: the near-ostium half empties within seconds, the far
  half follows on the 40-s mixing time. Pitch still helps, but less than in the one-box model.
- The sphenoid ostium sits ~1.4× higher in pressure than the maxillary one (results/ostium_pressure.md), so the
  sphenoid is ventilated as well as the maxillary. Frontal and ethmoid: ≈ 0–12 % (diffusion does it).
- `TWO=0`, `OSTP=0`, `P0=...`, `VOL=normal`, `LAW=2d` switch back to the earlier variants below.

## Earlier: one box, NasalSeg volumes, 200 Pa (the 200 Pa calibration of the one-compartment NO model)

## Current (2026-11-21): NasalSeg volumes, refit mixing law, calibrated 200 Pa

Maxillary volumes are drawn from the 259 maxillary sinuses of the 130 NasalSeg cases
(results/nasalseg_maxillary_volumes.csv: mean 13.1 mL, SD 6.6, median 12.9, 10–90 % 4.0–21.7, max 39.5; the earlier
assumption was normal 12.75 ± 4.38 mL, so the real spread is 1.5× wider). Ostium d and L are still the assumed ranges.

Resonance f0: maxillary median 567 Hz (10–90 %: 378–966 Hz), only 2.9 % inside 100–300 Hz; this range matches the
measured sinus resonances of Dang & Honda (about 310–1000 Hz). Sphenoid 886 Hz, frontal and ethmoid ~2.1 kHz.

| strategy (maxillary, 10 s) | 200 Pa, no harmonics | 200 Pa, −12 dB/oct (page default) | 100 Pa, no harmonics |
|---|---|---|---|
| 120 Hz | 73 % | 81 % | 21 % |
| 150 Hz | 82 % | 91 % | 27 % |
| 200 Hz | 92 % | 98 % | 40 % |
| 300 Hz | 99 % | 100 % | 72 % |
| sweep 100–200 Hz | 83 % | 92 % | 28 % |

Sphenoid at 200 Pa, −12 dB/oct: 150 Hz 74 %, 300 Hz 99 %. Frontal 0 %, ethmoid 5–12 % (diffusion does their job).

- With the calibrated pressure, one 10-s hum at an ordinary pitch exchanges most of the maxillary air in most people;
  pitch matters most at low pressure (quiet humming) and in sinuses with small strokes.
- Higher pitch is still better below resonance; harmonics add a lot at 100 Pa and less once the sinus is nearly
  emptied anyway.
- Using the NasalSeg volumes instead of the normal assumption changes the medians by ≤ 1 point at 100 Pa.

## First runs (for the record)

| strategy (maxillary, 10 s, 100 Pa) | old 2D law, normal volumes (first run) | refit law, normal volumes |
|---|---|---|
| 120 Hz | 40 % | 21 % |
| 150 Hz | 50 % | 27 % |
| 200 Hz | 65 % | 39 % |
| 300 Hz | 89 % | 70 % |
| sweep 100–200 Hz | 51 % | 28 % |
| 150 Hz + harmonics n^−2 | 50 % | 35 % |
| 150 Hz + harmonics n^−1 | 98 % | 89 % |

The first run used the 2D law 0.70·max(0, 1 − 0.60 L/L0), more generous than any 3D fit.
