"""
2D non-overlapping Schwarz for the Helmholtz model problem (paper eq. 6.1):

  -Δu - ω² u = 0       in (0,1)x(0,1)            (error equation: f = 0)
            u = 0       on y = 0, y = 1           (Dirichlet top/bottom)
   ∂u/∂x - iω u = 0     on x = 0
  -∂u/∂x - iω u = 0     on x = 1                  (1st-order radiation)

Split the unit square at x = 1/2 into Ω1 = [0,1/2]x[0,1] and Ω2 = [1/2,1]x[0,1].
Use a uniform N x N nodal finite-difference grid; standard 5-point Laplacian.
Sub-domain solves are direct (scipy sparse LU) since the matrices are small.

We compare three transmission conditions on the interface x = 1/2:
  classical : Dirichlet  -- u1 = u2  (paper "classical Schwarz w/o overlap" -> won't converge)
  robin     : Despres   --   ∂_n u_j + i ω u_j  = same from neighbor
  oo0       : optimized order-0 -- ∂_n u_j + (p* + i q*) u_j = same from neighbor

We measure ITERATION COUNT to drive the relative interface residual below 1e-6,
matching paper Table 6.1 (iterative columns) for the model problem.

Interface fluxes are stored as the "λ" auxiliary variables (paper eq. 5.2):
    λ1^n = -∂u2^n/∂n2 + S1(u2^n) on Γ12        (used as Robin RHS for Ω1)
    λ2^n = -∂u1^n/∂n1 + S2(u1^n) on Γ12        (used as Robin RHS for Ω2)

We discretize the Robin condition ∂_n u + s u = g at the interface using a one-sided
second-order finite difference, which keeps things stable and avoids ghost nodes.
The interface unknowns belong to BOTH subdomains as their respective boundary rows.
"""

from __future__ import annotations
import json
import math
import os
import time
from dataclasses import dataclass, field, asdict
from typing import Literal

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla


# --------------------- subdomain builder ---------------------

