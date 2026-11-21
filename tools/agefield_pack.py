"""Analyse a long agefield run (pages/agefield.template.html) and pack the sinus field for dist/hum-3d.html.

Run: python tools/agefield_pack.py results/lbm/fict_max_040_150hz geometry/fict_max_040 [max_cycle]
- prints the fresh-air fraction of the whole sinus and of its near/far halves (split by volume at the distance from
  the ostium, as the page's colouring), the per-cycle mixing efficiency over time, and the two-compartment model
  of the pages run with the 3D run's own initial exchange rate;
- writes <run>/field.bin.gz (uint8 fresh fraction 0..254, 255 = outside the sinus, 2x2x2 blocks of the 0.4 mm grid)
  and <run>/field.json (grid origin and step in page millimetres, snapshot cycles and their whole-sinus fresh share).
numpy only.
"""
import sys, os, json, gzip, glob
import numpy as np

run, geo = sys.argv[1], sys.argv[2]
MAXC = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9   # snapshots after this cycle are not packed (numerics, see results)
info = json.load(open(geo + '.json', encoding='utf-8'))
nx, ny, nz = info['dims']; dx = info['dx']; an = info.get('anat')   # page coordinates (fictional shapes only)
mask = np.frombuffer(gzip.open(geo + '.bin.gz').read(), np.uint8).reshape(nz, ny, nx).transpose(2, 1, 0)
cyc = json.load(open(os.path.join(run, 'cycles.json'), encoding='utf-8'))
meta, log = cyc['meta'], np.array(cyc['log'], float)
f_hz = meta['C']['f']
sin = mask == 2
ii, jj, kk = np.nonzero(sin)
A = np.array(info['A'])
dist = np.sqrt((ii - A[0]) ** 2 + (jj - A[1]) ** 2 + (kk - A[2]) ** 2)
near = dist <= np.median(dist)

snaps = []
for p in sorted(glob.glob(os.path.join(run, 'snap_*.u8'))):
    n = int(os.path.basename(p)[5:9])
    if n > MAXC: continue
    u = np.frombuffer(open(p, 'rb').read(), np.uint8).reshape(nz, ny, nx).transpose(2, 1, 0)
    fresh = 1 - u[sin].astype(np.float32) / 254
    snaps.append((n, fresh))

# two-compartment model of the pages with the 3D run's own exchange rate in the first frozen cycles
fz = log[log[:, 4] == 1]
C = np.concatenate([[1.0], log[:, 2]])
e0 = np.mean(1 - fz[:20, 2] / np.concatenate([[C[int(fz[0, 0])]], fz[:19, 2]]))     # fraction exchanged per cycle
k = e0 * f_hz
def two(t, fn=0.5, tau=40.0):
    a, b = 1 / tau / (1 - fn), 1 / tau / fn; n_, fa = 1.0, 1.0; h = 0.01
    for _ in range(int(round(t / h))): dn = -(k / fn) * n_ + b * (fa - n_); df = a * (n_ - fa); n_ += h * dn; fa += h * df
    return n_, fa
print(f"run {os.path.basename(run)}: {f_hz:.0f} Hz, L0/d {meta['L0d']:.3f}, Re {meta['Re']}, {len(log)} cycles in {meta['seconds']:.0f} s")
print(f"exchange per cycle at the start {e0 * 100:.4f} % -> k = {k:.4f} /s (one box: 10 s would give {(1 - np.exp(-10 * k)) * 100:.1f} %)")
print('\ncycle  time(s)  whole   near half  far half | two-compartment model: whole  near  far   | one box')
rows = []
for n, fr in snaps:
    t = n / f_hz; mn, mf = two(t)
    row = dict(cycle=n, t=t, whole=float(fr.mean()), near=float(fr[near].mean()), far=float(fr[~near].mean()),
               model_whole=1 - 0.5 * (mn + mf), model_near=1 - mn, model_far=1 - mf, one_box=float(1 - np.exp(-k * t)))
    rows.append(row)
    print(f"{n:5d}  {t:6.2f}   {row['whole'] * 100:5.1f}%   {row['near'] * 100:5.1f}%    {row['far'] * 100:5.1f}%  |"
          f"  {row['model_whole'] * 100:5.1f}%  {row['model_near'] * 100:5.1f}%  {row['model_far'] * 100:5.1f}%  | {row['one_box'] * 100:5.1f}%")
