"""Extract the shared 3D LBM engine pieces from legacy/sinus3d.src.html into engine/parts.json.
NOTE: parts.json also carries a hand-added `loadGeometry` entry; re-running this drops it (see docs/methods.md)."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'legacy', 'sinus3d.src.html'), encoding='utf-8').read()
js = src[src.index("(() => {\n'use strict';"):]
def block(start, end):
    a = js.index(start); b = js.index(end, a)
    return js[a:b]
def func(name):
    m = re.search(r'\n(async )?function ' + re.escape(name) + r'\(', js)
    i = m.start() + 1
    j = js.index('{', i); depth = 0; k = j
    while True:
        ch = js[k]
        if ch == '{': depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0: break
        k += 1
    return js[i:k + 1] + '\n'
parts = {}
parts['consts'] = block("// ---------------- D3Q19 ----------------", "// ---------------- geometry ----------------")
parts['wgsl'] = block("// ---------------- WGSL ----------------", "// ---------------- GPU ----------------")
parts['gpuvars'] = block("// ---------------- GPU ----------------", "async function checkShader")
parts['camera'] = block("// ---------------- camera ----------------", "function writeRender")
fn = ''
for n in ['buildFluid', 'checkShader', 'initGPU', 'setupBuffers', 'writeUniform', 'resetFlow', 'resetScalar', 'encodeSteps', 'encodeCycleEnd', 'writeRender', 'sizeCanvas', 'frame']:
    fn += func(n)
parts['funcs'] = fn
json.dump(parts, open(os.path.join(ROOT, 'engine', 'parts.json'), 'w', encoding='utf-8'))
for k, v in parts.items(): print(k, len(v))
