"""Sound pressure at each sinus ostium relative to the maxillary ostium, during humming [m] with the nose open.

The calibrated effective pressure of the pages (130 Pa) refers to the maxillary ostium. The other ostia sit elsewhere
along the nasal cavity, and the open nostril is a pressure node, so they see different pressures. This computes
g_s(f) = |p at ostium s| / |p at the maxillary ostium| with a 1D transmission-line model of the vocal and nasal
tract.

The tract model (dimensions, losses, soft walls, glottal source) is ported from ../sinus-rescue/tools/hum-model/
nasal_model.py (same author, written 2026-11-08 for the practice app), unchanged except that pressure is read out at
the ostium positions of all four sinuses. Positions from the velopharyngeal port outlet (approximate anatomy):
sphenoid (sphenoethmoidal recess) 2.5 cm, posterior ethmoid (superior meatus) 3.5 cm, maxillary (middle meatus)
5.5 cm, anterior ethmoid (ethmoid infundibulum) 6.0 cm, frontal (frontal recess) 6.5 cm; nostril 10 cm.
Writes results/ostium_pressure.json (a frequency table for the pages) and prints a summary.
Run: python tools/ostium_pressure.py
"""
import json, os
import numpy as np

RHO, C, GLOTTAL_R = 1.14, 350.0, 8e6
LOSS_ORAL, LOSS_NASAL = 0.55, 1.8
CM, CM2 = 0.01, 1e-4

def tube_matrix(length, area, f, loss):
    gamma = 1j * 2 * np.pi * f / C + loss * np.sqrt(f / 500)
    z0 = RHO * C / area
    ch, sh = np.cosh(gamma * length), np.sinh(gamma * length)
    return np.array([[ch, z0 * sh], [sh / z0, ch]])

def radiation(area, f):
    k = 2 * np.pi * f / C; a = np.sqrt(area / np.pi)
    return RHO * C / area * (0.25 * (k * a) ** 2 + 1j * 0.61 * k * a)

def soft_wall(area, f, mass=15.0, resistance=1e4, stiffness=4e6):
    w = 2 * np.pi * f
    return (resistance + 1j * w * mass + stiffness / (1j * w)) / area

parallel = lambda *z: 1 / sum(1 / x for x in z)

class Sinus:
    def __init__(self, name, volume, neck_area, neck_length, q=4.0):
        self.name = name; a = np.sqrt(neck_area / np.pi)
        self.mass = RHO * (neck_length + 1.7 * a) / neck_area
        self.compliance = volume / (RHO * C ** 2)
        self.resistance = np.sqrt(self.mass / self.compliance) / q
    def impedance(self, f):
        w = 2 * np.pi * f
        return self.resistance + 1j * w * self.mass + 1 / (1j * w * self.compliance)

# left + right lumped into one tube, so the sinuses are doubled too (same resonance as one side)
MAXILLARY = Sinus('maxillary', 2 * 15e-6, 2 * 4e-6, 6e-3)
SPHENOID = Sinus('sphenoid', 2 * 4e-6, 2 * 3e-6, 4e-3)

def tube(length, area, loss, step=0.25 * CM):
    n = max(1, int(round(length / step)))
    return [('tube', length / n, area, loss)] * n

PROBES = {'sph': 2.5, 'eth_post': 3.5, 'max': 5.5, 'eth_ant': 6.0, 'fro': 6.5}

def nasal_chain():
    """velopharyngeal port 1 cm, then the nasal cavity to the nostril (positions measured from the port outlet)."""
    ch = tube(1 * CM, 1.0 * CM2, LOSS_NASAL)
    ch += tube(2.5 * CM, 2.5 * CM2, LOSS_NASAL) + [('probe', 'sph'), ('sinus', SPHENOID)]
    ch += tube(1.0 * CM, 2.5 * CM2, LOSS_NASAL) + [('probe', 'eth_post')]
    ch += tube(2.0 * CM, 2.5 * CM2, LOSS_NASAL) + [('probe', 'max'), ('sinus', MAXILLARY)]
    ch += tube(0.5 * CM, 2.5 * CM2, LOSS_NASAL) + [('probe', 'eth_ant')]
    ch += tube(0.5 * CM, 2.5 * CM2, LOSS_NASAL) + [('probe', 'fro')]
    ch += tube(2.0 * CM, 2.5 * CM2, LOSS_NASAL)
    ch += tube(0.75 * CM, 1.2 * CM2, LOSS_NASAL) + [('wall', 5 * CM2)] + tube(0.75 * CM, 1.2 * CM2, LOSS_NASAL)
    return ch