# per-cycle mixing efficiency over time (moving average of 50 cycles)
eta = log[:, 3]; idx = [50, 100, 200, 400, 700, 1000, 1500, 2000, 2500, len(log) - 1]
print('\nmixing efficiency (50-cycle mean) vs the start of the frozen run:')
e_start = np.mean(eta[int(fz[0, 0]):int(fz[0, 0]) + 50])
for i in idx:
    if i < len(log):
        m = np.mean(eta[max(0, i - 50):i]); print(f"  cycle {i:5d} ({i / f_hz:5.1f} s): eta {m:.3f} ({m / e_start:.2f} of the start)")

# pack: 2x2x2 blocks over the sinus bounding box (only for geometries with page coordinates)
if an is None: sys.exit(0)
lo = np.array([ii.min(), jj.min(), kk.min()]) // 2 * 2; hi = np.array([ii.max(), jj.max(), kk.max()]) + 2
sub = [slice(lo[a], hi[a]) for a in range(3)]
ms = sin[tuple(sub)]
shape = [(hi[a] - lo[a] + 1) // 2 for a in range(3)]
def block(v):
    out = np.zeros([s * 2 for s in shape], np.float32); out[:v.shape[0], :v.shape[1], :v.shape[2]] = v
    return out.reshape(shape[0], 2, shape[1], 2, shape[2], 2).sum(axis=(1, 3, 5))
cnt = block(ms.astype(np.float32))
packed = []
for n, fr in snaps:
    full = np.zeros(mask.shape, np.float32); full[sin] = fr
    s = block(full[tuple(sub)] * ms)
    q = np.where(cnt >= 4, np.round(np.clip(s / np.maximum(cnt, 1), 0, 1) * 254), 255).astype(np.uint8)
    packed.append(np.ascontiguousarray(q.transpose(2, 1, 0)))    # index = (z*sy + y)*sx + x
blob = np.concatenate([p.ravel() for p in packed]).tobytes()
with gzip.open(os.path.join(run, 'field.bin.gz'), 'wb', compresslevel=9) as f: f.write(blob)
# page millimetres of voxel (0,0,0) centre: grid -> x = x0 + i dx, y = y_front - j dx, z = z0 + k dx; block centre = +0.5 cell
step = 2 * dx
origin = [an['x0'] + (lo[0] + 0.5) * dx, an['y_front'] - (lo[1] + 0.5) * dx, an['z0'] + (lo[2] + 0.5) * dx]
out = dict(what='fresh-air fraction in the sinus, uint8 0..254 (255 outside), snapshots concatenated; voxel (i,j,k) at '
                'x = origin[0] + i*step, y = origin[1] - j*step, z = origin[2] + k*step (page mm)',
           dims=[int(v) for v in shape], step=float(step), origin=[float(v) for v in origin], snaps=[r['cycle'] for r in rows], whole=[round(r['whole'], 4) for r in rows],
           run=os.path.basename(run), f_hz=f_hz, L0d=meta['L0d'], k_per_s=k, sinus_centre_mm=info['sinus_centre_mm'],
           sinus_scale=info['sinus_scale'], ostium_mm=info['ostium_mm'], rows=rows)
json.dump(out, open(os.path.join(run, 'field.json'), 'w', encoding='utf-8'), indent=1)
print(f"\npacked {len(packed)} snapshots of {shape} voxels ({step} mm): {os.path.getsize(os.path.join(run, 'field.bin.gz'))} bytes gzip")
