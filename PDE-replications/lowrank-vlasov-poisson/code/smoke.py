"""Smoke test: short Landau damping run with full solver and low-rank r=8."""
import sys, time
import numpy as np
sys.path.insert(0, '.')
from vp_common import Grid, landau_ic, total_mass
import vp_full, vp_lowrank

grid = Grid(Nx=64, Nv=128, L=4*np.pi, vmax=6.0)
f0 = landau_ic(grid, alpha=0.01, k=0.5)
print(f"Initial mass = {total_mass(f0, grid):.6f}  (expected = L = {grid.L:.6f})")
print(f"Grid: Nx={grid.Nx} Nv={grid.Nv} L={grid.L:.4f} vmax={grid.vmax}")

T = 5.0
dt = 0.05

print("\n== Full-grid baseline ==")
t0 = time.time()
res_full = vp_full.run(f0, grid, T, dt, diag_every=1)
tf = time.time() - t0
print(f"  elapsed: {tf:.2f}s")
print(f"  mass drift: {res_full['mass'][-1] - res_full['mass'][0]:.3e}")
print(f"  E-energy[0]={res_full['E_energy'][0]:.3e}  E-energy[end]={res_full['E_energy'][-1]:.3e}")

for r in [2, 4, 8]:
    print(f"\n== Low-rank r={r} ==")
    t0 = time.time()
    res_lr = vp_lowrank.run(f0, grid, T, dt, r=r, diag_every=1)
    tl = time.time() - t0
    print(f"  elapsed: {tl:.2f}s")
    print(f"  mass drift: {res_lr['mass'][-1] - res_lr['mass'][0]:.3e}")
    print(f"  E-energy[0]={res_lr['E_energy'][0]:.3e}  E-energy[end]={res_lr['E_energy'][-1]:.3e}")
    err = np.linalg.norm(res_full['f_final'] - res_lr['f_final']) * np.sqrt(grid.dx * grid.dv)
    print(f"  ||f_full - f_lr||_L2 at T={T}: {err:.3e}")
