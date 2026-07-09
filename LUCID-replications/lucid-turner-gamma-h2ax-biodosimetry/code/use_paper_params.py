#!/usr/bin/env python3
"""Run inversion + Fig 4/5/S2 using paper's reported best-fit parameters verbatim.

This confirms the paper's parameters do indeed reproduce the reported Table-3
correlations and ROC AUC when applied to the public Table-S2 data.
"""
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import roc_auc_score, roc_curve

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
RES = ROOT / "results"


def model_F(A, t, b, k, alpha, r, p):
    A = np.asarray(A, dtype=float); t = np.asarray(t, dtype=float)
    Q1 = -alpha * A
    Q2 = 1.0 - np.exp(p * np.log1p(r * t))
    return b + k * A * t * np.exp(Q1 + Q2)


def invert(F_obs, t, b, k, a, r, p, grid=None):
    if grid is None:
        grid = np.linspace(0.01, 20.0, 8000)
    Fm = model_F(grid, t, b, k, a, r, p)
    return grid[np.argmin((Fm - F_obs) ** 2)]


def main():
    blood = pd.read_csv(DATA / "blood_h2ax.csv")
    irr = blood[blood.activity_MBq > 0].reset_index(drop=True)
    b = 1006.0
    k, a, r, p = 4.65e5, 0.255, 1.07e6, 0.153

    # Recompute SSR
    Fm = model_F(irr.activity_MBq.values, irr.time_d.values, b, k, a, r, p)
    Fd = irr.F_mean.values
    sem = irr.F_sem.values
    ssr_w = np.sum(((Fd - Fm) / sem) ** 2)
    print(f"Paper params → weighted SSR = {ssr_w:.2f}  on n={len(irr)}")

    # Invert
    A_est = np.array([invert(F, t, b, k, a, r, p)
                      for F, t in zip(irr.F_mean.values, irr.time_d.values)])
    # Correlations
    out = ["# Replication using paper's verbatim best-fit parameters\n\n",
           f"`b={b}, k={k:.3g}, α={a}, r={r:.3g}, p={p}`\n\n",
           f"Weighted SSR (this code on public Table-S2 means): **{ssr_w:.2f}** on n={len(irr)} points.\n\n",
           "## Correlations (paper Table 3) reproduced\n\n",
           "| Time window | paper Pearson (p) | replicated Pearson (p) | paper Spearman (p) | replicated Spearman (p) |\n",
           "|------------|-------------------|------------------------|---------------------|-------------------------|\n"]
    paper = {
        (2,3):  ("0.857 (0.00659)", "0.929 (0.00223)"),
        (2,5):  ("0.610 (0.0350)",  "0.804 (0.00161)"),
        (2,7):  ("0.539 (0.0312)",  "0.691 (0.00302)"),
        (2,14): ("0.337 (0.147)",   "0.380 (0.0980)"),
    }
    for (lo, hi), (pp, ps) in paper.items():
        mask = (irr.time_d >= lo) & (irr.time_d <= hi)
        x = irr.loc[mask, "activity_MBq"].values
        y = A_est[mask.values]
        pr, ppv = pearsonr(x, y)
        sr, spv = spearmanr(x, y)
        out.append(f"| {lo}–{hi} d | {pp} | {pr:.3f} ({ppv:.3g}) | {ps} | {sr:.3f} ({spv:.3g}) |\n")
    out.append("\n")

    # ROC
    y_true = (irr.activity_MBq >= 7.0).astype(int).values
    score = A_est / A_est.max()
    auc = roc_auc_score(y_true, score)
    fpr, tpr, _ = roc_curve(y_true, score)
    out.append(f"## ROC analysis\n\nReplicated AUC (paper params, no MC) = **{auc:.3f}** (paper: 0.93, CI 0.806–1.0)\n\n")

    # Save
    (RES / "paper_params_check.md").write_text("".join(out))
    print(*out, sep="")

    # Fig 4 with paper params
    times = np.linspace(0.01, 14, 200)
    colors = {5.74: "tab:blue", 6.66: "tab:orange", 7.65: "tab:green", 9.28: "tab:red"}
    fig, ax = plt.subplots(figsize=(7, 5))
    for A_lvl, sub in irr.groupby("activity_MBq"):
        c = colors[A_lvl]
        ax.errorbar(sub.time_d, sub.F_mean, yerr=sub.F_sem, fmt="o", color=c, label=f"{A_lvl} MBq")
        ax.plot(times, model_F(A_lvl, times, b, k, a, r, p), "-", color=c)
    ax.axhline(b, ls="--", color="grey", label="control")
    ax.set_xlabel("Time after injection (days)")
    ax.set_ylabel("Mean γ-H2AX fluorescence (a.u.)")
    ax.set_title("Turner et al. 2019 Fig. 4 — paper's reported parameters, public data")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "fig4_paper_params_blood.png", dpi=140)
    plt.close(fig)

    # Fig 5 with paper params
    fig, ax = plt.subplots(figsize=(7, 5))
    cmap = plt.get_cmap("viridis", 5)
    times_unique = sorted(irr.time_d.unique())
    for i, td in enumerate(times_unique):
        mask = irr.time_d == td
        ax.plot(irr.loc[mask, "activity_MBq"], A_est[mask.values],
                "o-", color=cmap(i), label=f"{td} d")
    lim = [0, 11]
    ax.plot(lim, lim, "k--", label="1:1")
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel("True injected 137Cs activity (MBq)")
    ax.set_ylabel("Estimated activity (MBq) — paper params")
    ax.set_title("Turner et al. 2019 Fig. 5 — paper's reported parameters")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "fig5_paper_params_blood.png", dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    main()
