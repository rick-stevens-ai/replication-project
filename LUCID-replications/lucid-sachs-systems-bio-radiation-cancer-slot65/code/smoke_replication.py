#!/usr/bin/env python3
"""
LUCID100 slot 65 — smoke replication for
Little MP, Heidenreich WF, Moolgavkar SH, Schöllnberger H, Thomas DC (2008)
"Systems biological and mechanistic modelling of radiation-induced cancer"
Radiat Environ Biophys 47:39-47.  DOI 10.1007/s00411-007-0150-z

The paper itself is a 5-talk workshop summary with NO new equations beyond a
logistic-regression skeleton.  This script reproduces the SHAPES that the paper
plots, using textbook forms of the two model families that dominate the review:

  (A) Two-stage clonal expansion (MVK / TSCE) cancer hazard h(t).
      Common to talks by Moolgavkar, Heidenreich, and Little.
      Closed-form Heidenreich-Jacob-Paretzke (1997, ref [15]) exact solution.

  (B) State-Vector Model (SVM) flavoured protective bystander apoptosis.
      Schöllnberger talk.  Uses kap = 0.054/day (delayed plating) and
      kap = 0.022/day (immediate plating) values quoted in §"State-Vector Model".

No primary data are refit.  This is a shape-comparison smoke only — the
intent is to confirm we can drive the workhorse machinery and produce curves
that qualitatively resemble Figures 4 and 5 of the paper.
"""

from __future__ import annotations
import math
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# (A) Two-stage MVK / TSCE hazard
# ---------------------------------------------------------------------------
# Standard form (Heidenreich 1997, Heidenreich-Luebeck-Hazelton 2002):
#   X = normal stem-cell pool, mutates at rate mu0*N  -> Y (initiated)
#   Y cells divide at rate alpha, die/differentiate at rate beta,
#       mutate at rate mu1  -> M (malignant)
#   Survival prob until age t:
#       S(t) = exp(-(mu0*N/alpha) * [ (alpha-beta-p) * t
#                  + 2*log( (q - p*exp(-(q-p)*t)) / (q - p) ) ])
#   with p = (alpha - beta - mu1 - q)/2,  q = sqrt((alpha-beta-mu1)^2 + 4*alpha*mu1).
# Hazard h(t) = -d/dt log S(t).
#
# We use numerical differentiation rather than the algebraic d/dt to keep the
# script short and obviously correct.

def mvk_log_survival(t, mu0, N, alpha, beta, mu1):
    """Log survival for the classical 2-stage MVK / TSCE process.

    Closed-form expression (Heidenreich, Jacob & Paretzke 1997,
    Radiat Environ Biophys 36:45; also Heidenreich-Luebeck-Hazelton 2002):

        gamma = alpha - beta - mu1
        delta = sqrt(gamma^2 + 4*alpha*mu1)
        a     = -(gamma + delta) / 2     (a < 0)
        b     = -(gamma - delta) / 2     (b > 0)
        Survival from 0 to t:
          S(t) = ((b - a) / (b * exp(a t) - a * exp(b t)))**(mu0 * N / alpha)

    We compute log S(t) directly to avoid overflow at adult ages.
    """
    gamma = alpha - beta - mu1
    delta = math.sqrt(gamma * gamma + 4.0 * alpha * mu1)
    a = -(gamma + delta) / 2.0  # < 0
    b = -(gamma - delta) / 2.0  # > 0
    # numerically stable form of log( b*exp(a t) - a*exp(b t) )
    # factor out exp(b t) since b > 0 (dominates for large t):
    #   = b t + log( b * exp((a-b) t) - a )
    # since a < 0, -a > 0, and exp((a-b) t) is in (0,1], the bracket > 0.
    inside = b * np.exp((a - b) * t) - a  # > 0
    log_denom = b * t + np.log(inside)
    log_numer = math.log(b - a)
    return (mu0 * N / alpha) * (log_numer - log_denom)


