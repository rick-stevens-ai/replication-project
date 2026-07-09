#!/usr/bin/env python3
"""
Re-fit a linear-quadratic (LQ) survival model to the Patra et al. 2022 Fig. 2
colony-forming assay, using values digitized visually from the plot.

LQ model on SURVIVING FRACTION:
    SF(D) = exp(-alpha*D - beta*D^2)

Patra et al. report "plating efficiency" not surviving fraction. We normalize
to the 0-Gy control (PE(D)/PE(0)) per the standard clonogenic-assay convention.

Digitized data (mean midpoints, with rough +/- ranges from two independent
visual reads of Fig. 2 right-hand panel — see figures/fig2_panel.png).

Outputs:
  results/lq_fit.json
  figures/fig2_replication.png
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RES  = ROOT / "results"; RES.mkdir(exist_ok=True)
FIG  = ROOT / "figures"; FIG.mkdir(exist_ok=True)

# ----- Digitized Fig. 2 plating efficiency (%) -----
# Two independent visual reads (see PROGRESS.md / REPORT.md). Using midpoints.
dose = np.array([0.0, 5.0, 10.0, 15.0])
pe_pa1     = np.array([87.5, 59.5, 43.5, 14.0])    # %
pe_pa1_sd  = np.array([ 6.0,  3.0,  6.5,  3.0])    # roughly inferred from bar half-width
pe_del     = np.array([85.5, 40.5,  4.5,  1.0])    # %
pe_del_sd  = np.array([ 7.5,  7.5,  1.5,  1.5])

# Surviving fraction = PE(D) / PE(0)
sf_pa1 = pe_pa1 / pe_pa1[0]
sf_del = pe_del / pe_del[0]
# Propagate (rough) relative SD
sf_pa1_sd = sf_pa1 * np.sqrt((pe_pa1_sd/pe_pa1)**2 + (pe_pa1_sd[0]/pe_pa1[0])**2)
sf_del_sd = sf_del * np.sqrt((pe_del_sd/pe_del)**2 + (pe_del_sd[0]/pe_del[0])**2)

def lq(D, alpha, beta):
    return np.exp(-alpha*D - beta*D*D)

def fit(sf, sf_sd):
    # Work in log space to stabilize fit at low SF, but guard zeros
    # We fit directly with weighted nonlinear least squares.
    # Floor SDs to avoid divide-by-zero for points where SD is tiny.
    sigma = np.maximum(sf_sd, 1e-3)
    p0 = (0.1, 0.02)
    popt, pcov = curve_fit(lq, dose, sf, p0=p0, sigma=sigma, absolute_sigma=True, maxfev=20000)
    perr = np.sqrt(np.diag(pcov))
    return popt, perr

(a_w, b_w), (a_w_e, b_w_e) = fit(sf_pa1, sf_pa1_sd)
(a_m, b_m), (a_m_e, b_m_e) = fit(sf_del, sf_del_sd)

# Derived radiobiological metrics
def alpha_beta_ratio(a, b):
    return a / b if b > 1e-9 else float("inf")

def D10(a, b):
    # Dose at which SF = 0.10
    # exp(-a*D - b*D^2) = 0.10 -> b D^2 + a D + ln(0.10) = 0  -> b D^2 + a D - 2.3026 = 0
    if b > 1e-9:
        disc = a*a + 4*b*2.3026
        return (-a + np.sqrt(disc)) / (2*b)
    return 2.3026 / a if a > 0 else float("inf")

def SF2(a, b):
    return float(np.exp(-a*2 - b*4))

def dmf_at(D, a_w, b_w, a_m, b_m):
    # Dose modifying factor at given iso-effect level (typically SF of WT at dose D)
    target = lq(D, a_w, b_w)
    # find D_mut such that SF_mut(D_mut) = target  ->  b_m D^2 + a_m D + ln(target) = 0
    rhs = -np.log(target)
    if b_m > 1e-9:
        disc = a_m*a_m + 4*b_m*rhs
        d_eq = (-a_m + np.sqrt(disc)) / (2*b_m)
    else:
        d_eq = rhs / a_m if a_m > 0 else float("inf")
    return D / d_eq if d_eq > 0 else float("inf")

fit_summary = {
    "PA1_WT": {
        "alpha": a_w, "alpha_se": a_w_e,
        "beta":  b_w, "beta_se":  b_w_e,
        "alpha_over_beta_Gy": alpha_beta_ratio(a_w, b_w),
        "D10_Gy": D10(a_w, b_w),
        "SF2": SF2(a_w, b_w),
    },
    "PA1_PolBetaDelta": {
        "alpha": a_m, "alpha_se": a_m_e,
        "beta":  b_m, "beta_se":  b_m_e,
        "alpha_over_beta_Gy": alpha_beta_ratio(a_m, b_m),
        "D10_Gy": D10(a_m, b_m),
        "SF2": SF2(a_m, b_m),
    },
    "DMF_at_paper_optimal_dose_10Gy": dmf_at(10.0, a_w, b_w, a_m, b_m),
}

print(json.dumps(fit_summary, indent=2))

(RES / "lq_fit.json").write_text(json.dumps(fit_summary, indent=2))

# ----- Replication figure -----
D_smooth = np.linspace(0, 16, 200)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# Left: PE vs dose, with our digitized points
ax = axes[0]
ax.errorbar(dose, pe_pa1, yerr=pe_pa1_sd, fmt='o-', color='black',
            label='PA1 (digitized)', capsize=4, markersize=7)
ax.errorbar(dose, pe_del, yerr=pe_del_sd, fmt='s-', color='red',
            label='PA1PolβΔ (digitized)', capsize=4, markersize=7)
ax.set_xlabel("Dose (Gy)")
ax.set_ylabel("Plating efficiency (%)")
ax.set_title("Fig. 2 digitized (this work)")
ax.set_ylim(0, 100); ax.set_xlim(-1, 17)
ax.grid(True, alpha=0.3); ax.legend()

# Right: SF + LQ fits
ax = axes[1]
ax.errorbar(dose, sf_pa1, yerr=sf_pa1_sd, fmt='o', color='black',
            label='PA1 SF', capsize=4)
ax.errorbar(dose, sf_del, yerr=sf_del_sd, fmt='s', color='red',
            label='PA1PolβΔ SF', capsize=4)
ax.plot(D_smooth, lq(D_smooth, a_w, b_w), '-', color='black',
        label=f'WT LQ: α={a_w:.3f}, β={b_w:.4f}')
ax.plot(D_smooth, lq(D_smooth, a_m, b_m), '-', color='red',
        label=f'Δ  LQ: α={a_m:.3f}, β={b_m:.4f}')
ax.set_yscale("log")
ax.set_xlabel("Dose (Gy)")
ax.set_ylabel("Surviving fraction (PE(D)/PE(0))")
ax.set_title("Linear-quadratic re-fit")
ax.set_xlim(-1, 17); ax.set_ylim(1e-3, 2)
ax.grid(True, which='both', alpha=0.3); ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig(FIG / "fig2_replication.png", dpi=150)
print(f"\nFigure saved to {FIG/'fig2_replication.png'}")
