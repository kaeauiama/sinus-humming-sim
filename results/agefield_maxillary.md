# Long 3D runs: how fresh air spreads inside the maxillary sinus (2026-11-22)

Engine at commit d8528ea; page assembled with `python build/assemble.py agefield <geometry> test/out/...` from
pages/agefield.template.html and opened from the `dev` server (tools/devserver.py). Analysis:
tools/agefield_pack.py (whole / near / far, model comparison, packing), tools/agefield_spread.py (unevenness),
tools/agefield_budget.py (scalar budget). Raw snapshots are not in git (results/lbm/*/snap_*.u8).

## Fictional maxillary sinus of dist/hum-3d.html (results/lbm/fict_max_040_150hz)

12.75 mL, ostium 2.8 mm × 2.1 mm, middle meatus around it (geometry/build_fict.py, 0.4 mm, 408,786 fluid cells),
Re 300, nasal through-flow 0.12 × the jet peak, 150 Hz and 130 Pa (fundamental only) → target L0/d 1.476. The drive
froze at 0.91–0.92 of the target stroke (L0/d ≈ 1.35) and stayed there up to cycle 2000. 3000 cycles in 469 s.

Fresh-air share of the sinus (near / far half = split by volume at the median distance from the ostium). The
two-compartment model of the pages and a single well-mixed box are run with the 3D run's own starting rate
(0.0654 % of the sinus per cycle, k = 0.098 /s):

| cycle | time at 150 Hz | 3D whole | 3D near half | 3D far half | two-compartment whole (near / far) | one box |
|---|---|---|---|---|---|---|
| 10 | 0.07 s | 0.7 % | 0.9 % | 0.5 % | 0.7 % (1.4 / 0.0) | 0.7 % |
| 50 | 0.33 s | 3.3 % | 2.4 % | 4.2 % | 3.1 % (6.2 / 0.1) | 3.2 % |
| 100 | 0.67 s | 6.5 % | 5.3 % | 7.7 % | 6.2 % (12.1 / 0.2) | 6.3 % |
| 200 | 1.33 s | 12.6 % | 11.4 % | 13.8 % | 11.5 % (22.3 / 0.8) | 12.3 % |
| 400 | 2.67 s | 23.7 % | 22.8 % | 24.6 % | 20.6 % (38.5 / 2.7) | 23.0 % |
| 700 | 4.67 s | 38.1 % | 37.6 % | 38.7 % | 30.9 % (54.9 / 7.0) | 36.7 % |
| 1000 | 6.67 s | 50.6 % | 50.3 % | 50.9 % | 38.7 % (65.3 / 12.1) | 48.0 % |
| 1500 | 10.0 s | 67.5 % | 67.2 % | 67.8 % | 48.2 % (75.3 / 21.1) | 62.5 % |

Unevenness of the fresh air (sd / mean over the sinus cells; mean in five distance bands from the ostium,
0–12 / 12–15 / 15–18 / 18–21 / 21–28 mm):

| cycle | sd / mean | bands (near → far) |
|---|---|---|
| 10 | 4.61 | 1.4 / 0.5 / 0.5 / 0.8 / 0.3 % |
| 25 | 2.43 | 1.6 / 0.9 / 1.8 / 2.4 / 1.7 % |
| 50 | 1.38 | 1.8 / 2.3 / 4.0 / 4.7 / 3.7 % |
| 100 | 0.68 | 4.4 / 5.5 / 7.3 / 8.1 / 7.4 % |
| 200 | 0.31 | 10.5 / 11.5 / 13.2 / 13.9 / 13.8 % |
| 400 | 0.14 | 22.0 / 22.9 / 24.2 / 24.7 / 24.5 % |
| 1000 | 0.05 | 49.7 / 50.5 / 51.1 / 51.1 / 50.6 % |

Mixing efficiency per cycle (removed old air / inflow, relative to the current content): 0.37 for the first 500
cycles (3.3 s), 0.43 at 1000, 0.49 at 1500 (1.34 × the start); 0.59–0.94 later.

### Reading

- In the first 0.1–0.7 s the jet carries fresh air across the sinus: the middle and far bands are fresher than the
  band next to the ostium. After 1.3–2.7 s the sinus is nearly uniform. The air inside this sinus mixes in seconds.
- So the two-compartment structure of the pages (near half, far half mixing on 40 s), which was needed to match the
  in-vivo NO data (results/no_kinetics_2compartment.md), is not what the air does here. Whatever is slow in the NO
  data has to sit somewhere else (for example how NO is produced and stored at the mucosa), or the real sinus differs
  from this smooth fictional one. Open.
- In 10 s the 3D run exchanges 67.5 %, more than a well-mixed box at the starting rate (62.5 %) and much more than
  the two-compartment model with the same rate (48 %).
- dist/hum-3d.html uses the snapshots up to 1500 cycles for the colour pattern only; the amounts on the page still
  come from the calibrated two-compartment model.

### Numerics

- After about 2000 cycles the runs drift: at 0.4 mm the frozen stroke falls to 0.82 of the target by cycle 3000; at
  0.8 mm (results/lbm/fict_max_080_150hz) it jumps to 3.6 × and the mixing efficiency exceeds 1, which is impossible.
  Snapshots after 1500 cycles are not used.
- Whether the rise of the mixing efficiency between 500 and 1500 cycles is physical is not settled. A circulation
  inside the sinus spinning up on the viscous time R²/ν ≈ 12–15 s would do it, and both grids show a similar rise
  by cycle 1500 (1.34 and 1.36 ×). But the coarse grid goes unstable soon after, so a numerical part cannot be
  excluded. A finer grid (0.27 mm) or a conservative scalar scheme would decide it.
- No-flow control (`?ch=0`, 600 cycles, results/lbm/fict_max_040_ch0): the old air in sinus + ostium + nasal cavity
  falls from 12.74 to 11.88 mL (−6.7 %). The inlet cells are held at c = 0 and take up scalar by diffusion
  (estimated at the same order), so this control does not separate numerical loss.

## Real shape: NasalSeg P001 (results/lbm/p001_040_150hz)

Same page and settings on geometry/p001_040 (14.0 mL, ostium 2.8 mm × 2.05 mm, 348,086 fluid cells). Target L0/d
1.630 (x = 2.23); the frozen stroke sat at 1.10 × the target throughout (no drift up to 2000 cycles). 2000 cycles in
295 s. Starting exchange 0.0995 % per cycle (k = 0.149 /s).

| cycle | time | 3D whole | near half | far half | two-compartment whole | one box | sd / mean |
|---|---|---|---|---|---|---|---|
| 10 | 0.07 s | 0.9 % | 1.7 % | 0.0 % | 1.0 % | 1.0 % | 4.87 |
| 50 | 0.33 s | 4.7 % | 5.4 % | 4.1 % | 4.7 % | 4.9 % | 1.46 |
| 100 | 0.67 s | 9.3 % | 8.9 % | 9.6 % | 9.1 % | 9.5 % | 0.84 |
| 200 | 1.33 s | 17.7 % | 17.0 % | 18.3 % | 16.5 % | 18.0 % | 0.40 |
| 400 | 2.67 s | 32.3 % | 31.7 % | 32.9 % | 27.9 % | 32.8 % | 0.18 |
| 1000 | 6.67 s | 62.4 % | 62.1 % | 62.7 % | 47.0 % | 63.0 % | 0.05 |
| 1500 | 10.0 s | 77.0 % | 76.8 % | 77.2 % | 55.7 % | 77.5 % | 0.03 |
| 2000 | 13.3 s | 85.9 % | 85.8 % | 86.1 % | 62.0 % | 86.3 % | 0.01 |

Mixing efficiency per cycle: 0.44–0.47 from start to end (0.97–1.03 × the start), no rise.

### Reading (both shapes)

- In both the smooth fictional sinus and the real P001 sinus the jet reaches deep in the first second and the sinus
  is nearly uniform after about 2–3 s. The exchange then follows a single well-mixed box at the rate given by the
  early-cycle mixing efficiency (P001: 77.0 % vs 77.5 % at 10 s).
- The rise of the mixing efficiency seen in the fictional shape does not appear in P001, so it is not general (it is
  either specific to the smooth shape or numerical; see Numerics above).
- The two-compartment model of the pages underestimates the 3D exchange by 15–20 points at 10 s (P001: 55.7 % vs
  77.0 %) when run at the same rate. Its slow far half is not supported by the air flow.

## Rerun with the anatomical nasal cavity (results/lbm/fict_max_040_150hz_v2, engine d8528ea, shapes f3cfaee)

The nasal cavity of the page was redrawn (narrow airway, turbinates on laminae, ethmoid bulla); geometry/build_fict.py
uses the same shape, the sinus moved to x = 26.97 mm to keep the 2.1 mm ostium, nasal crop 9.5 mL, 348,136 fluid
cells, 1600 cycles in 213 s, stroke 0.93 × target throughout. The sinus interior hardly changed: 68.2 % exchanged at
10 s (first run 67.5 %), sd/mean 0.13 at 400 cycles and 0.04 at 1000, the mixing efficiency again rising to 1.42 × by
cycle 1500. dist/hum-3d.html now uses this run.
