"""Field of view of the NasalSeg CT images (headers only, from ../NasalSeg.zip): voxel spacing and extent, to judge
whether the sphenoid, ethmoid and frontal sinuses are inside the images and resolvable.
Also: where the labelled structures sit in z, so we know how far above the maxillary sinus the image reaches.
Run: python tools/nasalseg_ct_extent.py
"""
import gzip, os, zipfile
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
z = zipfile.ZipFile(os.path.join(os.path.dirname(ROOT), 'NasalSeg.zip'))

def header(name):
    with z.open(name) as f: raw = f.read(3000)
    head = raw[:raw.find(b'\n\n')].decode('latin1')
    h = {}
    for line in head.splitlines()[1:]:
        if ':' in line and not line.startswith('#'):
            k, v = line.split(':', 1); h[k.strip().lower()] = v.strip()
    sizes = [int(s) for s in h['sizes'].split()]
    dirs = [[float(x) for x in v.strip('()').split(',')] for v in h['space directions'].replace(') (', ')|(').split('|')]
    sp = [abs(np.linalg.norm(d)) for d in dirs]
    return sizes, sp

rows = []
for n in sorted(x for x in z.namelist() if x.startswith('images/') and x.endswith('.nrrd')):
    sizes, sp = header(n)
    rows.append((os.path.basename(n).split('_')[0], sizes, sp, [s * p for s, p in zip(sizes, sp)]))
dz = np.array([r[2][2] for r in rows]); ez = np.array([r[3][2] for r in rows]); dxy = np.array([r[2][0] for r in rows])
print(f'{len(rows)} images')
print(f'in-plane spacing: median {np.median(dxy):.3f} mm (range {dxy.min():.3f}-{dxy.max():.3f})')
print(f'slice spacing:    median {np.median(dz):.2f} mm (range {dz.min():.2f}-{dz.max():.2f}); <= 1 mm in {np.sum(dz <= 1.0)} cases')
print(f'z extent:         median {np.median(ez):.0f} mm (range {ez.min():.0f}-{ez.max():.0f}); >= 100 mm in {np.sum(ez >= 100)} cases')
print(f'x/y extent:       median {np.median([r[3][0] for r in rows]):.0f} x {np.median([r[3][1] for r in rows]):.0f} mm')
# for the label of P001 and a few others: z range of maxillary sinus vs the top of the image
def zrange(case, lab):
    raw = z.read(f'labels/{case}_seg.nrrd'); i = raw.find(b'\n\n')
    hd = raw[:i].decode('latin1'); body = gzip.decompress(raw[i + 2:])
    sizes = [int(s) for s in [l for l in hd.splitlines() if l.startswith('sizes')][0].split(':')[1].split()]
    a = np.frombuffer(body, np.int16, count=int(np.prod(sizes))).reshape(sizes[::-1])   # z, y, x
    zz = np.where((a == lab).any(axis=(1, 2)))[0]
    return (zz.min(), zz.max(), sizes[2]) if len(zz) else None
print('\nmaxillary sinus (label 1) z-slices vs image height, a sample of cases:')
for case in ['P001', 'P020', 'P050', 'P080', 'P110', 'P130']:
    r = zrange(case, 1); sp = [x for x in rows if x[0] == case][0][2][2]
    if r: print(f'  {case}: maxillary slices {r[0]}-{r[1]} of {r[2]} -> {((r[2] - 1 - r[1]) * sp):.0f} mm of image above its top (slice {sp:.2f} mm)')
