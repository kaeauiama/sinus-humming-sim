"""Does closing or narrowing a nostril change the sound pressure at the sinus ostia during humming [m]?

Uses the 1D vocal/nasal tract model of tools/ostium_pressure.py (ported from sinus-rescue), but splits the nasal
cavity into a left and a right passage after the velopharyngeal port (the septum runs from the choanae to the
nostrils), each with one maxillary and one sphenoid side branch and its own nostril. The glottal source is the same
in every case (same vocal effort), so the numbers compare the pressure at each ostium with both nostrils open.

Cases: both open; one closed (rigid end); one narrowed to a quarter of its area; both closed.
Both closed cannot be held: the exhaled air has nowhere to go. One closed side also loses the exhaled through-flow
that renews the air next to its ostia (see results/nostril_occlusion.md).
Run: python tools/nostril_occlusion.py  -> results/nostril_occlusion.json and a printed summary.
"""
import json, os
import numpy as np
from ostium_pressure import (tube, radiation, parallel, Sinus, zin, forward, ORAL_M, PHARYNX,
                             LOSS_NASAL, CM, CM2, GLOTTAL_R)

PORT = tube(1 * CM, 1.0 * CM2, LOSS_NASAL)

def side_chain(narrow=1.0):
    """One nasal passage (half the areas of the lumped model), as in ostium_pressure.nasal_chain()."""
    s = 0.5
    mx, sp = Sinus('maxillary', 15e-6, 4e-6, 6e-3), Sinus('sphenoid', 4e-6, 3e-6, 4e-3)
    ch = tube(2.5 * CM, 2.5 * CM2 * s, LOSS_NASAL) + [('probe', 'sph'), ('sinus', sp)]
    ch += tube(1.0 * CM, 2.5 * CM2 * s, LOSS_NASAL) + [('probe', 'eth_post')]
    ch += tube(2.0 * CM, 2.5 * CM2 * s, LOSS_NASAL) + [('probe', 'max'), ('sinus', mx)]
    ch += tube(0.5 * CM, 2.5 * CM2 * s, LOSS_NASAL) + [('probe', 'eth_ant')]
    ch += tube(0.5 * CM, 2.5 * CM2 * s, LOSS_NASAL) + [('probe', 'fro')]
    ch += tube(2.0 * CM, 2.5 * CM2 * s, LOSS_NASAL)
    ch += tube(0.75 * CM, 1.2 * CM2 * s, LOSS_NASAL) + [('wall', 5 * CM2 * s)] + tube(0.75 * CM, 1.2 * CM2 * s * narrow, LOSS_NASAL)
    return ch

def end_z(state, f):
    """nostril termination: 'open', 'closed' or a narrowing factor of the nostril area"""
    if state == 'closed': return 1e14
    return radiation(1.2 * CM2 * 0.5 * (1.0 if state == 'open' else state), f)

def solve(left, right, f):
    chL = side_chain(1.0 if left in ('open', 'closed') else left)
    chR = side_chain(1.0 if right in ('open', 'closed') else right)
    zL, zR = zin(chL, end_z(left, f), f), zin(chR, end_z(right, f), f)
    z_na = zin(PORT, parallel(zL, zR), f)
    z_or = zin(ORAL_M, 1e14, f)
    z_gl = zin(PHARYNX, parallel(z_or, z_na), f)
    u_gl = GLOTTAL_R / (GLOTTAL_R + z_gl); p_gl = u_gl * z_gl
    _, p_j = forward(PHARYNX, p_gl, u_gl, f)
    _, p_s = forward(PORT, p_j, p_j / z_na, f)          # pressure where the two passages split
    prL, _ = forward(chL, p_s, p_s / zL, f)
    prR, _ = forward(chR, p_s, p_s / zR, f)
    return {k: abs(v) for k, v in prL.items()}, {k: abs(v) for k, v in prR.items()}

CASES = [('both open', 'open', 'open'), ('left closed', 'closed', 'open'), ('left narrowed to 1/4', 0.25, 'open'),
         ('both closed', 'closed', 'closed')]
FREQS = [100, 130, 150, 200, 250, 300, 400, 600]

def main():
    base = {f: solve('open', 'open', f)[0] for f in FREQS}
    out = {'what': 'pressure at each ostium / the same ostium with both nostrils open; same glottal source (tools/nostril_occlusion.py)',
           'freqs_hz': FREQS, 'cases': {}}
    for name, l, r in CASES:
        rec = {'left': {}, 'right': {}}
        for f in FREQS:
            pl, pr = solve(l, r, f)
            for side, p in (('left', pl), ('right', pr)):
                for k, v in p.items(): rec[side].setdefault(k, []).append(round(v / base[f][k], 3))
        out['cases'][name] = rec
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results', 'nostril_occlusion.json')
    json.dump(out, open(path, 'w', encoding='utf-8'), indent=1)
    print('pressure at the maxillary ostium relative to both nostrils open (same voice):')
    print('  case                    side    ' + ''.join(f'{f:>7d}' for f in FREQS))
    for name, rec in out['cases'].items():
        for side in ('left', 'right'):
            if name == 'both open' and side == 'right': continue
            print(f'  {name:22s}  {side:6s}  ' + ''.join(f'{v:7.2f}' for v in rec[side]['max']))
    print('\nother ostia at 150 Hz (left closed):', {k: v[FREQS.index(150)] for k, v in out['cases']['left closed']['left'].items()})
    ref = solve('open', 'open', 150)[0]['max']
    tr = {f: round(solve('open', 'open', f)[0]['max'] / ref, 3) for f in [100, 130, 150, 200, 250, 300, 400]}
    print('both open, same glottal source: maxillary ostium pressure relative to 150 Hz:', tr)
    out['both_open_vs_150hz'] = tr
    json.dump(out, open(path, 'w', encoding='utf-8'), indent=1)
    print('wrote', path)

if __name__ == '__main__':
    main()
