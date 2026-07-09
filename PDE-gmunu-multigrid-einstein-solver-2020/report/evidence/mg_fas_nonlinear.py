#!/usr/bin/env python3
"""
FAS (Full Approximation Scheme) nonlinear V-cycle multigrid — Gmunu deep dive.

The Gmunu paper (Cheong+Lin+Li 2020) uses FAS specifically because its metric
sector — Eqs. (13)-(16) — is *nonlinear* (positive powers of the conformal
factor ψ in the source; the Hamiltonian-constraint-like eq. has terms in ψ^{-7}
and ψ^{-5}).  This spot-check adds the missing piece from the earlier linear
V-cycle spot-check: an *actual nonlinear FAS V-cycle* solving a nonlinear
elliptic PDE with a positive-power nonlinearity that structurally resembles
Gmunu Eq. (15) (a scalar semilinear Poisson-type eq.).

Test problem (a common MG benchmark; e.g. Trottenberg-Oosterlee-Schuller):
    L(u) = -Delta u + u^3 = f     on (0,1)^2,   u = 0 on boundary
with f chosen so that u_exact(x,y) = sin(pi x) sin(pi y):
    f(x,y) = 2 pi^2 sin(pi x) sin(pi y) + [sin(pi x) sin(pi y)]^3.

This is smooth, nonlinear, and has a unique nonnegative solution; the same MG
components (GS-RB smoother, restriction, bilinear prolongation) apply.

FAS V-cycle (paper Algorithm 1, with gamma=1):
  pre-smooth  Lh(uh) = fh, nu_pre GS-RB sweeps (nonlinear GS: solves cubic
              4 u_ij / h^2 + u_ij^3 = rhs_ij per point)
  compute rh = fh - Lh(uh)
  restrict   u_{2h} <- R(uh),  r_{2h} <- R(rh)
  build      f_{2h} = r_{2h} + L_{2h}(u_{2h})       (paper Eq. 32)
  recurse    solve L_{2h}(v) = f_{2h}, v0 = u_{2h}
  correct    uh += P( v - u_{2h} )                  (paper Eq. 33)
  post-smooth nu_post GS-RB sweeps

Depths swept: 1..6.  Grid: N_int=127 (129^2).  We match the paper's
`nu_pre = nu_post = 15` and use L1 residual as the convergence measure
(same as Gmunu Fig 11).

Outputs (this dir):
  mg_fas_nonlinear.csv        residual per (depth, cycle)
  mg_fas_nonlinear.png        semilog residual plot, one line per V-depth
  fas_nonlinear_summary.json  final summary
"""
from __future__ import annotations
import os, sys, csv, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mg_poisson_spotcheck import restrict_fullweight, prolong_bilinear


def make_problem_nl(N: int):
    h = 1.0 / (N + 1)
    xs = np.linspace(0.0, 1.0, N + 2)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    u_exact = np.sin(np.pi * X) * np.sin(np.pi * Y)
    f = 2.0 * np.pi ** 2 * u_exact + u_exact ** 3
    u = np.zeros_like(f)
    return u, f, h, u_exact


def L_apply(u: np.ndarray, h: float) -> np.ndarray:
    """L(u) = -Delta_h u + u^3, zero on boundary."""
    Lu = np.zeros_like(u)
    Lu[1:-1, 1:-1] = (
        4.0 * u[1:-1, 1:-1]
        - u[2:, 1:-1] - u[:-2, 1:-1]
        - u[1:-1, 2:] - u[1:-1, :-2]
    ) / (h * h) + u[1:-1, 1:-1] ** 3
    return Lu


def residual_nl(u: np.ndarray, f: np.ndarray, h: float) -> np.ndarray:
    return f - L_apply(u, h)


