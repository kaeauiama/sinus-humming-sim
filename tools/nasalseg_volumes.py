"""Maxillary sinus volumes of all NasalSeg cases (labels 1 and 2 = left/right maxillary sinus, found by centroid for
P001, docs/methods.md §4), read straight from ../NasalSeg.zip without unpacking. numpy only (no pynrrd).
Writes results/nasalseg_maxillary_volumes.csv and prints a summary.
Run: python tools/nasalseg_volumes.py [--header]   (--header: print the NRRD header of P001 and stop)
Data: NasalSeg, Zhang et al., Scientific Data 2024, CC BY 4.0, doi:10.5281/zenodo.13893419
"""
import gzip, io, os, sys, zipfile, zlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ZIP = os.path.join(os.path.dirname(ROOT), 'NasalSeg.zip')
DT = {'uchar': np.uint8, 'unsigned char': np.uint8, 'uint8': np.uint8, 'char': np.int8, 'signed char': np.int8, 'int8': np.int8,
      'short': np.int16, 'int16': np.int16, 'ushort': np.uint16, 'unsigned short': np.uint16, 'uint16': np.uint16,
      'int': np.int32, 'int32': np.int32, 'uint': np.uint32, 'unsigned int': np.uint32, 'uint32': np.uint32, 'float': np.float32, 'double': np.float64}

def read_nrrd(raw):
    i = raw.find(b'\n\n')
    head, body = raw[:i].decode('latin1'), raw[i + 2:]
    h = {}
    for line in head.splitlines()[1:]:
        if line.startswith('#') or ':' not in line: continue
        k, v = line.split(':', 1); h[k.strip().lower()] = v.strip().lstrip('=').strip()
    if h.get('encoding') in ('gzip', 'gz'): body = gzip.decompress(body)
    elif h.get('encoding') not in ('raw',): raise ValueError('encoding ' + h.get('encoding', '?'))
    dt = np.dtype(DT[h['type']])
    if dt.itemsize > 1 and h.get('endian', 'little') == 'big': dt = dt.newbyteorder('>')
    sizes = [int(s) for s in h['sizes'].split()]
    arr = np.frombuffer(body, dt, count=int(np.prod(sizes)))
    dirs = [[float(x) for x in v.strip('()').split(',')] for v in h['space directions'].replace(') (', ')|(').split('|') if v.strip() != 'none']
    vox = abs(np.linalg.det(np.array(dirs)))   # mm^3
    return h, arr, vox

z = zipfile.ZipFile(ZIP)
names = sorted(n for n in z.namelist() if n.startswith('labels/') and n.endswith('_seg.nrrd'))
if '--header' in sys.argv:
    raw = z.read(names[0]); print(raw[:raw.find(b'\n\n')].decode('latin1')); sys.exit()
rows = []
for n in names:
    h, arr, vox = read_nrrd(z.read(n))
    cnt = np.bincount(arr.astype(np.int64), minlength=6)
    case = os.path.basename(n).split('_')[0]
    rows.append((case, cnt[1] * vox / 1000, cnt[2] * vox / 1000, cnt[3] * vox / 1000, cnt[4] * vox / 1000, vox, h['sizes']))
out = os.path.join(ROOT, 'results', 'nasalseg_maxillary_volumes.csv')
with open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write('# Label volumes of NasalSeg (Zhang et al., Sci Data 2024, CC BY 4.0), counted from ../NasalSeg.zip by tools/nasalseg_volumes.py.\n')
    f.write('# label1/label2 = maxillary sinuses, label3/label4 = nasal cavities (assignment by centroid, checked on P001). mL.\n')
    f.write('case,label1_ml,label2_ml,label3_ml,label4_ml,voxel_mm3,sizes\n')
    for r in rows: f.write(f'{r[0]},{r[1]:.2f},{r[2]:.2f},{r[3]:.2f},{r[4]:.2f},{r[5]:.4f},{r[6].replace(" ", "x")}\n')
mx = np.array([v for r in rows for v in (r[1], r[2])])
nz = mx[mx > 0.05]
pct = lambda q: np.percentile(nz, q)
print(f'cases {len(rows)}, sinuses with label > 0.05 mL: {len(nz)} of {len(mx)}')
print(f'maxillary volume (mL): mean {nz.mean():.2f}  sd {nz.std(ddof=1):.2f}  median {np.median(nz):.2f}  10-90 % {pct(10):.1f}-{pct(90):.1f}  min {nz.min():.1f}  max {nz.max():.1f}')
print(f'left-right difference |l1 - l2| median {np.median([abs(r[1] - r[2]) for r in rows]):.2f} mL')
print('P001:', [f'{v:.2f}' for v in rows[0][1:5]], 'voxel', f'{rows[0][5]:.4f} mm3')
print('wrote', out)
