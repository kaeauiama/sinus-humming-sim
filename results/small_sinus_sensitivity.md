# How robust are the non-maxillary conclusions to their assumed dimensions? (tools/small_sinus_sensitivity.mjs, 2026-11-21)

Page model (two compartments, 130 Pa at the maxillary ostium × ostium pressure ratio, weak harmonics, 150 Hz).
"5 s" = whole-sinus fraction exchanged in 5 s; "diffusion tau" = V·L_e/(D·A).

| sinus, dimensions | L0/L | η | diffusion tau | 5 s hum + diffusion | 5 s diffusion only |
|---|---|---|---|---|---|
| frontal 2.9 mL, d 7.5 / L 4 mm (pages) | 0.03 | 0 % | 34 s | 13 % | 13 % |
| frontal, d 5 / L 10 mm | 0.02 | 0 % | 105 s | 5 % | 5 % |
| frontal, d 4 / L 15 mm | 0.03 | 0 % | 212 s | 2 % | 2 % |
| frontal, d 3 / L 20 mm | 0.03 | 0 % | 463 s | 1 % | 1 % |
| ethmoid cell 0.4 mL, d 1.5 / L 1.5 mm (pages) | 0.31 | 1 % | 31 s | 15 % | 14 % |
| ethmoid 0.4 mL, d 1.0 / L 1.5 mm | 0.70 | 8 % | 60 s | 18 % | 8 % |
| ethmoid 0.8 mL, d 1.5 / L 3 mm | 0.31 | 2 % | 97 s | 7 % | 5 % |
| ethmoid 0.2 mL, d 2.5 / L 1 mm | 0.08 | 0 % | 6 s | 42 % | 42 % |
| sphenoid 4 mL, d 2.2 / L 1.5 mm (pages) | 1.88 | 32 % | 177 s | 42 % | 3 % |
| sphenoid 4 mL, d 3.0 mm | 1.00 | 11 % | 115 s | 21 % | 4 % |
| sphenoid 4 mL, d 1.5 mm | 4.12 | 59 % | 314 s | 54 % | 2 % |
| sphenoid 8 mL, d 2.2 mm | 3.86 | 54 % | 355 s | 54 % | 1 % |
| sphenoid 2 mL, d 2.2 / L 3 mm | 0.47 | 3 % | 128 s | 10 % | 4 % |

- Frontal: humming never ventilates it (its stroke is ~0.1 mm). How fast diffusion does depends on the frontal
  drainage path, which is often a recess 1–2 cm long rather than a short wide opening: from ~30 s to ~8 min.
  The pages' "about 30 s" is the short-wide end.
- Ethmoid cells: humming adds at most ~10 points (narrow 1 mm ostia); diffusion takes 6 s to ~1.5 min.
- Sphenoid: the most variable. Small ostium or large sinus → well ventilated by humming (54 % in 5 s); wide ostium
  or small sinus with a thick wall → little (10–21 %). The same L0/L logic as the maxillary applies (stroke ∝ V/A).
- None of the frontal/ethmoid conclusions depend on the acoustic ostium ratio or the NO calibration.
