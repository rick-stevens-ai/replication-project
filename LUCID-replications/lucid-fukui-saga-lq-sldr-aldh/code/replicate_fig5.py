"""
Forward-replicate Figure 5 of Fukui et al. 2022.

For each cell line: take Table 1 mean parameters, evaluate the IMK two-
population model at the doses of the digitized data points, compare to
those digitized survival fractions, and compute R^2 in -ln S space.

Then plot model curve vs. digitized points and save figures.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from imk_model import (
    S_total_single_dose,
    r_squared_log,
    DOSE_RATE_ACUTE_GY_PER_H,
)
from params_table1 import mean_params, TABLE1
from digitized_fig5 import FIG5_DATA, FIG5_REPORTED_R2


HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.normpath(os.path.join(HERE, "..", "results"))
FIGS = os.path.normpath(os.path.join(HERE, "..", "figures"))
os.makedirs(RESULTS, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)


def predict_curve(cell, doses):
    p = mean_params(cell)
    return S_total_single_dose(doses, **p)


def evaluate_cell(cell):
    """Returns (doses, observed, predicted) for non-zero doses (R^2 in log space
    skips D=0 because log(1)=0 inflates SS_tot in a way that hides residuals)."""
    pts = [(d, s) for (d, s) in FIG5_DATA[cell] if d > 0]
    doses = np.array([d for d, _ in pts])
    obs   = np.array([s for _, s in pts])
    pred  = predict_curve(cell, doses)
    return doses, obs, pred


def main():
    summary_lines = []
    summary_lines.append(
        "# Forward replication of Fig 5 (Fukui et al. 2022) — IMK model "
        "with Table 1 mean parameters\n"
    )
    summary_lines.append(
        "Predicted survival vs. digitized experimental points. "
        "R^2 is computed in -ln S space, matching the paper.\n"
    )
    summary_lines.append(
        "| cell   | n_pts | R^2 (this work) | R^2 (paper, family) | "
        "RMS log10(S) residual |\n"
        "|--------|-------|-----------------|---------------------|"
        "----------------------|"
    )

    per_cell = {}
    for cell in ["SAS", "SAS-R", "HSC2", "HSC2-R"]:
        doses, obs, pred = evaluate_cell(cell)
        r2 = r_squared_log(obs, pred)
        rms_log10 = float(np.sqrt(np.mean((np.log10(obs) - np.log10(pred)) ** 2)))
        per_cell[cell] = dict(doses=doses, obs=obs, pred=pred,
                              r2=r2, rms_log10=rms_log10)
        family = "A_SAS_family" if cell.startswith("SAS") else "B_HSC2_family"
        summary_lines.append(
            f"| {cell:6s} | {len(doses):5d} | {r2: .3f}           | "
            f"{FIG5_REPORTED_R2[family]:.3f}               | {rms_log10:.3f} |"
        )

    # ------------------------------------------------------------------
    # Plot panel A and B
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    colors = {
        "SAS": "tab:blue", "SAS-R": "tab:red",
        "HSC2": "tab:blue", "HSC2-R": "tab:red",
    }
    panel_for = {"SAS": 0, "SAS-R": 0, "HSC2": 1, "HSC2-R": 1}

    dense = np.linspace(0.01, 15.0, 200)
    for cell in ["SAS", "SAS-R", "HSC2", "HSC2-R"]:
        ax = axes[panel_for[cell]]
        pc = per_cell[cell]
        ax.semilogy(pc["doses"], pc["obs"], "o", color=colors[cell],
                    label=f"{cell} digitized", markerfacecolor="none",
                    markersize=8)
        curve = predict_curve(cell, dense)
        ax.semilogy(dense, curve, "-", color=colors[cell],
                    label=f"{cell} IMK pred (Table 1)", lw=1.4)

    for ax, panel, title in zip(axes, ["A", "B"], ["SAS family", "HSC2 family"]):
        ax.set_xlabel("Dose (Gy)")
        ax.set_ylabel("Surviving fraction")
        ax.set_xlim(0, 16)
        ax.set_ylim(1e-5, 2)
        ax.set_title(f"({panel}) {title}")
        ax.legend(fontsize=8, loc="lower left")
        ax.grid(True, which="both", alpha=0.3)

    fig.suptitle(
        "Replication of Fig 5: IMK model (Table 1 means) vs. digitized data",
        y=1.02,
    )
    fig.tight_layout()
    out = os.path.join(FIGS, "fig5_replication.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    summary_lines.append(f"\nFigure saved → `figures/fig5_replication.png`\n")

    # ------------------------------------------------------------------
    # Per-point residual table
    # ------------------------------------------------------------------
    summary_lines.append("\n## Per-point residuals\n")
    summary_lines.append(
        "| cell | dose (Gy) | S_obs (digitized) | S_pred (IMK, Table 1) | "
        "log10(S_pred / S_obs) |\n"
        "|------|-----------|-------------------|-----------------------|"
        "-----------------------|"
    )
    for cell in ["SAS", "SAS-R", "HSC2", "HSC2-R"]:
        pc = per_cell[cell]
        for d, o, p in zip(pc["doses"], pc["obs"], pc["pred"]):
            ratio = float(np.log10(p / o))
            summary_lines.append(
                f"| {cell:6s} | {d:9.1f} | {o:17.5g} | {p:21.5g} | {ratio:+.3f} |"
            )

    # ------------------------------------------------------------------
    # Save summary
    # ------------------------------------------------------------------
    out_md = os.path.join(RESULTS, "fig5_replication_summary.md")
    with open(out_md, "w") as f:
        f.write("\n".join(summary_lines))
    print(f"Wrote {out_md}")
    print("\n".join(summary_lines))


if __name__ == "__main__":
    main()
