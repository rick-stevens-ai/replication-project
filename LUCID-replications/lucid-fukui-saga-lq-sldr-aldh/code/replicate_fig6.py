"""
Forward replication of Figure 6 (split-dose recovery) using Table 1 means.

The paper splits 4 Gy into 2 x 2 Gy with inter-fraction time tau, then plots
relative radiosensitivity = S(tau) / S(tau=0) (so 1.0 = no recovery).
Actually the caption says "normalized by the cell survival at 4 Gy
irradiation (i.e., non-interval irradiation)", i.e. the relative survival.
"Higher = more survival = more recovery." So we plot S_split(tau) / S_acute(4Gy).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from imk_model import S_total_split_dose, S_total_single_dose
from params_table1 import mean_params

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.normpath(os.path.join(HERE, "..", "results"))
FIGS = os.path.normpath(os.path.join(HERE, "..", "figures"))
os.makedirs(RESULTS, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)

# Digitized Fig 6: relative radiosensitivity = S(tau, 2+2 Gy) / S(acute 4 Gy)
# (so 1.0 = no recovery; values > 1 mean recovery vs. an acute 4-Gy reference)
# Note: paper normalizes by single 4-Gy dose, so the relative-radiosensitivity is
# expected to be >= 1.0 for tau > 0.
FIG6_DATA = {
    "SAS":    [(0.25, 0.93), (0.5, 0.88), (1.0, 0.83), (3.0, 0.68),
               (6.0, 0.67), (24.0, 0.55)],
    "SAS-R":  [(0.25, 0.92), (0.5, 0.73), (1.0, 0.72), (3.0, 0.58),
               (6.0, 0.56), (24.0, 0.51)],
    "HSC2":   [(0.25, 0.60), (0.5, 0.58), (1.0, 0.44), (3.0, 0.40),
               (6.0, 0.38), (24.0, 0.34)],
    "HSC2-R": [(0.25, 0.85), (0.5, 0.75), (1.0, 0.77), (3.0, 0.69),
               (6.0, 0.66), (24.0, 0.53)],
}
# NB: the vision read may have inverted the normalization sense (values < 1
# suggest "relative survival vs. 4 Gy single dose" with single dose = 1, and
# the curves DROP with tau because cells re-enter cell cycle and lose recovery,
# i.e. the SF goes down toward S_acute(4). The paper's wording "normalized by
# cell survival at 4 Gy" makes this 1.0 at tau=0 if no instantaneous recovery
# benefit, and >1 if split-dose preserves more survival. The digitized values
# < 1 are inconsistent with that, so we ALSO compute predicted relative-SF
# = S_split / S_acute_4Gy and compare absolute values rather than verdict.

def predict_split_dose_curve(cell, taus):
    p = mean_params(cell)
    S_acute_4 = float(S_total_single_dose([4.0], **p)[0])
    out = np.empty_like(taus)
    for i, tau in enumerate(taus):
        Spred = S_total_split_dose(D1=2.0, D2=2.0, tau_h=tau, **p)
        out[i] = Spred / S_acute_4
    return out


def main():
    taus_dense = np.logspace(-2, 1.6, 200)  # 0.01 h to ~40 h
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=True)
    cells = ["SAS", "SAS-R", "HSC2", "HSC2-R"]
    titles = ["(AI) SAS", "(AII) SAS-R", "(BI) HSC2", "(BII) HSC2-R"]
    colors = ["tab:blue", "tab:red", "tab:blue", "tab:red"]

    summary = ["# Figure 6 (split-dose 2+2 Gy) replication summary\n",
               "Predicted relative survival S(2+2,τ) / S(acute 4 Gy) using "
               "Table 1 mean parameters.\n",
               "| cell | τ (h) | rel-SF (digitized) | rel-SF (IMK pred) |",
               "|------|-------|--------------------|-------------------|"]
    for ax, cell, color, title in zip(axes.flatten(), cells, colors, titles):
        curve = predict_split_dose_curve(cell, taus_dense)
        pts = FIG6_DATA[cell]
        ax.semilogx(taus_dense, curve, "-", color=color, lw=1.5,
                    label="IMK (Table 1)")
        ax.semilogx([t for t, _ in pts], [s for _, s in pts],
                    "o", color=color, markerfacecolor="none", markersize=8,
                    label="digitized")
        ax.set_title(title)
        ax.set_ylabel("S(2+2 Gy, τ) / S(4 Gy)")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend(fontsize=8)
        ax.set_ylim(0, 2.5)
        ax.set_xlim(0.05, 40)

        for t, s_obs in pts:
            s_pred = float(predict_split_dose_curve(cell, np.array([t]))[0])
            summary.append(f"| {cell} | {t:.2f} | {s_obs:.3f} | {s_pred:.3f} |")

    axes[1, 0].set_xlabel("Inter-fraction time τ (h)")
    axes[1, 1].set_xlabel("Inter-fraction time τ (h)")
    fig.suptitle("Replication of Fig 6 (split-dose recovery), Table 1 means")
    fig.tight_layout()
    out = os.path.join(FIGS, "fig6_replication.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    summary.append(f"\nFigure → `figures/fig6_replication.png`\n")

    out_md = os.path.join(RESULTS, "fig6_replication_summary.md")
    with open(out_md, "w") as f:
        f.write("\n".join(summary))
    print(f"Wrote {out_md}")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
