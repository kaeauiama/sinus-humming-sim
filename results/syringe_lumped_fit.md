# Lumped-model fit to the syringe experiment (tools/syringe_fit.mjs, 2026-11-21)

> Superseded the same day by syringe_fig6_fit.md: the full text shows the output ratios used here disagree with the
> paper's direct exchange measurement (Fig. 6), which is now the target. Kept for the record.

Model: lumped Helmholtz (V=15 mL) + soft mixing law; free parameters nozzle length L (1–30 mm),
pressure amplitude P0 (10–2000 Pa), humming duration t (5/10/30 s). Output ∝ 1 − exp(−k_H t).

- Frequency response alone fits perfectly: L ≈ 7 mm, P0 ≈ 220 Pa, t = 5 s gives 0.78 : 1 : 0.48 for 120/200/450 Hz
  (experiment 230/295/143 → 0.78 : 1 : 0.48). f0 at d = 1.9 mm ≈ 260 Hz. => the "ostium" was a ~1 cm tube, not a 2 mm wall.
- Diameter trend cannot be fitted by any single (L, P0, t). Experiment 1 : 4.5 : 6 : 14 : 30 (0.8 → 4.0 mm).
  Best size-only fit (L = 30 mm, P0 ≈ 630 Pa) gives 1 : 5 : 9 : 9.5 : 4, and the frequency fit then fails.
- Even giving the 4.0 mm opening its own short length (1–2 mm) the ratio tops out at ~2.5–3.5 because the model's
  0.8 mm tube already exchanges ~30 % in 5 s; the experiment needs it at ≲ 3 % of the 4.0 mm one.
- Suspect: the soft mixing law is being used far outside its validated range: there L/d = 5–15, L0/d = 30–60,
  Re = 1000–4700 (validated: L/d ≤ 3, L0/d ≲ 12, Re = 300). Next step = 3D test of long thin tubes (docs/roadmap.md).
