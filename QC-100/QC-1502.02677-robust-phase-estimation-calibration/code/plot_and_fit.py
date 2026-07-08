"""Plot RPE precision-vs-N and fit power-law exponents.

Reads data/rpe_sweep.json produced by rpe_sim.py, fits log-log slopes
for both the RPE curve and the shot-noise baseline, and writes
figures/precision_vs_N.png plus a summary JSON with the fitted slopes.

Predictions:
    Heisenberg limit:  sigma ~ N^-1   (slope = -1.0 in log-log)
    Shot noise      :  sigma ~ N^-0.5 (slope = -0.5)
"""
from __future__ import annotations
import json
import math
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "rpe_sweep.json"
FIGDIR = ROOT / "figures"
FIGDIR.mkdir(exist_ok=True)


def loglog_fit(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """Return slope, intercept, r^2 of log10(y) = slope*log10(x) + intercept."""
    lx = np.log10(x)
    ly = np.log10(y)
    slope, intercept = np.polyfit(lx, ly, 1)
    y_pred = slope * lx + intercept
    ss_res = float(np.sum((ly - y_pred) ** 2))
    ss_tot = float(np.sum((ly - np.mean(ly)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return float(slope), float(intercept), r2


def main() -> None:
    payload = json.loads(DATA.read_text())
    rpe = payload["rpe"]
    sn = payload["shot_noise_baseline"]

    N_rpe = np.array([r["mean_total_queries_N"] for r in rpe], dtype=float)
    err_rpe = np.array([r["rmse_error"] for r in rpe], dtype=float)
    N_sn = np.array([s["actual_queries"] for s in sn], dtype=float)
    err_sn = np.array([s["rmse_error"] for s in sn], dtype=float)

    # Fit power laws.  Skip the first couple of small-N points where the
    # RPE ladder hasn't kicked in yet.  Use K >= 4 (N >= ~900).
    fit_mask = N_rpe >= 900
    slope_rpe, intr_rpe, r2_rpe = loglog_fit(N_rpe[fit_mask], err_rpe[fit_mask])
    slope_sn, intr_sn, r2_sn = loglog_fit(N_sn, err_sn)

    # Prediction lines.
    N_grid = np.geomspace(N_rpe.min(), N_rpe.max(), 200)
    hl_line = err_rpe[fit_mask][0] * (N_rpe[fit_mask][0] / N_grid)          # slope -1
    sn_line = err_sn[0] * np.sqrt(N_sn[0] / N_grid)                         # slope -1/2

    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    ax.loglog(N_rpe, err_rpe, "o-", color="tab:blue",
              label=f"RPE (Kimmel-Low-Yoder)  fitted slope = {slope_rpe:.2f}")
    ax.loglog(N_sn, err_sn, "s-", color="tab:orange",
              label=f"Shot-noise (k=1 only)      fitted slope = {slope_sn:.2f}")
    ax.loglog(N_grid, hl_line, "--", color="tab:blue", alpha=0.5,
              label="Heisenberg 1/N  reference")
    ax.loglog(N_grid, sn_line, "--", color="tab:orange", alpha=0.5,
              label="Shot-noise 1/sqrt(N)  reference")
    ax.set_xlabel("Total gate applications  N")
    ax.set_ylabel("RMSE of estimate of A = pi/2 + eps   (radians)")
    eps = payload["epsilon_true"]
    ax.set_title(f"RPE precision vs N   (single qubit R_x(pi/2 + eps), eps = {eps})")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="lower left", fontsize=8)
    fig.tight_layout()
    figpath = FIGDIR / "precision_vs_N.png"
    fig.savefig(figpath, dpi=150)
    print(f"[ok] wrote {figpath}")

    summary = {
        "slope_rpe": slope_rpe,
        "slope_rpe_r2": r2_rpe,
        "slope_rpe_fit_range_N": [float(N_rpe[fit_mask].min()), float(N_rpe[fit_mask].max())],
        "slope_sn": slope_sn,
        "slope_sn_r2": r2_sn,
        "heisenberg_prediction_slope": -1.0,
        "shot_noise_prediction_slope": -0.5,
        "rpe_slope_matches_heisenberg": abs(slope_rpe + 1.0) < 0.10,
        "sn_slope_matches_shot_noise": abs(slope_sn + 0.5) < 0.10,
        "figure": str(figpath.relative_to(ROOT)),
    }
    out = ROOT / "data" / "scaling_fit.json"
    out.write_text(json.dumps(summary, indent=2))
    print(f"[ok] wrote {out}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
