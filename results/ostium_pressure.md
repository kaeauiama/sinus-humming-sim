# Sound pressure at each ostium and what it does to the non-maxillary sinuses (2026-11-21)

## Model (tools/ostium_pressure.py → results/ostium_pressure.json)

1D transmission line of glottis–pharynx–mouth (lips closed)–nasal cavity, ported from
../sinus-rescue/tools/hum-model/nasal_model.py (same author; dimensions and losses are literature-scale guesses,
validated there against the nasal murmur peak near 250–300 Hz and the oral antiresonance near 1 kHz). Hum [m], nose
open. Ostium positions from the velopharyngeal port outlet (approximate anatomy): sphenoid 2.5 cm, posterior ethmoid
3.5 cm, maxillary 5.5 cm, anterior ethmoid 6.0 cm, frontal 6.5 cm; nostril 10 cm.

Pressure relative to the maxillary ostium:

| f (Hz) | sphenoid | posterior ethmoid | anterior ethmoid | frontal | ethmoid (mean used on the pages) |
|---|---|---|---|---|---|
| 100–200 | 1.36–1.43 | 1.24–1.29 | 0.93 | 0.85 | 1.08–1.11 |
| 300 | 1.49 | 1.32 | 0.93 | 0.86 | 1.12 |
| 450 | 1.57 | 1.39 | 0.93 | 0.86 | 1.16 |
| 900 | 1.26 | 1.20 | 0.95 | 0.90 | 1.08 |
| 1800 | 0.45 | 0.68 | 1.04 | 1.06 | 0.86 |

The open nostril is a pressure node, so pressure grows towards the back of the nose; at 150 Hz, relative to the
sphenoid ostium: posterior ethmoid 0.91, maxillary 0.71, anterior ethmoid 0.66, frontal 0.61.

## Effect (pages since 3dd5cde; P0 = 130 Pa now means the maxillary-ostium pressure)

- NO calibration: with the ratios, the two-compartment best fit is exactly the pages' defaults (cost 3.1 → 2.5).
- Ventilation map at 150 Hz, weak harmonics, 5 s: sphenoid η 20 → 32 %, exchange 26 → 42 % (same as the maxillary,
  42 %); frontal 13 % and ethmoid 15 % unchanged (diffusion; their strokes stay far below the ostium length).
- Integrated page: nasal NO mean 4.6×, first peak 15.8× (literature 15×), 2nd peak 27 %, quiet drop 20 %.
- Population (tools/population_pitch.py, 10 s, weak harmonics, median): sphenoid 150 Hz 50 % / 300 Hz 65 %
  (31 % / 56 % without the ratio); maxillary 46 % / 64 %. Both are capped near two thirds in 10 s by the far half's
  40-s mixing.

## Caveats

- The positions are approximate and individual noses differ (septal deviation, turbinate swelling). Congestion that
  narrows the front of the nose raises the pressure everywhere behind it (sinus-rescue §9).
- The model lumps both sides into one tube and includes only the maxillary and sphenoid sinuses as acoustic branches.
- For the frontal sinus and ethmoid cells the ratio does not matter: they are ventilated by diffusion.
