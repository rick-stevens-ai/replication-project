"""
Reproduce qualitative versions of Qi et al. 2021 Figures 3 and 7:
  - Repair kinetics comparison: Model A vs Model B vs experimental foci
  - Artemis-deficient vs wild-type
  - XLF-deficient vs wild-type
"""
from __future__ import annotations

import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from nhej_model import simulate
from experimental_data import (
    FIG3A_4GY_PHOTON_WT, FIG3B_2GY_PHOTON_WT, FIG4A_4GY_PROTON_WT,
    FIG7A_2GY_ARTEMIS_DEF, FIG7C_2GY_XLF_DEF,
)

OUT = os.path.expanduser(
    "~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-slow-fast-nhej/figures"
)
os.makedirs(OUT, exist_ok=True)


def chi2_per_point(model_t, model_y, exp_pts):
    """Reduced chi-square style metric vs experimental points (unit weight)."""
    chi2 = 0.0
    n = 0
    for (t_exp, y_exp) in exp_pts:
        idx = np.argmin(np.abs(model_t - t_exp))
        y_mod = model_y[idx]
        chi2 += (y_mod - y_exp) ** 2
        n += 1
    return chi2 / n if n else float("nan")


def plot_kinetics(ax, dose_gy, exp_data, title, *, kw_a=None, kw_b=None):
    t = np.linspace(1e-3, 24.0, 400)
    rA = simulate("A", t, dose_gy=dose_gy, **(kw_a or {}))
    rB = simulate("B", t, dose_gy=dose_gy, **(kw_b or {}))

    # Normalise to fraction (peak = 1)
    ax.plot(t, rA["unrepaired_frac"], "b-", label="Model A (Parallel)")
    ax.plot(t, rB["unrepaired_frac"], "r-", label="Model B (Entwined)")
    if exp_data:
        ex_t = [p[0] for p in exp_data]
        ex_y = [p[1] for p in exp_data]
        ax.plot(ex_t, ex_y, "ko", markersize=6, label="Experiment (digitised)")
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Unrepaired DSB fraction")
    ax.set_xlim(0, 24)
    ax.set_ylim(-0.02, 1.02)
    ax.set_title(title)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="upper right")

    chi_a = chi2_per_point(t, rA["unrepaired_frac"], exp_data) if exp_data else None
    chi_b = chi2_per_point(t, rB["unrepaired_frac"], exp_data) if exp_data else None
    return chi_a, chi_b


def figure_repair_kinetics_wt():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    out = {}
    chi_a, chi_b = plot_kinetics(axes[0], 4.0, FIG3A_4GY_PHOTON_WT,
                                 "4 Gy photon (WT) [Fig 3a]")
    out["fig3a"] = {"chi2_A": chi_a, "chi2_B": chi_b}
    chi_a, chi_b = plot_kinetics(axes[1], 2.0, FIG3B_2GY_PHOTON_WT,
                                 "2 Gy photon (WT) [Fig 3b]")
    out["fig3b"] = {"chi2_A": chi_a, "chi2_B": chi_b}
    chi_a, chi_b = plot_kinetics(axes[2], 4.0, FIG4A_4GY_PROTON_WT,
                                 "4 Gy proton (WT) [Fig 4a]")
    out["fig4a"] = {"chi2_A": chi_a, "chi2_B": chi_b}
    plt.tight_layout()
    out_path = os.path.join(OUT, "fig_repair_kinetics_wt.png")
    plt.savefig(out_path, dpi=130)
    plt.close()
    return out_path, out


def figure_deficient():
    """Artemis- and XLF-deficient cell repair kinetics — Model B only."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    out = {}
    t = np.linspace(1e-3, 24.0, 400)

    # Artemis-deficient
    ax = axes[0]
    rB_wt = simulate("B", t, dose_gy=2.0)
    rB_ad = simulate("B", t, dose_gy=2.0, artemis_deficient=True)
    ax.plot(t, rB_wt["unrepaired_frac"], "k-", label="Model B WT")
    ax.plot(t, rB_ad["unrepaired_frac"], "r-", label="Model B Artemis-deficient")
    ex_t = [p[0] for p in FIG7A_2GY_ARTEMIS_DEF]
    ex_y = [p[1] for p in FIG7A_2GY_ARTEMIS_DEF]
    ax.plot(ex_t, ex_y, "ks", markersize=6, label="Exp. CJ179 (Artemis-def, 2 Gy)")
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Unrepaired DSB fraction")
    ax.set_xlim(0, 24); ax.set_ylim(-0.02, 1.02)
    ax.set_title("Artemis deficiency [Fig 7a]")
    ax.grid(alpha=0.3); ax.legend(fontsize=8)
    out["fig7a"] = {
        "chi2_B_def_vs_exp": chi2_per_point(t, rB_ad["unrepaired_frac"], FIG7A_2GY_ARTEMIS_DEF),
    }

    # XLF-deficient
    ax = axes[1]
    rB_xlf = simulate("B", t, dose_gy=2.0, xlf_deficient=True)
    ax.plot(t, rB_wt["unrepaired_frac"], "k-", label="Model B WT")
    ax.plot(t, rB_xlf["unrepaired_frac"], "g-", label="Model B XLF-deficient")
    ex_t = [p[0] for p in FIG7C_2GY_XLF_DEF]
    ex_y = [p[1] for p in FIG7C_2GY_XLF_DEF]
    ax.plot(ex_t, ex_y, "ks", markersize=6, label="Exp. 2BN (XLF-def, 2 Gy)")
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Unrepaired DSB fraction")
    ax.set_xlim(0, 24); ax.set_ylim(-0.02, 1.02)
    ax.set_title("XLF deficiency [Fig 7c]")
    ax.grid(alpha=0.3); ax.legend(fontsize=8)
    out["fig7c"] = {
        "chi2_B_xlf_vs_exp": chi2_per_point(t, rB_xlf["unrepaired_frac"], FIG7C_2GY_XLF_DEF),
    }

    plt.tight_layout()
    out_path = os.path.join(OUT, "fig_deficient_cells.png")
    plt.savefig(out_path, dpi=130)
    plt.close()
    return out_path, out


def figure_state_decomp():
    """Show internal state decomposition for Model B at 2 Gy."""
    t = np.linspace(1e-3, 24.0, 400)
    r = simulate("B", t, dose_gy=2.0)
    fig, ax = plt.subplots(figsize=(8, 5))
    states = ["dsb", "ku", "fast", "slow", "slow_proc", "syn", "rep", "mis"]
    colors = plt.cm.tab10(np.linspace(0, 1, len(states)))
    for s, c in zip(states, colors):
        ax.plot(t, r[s], color=c, label=s, linewidth=1.5)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Population fraction")
    ax.set_xlim(0, 24); ax.set_ylim(-0.02, 1.02)
    ax.set_title("Model B internal compartments (2 Gy photon, dose-normalised)")
    ax.grid(alpha=0.3); ax.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    out_path = os.path.join(OUT, "fig_state_decomposition.png")
    plt.savefig(out_path, dpi=130)
    plt.close()
    return out_path


if __name__ == "__main__":
    p1, m1 = figure_repair_kinetics_wt()
    print("Wrote:", p1)
    p2, m2 = figure_deficient()
    print("Wrote:", p2)
    p3 = figure_state_decomp()
    print("Wrote:", p3)

    metrics = {**m1, **m2}
    metrics_path = os.path.join(OUT, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print("Wrote:", metrics_path)
    print(json.dumps(metrics, indent=2))
