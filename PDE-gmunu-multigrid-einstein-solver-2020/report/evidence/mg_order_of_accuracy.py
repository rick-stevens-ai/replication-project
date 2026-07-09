#!/usr/bin/env python3
"""
Order-of-accuracy verification for the 5-point Laplacian used in this MG spot-check
of Gmunu (Cheong+Lin+Li 2020).

The paper (§7.4) asserts second-order spatial accuracy of the metric solver on
smooth solutions.  Since the elliptic operator inside Gmunu is discretized with
the standard 2nd-order cell-centred stencil (and prolongation is bilinear which
does not degrade the fine-grid accuracy), the discrete solution error against
a smooth manufactured solution must scale as O(h^2).

We solve  -Delta u = 2 pi^2 sin(pi x) sin(pi y)  on the unit square with
Dirichlet BC u=0, using the same MG solver as `mg_poisson_spotcheck.py`, on a
sequence of refined grids N = 15, 31, 63, 127, 255.  For each grid we solve to
tight tolerance (so discretization error dominates iteration error), then
compare against the analytic solution.  We fit log(err) = p * log(h) + c and
report the observed order p (expected p ~ 2.0).

Outputs:
  order_of_accuracy.csv    N, h, err_L1, err_L2, err_Linf, cycles_run
  order_of_accuracy.json   fits + observed orders
  order_of_accuracy.png    log-log err vs h with fitted slope
"""
from __future__ import annotations
import os, sys, csv, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mg_poisson_spotcheck import make_problem, residual, vcycle
from mg_grid_independence import deepest_depth


def solve_to_tol(N: int, tol_abs: float = 1e-12, max_cycles: int = 60):
    depth = deepest_depth(N)
    u, f, h, u_exact = make_problem(N)
    r0 = residual(u, f, h)
    r0_L1 = float(np.mean(np.abs(r0[1:-1, 1:-1])))
    tol = max(tol_abs, 1e-11 * r0_L1)
    cycles = 0
    for it in range(1, max_cycles + 1):
        vcycle(u, f, h, level=1, max_level=depth)
        r = residual(u, f, h)
        r_L1 = float(np.mean(np.abs(r[1:-1, 1:-1])))
        cycles = it
        if r_L1 < tol:
            break
    diff = u - u_exact
    err_L1 = float(np.mean(np.abs(diff[1:-1, 1:-1])))
    err_L2 = float(np.sqrt(np.mean(diff[1:-1, 1:-1] ** 2)))
    err_Linf = float(np.max(np.abs(diff[1:-1, 1:-1])))
    return {
        "N_interior": N, "h": h, "grid": f"{N+2}x{N+2}", "depth": depth,
        "err_L1": err_L1, "err_L2": err_L2, "err_Linf": err_Linf,
        "cycles_run": cycles, "r_L1_final": r_L1,
    }


def main():
    Ns = [15, 31, 63, 127, 255]
    results = [solve_to_tol(N) for N in Ns]
    print(f"# Order-of-accuracy study (Gmunu-analogue MG on 2D Poisson)")
    for r in results:
        print(
            f"N={r['N_interior']:3d} grid={r['grid']:>9s} depth=V{r['depth']:d} "
            f"h={r['h']:.4e} err_L1={r['err_L1']:.3e} "
            f"err_L2={r['err_L2']:.3e} err_Linf={r['err_Linf']:.3e} "
            f"cycles={r['cycles_run']:2d} r_final={r['r_L1_final']:.1e}"
        )

    hs = np.array([r["h"] for r in results])
    orders = {}
    for norm in ("err_L1", "err_L2", "err_Linf"):
        errs = np.array([r[norm] for r in results])
        # Fit log(err) = p*log(h) + c using all points
        p, c = np.polyfit(np.log(hs), np.log(errs), 1)
        # Also pairwise refinement orders (successive halvings)
        pair = []
        for i in range(len(hs) - 1):
            pair.append(float(np.log(errs[i] / errs[i + 1]) / np.log(hs[i] / hs[i + 1])))
        orders[norm] = {"fit_slope": float(p),
                        "fit_intercept": float(c),
                        "pairwise_orders": pair}
        print(f"observed order [{norm}] slope = {p:.4f}   pairwise = "
              + ", ".join(f"{q:.3f}" for q in pair))

    # CSV
    csv_path = os.path.join(HERE, "order_of_accuracy.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)
    print(f"\nWrote {csv_path}")

    # JSON
    j_path = os.path.join(HERE, "order_of_accuracy.json")
    with open(j_path, "w") as fh:
        json.dump({"results": results, "observed_orders": orders,
                   "expected_order": 2.0,
                   "problem": "-Delta u = 2*pi^2 sin(pi x) sin(pi y), Dirichlet 0",
                   "operator": "5-point standard Laplacian (2nd order)"},
                  fh, indent=2)
    print(f"Wrote {j_path}")

    # Plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6.4, 5))
        for norm, marker in zip(("err_L1", "err_L2", "err_Linf"), ("o", "s", "^")):
            errs = np.array([r[norm] for r in results])
            p = orders[norm]["fit_slope"]
            ax.loglog(hs, errs, marker + "-", label=f"{norm} (slope={p:.2f})", ms=6)
        # 2nd-order reference line
        ref = errs[-1] * (hs / hs[-1]) ** 2
        ax.loglog(hs, ref, "k--", alpha=0.5, label="O(h^2) reference")
        ax.set_xlabel("h = 1/(N+1)")
        ax.set_ylabel("Discrete solution error")
        ax.set_title("Order-of-accuracy: MG-solved 2D Poisson\n(Gmunu paper §7.4 asserts 2nd order)")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()
        png = os.path.join(HERE, "order_of_accuracy.png")
        fig.tight_layout()
        fig.savefig(png, dpi=110)
        print(f"Wrote {png}")
    except Exception as e:
        print(f"plot skipped: {e}")


if __name__ == "__main__":
    main()
