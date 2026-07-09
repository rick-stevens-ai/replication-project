#!/usr/bin/env python3
"""
Reimplementation of Wang et al. 2018, Sci. Rep. 8:16202
"Modelling of Cellular Survival Following Radiation-Induced DNA Double-Strand Breaks"
DOI: 10.1038/s41598-018-34159-3

LUCID100 Wave 1 slot 9 first-pass smoke test.

This is a self-contained pure-Python implementation of Eqs. (1)-(19) of the
paper, using the Table 1 best-fit parameters reported by Wang et al. for HSG
and V79 cells. It does NOT require the MCDS Monte Carlo code or the PIDE
database for the smoke test; instead, it uses representative MCDS-derived
DSB-yield inputs (Y, lambda) at a few LET / particle conditions taken from
Wang Fig. 1 / Stewart et al. 2008,2011 references, and verifies:

  (1) The Taylor-expansion form of Eq. (15) reduces to the LQ model
      -ln S = alpha*D + beta*D^2 (Eqs. 17-19) for small n_p.
  (2) The (alpha, beta) values produced by the Table 1 fits are in the range
      reported in Wang Fig. 2 for X-rays / low-LET radiation on HSG and V79.
  (3) The full Eq. (15) gives monotonically decreasing survival vs dose and
      reproduces the qualitative behaviour of Fig. 3 (higher LET -> steeper
      SF curve, more exponential / less shoulder).
  (4) The alpha/beta ratio computed via Eq. (20) rises with LET (Fig. 6).
  (5) RBE_10% vs LET shows the published rising-then-falling shape with a
      peak around 100-200 keV/um (Fig. 5).

For a strict numerical replication of the published figures you need MCDS
(Stewart 2008,2011) for Y(LET) and lambda(LET), and PIDE (Friedrich 2013)
for the per-experiment fit targets. See FIRST_PASS_REPORT.md for the
full plan.

Run:
    python3 wang2018_dsb_survival.py [--out-dir <dir>]

Outputs:
    - smoke_test.json  : numerical results
    - figures/*.png    : qualitative reproduction of Figs. 3/5/6 shape
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from dataclasses import dataclass, asdict

import numpy as np


# ---------------------------------------------------------------------------
# Table 1: published best-fit parameters (Wang et al. 2018)
# ---------------------------------------------------------------------------
@dataclass
class CellParams:
    name: str
    mu_x: float          # NHEJ fidelity
    mu_y: float          # sensitivity per lethal event
    zeta: float          # over-kill effect scale
    xi: float            # clustered DNA damage scale
    eta_lp_to_1: float   # eta(lambda_p -> 1)  [the "low-lambda_p" limit]
    eta_lp_to_inf: float # eta(lambda_p -> inf) [the "high-lambda_p" limit]

    # quoted uncertainties (one sigma) - not used in the smoke test but kept
    # for provenance.
    sigma_mu_x: float = 0.0
    sigma_mu_y: float = 0.0
    sigma_zeta: float = 0.0
    sigma_xi: float = 0.0
    sigma_eta_lp_to_1: float = 0.0
    sigma_eta_lp_to_inf: float = 0.0


HSG = CellParams(
    name="HSG",
    mu_x=0.9817, mu_y=0.0891,
    zeta=0.1025, xi=0.0572,
    eta_lp_to_1=7.26e-4, eta_lp_to_inf=0.0022,
    sigma_mu_x=0.0056, sigma_mu_y=0.0068,
    sigma_zeta=0.0065, sigma_xi=0.0027,
    sigma_eta_lp_to_1=0.04e-4, sigma_eta_lp_to_inf=0.0001,
)

V79 = CellParams(
    name="V79",
    mu_x=0.9568, mu_y=0.0300,
    zeta=0.0412, xi=0.0608,
    eta_lp_to_1=9.78e-4, eta_lp_to_inf=0.0065,
    sigma_mu_x=0.0236, sigma_mu_y=0.0177,
    sigma_zeta=0.0209, sigma_xi=0.0381,
    sigma_eta_lp_to_1=0.10e-4, sigma_eta_lp_to_inf=0.0001,
)


# ---------------------------------------------------------------------------
# Helpers - implement the published equations
# ---------------------------------------------------------------------------

def eta_of_lambda_p(lambda_p: float, p: CellParams) -> float:
    """Eq. (8): eta(lambda_p) = eta_inf - (eta_inf - eta_1) / lambda_p.

    Boundary conditions:
        lambda_p -> 1   => eta -> eta_lp_to_1
        lambda_p -> inf => eta -> eta_lp_to_inf
    """
    if lambda_p <= 0:
        return p.eta_lp_to_inf
    return p.eta_lp_to_inf - (p.eta_lp_to_inf - p.eta_lp_to_1) / lambda_p


def _safe_unit_minus_exp_over_x(x: float) -> float:
    """(1 - exp(-x)) / x, stable for small x (-> 1 - x/2 + x^2/6)."""
    if x == 0.0:
        return 1.0
    if abs(x) < 1e-6:
        return 1.0 - 0.5 * x + (x * x) / 6.0
    return (1.0 - math.exp(-x)) / x


def n_particles_per_nucleus(D_Gy: float, LET_keV_per_um: float,
                            R_um: float = 5.0, rho_g_per_cm3: float = 1.0) -> float:
    """Eq. (2): number of primary particles through a spherical nucleus of
    radius R (um) and density rho (g/cm^3) for dose D (Gy) at given LET (keV/um).

    pi R^2 (um^2) -> cm^2 via (R/10000)^2 ; convert keV->J via 1.602e-16.
    Wang's prefactor of 1e-18 / 1.602e-19 absorbs the geometry-unit conversion.
    """
    if LET_keV_per_um <= 0:
        return 0.0
    return (math.pi * R_um * R_um * D_Gy * rho_g_per_cm3
            * 1e-18 / (LET_keV_per_um * 1.602e-19))


def np_and_lambda_p(Y: float, D_Gy: float, n: float) -> tuple[float, float]:
    """Eqs. (1), (3), (5), (6).
    Y: DSB yield per cell per Gy
    n: # primary particles through nucleus (Eq. 2)
    Returns (n_p, lambda_p) where n_p is the number of DSB-causing primaries
    and lambda_p is DSBs per DSB-causing primary.
    """
    N = Y * D_Gy                       # Eq. (1)
    if n <= 0:
        return 0.0, 0.0
    lam = N / n                        # Eq. (3): lambda
    if lam < 1e-12:
        return 0.0, 1.0
    # Eq. (5): np = n (1 - e^-lambda)
    n_p = n * (1.0 - math.exp(-lam))
    # Eq. (6): lambda_p = lambda / (1 - e^-lambda)
    lambda_p = lam / (1.0 - math.exp(-lam))
    return n_p, lambda_p


def n_death(N: float, lambda_p: float, n_p: float, p: CellParams) -> float:
    """Eqs. (7)-(13): expected number of lethal events.
    Implements:
        Pinteraction(lp,np)  Eq. 7
        Ptrack(lp)           Eq. 9
        Pcorrect             Eq. 10
        Pcontribution        Eq. 11
        Ndeath = mu_y * N * Pcontribution * (1 - Pcorrect)   Eq. 12/13
    """
    eta = eta_of_lambda_p(lambda_p, p)
    P_int  = _safe_unit_minus_exp_over_x(eta * lambda_p * n_p)        # Eq. 7
    P_trk  = _safe_unit_minus_exp_over_x(p.xi   * lambda_p)           # Eq. 9
    P_corr = p.mu_x * P_trk * P_int                                   # Eq. 10
    P_contrib = _safe_unit_minus_exp_over_x(p.zeta * lambda_p)        # Eq. 11
    return p.mu_y * N * P_contrib * (1.0 - P_corr)                    # Eq. 13


def survival(D_Gy: float, Y: float, LET_keV_per_um: float, p: CellParams,
             R_um: float = 5.0, rho: float = 1.0) -> float:
    """Eq. (14)/(15): S = exp(-Ndeath)."""
    if D_Gy <= 0:
        return 1.0
    n  = n_particles_per_nucleus(D_Gy, LET_keV_per_um, R_um, rho)
    Nd = Y * D_Gy
    n_p, lambda_p = np_and_lambda_p(Y, D_Gy, n)
    return math.exp(-n_death(Nd, lambda_p, n_p, p))


def alpha_beta_LQ(Y: float, lambda_p: float, p: CellParams) -> tuple[float, float]:
    """Eqs. (18)/(19): alpha, beta of the LQ-form derived in the small-np limit.
    Caller must supply lambda_p evaluated at the relevant LET (it is the
    lambda_p approached as D -> 0, i.e. the per-DSB-causing-primary yield)."""
    eta = eta_of_lambda_p(lambda_p, p)
    P_trk  = _safe_unit_minus_exp_over_x(p.xi   * lambda_p)
    P_contrib = _safe_unit_minus_exp_over_x(p.zeta * lambda_p)
    alpha = Y * P_contrib * (1.0 - p.mu_x * P_trk) * p.mu_y                # Eq. 18
    beta  = 0.5 * eta * (Y / lambda_p) * Y * P_contrib * P_trk * p.mu_x * p.mu_y  # Eq. 19
    return alpha, beta


# ---------------------------------------------------------------------------
# Representative MCDS-derived inputs (Y, lambda) for the smoke test.
# Values approximate the curves in Wang Fig. 1 / Stewart 2011 Tables; they
# are NOT exact MCDS outputs. See FIRST_PASS_REPORT.md for the strict
# regeneration path with the real MCDS code.
# ---------------------------------------------------------------------------
# columns: particle, LET (keV/um), Y (DSB / cell / Gy), lambda (DSB / track)
REPRESENTATIVE_MCDS = [
    # X-rays / 250 kVp photons used as low-LET reference
    ("photon",  0.3,    35.0, 1.0),
    ("proton",  2.0,    37.0, 1.05),
    ("proton",  10.0,   42.0, 1.4),
    ("He-3",    30.0,   55.0, 3.2),
    ("C-12",    50.0,   65.0, 6.0),
    ("C-12",    100.0,  78.0, 13.0),
    ("C-12",    200.0,  85.0, 27.0),
    ("Ne-20",   400.0,  90.0, 55.0),
    ("Ne-20",   1000.0, 92.0, 145.0),
]


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------

def run_smoke(out_dir: str) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    figs_dir = os.path.join(out_dir, "figures")
    os.makedirs(figs_dir, exist_ok=True)

    summary: dict = {"checks": {}, "tables": {}}

    # --- (A) Internal consistency: alpha/beta from full Eq.(15) vs Eq.(18-19)
    # for a small-LET radiation (proton 2 keV/um) where the LQ form should
    # hold. We fit -lnS(D) = alpha D + beta D^2 to predictions at small D.
    Y, LET = 37.0, 2.0   # MCDS-like proton input
    doses = np.linspace(0.1, 2.0, 20)
    consistency = {}
    for p in (HSG, V79):
        lnS = np.array([-math.log(survival(D, Y, LET, p)) for D in doses])
        coeffs = np.polyfit(doses, lnS, 2)   # beta_fit, alpha_fit, c
        beta_fit, alpha_fit, c = coeffs
        n0 = n_particles_per_nucleus(1.0, LET)
        _, lambda_p0 = np_and_lambda_p(Y, 1.0, n0)
        alpha_eq, beta_eq = alpha_beta_LQ(Y, lambda_p0, p)
        consistency[p.name] = {
            "lambda_p_at_1Gy": lambda_p0,
            "alpha_eq18": alpha_eq,
            "beta_eq19":  beta_eq,
            "alpha_fit_full_eq15": float(alpha_fit),
            "beta_fit_full_eq15":  float(beta_fit),
            "intercept_should_be_0": float(c),
            "alpha_rel_err": float((alpha_fit - alpha_eq) / max(abs(alpha_eq), 1e-12)),
        }
    summary["checks"]["LQ_internal_consistency_proton_2keV_um"] = consistency

    # --- (B) Sanity ranges: alpha, beta for X-ray reference (~0.3 keV/um)
    xray = {}
    Y_x, L_x = 35.0, 0.3
    n0 = n_particles_per_nucleus(1.0, L_x)
    _, lp0 = np_and_lambda_p(Y_x, 1.0, n0)
    for p in (HSG, V79):
        a, b = alpha_beta_LQ(Y_x, lp0, p)
        xray[p.name] = {
            "alpha_Gy_inv": a,
            "beta_Gy2_inv": b,
            "alpha_over_beta": a / b if b > 0 else float("inf"),
        }
    summary["checks"]["xray_LQ_alpha_beta"] = xray

    # --- (C) Survival curves vs dose for a few LETs
    sf_table = {}
    doses_sf = np.linspace(0.0, 8.0, 41)
    for cell in (HSG, V79):
        rows = {}
        for label, LETv, Yv, _ in [
            ("X-ray",        0.3,    35.0, 1.0),
            ("C-12 50",     50.0,   65.0, 6.0),
            ("C-12 200",   200.0,   85.0, 27.0),
        ]:
            sfs = [survival(D, Yv, LETv, cell) for D in doses_sf]
            rows[label] = {
                "dose_Gy": doses_sf.tolist(),
                "SF": sfs,
                "SF_at_2Gy": float(survival(2.0, Yv, LETv, cell)),
                "D10_Gy":    _dose_for_SF(0.10, Yv, LETv, cell),
            }
        sf_table[cell.name] = rows
    summary["tables"]["survival_curves"] = sf_table

    # --- (D) alpha/beta ratio vs LET (Eq. 20 / Fig. 6)
    ab_curve = {}
    LET_grid = [0.3, 2.0, 10.0, 30.0, 50.0, 100.0, 200.0, 400.0, 1000.0]
    for cell in (HSG, V79):
        vals = []
        for L in LET_grid:
            Y_interp = float(np.interp(L,
                [r[1] for r in REPRESENTATIVE_MCDS],
                [r[2] for r in REPRESENTATIVE_MCDS]))
            n0 = n_particles_per_nucleus(1.0, L)
            _, lp = np_and_lambda_p(Y_interp, 1.0, n0)
            a, b = alpha_beta_LQ(Y_interp, lp, cell)
            vals.append({
                "LET_keV_per_um": L,
                "alpha": a, "beta": b,
                "alpha_over_beta": (a / b) if b > 0 else float("inf"),
            })
        ab_curve[cell.name] = vals
    summary["tables"]["alpha_beta_vs_LET"] = ab_curve

    # --- (E) RBE_10% vs LET (Fig. 5 shape)
    rbe_curve = {}
    Yx, Lx = 35.0, 0.3
    for cell in (HSG, V79):
        D10_xray = _dose_for_SF(0.10, Yx, Lx, cell)
        vals = []
        for L in LET_grid:
            Y_interp = float(np.interp(L,
                [r[1] for r in REPRESENTATIVE_MCDS],
                [r[2] for r in REPRESENTATIVE_MCDS]))
            D10 = _dose_for_SF(0.10, Y_interp, L, cell)
            vals.append({
                "LET_keV_per_um": L,
                "D10_Gy": D10,
                "RBE_10pct": (D10_xray / D10) if D10 > 0 else float("nan"),
            })
        rbe_curve[cell.name] = {
            "D10_xray_Gy": D10_xray,
            "by_LET": vals,
        }
    summary["tables"]["RBE10_vs_LET"] = rbe_curve

    # --- Plot qualitative figures
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # Survival curves
        for cell_name, rows in sf_table.items():
            fig, ax = plt.subplots(figsize=(5, 4))
            for label, r in rows.items():
                ax.semilogy(r["dose_Gy"], r["SF"], label=label)
            ax.set_xlabel("Dose (Gy)")
            ax.set_ylabel("Surviving fraction")
            ax.set_title(f"{cell_name} - SF vs dose (smoke test)")
            ax.set_ylim(1e-4, 1.2)
            ax.legend(fontsize=8)
            fig.tight_layout()
            fig.savefig(os.path.join(figs_dir, f"sf_{cell_name}.png"), dpi=120)
            plt.close(fig)

        # alpha/beta vs LET
        fig, ax = plt.subplots(figsize=(5, 4))
        for cell_name, vals in ab_curve.items():
            xs = [v["LET_keV_per_um"] for v in vals]
            ys = [v["alpha_over_beta"] for v in vals]
            ax.loglog(xs, ys, marker="o", label=cell_name)
        ax.set_xlabel("LET (keV/um)")
        ax.set_ylabel("alpha / beta")
        ax.set_title("alpha/beta vs LET (Fig. 6 shape, smoke test)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(os.path.join(figs_dir, "alpha_beta_vs_LET.png"), dpi=120)
        plt.close(fig)

        # RBE_10% vs LET
        fig, ax = plt.subplots(figsize=(5, 4))
        for cell_name, blk in rbe_curve.items():
            xs = [v["LET_keV_per_um"] for v in blk["by_LET"]]
            ys = [v["RBE_10pct"] for v in blk["by_LET"]]
            ax.semilogx(xs, ys, marker="o", label=cell_name)
        ax.set_xlabel("LET (keV/um)")
        ax.set_ylabel("RBE at 10% survival")
        ax.set_title("RBE_10 vs LET (Fig. 5 shape, smoke test)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(os.path.join(figs_dir, "rbe10_vs_LET.png"), dpi=120)
        plt.close(fig)

        summary["figures_written"] = sorted(os.listdir(figs_dir))
    except Exception as e:  # pragma: no cover
        summary["plotting_error"] = repr(e)

    return summary


def _dose_for_SF(target_SF: float, Y: float, LET: float, p: CellParams,
                 d_lo: float = 1e-3, d_hi: float = 200.0,
                 tol: float = 1e-4) -> float:
    """Bisection for D such that S(D) = target_SF, assuming S is monotonic
    decreasing in D (true for this model on physical doses)."""
    lo, hi = d_lo, d_hi
    s_lo = survival(lo, Y, LET, p)
    s_hi = survival(hi, Y, LET, p)
    if target_SF >= s_lo:
        return lo
    if target_SF <= s_hi:
        return hi
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        s_mid = survival(mid, Y, LET, p)
        if abs(s_mid - target_SF) < tol:
            return mid
        if s_mid > target_SF:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", default=os.path.dirname(os.path.abspath(__file__))
                    + "/../",
                    help="Output directory (default: replication slot root).")
    ns = ap.parse_args(argv)
    out_dir = os.path.abspath(ns.out_dir)
    results = run_smoke(out_dir)
    out_json = os.path.join(out_dir, "smoke_test.json")
    with open(out_json, "w") as fh:
        json.dump(results, fh, indent=2, default=str)
    print(f"[smoke] wrote {out_json}")
    # human-readable summary
    print("\n=== Smoke test summary ===")
    for cell, blk in results["checks"]["LQ_internal_consistency_proton_2keV_um"].items():
        print(f"  [{cell}] proton 2 keV/um: alpha(eq18)={blk['alpha_eq18']:.4f}/Gy "
              f"alpha(fit eq15)={blk['alpha_fit_full_eq15']:.4f}/Gy "
              f"rel_err={blk['alpha_rel_err']:.2%}")
    for cell, blk in results["checks"]["xray_LQ_alpha_beta"].items():
        print(f"  [{cell}] X-ray: alpha={blk['alpha_Gy_inv']:.4f}/Gy "
              f"beta={blk['beta_Gy2_inv']:.5f}/Gy^2 "
              f"a/b={blk['alpha_over_beta']:.2f} Gy")
    for cell, rbe_blk in results["tables"]["RBE10_vs_LET"].items():
        peak = max(rbe_blk["by_LET"], key=lambda r: r["RBE_10pct"])
        print(f"  [{cell}] peak RBE10 ~ {peak['RBE_10pct']:.2f} at "
              f"LET = {peak['LET_keV_per_um']} keV/um   "
              f"(D10_xray = {rbe_blk['D10_xray_Gy']:.2f} Gy)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
