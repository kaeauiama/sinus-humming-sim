"""Does NO coming from the sinus wall (not from the air) make its concentration uneven enough to matter?
Order-of-magnitude estimates for the maxillary sinus of the pages. Run: python tools/no_wall_source.py
"""
import numpy as np

V = 12.75e-6                     # m^3
a = (3 * V / (4 * np.pi)) ** (1 / 3)   # radius of the equal-volume sphere
D = 2.0e-5                       # NO in air, m^2/s
tau_rec = 270.0                  # s, refill time constant of the pages (Menzel 2005)
k = 1 / tau_rec
area = 4 * np.pi * a ** 2

# 1) quiet state: wall production balanced by a loss spread through the air (worst case for unevenness)
#    D lap c = k c in a sphere, flux in at the wall: c(r) ~ sinh(lr)/r, l = sqrt(k/D)
lam = np.sqrt(k / D)
r = np.linspace(1e-6, a, 2001); c = np.sinh(lam * r) / r
uneven = c[-1] / c[0] - 1
tau_diff = a ** 2 / (np.pi ** 2 * D)   # slowest diffusion mode of a sphere
print(f'equal-volume sphere: radius {a * 1e3:.1f} mm, wall {area * 1e4:.1f} cm^2')
print(f'slowest diffusion mode a^2/(pi^2 D) = {tau_diff:.2f} s, vs the production/loss time {tau_rec:.0f} s')
print(f'quiet state, loss spread through the air: wall vs centre differ by {uneven * 100:.2f} %')
print('quiet state, loss at the wall too (re-uptake): no gradient at all apart from the ostium')

# 2) during a 10-s hum: how much NO the wall adds, relative to what the sinus holds at rest
for T in (5, 10, 30):
    print(f'NO added by the wall in {T:2d} s of humming: {T / tau_rec * 100:.1f} % of the resting content')

# 3) could the mucosa store NO and release it slowly? capacity of a wet layer of thickness h
henry = 1.9e-3               # mol/(L atm), NO in water at 25 C
gas = 1 / (0.08206 * 298)    # mol/L of an ideal gas at 1 atm
part = henry / gas           # dimensionless water/air partition
for h_um in (10, 100, 300):
    cap = area * h_um * 1e-6 * part / V
    print(f'wet layer {h_um:3d} um: holds {cap * 100:.3f} % of the NO in the sinus air (partition {part:.3f})')
# 4) the ostium wall is right in the path but tiny
ost = np.pi * 2.8e-3 * 2.1e-3
print(f'ostium wall {ost * 1e6:.0f} mm^2 = {ost / area * 100:.2f} % of the sinus wall')
