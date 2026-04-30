"""Merge metrics.json + chronos_metrics.json + tvae_metrics.json into a single
results_baselines.json and regenerate metric_bars.png across all baselines.
"""
from __future__ import annotations
import json, os, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "results"

base = json.load(open(OUT / "metrics.json"))
chronos = json.load(open(OUT / "chronos_metrics.json"))
tvae = json.load(open(OUT / "tvae_metrics.json"))

merged = {
    "constant": base["constant"],
    "chronos_t5_small": chronos,
    "tvae": tvae,
    "fno": base["fno"],
    "convlstm": base["convlstm"],
}
with open(OUT / "results_baselines.json", "w") as f:
    json.dump(merged, f, indent=2)
print("wrote", OUT / "results_baselines.json")

# Bar chart with all baselines
order = ["constant", "chronos_t5_small", "tvae", "fno", "convlstm"]
labels = ["Constant", "Chronos-T5\n(zero-shot)", "Temporal-VAE", "FNO-2D", "ConvLSTM"]
colors = ["gray", "C2", "C4", "C0", "C3"]

fig, ax = plt.subplots(1, 4, figsize=(15, 3.6))
metrics_list = [
    ("rho_pred_mean", "ρ_pred"),
    ("rho_resid_mean", "ρ_resid"),
    ("mse_total", "MSE (total)"),
    ("onset_roc_auc", "Onset ROC-AUC"),
]
for i, (mkey, title) in enumerate(metrics_list):
    vals = [merged[n][mkey] for n in order]
    ax[i].bar(labels, vals, color=colors)
    ax[i].set_title(title)
    ax[i].grid(alpha=.3, axis="y")
    ax[i].tick_params(axis="x", labelsize=8, rotation=15)
    for j, v in enumerate(vals):
        ax[i].text(j, v, f"{v:.3f}", ha="center", va="bottom", fontsize=8)
plt.tight_layout()
plt.savefig(OUT / "metric_bars.png", dpi=120)
print("wrote", OUT / "metric_bars.png")

# Print a markdown table
print("\n| Model | params | ρ_pred | ρ_resid | MSE | Onset AUC |")
print("|---|---|---|---|---|---|")
for n, lab in zip(order, labels):
    m = merged[n]
    p = m.get("params", 0)
    pstr = f"{p:,}" if p else "0"
    print(f"| {lab.replace(chr(10), ' ')} | {pstr} | "
          f"{m['rho_pred_mean']:.3f} | {m['rho_resid_mean']:.3f} | "
          f"{m['mse_total']:.4f} | {m['onset_roc_auc']:.3f} |")
