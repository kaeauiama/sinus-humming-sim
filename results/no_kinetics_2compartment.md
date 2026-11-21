# Two-compartment sinuses (tools/no_calibrate2.mjs, 2026-11-21)

## Why

The one-compartment NO model (pages since 5250f7e) empties the maxillary sinus in one hum and then has nothing left:
with 3-s gaps the 2nd peak is 13 % of the 1st. Maniscalco 2003 Fig. 3 (one subject, 5 hums at 5-s intervals,
digitised from publications.ersnet.org/content/erj/22/2/323/F3.large.jpg) shows instead:
- hum 1: peak ~4300 nL/min at 1.2 s, ~2/3 of it by 2.5 s, then a slow decline to ~1140 at 10 s (c(10)/c(2) ≈ 0.34);
- mean of the last 8 s relative to hum 1: hum 2 ≈ 0.49, hum 3 ≈ 0.40, hums 4–5 ≈ 0.3 (text: plateau 26 %).
Two time scales, which a single well-mixed box cannot give.

## Model

Each sinus = near-ostium part (fraction fn of the volume; exchanged by humming and diffusion) + far part, mixing with
each other at rate 1/tauInt (exchange volume per s ÷ whole volume). fn = 1 is the old model (checked: identical output).
Targets: the Fig. 3 sequence (49 / 40 / 27 %), the tail ratio 0.34, Menzel washout 3.0 ± 1.2 s, mean ratio 4.2–4.7×,
quiet drop after the hums 32 % (5–50), 3-min recovery ~complete, Menzel refill 4.5 ± 3.2 min (prior), mucosa ≥ 50 %.
Weak harmonics (−12 dB/oct). Grid 5 P0 × 5 tauRec × 3 mucosa × 2 phi × (1 + 3 fn × 5 tauInt) = 2400 runs.

## Result

| model | P0 | tauRec | mucosa | phi | fn | tauInt | ratio | hums 2/3/5 | tail | washout | quiet drop | 3-min | cost |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| target | | 4.5 ± 3.2 min | ≥ 50 % | | | | 4.2–4.7× | 49/40/27 % | 0.34 | 3.0 s | 32 % | ~100 % | |
| one compartment, page defaults | 200 | 120 s | 0.5 | 1 | 1 | — | 4.6× | 37/34/33 % | 0.20 | 2.7 s | 17 % | 87 % | 5.7 |
| one compartment, best | 160 | 120 s | 0.5 | 1 | 1 | — | 4.8× | 40/33/32 % | 0.30 | 3.6 s | 15 % | 87 % | 4.4 |
| two compartments, best | 160 | 180 s | 0.7 | 0.3 | 0.5 | 20 s | 4.5× | 53/39/32 % | 0.37 | 2.1 s | 18 % | 83 % | 2.9 |
| two compartments, literature-anchored | 130 | 270 s | 0.5 | 1 | 0.5 | 40 s | 4.4× | 56/44/34 % | 0.37 | 2.9 s | 20 % | 80 % | 3.1 |

- Every top-10 two-compartment fit has fn = 0.5: about half of the sinus volume is reached quickly by the humming jet,
  the rest exchanges with it on a 5–80 s scale (20–40 s typical).
- The repeated-hum sequence and the shape of the first hum now match; the one-compartment model cannot do both.
- The needed effective pressure drops to 130–160 Pa, and the refill time constant can stay at Menzel's 4.5 min
  ("literature-anchored" row: only P0, fn and tauInt are fitted; tauRec, phi = 1 and mucosa 50 % are not tuned).
- Still low: the quiet drop after repeated hums (18–20 % vs 32 %, inside 5–50 %).
- The pages still use the one-compartment model (200 Pa, 2 min). Adopting the two-compartment NO model is the next
  step (roadmap); it changes the NO numbers but not the ventilation map's 5-s exchange (which uses the whole sinus).
