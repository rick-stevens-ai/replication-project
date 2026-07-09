"""
Re-pass coverage extension for Gander, Magoulès, Nataf (2002):
"Optimized Schwarz Methods without Overlap for the Helmholtz Equation."

Pass-1 covered the per-mode ρ formulas (eqs. 2.6, 3.2, 3.17), OO0/OO2 optimal
parameters (Thms 3.1, 3.10), the OO0 √h asymptotic (Thm 4.1), and the 2D PDE
behavior of classical / Robin / OO0 with GMRES (Table 6.1 OO0-Krylov +
Robin-Krylov columns).

This re-pass adds:

  R1.  Theorem 4.2 (OO2 asymptotics) — per-mode numerical check that
       1 - ρ_p ~ ω^{-1/4} for propagating modes and 1 - ρ_e ~ √h for
       evanescent modes, matching the analytic forms (4.2) and (4.3).

  R2.  Table 6.2  — ω = 10π directly on a problem frequency. Iterative
       methods are theoretically stuck (ρ(k=ω)=1); only Krylov should
       converge. We reproduce the GMRES iteration counts for OO0 and the
       Taylor (Robin) families at h = 1/50, 1/100, 1/200.

  R3.  Figure 6.2 / 6.3 robustness — sample iteration count as a function of
       the OO0 parameter (p, q) and confirm that (i) the Fourier-predicted
       (p*, q*) sits in the minimum basin, (ii) the Krylov surface is much
       flatter than the iterative one. Done at the per-mode level (worst-case
       ρ across the discrete spectrum) which is what dictates iterate count.

  R4.  OO2 in 2D PDE: add a second-order tangential symbol to the interface
       row of the existing 2D Helmholtz solver (interface row is augmented
       with -β D_ττ where D_ττ is the standard 3-point tangential second
       derivative, and α is added to the constant Robin part). Run GMRES
       and compare iteration counts against paper Table 6.1 "OO2-Krylov".

Everything is CPU-only numpy/scipy.

Outputs (all under ../../results/repass and ../../figures/repass):
  - osh_repass_results.json  : structured numerical results for everything
  - fig_oo2_asymptotic.png   : log-log check for Thm 4.2
  - fig_param_robustness_iter.png, fig_param_robustness_krylov.png
  - fig_oo2_2d_iters.png     : iters vs h for OO2-GMRES in 2D
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Literal

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Pull in helpers from the pass-1 1D / 2D scripts (no edits to those).
HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PASS1_CODE = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, PASS1_CODE)
from osh_1d import (  # type: ignore
    lam,
    rho_general,
    oo0_optimal_pq,
    oo0_asymptotic_rho,
    oo2_optimal_ab,
    rho_oo2,
)
from osh_2d import (  # type: ignore
    build_subdomain,
    interface_indices,
    RunResult,
)

RESULTS_DIR = os.path.join(ROOT, "results", "repass")
FIG_DIR = os.path.join(ROOT, "figures", "repass")
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)


# =========================================================================
#  R1.  Theorem 4.2 (OO2 asymptotic h-scaling)
# =========================================================================

def thm42_check() -> dict:
    """Verify the OO2 asymptotic forms (4.2) and (4.3):

      ρ_p = 1 - 4 (2 Δω)^{1/4} (1/ω)^{1/4} + O(1/√ω)   for propagating modes
      ρ_e = 1 - 4 (ω_+² - ω²)^{1/4} / √π · √h   + O(h)  for evanescent modes

    where Δω = ω - ω_-.

    We compute:
      (a) the numerically-observed worst-case ρ on the PROPAGATING subset
          [k_min, ω_-] for fixed h and varying ω, with ω_- = ω - 1 (so Δω
          held fixed; the leading 1/ω^{1/4} dependence is visible);
      (b) the numerically-observed worst-case ρ on the EVANESCENT subset
          [ω_+, k_max] for fixed ω = 10π, varying h.

    For each, compare 1-ρ_numeric to the asymptotic prediction; on log-log
    axes we expect slopes 1/4 (in ω) and 1/2 (in h).
    """
    rng = np.random.default_rng(0)

    # ----- (a) propagating-mode test: ρ_p vs ω, Δω fixed -----
    # Pick kmax = 10 ω so the evanescent range is well-resolved at each ω;
    # otherwise kmax/ω varies and the OO2 evanescent symbol drifts.
    delta_omega = math.pi  # = π so Δω is fixed across the sweep
    omegas_prop = np.array([20 * math.pi, 50 * math.pi, 100 * math.pi,
                            200 * math.pi, 500 * math.pi, 1000 * math.pi,
                            2000 * math.pi])
    rows_prop = []
    for omega in omegas_prop:
        omega_minus = omega - delta_omega
        omega_plus = omega + delta_omega
        kmin = 0.5  # tangential frequency floor (well below ω_-)
        kmax = 10.0 * omega   # ensures kmax >> ω so the OO2 evanescent part is bounded
        alpha, beta = oo2_optimal_ab(omega, omega_minus, omega_plus,
                                     kmin, kmax)
        # propagating modes: |k| < ω -> sample [k_min, ω_-] inclusive
        kg = np.linspace(kmin, omega_minus, 6000)
        rho_p = rho_oo2(kg, omega, alpha, beta).max()
        # asymptotic prediction (4.2)
        rho_p_asym = 1.0 - 4.0 * (2.0 * delta_omega) ** 0.25 * (1.0 / omega) ** 0.25
        rows_prop.append({
            "omega": omega,
            "delta_omega": delta_omega,
            "alpha": str(alpha),
            "beta": beta,
            "rho_max_numeric": float(rho_p),
            "rho_asym_thm42_prop": float(rho_p_asym),
            "one_minus_rho_numeric": float(1.0 - rho_p),
            "one_minus_rho_asym": float(1.0 - rho_p_asym),
        })

    # ----- (b) evanescent-mode test: ρ_e vs h, ω fixed -----
    omega = 10.0 * math.pi
    omega_minus = 9.0 * math.pi
    omega_plus = 11.0 * math.pi
    kmin_b = math.pi  # = π
    hs = [1.0 / 50, 1.0 / 100, 1.0 / 200, 1.0 / 400, 1.0 / 800, 1.0 / 1600]
    rows_evan = []
    for h in hs:
        kmax_h = math.pi / h
        alpha, beta = oo2_optimal_ab(omega, omega_minus, omega_plus,
                                     kmin_b, kmax_h)
        # evanescent modes: |k| > ω -> sample [ω_+, k_max]
        kg = np.linspace(omega_plus, kmax_h, 8000)
        rho_e = rho_oo2(kg, omega, alpha, beta).max()
        # asymptotic prediction (4.3)
        rho_e_asym = 1.0 - 4.0 * (omega_plus ** 2 - omega ** 2) ** 0.25 \
            / math.sqrt(math.pi) * math.sqrt(h)
        rows_evan.append({
            "h": h,
            "alpha": str(alpha),
            "beta": beta,
            "rho_e_max_numeric": float(rho_e),
            "rho_e_asym_thm42_evan": float(rho_e_asym),
            "one_minus_rho_numeric": float(1.0 - rho_e),
            "one_minus_rho_asym": float(1.0 - rho_e_asym),
        })

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    # (a) propagating, slope -1/4 in ω of (1-ρ)
    ax = axes[0]
    omg = np.array([r["omega"] for r in rows_prop])
    omr_num = np.array([r["one_minus_rho_numeric"] for r in rows_prop])
    omr_asy = np.array([r["one_minus_rho_asym"] for r in rows_prop])
    ax.loglog(omg, omr_num, "o-", label="numeric (max over k<ω)")
    ax.loglog(omg, omr_asy, "s--", label="Thm 4.2 (4.2)")
    # reference slope ω^{-1/4}
    C = omr_num[0] / omg[0] ** (-0.25)
    ax.loglog(omg, C * omg ** (-0.25), "k:", alpha=0.6,
              label=r"$O(\omega^{-1/4})$")
    ax.set_xlabel("ω")
    ax.set_ylabel(r"$1 - \rho_p$")
    ax.set_title("OO2 propagating modes: Thm 4.2 (Δω = π)")
    ax.legend(fontsize=9)
    ax.grid(True, which="both", alpha=0.3)
    # (b) evanescent, slope 1/2 in h
    ax = axes[1]
    hs_arr = np.array([r["h"] for r in rows_evan])
    om_num = np.array([r["one_minus_rho_numeric"] for r in rows_evan])
    om_asy = np.array([r["one_minus_rho_asym"] for r in rows_evan])
    ax.loglog(hs_arr, om_num, "o-", label="numeric (max over k>ω)")
    ax.loglog(hs_arr, om_asy, "s--", label="Thm 4.2 (4.3)")
    C = om_num[0] / math.sqrt(hs_arr[0])
    ax.loglog(hs_arr, C * np.sqrt(hs_arr), "k:", alpha=0.6,
              label=r"$O(h^{1/2})$")
    ax.set_xlabel("h")
    ax.set_ylabel(r"$1 - \rho_e$")
    ax.set_title("OO2 evanescent modes: Thm 4.2 (ω = 10π)")
    ax.legend(fontsize=9)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_oo2_asymptotic.png"), dpi=140)
    plt.close(fig)

    # Slope check: log-log linear fit on the four largest-ω / smallest-h points
    # (preasymptotic at small ω / large h, so use the tail to estimate the
    # leading-order slope).
    log_omg = np.log(omg[-4:])
    log_om = np.log(np.array([r["one_minus_rho_numeric"] for r in rows_prop[-4:]]))
    slope_prop = float(np.polyfit(log_omg, log_om, 1)[0])
    log_hs = np.log(hs_arr[-4:])
    log_oe = np.log(np.array([r["one_minus_rho_numeric"] for r in rows_evan[-4:]]))
    slope_evan = float(np.polyfit(log_hs, log_oe, 1)[0])
    # Ratio of numeric (1-ρ) to asymptotic prediction — should approach 1 as
    # ω→∞ for propagating, h→0 for evanescent. Useful diagnostic.
    ratio_prop_tail = float((1.0 - rows_prop[-1]["rho_max_numeric"])
                            / (1.0 - rows_prop[-1]["rho_asym_thm42_prop"]))
    ratio_evan_tail = float((1.0 - rows_evan[-1]["rho_e_max_numeric"])
                            / (1.0 - rows_evan[-1]["rho_e_asym_thm42_evan"]))

    return {
        "propagating": rows_prop,
        "propagating_loglog_slope": slope_prop,
        "propagating_expected_slope": -0.25,
        "propagating_ratio_tail": ratio_prop_tail,
        "evanescent": rows_evan,
        "evanescent_loglog_slope": slope_evan,
        "evanescent_expected_slope": 0.5,
        "evanescent_ratio_tail": ratio_evan_tail,
    }


# =========================================================================
#  R3.  Fig 6.2 parameter-robustness (per-mode worst-case ρ vs (p, q))
# =========================================================================

def fig62_param_robustness() -> dict:
    """Approximate Fig 6.2 by mapping (p, q) -> worst-case ρ across the
    admissible discrete spectrum, then translating ρ -> #iters via the
    standard estimate iters ≈ -log(tol) / -log(ρ).

    This is the "iterative" surface. For the "Krylov" surface, we use the
    iteration estimate for the GMRES residual after k steps applied to the
    Schwarz-trace operator (I - T), where T has spectrum approximately
    ρ(k) on each mode. Then |r_k| / |r_0| ≤ max over modes of
    (1 - 1/(1-ρ_k))^k? Practical proxy: GMRES with optimal residual is
    bounded by the worst Chebyshev polynomial on the spectrum of (I-T).
    Since the spectrum is bounded in modulus by ρ_max < 1 and bounded away
    from 1, a sharp proxy is k = -log(tol) / -log(ρ_avg) where ρ_avg is the
    geometric mean of ρ(k) over modes — much flatter in (p,q) than ρ_max.

    Paper Fig 6.2 setup: h = 1/50, ω = 9.3596 π, ω_- = 8.8806 π, ω_+ = 9.8363 π.
    Star at the Fourier-predicted (p*, q*).
    """
    omega = 9.3596 * math.pi
    omega_minus = 8.8806 * math.pi
    omega_plus = 9.8363 * math.pi
    h = 1.0 / 50
    kmax = math.pi / h
    kmin = math.pi  # smallest tangential mode on unit interval (k = n π, n=1)

    p_star, q_star = oo0_optimal_pq(omega, omega_minus, kmax)

    # admissible-k grid (skip the gap [ω_-, ω_+] as in the paper)
    kg = np.concatenate([
        np.linspace(kmin, omega_minus, 1500),
        np.linspace(omega_plus, kmax, 1500),
    ])
    # also: include propagating evanescent split as a sanity check
    L = lam(kg, omega)

    p_grid = np.linspace(5, 60, 42)
    q_grid = np.linspace(5, 60, 42)
    iter_surface = np.zeros((len(q_grid), len(p_grid)))
    krylov_surface = np.zeros_like(iter_surface)
    rhomax_surface = np.zeros_like(iter_surface)
    rho_geom_surface = np.zeros_like(iter_surface)

    log_tol = -math.log(1e-6)
    for ip, p in enumerate(p_grid):
        for iq, q in enumerate(q_grid):
            s = p + 1j * q
            R1 = (-L + s) / (L + s)
            R2 = (L + (-s)) / (-L + (-s))  # σ_2 = -σ_1
            rho_k = np.abs(R1 * R2)
            # exclude any tiny artifacts near k=ω-band where ρ blows up; clip
            rho_k_safe = np.clip(rho_k, 1e-12, 0.999999)
            rho_max = float(rho_k_safe.max())
            rho_geom = float(np.exp(np.log(rho_k_safe).mean()))
            iters_iter = log_tol / max(-math.log(rho_max), 1e-12)
            iters_krylov = log_tol / max(-math.log(rho_geom), 1e-12)
            rhomax_surface[iq, ip] = rho_max
            rho_geom_surface[iq, ip] = rho_geom
            iter_surface[iq, ip] = iters_iter
            krylov_surface[iq, ip] = iters_krylov

    # ----- Plot iterative surface (Fig 6.2 left) -----
    def plot_surface(surf, title, fname, cmin=None, cmax=None,
                     levels=None):
        fig, ax = plt.subplots(figsize=(6.4, 5.4))
        P, Q = np.meshgrid(p_grid, q_grid)
        clip = surf.copy()
        if cmax is not None:
            clip = np.minimum(clip, cmax)
        if cmin is not None:
            clip = np.maximum(clip, cmin)
        if levels is None:
            levels = 18
        cs = ax.contourf(P, Q, clip, levels=levels, cmap="viridis")
        cl = ax.contour(P, Q, clip, levels=levels, colors="white",
                        linewidths=0.4, alpha=0.4)
        ax.clabel(cl, fontsize=7, fmt="%.0f")
        ax.plot([p_star], [q_star], "*", color="red", markersize=18,
                markeredgecolor="white", label=f"Fourier (p*, q*) = ({p_star:.2f}, {q_star:.2f})")
        ax.set_xlabel("p")
        ax.set_ylabel("q")
        ax.set_title(title)
        ax.legend(loc="upper right")
        plt.colorbar(cs, ax=ax, label="iterations to 1e-6 (estimate)")
        fig.tight_layout()
        fig.savefig(os.path.join(FIG_DIR, fname), dpi=140)
        plt.close(fig)

    plot_surface(iter_surface,
                 "Iterative OO0: estimated #iters to 1e-6 vs (p, q)  [Fig 6.2 left]",
                 "fig_param_robustness_iter.png", cmax=120)
    plot_surface(krylov_surface,
                 "Krylov-OO0 proxy: -log(tol)/-log(geomean ρ) vs (p, q) [Fig 6.2 right]",
                 "fig_param_robustness_krylov.png", cmax=60)

    # Verify: (p*, q*) lies in the minimum basin of the iterative surface
    iter_at_star = float(log_tol / -math.log(np.clip(float(
        np.abs((-lam(kg, omega) + (p_star + 1j * q_star)) / (lam(kg, omega) + (p_star + 1j * q_star)) *
               (lam(kg, omega) + (-(p_star + 1j * q_star))) / (-lam(kg, omega) + (-(p_star + 1j * q_star)))
               ).max()), 1e-12, 0.999999)))
    iter_min = float(iter_surface.min())
    iter_min_pos = np.unravel_index(np.argmin(iter_surface), iter_surface.shape)
    iter_min_p = float(p_grid[iter_min_pos[1]])
    iter_min_q = float(q_grid[iter_min_pos[0]])
    krylov_min = float(krylov_surface.min())
    krylov_max_scan = float(krylov_surface[(p_grid >= 10) & (p_grid <= 50)][:, :].max())

    # Flatness ratio
    p_lo, p_hi = 0.5 * p_star, 1.5 * p_star
    q_lo, q_hi = 0.5 * q_star, 1.5 * q_star
    p_mask = (p_grid >= p_lo) & (p_grid <= p_hi)
    q_mask = (q_grid >= q_lo) & (q_grid <= q_hi)
    iter_loc = iter_surface[np.ix_(q_mask, p_mask)]
    krylov_loc = krylov_surface[np.ix_(q_mask, p_mask)]
    iter_flatness = float(iter_loc.max() / iter_loc.min())
    krylov_flatness = float(krylov_loc.max() / krylov_loc.min())

    return {
        "omega": omega,
        "omega_minus": omega_minus,
        "omega_plus": omega_plus,
        "h": h,
        "p_star": float(p_star),
        "q_star": float(q_star),
        "iter_at_star": iter_at_star,
        "iter_min_observed": iter_min,
        "iter_min_p": iter_min_p,
        "iter_min_q": iter_min_q,
        "krylov_min": krylov_min,
        "iter_flatness_in_50pct_window": iter_flatness,
        "krylov_flatness_in_50pct_window": krylov_flatness,
    }


# =========================================================================
#  R2 + R4.  2D PDE: Table 6.2 (ω on a mode) and OO2 in 2D GMRES
# =========================================================================

def schwarz_gmres_general(N: int, omega: float, mode: Literal["robin", "oo0", "oo2"],
                          *, s0: complex = 0.0 + 0j, alpha: complex = 0.0 + 0j,
                          beta: float = 0.0,
                          tol: float = 1e-6, maxiter: int = 600,
                          restart: int = 80) -> RunResult:
    """Generalized substructured-Schwarz GMRES driver.

    For mode == "robin"  -> transmission s = i ω.
    For mode == "oo0"    -> transmission s = s0 (scalar p + i q).
    For mode == "oo2"    -> transmission s = α  + β D_ττ  on the interface row,
                            with α scalar, β scalar (tangential derivative is
                            the standard 3-point centered FD along y).

    The subdomain matrix is built ONCE with Robin row constant = α (OR s0 for
    OO0/Robin), and the tangential β D_ττ is added as a rank-(ny-2) update
    along the interface row only. This is mathematically the same as the
    paper's OO2 transmission condition  (α + β ∂_ττ) u on Γ.
    """
    if N % 2 != 0:
        raise ValueError("N must be even")
    h = 1.0 / N
    nx = N // 2 + 1
    ny = N + 1
    hx = hy = h

    if mode == "robin":
        s_scalar = 1j * omega
        q_coef = 0.0 + 0j
    elif mode == "oo0":
        s_scalar = s0
        q_coef = 0.0 + 0j
    elif mode == "oo2":
        # Translate (α, β) (Thm 3.10 symbol params) to the actual BC coefficients
        # of eq. (3.15):  ∂_n u + s_scalar u + q_coef ∂²_ττ u = g.
        if alpha + beta == 0:
            raise ValueError("alpha + beta must be nonzero for OO2")
        s_scalar = (alpha * beta - omega ** 2) / (alpha + beta)
        q_coef = -1.0 / (alpha + beta)
    elif mode == "taylor2":
        # Taylor-2 absorbing BC for Helmholtz:
        #   ∂_n u + iω u + (1/(2 i ω)) ∂²_ττ u = g
        #   <=>  s_scalar = iω,  q_coef = 1/(2 i ω) = -i / (2ω).
        s_scalar = 1j * omega
        q_coef = -1j / (2.0 * omega)
    else:
        raise ValueError(mode)

    # build subdomain operators (Robin row uses s_scalar as the constant α part)
    A1 = build_subdomain(nx, ny, hx, hy, omega,
                         left_bc="robin_omega", right_bc="interface",
                         interface_side="right", s_interface=s_scalar)
    A2 = build_subdomain(nx, ny, hx, hy, omega,
                         left_bc="robin_omega", right_bc="interface",
                         interface_side="left", s_interface=s_scalar)

    if mode in ("oo2", "taylor2"):
        # Add q_coef * D_ττ contribution to the interface row of each subdomain.
        # The Robin BC at i=nx-1 (Ω1) was discretized via ghost-point as
        #   diag += 2 s_scalar / hx  ;  off-diag (i=nx-2) += -2/hx^2.
        # OO2 / Taylor2 BC has form (paper eq. 3.15 for OO2):
        #   ∂_n u + s_scalar u + q_coef ∂²_ττ u = g
        # where s_scalar = (αβ-ω²)/(α+β) and q_coef = -1/(α+β).
        # Ghost-point elimination of u_{-1} from
        #   -(u_1 - u_{-1})/(2 hx) + s u_0 + q D_ττ u_0 = g
        # gives u_{-1} = u_1 + 2 hx (g - s u_0 - q D_ττ u_0). Substituting into
        # the PDE row at i=0 of Ω2 yields the additions to row k = i + nx*j:
        #   diag  (k, k)         +=  (2 q / hx) * (-2 / hy^2)
        #   (k, k_{j-1})         +=  (2 q / hx) * (1 / hy^2)
        #   (k, k_{j+1})         +=  (2 q / hx) * (1 / hy^2)
        inv_hy2 = 1.0 / (hy * hy)
        coef = 2.0 * q_coef / hx

        def add_oo2_row(A, side):
            A = A.tolil()
            i_row = nx - 1 if side == "right" else 0
            for j in range(1, ny - 1):
                k = i_row + nx * j
                k_dn = i_row + nx * (j - 1)
                k_up = i_row + nx * (j + 1)
                # diag
                if k in A.rows[k]:
                    pos = A.rows[k].index(k)
                    A.data[k][pos] += coef * (-2.0 * inv_hy2)
                else:
                    A.rows[k].append(k); A.data[k].append(coef * (-2.0 * inv_hy2))
                # below
                if k_dn in A.rows[k]:
                    pos = A.rows[k].index(k_dn)
                    A.data[k][pos] += coef * inv_hy2
                else:
                    A.rows[k].append(k_dn); A.data[k].append(coef * inv_hy2)
                # above
                if k_up in A.rows[k]:
                    pos = A.rows[k].index(k_up)
                    A.data[k][pos] += coef * inv_hy2
                else:
                    A.rows[k].append(k_up); A.data[k].append(coef * inv_hy2)
            # special: j=1 row's neighbor j=0 is Dirichlet (u=0) -> matrix
            # entry there is 1.0; adding D_ττ from j=1 references j=0. But
            # since u(j=0)=0 enforced via identity row, the linear contribution
            # via the row at j=1 only matters through the column entry. We
            # leave it (matrix is still nonsingular).
            return A.tocsc()

        A1 = add_oo2_row(A1, "right")
        A2 = add_oo2_row(A2, "left")

    solve1 = spla.splu(A1)
    solve2 = spla.splu(A2)

    idx1 = interface_indices(nx, ny, "right")
    idx2 = interface_indices(nx, ny, "left")
    ny_iface = ny - 2
    ghost_scale = 2.0 / hx

    # For the "Lions dual variable" update we need s1 + s2 acting on the
    # interface trace.  In OO2 / Taylor2 this is (s1+s2) + (q1+q2) D_ττ with
    # s1 = s2 = s_scalar and q1 = q2 = q_coef.
    if mode in ("oo2", "taylor2"):
        s_sum_scalar = 2 * s_scalar
        q_sum = 2 * q_coef
        inv_hy2 = 1.0 / (hy * hy)
        # build a (ny_iface x ny_iface) tridiagonal Dττ matrix with Dirichlet BC
        diag_t = -2 * inv_hy2 * np.ones(ny_iface)
        off_t = inv_hy2 * np.ones(ny_iface - 1)
        D_tt = sp.diags([off_t, diag_t, off_t], offsets=[-1, 0, 1],
                        shape=(ny_iface, ny_iface), format="csr", dtype=complex)
        S_sum_op = sp.eye(ny_iface, dtype=complex) * s_sum_scalar + q_sum * D_tt
    else:
        s_sum_scalar = 2 * s_scalar
        S_sum_op = None  # multiply scalar

    N1 = nx * ny
    N2 = nx * ny

    def apply_T(g_flat):
        g1 = g_flat[:ny_iface]
        g2 = g_flat[ny_iface:]
        rhs1 = np.zeros(N1, dtype=complex); rhs1[idx1] = ghost_scale * g1
        rhs2 = np.zeros(N2, dtype=complex); rhs2[idx2] = ghost_scale * g2
        u1 = solve1.solve(rhs1)
        u2 = solve2.solve(rhs2)
        if S_sum_op is not None:
            g1n = (S_sum_op @ u2[idx2]) - g2
            g2n = (S_sum_op @ u1[idx1]) - g1
        else:
            g1n = s_sum_scalar * u2[idx2] - g2
            g2n = s_sum_scalar * u1[idx1] - g1
        return np.concatenate([g1n, g2n])

    n_iface = 2 * ny_iface
    op = spla.LinearOperator((n_iface, n_iface),
                             matvec=lambda v: v - apply_T(v),
                             dtype=complex)

    rng = np.random.default_rng(42)
    rhs = rng.standard_normal(n_iface) + 1j * rng.standard_normal(n_iface)
    rhs /= np.linalg.norm(rhs)

    iters_count = [0]
    def cb(xk):
        iters_count[0] += 1

    t0 = time.time()
    sol, info = spla.gmres(op, rhs, rtol=tol, restart=restart, maxiter=maxiter,
                           callback=cb, callback_type="pr_norm")
    elapsed = time.time() - t0
    final_res = float(np.linalg.norm(rhs - op @ sol))
    converged = (info == 0)

    s_param = s_scalar  # always the effective constant Robin coefficient

    return RunResult(method=mode + "_gmres", N=N, h=h, omega=omega,
                     s_param=s_param,
                     converged=converged, iters=iters_count[0],
                     final_residual=final_res,
                     history=[final_res], elapsed_sec=elapsed)


def table62_repro() -> dict:
    """Reproduce paper Table 6.2: ω = 10π directly on a problem frequency.

    Iterative methods would have ρ(k=ω)=1 and cannot converge; only Krylov
    works. We run GMRES for Taylor (Robin, s=iω) and OO0 at three resolutions
    and compare against the paper's numbers.

    Paper Table 6.2:
      h     | Taylor-K | OO0-K | Taylor2-K | OO2-K
      1/50  |   24     |  15   |    27     |   9
      1/100 |   35     |  21   |    35     |  11
      1/200 |   44     |  26   |    41     |  13
    """
    omega = 10.0 * math.pi
    # For OO0/OO2 we still need a band [ω_-, ω_+] to avoid; since ω is on
    # a mode (k = 10 π = ω exactly), the natural choice is ω_± = ω ± π
    # as the paper uses for its model problem.
    omega_minus = 9.0 * math.pi
    omega_plus = 11.0 * math.pi

    Ns = [50, 100, 200]
    paper = {
        50:  {"robin": 24, "oo0": 15, "oo2": 9, "taylor2": 27},
        100: {"robin": 35, "oo0": 21, "oo2": 11, "taylor2": 35},
        200: {"robin": 44, "oo0": 26, "oo2": 13, "taylor2": 41},
    }
    rows = []
    for N in Ns:
        h = 1.0 / N
        kmax = math.pi / h
        kmin = math.pi
        # OO0 parameters
        p_star, _ = oo0_optimal_pq(omega, omega_minus, kmax)
        s_oo0 = p_star + 1j * p_star
        # OO2 parameters (paper Thm 3.10)
        alpha, beta = oo2_optimal_ab(omega, omega_minus, omega_plus, kmin, kmax)
        results_for_h = {}
        for label, mode, params in [
            ("robin", "robin", {}),
            ("oo0", "oo0", {"s0": s_oo0}),
            ("oo2", "oo2", {"alpha": alpha, "beta": beta}),
            ("taylor2", "taylor2", {}),
        ]:
            print(f"  [Table 6.2] N={N} {label} ...", flush=True)
            r = schwarz_gmres_general(N, omega, mode, tol=1e-6, maxiter=400,
                                      restart=80, **params)
            print(f"    -> iters={r.iters}  converged={r.converged}  "
                  f"final={r.final_residual:.2e}  "
                  f"elapsed={r.elapsed_sec:.1f}s")
            results_for_h[label] = {"iters": r.iters, "converged": r.converged,
                                    "final_res": r.final_residual,
                                    "elapsed": r.elapsed_sec}
        row = {"N": N, "h": h, "paper": paper[N], "ours": results_for_h,
               "p_star": p_star,
               "alpha": str(alpha), "beta": float(beta)}
        rows.append(row)

    return {"omega": omega, "rows": rows, "paper_table_6_2": paper}


def table61_oo2_repro() -> dict:
    """Add OO2-Krylov column to the Table 6.1 sweep (ω = 9.5π, off-mode)."""
    omega = 9.5 * math.pi
    omega_minus = 9.0 * math.pi
    omega_plus = 10.0 * math.pi
    Ns = [50, 100, 200]
    paper = {50: {"oo2": 9, "robin": 26, "oo0": 16, "taylor2": 28},
             100: {"oo2": 10, "robin": 34, "oo0": 21, "taylor2": 33},
             200: {"oo2": 13, "robin": 44, "oo0": 26, "taylor2": 40}}
    rows = []
    for N in Ns:
        h = 1.0 / N
        kmax = math.pi / h
        kmin = math.pi
        alpha, beta = oo2_optimal_ab(omega, omega_minus, omega_plus, kmin, kmax)
        results_for_h = {}
        for label, mode, params in [
            ("oo2", "oo2", {"alpha": alpha, "beta": beta}),
            ("taylor2", "taylor2", {}),
        ]:
            print(f"  [Table 6.1 OO2] N={N} {label} ...", flush=True)
            r = schwarz_gmres_general(N, omega, mode, tol=1e-6, maxiter=400,
                                      restart=80, **params)
            print(f"    -> iters={r.iters} converged={r.converged}  "
                  f"final={r.final_residual:.2e}  elapsed={r.elapsed_sec:.1f}s")
            results_for_h[label] = {"iters": r.iters,
                                    "converged": r.converged,
                                    "final_res": r.final_residual,
                                    "elapsed": r.elapsed_sec}
        rows.append({"N": N, "h": h, "paper": paper[N], "ours": results_for_h,
                     "alpha": str(alpha), "beta": float(beta)})

    # Plot iters vs h
    fig, ax = plt.subplots(figsize=(6, 4))
    hs = np.array([1.0 / r["N"] for r in rows])
    paper_oo2 = np.array([r["paper"]["oo2"] for r in rows])
    paper_taylor2 = np.array([r["paper"]["taylor2"] for r in rows])
    our_oo2 = np.array([r["ours"]["oo2"]["iters"] for r in rows])
    our_taylor2 = np.array([r["ours"]["taylor2"]["iters"] for r in rows])
    ax.loglog(hs, paper_oo2, "s--", color="tab:blue", label="paper OO2-Krylov")
    ax.loglog(hs, our_oo2, "o-", color="tab:blue", label="ours OO2-Krylov")
    ax.loglog(hs, paper_taylor2, "s--", color="tab:red", label="paper Taylor2-Krylov")
    ax.loglog(hs, our_taylor2, "o-", color="tab:red", label="ours Taylor2-Krylov")
    ax.set_xlabel("h")
    ax.set_ylabel("iterations to 1e-6")
    ax.set_title("Table 6.1: OO2 and Taylor2 Krylov iters vs h (ω = 9.5π)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_oo2_2d_iters.png"), dpi=140)
    plt.close(fig)

    return {"omega": omega, "rows": rows, "paper_table_6_1_subset": paper}


# =========================================================================
#  Main driver
# =========================================================================

def main():
    t0 = time.time()
    print("=== R1: Theorem 4.2 (OO2 asymptotic) ===")
    r1 = thm42_check()
    print(f"  propagating slope (log-log fit): {r1['propagating_loglog_slope']:.4f}"
          f"  (expected {r1['propagating_expected_slope']})")
    print(f"  evanescent  slope (log-log fit): {r1['evanescent_loglog_slope']:.4f}"
          f"  (expected {r1['evanescent_expected_slope']})")

    print("\n=== R3: Parameter robustness surface (Fig 6.2) ===")
    r3 = fig62_param_robustness()
    print(f"  p* = {r3['p_star']:.3f}  q* = {r3['q_star']:.3f}")
    print(f"  iter at (p*,q*) = {r3['iter_at_star']:.1f}")
    print(f"  iter min on grid = {r3['iter_min_observed']:.1f} at "
          f"(p={r3['iter_min_p']:.2f}, q={r3['iter_min_q']:.2f})")
    print(f"  iter flatness in ±50% window: {r3['iter_flatness_in_50pct_window']:.2f}")
    print(f"  krylov flatness in ±50% window: {r3['krylov_flatness_in_50pct_window']:.2f}")

    print("\n=== R4: Table 6.1 OO2-Krylov + Taylor2-Krylov columns (off-mode) ===")
    r4 = table61_oo2_repro()
    for row in r4["rows"]:
        N = row["N"]
        po = row["paper"]["oo2"]; pt = row["paper"]["taylor2"]
        oo = row["ours"]["oo2"]["iters"]; ot = row["ours"]["taylor2"]["iters"]
        print(f"  N={N:3d}  paper OO2={po:3d}  ours OO2={oo:3d}  | "
              f"paper Taylor2={pt:3d}  ours Taylor2={ot:3d}")

    print("\n=== R2: Table 6.2 (ω on a mode = 10π) ===")
    r2 = table62_repro()
    for row in r2["rows"]:
        N = row["N"]
        pap = row["paper"]
        ours = row["ours"]
        print(f"  N={N:3d}  "
              f"Taylor: paper={pap['robin']:3d} ours={ours['robin']['iters']:3d} | "
              f"OO0:    paper={pap['oo0']:3d}  ours={ours['oo0']['iters']:3d}  | "
              f"OO2:    paper={pap['oo2']:3d}  ours={ours['oo2']['iters']:3d}  | "
              f"Taylor2: paper={pap['taylor2']:3d} ours={ours['taylor2']['iters']:3d}")

    out = {
        "thm42_oo2_asymptotic": r1,
        "fig62_param_robustness": r3,
        "table61_oo2_repro": r4,
        "table62_repro": r2,
        "wall_time_sec": time.time() - t0,
    }
    json_path = os.path.join(RESULTS_DIR, "osh_repass_results.json")
    with open(json_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nWrote {json_path}  ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
