"""Linear Landau damping benchmark, full vs low-rank.

Setup follows Einkemmer-Lubich 2018 §4.1 (linear Landau): k=0.5, α=0.01, T=40.
Expected: electric field |E|_∞ (or √(2 E_e)) decays at γ ≈ 0.1533 (linear Landau rate).
"""
import sys, time, json, os
import numpy as np
sys.path.insert(0, '.')
from vp_common import Grid, landau_ic, total_mass
import vp_full, vp_lowrank

OUT = '../results'
os.makedirs(OUT, exist_ok=True)

grid = Grid(Nx=64, Nv=128, L=4*np.pi, vmax=6.0)   # 1 wavelength of k=0.5? L = 4π gives 2 wavelengths.
f0 = landau_ic(grid, alpha=0.01, k=0.5)

T = 40.0
dt = 0.05

results = {}

print("== Full-grid baseline ==")
t0 = time.time()
r_full = vp_full.run(f0, grid, T, dt, diag_every=1)
results['full'] = {
    'wall_sec': time.time() - t0,
    't': r_full['t'].tolist(),
    'E_energy': r_full['E_energy'].tolist(),
    'mass': r_full['mass'].tolist(),
    'kinetic_energy': r_full['kinetic_energy'].tolist(),
    'l2': r_full['l2'].tolist(),
}
np.save(f'{OUT}/landau_f_final_full.npy', r_full['f_final'])
print(f"  wall = {results['full']['wall_sec']:.2f}s   final E_e = {r_full['E_energy'][-1]:.3e}")

for r in [2, 4, 8, 16]:
    print(f"== Low-rank r={r} ==")
    t0 = time.time()
    r_lr = vp_lowrank.run(f0, grid, T, dt, r=r, diag_every=1)
    wall = time.time() - t0
    err_t = np.zeros_like(r_full['t'])
    # final-time error in distribution
    f_lr_final = r_lr['f_final']
    f_full_final = r_full['f_final']
    err_final = np.linalg.norm(f_full_final - f_lr_final) * np.sqrt(grid.dx * grid.dv)
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
    np.save(f'{OUT}/landau_f_final_r{r}.npy', f_lr_final)
    print(f"  wall = {wall:.2f}s   final E_e = {r_lr['E_energy'][-1]:.3e}   ||Δf||_L2 = {err_final:.3e}")

# Estimate damping rate from full run (fit ln(sqrt(2 E_e)) over t∈[5,20] envelope peaks)
t = np.array(r_full['t'])
sE = np.sqrt(2.0 * np.array(r_full['E_energy']))
# Pick local maxima as envelope
peaks = []
for i in range(1, len(sE)-1):
    if sE[i] > sE[i-1] and sE[i] > sE[i+1] and 2 < t[i] < 25:
        peaks.append((t[i], sE[i]))
if len(peaks) >= 3:
    tp = np.array([p[0] for p in peaks])
    sp = np.array([p[1] for p in peaks])
    A = np.vstack([tp, np.ones_like(tp)]).T
    slope, intercept = np.linalg.lstsq(A, np.log(sp), rcond=None)[0]
    results['damping_rate_estimate'] = float(-slope)
    results['damping_rate_analytic'] = 0.1533
    print(f"\nEstimated damping rate from peaks: γ ≈ {-slope:.4f}  (analytic 0.1533)")

with open(f'{OUT}/landau_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nResults written to {OUT}/landau_results.json")
