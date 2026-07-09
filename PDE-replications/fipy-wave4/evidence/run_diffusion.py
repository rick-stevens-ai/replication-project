#!/usr/bin/env python
"""
FiPy replication — Wave 4
=========================
1D transient diffusion with a step initial condition, on a finite mesh.
Compared against the half-space analytical solution u(x,t) = 0.5*erfc((x-L/2)/(2 sqrt(D t)))
for early times (before boundary effects pollute the interior).
"""
import json, os, time
import numpy as np
from scipy.special import erfc
from fipy import CellVariable, Grid1D, TransientTerm, DiffusionTerm, Viewer
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

EDIR = os.path.dirname(os.path.abspath(__file__))


def run(nx=100, D=1.0, t_final=0.05, dt=None, L=1.0):
    dx = L / nx
    if dt is None:
        # CFL-ish: dt = 0.5 * dx^2 / D for implicit Euler we have no stab limit,
        # but use this for time accuracy.
        dt = 0.45 * dx * dx / D
    mesh = Grid1D(nx=nx, dx=dx)
    phi = CellVariable(name="phi", mesh=mesh, value=0.0)
    # Step initial condition: phi=1 for x<L/2, 0 otherwise
    x = mesh.cellCenters[0]
    phi.setValue(1.0, where=x < L / 2.0)

    # Dirichlet BCs: 1 on left, 0 on right
    phi.constrain(1.0, mesh.facesLeft)
    phi.constrain(0.0, mesh.facesRight)

    eq = TransientTerm() == DiffusionTerm(coeff=D)

    n_steps = int(np.ceil(t_final / dt))
    dt_actual = t_final / n_steps
    t0 = time.time()
    for step in range(n_steps):
        eq.solve(var=phi, dt=dt_actual)
    elapsed = time.time() - t0

    # Compare to half-space erfc reference at t = t_final
    xc = np.array(x)
    phi_num = np.array(phi)
    # Reference (infinite-domain solution starting from step at x=L/2):
    phi_ref = 0.5 * erfc((xc - L / 2.0) / (2.0 * np.sqrt(D * t_final)))

    # Compute L2 and Linf errors in an interior window away from boundaries
    # (avoid the leftmost / rightmost decile where Dirichlet BCs distort)
    mask = (xc > 0.1 * L) & (xc < 0.9 * L)
    L2 = float(np.sqrt(np.mean((phi_num[mask] - phi_ref[mask]) ** 2)))
    Linf = float(np.max(np.abs(phi_num[mask] - phi_ref[mask])))

    return dict(
        nx=nx,
        dx=dx,
        dt=dt_actual,
        n_steps=n_steps,
        t_final=t_final,
        D=D,
        L=L,
        elapsed_s=round(elapsed, 3),
        L2_interior=L2,
        Linf_interior=Linf,
        xc=xc.tolist(),
        phi_num=phi_num.tolist(),
        phi_ref=phi_ref.tolist(),
    )


def plot(result, outpath):
    xc = np.array(result["xc"])
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(xc, result["phi_num"], "b-", lw=2, label=f"FiPy numerical (nx={result['nx']})")
    ax.plot(xc, result["phi_ref"], "r--", lw=1.5, label="Analytic erfc reference")
    ax.set_xlabel("x")
    ax.set_ylabel("phi")
    ax.set_title(
        f"FiPy 1D diffusion, t={result['t_final']}, D={result['D']}; "
        f"interior L2={result['L2_interior']:.3e}, Linf={result['Linf_interior']:.3e}"
    )
    ax.legend()
    ax.grid(True, ls=":")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_convergence(results, outpath):
    Ns = [r["nx"] for r in results]
    L2 = [r["L2_interior"] for r in results]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.loglog(Ns, L2, "bo-", lw=2, label="FiPy L2 (interior)")
    # First-order reference line through first point
    ax.loglog(Ns, [L2[0] * (Ns[0] / N) for N in Ns], "r--", label="O(Δx)")
    ax.loglog(Ns, [L2[0] * (Ns[0] / N) ** 2 for N in Ns], "g--", label="O(Δx²)")
    ax.set_xlabel("nx")
    ax.set_ylabel("interior L2 error vs analytic erfc")
    ax.set_title("FiPy 1D diffusion — mesh refinement")
    ax.legend()
    ax.grid(True, which="both", ls=":")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


if __name__ == "__main__":
    print("FiPy replication — 1D diffusion")
    print("=" * 50)
    results = []
    for nx in (50, 100, 200, 400):
        r = run(nx=nx, D=1.0, t_final=0.05)
        print(f"  nx={nx:4d}  steps={r['n_steps']:4d}  dt={r['dt']:.2e}  "
              f"L2_interior={r['L2_interior']:.3e}  Linf={r['Linf_interior']:.3e}  "
              f"({r['elapsed_s']}s)")
        results.append(r)

    # Compute observed order from successive L2s
    orders = []
    for i in range(1, len(results)):
        o = np.log(results[i - 1]["L2_interior"] / results[i]["L2_interior"]) / np.log(
            results[i]["nx"] / results[i - 1]["nx"]
        )
        orders.append(round(float(o), 3))
    print(f"  observed orders: {orders}")

    plot(results[1], os.path.join(EDIR, "diffusion_solution.png"))
    plot_convergence(results, os.path.join(EDIR, "convergence.png"))

    # Summary JSON (drop big arrays for finest grids)
    summary = dict(
        runs=[{k: v for k, v in r.items() if k not in ("xc", "phi_num", "phi_ref")}
              for r in results],
        observed_orders=orders,
        notes="1D transient diffusion, Dirichlet BCs phi=1 at x=0 and phi=0 at x=L; "
              "compared in interior 10–90% window against half-space erfc reference.",
    )
    out = os.path.join(EDIR, "results.json")
    with open(out, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n  results → {out}")
    print("Done.")
