# Why the P001 ostium mixes more than the ideal-geometry law (tools/ostium_effective_length.py, 2026-11-21)

## Enclosed length of the carved cylinder

Ring just outside the hole (radius r + 0.5 … r + 1.5 cells), base mask of geometry/p001_040; "enclosed" = at least 50 %
of the ring is solid. Nominal tube A → B: 2.05 mm (axis along −x).

| d (mm) | enclosed length | note |
|---|---|---|
| 2.0 | 1.20 mm | sinus side open early (ring 81 % sinus at 0.5 cell), nasal side opens gradually |
| 2.8 | 1.60 mm | |
| 4.0 | 2.40 mm | the wider ring reaches thicker bone; both ends open obliquely and gradually |

## Length the mixing law needs to reproduce the measured 3D mixing

| case | d | stroke L0 | L0/L (nominal) | η 3D | law at 2.1 mm | law matches 3D at L = |
|---|---|---|---|---|---|---|
| E2, 100 Pa | 2.0 | 7.24 mm | 3.4 | 0.56 | 0.56 | 2.17 mm |
| E2, 100 Pa | 2.8 | 3.51 mm | 1.7 | 0.36 | 0.28 | 1.58 mm |
| E2, 100 Pa | 4.0 | 1.67 mm | 0.8 | 0.16 | 0.07 | 1.15 mm |
| integrated, 100 Pa | 2.8 | 3.25 mm | 1.5 | 0.35 | 0.25 | 1.47 mm |
| integrated, 200 Pa | 2.8 | 7.21 mm | 3.4 | 0.50 | 0.53 | 2.52 mm (law is flat here) |

## Reading

- "The effective ostium is shorter" works for 2.8 mm (enclosed 1.60 mm vs needed 1.47–1.58 mm) but not across
  diameters: 4.0 mm would need 1.15 mm while it is enclosed over 2.4 mm, and 2.0 mm needs no correction at all.
- The pattern of the excess matches rounding instead: the real geometry mixes more only when L0/L is small
  (4.0 mm at 0.8: +9 points; 2.8 mm at 1.5–1.7: +8–10) and not at L0/L ≈ 3.4 (2.0 mm: 0; 2.8 mm at 200 Pa: −2).
  Rounding experiment E1 (ideal geometry) had the same signature: fully rounded edges raise η at L0/L = 1 (11 → 21 %)
  and change it by ≤ 3 points at L0/L = 2 and 4. The CT wall meets the cylinder obliquely and irregularly, so its
  openings act like flared/rounded edges.
- With the calibrated defaults (200 Pa, L0/L ≈ 3.4 for P001) the difference is gone (50 vs 52 %), so the pages need no
  correction. It matters only for small strokes (quiet humming, wide ostia).
