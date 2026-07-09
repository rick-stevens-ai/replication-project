#!/usr/bin/env python3
"""
Smoke reproduction for Brahme 2024 (Ann Case Rep 9:1625, doi:10.29011/2574-7754.101625).

The paper itself contains NO original data and NO code. What it *does* state
explicitly is the complication-free-cure formula (its Eq. 1):

    P+(D) = PB(D) - PI(D) + delta * (1 - PB(D)) * PI(D)              (Eq. 1)

with delta on the order of 0.2 for many normal-tissue / tumor configurations
(Brahme, near manuscript line 693 / line 1028). The dose-response curves PB
(tumor benefit) and PI (normal-tissue injury) are sigmoid Poisson-derived
curves, parameterised by D50 and the normalized slope gamma50 (or gamma_C),
as in Brahme's other writings (Källman, Ågren, Brahme 1992; Brahme &
Källman series).

This script implements PB and PI as canonical Poisson sigmoids:

    P(D) = 2^(-exp( e * gamma50 * (1 - D/D50) ))                    (eq. P)

and recovers two qualitative claims that the paper makes about Eq. 1:

  (a) The "statistically independent" form P+ = PB*(1-PI) (which equals
      Eq. 1 with delta = 1) over-counts the residual injury term and
      underestimates the achievable complication-free cure relative to
      delta ~ 0.2.
  (b) Reducing the tumor-response slope gamma_C (mimicking the high-LET /
      microdosimetric-heterogeneity penalty that Figures 13-18 emphasise)
      lowers the peak P+ and shifts its optimum.

These are *qualitative* reproductions of the formalism, not refits to any
of Brahme's published TCP/NTCP fits (no such tabular data are released in
this paper).

Run:
    python3 p_plus_smoke.py
Outputs:
    ../figs/p_plus_smoke.png
    ../figs/p_plus_smoke.csv
"""

from __future__ import annotations
import os
import math
import csv

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.abspath(os.path.join(HERE, "..", "figs"))
os.makedirs(FIG_DIR, exist_ok=True)


def poisson_sigmoid(D: np.ndarray, D50: float, gamma50: float) -> np.ndarray:
    """Brahme/Källman canonical Poisson-derived sigmoid.

    P(D) = 2 ** ( -exp( e * gamma50 * (1 - D/D50) ) )

    At D = D50  -> P = 0.5
    dP/d(lnD) at D50 -> gamma50  (definition of the normalized slope).
    """
    return np.power(2.0, -np.exp(math.e * gamma50 * (1.0 - D / D50)))


def p_plus(PB: np.ndarray, PI: np.ndarray, delta: float) -> np.ndarray:
    """Brahme 2024, Eq. (1)."""
    return PB - PI + delta * (1.0 - PB) * PI


