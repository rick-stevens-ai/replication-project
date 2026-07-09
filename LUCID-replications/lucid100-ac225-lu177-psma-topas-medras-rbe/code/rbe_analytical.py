#!/usr/bin/env python3
"""Analytical reproduction of Fig 9 RBE(D) curves using the published
Table 3 (177Lu) and Table 4 (225Ac) fit parameters from
Rumiantcev et al. 2023, EJNMMI Physics 10:53.

The paper fits N_DSB(D) per cell-geometry × internalization × 2D/3D:
  177Lu: N = a_Lu * D^2 + b_Lu * D  (linear-quadratic, with a_Lu fixed to 0
                                     for the initial-damage curves)
  225Ac: N = b_Ac * D               (linear)

Isoeffect (N_DSB equal) → RBE_225Ac(D_177Lu) [Eq. 6] or RBE_225Ac(D_225Ac) [Eq. 7].

This script regenerates the limit
  lim_{D->0} RBE_225Ac = b_225Ac / b_177Lu
for every entry of Tables 3 & 4, prints a comparison table, and writes
a CSV + matplotlib figure of RBE(D_177Lu) for the 3D scenario.
"""
from __future__ import annotations
import csv
import math
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"
FIGURES = HERE.parent / "figures"
RESULTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

# --- Published Table 3: 177Lu fit parameters (b_init = b_Lu for initial dmg;
#     a_repair + b_repair = a_Lu, b_Lu for post-repair LQ fit). ----------------
# Schema: (cell_geom, internalization, arrangement, b_init, b_repair, a_repair)
TABLE3 = [
    (1, "int.",   "2D", 76.75, 16.84, 0.30),
    (1, "membr.", "2D", 77.17, 17.00, 0.00),
    (2, "int.",   "2D", 79.13, 15.91, 1.36),
    (2, "membr.", "2D", 78.00, 15.42, 1.06),
    (3, "int.",   "2D", 79.31, 17.13, 0.00),
    (3, "membr.", "2D", 77.18, 11.63, 4.51),
    (4, "int.",   "2D", 78.28, 14.84, 2.67),
    (4, "membr.", "2D", 76.40,  9.43, 6.89),
    (5, "int.",   "2D", 78.78, 16.54, 0.43),
    (5, "membr.", "2D", 75.57, 14.27, 1.87),
    (1, "int.",   "3D", 77.69, 16.31, 1.21),
    (1, "membr.", "3D", 78.28, 15.50, 1.45),
    (2, "int.",   "3D", 76.89, 15.05, 1.32),
    (2, "membr.", "3D", 78.93, 14.87, 1.49),
    (3, "int.",   "3D", 76.94, 14.41, 1.49),
    (3, "membr.", "3D", 76.59, 16.35, 1.11),
    (4, "int.",   "3D", 77.19, 14.48, 1.48),
    (4, "membr.", "3D", 77.57, 15.73, 1.30),
    (5, "int.",   "3D", 77.41, 14.86, 1.48),
    (5, "membr.", "3D", 77.20, 15.10, 1.32),
]

# --- Published Table 4: 225Ac fit parameters. ----------------------------------
# Schema: (cell_geom, internalization, arrangement, b_init_225, b_repair_225)
TABLE4 = [
    (1, "int.",   "2D", 163.10, 145.36),
    (1, "membr.", "2D", 160.81, 144.95),
    (2, "int.",   "2D", 161.95, 143.88),
    (2, "membr.", "2D", 161.97, 144.90),
    (3, "int.",   "2D", 157.35, 137.71),
    (3, "membr.", "2D", 159.63, 142.29),
    (4, "int.",   "2D", 157.15, 137.76),
    (4, "membr.", "2D", 163.13, 143.89),
    (5, "int.",   "2D", 160.69, 141.67),
    (5, "membr.", "2D", 160.12, 142.74),
    (1, "int.",   "3D", 166.60, 152.99),
    (1, "membr.", "3D", 166.96, 154.34),
    (2, "int.",   "3D", 164.56, 150.75),
    (2, "membr.", "3D", 167.69, 154.83),
    (3, "int.",   "3D", 169.71, 156.25),
    (3, "membr.", "3D", 165.86, 152.59),
    (4, "int.",   "3D", 164.95, 150.78),
    (4, "membr.", "3D", 164.47, 149.65),
    (5, "int.",   "3D", 164.49, 150.94),
    (5, "membr.", "3D", 165.55, 152.14),
]


def rbe_vs_DLu(D_Lu: np.ndarray, b_Lu: float, a_Lu: float, b_Ac: float) -> np.ndarray:
    """Eq. 6: RBE_225Ac(D_177Lu) = (a_Lu * D_Lu + b_Lu) / b_Ac.

    The paper writes it inversely (b_Ac/(a_Lu*D_Lu + b_Lu)) but conventionally
    RBE > 1 means the test radiation is more effective per Gy than the
    reference, so RBE = b_Ac/b_Lu at D->0 is the published low-dose limit.
    """
    return b_Ac / (a_Lu * D_Lu + b_Lu)


