"""
2-D transient diffusion on a periodic square, method of manufactured solutions.

PDE:  dphi/dt = D * Laplacian(phi) + S(x,y,t)
Manufactured solution:
        phi*(x,y,t) = exp(-2*D*k^2*t) * sin(k*x) * sin(k*y),   k = 2*pi/L
Inserting into the PDE gives S == 0 (the manufactured solution is the
homogeneous heat-equation eigenmode), so we test the *unforced* 2-D
diffusion equation directly.

Periodic boundary conditions (PeriodicGrid2D) are exact for sin(k*x)
products with k = 2*pi*n/L, so no boundary modelling error contaminates
the convergence study.  Expected: 2nd-order spatial convergence for FiPy's
cell-centered FV discretisation.

This exercises:
  - 2D mesh
  - PERIODIC boundary conditions (the task explicitly asks for these)
  - quantitative agreement with an exact analytic solution
  - mesh-refinement order-of-accuracy
"""
from __future__ import annotations
import json, time
from pathlib import Path
import numpy as np
from fipy import CellVariable, PeriodicGrid2D, TransientTerm, DiffusionTerm

OUT_DIR = Path(__file__).resolve().parent
RESULTS = OUT_DIR / "results_2d_mms.json"

L = 1.0
D = 1.0
K = 2.0 * np.pi / L        # one full wavelength across [0,L]
T_FINAL = 0.002
# Implicit Euler is O(dt) in time and O(dx^2) in space. To recover the
# expected 2nd-order spatial convergence we refine dt in lockstep with dx^2.
# DT_BASE is the dt used at the COARSEST grid; finer grids use
# DT_BASE * (dx/dx_base)^2 so both errors decay at rate dx^2.
DT_BASE = 2.0e-4

def exact(x, y, t):
    return np.exp(-2.0 * D * K * K * t) * np.sin(K * x) * np.sin(K * y)

def run(n, n_base):
    dx = L / n
    dx_base = L / n_base
    dt = DT_BASE * (dx / dx_base) ** 2
    mesh = PeriodicGrid2D(nx=n, ny=n, dx=dx, dy=dx)
    phi = CellVariable(name="phi", mesh=mesh, value=0.0)
    cc = mesh.cellCenters
    # cellCenters can be a Variable (with .value) or a plain ndarray of shape (dim, ncells)
    cc_arr = np.array(cc.value if hasattr(cc, "value") else cc)
    x = cc_arr[0]
    y = cc_arr[1]
    phi.setValue(exact(x, y, 0.0))
    eq = TransientTerm() == DiffusionTerm(coeff=D)

    nsteps = int(round(T_FINAL / dt))
    t0 = time.time()
    for _ in range(nsteps):
        eq.solve(var=phi, dt=dt)
    wall = time.time() - t0

    phi_num = np.array(phi.value)
    phi_ana = exact(x, y, T_FINAL)
    err = phi_num - phi_ana
    L2 = float(np.sqrt(dx * dx * np.sum(err ** 2)))
    Linf = float(np.max(np.abs(err)))
    # Decay amplitude check: max|phi| should equal exp(-2*D*k^2*T) since
    # sin(kx)*sin(ky) has amplitude 1.
    decay_num = float(np.max(np.abs(phi_num)))
    decay_ana = float(np.exp(-2.0 * D * K * K * T_FINAL))
    return {
        "n": n, "dx": dx, "dt": dt, "nsteps": nsteps,
        "L2_vs_exact": L2, "Linf_vs_exact": Linf,
        "amp_num": decay_num, "amp_ana": decay_ana,
        "amp_rel_err": float(abs(decay_num - decay_ana) / decay_ana),
        "wall_s": wall,
    }

def main():
    grids = [16, 32, 64]
    n_base = grids[0]
    print(f"DT_BASE={DT_BASE:.1e} at n_base={n_base}; dt scales as dx^2 across grids.")
    results = []
    for n in grids:
        r = run(n, n_base)
        results.append(r)
        print(
            f"n={n:4d} dx={r['dx']:.4e}  L2={r['L2_vs_exact']:.4e}  "
            f"Linf={r['Linf_vs_exact']:.4e}  "
            f"amp_num={r['amp_num']:.6e}  amp_ana={r['amp_ana']:.6e}  "
            f"rel_amp_err={r['amp_rel_err']:.2e}  ({r['wall_s']:.1f}s)"
        )
    orders = []
    for i in range(1, len(results)):
        ratio = results[i - 1]["L2_vs_exact"] / results[i]["L2_vs_exact"]
        orders.append(float(np.log2(ratio)))
    print("observed L2 orders:", orders)

    summary = {
        "problem": "2D transient diffusion, periodic BCs, eigenmode IC",
        "L": L, "D": D, "K": K, "T_FINAL": T_FINAL,
        "DT_BASE": DT_BASE, "dt_scaling": "dt ~ dx^2 (lockstep with spatial)",
        "DT_FIXED": None,
        "exact_solution": "exp(-2*D*k^2*t) * sin(k*x) * sin(k*y), k=2*pi/L",
        "grids": results,
        "observed_L2_orders": orders,
        "expected_order": 2.0,
    }
    RESULTS.write_text(json.dumps(summary, indent=2))
    print(f"\nwrote {RESULTS}")

if __name__ == "__main__":
    main()
