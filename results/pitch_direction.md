# Pitch: why the in-vivo NO falls with pitch while the model ventilates faster (2026-11-21)

Maniscalco 2003 in vivo (5 subjects, nasal humming at three pitches, mean nasal NO output over the last 8 s of a 10-s
exhalation): 130 Hz 940, 150 Hz 807, 450 Hz 719 nL/min → 1.16 : 1 : 0.89. The model says the maxillary hum
ventilation rate rises with pitch below resonance (kH 0.10 → 0.88 /s from 130 to 450 Hz at 130 Pa), which looked
like the opposite direction.

Same protocol in the model (tools/no_model.mjs; quiet 10 s, inhale 5 s, one 10-s hum), nasal NO ÷ quiet:

| setting | f (Hz) | maxillary kH (1/s) | mean of last 8 s | mean of all 10 s | first peak |
|---|---|---|---|---|---|
| page defaults (2 compartments, 130 Pa, weak harmonics) | 130 | 0.096 | 4.39× | 5.34× | 11.3× |
| | 150 | 0.115 | 4.45× | 5.60× | 13.0× |
| | 200 | 0.174 | 4.18× | 6.18× | 21.5× |
| | 300 | 0.369 | 3.40× | 6.73× | 44.5× |
| | 450 | 0.875 | 2.95× | 6.97× | 74.4× |
| one compartment, 200 Pa (previous defaults) | 130 / 150 / 200 / 300 / 450 | 0.20–1.22 | 4.77 / 4.63 / 3.82 / 2.60 / 2.13× | 6.41–7.36× | 16.6–75.2× |

- With the measurement's own definition the model gives 450 Hz the lowest value, as measured. The previous
  one-compartment defaults even reproduce the full order 130 > 150 > 450; the two-compartment defaults give
  130 ≈ 150 > 450 (0.99 : 1 : 0.66; measured 1.16 : 1 : 0.89).
- Reason: the faster the sinus is ventilated, the more of its NO comes out in the first 1–2 s, which the
  last-8-s mean leaves out. The same saturation made the mean ratio peak and then fall with sound pressure
  (results/no_literature_comparison.md).
- The peak and the whole-hum mean rise with pitch. A fast analyser looking at peaks (as Menzel 2005) should therefore
  see the opposite order: a testable prediction.
- So there is no conflict with "higher pitch ventilates faster below resonance". It does mean that pitch effects in
  NO studies depend strongly on which number is reported.
