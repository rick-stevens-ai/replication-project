#!/usr/bin/env python3
"""Bar plots + QAOA landscape figures for the readout-noise mitigation replication."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

evd = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/QC-2101.02331-crosstalk-readout-noise/report/evidence")
res = json.loads((evd / "results.json").read_text())
qres = json.loads((evd / "qaoa_grid_results.json").read_text())
agg = res["aggregate"]

# --- Fig 1: error-reduction bar chart ---
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
labels = ["Raw noisy", "Tensor-product\nmitigation", "Correlated\nmitigation"]
tvds  = [agg["mean_tvd_raw"], agg["mean_tvd_tp"], agg["mean_tvd_corr"]]
enrs  = [agg["mean_err_energy_noisy"], agg["mean_err_energy_tp"], agg["mean_err_energy_corr"]]
colors = ["#d62728", "#ff9f43", "#2ca02c"]

axes[0].bar(labels, tvds, color=colors)
axes[0].set_ylabel("Mean TVD to ideal distribution")
axes[0].set_title("Distribution-level error (mean over 25 random p=2 QAOA circuits)")
for i, v in enumerate(tvds):
    axes[0].text(i, v + max(tvds)*0.02, f"{v:.4f}", ha="center", fontsize=9)

axes[1].bar(labels, enrs, color=colors)
axes[1].set_ylabel(r"Mean $|\langle H\rangle_{\rm est}-\langle H\rangle_{\rm ideal}|$")
axes[1].set_title(r"Observable-level error ($H=\sum_{(i,j)\in E} Z_iZ_j$, line-4 MaxCut)")
for i, v in enumerate(enrs):
    axes[1].text(i, v + max(enrs)*0.02, f"{v:.4f}", ha="center", fontsize=9)

fig.suptitle(
    "Independent replication of Maciejewski et al. 2021 (arXiv:2101.02331)\n"
    r"N=4 qubits, 5% cross-talk cluster on qubits {1,2}, Qiskit Aer",
    fontsize=11,
)
plt.tight_layout()
plt.savefig(evd / "fig1_error_bars.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# --- Fig 2: QAOA landscapes ---
grids = np.load(evd / "qaoa_grids.npz")
gammas = grids["gammas"]; betas = grids["betas"]
gi = grids["grid_ideal"]; gn = grids["grid_noisy"]
gt = grids["grid_mit_tp"]; gc = grids["grid_mit_corr"]

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
def plot_grid(ax, g, title):
    im = ax.imshow(g, origin="lower",
                   extent=[betas.min(), betas.max(), gammas.min(), gammas.max()],
                   aspect="auto", cmap="viridis", vmin=0, vmax=3)
    ax.set_xlabel(r"$\beta$"); ax.set_ylabel(r"$\gamma$")
    ax.set_title(title)
    plt.colorbar(im, ax=ax, label="MaxCut cost (max=3)")

plot_grid(axes[0,0], gi, "Ideal (noiseless)")
plot_grid(axes[0,1], gn, "Raw noisy")
plot_grid(axes[1,0], gt, "Tensor-product mitigation")
plot_grid(axes[1,1], gc, "Correlated mitigation")

fig.suptitle("QAOA p=1 landscapes on line-4 MaxCut (cost = sum(1-<ZZ>)/2)", fontsize=11)
plt.tight_layout()
plt.savefig(evd / "fig2_qaoa_landscapes.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print("Saved fig1_error_bars.png and fig2_qaoa_landscapes.png")
