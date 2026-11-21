# Page numbers after switching to the refit mixing law (commit eee38fa, 2026-11-21)

> Update (commit eafe134, long-tube factor added): rechecked the same day. Integrated page unchanged except
> 2nd/1st peak (law only) 64 → 65 %. Ventilation map: NO 4.1 → 4.0×, 15× at 226 → 225 Pa, −12 dB/oct 4.8 → 4.9×,
> mucosa 0.5 mm 11.0 → 11.1×, sphenoid η 12 → 13 %, maxillary 5-s exchange 29 → 28 %; everything else identical.

Built-in browser, NVIDIA Ampere. 150 Hz, 100 Pa, maxillary 14 mL / 2.8 mm / 2.1 mm unless noted.
"Before" values are the ones in docs/findings.md up to 2026-11-21 (old soft law; the 2D law for population_pitch).

## Integrated page (dist/sinus3d-integrated.html?autorun, P001 on the 0.4 mm grid)

| item | 3D (maxillary η measured) | law only | before (3D / law) |
|---|---|---|---|
| maxillary η | 35 % (stroke 3.25 mm, 3 cycles) | 29 % | — / 33 % |
| nasal NO, first hum peak ÷ quiet | 4.7× | 4.1× | 4.4–4.9× |
| 2nd peak ÷ 1st | 57 % | 64 % | ≈ 60 % |
| quiet NO drop after repeated hums | 10 % | 10 % | ≈ 10 % |
| peak after 3 min rest ÷ 1st | 66 % | 70 % | 66–71 % |

The 3D column moves little because the maxillary η is measured, not taken from the law; only the other sinuses
(sphenoid, frontal, ethmoid) use the law there.

## Ventilation map (dist/hum-map.html)

| item | after | before |
|---|---|---|
| η (fundamental): maxillary / sphenoid / frontal / ethmoid | 28 / 12 / 0 / 1 % | 33 / 17 / 0 / ≈ 1 % |
| 5 s of humming + diffusion: maxillary / sphenoid | 29 / 15 % | — |
| nasal NO peak ratio | 4.1× | 4.6× |
| 2nd peak ÷ 1st | 65 % | ≈ 60 % |
| peak after 3 min rest ÷ 1st | 74 % | 66–71 % |
| quiet NO drop after repeated hums | 9 % | ≈ 10 % |
| P0 needed for 15× (no harmonics) | 226 Pa | 216 Pa |
| harmonics −12 dB/oct: ratio, 2nd peak | 4.8×, 57 % | — |
| harmonics −6 dB/oct: ratio, 2nd peak | 18.1×, 11 % (15× at 91 Pa) | 22.7×, 7 % |
| mucosa 0.5 mm (d_eff 1.8 mm) | 11.0× | 10.6× |
| mucosa 0.5 mm + mucus 150 µm | 1.0× (closed) | 1.0× |

## Tools

- tools/ostium_sweep.mjs → results/ostium_sweep_lumped.md (best ostium for humming still 1.2–1.6 mm; wide ostia much worse).
- tools/population_pitch.py → results/population_pitch.md (absolute exchange about halves vs the old 2D law; conclusions hold).
- tools/syringe_fig6_fit.mjs → results/syringe_fig6_fit.md (Fig. 6 fit worsens to rms 9–10 points; outside the law's range).