def rbe_vs_DAc(D_Ac: np.ndarray, b_Lu: float, a_Lu: float, b_Ac: float) -> np.ndarray:
    """Eq. 7: RBE_225Ac(D_225Ac) = 2 * b_Ac / (sqrt(b_Lu^2 + 4*a_Lu*b_Ac*D_Ac) + b_Lu)."""
    return 2 * b_Ac / (np.sqrt(b_Lu ** 2 + 4 * a_Lu * b_Ac * D_Ac) + b_Lu)


def join_tables():
    """Merge Table 3 and Table 4 on (geom, intern, arr)."""
    lu = {(g, i, a): (b_init, b_rep, a_rep) for g, i, a, b_init, b_rep, a_rep in TABLE3}
    ac = {(g, i, a): (b_init, b_rep) for g, i, a, b_init, b_rep in TABLE4}
    rows = []
    for k in lu:
        bLu_i, bLu_r, aLu_r = lu[k]
        bAc_i, bAc_r = ac[k]
        rows.append((*k, bLu_i, bLu_r, aLu_r, bAc_i, bAc_r))
    return rows


def main():
    rows = join_tables()
    csv_path = RESULTS / "rbe_low_dose_limit_per_config.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "cell_geom", "internalization", "arrangement",
            "b_Lu_initial", "b_Lu_repair", "a_Lu_repair",
            "b_Ac_initial", "b_Ac_repair",
            "RBE_init_lowdose (b_Ac_i / b_Lu_i)",
            "RBE_repair_lowdose (b_Ac_r / b_Lu_r)",
        ])
        for g, i, a, bLu_i, bLu_r, aLu_r, bAc_i, bAc_r in rows:
            w.writerow([g, i, a, bLu_i, bLu_r, aLu_r, bAc_i, bAc_r,
                        round(bAc_i / bLu_i, 4),
                        round(bAc_r / bLu_r, 4)])
    print(f"wrote {csv_path}")

    # Paper headline check: 3D, geom 1, internalized
    for g, i, a, bLu_i, bLu_r, aLu_r, bAc_i, bAc_r in rows:
        if g == 1 and i == "int." and a == "3D":
            init_rbe = bAc_i / bLu_i
            print(
                f"[CHECK 3D / geom 1 / internalized] "
                f"RBE_init_lowdose = {init_rbe:.3f} "
                f"(paper says ~2.14)"
            )

            # Eq. 7 evaluated at 0 and 50 Gy of 225Ac dose
            d_ac = np.array([0.0, 50.0])
            rbe = rbe_vs_DAc(d_ac, bLu_r, aLu_r, bAc_r)
            print(
                f"[CHECK 3D / geom 1 / internalized, post-repair Eq. 7] "
                f"RBE(0 Gy)={rbe[0]:.3f}, RBE(50 Gy)={rbe[1]:.3f} "
                f"(paper headline 9.38 → 1.46)"
            )
            break

    # Reproduce Fig 9-style curves for the 3D, internalized configs
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    D_Lu = np.linspace(0.01, 50, 200)
    D_Ac = np.linspace(0.01, 50, 200)
    for g, i, a, bLu_i, bLu_r, aLu_r, bAc_i, bAc_r in rows:
        if a != "3D" or i != "int.":
            continue
        axes[0].plot(D_Lu, rbe_vs_DLu(D_Lu, bLu_r, aLu_r, bAc_r),
                     label=f"geom {g} (repair)")
        axes[1].plot(D_Ac, rbe_vs_DAc(D_Ac, bLu_r, aLu_r, bAc_r),
                     label=f"geom {g} (repair)")
    axes[0].set_xlabel("D_{177Lu}  [Gy]")
    axes[0].set_ylabel("RBE_{225Ac}")
    axes[0].set_title("Post-repair RBE vs D_{177Lu} (Eq. 6) — 3D, internalized")
    axes[0].legend(fontsize=8)
    axes[0].grid(alpha=0.3)
    axes[1].set_xlabel("D_{225Ac}  [Gy]")
    axes[1].set_ylabel("RBE_{225Ac}")
    axes[1].set_title("Post-repair RBE vs D_{225Ac} (Eq. 7) — 3D, internalized")
    axes[1].legend(fontsize=8)
    axes[1].grid(alpha=0.3)
    fig.tight_layout()
    out_png = FIGURES / "fig9_repro_3D_internalized.png"
    fig.savefig(out_png, dpi=130)
    print(f"wrote {out_png}")


if __name__ == "__main__":
    main()
