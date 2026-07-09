"""
Replication of Huang et al. 2022 (J Hepatocell Carcinoma; doi:10.2147/JHC.S383959)
"Boron Neutron Capture Therapy Eliminates Radioresistant Liver Cancer Cells by
Targeting DNA Damage and Repair Responses"

Replicable targets (no wet-lab access required):
  T1. Linear-quadratic (LQ) fits to γ-ray clonogenic curves (Figure 1C),
      and recovery of D10 values for HepG2 and HepG2-R.
  T2. LQ fits to BNCT clonogenic curves (Figure 3B), and recovery of D10
      for HepG2 and HepG2-R after BNCT.
  T3. Recomputation of RBE = D10(γ) / D10(BNCT) using both
      (a) reported D10 values (algebraic check) and (b) refit D10 values.
  T4. Sanity check of Table 1: irradiation time vs dose rate
      (dose = dose_rate * time, given dose_rate 1.18 Gy/min for 1–8 Gy entries).
  T5. Cross-check that the dose-rate of 0.6 Gy/min × 47 s gives ≈0.5 Gy
      (boundary entry uses different distance/dose rate).

Method
------
LQ model: SF(D) = exp(-α D - β D^2),   SF(0)=1.
Fit by weighted least-squares on log(SF) vs D using only nonzero doses
(and excluding the 0-Gy reference which is fixed to 1).

We use two sources of data points:
  (a) Author-reported numerical values (mean ± SD) extracted from the
      Results text — most rigorous.
  (b) Digitized read-offs from Figure 1C / Figure 3B for points whose
      means are NOT cited in the text (used as a secondary cross-check
      only; we DO NOT pretend these are author values).

D10 is solved analytically from SF(D10)=0.1 → α D + β D^2 = ln(10).

Outputs
-------
results/fit_parameters.csv        per curve: alpha, beta, D10_fit, D10_paper, rel_err
results/rbe_table.csv             paper RBE vs our recomputed RBE
results/table1_check.csv          Table 1 cross-check
figures/clonogenic_gamma.png      Fig 1C replication overlay
figures/clonogenic_bnct.png       Fig 3B replication overlay
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(ROOT, "results")
FIGURES = os.path.join(ROOT, "figures")
os.makedirs(RESULTS, exist_ok=True)
os.makedirs(FIGURES, exist_ok=True)


# ---------------------------------------------------------------------------
# Data tables
# ---------------------------------------------------------------------------

@dataclass
class CurveData:
    label: str
    dose: np.ndarray         # Gy
    sf: np.ndarray           # survival fraction
    sd: np.ndarray           # 1-sigma SD on SF (NaN if unknown)
    cited: np.ndarray        # True where mean is text-cited; False where digitized
    paper_d10: float | None  # paper-reported D10 (Gy)


# --- Figure 1C (γ-ray) ----------------------------------------------------
# Text quotes (Results):
#   HepG2-R: SF = 0.91±0.06 (1Gy), 0.59±0.11 (2Gy), 0.15±0.01 (5Gy)
#   HepG2  : SF = 0.54±0.06 (1Gy), 0.27±0.03 (2Gy), 0.03±0.04 (5Gy)
# Other points (0,3,8 Gy) are not cited numerically: digitized from Fig 1C
# (see image-extraction notes); included only for visualization, NOT for the fit
# unless flagged.

fig1c_hepg2 = CurveData(
    label="HepG2, γ-ray (Fig 1C)",
    dose=np.array([1.0, 2.0, 5.0]),
    sf=np.array([0.54, 0.27, 0.03]),
    sd=np.array([0.06, 0.03, 0.04]),
    cited=np.array([True, True, True]),
    paper_d10=3.496,
)

fig1c_hepg2r = CurveData(
    label="HepG2-R, γ-ray (Fig 1C)",
    dose=np.array([1.0, 2.0, 5.0]),
    sf=np.array([0.91, 0.59, 0.15]),
    sd=np.array([0.06, 0.11, 0.01]),
    cited=np.array([True, True, True]),
    paper_d10=5.749,
)

# --- Figure 3B (BNCT) -----------------------------------------------------
# The paper text does NOT give per-point numerical SF for Fig 3B; only D10.
# We digitize the plotted points from Fig 3B for fitting and overlay.
# Image-read-offs (see image-analysis output in repo PROGRESS):
fig3b_hepg2_bnct = CurveData(
    label="HepG2, BNCT (Fig 3B)",
    dose=np.array([1.0, 2.0, 3.0]),
    sf=np.array([0.09, 0.025, 0.002]),
    sd=np.array([0.05, 0.015, 0.001]),
    cited=np.array([False, False, False]),
    paper_d10=0.9513,
)

fig3b_hepg2r_bnct = CurveData(
    label="HepG2-R, BNCT (Fig 3B)",
    dose=np.array([1.0, 2.0, 3.0]),
    sf=np.array([0.11, 0.035, 0.0017]),
    sd=np.array([0.08, 0.02, 0.001]),
    cited=np.array([False, False, False]),
    paper_d10=0.9627,
)

# γ-ray curves repeated in Fig 3B for the same dose range; we just reuse Fig 1C
# parameters and overlay the 1,2,3 Gy reads for visualization only.
fig3b_hepg2_gamma_overlay = (
    np.array([1.0, 2.0, 3.0]),
    np.array([0.57, 0.27, 0.13]),
    np.array([0.10, 0.06, 0.06]),
)
fig3b_hepg2r_gamma_overlay = (
    np.array([1.0, 2.0, 3.0]),
    np.array([0.92, 0.67, 0.40]),
    np.array([0.05, 0.05, 0.28]),
)


# ---------------------------------------------------------------------------
# LQ fit + D10 utilities
# ---------------------------------------------------------------------------

def neg_log_sf(D, alpha, beta):
    """- ln SF(D) under the LQ model."""
    return alpha * D + beta * D * D


def fit_lq(curve: CurveData):
    """Weighted LS fit of LQ to log-SF.

    Weights = (sf/sd)^2  (delta-method approx for variance of ln(SF)).
    Falls back to unweighted if SD missing.
    """
    D = curve.dose
    y = -np.log(curve.sf)
    if np.all(np.isfinite(curve.sd)) and np.all(curve.sd > 0):
        # var(ln SF) ≈ (sd/sf)^2  → sigma on -ln SF
        sigma_y = curve.sd / curve.sf
    else:
        sigma_y = None
    p0 = [0.3, 0.05]
    bounds = ([0.0, 0.0], [5.0, 5.0])
    popt, pcov = curve_fit(
        neg_log_sf, D, y, p0=p0, sigma=sigma_y, absolute_sigma=False, bounds=bounds
    )
    alpha, beta = popt
    perr = np.sqrt(np.diag(pcov)) if pcov is not None and np.all(np.isfinite(pcov)) else (np.nan, np.nan)
    return alpha, beta, perr[0], perr[1]


def d10_from_lq(alpha: float, beta: float) -> float:
    """Solve α D + β D² = ln(10) for D>0."""
    c = -np.log(10.0)
    if beta <= 1e-9:
        return -c / alpha
    disc = alpha * alpha - 4 * beta * c   # c<0 so disc>0
    return (-alpha + np.sqrt(disc)) / (2 * beta)


def fit_and_summarize(curves: Iterable[CurveData]) -> pd.DataFrame:
    rows = []
    for c in curves:
        alpha, beta, da, db = fit_lq(c)
        D10 = d10_from_lq(alpha, beta)
        rel_err = (D10 - c.paper_d10) / c.paper_d10 * 100 if c.paper_d10 else np.nan
        rows.append(
            dict(
                curve=c.label,
                alpha=alpha,
                alpha_se=da,
                beta=beta,
                beta_se=db,
                D10_fit=D10,
                D10_paper=c.paper_d10,
                rel_err_pct=rel_err,
                n_points=len(c.dose),
                points_text_cited=int(c.cited.sum()),
            )
        )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def _doses_dense(dmax: float, n: int = 200) -> np.ndarray:
    return np.linspace(0.0, dmax, n)


def plot_clonogenic(curves: Iterable[CurveData], title: str, outfile: str,
                    dmax: float, overlays: list | None = None):
    fig, ax = plt.subplots(figsize=(5.6, 4.5))
    colors = {
        "HepG2, γ-ray (Fig 1C)":      "tab:blue",
        "HepG2-R, γ-ray (Fig 1C)":    "tab:red",
        "HepG2, BNCT (Fig 3B)":       "tab:cyan",
        "HepG2-R, BNCT (Fig 3B)":     "tab:orange",
    }
    for c in curves:
        col = colors.get(c.label, "k")
        ax.errorbar(c.dose, c.sf, yerr=c.sd, fmt="o", color=col,
                    label=f"{c.label} (data)", capsize=3, markersize=6)
        alpha, beta, *_ = fit_lq(c)
        D = _doses_dense(dmax)
        ax.plot(D, np.exp(-alpha * D - beta * D * D), "-", color=col,
                label=f"  LQ fit: α={alpha:.3f}, β={beta:.3f}")
        D10_fit = d10_from_lq(alpha, beta)
        ax.axvline(D10_fit, color=col, lw=0.6, ls=":", alpha=0.6)
    if overlays:
        for (D, sf, sd, lbl, col, marker) in overlays:
            ax.errorbar(D, sf, yerr=sd, fmt=marker, color=col, alpha=0.5,
                        label=lbl, capsize=3, markersize=5, mfc="white")
    ax.set_yscale("log")
    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Survival fraction")
    ax.set_title(title)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=7, loc="lower left")
    ax.set_ylim(1e-4, 2.0)
    fig.tight_layout()
    fig.savefig(outfile, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Table 1 cross-check
# ---------------------------------------------------------------------------

def table1_check() -> pd.DataFrame:
    """Paper Table 1: dose rate, distance, irradiation time.
    First row uses dose-rate 0.6 Gy/min at distance 40 cm for 0.5 Gy (47 s).
    Remaining rows (1,2,3,5,8 Gy) all use dose-rate 1.18 Gy/min at distance 30 cm.
    Check that listed time ≈ dose / dose-rate.
    """
    rows = [
        (0.5, 0.6, 40, 47),
        (1.0, 1.18, 30, 51),
        (2.0, 1.18, 30, 102),
        (3.0, 1.18, 30, 153),
        (5.0, 1.18, 30, 255),
        (8.0, 1.18, 30, 408),
    ]
    out = []
    for dose, rate, dist, t in rows:
        t_expected = dose / rate * 60.0
        out.append(dict(
            dose_Gy=dose, dose_rate_Gy_per_min=rate, distance_cm=dist,
            time_listed_s=t, time_expected_s=round(t_expected, 1),
            abs_diff_s=round(abs(t - t_expected), 2),
        ))
    return pd.DataFrame(out)


# ---------------------------------------------------------------------------
# RBE recomputation
# ---------------------------------------------------------------------------

def rbe_table(fit_df: pd.DataFrame) -> pd.DataFrame:
    """RBE = D10(γ) / D10(BNCT). Use paper-reported D10s (algebraic check)
    and refit D10s (digitization-sensitive)."""
    def d10(curve_label: str, col: str) -> float:
        row = fit_df.loc[fit_df["curve"] == curve_label].iloc[0]
        return float(row[col])

    rows = []
    for cell, gamma_label, bnct_label, rbe_paper in [
        ("HepG2",   "HepG2, γ-ray (Fig 1C)",   "HepG2, BNCT (Fig 3B)",   3.675),
        ("HepG2-R", "HepG2-R, γ-ray (Fig 1C)", "HepG2-R, BNCT (Fig 3B)", 5.972),
    ]:
        g_paper = d10(gamma_label, "D10_paper")
        b_paper = d10(bnct_label, "D10_paper")
        g_fit   = d10(gamma_label, "D10_fit")
        b_fit   = d10(bnct_label,  "D10_fit")
        rows.append(dict(
            cell=cell,
            D10_gamma_paper=g_paper, D10_bnct_paper=b_paper,
            RBE_paper_recomputed=g_paper / b_paper,
            RBE_paper_stated=rbe_paper,
            paper_arith_match=abs(g_paper / b_paper - rbe_paper) < 5e-3,
            D10_gamma_refit=g_fit, D10_bnct_refit=b_fit,
            RBE_from_our_fits=g_fit / b_fit,
        ))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # T1 + T2 fits
    curves = [fig1c_hepg2, fig1c_hepg2r, fig3b_hepg2_bnct, fig3b_hepg2r_bnct]
    fit_df = fit_and_summarize(curves)
    fit_df.to_csv(os.path.join(RESULTS, "fit_parameters.csv"), index=False)
    print("\n=== LQ fit parameters ===")
    print(fit_df.to_string(index=False))

    # T3 RBE
    rbe_df = rbe_table(fit_df)
    rbe_df.to_csv(os.path.join(RESULTS, "rbe_table.csv"), index=False)
    print("\n=== RBE recomputation ===")
    print(rbe_df.to_string(index=False))

    # T4 Table 1
    t1 = table1_check()
    t1.to_csv(os.path.join(RESULTS, "table1_check.csv"), index=False)
    print("\n=== Table 1 cross-check ===")
    print(t1.to_string(index=False))

    # Figures
    plot_clonogenic(
        [fig1c_hepg2, fig1c_hepg2r],
        "Replication of Fig 1C: γ-ray clonogenic survival",
        os.path.join(FIGURES, "clonogenic_gamma.png"),
        dmax=8.0,
    )
    overlays_fig3b = [
        (*fig3b_hepg2_gamma_overlay,  "HepG2, γ-ray (Fig 3B digitized)",  "tab:blue", "s"),
        (*fig3b_hepg2r_gamma_overlay, "HepG2-R, γ-ray (Fig 3B digitized)", "tab:red",  "s"),
    ]
    plot_clonogenic(
        [fig3b_hepg2_bnct, fig3b_hepg2r_bnct],
        "Replication of Fig 3B: BNCT vs γ-ray clonogenic survival",
        os.path.join(FIGURES, "clonogenic_bnct.png"),
        dmax=3.5,
        overlays=overlays_fig3b,
    )
    print("\nWrote figures to", FIGURES)


if __name__ == "__main__":
    main()