def build_subdomain(nx: int, ny: int, hx: float, hy: float, omega: float,
                    left_bc: Literal["robin_omega", "dirichlet"],
                    right_bc: Literal["robin_omega", "interface", "dirichlet"],
                    interface_side: Literal["left", "right"],
                    s_interface: complex,
                    ) -> sp.csc_matrix:
    """Build a 5-point complex Helmholtz operator on an nx-by-ny nodal grid using
    GHOST-POINT centered finite differences for all Robin/radiation BCs.

    Centered ghost-point BC discretization for ∂_n u + s u = g at the left boundary
    (outward normal = -e_x), where u_{-1} is the ghost:
        -(u_1 - u_{-1})/(2 hx) + s u_0 = g
    Combined with the interior PDE at i=0 (which uses u_{-1}):
        -(u_1 - 2 u_0 + u_{-1})/hx^2 - (...y...) - ω^2 u_0 = f_0
    Eliminate u_{-1} = u_1 + 2 hx (g - s u_0) -> ghost in PDE row.
    Net row at i=0:
        -2/hx^2 u_1 + (2/hx^2 + ...y... - ω^2 + 2 s/hx) u_0 = f_0 + 2/hx g
    For interface BC the RHS contribution is held in the per-iter rhs vector.

    Index ordering: column-major flatten, i + nx * j.

    Top/bottom (y=0, y=ny-1) are always Dirichlet u = 0.
    """
    N = nx * ny

    def idx(i, j):
        return i + nx * j

    rows, cols, data = [], [], []

    inv_hx2 = 1.0 / (hx * hx)
    inv_hy2 = 1.0 / (hy * hy)
    diag_base = 2.0 * inv_hx2 + 2.0 * inv_hy2 - omega ** 2 + 0j

    for j in range(ny):
        for i in range(nx):
            k = idx(i, j)
            # top/bottom Dirichlet u=0
            if j == 0 or j == ny - 1:
                rows.append(k); cols.append(k); data.append(1.0 + 0j)
                continue

            # determine x-direction BC contributions via ghost-point method
            #
            # General PDE row (interior):
            #   -inv_hx2 (u_{i+1} - 2 u_i + u_{i-1}) - inv_hy2 (u_{j+1} - 2 u_i + u_{j-1}) - ω^2 u_i = f_i
            #
            # At i=0 the ghost u_{-1} is eliminated using the BC at x=0 with outward
            # normal -e_x: ∂_n u + s u = g  =>  -(u_1 - u_{-1})/(2 hx) + s u_0 = g
            #   =>  u_{-1} = u_1 + 2 hx (g - s u_0)
            # Substituting into the PDE row gives:
            #   (-2 inv_hx2) u_1 + (diag_base + 2 s / hx) u_0 + ...y... = f_0 + 2 g / hx
            #
            # At i=nx-1 the ghost u_{nx} is eliminated using BC at x=1 with outward
            # normal +e_x: ∂_n u + s u = g  =>  (u_{nx} - u_{nx-2})/(2 hx) + s u_{nx-1} = g
            #   =>  u_{nx} = u_{nx-2} + 2 hx (g - s u_{nx-1})
            # Substituting:
            #   (-2 inv_hx2) u_{nx-2} + (diag_base + 2 s / hx) u_{nx-1} + ...y... = f_{nx-1} + 2 g / hx

            def x_bc_side(side: str):
                """Returns (s_bc, is_interface)."""
                if side == "left":
                    if interface_side == "left":
                        return s_interface, True
                    # paper:  ∂u/∂x - i ω u = 0   <=>  -(-∂u/∂x) - i ω u = 0
                    # in normal form:  ∂_n u + s u = 0 with ∂_n = -∂_x:
                    # -∂_x u - i ω u = 0  -> NOT what the paper writes.
                    # paper writes  ∂u/∂x - i ω u = 0 at x=0, which is  -∂_n u - i ω u = 0,
                    # i.e.  ∂_n u + i ω u = 0  -> s_left = i ω.
                    return 1j * omega, False
                else:
                    if interface_side == "right":
                        return s_interface, True
                    # paper at x=1:  -∂u/∂x - i ω u = 0, normal = +e_x:
                    # ∂_n u = +∂_x u, so  -∂_n u - i ω u = 0  ->  ∂_n u + i ω u = 0  -> s_right = i ω.
                    return 1j * omega, False

            # collect y-direction stencil entries (interior in y guaranteed by j check above)
            y_entries = [(idx(i, j - 1), -inv_hy2), (idx(i, j + 1), -inv_hy2)]

            if i == 0:
                s_bc, _ = x_bc_side("left")
                rows += [k, k] + [e[0] for e in y_entries]
                cols += [k, idx(1, j)] + [e[0] for e in y_entries]
                data += [diag_base + 2.0 * s_bc / hx,
                         -2.0 * inv_hx2 + 0j] + [e[1] + 0j for e in y_entries]
            elif i == nx - 1:
                s_bc, _ = x_bc_side("right")
                rows += [k, k] + [e[0] for e in y_entries]
                cols += [k, idx(nx - 2, j)] + [e[0] for e in y_entries]
                data += [diag_base + 2.0 * s_bc / hx,
                         -2.0 * inv_hx2 + 0j] + [e[1] + 0j for e in y_entries]
            else:
                rows += [k, k, k, k, k]
                cols += [idx(i - 1, j), idx(i + 1, j),
                         idx(i, j - 1), idx(i, j + 1), k]
                data += [-inv_hx2 + 0j,
                         -inv_hx2 + 0j,
                         -inv_hy2 + 0j,
                         -inv_hy2 + 0j,
                         diag_base]

    A = sp.csc_matrix((data, (rows, cols)), shape=(N, N), dtype=complex)
    return A


def interface_indices(nx: int, ny: int, side: Literal["left", "right"]):
    """Return the flat indices of the interface column on this subdomain (one per y-row,
    interior y nodes only, j=1..ny-2)."""
    if side == "left":
        i = 0
    else:
        i = nx - 1
    return np.array([i + nx * j for j in range(1, ny - 1)], dtype=int)


# --------------------- Schwarz driver ---------------------

@dataclass
class RunResult:
    method: str
    N: int
    h: float
    omega: float
    s_param: complex
    converged: bool
    iters: int
    final_residual: float
    history: list = field(default_factory=list)
    elapsed_sec: float = 0.0


