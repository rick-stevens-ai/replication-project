"""
Independent re-fit of the digitized Fig 1A (single-dose) and Fig 5
(split-dose) data using the same equations the paper uses (eq. 3 and 4).

Compares our refit parameters to Table S1 to gauge:
  * how well the published parameters reproduce the (digitized) data
  * how identifiable the parameters are from the data alone

Outputs:
  results/refit_single.csv
  results/refit_split.csv
  figures/refit_overlay.png
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
from scipy.optimize import least_squares

import model as M


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RES = ROOT / "results"
FIG = ROOT / "figures"


# ---------- 1. Refit single-dose acute -------------------------------------

def fit_acute(t, y, p0=None, bounds=None):
    if p0 is None:
        p0 = [max(y) * 1.2, 5.0, 0.5, 0.5, 0.05]
    if bounds is None:
        bounds = ([0, 0.01, 0.0, 1e-4, 1e-8],
                  [200, 30, 1.0, 10, 5])

    def resid(p):
        return M.acute(t, *p) - y

    res = least_squares(resid, p0, bounds=bounds, max_nfev=5000)
    return res.x, res.cost, res.success


def refit_single_dose():
    df = pd.read_csv(DATA / "digitized_fig1A.csv", comment="#")
    rows = []
    for label in ["1Gy", "2Gy"]:
        sub = df[df.curve == label].sort_values("t_hr")
        t, y = sub.t_hr.values, sub.foci_per_cell.values
        params, cost, ok = fit_acute(t, y)
        pub = (M.SINGLE_ACUTE[f"{label}_225kVp"].as_tuple())
        # RMSE for both
        rmse_fit = float(np.sqrt(np.mean((M.acute(t, *params) - y) ** 2)))
        rmse_pub = float(np.sqrt(np.mean((M.acute(t, *pub) - y) ** 2)))
        rows.append(dict(
            curve=label,
            refit_params=tuple(params.round(4)),
            pub_params=pub,
            rmse_refit=rmse_fit,
            rmse_pub=rmse_pub,
            success=bool(ok),
            n=len(sub),
        ))
    return rows


# ---------- 2. Refit split-dose --------------------------------------------

def refit_split_dose():
    """Refit second-exposure parameters while keeping first-exposure fixed."""
    df = pd.read_csv(DATA / "digitized_fig5.csv", comment="#")
    p_first = M.FIRST_FIXED.as_tuple()
    rows = []
    for gap_hr, p_second_pub in M.SECOND_EXPOSURE.items():
        # Label
        from validate import gap_label
        label = gap_label(gap_hr)
        sub = df[df.gap_label == label].sort_values("t_hr")
        t, y = sub.t_hr.values, sub.foci_per_cell.values

        def resid(p):
            return M.split_dose(t, p_first, tuple(p), gap_hr) - y

        # Generous bounds; A in [0, 200] etc.
        p0 = list(p_second_pub.as_tuple())
        bounds = ([0, 0.01, 0.0, 1e-4, 1e-8],
                  [200, 30, 1.0, 10, 5])
        try:
            res = least_squares(resid, p0, bounds=bounds, max_nfev=5000)
            refit = tuple(res.x.round(4))
            rmse_refit = float(np.sqrt(np.mean(res.fun ** 2)))
        except Exception as e:
            refit, rmse_refit = None, None

        pub = p_second_pub.as_tuple()
        rmse_pub = float(np.sqrt(np.mean(
            (M.split_dose(t, p_first, pub, gap_hr) - y) ** 2)))

        rows.append(dict(
            gap_hr=gap_hr,
            gap_label=label,
            refit_params=refit,
            pub_params=pub,
            rmse_refit=rmse_refit,
            rmse_pub=rmse_pub,
            n=len(sub),
        ))
    return rows


# ---------- 3. Overlay figure ----------------------------------------------

def overlay_figure(single_rows, split_rows):
    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    axes = axes.ravel()

    # Single-dose overlay
    df1 = pd.read_csv(DATA / "digitized_fig1A.csv", comment="#")
    ax = axes[0]
    t_grid = np.linspace(0.01, 25, 1000)
    for r, color in zip(single_rows, ["C0", "C1"]):
        label = r["curve"]
        sub = df1[df1.curve == label]
        ax.scatter(sub.t_hr, sub.foci_per_cell, s=30, color=color, label=f"data {label}")
        ax.plot(t_grid, M.acute(t_grid, *r["refit_params"]), "-", color=color,
                label=f"refit {label}")
        ax.plot(t_grid, M.acute(t_grid, *r["pub_params"]), "--", color=color, alpha=0.6,
                label=f"pub {label}")
    ax.set_title("Single dose (Fig 1A): refit vs published")
    ax.set_xlabel("Time (h)"); ax.set_ylabel("Foci/cell")
    ax.set_ylim(0, 55); ax.legend(fontsize=7); ax.grid(alpha=0.3)

    # Split-dose overlay (one panel per gap)
    df5 = pd.read_csv(DATA / "digitized_fig5.csv", comment="#")
    p_first = M.FIRST_FIXED.as_tuple()
    for ax, r in zip(axes[1:], split_rows):
        gap = r["gap_hr"]
        label = r["gap_label"]
        sub = df5[df5.gap_label == label]
        t_grid = np.linspace(0.01, 28, 1500)
        ax.scatter(sub.t_hr, sub.foci_per_cell, s=30, color="C3", label="data")
        if r["refit_params"] is not None:
            ax.plot(t_grid, M.split_dose(t_grid, p_first, r["refit_params"], gap),
                    "-", color="C0", label="refit")
        ax.plot(t_grid, M.split_dose(t_grid, p_first, r["pub_params"], gap),
                "--", color="C2", alpha=0.7, label="pub Table S1")
        ax.set_title(f"Gap = {label}")
        ax.set_xlabel("Time after 1st (h)"); ax.set_ylabel("Foci/cell")
        ax.set_ylim(0, 45); ax.legend(fontsize=7); ax.grid(alpha=0.3)

    fig.suptitle("Refit vs published parameters (Mariotti 2013 model)",
                 fontsize=13)
    fig.tight_layout()
    fig.savefig(FIG / "refit_overlay.png", dpi=150)
    plt.close(fig)


def main():
    single = refit_single_dose()
    split = refit_split_dose()
    overlay_figure(single, split)

    def write_csv(name, rows):
        with open(RES / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            for r in rows:
                w.writerow(r)

    write_csv("refit_single.csv", single)
    write_csv("refit_split.csv", split)

    print(json.dumps({"single": single, "split": split}, indent=2, default=float))


if __name__ == "__main__":
    main()