def _cubic_root(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Real root of  x^3 + a x - b = 0  (single real root since discriminant<0
    is not guaranteed but for our problem a>0 always so exactly one real root).
    Cardano: x = cbrt(b/2 + sqrt(b^2/4 + a^3/27)) + cbrt(b/2 - sqrt(...))."""
    disc = b * b / 4.0 + (a ** 3) / 27.0
    sd = np.sqrt(np.maximum(disc, 0.0))
    p = b / 2.0 + sd
    q = b / 2.0 - sd
    cbrt_p = np.sign(p) * np.abs(p) ** (1.0 / 3.0)
    cbrt_q = np.sign(q) * np.abs(q) ** (1.0 / 3.0)
    return cbrt_p + cbrt_q


def gs_rb_relax_nl(u: np.ndarray, f: np.ndarray, h: float, nu: int) -> None:
    """Nonlinear red-black Gauss-Seidel for -Delta_h u + u^3 = f.

    Point update at (i,j): let s = u_neighbours_sum, then
       (4/h^2) u_ij - (1/h^2) s + u_ij^3 = f_ij
    -> u_ij^3 + (4/h^2) u_ij = f_ij + s/h^2
    -> cubic in u_ij with a = 4/h^2, b = f_ij + s/h^2
       => u_ij = real_root(a, b) using Cardano.
    """
    h2 = h * h
    a = 4.0 / h2
    Ny, Nx = u.shape
    ii, jj = np.ogrid[0:Ny, 0:Nx]
    parity = ((ii + jj) & 1).astype(bool)
    I = slice(1, -1)
    for _ in range(nu):
        for want in (0, 1):
            s = u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2]
            b_ = f[1:-1, 1:-1] + s / h2
            a_arr = np.full_like(b_, a)
            new = _cubic_root(a_arr, b_)
            mask = (parity[1:-1, 1:-1] == bool(want))
            u_int = u[I, I]
            u_int[mask] = new[mask]
            u[I, I] = u_int


def restrict_solution(u: np.ndarray) -> np.ndarray:
    """For solution restriction in FAS we inject the fine-grid coincident points
    (works fine on a vertex-centred grid where coarse points ARE fine points)."""
    Nf = u.shape[0]
    assert (Nf - 1) % 2 == 0
    return u[::2, ::2].copy()


def solve_coarse(u: np.ndarray, f: np.ndarray, h: float, tol=1e-11, itmax=500) -> None:
    """Coarsest-grid solve: just iterate nonlinear GS-RB to tight tolerance."""
    for _ in range(itmax):
        gs_rb_relax_nl(u, f, h, 1)
        r = residual_nl(u, f, h)
        if float(np.max(np.abs(r[1:-1, 1:-1]))) < tol:
            return


def fas_vcycle(u: np.ndarray, f: np.ndarray, h: float, level: int, max_level: int,
               nu_pre: int = 15, nu_post: int = 15) -> None:
    """FAS V-cycle per paper Algorithm 1 with gamma=1."""
    if level == max_level:
        solve_coarse(u, f, h)
        return
    # Pre-smooth
    gs_rb_relax_nl(u, f, h, nu_pre)
    # Residual on fine
    rh = residual_nl(u, f, h)
    # Restrict residual (full weighting) and solution (injection)
    r2h = restrict_fullweight(rh)
    u2h = restrict_solution(u)
    # Coarse-grid RHS: f_{2h} = r_{2h} + L_{2h}(u_{2h})
    f2h = np.zeros_like(u2h)
    f2h[1:-1, 1:-1] = r2h[1:-1, 1:-1] + L_apply(u2h, 2.0 * h)[1:-1, 1:-1]
    # Save initial coarse solution for FAS correction
    u2h_init = u2h.copy()
    # Recurse
    fas_vcycle(u2h, f2h, 2.0 * h, level + 1, max_level, nu_pre, nu_post)
    # Prolong correction
    e = prolong_bilinear(u2h - u2h_init)
    u[:] = u[:] + e
    # Post-smooth
    gs_rb_relax_nl(u, f, h, nu_post)


def run(depths=(1, 2, 3, 4, 5, 6), max_cycles=50, N=127, tol_abs=1e-10):
    rows = []
    summary = []
    print(f"# FAS nonlinear MG spot-check for Gmunu (paper Algorithm 1)")
    print(f"# Problem: -Delta u + u^3 = f (Poisson + cubic nonlinearity), N={N}")
    print(f"# Smoother: nonlinear GS-RB, nu=15+15;  Restriction=full-weighting;  Prolongation=bilinear")
    for k in depths:
        u, f, h, u_exact = make_problem_nl(N)
        r0 = residual_nl(u, f, h)
        r0_L1 = float(np.mean(np.abs(r0[1:-1, 1:-1])))
        history = [(0, r0_L1)]
        t0 = time.time()
        for it in range(1, max_cycles + 1):
            fas_vcycle(u, f, h, level=1, max_level=k)
            r = residual_nl(u, f, h)
            r_L1 = float(np.mean(np.abs(r[1:-1, 1:-1])))
            history.append((it, r_L1))
            if r_L1 < tol_abs:
                break
        dt = time.time() - t0
        err_L1 = float(np.mean(np.abs(u - u_exact)))
        red = history[-1][1] / r0_L1
        print(
            f"depth V{k:d}: {history[-1][0]:2d} cycles -> L1 res {history[-1][1]:.3e} "
            f"(red {red:.2e}, err_vs_exact {err_L1:.3e}, {dt:.2f}s)"
        )
        for it, r_L1 in history:
            rows.append({"depth": k, "iteration": it, "L1_residual": r_L1})
        summary.append({
            "depth": k, "cycles_run": history[-1][0],
            "L1_residual_final": history[-1][1], "reduction": red,
            "err_vs_exact_L1": err_L1, "wall_seconds": dt,
        })

    csv_path = os.path.join(HERE, "mg_fas_nonlinear.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["depth", "iteration", "L1_residual"])
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {csv_path}")
    j_path = os.path.join(HERE, "fas_nonlinear_summary.json")
    with open(j_path, "w") as fh:
        json.dump({
            "problem": "-Delta u + u^3 = f, u_exact = sin(pi x) sin(pi y)",
            "N_interior": N, "smoother": "nonlinear GS-RB nu_pre=nu_post=15",
            "restriction_residual": "full-weighting",
            "restriction_solution": "injection at coincident points",
            "prolongation": "bilinear",
            "cycle": "FAS V-cycle (paper Algorithm 1, gamma=1)",
            "tolerance_abs_L1_residual": tol_abs,
            "results": summary,
        }, fh, indent=2)
    print(f"Wrote {j_path}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 5))
        by_depth = {}
        for r in rows:
            by_depth.setdefault(r["depth"], []).append((r["iteration"], r["L1_residual"]))
        colors = plt.cm.plasma(np.linspace(0, 0.85, len(depths)))
        for c, k in zip(colors, depths):
            arr = np.array(by_depth[k])
            ax.semilogy(arr[:, 0], arr[:, 1], "o-", color=c, ms=3, label=f"V{k}")
        ax.set_xlabel("Number of iterations (FAS V-cycles)")
        ax.set_ylabel("L1 norm of residual")
        ax.set_title("FAS nonlinear multigrid (Gmunu Algorithm 1)\n"
                     "Test problem: -Delta u + u^3 = f")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()
        ax.set_xlim(0, max_cycles)
        png = os.path.join(HERE, "mg_fas_nonlinear.png")
        fig.tight_layout()
        fig.savefig(png, dpi=110)
        print(f"Wrote {png}")
    except Exception as e:
        print(f"plot skipped: {e}")


if __name__ == "__main__":
    run()