def schwarz_solve(N: int, omega: float, method: str,
                  s_param: complex,
                  tol: float = 1e-6, maxiter: int = 2000,
                  initial_random_seed: int = 0,
                  verbose: bool = False) -> RunResult:
    """Iterate the parallel Schwarz method on the error equation (f = 0).

    Convergence is measured by the relative change in the interface trace.
    """
    # global grid: (N+1) x (N+1) nodes, h = 1/N
    h = 1.0 / N
    # split at x = 1/2 -> nx-per-subdomain = N/2 + 1 nodes (shared interface point)
    if N % 2 != 0:
        raise ValueError("N must be even so x=1/2 is on the grid")
    nx = N // 2 + 1
    ny = N + 1
    hx = h
    hy = h

    # Build subdomain matrices ONCE
    if method == "classical":
        # Dirichlet trace transmission on the interface. We implement this as
        # a Robin-type row with s_param == "very large" doesn't work; instead
        # we override the interface row to be u = g. Equivalent to setting s -> oo.
        # We'll build the matrix with a placeholder Robin and patch the interface row.
        s1 = 1.0 + 0j   # placeholder
        s2 = 1.0 + 0j
    else:
        s1 = s_param
        s2 = s_param  # symmetric: S1 = S2 = same Robin coef p+iq for the LEFT/RIGHT subdomain

    A1 = build_subdomain(nx, ny, hx, hy, omega,
                         left_bc="robin_omega", right_bc="interface",
                         interface_side="right", s_interface=s1)
    A2 = build_subdomain(nx, ny, hx, hy, omega,
                         left_bc="dirichlet" if False else "robin_omega",  # left of subdom 2 is the interface, set via interface_side
                         right_bc="robin_omega",
                         interface_side="left", s_interface=s2)
    # Wait: Ω2's left boundary is the interface; we passed interface_side="left" so the
    # builder uses the interface Robin row at x=0 of Ω2 (overriding left_bc). Good.

    if method == "classical":
        # patch interface rows of both subdomains to enforce u = g (Dirichlet).
        # interface index in Ω1 is i=nx-1; in Ω2 is i=0; for interior j.
        idx1 = interface_indices(nx, ny, "right")
        idx2 = interface_indices(nx, ny, "left")
        A1 = A1.tolil()
        for k in idx1:
            A1.rows[k] = [k]
            A1.data[k] = [1.0 + 0j]
        A1 = A1.tocsc()
        A2 = A2.tolil()
        for k in idx2:
            A2.rows[k] = [k]
            A2.data[k] = [1.0 + 0j]
        A2 = A2.tocsc()

    solve1 = spla.splu(A1)
    solve2 = spla.splu(A2)

    N1 = nx * ny
    N2 = nx * ny

    # Random initial trace on the interface (interior y nodes)
    rng = np.random.default_rng(initial_random_seed)
    ny_iface = ny - 2

    # Solution arrays initialized random on interface, zero elsewhere
    u1 = np.zeros(N1, dtype=complex)
    u2 = np.zeros(N2, dtype=complex)

    idx1 = interface_indices(nx, ny, "right")  # x = 1/2 nodes in Ω1
    idx2 = interface_indices(nx, ny, "left")   # x = 1/2 nodes in Ω2
    # near-interface (i = nx-2 in Ω1, i = 1 in Ω2) for finite-diff fluxes
    idx1_in = np.array([nx - 2 + nx * j for j in range(1, ny - 1)], dtype=int)
    idx1_in2 = np.array([nx - 3 + nx * j for j in range(1, ny - 1)], dtype=int)
    idx2_in = np.array([1 + nx * j for j in range(1, ny - 1)], dtype=int)
    idx2_in2 = np.array([2 + nx * j for j in range(1, ny - 1)], dtype=int)

    # Initialize the iteration with random interface values + zero interior
    # by setting initial λ_1, λ_2 random.
    lam1 = rng.standard_normal(ny_iface) + 1j * rng.standard_normal(ny_iface)
    lam2 = rng.standard_normal(ny_iface) + 1j * rng.standard_normal(ny_iface)
    lam1 /= np.linalg.norm(lam1)
    lam2 /= np.linalg.norm(lam2)

    history = []
    converged = False

    t0 = time.time()

    # Pre-compute scaling for ghost-point RHS contribution at interface rows.
    # For a row at i=0 of Ω2 with ghost-point centered Robin, RHS contribution is +2 g / hx.
    # Same for i=nx-1 of Ω1. classical (Dirichlet) keeps RHS = g (the identity row).
    ghost_scale = 2.0 / hx

    # Discrete transmission via the Lions "dual variable" trick.
    # Each subdomain enforces  ∂_n u_j + s_j u_j = g_j  on Γ.
    # The CONSISTENCY condition between the two subdomain BCs (which together
    # encode  u_1 = u_2  AND  ∂_n1 u_1 = -∂_n2 u_2  on Γ) is
    #     g_1 + g_2 = (s_1 + s_2) u_local
    # so the natural update (eq. (5.2) of the paper, discrete form) is
    #     g_1^{n+1} = (s_1 + s_2) u_2^n |_Γ  -  g_2^n
    #     g_2^{n+1} = (s_1 + s_2) u_1^n |_Γ  -  g_1^n
    # which avoids any explicit normal-derivative reconstruction at the interface
    # and is the standard formulation that gives the analytic ρ(k) at the discrete
    # level (modulo small O(h) corrections).  See Lions (1990), Despres (1991),
    # and the paper's section 5.1 (eq. 5.2).
    g1_cur = lam1.copy() if method != "classical" else None
    g2_cur = lam2.copy() if method != "classical" else None
    s_sum = s1 + s2  # both Ω1 and Ω2 use the same s here

    for it in range(1, maxiter + 1):
        # build RHS for subdomain 1
        rhs1 = np.zeros(N1, dtype=complex)
        if method == "classical":
            # Dirichlet interface row:  u_iface = g = u2_old(iface)
            rhs1[idx1] = u2[idx2] if it > 1 else lam1
        else:
            rhs1[idx1] = ghost_scale * g1_cur

        u1 = solve1.solve(rhs1)

        # build RHS for subdomain 2
        rhs2 = np.zeros(N2, dtype=complex)
        if method == "classical":
            rhs2[idx2] = u1[idx1] if it > 1 else lam2
        else:
            rhs2[idx2] = ghost_scale * g2_cur

        u2 = solve2.solve(rhs2)

        # Update g_1, g_2 by Lions's dual-variable rule (Jacobi, both updated
        # from PRE-update values to mimic the parallel iteration).
        if method != "classical":
            g1_new = s_sum * u2[idx2] - g2_cur
            g2_new = s_sum * u1[idx1] - g1_cur
            g1_cur, g2_cur = g1_new, g2_new

        # Convergence metric for the error equation (f = 0, true solution u ≡ 0):
        # the error norm is simply ||(u1, u2)||.  We normalize by the initial random
        # interface seed (λ1, λ2) so the curve starts near 1.
        err = math.sqrt(float(np.vdot(u1, u1).real) + float(np.vdot(u2, u2).real))
        if it == 1:
            err0 = max(err, 1e-300)
        rel_err = err / err0
        history.append(rel_err)

        if verbose and (it < 6 or it % 20 == 0):
            print(f"  iter {it:4d}  rel_err = {rel_err:.3e}")

        if rel_err < tol:
            converged = True
            break

    elapsed = time.time() - t0
    return RunResult(method=method, N=N, h=h, omega=omega, s_param=s_param,
                     converged=converged, iters=it, final_residual=float(history[-1]),
                     history=history, elapsed_sec=elapsed)


