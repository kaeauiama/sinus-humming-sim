"""Fictional maxillary sinus + middle meatus of dist/hum-3d.html as a grid for the 3D LBM engine.

Same shapes as the page (maxSDF(1) and nasal(), anatomical mm: x left-right, y forward, z up), the sinus scaled to
12.75 mL on this grid and moved along the ostium axis so that the bony ostium is L_TARGET long. Grid layout as
geometry/build_geom.py: labels 0 solid, 1 nasal fluid, 2 sinus fluid, 3 inlet, 4 outlet; the engine carves the
ostium cylinder from A (sinus side) to B (nasal side). The engine drives the exhaled flow along -y of the grid, so
grid j runs from the front (j = 0, outlet) to the back (inlet): j = (Y_FRONT - y) / dx.

Run: python geometry/build_fict.py 0.4   (or 0.8 for a quick test) -> geometry/fict_max_040.{bin.gz,json}
numpy only.
"""
import sys, os, json, gzip
import numpy as np

DX = float(sys.argv[1]) if len(sys.argv) > 1 else 0.4
HERE = os.path.dirname(os.path.abspath(__file__))
V_TARGET, L_TARGET, D_OST = 12.75, 2.1, 2.8          # mL, mm, mm (dist/hum-3d.html DIM.max)
START, DIR = np.array([24.0, 20.0, 2.0]), np.array([-1.0, 0.0, 0.1]) / np.hypot(1.0, 0.1)   # as the page's ostPath
X0, X1, Y_BACK, Y_FRONT, Z0, Z1 = 0.4, 44.0, 0.8, 39.2, -23.6, 13.6       # domain, mm
CAV_Z = (-20.0, 12.0)                                                     # nasal crop: closed floor and lid

def ln(x, y, z): return np.sqrt(x * x + y * y + z * z)
def sd_ell(x, y, z, rx, ry, rz):
    k0 = ln(x / rx, y / ry, z / rz); k1 = ln(x / (rx * rx), y / (ry * ry), z / (rz * rz))
    return np.where(k1 > 1e-9, k0 * (k0 - 1) / np.maximum(k1, 1e-9), -np.minimum(np.minimum(rx, ry), rz))
def sd_taper(x, y, z, a, b, ra, rb):
    bx, by, bz = b[0] - a[0], b[1] - a[1], b[2] - a[2]; px, py, pz = x - a[0], y - a[1], z - a[2]
    t = np.clip((px * bx + py * by + pz * bz) / (bx * bx + by * by + bz * bz), 0, 1)
    return ln(px - t * bx, py - t * by, pz - t * bz) - (ra + (rb - ra) * t)
def sd_rbox(x, y, z, hx, hy, hz, r):
    qx, qy, qz = np.abs(x) - hx, np.abs(y) - hy, np.abs(z) - hz
    return ln(np.maximum(qx, 0), np.maximum(qy, 0), np.maximum(qz, 0)) + np.minimum(np.maximum(np.maximum(qx, qy), qz), 0) - r
def smin(a, b, k): h = np.maximum(k - np.abs(a - b), 0) / k; return np.minimum(a, b) - h * h * k * 0.25
def smax(a, b, k): return -smin(-a, -b, k)
# nasal cavity of pages/hum3d.template.html (2026-11-22 anatomical version; nasopharynx and nostrils are outside this grid)
NW_Z, NW_W = [-22, -15, -5, 4, 10, 16, 20, 24], [10, 12.5, 13, 14, 11.5, 7.5, 4.2, 3.2]
NA_Y, NA_A = [-30, -22, 28, 46, 54, 64], [0.85, 1, 1, 0.62, 0.78, 0.78]
NR_Y, NR_Z = [-26, -21, 22, 56], [6, 24, 24, 0]
NF_Y, NF_Z = [-30, 48, 62], [-22, -22, -18]
def wallX(y, z): return np.interp(z, NW_Z, NW_W) * np.interp(y, NA_Y, NA_A)
def septDev(y, z): return 0.7 * np.sin((y - 8) * 0.075) * np.exp(-((z + 6) / 13) ** 2)
TURB = [dict(yc=12, hy=30, za=-8, zb=-18, gap=1.6, rb=3.6, t=1.6), dict(yc=16, hy=24, za=8.5, zb=-0.5, gap=1.5, rb=2.3, t=1.2),
        dict(yc=-6, hy=13, za=18.5, zb=13, gap=0.6, rb=1.2, t=1.0)]
