"""Compare long agefield runs cycle by cycle (grid check): frozen stroke, mixing efficiency over time, exchange.

Run: python tools/agefield_compare.py results/lbm/fict_max_040_150hz_v2 results/lbm/fict_max_020_150hz [...]
Reads only <run>/cycles.json. The mixing efficiency eta of a cycle is the old air it removes from the sinus
(relative to the current content) per inflow volume, as logged by pages/agefield.template.html.
numpy only.
"""
import sys, os, json
import numpy as np

runs = sys.argv[1:]
MARK = [50, 100, 200, 400, 700, 1000, 1200, 1500]
rows = []
for run in runs:
    cyc = json.load(open(os.path.join(run, 'cycles.json'), encoding='utf-8'))
    m, log = cyc['meta'], np.array(cyc['log'], float)
    f = m['C']['f']; target = m['L0d'] * m['dCells'] * m['area']
    fz = int(log[log[:, 4] == 1][0, 0])
    eta, C, inflow = log[:, 3], log[:, 2], log[:, 1]
    e0 = eta[fz:fz + 50].mean()
    k0 = None
    print(f"\n{os.path.basename(run)}: dx {m['dx']} mm, {m['nf']:,} fluid cells, {m['sinusCells']:,} sinus cells, "
          f"ostium {m['dCells']:.0f} cells across, {len(log)} cycles in {m['seconds']:.0f} s ({m['stepsPerSecond']:.0f} steps/s)")
    print(f"  frozen at cycle {fz}; stroke / target: start {inflow[fz:fz + 50].mean() / target:.3f}, "
          f"end {inflow[-50:].mean() / target:.3f}")
    print('  cycle   time    eta(50-cycle mean)  x start   exchanged   one box at the start rate')
    # one well-mixed box with the starting per-cycle exchange: each cycle removes e1 of the content
    n1 = min(20, len(log) - fz)
    e1 = np.mean(1 - C[fz:fz + n1] / np.concatenate([[C[fz - 1]], C[fz:fz + n1 - 1]]))
    out = {'run': os.path.basename(run), 'dx': m['dx'], 'e0': e0}
    for i in MARK:
        if i > len(log): continue
        e = eta[max(fz, i - 50):i].mean()
        box = 1 - C[fz - 1] * (1 - e1) ** (i - fz)
        print(f"  {i:5d}  {i / f:5.2f} s   {e:.3f}              {e / e0:5.2f}    {(1 - C[i - 1]) * 100:5.1f} %     {box * 100:5.1f} %")
        out[i] = (e, e / e0, 1 - C[i - 1])
    rows.append(out)

if len(rows) > 1:
    print('\nratio of the later runs to the first (eta x start):')
    for i in MARK:
        if all(i in r for r in rows):
            print(f"  {i:5d}  " + '  '.join(f"{r['run']}: {r[i][1]:.2f}" for r in rows))
