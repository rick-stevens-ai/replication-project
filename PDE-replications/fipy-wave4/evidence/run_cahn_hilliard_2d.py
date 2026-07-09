"""
2-D Cahn-Hilliard on a periodic square — mass-conservation test.

The Cahn-Hilliard equation models spinodal decomposition / phase separation:
    dc/dt = nabla . ( M * nabla mu )
    mu    = df/dc - epsilon^2 * Laplacian(c)        (chemical potential)
    f(c)  = (a^2/2) * c^2 * (1 - c)^2               (double-well free energy)

Properties tested:
  C-CH-1: GLOBAL MASS CONSERVATION.  Because the RHS is the divergence of a
          flux and the domain is periodic, the spatial integral of c (the
          total mass) must be conserved EXACTLY to within solver / round-off
          tolerance.  This is the FiPy paper's headline correctness property
          for the Cahn-Hilliard family.
  C-CH-2: FREE-ENERGY DECREASE.  The total free energy
              F[c] = integral( f(c) + (eps^2/2) * |grad c|^2 ) dV
          must be non-increasing in time (Lyapunov property).
  C-CH-3: PHASE SEPARATION.  Starting from a small random perturbation around
          c=0.5, the field must coarsen toward the two stable phases c=0 and
          c=1 (standard double-well basins).

This exercises FiPy's higher-order PDE (4th-order via coupled 2nd-order
equations), 2D mesh, PERIODIC BCs, and conservation/Lyapunov properties.
"""
from __future__ import annotations
import json, time
from pathlib import Path
import numpy as np
from fipy import (
    CellVariable, PeriodicGrid2D, TransientTerm, DiffusionTerm,
    ImplicitSourceTerm, Variable,
)

OUT_DIR = Path(__file__).resolve().parent
RESULTS = OUT_DIR / "results_cahn_hilliard.json"

L = 1.0
N = 64
DX = L / N
M = 1.0          # mobility
A2 = 1.0         # well height
EPS = 0.01       # interface thickness scale
DT = 1.0e-3
T_FINAL = 0.3
SEED = 12345
NOISE_AMPL = 0.05
C0 = 0.5          # initial mean concentration

def main():
    mesh = PeriodicGrid2D(nx=N, ny=N, dx=DX, dy=DX)
    c = CellVariable(name="c", mesh=mesh, hasOld=True)
    mu = CellVariable(name="mu", mesh=mesh, hasOld=True)
    rng = np.random.default_rng(SEED)
    c.setValue(C0 + NOISE_AMPL * (rng.random(N * N) - 0.5))
    initial_mass = float((c.value * DX * DX).sum())

    # f(c) = (a^2/2) c^2 (1-c)^2
    # df/dc = a^2 * c * (1-c) * (1-2c)
    # split for implicit treatment: linearise df/dc around the current value.
    # Standard FiPy coupled formulation:
    #   eq_c  : TransientTerm(var=c) == DiffusionTerm(coeff=M, var=mu)
    #   eq_mu : ImplicitSourceTerm(coeff=1.0, var=mu)
    #             == df/dc(c)  -  DiffusionTerm(coeff=eps^2, var=c)
    # Solve as a coupled system via &.
    dfdc = A2 * c * (1.0 - c) * (1.0 - 2.0 * c)
    eq_c = TransientTerm(var=c) == DiffusionTerm(coeff=M, var=mu)
    eq_mu = (
        ImplicitSourceTerm(coeff=1.0, var=mu)
        == dfdc - DiffusionTerm(coeff=EPS ** 2, var=c)
    )
    eq = eq_c & eq_mu

    def free_energy():
        # f(c) is a CellVariable expression; integrate over volume
        f_density = (A2 / 2.0) * (c * c * (1.0 - c) ** 2)
        # |grad c|^2: use FiPy's grad operator
        grad_c = c.grad
        grad_sq = (grad_c.dot(grad_c))
        # integrate over cell volumes
        cellVol = mesh.cellVolumes
        return float(((f_density + 0.5 * EPS ** 2 * grad_sq) * cellVol).sum())

    history = []
    nsteps = int(round(T_FINAL / DT))
    t0 = time.time()
    F0 = free_energy()
    m0 = float((c.value * mesh.cellVolumes).sum())
    history.append({"step": 0, "t": 0.0, "mass": m0, "F": F0,
                    "c_min": float(np.min(c.value)),
                    "c_max": float(np.max(c.value))})
    print(f"step=    0  t=0.000  mass={m0:.10f}  F={F0:.6e}  "
          f"c in [{np.min(c.value):.4f}, {np.max(c.value):.4f}]")

    for step in range(1, nsteps + 1):
        c.updateOld()
        mu.updateOld()
        # Newton-like sweep: re-solve a few times per step for the nonlinear
        # df/dc term to converge.
        for _ in range(2):
            eq.solve(dt=DT)
        if step % 50 == 0 or step == nsteps:
            m = float((c.value * mesh.cellVolumes).sum())
            F = free_energy()
            cmin = float(np.min(c.value)); cmax = float(np.max(c.value))
            history.append({"step": step, "t": step * DT, "mass": m, "F": F,
                            "c_min": cmin, "c_max": cmax})
            print(f"step={step:5d}  t={step*DT:.3f}  mass={m:.10f}  "
                  f"F={F:.6e}  c in [{cmin:.4f}, {cmax:.4f}]")
    wall = time.time() - t0

    final_mass = float((c.value * mesh.cellVolumes).sum())
    mass_drift_abs = abs(final_mass - initial_mass)
    mass_drift_rel = mass_drift_abs / abs(initial_mass)
    F_final = free_energy()
    F_initial = history[0]["F"]
    F_monotone = all(history[i + 1]["F"] <= history[i]["F"] + 1e-12
                     for i in range(len(history) - 1))

    summary = {
        "problem": "2D Cahn-Hilliard, periodic BCs, random IC around c=0.5",
        "N": N, "DX": DX, "DT": DT, "T_FINAL": T_FINAL,
        "M": M, "A2": A2, "EPS": EPS, "SEED": SEED,
        "initial_mass": initial_mass, "final_mass": final_mass,
        "mass_drift_abs": mass_drift_abs,
        "mass_drift_rel": mass_drift_rel,
        "F_initial": F_initial, "F_final": F_final,
        "F_monotone_decreasing": bool(F_monotone),
        "c_final_min": float(np.min(c.value)),
        "c_final_max": float(np.max(c.value)),
        "wall_s": wall,
        "history": history,
    }
    RESULTS.write_text(json.dumps(summary, indent=2))
    print(f"\nMass drift (relative): {mass_drift_rel:.3e}  "
          f"(target: < 1e-8 for conserved flux)")
    print(f"Free energy: {F_initial:.6e} -> {F_final:.6e}  "
          f"monotone-decreasing: {F_monotone}")
    print(f"c range: [{np.min(c.value):.4f}, {np.max(c.value):.4f}]  "
          f"(phase separation -> approach [0, 1])")
    print(f"wrote {RESULTS}  ({wall:.1f}s)")

if __name__ == "__main__":
    main()
