#!/usr/bin/env python3
"""
Piecewise-constant restriction — exact match to Gmunu Fig 2a — spot check.

Gmunu paper §4.4 specifies the exact restriction stencil (Fig 2a): piecewise
constant restriction on a *cell-centred* grid, i.e. the coarse-cell value is
the arithmetic mean of the four child fine cells:
    u_coarse[I,J] = (1/4) * ( u[2I,2J] + u[2I+1,2J] + u[2I,2J+1] + u[2I+1,2J+1] )

The earlier spot-check used full-weighting on a vertex-centred grid, which is a
close but not identical operator.  This script implements piecewise-constant
restriction on a cell-centred layout and re-runs the linear V-cycle convergence
sweep, to confirm the paper's exact restriction choice yields the same
qualitative convergence (V6 in tens of iterations, V1 essentially frozen).

For simplicity we keep the model problem linear (-Delta u = f, u_exact =
sin(pi x) sin(pi y), homogeneous Dirichlet), on a cell-centred N x N interior
grid (N = 2^k so restriction chain is clean).

Outputs (this dir):
  mg_pwc_restriction.csv        residual per (depth, cycle)
  mg_pwc_restriction.png        semilog residual plot
  pwc_restriction_summary.json  final summary
"""
from __future__ import annotations
import os, sys, csv, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def make_problem_cc(N: int):
    """Cell-centred N x N grid on (0,1)^2, Dirichlet BC 0 (ghost cells).
    Cell centres at x_i = (i+0.5)/N, i=0..N-1.  We store a (N+2)x(N+2) array
    with ghosts at index 0 and N+1 mirroring the reflected boundary."""
    h = 1.0 / N
    xs = (np.arange(N) + 0.5) / N
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    u_exact = np.sin(np.pi * X) * np.sin(np.pi * Y)
    f = 2.0 * np.pi ** 2 * u_exact
    u_full = np.zeros((N + 2, N + 2))
    f_full = np.zeros((N + 2, N + 2))
    f_full[1:-1, 1:-1] = f
    return u_full, f_full, h, u_exact


def apply_dirichlet_ghosts(u: np.ndarray) -> None:
    """Reflect through the boundary at half-cell so that (u_ghost + u_int)/2 = 0."""
    u[0, :] = -u[1, :]
    u[-1, :] = -u[-2, :]
    u[:, 0] = -u[:, 1]
    u[:, -1] = -u[:, -2]


def residual_cc(u: np.ndarray, f: np.ndarray, h: float) -> np.ndarray:
    apply_dirichlet_ghosts(u)
    r = np.zeros_like(u)
    r[1:-1, 1:-1] = f[1:-1, 1:-1] - (
        4.0 * u[1:-1, 1:-1]
        - u[2:, 1:-1] - u[:-2, 1:-1]
        - u[1:-1, 2:] - u[1:-1, :-2]
    ) / (h * h)
    return r


def gs_rb_relax_cc(u: np.ndarray, f: np.ndarray, h: float, nu: int) -> None:
    h2 = h * h
    Ny, Nx = u.shape
    ii, jj = np.ogrid[0:Ny, 0:Nx]
    parity = ((ii + jj) & 1).astype(bool)
    I = slice(1, -1)
    for _ in range(nu):
        for want in (0, 1):
            apply_dirichlet_ghosts(u)
            new = 0.25 * (
                u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2]
                + h2 * f[1:-1, 1:-1]
            )
            mask = (parity[1:-1, 1:-1] == bool(want))
            u_int = u[I, I]
            u_int[mask] = new[mask]
            u[I, I] = u_int


def restrict_pwc_cc(r: np.ndarray) -> np.ndarray:
    """PIECEWISE-CONSTANT restriction on cell-centred data (paper Fig 2a).
    Input r is (N+2)x(N+2), interior N x N with N even.  Coarse interior is (N/2)x(N/2).
    Coarse value = mean of 2x2 block of fine cells."""
    N = r.shape[0] - 2
    assert N % 2 == 0
    Nc = N // 2
    r_int = r[1:-1, 1:-1]
    rc_int = 0.25 * (
        r_int[0::2, 0::2] + r_int[1::2, 0::2] + r_int[0::2, 1::2] + r_int[1::2, 1::2]
    )
    rc_full = np.zeros((Nc + 2, Nc + 2))
    rc_full[1:-1, 1:-1] = rc_int
    return rc_full


