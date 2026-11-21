# Closing or narrowing a nostril (2026-11-22, `python tools/nostril_occlusion.py`, engine-independent)

1D vocal/nasal tract model of tools/ostium_pressure.py with the nasal cavity split into left and right passages after
the velopharyngeal port. Same glottal source in every case. Pressure at the maxillary ostium relative to the same
ostium with both nostrils open (results/nostril_occlusion.json has all ostia):

| case | side | 100 Hz | 130 | 150 | 200 | 250 | 300 | 400 | 600 |
|---|---|---|---|---|---|---|---|---|---|
| left closed | left (closed) | 3.83 | 4.03 | 4.10 | 2.71 | 1.29 | 1.17 | 1.40 | 1.79 |
| left closed | right (open) | 2.07 | 2.16 | 2.17 | 1.38 | 0.62 | 0.70 | 0.87 | 0.94 |
| left narrowed to 1/4 area | left | 1.49 | 1.51 | 1.54 | 1.56 | 1.25 | 1.10 | 1.15 | 1.24 |
| left narrowed to 1/4 area | right | 1.19 | 1.20 | 1.22 | 1.22 | 0.96 | 0.90 | 0.96 | 0.99 |
| both closed | both | 7.54 | 4.82 | 3.46 | 1.48 | 0.80 | 0.90 | 1.22 | 1.69 |

At 150 Hz with the left nostril closed, the other ostia on the closed side get 2.8 (sphenoid) to 4.8 (frontal) times
their open-nose pressure.

## Reading

- The open nostril is a pressure node. Closing it turns the passage into a closed-end tube and removes most of the
  radiation load, so in the humming range (100–200 Hz) the pressure at the ostia rises several-fold. The effect fades
  above about 250 Hz, where the tract's resonances move.
- In the ventilation model, 4 × 130 Pa ≈ 520 Pa would bring the maxillary sinus to 68 % in 10 s (half in 1.3 s) and
  the ethmoid cells to about 63 % (results/pitch_loudness.md).
- But the model assumes the air outside the ostium is always fresh, renewed by the exhaled flow. With the nostril
  closed there is no through-flow on that side. The passage (several mL) exchanges with the nasopharynx only by its
  own small compression stroke, while the sinus pushes a comparable volume of its own air into it each second. The
  air the sinus draws back in would soon be largely its own. Whether the net exchange with outside air goes up or
  down cannot be settled with this model; it needs the nasal passage as a third compartment, or a 3D run.
- Both nostrils closed cannot be sustained: the exhaled air has nowhere to go.
- The absolute factors depend on the tract model's loss and wall parameters, which were not fitted to measurements.
  Treat them as "several-fold", not as 4.1.
