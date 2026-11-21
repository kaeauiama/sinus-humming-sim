# NO model rebuilt: one well-mixed sinus air + a mucosal store (2026-11-22, `node tools/no_calibrate3.mjs [fine]`)

## Why

The pages' two-compartment sinus (a near half flushed by humming, a far half mixing with it on 40 s) was needed to
match Maniscalco 2003 Fig. 3 (results/no_kinetics_2compartment.md). The long 3D runs show that the sinus air mixes
within 2–3 s (results/agefield_maxillary.md), and the mucosa cannot hold a physical NO reserve (results/no_wall_source.md).
So the slow part goes to the mucosal side: a store that exchanges NO with the air.

## Model (tools/no_model.mjs, `o.store`)

- Sinus air: one box, exchanged at k = k_D + k_H (diffusion + humming, the same resonance model and mixing law).
- Store at the mucosa: capacity σ × the air volume, exchanging with the air on τ_ex; both scaled with the
  sinus's area/volume relative to the maxillary sinus (small sinuses carry more store per volume of air).
- All production goes into the store; the store loses NO on τ_rec (uptake into the blood). Whether this is a chemical
  store or production that rises when the air NO falls cannot be told apart: the equations are the same.
- Quiet maxillary air at 8000 ppb; nasal mucosal share of quiet nasal NO as before.

## Fit

Same targets and cost as no_calibrate2 (Maniscalco Fig. 3 sequence 49/40/27 % and tail 0.34, mean ratio 4.2–4.7×,
Menzel washout 3.0 ± 1.2 s, quiet drop 32 % (5–50), 3-min recovery ~complete, Menzel refill prior on the slowest time
constant, mucosal share ≥ 50 %). Weak harmonics (−12 dB/oct), 150 Hz. Coarse grid 2160 runs, fine grid 2700.

| model | P0 | other | ratio (peak) | hums 2/3/5 | tail | washout | quiet drop | 3-min | cost | maxillary air exchanged in 10 s |
|---|---|---|---|---|---|---|---|---|---|---|
| target | | | 4.2–4.7× (15×) | 49/40/27 % | 0.34 | 3.0 s | 32 % | ~100 % | | |
| one box, no store | 200 | τ 120 s, mucosa 50 % | 4.5× (22×) | 36/34/34 % | 0.17 | 2.6 s | 18 % | 87 % | 6.6 | — |
| two air compartments (pages 2026-11-21) | 130 | fn 0.5, 40 s, τ 270 s, mucosa 50 % | 4.6× (14×) | 55/42/32 % | 0.34 | 2.8 s | 21 % | 80 % | 2.5 | 56 % (two compartments) |
| store, best | 180 | σ 0.6, τ_ex 16 s, τ_rec 90 s, mucosa 70 % | 4.5× (13×) | 49/37/32 % | 0.36 | 2.9 s | 11 % | 81 % | 3.5 | 95 % |
| **store, pages since 2026-11-22** | **180** | **σ 0.6, τ_ex 24 s, τ_rec 120 s, mucosa 70 %** | **4.5× (14×)** | **49/37/31 %** | **0.32** | **2.9 s** | **11 %** | **78 %** | **3.6** | **95 %** |

- The optimum is broad: P0 160–200 Pa, σ 0.45–0.8, τ_ex 12–32 s, τ_rec 90–150 s (slowest time constant 190–250 s),
  mucosal share 70 %. The page set sits inside it with a slowest time constant of 234 s (Menzel 4.5 ± 3.2 min).
- Measured Menzel's way (peak of a hum vs the rest before it), the apparent recovery is 2.8 min (tools/no_recovery.mjs).
- The NO data alone fit the store model about as well as the two air compartments (cost 3.6 vs 2.5; both inside the
  measured spreads except the quiet drop, 11 % vs 32 % with range 5–50 %). The 3D runs decide between them.
- Consequence for the ventilation: Menzel's 3-s washout now means the whole sinus air is flushed with a time constant
  of about 3 s, so a 10-s hum at 150 Hz replaces ~95 % of the maxillary air (pages before: 56 %). The NO keeps coming
  for longer because the store keeps feeding the air.
- The effective pressure goes back up to 180 Pa (two compartments: 130 Pa), because humming now has to flush the whole
  sinus, not half of it.
