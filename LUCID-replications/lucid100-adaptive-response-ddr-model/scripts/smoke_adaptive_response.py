#!/usr/bin/env python3
"""
Smoke replication of Piotrowski, Krasowska & Fornalski (2023),
"Mechanistic Modelling of DNA Damage Repair by the Radiation Adaptive
Response Mechanism and Its Significance",
BioMedInformatics 3(1), 150-163, doi:10.3390/biomedinformatics3010011.

This script reproduces the *analytical* curves the paper presents in
Figures 1, 2 (theoretical curve only), and 12.  The full Monte Carlo
model (Figures 3-11) is referenced from Fornalski et al. 2022
Dose-Response and is NOT re-implemented here -- the authors did not
release code or data ("Data Availability Statement: No new data
creation").  This smoke check verifies that the analytical equations
and parameters quoted in the paper reproduce the qualitative behaviour
seen in Figures 1 and 12.

Equations used
--------------
(1)  P_hit(D)   = 1 - exp(-a D)               a = 1.3 Gy^-1
     P_RDEM(D) = 1 - exp(-a2 D)               a2 = 2.4 Gy^-1     (not needed here)
(2)  P_AR(D, k) = alpha0 * D^2 * k^2 * exp(-alpha1*D - alpha2*k)
     alpha0 = 22.9 Gy^-2 h^-3
     alpha1 = 79.4 Gy^-1
     alpha2 = 0.0832 h^-1
(3)  f(D) = (1/(N0 * P_hit(D))) * sum_{n=1..T0-1} S_n(D)
(4)  S_1(D)         = N0 * P_hit(D) * P_AR(D, 1)
     S_n(D) for n>1 = (N0 * P_hit(D) - sum_{i=1..n-1} S_i(D)) * P_AR(D, n)

Constants:
  N0  = 493,000 cells
  T0  = 120 h    (paper says T = 120 h; loop goes n=1..T0-1)

Outputs:
  outputs/fig1_repair_fraction.png   -- equiv. of paper Fig. 1
  outputs/fig12_global_fraction.png  -- equiv. of paper Fig. 12 (f(D) and
                                        f(D) * P_hit(D) i.e. fraction of
                                        whole colony)
  outputs/smoke_summary.json         -- key numeric checks
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---- model parameters (paper-exact) ---------------------------------------

A_HIT = 1.3        # Gy^-1, human lymphocytes / X-rays
ALPHA0 = 22.9      # Gy^-2 h^-3
ALPHA1 = 79.4      # Gy^-1
ALPHA2 = 0.0832    # h^-1

N0_CELLS = 493_000
T0_HOURS = 120     # simulation end (paper uses T = 120 h)


def p_hit(D: np.ndarray | float) -> np.ndarray | float:
    """Eq. (1)."""
    return 1.0 - np.exp(-A_HIT * np.asarray(D))


def p_ar(D: np.ndarray | float, k: int) -> np.ndarray | float:
    """Eq. (2): P_AR(D, k)."""
    D = np.asarray(D, dtype=float)
    return ALPHA0 * (D ** 2) * (k ** 2) * np.exp(-ALPHA1 * D - ALPHA2 * k)


def repair_fraction(D_vec: np.ndarray, N0: int = N0_CELLS, T0: int = T0_HOURS):
    """Compute analytical f(D) per Eq. (3)-(4) over a vector of doses.

    Returns
    -------
    f       : f(D)                                          (cells repaired / cells hit)
    S_total : sum_n S_n(D)                                  (total repaired cells)
    cells_hit : N0 * P_hit(D)                               (cells hit by dose pulse)
    """
    D_vec = np.asarray(D_vec, dtype=float)
    cells_hit = N0 * p_hit(D_vec)                # vector over D
    S_total = np.zeros_like(D_vec)
    # Track cumulative sum so we can build S_n recursively per dose
    cum = np.zeros_like(D_vec)
    for n in range(1, T0):                       # n = 1 .. T0-1
        par_n = p_ar(D_vec, n)
        if n == 1:
            S_n = cells_hit * par_n
        else:
            S_n = (cells_hit - cum) * par_n
            # Clamp tiny negatives from float arithmetic (cum may overshoot for D
            # values where almost all hit cells get "repaired" in early n).
            S_n = np.where(S_n < 0, 0.0, S_n)
        cum = cum + S_n
        S_total = S_total + S_n
    # Avoid div by zero at D = 0
    safe = np.where(cells_hit > 0, cells_hit, 1.0)
    f = np.where(cells_hit > 0, S_total / safe, 0.0)
    return f, S_total, cells_hit


# ---- main ------------------------------------------------------------------

def main() -> None:
    here = Path(__file__).resolve().parent
    out_dir = here.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Paper Fig. 1 sweeps a single dose pulse; the legend/x-axis ranges to
    # ~150 mGy.  Use a fine grid from 0 to 200 mGy.
    D_mGy = np.linspace(0.0, 200.0, 401)
    D_Gy = D_mGy / 1000.0

    f, S_total, cells_hit = repair_fraction(D_Gy)

    # Replica of Figure 1: f(D) (ratio repaired-to-hit) vs D in mGy.
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.plot(D_mGy, 100.0 * f, color="tab:blue", lw=2,
            label=r"analytical $f(D)$ (Eq. 3)")
    ax.set_xlabel("Dose pulse D [mGy]")
    ax.set_ylabel("Repair fraction f(D) [%]\n(cells repaired by AR / cells hit)")
    ax.set_title("Smoke replica of Fig. 1 — "
                 f"N0={N0_CELLS:,}, T0={T0_HOURS} h")
    ax.set_ylim(0, 110)
    ax.set_xlim(0, 200)
    ax.axvspan(10, 45, alpha=0.10, color="tab:green",
               label="paper's quoted ~100% band (10-45 mGy)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "fig1_repair_fraction.png", dpi=150)
    plt.close(fig)

    # Replica of Figure 12: cell repair fraction in reference to the global
    # colony (N0) vs D.  This is f(D) * P_hit(D) = S_total / N0.
    global_frac = S_total / N0_CELLS
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.plot(D_mGy, 100.0 * global_frac, color="tab:red", lw=2,
            label=r"$f(D)\cdot P_{hit}(D)$ = $S_{total}/N_0$")
    ax.set_xlabel("Dose pulse D [mGy]")
    ax.set_ylabel("Fraction of WHOLE population [%]")
    ax.set_title("Smoke replica of Fig. 12 (analytical curve only)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "fig12_global_fraction.png", dpi=150)
    plt.close(fig)

    # Numeric sanity checks
    # Paper: "within the range of 10-45 mGy, the ratio ... is ~100%"
    idx_band = (D_mGy >= 10) & (D_mGy <= 45)
    f_band_mean = float(np.mean(f[idx_band]))
    f_band_min = float(np.min(f[idx_band]))
    f_band_max = float(np.max(f[idx_band]))

    # Paper: "focusing on the whole system, this phenomenon practically
    # disappears, and it is at the level of 0.126%".  This refers to global
    # repair fraction over the *colony* at the optimum.  Find peak.
    peak_idx = int(np.argmax(global_frac))
    peak_dose = float(D_mGy[peak_idx])
    peak_global = float(global_frac[peak_idx])

    # Verify analytical PAR peak time for D at optimum
    # P_AR maximum in k: dP/dk = 0 -> k* = 2/alpha2
    k_star = 2.0 / ALPHA2
    # And in D: k constant, dP/dD = 0 -> D* = 2/alpha1
    D_star_Gy = 2.0 / ALPHA1
    D_star_mGy = D_star_Gy * 1000.0

    summary = {
        "model": {
            "a_hit_Gy_inv": A_HIT,
            "alpha0_Gy2_h3_inv": ALPHA0,
            "alpha1_Gy_inv": ALPHA1,
            "alpha2_h_inv": ALPHA2,
            "N0_cells": N0_CELLS,
            "T0_hours": T0_HOURS,
        },
        "analytical_PAR_peak": {
            "k_star_hours": k_star,
            "D_star_Gy": D_star_Gy,
            "D_star_mGy": D_star_mGy,
        },
        "fig1_replica": {
            "dose_band_mGy": [10, 45],
            "f_mean_in_band_pct": 100.0 * f_band_mean,
            "f_min_in_band_pct":  100.0 * f_band_min,
            "f_max_in_band_pct":  100.0 * f_band_max,
            "paper_claim": "ratio ~100% in 10-45 mGy band",
            "pass_qualitative": bool(f_band_min > 0.50),
        },
        "fig12_replica": {
            "peak_dose_mGy": peak_dose,
            "peak_global_fraction_pct": 100.0 * peak_global,
            "paper_claim_pct": 0.126,
            "qualitative_check": (
                "peak should sit near a few tens of mGy and be << 1% "
                "(paper quotes 0.126%)"
            ),
        },
        "outputs": [
            str((out_dir / "fig1_repair_fraction.png").resolve()),
            str((out_dir / "fig12_global_fraction.png").resolve()),
        ],
    }
    with open(out_dir / "smoke_summary.json", "w") as fp:
        json.dump(summary, fp, indent=2)

    print("=" * 60)
    print("SMOKE REPLICA OF PIOTROWSKI/KRASOWSKA/FORNALSKI 2023")
    print("=" * 60)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
