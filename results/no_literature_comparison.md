# How much does humming raise nasal NO? Literature vs model (2026-11-21)

## Literature (abstracts via Europe PMC; Maniscalco 2003 full text at publications.ersnet.org)

| study | subjects, method | humming ÷ quiet | what was compared |
|---|---|---|---|
| Weitzberg & Lundberg 2002, AJRCCM 166:144 (letter) | 10 healthy, chemiluminescence, fixed flow | **15×** | not stated in the abstract; full text behind a bot check (not read) |
| Maniscalco et al. 2003, Eur Respir J 22:323 | 10 healthy, 0.2 L/s, 10-s exhalation, NIOX | **4.7×** (2233 ± 467 vs 471 ± 73 nL/min) | mean output over the last 8 s |
| Shusterman et al. 2007, Eur J Clin Invest (doi 10.1111/j.1365-2362.2007.01845.x) | 10 healthy, ATS parallel technique | **4.2×** (series technique 2.1×) | mean ratio of humming to quiet NO |

Also from Maniscalco 2003 in vivo: with 5-s intervals the output fell step-wise to a plateau of 571 nL/min (26 % of the first)
within four hums; with 3-min intervals the variability was < 15 % (complete recovery); with 1-min intervals ~70 %.
Quiet nasal NO after repeated hums was 5–50 % lower (mean 32 %). In the syringe model ~100 % of the gas was exchanged
by one hum at the widest ostium. The thesis (Maniscalco 2006, KI) is a 496 kB PDF; not downloaded (needs the user's OK).

The 15× is the outlier and its definition is unknown; the two quantitative studies give a mean increase of 4.2–4.7×.

## Model, same definition (tools/no_model.mjs; matches the pages' NO model)

150 Hz, 100 Pa:

| setting | peak ÷ quiet (pages' old metric) | mean of last 8 s ÷ quiet | 2nd/1st peak | after 3 min |
|---|---|---|---|---|
| law, no harmonics | 4.0× | 3.1× | 65 % | 70 % |
| maxillary η from 3D (0.35) | 4.7× | 3.4× | 58 % | 66 % |
| harmonics −12 dB/oct | 4.9× | 3.4× | 57 % | 66 % |
| harmonics −6 dB/oct | 18.1× | 4.1× | 11 % | 56 % |

Pressure needed: mean 4.2× at 148 Pa (no harmonics), 132 Pa (−12 dB/oct), 67 Pa (−6 dB/oct). The mean never reaches
4.7×: it saturates at 4.4× (182 / 157 / 86 Pa) because the maxillary sinus empties during the hum.

- Compared like with like, the gap is 3.1–3.4× vs 4.2–4.7× (a factor ~1.4), not 4× vs 15×. A nasal sound pressure of
  ~130–150 Pa instead of the assumed 100 Pa (+2.5 to +3.5 dB) closes it; that pressure has never been measured.
- The measured 4.7× sits at the model's ceiling: it implies the maxillary sinus is nearly emptied by one 10-s hum,
  consistent with Maniscalco's own reading.
- Tension in the kinetics: near-complete emptying plus complete recovery in 3 min needs a refill time constant of about
  1 min, while the model uses Menzel 2005's 4.5 ± 3.2 min. With tau 60–90 s the 3-min recovery becomes 90–98 %, but the
  mean ratio drops to 2.1–3.0× at 100–200 Pa (the small sinuses then add more to the quiet baseline). The NO model's
  calibration (fixed 8 ppm, NO production ∝ surface, 70 % mucosal share) cannot meet all of Maniscalco's in-vivo
  numbers at once.

## Sound pressure and harmonics (searched, not found)

- No direct measurement of the acoustic pressure inside the nasal cavity during humming was found (also not in the
  ../sinus-rescue notes). 100 Pa stays an assumption.
- Harmonic content: the voice source falls about 12 dB per octave above ~250 Hz (general speech-acoustics text); the
  first nasal resonance is near 250–500 Hz with a broad bandwidth, lifting the harmonics near it by a few dB. So the
  pages' "weak" setting (−12 dB/oct) is the realistic one and "strong" (−6 dB/oct) an upper bound.
