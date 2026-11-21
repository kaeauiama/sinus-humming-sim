# NO comes from the wall: does that make the sinus air uneven? (2026-11-22, `python tools/no_wall_source.py`)

Order-of-magnitude estimates for the maxillary sinus of the pages (12.75 mL; equal-volume sphere of radius 14.5 mm,
wall 26.4 cm²; NO diffusivity 2×10⁻⁵ m²/s; refill time 270 s as in the pages).

- NO at ppm levels is a passive tracer: it does not change the flow, only what the flow carries.
- At rest the sinus air is uniform. The slowest diffusion mode across the sinus takes a²/(π²D) ≈ 1.1 s, against
  270 s for production and loss to balance. With the loss spread through the air (the worst case), wall and centre
  differ by 0.65 %. With the loss at the wall too (re-uptake into the mucosa), there is no gradient at all apart
  from the ostium.
- During a hum the wall adds little: 1.9 % of the resting content in 5 s, 3.7 % in 10 s. Even if all of it stayed
  next to the wall, the NO output would change by a few percent at most, and the 3D runs stir the sinus within 2–3 s
  (results/agefield_maxillary.md).
- The ostium wall is 18 mm², 0.7 % of the sinus wall.
- The mucosa cannot hold a meaningful NO store: NO dissolves poorly in water (water/air partition 0.046), so a wet
  layer of 10–300 µm holds 0.01–0.3 % of what the sinus air holds.

## Consequence

The uneven source does not matter for the mixing or the NO output. It also cannot be the slow part that the in-vivo
NO data need (results/no_kinetics_2compartment.md): neither the sinus air (it mixes in seconds) nor a physical store
in the mucosa (too small) can provide it. What remains is how the production rate itself behaves (for example a
production that rises when the sinus concentration falls, or that is exhausted and recovers), something outside the
sinus (the nasal mucosa's share during humming), or how the in-vivo numbers were measured. This narrows the NO model
rebuild (roadmap §0).
