#!/usr/bin/env python3
"""
Grid-independence of multigrid V-cycle convergence — Gmunu (Cheong+Lin+Li 2020) deep dive.

The textbook hallmark of a well-designed multigrid solver (the property that
Gmunu Fig 11 implicitly demonstrates) is that the number of V-cycles required
to reach a given residual tolerance is *independent of the grid size*.  This
is what makes MG an O(N) solver rather than an O(N^alpha) iterative solver.

This script sweeps N in {31, 63, 127, 255, 511} interior points per side (so
grids 33^2 .. 513^2) at the deepest allowed V-cycle depth and measures:

  1. Iterations to reach an L1 residual tolerance (1e-9 relative).
  2. Asymptotic per-cycle convergence factor rho = (r_k / r_0)^(1/k).
  3. Wall time.

If grid-independent convergence is observed, that is quantitatively the
same behavior the Gmunu paper reports (deep V-cycle: tens of iterations,
independent of the 640x64 grid; single-grid GS: O(10^5), scales badly with N).

Same problem as `mg_poisson_spotcheck.py`:  -Delta u = f, u = sin(pi x) sin(pi y).
Same smoother, restriction, prolongation and cycle as `mg_poisson_spotcheck.py`.

Outputs (in this dir):
  mg_grid_independence.csv   iterations & residual per (N, cycle)
  mg_grid_independence.png   log-residual vs cycle, one line per N
  grid_independence_summary.json   final summary table
"""
from __future__ import annotations
import os, sys, csv, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mg_poisson_spotcheck import (
    make_problem, residual, gs_rb_relax,
    restrict_fullweight, prolong_bilinear, solve_direct, vcycle,
)


def deepest_depth(N: int) -> int:
    """Largest V-cycle depth allowed for N interior pts (so N+1 = 2^k)."""
    Nb = N + 1
    k = 0
    while (Nb % 2) == 0 and Nb > 2:
        Nb //= 2
        k += 1
    return k  # e.g. N=127 -> N+1 = 128 = 2^7 -> depth 7


def run_one(N: int, tol_rel: float = 1e-9, max_cycles: int = 60):
    depth = deepest_depth(N)
    u, f, h, u_exact = make_problem(N)
    r0 = residual(u, f, h)
    r_L1_0 = float(np.mean(np.abs(r0[1:-1, 1:-1])))
    tol = tol_rel * r_L1_0
    history = [(0, r_L1_0)]
    t0 = time.time()
    hit_tol_at = None
    for it in range(1, max_cycles + 1):
        vcycle(u, f, h, level=1, max_level=depth)
        r = residual(u, f, h)
        r_L1 = float(np.mean(np.abs(r[1:-1, 1:-1])))
        history.append((it, r_L1))
        if hit_tol_at is None and r_L1 <= tol:
            hit_tol_at = it
        # Stop once we've clearly hit the double-precision noise floor so the
        # asymptotic rate estimate below isn't polluted by round-off plateau.
        if r_L1 < 1e-12 or (hit_tol_at is not None and it >= hit_tol_at + 2):
            break
    dt = time.time() - t0
    err_L1 = float(np.mean(np.abs(u - u_exact)))

    # Asymptotic per-cycle convergence factor: geometric mean of ratios in the
    # "clean" regime after the initial transient and before the round-off noise
    # floor at ~1e-11..1e-13.  Restrict to residuals >= 1e-10 and iteration>=2.
    resids = np.array([h_[1] for h_ in history])
    rho = None
    if len(resids) >= 3:
        clean_mask = (resids > 1e-10)
        clean = resids[clean_mask]
        if len(clean) >= 3:
            tail = clean[-min(4, len(clean)):]
            ratios = tail[1:] / tail[:-1]
            ratios = ratios[(ratios > 0) & (ratios < 1) & np.isfinite(ratios)]
            if len(ratios) > 0:
                rho = float(np.exp(np.mean(np.log(ratios))))
    return {
        "N_interior": N,
        "grid": f"{N+2}x{N+2}",
        "depth": depth,
        "cycles_run": history[-1][0],
        "iters_to_tol": hit_tol_at,
        "tol_rel": tol_rel,
        "r_L1_initial": r_L1_0,
        "r_L1_final": history[-1][1],
        "reduction": history[-1][1] / r_L1_0 if r_L1_0 else None,
        "rho_asymptotic": rho,
        "err_vs_exact_L1": err_L1,
        "wall_seconds": dt,
        "history": history,
    }


def main():
    Ns = [31, 63, 127, 255, 511]
    print(f"# Grid-independence of MG V-cycle convergence")
    print(f"# tol_rel=1e-9, smoother=GS-RB 15+15, restriction=full-weighting, prolongation=bilinear")
    print(f"# Poisson: -Delta u = f, u = sin(pi x) sin(pi y), Dirichlet BC")
    results = []
    for N in Ns:
        r = run_one(N)
        results.append(r)
        print(
            f"N_interior={N:4d} grid={r['grid']:>9s} depth=V{r['depth']:d} "
            f"iters_to_1e-9_rel={str(r['iters_to_tol']):>4s} "
            f"cycles_run={r['cycles_run']:2d} "
            f"final_L1_res={r['r_L1_final']:.2e} "
            f"reduction={r['reduction']:.1e} "
            f"rho={r['rho_asymptotic']:.3f} "
            f"err_vs_exact={r['err_vs_exact_L1']:.2e} "
            f"t={r['wall_seconds']:.2f}s"
        )
    # csv
    csv_path = os.path.join(HERE, "mg_grid_independence.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["N_interior", "grid", "depth", "cycle", "L1_residual"])
        for r in results:
            for it, res in r["history"]:
                w.writerow([r["N_interior"], r["grid"], r["depth"], it, res])
    print(f"\nWrote {csv_path}")

    # summary json
    summary = [{k: v for k, v in r.items() if k != "history"} for r in results]
    j_path = os.path.join(HERE, "grid_independence_summary.json")
    with open(j_path, "w") as fh:
        json.dump({"tol_rel": 1e-9, "smoother": "GS-RB nu_pre=nu_post=15",
                   "restriction": "full-weighting", "prolongation": "bilinear",
                   "problem": "-Delta u = 2*pi^2 sin(pi x) sin(pi y), Dirichlet BC",
                   "results": summary}, fh, indent=2)
    print(f"Wrote {j_path}")

    # plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 5))
        colors = plt.cm.viridis(np.linspace(0, 0.9, len(results)))
        for c, r in zip(colors, results):
            arr = np.array(r["history"])
            ax.semilogy(arr[:, 0], arr[:, 1], "o-", color=c, ms=3,
                        label=f"{r['grid']} (V{r['depth']})")
        ax.set_xlabel("V-cycle iteration")
        ax.set_ylabel("L1 norm of residual")
        ax.set_title("Grid-independence of MG V-cycle convergence\n"
                     "(Gmunu Fig 11 analogue: 2D Poisson, GS-RB 15+15)")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend(loc="upper right", fontsize=9)
        png = os.path.join(HERE, "mg_grid_independence.png")
        fig.tight_layout()
        fig.savefig(png, dpi=110)
        print(f"Wrote {png}")
    except Exception as e:
        print(f"plot skipped: {e}")


if __name__ == "__main__":
    main()
