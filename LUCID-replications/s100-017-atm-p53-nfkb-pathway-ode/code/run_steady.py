"""Run model to steady state with no input to confirm published ICs are stable."""
import numpy as np
from scipy.integrate import solve_ivp
import model

y0 = model.initial_state("Ctr")
print(f"y0 size = {y0.size}, sum = {y0.sum():.3e}")

# 48 h of no perturbation
t_final = 48.0 * 3600.0

sol = solve_ivp(
    fun=lambda t, y: model.rhs(t, y, lambda t: 0.0, lambda t: 0.0, siR=0),
    t_span=(0.0, t_final),
    y0=y0,
    method="LSODA",
    rtol=1e-6, atol=1e-3,
    max_step=60.0,
    dense_output=False,
)

print(f"solver status: {sol.status}, message: {sol.message}")
print(f"final t = {sol.t[-1]/3600:.3f} h, nsteps={len(sol.t)}")

names = model.NAMES
yf = sol.y[:, -1]
y0v = sol.y[:, 0]
print("\n key variable steady-state drift (initial -> 48h):")
for k in ["P53pn", "P53n", "WIP1n", "MDM2pn", "MDM2", "BAX", "P21",
          "ATMan", "CHK2pn", "NFKB", "NFKBn", "A20", "IKBA", "DSB"]:
    i = model.IDX[k]
    print(f"  {k:10s}  {y0v[i]:12.3f}  ->  {yf[i]:12.3f}   (Δ={yf[i]-y0v[i]:+.3f})")
