"""Build the P001 maxillary-sinus + nasal-cavity lattice mask from NasalSeg labels.
Usage: python geometry/build_geom.py [DX_mm=0.4] [path/to/P001_seg.nrrd]
Needs numpy, scipy, pynrrd. Label mapping found by centroid: 1,2 = maxillary sinuses, 3,4 = nasal cavities, 5 = nasopharynx."""
import sys, os, json, gzip, numpy as np, nrrd
HERE = os.path.dirname(os.path.abspath(__file__))
from scipy import ndimage as ndi
DX = float(sys.argv[1]) if len(sys.argv) > 1 else 0.4
# NasalSeg labels, e.g. extracted from ../../nasalseg-work/labels_and_3imgs.tgz (labels/P001_seg.nrrd)
src = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', '..', 'nasalseg-work', 'labels', 'P001_seg.nrrd')
L, h = nrrd.read(src)
sp = np.abs(np.diag(np.array(h['space directions'], float)))
SIN, NAS = 2, 4
# natural ostium (voxel coords in source), found from the CT air bridge
ost_sinus = np.array([104.5, 85.5, 34.6]); ost_nasal = np.array([101.0, 85.5, 34.6])
# crop box in source voxel coords (inclusive), mm-sized margins
x0, x1 = 74, 149; y0, y1 = 50, 122; z0, z1 = 10, 47
def mm(v): return np.asarray(v) * sp
lo = mm([x0, y0, z0]); hi = mm([x1, y1, z1])
size = hi - lo
dims = np.ceil(size / DX).astype(int) + 1
print('grid', dims, 'cells', dims.prod())
# smooth indicator functions, sampled on the isotropic grid
def field(m):
    m = m.astype(np.float32)
    sig = 0.5 / sp  # 0.5 mm gaussian
    return ndi.gaussian_filter(m, sigma=sig)
fS = field(ndi.label(L == SIN)[0] == np.argmax(np.bincount(ndi.label(L == SIN)[0].ravel())[1:]) + 1)
fN = field(L == NAS)
gx = lo[0] + np.arange(dims[0]) * DX; gy = lo[1] + np.arange(dims[1]) * DX; gz = lo[2] + np.arange(dims[2]) * DX
X, Y, Z = np.meshgrid(gx / sp[0], gy / sp[1], gz / sp[2], indexing='ij')
coords = np.stack([X, Y, Z])
S = ndi.map_coordinates(fS, coords, order=1) > 0.5
N = ndi.map_coordinates(fN, coords, order=1) > 0.5
# keep largest connected components
def largest(m):
    lab, n = ndi.label(m)
    if n == 0: return m
    c = np.bincount(lab.ravel()); c[0] = 0
    return lab == np.argmax(c)
S = largest(S)
# enforce a solid wall of >= 2 cells between sinus and nasal cavity
wall = ndi.binary_dilation(S, iterations=2) & ~S
N = N & ~wall & ~S
# inlet / outlet: nasal cells on the posterior (max y) and anterior (min y) faces
N = largest(N)
mask = np.zeros(dims, np.uint8)   # 0 solid, 1 nasal fluid, 2 sinus fluid, 3 inlet, 4 outlet
mask[N] = 1; mask[S] = 2
mask[:, -1, :][mask[:, -1, :] == 1] = 3   # posterior face -> inlet (exhalation flows anteriorly)
mask[:, 0, :][mask[:, 0, :] == 1] = 4     # anterior face -> outlet
# outer boundary of box other than in/out faces is solid
for sl in [(0, slice(None), slice(None)), (-1, slice(None), slice(None)), (slice(None), slice(None), 0), (slice(None), slice(None), -1)]:
    mask[sl] = 0
a = mm(ost_sinus) - lo; b = mm(ost_nasal) - lo
A = (a / DX).tolist(); B = (b / DX).tolist()
info = dict(dims=dims.tolist(), dx=DX, A=A, B=B,
            sinus_ml=float(S.sum() * DX**3 / 1000), nasal_ml=float(N.sum() * DX**3 / 1000),
            inlet_cells=int((mask == 3).sum()), outlet_cells=int((mask == 4).sum()),
            source='NasalSeg P001 (Zhang et al., Sci Data 2024, CC BY 4.0): labels 2 (maxillary sinus) and 4 (nasal cavity), resampled, cropped and with a carved ostium')
print(json.dumps(info, indent=1))
# check the gap at the ostium in the resampled grid
seg = [np.round(np.array(A) + (np.array(B) - np.array(A)) * t).astype(int) for t in np.linspace(-0.3, 1.3, 12)]
print('mask along ostium axis', [int(mask[tuple(p)]) for p in seg])
# store layout: z-major (index = (z*ny + y)*nx + x)
raw = np.ascontiguousarray(mask.transpose(2, 1, 0)).tobytes()
with gzip.open(os.path.join(HERE, f'p001_{int(DX*100):03d}.bin.gz'), 'wb', compresslevel=9) as f: f.write(raw)
json.dump(info, open(os.path.join(HERE, f'p001_{int(DX*100):03d}.json'), 'w'))
np.save(os.path.join(HERE, 'mask_preview.npy'), mask)