def turbinate(ax, y, z, T):
    bx = 1.1 + T['gap'] + T['rb']; bz = (T['za'] + T['zb']) / 2
    body = sd_ell(ax - bx, y - T['yc'], z - bz, T['rb'], T['hy'], (T['za'] - T['zb']) / 2)
    xw = wallX(y, T['za']) + 1
    lam = sd_rbox(ax - (bx + xw) / 2, y - T['yc'], z - (T['za'] - T['t'] / 2), (xw - bx) / 2, T['hy'] * 0.9, T['t'] / 2, 0.4)
    return smin(body, lam, 1.2)
def nasal(x, y, z):
    dv = septDev(y, z); a_s = np.abs(x - dv); ax = np.abs(x)
    d = 1.1 - a_s
    d = smax(d, ax - wallX(y, z), 2)
    d = smax(d, np.interp(y, NF_Y, NF_Z) - z, 3); d = smax(d, z - np.interp(y, NR_Y, NR_Z), 3)
    d = smax(d, y - 62, 3); d = smax(d, -26 - y, 2)
    t = np.minimum(np.minimum(turbinate(ax, y, z, TURB[0]), turbinate(ax, y, z, TURB[1])), turbinate(ax, y, z, TURB[2]))
    t = np.minimum(t, sd_ell(ax - wallX(y, 6), y - 11, z - 6, 3, 5, 2.8))
    d = smax(d, -t, 1.0)
    d = np.minimum(d, sd_taper(ax, y, z, [8, 49, 30], [8, 41, 12], 3.6, 6))
    return d
def max_sdf(x, y, z, c=(29.0, 20.0, -4.0)):
    X = x - c[0]; tp = 1 - 0.3 * np.maximum(X / 12, 0)
    return smin(sd_ell(X, y - c[1], z - c[2], 12, 16 * tp, 15 * tp), sd_ell(X + 1, y - c[1] - 4, z - c[2] + 11, 8, 10, 6), 5)

gx = X0 + np.arange(int(round((X1 - X0) / DX)) + 1) * DX
gy = Y_FRONT - np.arange(int(round((Y_FRONT - Y_BACK) / DX)) + 1) * DX
gz = Z0 + np.arange(int(round((Z1 - Z0) / DX)) + 1) * DX
X, Y, Z = np.meshgrid(gx, gy, gz, indexing='ij')
dims = np.array(X.shape)
print('grid', dims.tolist(), 'cells', int(dims.prod()))

def sinus_field(cen, s):
    # scaled about its own centre, as scaled() in the page
    return s * max_sdf(cen[0] + (X - cen[0]) / s, cen[1] + (Y - cen[1]) / s, cen[2] + (Z - cen[2]) / s, c=cen)
def point_sdf(p, cen, s):
    q = [np.array([cen[i] + (p[i] - cen[i]) / s]) for i in range(3)]
    return float(s * max_sdf(q[0], q[1], q[2], c=cen)[0])

cav_d = nasal(X, Y, Z)
cav = (cav_d < 0) & (Z > CAV_Z[0]) & (Z < CAV_Z[1])
cen = np.array([29.0, 20.0, -4.0]); s = 1.0
for it in range(4):
    for _ in range(3):   # volume
        S = sinus_field(cen, s) < 0
        s *= (V_TARGET / (S.sum() * DX ** 3 / 1000)) ** (1 / 3)
    S = sinus_field(cen, s) < 0
    # wall of >= 2 cells between sinus and nasal cavity (6-neighbour dilation twice, as build_geom.py)
    grow = S.copy()
    for _ in range(2):
        g = grow.copy()
        g[1:] |= grow[:-1]; g[:-1] |= grow[1:]; g[:, 1:] |= grow[:, :-1]; g[:, :-1] |= grow[:, 1:]; g[:, :, 1:] |= grow[:, :, :-1]; g[:, :, :-1] |= grow[:, :, 1:]
        grow = g
    N = cav & ~grow
    # ostium: leave the sinus along DIR from START, then the first nasal fluid cell
    p = START.copy(); ex = None
    for _ in range(4000):
        p = p + DIR * 0.02
        if ex is None:
            if point_sdf(p, cen, s) > 0: ex = p.copy()
        else:
            i = int(round((p[0] - X0) / DX)); j = int(round((Y_FRONT - p[1]) / DX)); k = int(round((p[2] - Z0) / DX))
            if N[i, j, k]: en = p.copy(); break
    gap = float(np.linalg.norm(en - ex))
    print(f'iteration {it}: scale {s:.4f}, sinus {S.sum() * DX ** 3 / 1000:.2f} mL, ostium length {gap:.2f} mm, centre x {cen[0]:.2f}')
    if abs(gap - L_TARGET) < 0.06: break
    cen = cen + DIR * (gap - L_TARGET)   # move the sinus toward the cavity along the axis
    START = START + DIR * (gap - L_TARGET)