def prolong_pwc_cc(uc: np.ndarray) -> np.ndarray:
    """Bilinear prolongation on cell-centred data, from Nc to 2*Nc (paper Fig 2b).
    We use the standard cell-centred bilinear formula:
    each fine cell inherits a weighted mix of the 4 nearest coarse cell centres."""
    Nc = uc.shape[0] - 2
    N = 2 * Nc
    apply_dirichlet_ghosts(uc)
    # Fine cell (i,j) with i,j in [0,N) has centre at ((i+0.5)/N, (j+0.5)/N).
    # Nearest 4 coarse centres are indexed with a stagger of +/- 0.5 relative to
    # (i/2, j/2).  Standard cell-centred bilinear: weights (3/4,1/4)x(3/4,1/4).
    uf = np.zeros((N + 2, N + 2))
    uc_int = uc[1:-1, 1:-1]  # (Nc, Nc)
    # Build padded coarse to include one ring of ghosts (for boundary fine cells)
    ucp = uc  # already (Nc+2, Nc+2) with ghosts
    # For each of the 4 fine-cell offsets in a 2x2 block:
    #   fine (2I, 2J):    weights on (I-1,J-1), (I,J-1), (I-1,J), (I,J) = 1/16,3/16,3/16,9/16
    #   fine (2I+1, 2J):  weights on (I,J-1), (I+1,J-1), (I,J), (I+1,J)  = 3/16,1/16,9/16,3/16
    #   fine (2I, 2J+1):  weights on (I-1,J), (I,J), (I-1,J+1), (I,J+1)  = 3/16,9/16,1/16,3/16
    #   fine (2I+1, 2J+1):weights on (I,J), (I+1,J), (I,J+1), (I+1,J+1)  = 9/16,3/16,3/16,1/16
    # We use ucp with indices offset by +1 (ghost).
    # slices over I in [0, Nc), J in [0, Nc):
    A = ucp[0:Nc,   0:Nc  ]  # (I-1,J-1)
    B = ucp[1:Nc+1, 0:Nc  ]  # (I,  J-1)
    C = ucp[0:Nc,   1:Nc+1]  # (I-1,J  )
    D = ucp[1:Nc+1, 1:Nc+1]  # (I,  J  )   == uc_int
    E = ucp[2:Nc+2, 0:Nc  ]  # (I+1,J-1)
    F = ucp[2:Nc+2, 1:Nc+1]  # (I+1,J  )
    G = ucp[0:Nc,   2:Nc+2]  # (I-1,J+1)
    H = ucp[1:Nc+1, 2:Nc+2]  # (I,  J+1)
    K = ucp[2:Nc+2, 2:Nc+2]  # (I+1,J+1)
    # (2I,2J):
    uf[1:N+1:2, 1:N+1:2] = (A + 3*B + 3*C + 9*D) / 16.0
    # (2I+1,2J): uses B,E,D,F
    uf[2:N+1:2, 1:N+1:2] = (B + 3*E + 3*D + 9*F) / 16.0  # careful: pattern
    # actually recompute:  fine (2I+1,2J): weights on (I,J-1)=B (row shift +1),
    #   (I+1,J-1)=E, (I,J)=D, (I+1,J)=F  with weights 3,1,9,3
    uf[2:N+1:2, 1:N+1:2] = (3*B + 1*E + 9*D + 3*F) / 16.0
    # (2I,2J+1): weights on (I-1,J)=C, (I,J)=D, (I-1,J+1)=G, (I,J+1)=H  = 3,9,1,3
    uf[1:N+1:2, 2:N+1:2] = (3*C + 9*D + 1*G + 3*H) / 16.0
    # (2I+1,2J+1): (I,J)=D,(I+1,J)=F,(I,J+1)=H,(I+1,J+1)=K  = 9,3,3,1
    uf[2:N+1:2, 2:N+1:2] = (9*D + 3*F + 3*H + 1*K) / 16.0
    return uf


