"""How uneven is the fresh air inside the sinus at each snapshot? (mean, spread, percentiles, distance bands)
Run: python tools/agefield_spread.py results/lbm/<run> geometry/<geometry>
"""
import sys, os, json, gzip, glob
import numpy as np

run, geo = sys.argv[1], sys.argv[2]
info = json.load(open(geo + '.json', encoding='utf-8'))
nx, ny, nz = info['dims']; dx = info['dx']
mask = np.frombuffer(gzip.open(geo + '.bin.gz').read(), np.uint8).reshape(nz, ny, nx).transpose(2, 1, 0)
sin = mask == 2
ii, jj, kk = np.nonzero(sin); A = np.array(info['A'])
dist = np.sqrt((ii - A[0]) ** 2 + (jj - A[1]) ** 2 + (kk - A[2]) ** 2) * dx
bands = np.percentile(dist, [0, 20, 40, 60, 80, 100])
print('distance bands from the ostium (mm):', ' | '.join(f'{a:.0f}-{b:.0f}' for a, b in zip(bands[:-1], bands[1:])))
print('cycle   mean   sd/mean   p10    p90  | mean fresh in each distance band (near -> far)')
for p in sorted(glob.glob(os.path.join(run, 'snap_*.u8'))):
    u = np.frombuffer(open(p, 'rb').read(), np.uint8).reshape(nz, ny, nx).transpose(2, 1, 0)
    fr = 1 - u[sin].astype(np.float64) / 254
    m = fr.mean(); b = [fr[(dist >= lo) & (dist <= hi)].mean() for lo, hi in zip(bands[:-1], bands[1:])]
    print(f"{int(os.path.basename(p)[5:9]):5d}  {m * 100:5.1f}%   {fr.std() / m:5.2f}   {np.percentile(fr, 10) * 100:5.1f}% {np.percentile(fr, 90) * 100:5.1f}% | " + ' '.join(f'{v * 100:5.1f}%' for v in b))
