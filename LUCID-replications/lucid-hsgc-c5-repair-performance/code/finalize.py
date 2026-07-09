"""
Final replication run: evaluates BOTH parameter sets (paper Table 1 and our refit)
and produces side-by-side comparison figures + a combined metrics JSON.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from tlk_model import (
    TABLE1, sf_at_dose, far_curve, sigmas_for,
    SIGMA1_0MM, SIGMA1_32MM, SIGMA2_0MM, SIGMA2_32MM,
)
from replicate import (
    load_sf, load_far, predict_sf, predict_far,
    compute_metrics,
)

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


def main():
    sf_df = load_sf()
    far_df = load_far()

    # Load refit if present
    refit_path = RESULTS / "refit.json"
    if refit_path.exists():
        fitted = json.loads(refit_path.read_text())["fitted_params"]
    else:
        fitted = None

    summary = {
        "datasets": {
            "SF_n_HSG": int(len(sf_df)),
            "FAR_n_HSG": int(len(far_df)),
        },
        "sigmas_used": {
            "PMMA_0mm": {"Sigma1": SIGMA1_0MM, "Sigma2": SIGMA2_0MM},
            "PMMA_32mm": {"Sigma1": SIGMA1_32MM, "Sigma2": SIGMA2_32MM},
        },
        "paper_Table1": TABLE1,
        "refit_params": fitted,
    }

    sf_pred_table1 = predict_sf(sf_df, TABLE1)
    far_pred_table1 = predict_far(far_df, TABLE1)
    sf_pred_table1.to_csv(RESULTS / "sf_pred_Table1.csv", index=False)
    far_pred_table1.to_csv(RESULTS / "far_pred_Table1.csv", index=False)
    summary["metrics_Table1"] = compute_metrics(sf_pred_table1, far_pred_table1)

    if fitted is not None:
        sf_pred_fit = predict_sf(sf_df, fitted)
        far_pred_fit = predict_far(far_df, fitted)
        sf_pred_fit.to_csv(RESULTS / "sf_pred_refit.csv", index=False)
        far_pred_fit.to_csv(RESULTS / "far_pred_refit.csv", index=False)
        summary["metrics_refit"] = compute_metrics(sf_pred_fit, far_pred_fit)

    (RESULTS / "metrics_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

    # Combined SF figure
    fig, ax = plt.subplots(figsize=(7, 5.5))
    colors = {0: "tab:blue", 32: "tab:red"}
    dense_d = np.linspace(0, 8, 81)
    for pmma in sorted(sf_df["PMMA"].unique()):
        s1, s2 = sigmas_for(int(pmma))
        sub = sf_df[sf_df["PMMA"] == pmma]
        ax.errorbar(sub["Dose"], sub["SF"], yerr=sub["StdDev"],
                    fmt="o", color=colors[pmma], capsize=3, ms=6,
                    label=f"Exp. PMMA {pmma} mm")
        sf_t1 = [sf_at_dose(float(d), TABLE1, s1, s2) for d in dense_d]
        ax.plot(dense_d, sf_t1, "--", color=colors[pmma], lw=1.5,
                label=f"Paper Table1 PMMA {pmma} mm")
        if fitted is not None:
            sf_rf = [sf_at_dose(float(d), fitted, s1, s2) for d in dense_d]
            ax.plot(dense_d, sf_rf, "-", color=colors[pmma], lw=2,
                    label=f"Refit PMMA {pmma} mm")
    ax.set_yscale("log")
    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Cell Surviving Fraction")
    ax.set_title("HSGc-C5 SF — Sakata et al. 2021 Figure 5 (left), replication")
    ax.set_ylim(1e-2, 1.5)
    ax.grid(True, alpha=0.3, which="both")
    ax.legend(fontsize=7, loc="lower left", ncol=2)
    fig.tight_layout()
    fig.savefig(FIGURES / "sf_curve.png", dpi=150)
    plt.close(fig)

    # Combined FAR figure
    fig, ax = plt.subplots(figsize=(7, 5.5))
    for (pmma, dose), sub in far_df.groupby(["PMMA", "Dose"]):
        s1, s2 = sigmas_for(int(pmma))
        dense_t = np.linspace(0.01, max(12.5, sub["time"].max()), 200)
        ax.plot(sub["time"], sub["FAR"], "o", color=colors[pmma], ms=6,
                label=f"Exp. PMMA {pmma} mm, {int(dose)} Gy")
        rel_t1 = far_curve(float(dose), TABLE1, s1, s2, dense_t)
        ax.plot(dense_t, rel_t1, "--", color=colors[pmma], lw=1.5,
                label=f"Paper Table1")
        if fitted is not None:
            rel_rf = far_curve(float(dose), fitted, s1, s2, dense_t)
            ax.plot(dense_t, rel_rf, "-", color=colors[pmma], lw=2,
                    label=f"Refit")
    ax.set_xlabel("Time after irradiation end (h)")
    ax.set_ylabel("Relative FAR")
    ax.set_title("HSGc-C5 FAR — Sakata et al. 2021 Figure 5 (right), replication")
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, loc="upper right", ncol=1)
    fig.tight_layout()
    fig.savefig(FIGURES / "far_curve.png", dpi=150)
    plt.close(fig)

    # Parameter comparison bar chart
    if fitted is not None:
        fig, ax = plt.subplots(figsize=(7, 4))
        names = ["lam1", "lam2", "eta", "beta2", "gamma"]
        paper_vals = np.array([TABLE1[n] for n in names])
        fit_vals = np.array([fitted[n] for n in names])
        idx = np.arange(len(names))
        w = 0.38
        ax.bar(idx - w/2, paper_vals, w, label="Paper Table 1", color="tab:blue")
        ax.bar(idx + w/2, fit_vals, w, label="Our refit", color="tab:orange")
        ax.set_yscale("log")
        ax.set_xticks(idx)
        ax.set_xticklabels(names)
        ax.set_ylabel("Parameter value (log scale)")
        ax.set_title("TLK parameter comparison (paper Table 1 vs our refit)")
        ax.grid(True, alpha=0.3, which="both", axis="y")
        ax.legend()
        fig.tight_layout()
        fig.savefig(FIGURES / "params_compare.png", dpi=150)
        plt.close(fig)

    print("Wrote figures: sf_curve.png, far_curve.png, params_compare.png")


if __name__ == "__main__":
    main()
