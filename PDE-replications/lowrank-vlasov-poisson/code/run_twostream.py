"""Two-stream instability benchmark, full vs low-rank.

Setup (Einkemmer-Lubich 2018 §4.2 / classical two-stream):
   f₀(x,v) = (1 + α cos(kx)) · 0.5·[g(v-v0) + g(v+v0)],  g = e^{-v²/2}/√(2π)
   α = 0.05, k = 0.5, v0 = 2.4, T = 40.
Expected: linear instability growth of E-field, then nonlinear saturation and
filamentation/phase-mixing in phase space (the characteristic "hole/eye" pattern).
"""
import sys, time, json, os
import numpy as np
sys.path.insert(0, '.')
from vp_common import Grid, two_stream_ic, total_mass
import vp_full, vp_lowrank

OUT = '../results'

grid = Grid(Nx=128, Nv=256, L=4*np.pi, vmax=8.0)
f0 = two_stream_ic(grid, alpha=0.05, k=0.5, v0=2.4)

T = 40.0
dt = 0.05

results = {}
print("== Full-grid baseline (two-stream) ==")
t0 = time.time()
r_full = vp_full.run(f0, grid, T, dt, diag_every=2)
results['full'] = {
    'wall_sec': time.time() - t0,
    't': r_full['t'].tolist(),
    'E_energy': r_full['E_energy'].tolist(),
    'mass': r_full['mass'].tolist(),
    'kinetic_energy': r_full['kinetic_energy'].tolist(),
    'l2': r_full['l2'].tolist(),
}
np.save(f'{OUT}/twostream_f_final_full.npy', r_full['f_final'])
print(f"  wall = {results['full']['wall_sec']:.2f}s   peak E_e = {max(r_full['E_energy']):.3e}")

# KSL projector-splitting is known to be non-robust for over-rank cases (Kieri-
# Lubich-Walach 2016): when the chosen rank exceeds the effective rank of the
# evolving solution, S becomes near-singular and the scheme can blow up. Use a
# smaller dt for higher rank as mitigation; the BUG / robust variants of
# Ceruti-Lubich (2022) are the recommended cure but are out of scope here.
rank_dt = {4: dt, 8: 0.01, 16: 0.005, 32: 0.0025}
for r in [4, 8, 16, 32]:
    print(f"== Low-rank r={r} ==")
    dt_r = rank_dt[r]
    t0 = time.time()
    r_lr = vp_lowrank.run(f0, grid, T, dt_r, r=r, diag_every=max(1, int(0.1/dt_r)))
    wall = time.time() - t0
    err_final = np.linalg.norm(r_full['f_final'] - r_lr['f_final']) * np.sqrt(grid.dx * grid.dv)
    results[f'lr_r{r}'] = {
        'rank': r,
        'wall_sec': wall,
        't': r_lr['t'].tolist(),
        'E_energy': r_lr['E_energy'].tolist(),
        'mass': r_lr['mass'].tolist(),
        'kinetic_energy': r_lr['kinetic_energy'].tolist(),
        'l2': r_lr['l2'].tolist(),
        'final_distribution_L2_error': float(err_final),
    }
    np.save(f'{OUT}/twostream_f_final_r{r}.npy', r_lr['f_final'])
    print(f"  wall = {wall:.2f}s   peak E_e = {max(r_lr['E_energy']):.3e}   ||Δf||_L2 = {err_final:.3e}")

with open(f'{OUT}/twostream_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nResults written to {OUT}/twostream_results.json")
