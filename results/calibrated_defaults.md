# Page numbers with the calibrated defaults

## Current (2026-11-22): one-box sinus air + mucosal store, 180 Pa, mucosa 70 % (results/no_kinetics_store.md)

Checked in the built-in browser: integrated page (`?fake&autorun`, law for the maxillary) mean 4.6×, first peak 14.3×,
3 of 3 comparable items inside the literature; maxillary air exchanged in one 10-s hum 95 %. Ventilation map: mean
4.6×, peak 14.3×, quiet drop after the repeated hums 11 %. 3D page: 10 s at 150 Hz exchanges 94 % (maxillary), 95 %
(sphenoid), 25 % (frontal, diffusion), ~40 % (ethmoid cell, mostly diffusion). Integrated page with the real 3D run (`?autorun`, P001, 0.4 mm, commit 4d3b281): stroke 6.81 mm, mixing efficiency
49 % (law 50 %), mean 4.6×, first peak 14.3×, 3 of 3 comparable items inside the literature, maxillary air exchanged
in one 10-s hum 95 %. At this larger stroke the real shape and the ideal-geometry law agree, as found before for
L0/L above ~3.

## Previous: two-compartment sinuses (commit b38d329, 2026-11-21)

Defaults: 150 Hz, effective 130 Pa, weak harmonics, near-ostium half + far half mixing on 40 s, NO refill 4.5 min
(Menzel, untuned), mucosa 50 % (results/no_kinetics_2compartment.md). Built-in browser, NVIDIA Ampere.

Integrated page (?autorun, P001, 0.4 mm grid):

| item | 3D / law only | literature |
|---|---|---|
| stroke L0 | 4.56 mm (L0/L 2.2; run reached 5.03 mm) | |
| maxillary η | 44 % / 39 % | |
| whole maxillary exchanged by one 10-s hum (two compartments) | 58 % | |
| nasal NO mean of last 8 s ÷ quiet | 4.4× / 4.5× ✓ | 4.2–4.7× |
| first peak ÷ quiet | 14.4× / 13.3× | 15× |
| 2nd peak ÷ 1st (3-s gaps) | 28 % / 30 % ✓ | gradual fall |
| quiet NO drop after the hums | 19 % ✓ | 5–50 % |
| peak after 3 min ÷ 1st | 63 % / 64 % ✗ | ~complete |

Ventilation map: maxillary η 38 %, 5-s exchange 42 %; sphenoid 20 %, 26 %; frontal 13 % and ethmoid 15 % (diffusion).
NO: mean 4.5×, peak 13.0×, 2nd/1st 31 %, quiet drop 18 %, 3-min recovery 68 %; the mean reaches 4.2× from ~105 Pa.

Four of five literature items are now inside their bands, and the first peak lands on the 15× of 2002. The 3-min
recovery stays low because the refill time constant is Menzel's published 4.5 min (Maniscalco's "complete recovery
after 3 min" and Menzel's 4.5 ± 3.2 min disagree unless refill is ~2 min).

## Previous: one compartment (commit 5250f7e, 2026-11-21)

Defaults now: 150 Hz, effective 200 Pa, weak harmonics (−12 dB/oct), NO refill time constant 2 min, mucosal share 50 %
(results/no_kinetics_calibration.md). Built-in browser, NVIDIA Ampere. Before = 100 Pa, no harmonics, 4.5 min, 70 %.

## Integrated page (?autorun, P001 on the 0.4 mm grid)

| item | now (3D / law only) | before (3D / law only) |
|---|---|---|
| stroke L0, L0/L | 7.0 mm, 3.4 (3D run reached 7.21 mm) | 3.5 mm, 1.7 |
| maxillary η | 50 % / 52 % | 35 % / 29 % |
| maxillary air exchanged by one 10-s hum | 97 % | 57 % |
| nasal NO, mean of last 8 s ÷ quiet (lit. 4.2–4.7×) | 4.7× / 4.7× ✓ | 3.4× / 3.1× |
| first peak ÷ quiet (lit. 15×, method unknown) | 19.4× / 19.9× | 4.7× / 4.0× |
| 2nd peak ÷ 1st (3-s gaps) | 13 % / 13 % | 57 % / 65 % |
| quiet NO drop after the hums (lit. 5–50 %) | 18 % ✓ | 10 % |
| peak after 3 min ÷ 1st (lit. ~complete) | 82 % | 66 % / 70 % |

- At 200 Pa the real geometry mixes like the ideal-geometry law (50 vs 52 %); the excess seen at 100 Pa (35 vs 29 %,
  L0/L 1.7) disappears at L0/L 3.4.
- Still outside the literature bands: the second peak collapses too fast (13 %; Maniscalco's means fall gradually to
  26 % over four hums) and the 3-min recovery is 82 % (band 85–110 %).

## Ventilation map (hum-map.html)

| sinus | L0 | L0/L | η | 5 s humming + diffusion | 5 s diffusion only |
|---|---|---|---|---|---|
| maxillary | 7.0 mm | 3.3 | 52 % | 84 % | 1 % |
| sphenoid | 3.1 mm | 2.1 | 35 % | 61 % | 3 % |
| frontal | 0.19 mm | 0.05 | 0 % | 14 % | 14 % |
| ethmoid cell | 0.65 mm | 0.4 | 3 % | 20 % | 15 % |

NO: mean 4.7×, first peak 19.7×, 2nd/1st peak 13 %, 3-min recovery 81 %, quiet drop after hums 17 %.
The mean reaches the measured 4.2× from about 115 Pa (with the weak harmonics and the calibrated NO parameters).