# --------------------- driver ---------------------

def main():
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
    fig_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "figures"))
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    # Paper Table 6.1 setup: ω = 9.5π so ω lies between Fourier modes (k = nπ)
    # -> iterative method converges with ω_- = 9π, ω_+ = 10π
    omega = 9.5 * math.pi
    omega_minus = 9.0 * math.pi
    omega_plus = 10.0 * math.pi

    Ns = [24, 50, 100, 200]   # = 1/h ; paper goes to 800 but we cap for CPU time
    methods = ["classical", "robin", "oo0"]

    all_results = []
    gmres_results = []

    for N in Ns:
        h = 1.0 / N
        kmax = math.pi / h
        # OO0 optimal p* = q* (eq. 3.7)
        p_star = ((omega ** 2 - omega_minus ** 2) * (kmax ** 2 - omega ** 2)) ** 0.25 / math.sqrt(2)
        s_oo0 = p_star + 1j * p_star

        # GMRES-accelerated experiments (this is what the paper uses for its
        # Krylov columns of Table 6.1)
        for gmethod, gs in [("robin", 1j * omega), ("oo0", s_oo0)]:
            print(f"\n--- N = {N} GMRES on {gmethod} ---")
            try:
                gr = schwarz_gmres(N, omega, gmethod, gs, tol=1e-6, maxiter=400)
                print(f"  -> converged={gr.converged}  iters={gr.iters}  "
                      f"final={gr.final_residual:.3e}  elapsed={gr.elapsed_sec:.2f}s")
                gmres_results.append(gr)
            except Exception as e:
                print(f"  ! GMRES failed: {e}")

        for method in methods:
            print(f"\n=== N = {N} (h = 1/{N})  method = {method} ===")
            if method == "robin":
                s = 1j * omega
            elif method == "oo0":
                s = s_oo0
            else:
                s = 0.0 + 0j

            # classical Schwarz doesn't converge without overlap -> cap maxiter low
            # Robin (Despres) also stalls without Krylov for our discretization; cap it.
            # OO0 should converge in O(1/sqrt(h)) iters.
            if method == "classical":
                maxiter = 200
            elif method == "robin":
                maxiter = 600
            else:
                maxiter = 3000
            r = schwarz_solve(N, omega, method, s_param=s, tol=1e-6, maxiter=maxiter,
                              initial_random_seed=42, verbose=True)
            print(f"  -> converged={r.converged}  iters={r.iters}  "
                  f"final={r.final_residual:.3e}  elapsed={r.elapsed_sec:.2f}s")
            all_results.append(r)

    # JSON dump
    serialized = []
    for r in all_results:
        d = asdict(r)
        d["s_param"] = str(d["s_param"])
        # truncate history
        d["history"] = [float(x) for x in d["history"]]
        serialized.append(d)
    gmres_serialized = []
    for r in gmres_results:
        d = asdict(r); d["s_param"] = str(d["s_param"])
        d["history"] = [float(x) for x in d["history"]]
        gmres_serialized.append(d)

    with open(os.path.join(out_dir, "osh_2d_results.json"), "w") as f:
        json.dump({
            "omega": omega,
            "omega_minus": omega_minus,
            "omega_plus": omega_plus,
            "Ns": Ns,
            "runs": serialized,
            "gmres_runs": gmres_serialized,
        }, f, indent=2)

    # Make Table 6.1-style summary CSV
    import csv
    rows = []
    for N in Ns:
        row = {"h": f"1/{N}"}
        for m in methods:
            r = next((x for x in all_results if x.N == N and x.method == m), None)
            row[m + "_iters"] = r.iters if r else None
            row[m + "_converged"] = r.converged if r else None
        rows.append(row)
    with open(os.path.join(out_dir, "table_iterations.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # Plot convergence histories per N
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, len(Ns), figsize=(4 * len(Ns), 3.6), sharey=True)
    for ax, N in zip(np.atleast_1d(axes), Ns):
        for method, color in zip(methods, ["tab:gray", "tab:red", "tab:blue"]):
            r = next((x for x in all_results if x.N == N and x.method == method), None)
            if r and len(r.history) > 0:
                ax.semilogy(r.history, label=f"{method} (it={r.iters}{'' if r.converged else '*'})",
                            color=color)
        ax.set_title(f"N = {N} (h = 1/{N})")
        ax.set_xlabel("iteration")
        ax.set_ylabel("interface jump (rel)")
        ax.axhline(1e-6, color="k", lw=0.5, ls="--", alpha=0.5)
        ax.grid(True, which="both", alpha=0.3)
        ax.legend(fontsize=8)
    fig.suptitle(f"2D Helmholtz non-overlap Schwarz convergence (ω = 9.5π)", y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(fig_dir, "fig_2d_convergence.png"), dpi=140,
                bbox_inches="tight")
    plt.close(fig)

    # Iters-vs-h plot (Table 6.1 visualization)
    fig, ax = plt.subplots(figsize=(6, 4))
    h_arr = np.array([1.0 / N for N in Ns])
    for method, color in zip(methods, ["tab:gray", "tab:red", "tab:blue"]):
        iters = []
        for N in Ns:
            r = next((x for x in all_results if x.N == N and x.method == method), None)
            iters.append(r.iters if (r and r.converged) else np.nan)
        ax.loglog(h_arr, iters, "o-", label=method, color=color)
    # reference slope h^{-1/2} for OO0 from Theorem 4.1: iters ~ -log(tol)/(1-rho) ~ 1/sqrt(h)
    # so iters ~ C h^{-1/2}
    ax.loglog(h_arr, 16 / np.sqrt(h_arr) * h_arr[0] ** 0.5, "k--", alpha=0.5,
              label="O(h^{-1/2})  (OO0 theory)")
    ax.set_xlabel("h")
    ax.set_ylabel("iterations to 1e-6")
    ax.set_title("Iteration count vs h (reproducing paper Table 6.1, iterative columns)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(fig_dir, "fig_2d_iters_vs_h.png"), dpi=140)
    plt.close(fig)

    print("\n=== TABLE (iterative; * = did not reach 1e-6) ===")
    print(f"{'h':>10}  {'classical':>12}  {'Robin':>10}  {'OO0':>10}")
    for N in Ns:
        cells = []
        for m in methods:
            r = next((x for x in all_results if x.N == N and x.method == m), None)
            mark = "" if r.converged else "*"
            cells.append(f"{r.iters}{mark}")
        print(f"1/{N:<8}  {cells[0]:>12}  {cells[1]:>10}  {cells[2]:>10}")


# --------------------- GMRES-accelerated variant ---------------------

def schwarz_gmres(N: int, omega: float, method: str, s_param: complex,
                  tol: float = 1e-6, maxiter: int = 400) -> RunResult:
    """Apply GMRES to the substructured λ-system implicitly defined by the
    Schwarz iteration.

    Let T be the linear map  (g_1, g_2) -> (g_1', g_2')  defined by:
      solve Ω1 with Robin RHS g_1; solve Ω2 with Robin RHS g_2;
      g_1' = (s1+s2) u_2|_Γ - g_2;  g_2' = (s1+s2) u_1|_Γ - g_1.
    A fixed point of T is the converged Schwarz state. For the error problem
    (f=0), the fixed point is (g_1, g_2) = (0, 0). The corresponding linear
    system to solve is  (I - T) [g] = 0 ; but for f ≠ 0 the RHS is the
    contribution from the source term. Since we drive f = 0 and start from a
    random initial λ, what we want is to find the kernel direction — i.e.
    converge λ to zero. For that, GMRES on (I-T)λ = 0 is degenerate; the
    right thing is to drive the *consistency residual* to zero, which equals
    λ itself after applying (I-T) on a perturbation. Concretely we apply GMRES
    to (I-T) on a *random* RHS and measure how many iters it needs to reach
    a small residual; that mirrors what the paper does, which is to use GMRES
    on the substructured Schwarz system.
    """
    h = 1.0 / N
    nx = N // 2 + 1
    ny = N + 1
    hx = hy = h

    if method == "classical":
        # not used for GMRES variant
        raise NotImplementedError("classical GMRES not implemented")

    s1 = s2 = s_param
    A1 = build_subdomain(nx, ny, hx, hy, omega, "robin_omega", "interface",
                         "right", s1)
    A2 = build_subdomain(nx, ny, hx, hy, omega, "robin_omega", "interface",
                         "left", s2)
    solve1 = spla.splu(A1)
    solve2 = spla.splu(A2)

    idx1 = interface_indices(nx, ny, "right")
    idx2 = interface_indices(nx, ny, "left")
    ny_iface = ny - 2
    ghost_scale = 2.0 / hx
    s_sum = s1 + s2
    N1 = nx * ny; N2 = nx * ny

    def apply_T(g_flat):
        g1 = g_flat[:ny_iface]
        g2 = g_flat[ny_iface:]
        rhs1 = np.zeros(N1, dtype=complex); rhs1[idx1] = ghost_scale * g1
        rhs2 = np.zeros(N2, dtype=complex); rhs2[idx2] = ghost_scale * g2
        u1 = solve1.solve(rhs1)
        u2 = solve2.solve(rhs2)
        g1n = s_sum * u2[idx2] - g2
        g2n = s_sum * u1[idx1] - g1
        return np.concatenate([g1n, g2n])

    n_iface = 2 * ny_iface
    op = spla.LinearOperator((n_iface, n_iface), matvec=lambda v: v - apply_T(v),
                             dtype=complex)

    rng = np.random.default_rng(42)
    rhs = rng.standard_normal(n_iface) + 1j * rng.standard_normal(n_iface)
    rhs /= np.linalg.norm(rhs)

    iters_count = [0]
    history = []
    def cb(xk):
        iters_count[0] += 1
        # for scipy 1.4+, xk may be the iterate; we just count

    t0 = time.time()
    sol, info = spla.gmres(op, rhs, rtol=tol, restart=50, maxiter=maxiter,
                           callback=cb, callback_type="pr_norm")
    elapsed = time.time() - t0
    final_res = float(np.linalg.norm(rhs - op @ sol))
    converged = (info == 0)
    return RunResult(method=method + "_gmres", N=N, h=h, omega=omega,
                     s_param=s_param, converged=converged,
                     iters=iters_count[0], final_residual=final_res,
                     history=[final_res], elapsed_sec=elapsed)


if __name__ == "__main__":
    main()
