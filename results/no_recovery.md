# NO recovery between hums, compared the way each study measured it (tools/no_recovery.mjs, 2026-11-21)

The pages flagged "peak after a 3-min rest ÷ first peak" (63–68 %) against "almost complete recovery". Both
literature statements were taken with other procedures:
- Menzel 2005 (abstract; full text behind a Cloudflare check, not in PMC, PMID 15691901): peak height of a hum vs the
  time since the previous hum, fitted with one time constant: 4.5 ± 3.2 min.
- Maniscalco 2003: five hums with equal 3-min intervals were alike (intra-individual variability < 15 %); with 1-min
  intervals ~70 %.

## Menzel's way (peak of hum 2 ÷ peak of a rested hum 1, vs interval), page model (two compartments, 130 Pa)

| model parameter tauRec | 5 s | 30 s | 1 min | 2 min | 3 min | 5 min | 10 min | apparent tau (peaks) |
|---|---|---|---|---|---|---|---|---|
| 120 s | 40 % | 64 % | 73 % | 84 % | 90 % | 96 % | 100 % | 1.2 min |
| 270 s (pages) | 35 % | 55 % | 61 % | 69 % | 75 % | 84 % | 95 % | 2.5 min |
| 600 s | 32 % | 51 % | 56 % | 61 % | 66 % | 73 % | 85 % | 4.2 min |

In two compartments the peak first recovers fast (the far half refills the near half on ~40 s) and then slowly, so the
apparent single time constant is shorter than the model parameter. The pages' 270 s gives an apparent 2.5 min,
inside Menzel's 4.5 ± 3.2 min.

## Maniscalco's way (five hums at equal intervals, mean of the last 8 s)

| interval | tauRec 120 s | 180 s | 270 s (pages) | 600 s |
|---|---|---|---|---|
| 3 min: hums 2–5 ÷ hum 1; CV | 93–92 %; 4 % | 87–85 %; 7 % | 80–75 %; 13 % | 71–58 %; 25 % |
| 1 min: hums 2–5 ÷ hum 1; CV | 80–73 %; 14 % | 74–63 %; 21 % | 69–52 %; 30 % | 62–38 %; 45 % |

With "variability" read as the coefficient of variation, the pages' 270 s meets the 3-min statement (13 % < 15 %).
No setting gives a 70 % CV at 1 min; read as range/mean, 270 s gives 73 % at 1 min (but 31 % at 3 min). The two
statements are too loosely defined to pin the refill time better than "about 2–5 min".

## Consequence

The pages' recovery row compared a different protocol (three hums 3 s apart, then 3 min) with "almost complete";
it is now shown as a reference row without a pass/fail mark (integrated page and hum-map). Measured like-for-like,
the current parameters agree with both studies.
