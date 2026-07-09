#!/usr/bin/env python3
"""
Independent multigrid Poisson spot-check for Gmunu (Cheong+Lin+Li 2020, arXiv:2001.05723).

Gmunu solves the elliptic xCFC/CFC metric equations in numerical relativity using
a Full Approximation Scheme (FAS) V-cycle multigrid with:
  - red-black Gauss-Seidel smoother, 15 relaxations
  - piecewise constant restriction
  - bilinear prolongation
  - L1-norm residual convergence criterion

The main quantitative claim we spot-check (Figure 11 of the paper):
  "V6 converges in ~40 iterations, V1 (single-grid Gauss-Seidel) needs O(10^5)"

We are not solving the general-relativistic xCFC system — that requires the full
matter/hydro stack. Instead we solve a linear 2D Poisson problem
    -Delta u = f  on the unit square, Dirichlet BC = 0,
with a known analytic solution u(x,y) = sin(pi x) sin(pi y) so f = 2 pi^2 sin sin.

Grid: 257x257 cell-centered (2^8+1 vertex-equivalent -> 8 grid levels available).
Smoother: red-black Gauss-Seidel, nu = 15 pre + 15 post.
Restriction: full-weighting (close analogue of the piecewise-constant restriction
used in the paper; both are conservative 4-point averages of same order).
Prolongation: bilinear.
Coarsest-grid solve: same Gauss-Seidel smoother iterated to tolerance.

We compare V1 (essentially pure GS on the fine grid) vs V-cycles of depth 2..7
in terms of L1-norm residual reduction per cycle.

Output written next to this script:
  mg_poisson_convergence.csv       (residuals per cycle, per depth)
  mg_poisson_convergence.png       (plot analogous to paper Figure 11)
"""

from __future__ import annotations
import numpy as np
import csv, time, sys, os

RNG = np.random.default_rng(0)
HERE = os.path.dirname(os.path.abspath(__file__))


def make_problem(N: int):
    """N = number of interior points per side (so grid is N+2 including ghosts).
    Returns (u_guess, f, h, u_exact)."""
    # N interior => total grid N+2 including boundary. We want (N+1) = 2^k for
    # depth-k V-cycles, so pass N = 2^k - 1 (e.g. 127 -> full 129 = 2^7+1).
    h = 1.0 / (N + 1)
    xs = np.linspace(0.0, 1.0, N + 2)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    u_exact = np.sin(np.pi * X) * np.sin(np.pi * Y)
    f = 2.0 * np.pi ** 2 * np.sin(np.pi * X) * np.sin(np.pi * Y)
    # Dirichlet BC = 0 (matches sin at edges).
    u = np.zeros_like(f)
    return u, f, h, u_exact


def apply_L(u: np.ndarray, h: float) -> np.ndarray:
    """L u = -Delta u, standard 5-point stencil. Returns array same shape as u;
    boundary rows/cols are left as zeros (they belong to BC)."""
    Lu = np.zeros_like(u)
    Lu[1:-1, 1:-1] = (
        4.0 * u[1:-1, 1:-1]
        - u[2:, 1:-1] - u[:-2, 1:-1]
        - u[1:-1, 2:] - u[1:-1, :-2]
    ) / (h * h)
    return Lu


def residual(u: np.ndarray, f: np.ndarray, h: float) -> np.ndarray:
    r = np.zeros_like(u)
    r[1:-1, 1:-1] = f[1:-1, 1:-1] - (
        4.0 * u[1:-1, 1:-1]
        - u[2:, 1:-1] - u[:-2, 1:-1]
        - u[1:-1, 2:] - u[1:-1, :-2]
    ) / (h * h)
    return r


def gs_rb_relax(u: np.ndarray, f: np.ndarray, h: float, nu: int) -> None:
    """In-place red-black Gauss-Seidel on interior points.  Vectorized."""
    h2 = h * h
    Ny, Nx = u.shape
    # Interior parity masks (computed once by caller via cache would be better,
    # but arrays are small).
    ii, jj = np.ogrid[0:Ny, 0:Nx]
    parity = ((ii + jj) & 1).astype(bool)
    # Interior slices
    I = slice(1, -1)
    for _ in range(nu):
        for want in (0, 1):
            # New candidate values at interior points
            new = 0.25 * (
                u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2]
                + h2 * f[1:-1, 1:-1]
            )
            mask = (parity[1:-1, 1:-1] == bool(want))
            u_int = u[I, I]
            u_int[mask] = new[mask]
            u[I, I] = u_int


def restrict_fullweight(r: np.ndarray) -> np.ndarray:
    """Full-weighting restriction on a cell-vertex grid: (N_fine-1)/2+1 -> N_coarse."""
    Nf = r.shape[0]
    assert (Nf - 1) % 2 == 0, f"restrict requires (N-1) even, got {Nf}"
    Nc = (Nf - 1) // 2 + 1
    rc = np.zeros((Nc, Nc), dtype=r.dtype)
    # Interior full-weighting
    rc[1:-1, 1:-1] = (
        4.0 * r[2:-2:2, 2:-2:2]
        + 2.0 * (r[1:-3:2, 2:-2:2] + r[3:-1:2, 2:-2:2]
                  + r[2:-2:2, 1:-3:2] + r[2:-2:2, 3:-1:2])
        + (r[1:-3:2, 1:-3:2] + r[1:-3:2, 3:-1:2]
           + r[3:-1:2, 1:-3:2] + r[3:-1:2, 3:-1:2])
    ) / 16.0
    return rc


