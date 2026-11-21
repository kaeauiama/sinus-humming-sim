# Dimensions of the non-maxillary sinuses from the literature (web search, 2026-11-21)

Values were read from abstracts and search summaries, not full texts; treat single-study numbers as indicative.

| sinus | quantity | literature | pages / model before | source |
|---|---|---|---|---|
| sphenoid | volume | 4.00 ± 1.99 mL (men 4.74 ± 2.06, women 3.55 ± 1.73; healthy adults, CT) | 4.0 mL; population 4.0 ± 2.0 | Cohen et al. 2018, Auris Nasus Larynx 45:96–102 (abstract) |
| sphenoid | ostium diameter | 2.18 ± 0.42 mm (women), 2.26 ± 0.53 mm (men), CBCT; usually quoted 2–3 mm, 11–14 mm above the sinus floor, 4–5 mm from the septum | 2.2 mm; population 2.2 ± 0.5 | CBCT study of a Turkish population (dergipark.org.tr, 2022) |
| sphenoid | anterior wall thickness at the ostium (= ostium length L) | not found | 1.5 mm; population 1–3 mm | — |
| frontal | volume | 2.92 ± 2.57 mL (men 3.74, women 3.21) | 2.9 mL; population 2.9 ± 2.6 | Cohen et al. 2018 |
| frontal | ostium, anteroposterior diameter | 7.5 ± 2.7 mm (range 2–15 mm); below 5 mm in 17.6 % of sinuses | 7.5 mm; population 7.6 ± 2.0 → now 7.5 ± 2.7 (2–15) | CT study tied to endoscopic difficulty (search summary; probably Ear Nose Throat J 2021 "Frontal angle"; not verified) |
| frontal | drainage path | not a duct: the frontal sinus and frontal recess form an hourglass on sagittal CT, the narrowest part being the ostium ("nasofrontal duct" is no longer used) | L 4 mm (a short neck) | review statements in the search results |
| ethmoid | number of cells | 9 per side on average (4–17) | 8 | review (search summary) |
| ethmoid | volume | anterior group 4.33–4.92 cm³, posterior 3.01–3.47 cm³ (≈ 7.5–8.4 mL per side); another 3D-CT study ≈ 3.3–3.5 mL per side | 0.4 mL × 8 cells = 3.2 mL; population 0.2–0.8 → now 0.3–0.9 mL per cell | Rom J Rhinol 2017 (doi 10.1515/rjr-2017-0020); 3D-CT 150 cases (already cited on hum-map) |
| ethmoid | cell ostium | not found | 1.5 mm; population 1–2.5 mm | — |

## What changed

- The pages' default dimensions were already at the literature means; they stay.
- Population model (tools/population_pitch.py): frontal ostium 7.5 ± 2.7 mm (2–15), ethmoid cells 0.3–0.9 mL.
- Still unmeasured: the wall thickness at the sphenoid ostium, the ethmoid cell ostia. The sphenoid result is most
  sensitive to ostium size and volume, which now come from measurements; the wall thickness remains a guess (1–3 mm).

## Spread between people (population model, 10 s at 150 Hz, weak harmonics; 10 / 50 / 90 percentiles)

| sinus | exchanged by humming | diffusion time constant |
|---|---|---|
| maxillary | 7 / 46 / 63 % | 166 / 482 / 1083 s |
| sphenoid | 10 / 50 / 65 % | 69 / 197 / 431 s |
| frontal | 0 / 0 / 0 % | 4 / 36 / 117 s |
| ethmoid cell | 0 / 3 / 19 % | 21 / 42 / 92 s |

- About one person in ten gets only 7–10 % in the maxillary and sphenoid sinuses: small sinus plus wide ostium,
  so the stroke is short compared with the ostium length.
- Frontal and ethmoid: humming does essentially nothing; diffusion takes under two minutes for most people.
