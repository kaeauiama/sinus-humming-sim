# Can NasalSeg give real geometry for the other sinuses? (tools/nasalseg_ct_extent.py, 2026-11-21)

Headers of all 130 CT images in ../NasalSeg.zip:

| quantity | value |
|---|---|
| in-plane spacing | 0.586 mm (all cases) |
| slice spacing | 1.50 mm (all cases; none ≤ 1 mm) |
| height (z extent) | median 77 mm, 59–89 mm |
| in-plane extent | ~89 × 109 mm |
| image above the top of the maxillary sinus (6 cases) | 17–26 mm |

- Frontal sinus (above the orbits, several cm above the maxillary roof): essentially outside the images.
- Ethmoid cells: partly inside, but their 0.2–0.5 mm septa cannot be resolved with 1.5 mm slices (the earlier P001
  observation holds for every case).
- Sphenoid sinus: at best partly inside; separating it from the posterior ethmoid cells would need hand work.

So NasalSeg cannot supply real 3D geometry for the non-maxillary sinuses. Their modelling stays lumped (literature
dimensions), improved instead by where each ostium sits in the nasal cavity (results/ostium_pressure.md).
