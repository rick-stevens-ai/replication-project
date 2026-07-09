#!/usr/bin/env python3
"""Reconstruct Figs 3A (8-oxo-dG), 5A/B (γH2AX kinetics), 6A (TIFs) and Table 1 from published values."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

FIG = Path(__file__).resolve().parent.parent / "figures"
FIG.mkdir(exist_ok=True)

# --- Fig 5A/B-equivalent: γH2AX foci kinetics ---
times = np.array([0, 0.75, 24, 48])  # h
series = {
    "P8":   ([0.20, 17.0, 0.30, 0.30], [0.05, 2.0, 0.10, 0.10]),
    "P23":  ([3.50, 22.0, 10.0, 10.0], [1.30, 2.0, 1.0, 1.0]),
    "P19-C": ([3.50, np.nan, 4.50, 4.50], [0.50, 0, 0.70, 0.70]),
    "P19-ST":([3.50, np.nan, 4.50, 4.50], [0.50, 0, 0.70, 0.70]),
    "P19-IR":([3.50, np.nan, 4.50, 4.50], [0.50, 0, 0.70, 0.70]),
}
fig, ax = plt.subplots(figsize=(7,5))
for name, (m, se) in series.items():
    m = np.array(m, dtype=float); se = np.array(se, dtype=float)
    mask = ~np.isnan(m)
    ax.errorbar(times[mask], m[mask], yerr=se[mask], marker='o', label=name, capsize=3)
ax.set_xlabel("Time after 1 Gy (h)"); ax.set_ylabel("γH2AX foci / cell")
ax.set_title("Reconstructed γH2AX repair kinetics (Sangsuwan 2023 Fig 5A/B)")
ax.legend(); ax.set_xscale("symlog", linthresh=1)
fig.tight_layout(); fig.savefig(FIG/"fig5_gh2ax_kinetics.png", dpi=140); plt.close(fig)

# --- Fig 3A-equivalent: 8-oxo-dG linear regression slopes ---
weeks = np.arange(1,9)
slopes = {"P8 C":16, "P8 LDR":27, "P13 C":26, "P13 LDR":45}
intercepts = {"P8 C":16, "P8 LDR":16, "P13 C":18, "P13 LDR":18}
fig, ax = plt.subplots(figsize=(7,5))
for k, s in slopes.items():
    y = intercepts[k] + s*(weeks-1)
    ls = "--" if "LDR" in k else "-"
    ax.plot(weeks, y, marker='o', linestyle=ls, label=f"{k} (slope={s} ng/10^6/wk)")
ax.set_xlabel("Week"); ax.set_ylabel("8-oxo-dG (ng / 10^6 cells)")
ax.set_title("Reconstructed extracellular 8-oxo-dG accumulation (Sangsuwan 2023 Fig 3A)")
ax.legend(); fig.tight_layout(); fig.savefig(FIG/"fig3_oxodg.png", dpi=140); plt.close(fig)

# --- Fig 6A / Table 1-equivalent: TIFs ---
groups = ["P8","P19-C","P19-IR","P19-ST","P23"]
ctrl = [1.91, 7.95, 12.32, 11.55, 18.27]
ctrl_se = [0.45, 1.13, 1.52, 1.29, 2.72]
gy   = [3.88, 10.71, 14.75, 16.33, 28.55]
gy_se = [0.42, 1.58, 1.91, 2.26, 2.55]
x = np.arange(len(groups)); w = 0.35
fig, ax = plt.subplots(figsize=(7,5))
ax.bar(x - w/2, ctrl, w, yerr=ctrl_se, capsize=4, label="Control")
ax.bar(x + w/2, gy,   w, yerr=gy_se,   capsize=4, label="1 Gy, 48 h")
ax.set_xticks(x); ax.set_xticklabels(groups)
ax.set_ylabel("TIFs / cell")
ax.set_title("Reconstructed telomere dysfunction-induced foci (Sangsuwan 2023 Fig 6A / Table 1)")
ax.legend(); fig.tight_layout(); fig.savefig(FIG/"fig6_tifs.png", dpi=140); plt.close(fig)

print("Wrote figures to", FIG)
