#!/usr/bin/env python3
"""
Minimal smoke replication of the closed-form quantities in
Belov O et al., "Dose-Dependent Shift in Relative Contribution of Homologous
Recombination to DNA Repair after Low-LET Ionizing Radiation Exposure: Empirical
Evidence and Numerical Simulation", Curr. Issues Mol. Biol. 45(9):7352-7373 (2023).
DOI 10.3390/cimb45090465. Source paper-only, no code released by authors.

This script verifies two quantities that are fully specified in the paper text
and Appendix C parameter table, without requiring the full ODE solve:

  1. Initial DSB yield per cell vs. dose (Eq. A1 + alpha(L) = a * exp(-b*L)).
     Paper values: a = 27.5, b = 2.43e-3, with L = LET in keV/um.
     For low-LET X-rays (RUB RUST-M1, 200 kVp ~ 0.3-2 keV/um), alpha(L) ~ 27.5.

  2. Irreparable-DSB fraction Nirrep(D) piecewise function from Table A1:
        Nirrep(D) = 0.12 * exp(-2.48 * D^2.02) - 0.11 * exp(-5.43 * D^0.76),  D<1
        Nirrep(D) = 0.01,                                                       D>=1
     This is the residual-foci floor at 24 h that the paper attributes to HR-
     unresolved damage and feeds into the PHR(D) calculation.

Outputs CSVs and one PNG into ../results/ and ../figures/.

Runs in <1 second on a laptop CPU.
"""
import math
import os
import csv
from pathlib import Path

import numpy as np

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover
    plt = None

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

# Paper parameters from Table A1 (Appendix C).
A = 27.5             # Gy^-1 per cell (DSB induction slope at L=0)
B = 2.43e-3          # keV/um^-1 (LET attenuation)
LET_XRAY_KEVUM = 0.3 # representative low-LET X-ray track-averaged LET; sensitivity tested below

# Dose grid used by the paper (Section 2.1.2 + Section 3.1): 20, 40, 80, 160, 250, 500, 1000 mGy.
DOSES_MGY_PAPER = np.array([20.0, 40.0, 80.0, 160.0, 250.0, 500.0, 1000.0])


def alpha_of_L(L_keVum: float) -> float:
    """DSB induction slope alpha(L) = a * exp(-b * L)  (Gy^-1 per cell)."""
    return A * math.exp(-B * L_keVum)


def initial_dsb_yield(dose_Gy: np.ndarray, L_keVum: float = LET_XRAY_KEVUM) -> np.ndarray:
    """Eq. (A1) integrated for a delivered dose D (Gy): N0 = alpha(L) * D."""
    return alpha_of_L(L_keVum) * dose_Gy


def nirrep(dose_Gy: np.ndarray) -> np.ndarray:
    """Table A1: Nirrep piecewise function of dose D (Gy)."""
    d = np.asarray(dose_Gy, dtype=float)
    low = 0.12 * np.exp(-2.48 * d ** 2.02) - 0.11 * np.exp(-5.43 * d ** 0.76)
    out = np.where(d < 1.0, low, 0.01)
    return out


def main() -> None:
    print(f"alpha(L=0)            = {alpha_of_L(0.0):.4f} DSB/Gy/cell  (paper a = {A})")
    print(f"alpha(L={LET_XRAY_KEVUM:.2f} keV/um) = {alpha_of_L(LET_XRAY_KEVUM):.4f} DSB/Gy/cell")
    print(f"alpha(L=1.0 keV/um)   = {alpha_of_L(1.0):.4f} DSB/Gy/cell")
    print(f"alpha(L=10  keV/um)   = {alpha_of_L(10.0):.4f} DSB/Gy/cell")

    doses_Gy = DOSES_MGY_PAPER / 1000.0
    n0 = initial_dsb_yield(doses_Gy)
    ni = nirrep(doses_Gy)
    ni_pct = 100.0 * ni / np.maximum(n0 / np.maximum(n0, 1e-12), 1e-12)  # fraction, not percent of N0
    # Note: paper defines Nirrep as a fraction (limits to ~0.01 at D>=1 Gy).
    # That fraction is what is residual at 24h relative to peak; report it directly.

    # Write CSV
    csv_path = RESULTS / "smoke_dsb_yield.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dose_mGy", "dose_Gy", "alpha_xray_per_Gy_per_cell", "N0_DSBs_per_cell", "Nirrep_fraction"])
        for d_mgy, d_gy, n, nr in zip(DOSES_MGY_PAPER, doses_Gy, n0, ni):
            w.writerow([f"{d_mgy:g}", f"{d_gy:g}", f"{alpha_of_L(LET_XRAY_KEVUM):.4f}", f"{n:.4f}", f"{nr:.4f}"])
    print(f"\nWrote {csv_path}")
    print(f"{'Dose (mGy)':>10} {'N0 DSBs/cell':>14} {'Nirrep frac':>12}")
    for d, n, nr in zip(DOSES_MGY_PAPER, n0, ni):
        print(f"{d:>10g} {n:>14.3f} {nr:>12.4f}")

    # Fine grid for figure
    dose_fine_mGy = np.linspace(0.0, 1000.0, 1001)
    dose_fine_Gy = dose_fine_mGy / 1000.0
    n0_fine = initial_dsb_yield(dose_fine_Gy)
    ni_fine = nirrep(dose_fine_Gy)
    # Per-cell residual count = Nirrep * N0
    resid_fine = ni_fine * n0_fine

    grid_path = RESULTS / "smoke_dsb_yield_grid.csv"
    with open(grid_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dose_mGy", "N0_DSBs_per_cell", "Nirrep_fraction", "N_residual_24h_per_cell"])
        for d, n, nr, r in zip(dose_fine_mGy, n0_fine, ni_fine, resid_fine):
            w.writerow([f"{d:g}", f"{n:.4f}", f"{nr:.6f}", f"{r:.6f}"])
    print(f"Wrote {grid_path}")

    if plt is None:
        print("matplotlib not available; skipping figure.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(dose_fine_mGy, n0_fine, color="C0")
    axes[0].scatter(DOSES_MGY_PAPER, n0, color="C0", marker="o", zorder=3, label="paper dose points")
    axes[0].set_xlabel("Dose (mGy)")
    axes[0].set_ylabel("Initial DSB yield N0 (per cell)")
    axes[0].set_title("Eq. (A1): N0 = a·exp(-bL)·D")
    axes[0].legend(loc="upper left")
    axes[0].grid(alpha=0.3)

    axes[1].plot(dose_fine_mGy, ni_fine, color="C3", label="Nirrep(D)")
    axes[1].scatter(DOSES_MGY_PAPER, ni, color="C3", marker="o", zorder=3)
    axes[1].set_xlabel("Dose (mGy)")
    axes[1].set_ylabel("Irreparable DSB fraction (24 h)")
    axes[1].set_title("Table A1: Nirrep(D)  piecewise")
    axes[1].set_ylim(0, 0.12)
    axes[1].grid(alpha=0.3)

    fig.suptitle("Belov et al. 2023 (CIMB 45:7352) — closed-form smoke checks", fontsize=11)
    fig.tight_layout()
    out_png = FIGURES / "smoke_dsb_yield.png"
    fig.savefig(out_png, dpi=140)
    print(f"Wrote {out_png}")


if __name__ == "__main__":
    main()
