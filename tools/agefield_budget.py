"""Scalar budget of an agefield run: old-air content (mL) of the sinus, ostium tube and nasal cavity per snapshot.

With the through-flow switched off (?ch=0) the total should stay nearly constant (the only sink is diffusion into
the inlet cells, held at c = 0); a falling total would mean the advection scheme loses scalar.
Run: python tools/agefield_budget.py results/lbm/<run> geometry/<geometry>
"""
import sys, os, json, gzip, glob
import numpy as np

run, geo = sys.argv[1], sys.argv[2]
info = json.load(open(geo + '.json', encoding='utf-8'))
nx, ny, nz = info['dims']; dv = info['dx'] ** 3 / 1000
lab = np.frombuffer(gzip.open(geo + '.bin.gz').read(), np.uint8)          # same (z, y, x) order as the snapshots
print('cycle   sinus mL   tube mL   nasal mL   total mL')
for p in sorted(glob.glob(os.path.join(run, 'snap_*.u8'))):
    u = np.frombuffer(open(p, 'rb').read(), np.uint8)
    fl = u != 255; c = np.where(fl, u.astype(np.float64) / 254, 0)
    s = c[lab == 2].sum() * dv; t = c[(lab == 0) & fl].sum() * dv; n = c[(lab == 1) | (lab == 3) | (lab == 4)].sum() * dv
    print(f"{int(os.path.basename(p)[5:9]):5d}   {s:8.3f}   {t:7.3f}   {n:8.3f}   {s + t + n:8.3f}")