def main() -> None:
    # --- Reference tumor + normal-tissue dose-response parameters --------
    # Photon-like, "low-LET" reference (illustrative, not a refit):
    D = np.linspace(0.0, 100.0, 1001)  # Gy or GyE
    D50_T, gamma_T_low = 60.0, 3.0      # tumor
    D50_N, gamma_N = 70.0, 4.0          # normal tissue (a bit steeper, higher D50)
    PB = poisson_sigmoid(D, D50_T, gamma_T_low)
    PI = poisson_sigmoid(D, D50_N, gamma_N)

    # Three values of the correlation parameter delta in Eq. (1):
    deltas = [0.0, 0.2, 1.0]
    Pp = {d: p_plus(PB, PI, d) for d in deltas}

    # --- High-LET-like case: reduce tumor gamma_C to mimic Fig 15/18 -----
    gamma_T_high = 1.8
    PB_high = poisson_sigmoid(D, D50_T, gamma_T_high)
    Pp_high = p_plus(PB_high, PI, 0.2)

    # --- Print and write CSV ---------------------------------------------
    csv_path = os.path.join(FIG_DIR, "p_plus_smoke.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Dose_Gy", "PB_low_LET", "PB_high_LET", "PI",
                    "Pplus_delta0", "Pplus_delta0p2", "Pplus_delta1",
                    "Pplus_high_LET_delta0p2"])
        for i, d in enumerate(D):
            w.writerow([
                f"{d:.3f}", f"{PB[i]:.6f}", f"{PB_high[i]:.6f}", f"{PI[i]:.6f}",
                f"{Pp[0.0][i]:.6f}", f"{Pp[0.2][i]:.6f}", f"{Pp[1.0][i]:.6f}",
                f"{Pp_high[i]:.6f}",
            ])

    summary = []
    for d, arr in Pp.items():
        i = int(np.argmax(arr))
        summary.append((d, float(arr[i]), float(D[i])))
    i_h = int(np.argmax(Pp_high))
    summary_high = (float(Pp_high[i_h]), float(D[i_h]))

    print("Brahme 2024 Eq.(1) smoke replication")
    print("------------------------------------")
    print(f"Tumor:  D50={D50_T} Gy, gamma_C(low LET)={gamma_T_low}, gamma_C(high LET)={gamma_T_high}")
    print(f"Normal: D50={D50_N} Gy, gamma_N={gamma_N}")
    print("Max P+ vs delta (low-LET tumor):")
    for d, mx, dopt in summary:
        print(f"  delta={d:.2f}  ->  P+_max={mx:.3f}  at D*={dopt:.1f} Gy")
    print(f"High-LET (gamma_C={gamma_T_high}), delta=0.2 -> "
          f"P+_max={summary_high[0]:.3f} at D*={summary_high[1]:.1f} Gy")

    # --- Plot -----------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))

    ax = axes[0, 0]
    ax.plot(D, PB, label=f"PB tumor (gamma_C={gamma_T_low})", lw=2)
    ax.plot(D, PI, label=f"PI normal (gamma_N={gamma_N})", lw=2)
    ax.set_xlabel("Dose (Gy or GyE)")
    ax.set_ylabel("Probability")
    ax.set_title("Sigmoid dose-response inputs")
    ax.set_ylim(-0.02, 1.02)
    ax.legend(loc="best", fontsize=9)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    for d in deltas:
        ax.plot(D, Pp[d], label=f"delta={d}", lw=2)
    ax.set_xlabel("Dose (Gy or GyE)")
    ax.set_ylabel("P+ (complication-free cure)")
    ax.set_title("Brahme 2024 Eq.(1): effect of correlation delta")
    ax.set_ylim(-0.02, 1.02)
    ax.legend(loc="best", fontsize=9)
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.plot(D, Pp[0.2], label=f"low LET, gamma_C={gamma_T_low}", lw=2)
    ax.plot(D, Pp_high, label=f"high LET, gamma_C={gamma_T_high}", lw=2)
    ax.set_xlabel("Dose (Gy or GyE)")
    ax.set_ylabel("P+ at delta=0.2")
    ax.set_title("Microdosimetric / LET penalty on P+ (Fig 15/18 motif)")
    ax.set_ylim(-0.02, 1.02)
    ax.legend(loc="best", fontsize=9)
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    ds_scan = np.linspace(0.0, 1.0, 41)
    peak = [np.max(p_plus(PB, PI, d)) for d in ds_scan]
    dopt = [D[int(np.argmax(p_plus(PB, PI, d)))] for d in ds_scan]
    ax.plot(ds_scan, peak, "o-", label="peak P+")
    ax2 = ax.twinx()
    ax2.plot(ds_scan, dopt, "s--", color="tab:red", label="optimal dose D*")
    ax.set_xlabel("delta in Eq.(1)")
    ax.set_ylabel("peak P+", color="tab:blue")
    ax2.set_ylabel("optimal dose D* (Gy)", color="tab:red")
    ax.set_title("Peak P+ and optimal dose vs delta")
    ax.grid(alpha=0.3)

    fig.suptitle(
        "Smoke reproduction of Brahme 2024 Eq.(1) (DOI 10.29011/2574-7754.101625)",
        fontsize=11,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png_path = os.path.join(FIG_DIR, "p_plus_smoke.png")
    fig.savefig(png_path, dpi=140)
    print(f"\nWrote {png_path}")
    print(f"Wrote {csv_path}")


if __name__ == "__main__":
    main()
