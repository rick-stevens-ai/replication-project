"""
plot_predictions.py — render the model-predicted condition comparison
+ post-CD kinetics for Plodowska 2025 replication slot.

Outputs:
  figures/condition_peak_comparison.png  — bar chart of predicted peak
      foci/cell for the five conditions (AD-low, AD-high, CD, AD-low+CD,
      AD-high+CD), with KU overlay.
  figures/post_cd_kinetics.png           — CD-only foci decay curves
      (with and without KU) at 1-h resolution out to 24 h.
  figures/detectability_landscape.png    — heat-style line plot of
      predicted AD-only steady-state vs k_repair, with literature
      background band shaded.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from foci_kinetics import acute_N  # noqa: E402

FIG = ROOT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------
# 1) condition peak bar chart
# --------------------------------------------------------------------------
Y, k = 35.0, 0.45
AD_low_ss = Y * 31e-6 / k       # 0.00241
AD_high_ss = Y * 55e-6 / k      # 0.00428
CD_peak = Y * 1.0               # 35
KU_AD = 1.00
KU_CD = 0.40

conditions = [
    "AD-low\n(31 µGy/h)",
    "AD-high\n(55 µGy/h)",
    "CD\n(1 Gy)",
    "AD-low\n+CD",
    "AD-high\n+CD",
]
vals_noKU = [AD_low_ss, AD_high_ss, CD_peak,
             AD_low_ss + CD_peak, AD_high_ss + CD_peak]
vals_KU = [AD_low_ss * KU_AD, AD_high_ss * KU_AD, CD_peak * KU_CD,
           AD_low_ss * KU_AD + CD_peak * KU_CD,
           AD_high_ss * KU_AD + CD_peak * KU_CD]

fig, ax = plt.subplots(figsize=(8, 4.5))
x = list(range(len(conditions)))
w = 0.38
ax.bar([i - w/2 for i in x], vals_noKU, width=w, label="no KU-55933", color="#1f77b4")
ax.bar([i + w/2 for i in x], vals_KU, width=w, label="+ KU-55933 (model)", color="#d62728")
ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=9)
ax.set_ylabel("predicted mean 53BP1 foci / cell")
ax.set_yscale("log")
ax.set_ylim(1e-4, 1e2)
ax.set_title("Plodowska 2025 — predicted condition peak (model only, NOT author fit)")
ax.legend(loc="lower right", frameon=False, fontsize=9)
ax.grid(axis="y", which="major", alpha=0.3)
for i, (a, b) in enumerate(zip(vals_noKU, vals_KU)):
    ax.text(i - w/2, a * 1.4, f"{a:.3g}", ha="center", fontsize=7)
    ax.text(i + w/2, b * 1.4, f"{b:.3g}", ha="center", fontsize=7)
fig.tight_layout()
fig.savefig(FIG / "condition_peak_comparison.png", dpi=150)
plt.close(fig)

# --------------------------------------------------------------------------
# 2) post-CD kinetics
# --------------------------------------------------------------------------
ts = [i * 0.25 for i in range(0, 96 * 4 + 1)]  # 0 .. 96 h at 15-min res, actually 0..24
ts = [i * 0.25 for i in range(0, 24 * 4 + 1)]   # 0..24 h, 15-min res
N_cd = [acute_N(t, 0.0, Y * 1.0, k) for t in ts]
N_cd_ku = [acute_N(t, 0.0, Y * 1.0 * KU_CD, k) for t in ts]

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(ts, N_cd, "-", color="#1f77b4", linewidth=2, label="CD only")
ax.plot(ts, N_cd_ku, "--", color="#d62728", linewidth=2, label="CD + KU-55933 (model, 40% Y)")
ax.set_xlabel("time after CD (h)")
ax.set_ylabel("mean 53BP1 foci / cell")
ax.set_title("Plodowska 2025 — CD-only kinetics (model)")
ax.axhline(0.30, color="grey", linestyle=":", linewidth=1,
           label="spontaneous bg estimate (0.30 foci/cell)")
ax.set_xlim(0, 24)
ax.set_ylim(0, 40)
ax.legend(loc="upper right", frameon=False, fontsize=9)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(FIG / "post_cd_kinetics.png", dpi=150)
plt.close(fig)

# --------------------------------------------------------------------------
# 3) detectability landscape
# --------------------------------------------------------------------------
ks = [0.01, 0.02, 0.03, 0.05, 0.075, 0.10, 0.15, 0.25, 0.35, 0.45, 0.55, 0.70]
ss_low = [Y * 31e-6 / kk for kk in ks]
ss_high = [Y * 55e-6 / kk for kk in ks]

fig, ax = plt.subplots(figsize=(7.5, 4.5))
ax.plot(ks, ss_low, "o-", color="#1f77b4", label="AD-low (31 µGy/h)")
ax.plot(ks, ss_high, "s-", color="#ff7f0e", label="AD-high (55 µGy/h)")
ax.axhspan(0.10, 0.50, color="grey", alpha=0.18,
           label="literature spontaneous bg (0.1-0.5 foci/cell)")
ax.set_xlabel("repair-rate parameter k_repair (1/h)")
ax.set_ylabel("predicted AD-only steady-state foci / cell")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_title("Plodowska 2025 — AD-only detectability landscape")
ax.legend(loc="upper right", frameon=False, fontsize=9)
ax.grid(which="both", alpha=0.3)
ax.annotate("consensus k=0.45/h\n=> N_ss invisible\n(50-200x below bg)",
            xy=(0.45, Y * 55e-6 / 0.45),
            xytext=(0.05, 0.0008),
            fontsize=8,
            arrowprops=dict(arrowstyle="->", color="black", lw=0.8))
ax.annotate("slow-component k~0.02/h\n=> N_ss in bg range\n(detectable)",
            xy=(0.02, Y * 55e-6 / 0.02),
            xytext=(0.012, 0.4),
            fontsize=8,
            arrowprops=dict(arrowstyle="->", color="black", lw=0.8))
fig.tight_layout()
fig.savefig(FIG / "detectability_landscape.png", dpi=150)
plt.close(fig)

print("wrote 3 figures to", FIG)