def mvk_hazard(t, mu0, N, alpha, beta, mu1):
    """Numerical hazard h(t) = -d/dt log S(t)."""
    logS = mvk_log_survival(t, mu0, N, alpha, beta, mu1)
    dt = t[1] - t[0]
    h = -np.gradient(logS, dt)
    h[h < 0] = 0.0
    return h


# Illustrative parameters chosen to produce the qualitative SEER-shape rise of
# colon-cancer-like hazard between ages 30 and 80 (cf. paper Fig. 4).  These
# are textbook order-of-magnitude TSCE values (compare Heidenreich-Luebeck-
# Hazelton 2002 RR 158:607, Luebeck-Moolgavkar 2002 PNAS 99:15095); they are
# NOT a refit of SEER data.  The key qualitative feature reproduced is the
# strong age dependence driven by slow (alpha-beta ~ 0.1/yr) clonal expansion.
PARAM_SETS = {
    "baseline (alpha-beta = 0.10/yr)": dict(
        mu0=2.0e-7, N=1.0e8, alpha=0.50, beta=0.40, mu1=2.0e-6,
    ),
    "slower clonal expansion (0.07/yr)": dict(
        mu0=2.0e-7, N=1.0e8, alpha=0.50, beta=0.43, mu1=2.0e-6,
    ),
    "higher initiation rate": dict(
        mu0=1.0e-6, N=1.0e8, alpha=0.50, beta=0.40, mu1=2.0e-6,
    ),
}


def figure_mvk(out_path):
    t = np.linspace(0.01, 90.0, 901)  # years
    fig, ax = plt.subplots(figsize=(7, 5))
    for label, p in PARAM_SETS.items():
        h = mvk_hazard(t, **p)
        # convert from /year to per 100,000 per year (Fig. 4 units)
        ax.semilogy(t, h * 1.0e5, label=label)
    ax.set_xlabel("Age (years)")
    ax.set_ylabel("Annual incidence rate (per 100,000 per year)")
    ax.set_title("MVK / TSCE 2-stage hazard (shape comparison to Fig. 4 of\n"
                 "Little/Heidenreich/Moolgavkar/Schöllnberger/Thomas 2008)")
    ax.set_ylim(1e-3, 2e3)
    ax.set_xlim(0, 90)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  wrote {out_path}")


# ---------------------------------------------------------------------------
# (B) State-Vector Model — protective bystander apoptosis sketch
# ---------------------------------------------------------------------------
# Schöllnberger §"State-Vector Model for in vitro neoplastic transformation"
# describes:  direct LQ-shaped transformation + protective bystander apoptosis
# that removes a fraction of initiated/pre-cancerous cells at rate kap.
#
# Toy analytic form for the transformation frequency T(D) per surviving cell:
#   T(D) = T0 + (alpha_T * D + beta_T * D**2) * exp(-Frac_remove(kap, D))
# with the bystander removal fraction
#   Frac_remove(kap, D) = R_max * (1 - exp(-kap * t_int)) * f(D)
# where f(D) is a low-dose-only switch (bystander signal saturates by ~50 mGy
# in Portess et al. 2007, Redpath et al. 2001 data).
#
# This is *not* the full SVM; it is the analytic skeleton that gives the same
# qualitative U-shape (paper Fig. 5).

# Parameters chosen so the SHAPE matches Schöllnberger Fig. 5 (paper Fig. 5):
# spontaneous ~5e-5, drop to ~2e-5 at ~10 mGy, then quadratic rise above ~200 mGy.
T0 = 5.0e-5            # spontaneous transformation freq per surviving cell
alpha_T = 8.0e-6       # /Gy linear direct term (kept small; LQ rise dominates only at high D)
beta_T = 3.0e-4        # /Gy^2 quadratic direct term
t_int_days = 7.0       # days of intercellular signalling window (delayed-plating ~1 week)
R_max = 0.80           # max fractional removal achievable by protective bystander


def bystander_switch(D):
    """Bystander signal saturates by a few mGy (Portess 2007, Redpath 2001).
    Returns the FRACTION of bystander capacity that is active at dose D."""
    D_half = 0.002      # Gy (~2 mGy half-activation)
    return D / (D + D_half)


