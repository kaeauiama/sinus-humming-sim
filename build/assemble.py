"""Assemble a self-contained HTML page from a template, the shared 3D LBM engine and a geometry.

Usage (run from the project root):
  python build/assemble.py integrated geometry/p001_040 dist/sinus3d-integrated.html
  python build/assemble.py rounding   geometry/p001_040 dist/verify-rounding.html
  python build/assemble.py integrated geometry/p001_080 test/out/int080.html   # coarse, for quick tests

The engine lives in engine/parts.json (extracted from legacy/sinus3d.src.html by build/extract.py).
Templates hold placeholders (/*CONSTS*/, /*WGSL*/, /*GPUVARS*/, /*CAMERA*/, /*FUNCS*/, /*LOADGEOM*/, /*MODEL*/,
/*INFO*/null and "/*B64*/") that are replaced here.
"""
import base64, json, os, sys
from patch_sync import patch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kind, geo, out = sys.argv[1], sys.argv[2], sys.argv[3]
p = json.load(open(os.path.join(ROOT, 'engine', 'parts.json'), encoding='utf-8'))

funcs = p['funcs']
# 1) the ostium slab must be a half-open window, or it is empty when the axis sits on half-integer coordinates;
#    and it must be tested on the exact axial coordinate t, not on the float32 tParam * len (whose rounding gives
#    0 or 2 layers for some tube lengths, e.g. 2 layers at len = 100: the flux is then counted twice)
for a, b in [("const tParam = new Float32Array(N).fill(-1);", "const tParam = new Float32Array(N).fill(-1), tAx = new Float64Array(N);"),
             ("if (m[i] === 0) { m[i] = 5; tParam[i] = Math.max(0, Math.min(1, t / len)); }",
              "if (m[i] === 0) { m[i] = 5; tParam[i] = Math.max(0, Math.min(1, t / len)); tAx[i] = t; }"),
             ("if (Math.abs(tParam[i] * len - len / 2) < 0.5) slab.push(k);",
              "{ const sm = tAx[i] - len / 2; if (sm >= -0.5 && sm < 0.5) slab.push(k); }")]:
    assert a in funcs, a
    funcs = funcs.replace(a, b)
# 2) lock drive-amplitude updates to cycle boundaries (see build/patch_sync.py)
funcs = patch(funcs)
# 3) HUD shows the open-ended cycle count
funcs = funcs.replace('`周期 ${Math.min(R.cycle + 1, CYCLES)}/${CYCLES}・位相', '`周期 ${R.cycle + 1}・位相')
consts = p['consts'].replace("|| 7)", "|| 18)")
# 4) WGSL: the fragment shader may not take a second @builtin(position)
wgsl = p['wgsl'].replace("fn fs(i: VO, @builtin(position) fc: vec4f) -> @location(0) vec4f {",
                         "fn fs(i: VO) -> @location(0) vec4f {\n  let fc = i.pos;")
assert wgsl != p['wgsl']

tpl_path = os.path.join(ROOT, 'pages', kind + '.template.html')
s = open(tpl_path, encoding='utf-8').read()
reps = [('/*CONSTS*/', consts), ('/*WGSL*/', wgsl), ('/*GPUVARS*/', p['gpuvars']), ('/*CAMERA*/', p['camera'])]
if kind == 'integrated':
    reps += [('/*LOADGEOM*/', p['loadGeometry']), ('/*FUNCS*/', funcs)]
elif kind == 'agefield':
    # long runs that save the scalar field: a hook right after each cycle end (pages/agefield.template.html)
    a = "R.cycle++; R.stepInCycle = 0; R.wait = true;"
    assert funcs.count(a) == 1, a
    funcs = funcs.replace(a, a + " { const h = snapHook(enc, R.cycle - 1); if (h) after.push(h); }")
    # finer grids (0.2 mm: ~2.8 M fluid cells, 19 * 4 * nf ~ 210 MB per buffer) need more than the 420k-cell
    # request of the engine; the device is made before the geometry is read, so ask for what the adapter allows
    a = "const need = 19 * 4 * 420000;"
    assert funcs.count(a) == 1, a
    funcs = funcs.replace(a, "const need = Math.min(adapter.limits.maxStorageBufferBindingSize, adapter.limits.maxBufferSize);")
    # the sinus scalar sum is fixed point (c * 4096) in one u32: it wraps above ~1.05 M sinus cells (0.2 mm has
    # 1.6 M). Carry into a second word; the JS side adds it back.
    a = "if (li == 0u) { atomicAdd(&csum[0], acc[0]); }"
    assert wgsl.count(a) == 1, a
    wgsl = wgsl.replace(a, "if (li == 0u) { let old = atomicAdd(&csum[0], acc[0]); if (old + acc[0] < old) { atomicAdd(&csum[1], 1u); } }")
    a = "onCycle(cycle, st[0], st[1], cs[0] / FIX);"
    assert funcs.count(a) == 1, a
    funcs = funcs.replace(a, "onCycle(cycle, st[0], st[1], (cs[0] + cs[1] * 4294967296) / FIX);")
    reps[1] = ('/*WGSL*/', wgsl)
    reps += [('/*LOADGEOM*/', p['loadGeometry']), ('/*FUNCS*/', funcs)]
elif kind == 'rounding':
    # the rounding page brings its own buildFluid (with edge fillets); drop the engine's copy
    i = funcs.index('function buildFluid('); j = funcs.index('async function checkShader')
    reps += [('/*FUNCS*/', funcs[:i] + funcs[j:])]
    # it also reuses the lumped + NO model code of the integrated page
    integ = open(os.path.join(ROOT, 'pages', 'integrated.template.html'), encoding='utf-8').read()
    a = integ.index('// ---------------- lumped resonance'); b = integ.index('let lastLump = null;')
    c = integ.index('// ---------------- NO model'); d = integ.index('// ---------------- pipeline')
    reps += [('/*MODEL*/', integ[a:b] + integ[c:d])]
else:
    raise SystemExit('unknown page kind: ' + kind)
for k, v in reps:
    assert k in s, k
    s = s.replace(k, v, 1)
info = open(os.path.join(ROOT, geo + '.json'), encoding='utf-8').read().strip()
b64 = base64.b64encode(open(os.path.join(ROOT, geo + '.bin.gz'), 'rb').read()).decode()
s = s.replace('/*INFO*/null', info, 1).replace('"/*B64*/"', '"' + b64 + '"', 1)
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
# newline='\n': text mode on Windows would otherwise write CRLF, and dist/ must match byte for byte
with open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)
print('wrote', out, os.path.getsize(out), 'bytes')