mask = np.zeros(dims, np.uint8)
mask[N] = 1; mask[S] = 2
mask[:, -1, :][mask[:, -1, :] == 1] = 3     # back face -> inlet (exhalation flows forward = -y of the grid)
mask[:, 0, :][mask[:, 0, :] == 1] = 4       # front face -> outlet
for sl in [(0, slice(None), slice(None)), (-1, slice(None), slice(None)), (slice(None), slice(None), 0), (slice(None), slice(None), -1)]:
    mask[sl] = 0
# D3Q19 leak check: no sinus cell may have a nasal neighbour along any lattice link
EX = [1, -1, 0, 0, 0, 0, 1, -1, 1, -1, 0, 0, 1, -1, 1, -1, 0, 0]
EY = [0, 0, 1, -1, 0, 0, 1, -1, 0, 0, 1, -1, -1, 1, 0, 0, 1, -1]
EZ = [0, 0, 0, 0, 1, -1, 0, 0, 1, -1, 1, -1, 0, 0, -1, 1, -1, 1]
sin_, nas_ = mask == 2, (mask == 1) | (mask == 3) | (mask == 4)
leaks = sum(int((sin_ & np.roll(np.roll(np.roll(nas_, ex_, 0), ey_, 1), ez_, 2)).sum()) for ex_, ey_, ez_ in zip(EX, EY, EZ))
to_grid = lambda q: [(q[0] - X0) / DX, (Y_FRONT - q[1]) / DX, (q[2] - Z0) / DX]
A, B = to_grid(ex), to_grid(en)
info = dict(dims=dims.tolist(), dx=DX, A=A, B=B, sinus_ml=float((mask == 2).sum() * DX ** 3 / 1000), nasal_ml=float(nas_.sum() * DX ** 3 / 1000),
            inlet_cells=int((mask == 3).sum()), outlet_cells=int((mask == 4).sum()),
            source='fictional maxillary sinus and middle meatus of dist/hum-3d.html (geometry/build_fict.py)',
            anat=dict(x0=X0, y_front=Y_FRONT, z0=Z0, note='x = x0 + i dx, y = y_front - j dx, z = z0 + k dx (mm, page coordinates)'),
            sinus_centre_mm=cen.tolist(), sinus_scale=s, ostium_mm=dict(exit=ex.tolist(), entry=en.tolist(), length=gap, d=D_OST))
print(json.dumps({k: v for k, v in info.items() if k not in ('source',)}, indent=None))
print('lattice links from sinus to nasal fluid (must be 0):', leaks)
seg = [np.round(np.array(A) + (np.array(B) - np.array(A)) * t).astype(int) for t in np.linspace(-0.3, 1.3, 12)]
print('mask along ostium axis', [int(mask[tuple(q)]) for q in seg])
tag = f'fict_max_{int(round(DX * 100)):03d}'
raw = np.ascontiguousarray(mask.transpose(2, 1, 0)).tobytes()   # index = (z*ny + y)*nx + x
with gzip.open(os.path.join(HERE, tag + '.bin.gz'), 'wb', compresslevel=9) as f: f.write(raw)
json.dump(info, open(os.path.join(HERE, tag + '.json'), 'w', encoding='utf-8'))
print('wrote', tag)
