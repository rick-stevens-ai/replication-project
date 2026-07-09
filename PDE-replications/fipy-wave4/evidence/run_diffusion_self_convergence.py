"""
1-D transient diffusion, FiPy self-convergence study.

Improvement over run_diffusion.py:
  - Compare against a high-resolution FiPy reference (nx=2048) interpolated to
    coarse grids, instead of the infinite-domain erfc.  This eliminates the
    finite-vs-infinite domain modelling bias and exposes the true spatial
    order-of-accuracy of FiPy's cell-centered FV / implicit Euler scheme.
  - Use a SMOOTH initial condition (Gaussian bump well inside the domain) so
    the IC itself does not introduce a non-smooth-data convergence floor.
  - Hold dt FIXED across all grids so the observed order is purely spatial.

Expected: ~2nd-order spatial convergence for cell-centered FV on a smooth
solution (Guyer/Wheeler/Warren 2009, "FiPy" CSE paper, §"Discretization").
"""
from __future__ import annotations
import json, time, os
from pathlib import Path
import numpy as np
from fipy import CellVariable, Grid1D, TransientTerm, DiffusionTerm

OUT_DIR = Path(__file__).resolve().parent
RESULTS = OUT_DIR / "results_self_convergence_1d.json"

L = 1.0
D = 1.0
T_FINAL = 0.02            # short enough that Gaussian stays well inside [0,L]
DT_FIXED = 5.0e-5         # same dt for every grid -> isolates spatial order
SIGMA = 0.05
X0 = 0.5

def gaussian_ic(x):
    return np.exp(-((x - X0) ** 2) / (2.0 * SIGMA ** 2))

def run(nx):
    dx = L / nx
    mesh = Grid1D(nx=nx, dx=dx)
    phi = CellVariable(name="phi", mesh=mesh, value=0.0)
    x = mesh.cellCenters[0].value
    phi.setValue(gaussian_ic(x))
    # Dirichlet BCs far from the bump: phi=0 at both ends (bump decays to ~0
    # before hitting the boundary in the time window we use).
    phi.constrain(0.0, mesh.facesLeft)
    phi.constrain(0.0, mesh.facesRight)
    eq = TransientTerm() == DiffusionTerm(coeff=D)

    nsteps = int(round(T_FINAL / DT_FIXED))
    t0 = time.time()
    for _ in range(nsteps):
        eq.solve(var=phi, dt=DT_FIXED)
    wall = time.time() - t0
    return {
        "nx": nx,
        "dx": dx,
        "dt": DT_FIXED,
        "nsteps": nsteps,
        "x": x.tolist(),
        "phi": phi.value.tolist(),
        "wall_s": wall,
    }

def cell_average_reference(x_fine, phi_fine, dx_fine, x_coarse, dx_coarse):
    """Average the fine-grid cell-centered solution over each coarse cell
    (proper FV restriction)."""
    out = np.empty_like(x_coarse)
    for i, xc in enumerate(x_coarse):
        lo, hi = xc - 0.5 * dx_coarse, xc + 0.5 * dx_coarse
        mask = (x_fine + 0.5 * dx_fine > lo) & (x_fine - 0.5 * dx_fine < hi)
        # weight by overlap length
        x_lo = np.maximum(x_fine[mask] - 0.5 * dx_fine, lo)
        x_hi = np.minimum(x_fine[mask] + 0.5 * dx_fine, hi)
        w = (x_hi - x_lo)
        out[i] = (w * phi_fine[mask]).sum() / w.sum()
    return out

def main():
    grids = [32, 64, 128, 256]
    ref_nx = 2048

    print(f"Computing high-resolution reference at nx={ref_nx} ...")
    ref = run(ref_nx)
    x_ref = np.array(ref["x"])
    phi_ref = np.array(ref["phi"])
    dx_ref = ref["dx"]

    results = []
    for nx in grids:
        r = run(nx)
        x = np.array(r["x"])
        phi = np.array(r["phi"])
        # FV-consistent restriction of the fine solution to this coarse grid
        phi_ref_on_coarse = cell_average_reference(x_ref, phi_ref, dx_ref, x, r["dx"])
        err = phi - phi_ref_on_coarse
        L2 = float(np.sqrt(r["dx"] * np.sum(err ** 2)))
        Linf = float(np.max(np.abs(err)))
        r["L2_vs_ref"] = L2
        r["Linf_vs_ref"] = Linf
        # drop big arrays from per-grid record (still keep in summary plot data)
        r["x"] = None
        r["phi"] = None
        results.append(r)
        print(f"nx={nx:4d} dx={r['dx']:.4e} L2={L2:.4e}  Linf={Linf:.4e}  ({r['wall_s']:.1f}s)")

    # Observed orders between successive halvings of dx
    orders = []
    for i in range(1, len(results)):
        ratio = results[i - 1]["L2_vs_ref"] / results[i]["L2_vs_ref"]
        orders.append(float(np.log2(ratio)))
    print("observed L2 orders (between successive grids):", orders)

    summary = {
        "problem": "1D transient diffusion, smooth Gaussian IC, Dirichlet BCs",
        "L": L, "D": D, "T_FINAL": T_FINAL, "DT_FIXED": DT_FIXED,
        "SIGMA": SIGMA, "X0": X0,
        "ref_nx": ref_nx, "ref_wall_s": ref["wall_s"],
        "grids": results,
        "observed_L2_orders": orders,
        "expected_order": 2.0,
        "note": (
            "Cell-centered FV with FV-consistent restriction of a fine FiPy "
            "reference; dt held fixed across grids so the observed order is "
            "purely spatial.  Expected ~2 (Guyer/Wheeler/Warren 2009)."
        ),
    }
    RESULTS.write_text(json.dumps(summary, indent=2))
    print(f"\nwrote {RESULTS}")

if __name__ == "__main__":
    main()
