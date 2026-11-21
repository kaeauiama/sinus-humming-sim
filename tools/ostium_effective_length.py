"""Effective length of the carved P001 ostium (roadmap: real geometry mixes more than the ideal-geometry law).

The pages carve a cylinder of diameter d along A -> B (geometry/p001_040.json) through the CT wall between the
maxillary sinus and the nasal cavity; its nominal length |AB| is 2.05 mm. If the wall around the hole is thinner than
that, or the cylinder's rim breaks into a cavity sideways, the part of the tube that is really enclosed by bone is
shorter. Here, for each axial position, we sample a ring just outside the hole (radius r + 0.5 ... r + 1.5 cells) in the
base mask and record how much of it is solid. The enclosed length = axial extent where >= 50 % of the ring is solid.
Then we ask which ostium length the mixing law needs to reproduce the measured 3D mixing (E2 and the integrated page).
Run: python tools/ostium_effective_length.py   (numpy only)
"""
import gzip, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
info = json.load(open(os.path.join(ROOT, 'geometry', 'p001_040.json')))
nx, ny, nz = info['dims']; dx = info['dx']
mask = np.frombuffer(gzip.open(os.path.join(ROOT, 'geometry', 'p001_040.bin.gz')).read(), np.uint8).reshape(nz, ny, nx)
A = np.array(info['A']); B = np.array(info['B'])
ax = B - A; L = np.linalg.norm(ax); a = ax / L
# two unit vectors perpendicular to the axis
tmp = np.array([0.0, 0.0, 1.0]) if abs(a[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
u = np.cross(a, tmp); u /= np.linalg.norm(u); v = np.cross(a, u)

def val(p):  # nearest-cell mask value at grid point p = (x, y, z)
    x, y, z = np.round(p).astype(int)
    if not (0 <= x < nx and 0 <= y < ny and 0 <= z < nz): return 0
    return mask[z, y, x]

MIX = dict(m=0.695, x0=1.68, n=1.76, k=1.15, p=0.57, lam=48.0)
sat = lambda v, v0, n: 1 - math.exp(-max(v, 0) / v0 if n == 1 else -(max(v, 0) / v0) ** n) if False else 1 - math.exp(-(max(v, 0) / v0) ** n)
law = lambda x, ld: MIX['m'] * sat(x, MIX['x0'], MIX['n']) * sat(x * ld, MIX['k'], MIX['p']) * math.exp(-ld / MIX['lam'])

print(f'nominal ostium A->B: {L:.2f} cells = {L * dx:.2f} mm, axis {np.round(a, 3)}')
for dmm in [2.0, 2.8, 4.0]:
    r = dmm / 2 / dx
    rows, encl = [], []
    for s in np.arange(-4.0, L + 4.0 + 1e-9, 0.25):
        c = A + s * a; tot = sol = sin = nas = 0
        for rho in np.arange(r + 0.5, r + 1.51, 0.5):
            for th in np.linspace(0, 2 * math.pi, 48, endpoint=False):
                m = val(c + rho * (math.cos(th) * u + math.sin(th) * v)); tot += 1
                sol += m == 0; sin += m == 2; nas += m in (1, 3, 4)
        rows.append((s, sol / tot, sin / tot, nas / tot))
        if sol / tot >= 0.5: encl.append(s)
    # contiguous enclosed run that overlaps the nominal tube
    Le = (max(encl) - min(encl) + 0.25) if encl else 0.0
    print(f'\nd = {dmm} mm (r = {r:.1f} cells): enclosed (>=50 % solid ring) from s = {min(encl) if encl else float("nan"):.2f} to {max(encl) if encl else float("nan"):.2f} cells -> {Le * dx:.2f} mm (nominal {L * dx:.2f} mm)')
    print('   s(cells)  solid  sinus  nasal')
    for s, so, si, na in rows[::2]:
        print(f'   {s:7.2f}   {so:4.2f}   {si:4.2f}   {na:4.2f}')

# which length does the law need to match the measured 3D mixing?
cases = [('E2 100 Pa', 2.0, 7.24, 0.56), ('E2 100 Pa', 2.8, 3.51, 0.36), ('E2 100 Pa', 4.0, 1.67, 0.16),
         ('integrated 100 Pa', 2.8, 3.25, 0.35), ('integrated 200 Pa', 2.8, 7.21, 0.50)]
print('\nlength the law needs (L0 = stroke in mm, eta = 3D):')
for name, d, L0, eta in cases:
    nominal = law(L0 / 2.1, 2.1 / d)
    sols = []
    prev = None
    for Lm in np.arange(0.2, 6.0, 0.01):
        val_ = law(L0 / Lm, Lm / d) - eta
        if prev is not None and np.sign(val_) != np.sign(prev): sols.append(Lm)
        prev = val_
    print(f'  {name:18s} d {d} mm, L0 {L0:.2f} mm: 3D {eta:.2f}, law at 2.1 mm {nominal:.2f}; law matches 3D at L = {", ".join(f"{x:.2f}" for x in sols) or "none"} mm')
