"""
Validate the reimplemented Mariotti 2013 model:

  1. Plot the eq.(3) curves with Table-S1 parameters for 1 Gy and 2 Gy
     (225 kVp) and overlay digitized Fig 1A data.
  2. Plot the eq.(4) split-dose curves with the corresponding Table-S1
     parameters for each gap (20 min, 1 h, 2 h, 5 h, 12 h) and overlay
     digitized Fig 5 data.
  3. Quantify agreement (RMSE on the foci scale; relative RMSE; peak
     height & peak time errors).

Outputs:
  results/single_dose_validation.csv
  results/split_dose_validation.csv
  results/summary.json
  figures/fig1A_replication.png
  figures/fig5_replication.png
"""

from __future__ import annotations

import json
import csv
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import model as M


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RES = ROOT / "results"
FIG = ROOT / "figures"
RES.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)


# ---------- Helpers --------------------------------------------------------

def peak_of(t, y):
    """Return (peak_y, peak_t) from arrays."""
    i = int(np.argmax(y))
    return float(y[i]), float(t[i])


def rmse(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float(np.sqrt(np.mean((a - b) ** 2)))


# ---------- 1. Single acute dose ------------------------------------------

def validate_single_dose():
    df = pd.read_csv(DATA / "digitized_fig1A.csv", comment="#")

    t_grid = np.linspace(0.01, 25.0, 1000)
    fig, ax = plt.subplots(figsize=(7, 5))

    rows = []
    for label, p in M.SINGLE_ACUTE.items():
        # Pretty label
        dose_label = "1 Gy" if "1Gy" in label else "2 Gy"
        curve = M.acute(t_grid, *p.as_tuple())
        py, pt = peak_of(t_grid, curve)

        # Plot model
        ax.plot(t_grid, curve, label=f"Model {dose_label} (Table S1)")

        # Plot digitized data
        sub = df[df.curve == dose_label.replace(" ", "")]
        if not sub.empty:
            ax.scatter(sub.t_hr, sub.foci_per_cell,
                       s=42, label=f"Digitized {dose_label} (Fig 1A)")

            # Eval model at the data times and compute RMSE
            model_at_data = M.acute(sub.t_hr.values, *p.as_tuple())
            r = rmse(sub.foci_per_cell.values, model_at_data)
            rel = r / np.mean(sub.foci_per_cell.values)
            rows.append(dict(
                curve=dose_label,
                params=p.as_tuple(),
                model_peak=py,
                model_peak_t_hr=pt,
                rmse_foci=r,
                rel_rmse=rel,
                n_points=len(sub),
            ))
        else:
            rows.append(dict(
                curve=dose_label,
                params=p.as_tuple(),
                model_peak=py,
                model_peak_t_hr=pt,
                rmse_foci=None,
                rel_rmse=None,
                n_points=0,
            ))

    ax.set_xlabel("Time after irradiation (h)")
    ax.set_ylabel("γ-H2AX foci per cell")
    ax.set_title("Replication of Fig 1A (Mariotti 2013) — 225 kVp X-rays")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(alpha=0.3)
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 55)
    fig.tight_layout()
    fig.savefig(FIG / "fig1A_replication.png", dpi=150)
    plt.close(fig)

    # Write CSV summary
    with open(RES / "single_dose_validation.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)

    return rows


# ---------- 2. Split-dose --------------------------------------------------

def gap_label(gap_hr: float) -> str:
    if abs(gap_hr - 20/60.0) < 1e-3: return "20min"
    return {1.0: "1hr", 2.0: "2hr", 5.0: "5hr", 12.0: "12hr"}[gap_hr]


def validate_split_dose():
    df = pd.read_csv(DATA / "digitized_fig5.csv", comment="#")
    p_first = M.FIRST_FIXED  # 1 Gy 225 kVp parameters

    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    axes = axes.ravel()

    rows = []
    for ax, (gap_hr, p_second) in zip(axes, M.SECOND_EXPOSURE.items()):
        label = gap_label(gap_hr)
        t_grid = np.linspace(0.01, 28.0, 1500)

        # Full split-dose model
        total = M.split_dose(t_grid, p_first.as_tuple(),
                             p_second.as_tuple(), gap_hr)
        # Individual components (for the dashed overlay style of paper Fig 5)
        first_curve = M.acute(t_grid, *p_first.as_tuple())
        second_curve = np.where(t_grid >= gap_hr,
                                M.acute(t_grid - gap_hr, *p_second.as_tuple()),
                                0.0)

        ax.plot(t_grid, total, "-", lw=2, label="Model: total")
        ax.plot(t_grid, first_curve, "--", color="grey", alpha=0.7,
                label="Model: 1st only")
        ax.plot(t_grid, second_curve, ":", color="grey", alpha=0.7,
                label="Model: 2nd only")

        # Digitized data
        sub = df[df.gap_label == label]
        if not sub.empty:
            ax.scatter(sub.t_hr, sub.foci_per_cell, s=35,
                       color="C3", label="Digitized data")
            model_at_data = M.split_dose(sub.t_hr.values,
                                         p_first.as_tuple(),
                                         p_second.as_tuple(),
                                         gap_hr)
            r = rmse(sub.foci_per_cell.values, model_at_data)
            mean_y = float(np.mean(sub.foci_per_cell.values))
            rel = r / mean_y if mean_y > 0 else None
        else:
            r, rel = None, None

        py, pt = peak_of(t_grid, total)
        rows.append(dict(
            gap_hr=gap_hr,
            gap_label=label,
            second_params=p_second.as_tuple(),
            model_peak=py,
            model_peak_t_hr=pt,
            rmse_foci=r,
            rel_rmse=rel,
            n_points=int(len(sub)),
        ))

        ax.set_title(f"Gap = {label}  (Δt = {gap_hr:g} h)")
        ax.set_xlabel("Time after 1st irradiation (h)")
        ax.set_ylabel("γ-H2AX foci/cell")
        ax.set_ylim(0, 40)
        ax.grid(alpha=0.3)
        if ax is axes[0]:
            ax.legend(loc="upper right", fontsize=8)

    # Hide 6th unused axes
    axes[-1].axis("off")
    axes[-1].text(0.05, 0.5,
                  "Eq.(4) = 1st acute (fixed)\n + 2nd acute (free, Table S1)\n\n"
                  "1st-exposure params:\nA=24.63, B=8.011,\nC=0.91, D=0.23,\nE=3.32e-12",
                  fontsize=10, va="center")

    fig.suptitle("Replication of Fig 5 (Mariotti 2013) — 1+1 Gy 225 kVp split-dose",
                 fontsize=13)
    fig.tight_layout()
    fig.savefig(FIG / "fig5_replication.png", dpi=150)
    plt.close(fig)

    with open(RES / "split_dose_validation.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)

    return rows


# ---------- 3. Summary -----------------------------------------------------

def main():
    single = validate_single_dose()
    split = validate_split_dose()

    summary = {
        "paper": "Mariotti et al. 2013, PLOS ONE 8:e79541",
        "model_eqs": "(1) N=A(1-e^-Bt); (2) Ce^-Dt+(1-C)e^-Et; "
                     "(3) product; (4) sum of two acute terms with offset Δt",
        "time_unit": "hours",
        "single_dose": single,
        "split_dose": split,
        "reported_peaks_text": {
            "1Gy_225kVp_text": 21,
            "2Gy_225kVp_text": 37,
            "note": "Paper text says '~21 and 37 foci/cell for 1 Gy and 2 Gy "
                    "exposures' at the 30-min peak. The Table-S1 fits give the "
                    "model peak heights below."
        },
    }
    with open(RES / "summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=float)

    print(json.dumps(summary, indent=2, default=float))


if __name__ == "__main__":
    main()