ORAL_M = tube(4 * CM, 3 * CM2, LOSS_ORAL) + [('wall', 15 * CM2)] + tube(4 * CM, 3 * CM2, LOSS_ORAL)   # lips closed
PHARYNX = tube(9 * CM, 3 * CM2, LOSS_ORAL)

def elem(e, f):
    if e[0] == 'tube': return tube_matrix(e[1], e[2], f, e[3])
    if e[0] == 'sinus': return e[1].impedance(f)
    if e[0] == 'wall': return soft_wall(e[1], f)
    return None

def zin(chain, zend, f):
    z = zend
    for e in reversed(chain):
        if e[0] == 'probe': continue
        m = elem(e, f)
        z = (m[0, 0] * z + m[0, 1]) / (m[1, 0] * z + m[1, 1]) if e[0] == 'tube' else parallel(z, m)
    return z

def forward(chain, p, u, f):
    probes = {}
    for e in chain:
        if e[0] == 'probe': probes[e[1]] = p; continue
        m = elem(e, f)
        if e[0] == 'tube': p, u = np.linalg.solve(m, np.array([p, u]))
        else: u = u - p / m
    return probes, p

def solve(f):
    nasal = nasal_chain()
    z_or = zin(ORAL_M, 1e14, f)
    z_na = zin(nasal, radiation(1.2 * CM2, f), f)
    z_gl = zin(PHARYNX, parallel(z_or, z_na), f)
    u_gl = GLOTTAL_R / (GLOTTAL_R + z_gl); p_gl = u_gl * z_gl
    _, p_j = forward(PHARYNX, p_gl, u_gl, f)
    probes, _ = forward(nasal, p_j, p_j / z_na, f)
    return {k: abs(v) for k, v in probes.items()}

def main():
    FREQS = np.round(np.geomspace(50, 2500, 60)).astype(int).tolist()
    table = {k: [] for k in PROBES}
    for f in FREQS:
        p = solve(f)
        for k in PROBES: table[k].append(round(p[k] / p['max'], 4))
    # the pages use one ethmoid cell type: average of the anterior and posterior cells
    table['eth'] = [round((a + b) / 2, 4) for a, b in zip(table['eth_ant'], table['eth_post'])]
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results', 'ostium_pressure.json')
    json.dump({'what': 'pressure at each ostium / pressure at the maxillary ostium, hum [m], nose open (tools/ostium_pressure.py)',
               'positions_cm_from_port': PROBES, 'freqs_hz': FREQS, 'g': {k: table[k] for k in ('sph', 'fro', 'eth', 'eth_ant', 'eth_post')}},
              open(out, 'w', encoding='utf-8'), indent=None)
    print('pressure relative to the maxillary ostium:')
    print('  f (Hz)   ' + ''.join(f'{k:>9}' for k in ('sph', 'eth_post', 'eth_ant', 'fro', 'eth')))
    for f in [100, 130, 150, 200, 300, 450, 600, 900, 1200, 1800]:
        i = int(np.argmin([abs(x - f) for x in FREQS]))
        print(f'  {FREQS[i]:6d}   ' + ''.join(f'{table[k][i]:9.2f}' for k in ('sph', 'eth_post', 'eth_ant', 'fro', 'eth')))
    p150 = solve(150); top = max(p150.values())
    print('\nat 150 Hz, relative to the highest of the probes: ' + ', '.join(f'{k} {v / top:.2f}' for k, v in p150.items()))
    print('wrote', out)


if __name__ == '__main__':
    main()