def solve_direct_cc(u: np.ndarray, f: np.ndarray, h: float, tol=1e-12, itmax=500):
    for _ in range(itmax):
        gs_rb_relax_cc(u, f, h, 1)
        r = residual_cc(u, f, h)
        if np.max(np.abs(r)) < tol:
            return


def vcycle_cc_pwc(u: np.ndarray, f: np.ndarray, h: float, level: int, max_level: int,
                  nu_pre: int = 15, nu_post: int = 15) -> None:
    if level == max_level:
        solve_direct_cc(u, f, h)
        return
    gs_rb_relax_cc(u, f, h, nu_pre)
    r = residual_cc(u, f, h)
    r_c = restrict_pwc_cc(r)
    u_c = np.zeros_like(r_c)
    vcycle_cc_pwc(u_c, r_c, 2.0 * h, level + 1, max_level, nu_pre, nu_post)
    e = prolong_pwc_cc(u_c)
    u[:] = u[:] + e
    gs_rb_relax_cc(u, f, h, nu_post)


def run(depths=(1, 2, 3, 4, 5, 6, 7), max_cycles=50, N=128, tol_abs=1e-10):
    rows = []
    summary = []
    print(f"# Piecewise-constant restriction spot-check (matches Gmunu Fig 2a exactly)")
    print(f"# Cell-centred N={N}x{N} interior grid; smoother=GS-RB 15+15; bilinear prolongation")
    for k in depths:
        u, f, h, u_exact = make_problem_cc(N)
        r0 = residual_cc(u, f, h)
        r0_L1 = float(np.mean(np.abs(r0[1:-1, 1:-1])))
        history = [(0, r0_L1)]
        t0 = time.time()
        for it in range(1, max_cycles + 1):
            vcycle_cc_pwc(u, f, h, level=1, max_level=k)
            r = residual_cc(u, f, h)
            r_L1 = float(np.mean(np.abs(r[1:-1, 1:-1])))
            history.append((it, r_L1))
            if r_L1 < tol_abs:
                break
        dt = time.time() - t0
        err_L1 = float(np.mean(np.abs(u[1:-1, 1:-1] - u_exact)))
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

    csv_path = os.path.join(HERE, "mg_pwc_restriction.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["depth", "iteration", "L1_residual"])
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {csv_path}")
    j_path = os.path.join(HERE, "pwc_restriction_summary.json")
    with open(j_path, "w") as fh:
        json.dump({
            "problem": "-Delta u = 2*pi^2 sin(pi x) sin(pi y), Dirichlet 0, cell-centred",
            "N_interior": N,
            "restriction": "piecewise-constant (paper Fig 2a): mean of 2x2 fine-cell block",
            "prolongation": "bilinear on cell-centred (paper Fig 2b analogue)",
            "smoother": "GS-RB nu_pre=nu_post=15",
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
        colors = plt.cm.cividis(np.linspace(0, 0.9, len(depths)))
        for c, k in zip(colors, depths):
            arr = np.array(by_depth[k])
            ax.semilogy(arr[:, 0], arr[:, 1], "o-", color=c, ms=3, label=f"V{k}")
        ax.set_xlabel("V-cycle iteration")
        ax.set_ylabel("L1 norm of residual")
        ax.set_title("Piecewise-constant restriction (Gmunu Fig 2a)\n"
                     "Cell-centred MG on 2D Poisson")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()
        ax.set_xlim(0, max_cycles)
        png = os.path.join(HERE, "mg_pwc_restriction.png")
        fig.tight_layout()
        fig.savefig(png, dpi=110)
        print(f"Wrote {png}")
    except Exception as e:
        print(f"plot skipped: {e}")


if __name__ == "__main__":
    run()
