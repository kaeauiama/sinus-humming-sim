# Pitch x sound pressure (2026-11-22, `node tools/pitch_loudness.mjs`, engine-independent)

Page defaults (two compartments, weak harmonics n^-2, per-ostium pressure ratios, diffusion included), fictional head of
dist/hum-3d.html (literature means). Cells: share of the sinus exchanged in 10 s of humming, and the stroke ratio
x = L0/L of the fundamental. P0 is the effective pressure at the maxillary ostium (130 Pa = calibrated default).

Ceiling for an infinitely fast exchange at the ostium: 70 % in 10 s (the near half empties at once, the far half mixes
on 40 s).

maxillary (12.75 mL, 2.8 mm, 2.1 mm; resonance 578 Hz; diffusion alone 2 %)

| P0 \ f | 100 Hz | 150 Hz | 200 Hz | 300 Hz |
|---|---|---|---|---|
| 65 Pa | 13 % (x 0.95) | 22 % (0.98) | 36 % (1.04) | 56 % (1.25) |
| 130 Pa | 43 % (1.89) | 56 % (1.97) | 62 % (2.08) | 66 % (2.48) |
| 260 Pa | 63 % (3.78) | 66 % (3.93) | 67 % (4.15) | 68 % (4.83) |
| 520 Pa | 67 % (7.56) | 68 % (7.84) | 69 % (8.22) | 69 % (8.95) |

sphenoid (4.0 mL, 2.2 mm, 1.5 mm; resonance 935 Hz; diffusion alone 5 %): 130 Pa gives 48 / 56 / 60 / 66 % at
100 / 150 / 200 / 300 Hz; 260 Pa gives 64–69 %.

frontal (2.9 mL, 7.5 mm, 4.0 mm; resonance 2135 Hz): 23–24 % everywhere, all of it diffusion (x 0.01–0.11).

ethmoid cell (0.4 mL, 1.5 mm, 1.5 mm; resonance 2223 Hz): diffusion gives 25 %; humming adds 1–4 points at 130 Pa,
11–25 at 260 Pa and 35–41 at 520 Pa (x reaches about 1.2).

Seconds of humming to exchange half of the maxillary sinus: 150 Hz 130 Pa 7.8 s; 300 Hz 130 Pa 2.8 s; 150 Hz 260 Pa
2.8 s; 300 Hz 260 Pa 1.3 s; 150 Hz 520 Pa 1.3 s.

## Reading

- Below the sinus resonance the stroke volume is the sinus compression V·P/(γ·p_atm), independent of pitch, so x
  hardly changes with f (1.89 → 2.08 from 100 to 200 Hz). Higher pitch helps because there are more strokes per
  second. Near the resonance x grows (2.48 at 300 Hz for the maxillary, f/f0 = 0.52), and the harmonics (300–900 Hz
  for a 150 Hz hum) sit around the resonance, which is why they add so much.
- Doubling the pressure does about as much as doubling the pitch (half-time 7.8 → 2.8 s either way). Louder also
  lifts x, which matters most where x is small (ethmoid cells: nothing at 130 Pa, a real effect at 520 Pa).
- Above the defaults both run into the 10-s ceiling (~70 %), set by how fast the far part of the sinus mixes
  (the 40-s compartment time, a calibrated assumption). Past that point, humming longer helps more than louder or
  higher. **Later the same day the long 3D runs (results/agefield_maxillary.md) showed the sinus air mixing within
  2–3 s, so this ceiling is an artefact of the two-compartment structure; with a well-mixed sinus, louder and higher
  keep paying off.**
- The frontal sinus does not respond to either within the model: its wide, short ostium gives a stroke of 1–10 % of
  its length.
- The pages keep P0 constant across pitch. The 1D tract model of tools/nostril_occlusion.py gives, for the same
  glottal source and both nostrils open, a maxillary-ostium pressure of 0.57 / 0.80 / 1.00 / 1.75 / 2.48 / 1.70 /
  1.73 times the 150-Hz value at 100 / 130 / 150 / 200 / 250 / 300 / 400 Hz (the nasal tract's first resonance near
  250 Hz). If that holds, the advantage of a higher hum is larger than the pages show; how the voice source itself
  changes with pitch is not in the model. The intranasal pressure during humming has not been measured
  (roadmap §1), so this stays the largest uncertainty.