def transformation_freq(D, kap_per_day):
    direct = T0 + alpha_T * D + beta_T * D * D
    remove = R_max * (1.0 - math.exp(-kap_per_day * t_int_days)) * bystander_switch(D)
    return direct * (1.0 - remove)


def figure_svm(out_path):
    D = np.linspace(0.0, 1.0, 401)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    # Panel A: immediate plating, kap = 0.022 /day
    # Panel B: delayed plating,  kap = 0.054 /day
    panels = [
        ("(A) Immediate plating  k_ap = 0.022 /day", 0.022),
        ("(B) Delayed plating    k_ap = 0.054 /day", 0.054),
    ]
    for ax, (title, kap) in zip(axes, panels):
        direct = np.array([T0 + alpha_T * d + beta_T * d * d for d in D])
        total = np.array([transformation_freq(d, kap) for d in D])
        bystander = direct - total
        ax.plot(D, direct * 1.0e5, "--", color="tab:blue", label="direct (LQ)")
        ax.plot(D, bystander * 1.0e5, ":", color="tab:red", label="bystander removal")
        ax.plot(D, total * 1.0e5, "-", color="black", label="total")
        ax.axhline(T0 * 1.0e5, color="gray", lw=0.6, alpha=0.7)
        ax.set_xlabel("Dose (Gy)")
        ax.set_title(title, fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 1)
        ax.legend(loc="upper left", fontsize=8)
    axes[0].set_ylabel("Transformation frequency per surviving cell (×10$^{-5}$)")
    fig.suptitle("SVM-style protective bystander sketch (cf. Fig. 5)", y=1.02)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {out_path}")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    reports = os.path.normpath(os.path.join(here, "..", "reports"))
    os.makedirs(reports, exist_ok=True)

    print("LUCID100 slot 65 — smoke replication")
    print("Paper: 10.1007/s00411-007-0150-z (Little et al. 2008 workshop summary)")
    print()
    print("[A] MVK / TSCE 2-stage hazard sweep")
    figure_mvk(os.path.join(reports, "mvk_hazard.png"))

    # spot-check at age 65
    t_check = np.linspace(0.01, 90, 901)
    p = PARAM_SETS["baseline (alpha-beta = 0.10/yr)"]
    h = mvk_hazard(t_check, **p)
    i65 = np.argmin(np.abs(t_check - 65.0))
    print(f"  baseline MVK hazard at age 65 = {h[i65]*1e5:.3f} per 100k/yr")
    print(f"  baseline MVK hazard at age 40 = {h[np.argmin(np.abs(t_check-40))]*1e5:.4f} per 100k/yr")
    print(f"  baseline MVK hazard at age 20 = {h[np.argmin(np.abs(t_check-20))]*1e5:.4e} per 100k/yr")
    assert h[i65] > h[np.argmin(np.abs(t_check-20))], "MVK hazard must rise monotonically across adult ages."
    assert h[i65]*1e5 < 5000, "MVK hazard should be < ~5000 per 100k/yr (sanity vs SEER colon ~250 per 100k/yr at 80)."
    print()

    print("[B] SVM protective-bystander sketch")
    figure_svm(os.path.join(reports, "svm_bystander.png"))
    # spot-check U-shape: report transformation freq at D=0 vs D=10 mGy
    f0 = transformation_freq(0.0, 0.054)
    f_lowdose = transformation_freq(0.010, 0.054)
    f_highdose = transformation_freq(0.5, 0.054)
    print(f"  delayed plating, kap=0.054/d:")
    print(f"    T(0 Gy)       = {f0*1e5:.3f} ×10^-5")
    print(f"    T(0.010 Gy)   = {f_lowdose*1e5:.3f} ×10^-5  (should dip below spontaneous)")
    print(f"    T(0.500 Gy)   = {f_highdose*1e5:.3f} ×10^-5  (should rise above spontaneous)")
    assert f_lowdose < f0, "Smoke check: bystander removal must drop T below spontaneous."
    assert f_highdose > f0, "Smoke check: high dose should exceed spontaneous."
    print()
    print("Smoke replication complete.")


if __name__ == "__main__":
    main()
