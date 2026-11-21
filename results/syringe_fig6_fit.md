# Lumped-model fit to Fig. 6 of the syringe experiment (tools/syringe_fig6_fit.mjs, 2026-11-21)

Target changed: the earlier fit (syringe_lumped_fit.md) used the printed NO-output ratios 1 : 4.5 : 6 : 14 : 30.
The full text (checked 2026-11-21, results/syringe_experiment.json) also has Fig. 6: the fraction of syringe gas
gone after ONE 10-s human hum, measured from syringe NO before/after. This is the direct measure of exchange, and it
does not agree with the output ratios (nor with the absolute outputs, by ~3.5x), so it is used here.

| tip d (mm) | 0.8 | 1.29 | 1.9 | 2.1 | 4.0 |
|---|---|---|---|---|---|
| Fig. 6, exchanged in 10 s (%) | 6 | 50 | 75 | 81 | 97 |

Model: lumped Helmholtz (V = 15 mL) + soft mixing law, t = 10 s, human hum at 150 Hz (also 130 Hz). Free: tip length(s), P0.

- (0) The paper's own resonance calculation (200 Hz for 15 mL / 1.9 mm) needs L ≈ 13 mm in this model.
- (A) One length for all five tips: best rms 8.6 points, and only at the edge of the grid (L = 80 mm, P0 ≈ 2000 Pa). Not plausible.
- (B) Each tip its own length, common P0: at P0 = 250 Pa the 0.8 / 1.29 / 1.9 / 2.1 mm tips need 24 / 22 / 30 / 32 mm.
  The thin tips do NOT need to be longer, contrary to the "needle vs Luer tip" hypothesis raised in the review.
  The 4.0 mm opening must be short.
- (C) Two lengths (the four tips 0.8–2.1 mm share L, the 4.0 mm opening has its own L4), 3 parameters for 5 points:

| hum | L (mm) | L4 (mm) | P0 (Pa) | model (%) | rms |
|---|---|---|---|---|---|
| 130 Hz | 23.5 (22–26) | ≤ 1 | 214 (195–234) | 6 / 49 / 85 / 78 / 91 | 5.6 |
| 150 Hz | 18 (17–20) | ≤ 1 | 170 (155–191) | 7 / 48 / 85 / 79 / 89 | 5.8 |

  (ranges: rms within 1 point of the best). The steep step 0.8 → 1.29 mm (6 → 49 %) is reproduced. It comes from
  dead space: L0/L crosses about 1 between these two tips (0.7–0.8 → 1.2), where the soft law is steep (η ∝ x^1.76).
  Regime of the thin tips: L/d = 9–30, L0/L = 0.7–1.4, L0/d = 10–22, Re = 340–1600. The soft law was fitted at
  L/d ≤ 3, Re = 300, and the corrected engine already falls below it at L0/L = 1 (11 % vs 17 %, rounding_e1.csv).
  Misses: 1.9 mm too high (85 vs 75, its f0 ≈ 150–170 Hz sits on the hum), 4.0 mm too low (≈ 90 vs 97, inflow-limited).

- Conflict with the frequency data: with the (C) parameters the 1.9 mm tip gives ≈ 0–1 % at 450 Hz (far above its
  ≈ 150–170 Hz resonance, so the inflow is tiny and L0/L ≈ 0.1). The paper reports 450 Hz still giving 143 nL/min,
  about 80 % of the 150 Hz output (human) and 50 % of the 200 Hz output (duck call). No single tip length in this
  model satisfies both Fig. 6 and the 450 Hz data; something the lumped model leaves out (e.g. the syringe plunger's
  own compliance and mass, the cylinder's acoustics, the 0.2 L/s cross-flow over the tip) or a different sound
  amplitude at 450 Hz would be needed.

Conclusion: the mixing law does not have to fail at large L0/L (the old roadmap 2 hypothesis) to explain the size
dependence. What matters is the law at L0/L ≈ 0.5–1.5 in LONG tubes (L/d ≈ 10–30), which is untested in 3D.

## Update: refit mixing law (same day, `node tools/syringe_fig6_fit.mjs`; the numbers above are `LAW=old`)

| hum | (C) best L (mm) | L4 (mm) | P0 (Pa) | model (%) | rms |
|---|---|---|---|---|---|
| 130 Hz | 25.5 (23–30) | ≤ 2 | 214 (191–263) | 6 / 48 / 90 / 85 / 82 | 9.8 |
| 150 Hz | 80 (grid edge) | — | 1778 | 7 / 35 / 82 / 92 / 100 | 9.0 |

- The fit gets worse (rms 6 → 9–10 points). The thin end is still reproduced (6 / 48 % at 130 Hz), but the wide
  4.0 mm opening now tops out near 82 %: with a sub-millimetre opening its stroke (≈ 3.7 mm) is shorter than its
  diameter, so the new stroke factor (L0/d) cuts its mixing to η ≈ 0.42.
- Both ends lean on the law outside its measured range: the thin tips at L/d 12–32 and the 4.0 mm opening at
  L/d ≈ 0.1 (measured: 0.5–3). The data themselves are good to about 10 points (syringe_experiment.json).
  So this does not decide anything; roadmap 2 (long tubes) and a check at L/d < 0.5 would.

## Update 2: law with the long-tube factor, measured up to L/d = 20 (commit eafe134)

| hum | (C) best L (mm) | L4 (mm) | P0 (Pa) | model (%) | rms |
|---|---|---|---|---|---|
| 130 Hz | 24.5 (22–28) | ≤ 2 | 229 (204–275) | 5 / 46 / 88 / 84 / 84 | 8.7 |
| 150 Hz | 20 (18–25) | ≤ 2 | 200 (170–275) | 6 / 46 / 91 / 90 / 83 | 10.2 |

- The thin tips now sit inside the measured range of the law (L/d 10–31, x 0.7–1.4; measured up to L/d 20 and
  x 2). The steep step 0.8 → 1.29 mm (6 → 50 % in Fig. 6, 5 → 46 % here) is reproduced by dead space in ~2 cm
  tips: x goes 0.69 → 1.17 between these two tips, and the law gives η ≈ 0.07 → 0.19 there (3D in long tubes:
  6–7 % at x ≈ 0.5, 16–19 % at x ≈ 1).
  So the size dependence does NOT need the law to break down; roadmap 2 answers its own question.
- What still misses: 1.9 / 2.1 mm come out 7–16 points high (their resonance sits on the hum, 150–180 Hz), and the
  4.0 mm opening tops out at 83–84 % (L/d ≈ 0.1, below the measured 0.5; stroke ≈ one diameter). With data good to
  about 10 points these are at the edge of meaningful.
- Unchanged conflict: with these lengths the 1.9 mm tip barely exchanges at 450 Hz (0–1 %), while the paper reports
  450 Hz at about 80 % of the 150 Hz output.

