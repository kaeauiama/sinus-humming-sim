"""Build dist/hum-3d.html from pages/hum3d.template.html and a packed 3D LBM run (tools/agefield_pack.py).

Usage (from the project root):
  python build/build_hum3d.py results/lbm/fict_max_040_150hz dist/hum-3d.html
  python build/build_hum3d.py none dist/hum-3d.html      # without the 3D field (two-compartment colouring only)
"""
import base64, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
run, out = sys.argv[1], sys.argv[2]
s = open(os.path.join(ROOT, 'pages', 'hum3d.template.html'), encoding='utf-8').read()
assert '/*AGEFIELD*/null' in s
if run != 'none':
    meta = json.load(open(os.path.join(ROOT, run, 'field.json'), encoding='utf-8'))
    keep = {k: meta[k] for k in ('dims', 'step', 'origin', 'snaps', 'whole', 'run', 'f_hz', 'L0d', 'sinus_centre_mm', 'sinus_scale')}
    keep['b64'] = base64.b64encode(open(os.path.join(ROOT, run, 'field.bin.gz'), 'rb').read()).decode()
    s = s.replace('/*AGEFIELD*/null', json.dumps(keep, separators=(',', ':')), 1)
with open(os.path.join(ROOT, out), 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)
print('wrote', out, os.path.getsize(os.path.join(ROOT, out)), 'bytes')