def prolong_bilinear(uc: np.ndarray) -> np.ndarray:
    """Bilinear prolongation from Nc to Nf = 2*(Nc-1)+1."""
    Nc = uc.shape[0]
    Nf = 2 * (Nc - 1) + 1
    uf = np.zeros((Nf, Nf), dtype=uc.dtype)
    # Coincident points
    uf[::2, ::2] = uc
    # Horizontal midpoints
    uf[::2, 1::2] = 0.5 * (uc[:, :-1] + uc[:, 1:])
    # Vertical midpoints
    uf[1::2, ::2] = 0.5 * (uc[:-1, :] + uc[1:, :])
    # Cell centers
    uf[1::2, 1::2] = 0.25 * (
        uc[:-1, :-1] + uc[1:, :-1] + uc[:-1, 1:] + uc[1:, 1:]
    )
    return uf


def solve_direct(u: np.ndarray, f: np.ndarray, h: float, tol=1e-12, itmax=500) -> None:
    """Coarsest-grid solve: just iterate GS-RB hard.  For 3x3 or 5x5 this is essentially exact."""
    for _ in range(itmax):
        gs_rb_relax(u, f, h, 1)
        r = residual(u, f, h)
        if np.max(np.abs(r)) < tol:
            return


def vcycle(u: np.ndarray, f: np.ndarray, h: float, level: int, max_level: int,
           nu_pre: int = 15, nu_post: int = 15) -> None:
    """FAS-style linear V-cycle.  Since problem is linear the coarse eq is on the
    correction e_H (not full u).  We use the standard linear-MG form."""
    if level == max_level:
        solve_direct(u, f, h)
        return
    # Pre-smooth
    gs_rb_relax(u, f, h, nu_pre)
    # Residual
    r = residual(u, f, h)
    # Restrict residual
    r_c = restrict_fullweight(r)
    # Coarse-grid correction
    u_c = np.zeros_like(r_c)
    vcycle(u_c, r_c, 2.0 * h, level + 1, max_level, nu_pre, nu_post)
    # Prolong correction
    e = prolong_bilinear(u_c)
    u[:] = u[:] + e
    # Post-smooth
    gs_rb_relax(u, f, h, nu_post)


def run(depth_levels=(1, 2, 3, 4, 5, 6, 7), n_cycles=50, N=127):
    """depth=1 means one grid (pure smoother, no coarse correction).
       depth=k means k levels total, i.e. one V-cycle recurses k-1 times."""
    rows = []
    print(f"# Independent MG Poisson spot-check for Gmunu (paper Fig 11)")
    print(f"# Fine grid: {N}x{N}, nu_pre = nu_post = 15 GS-RB relax, full-weighting + bilinear")
    print(f"# depth k=1 => pure GS on the fine grid (no coarsening), matches paper's 'V1'")
    for k in depth_levels:
        u, f, h, u_exact = make_problem(N)
        r0 = residual(u, f, h)
        # First residual is with u=0 so L1 residual = L1(f)
        r_L1 = float(np.mean(np.abs(r0[1:-1, 1:-1])))
        history = [(0, r_L1)]
        t0 = time.time()
        for it in range(1, n_cycles + 1):
            vcycle(u, f, h, level=1, max_level=k)
            r = residual(u, f, h)
            r_L1 = float(np.mean(np.abs(r[1:-1, 1:-1])))
            history.append((it, r_L1))
            if r_L1 < 1e-10:
                break
        t = time.time() - t0
        final_it = history[-1][0]
        final_res = history[-1][1]
        red = final_res / history[0][1]
        # Solution error vs analytic
        err_L1 = float(np.mean(np.abs(u - u_exact)))
        print(f"depth V{k:d}: {final_it:3d} cycles -> L1 residual {final_res:.3e} "
              f"(reduction {red:.2e}, err_vs_exact {err_L1:.3e}, {t:.2f}s)")
        for it, r_L1 in history:
            rows.append({"depth": k, "iteration": it, "L1_residual": r_L1})

    # Write CSV
    csv_path = os.path.join(HERE, "mg_poisson_convergence.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["depth", "iteration", "L1_residual"])
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {csv_path}")

    # Plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 5))
        colors = plt.cm.viridis(np.linspace(0, 0.9, len(depth_levels)))
        by_depth = {}
        for r in rows:
            by_depth.setdefault(r["depth"], []).append((r["iteration"], r["L1_residual"]))
        for c, k in zip(colors, depth_levels):
            arr = np.array(by_depth[k])
            ax.semilogy(arr[:, 0], arr[:, 1], "o-", color=c, ms=3, label=f"V{k}")
        ax.set_xlabel("Number of iterations (V-cycles)")
        ax.set_ylabel("L1 norm of residual")
        ax.set_title("Independent MG Poisson spot-check\n(analog of Gmunu Fig 11)")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()
        ax.set_xlim(0, n_cycles)
        png = os.path.join(HERE, "mg_poisson_convergence.png")
        fig.tight_layout()
        fig.savefig(png, dpi=110)
        print(f"Wrote {png}")
    except Exception as e:
        print(f"plot skipped: {e}")


if __name__ == "__main__":
    run()
