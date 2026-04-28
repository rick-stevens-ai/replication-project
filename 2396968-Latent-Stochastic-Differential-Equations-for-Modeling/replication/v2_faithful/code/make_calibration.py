#!/usr/bin/env python3
"""Calibration: empirical coverage vs nominal quantile, per-parameter.

Reads metrics from v2_run.log (parsed manually below) and writes
figures/calibration.pdf.
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

NOMINAL = np.array([0.638, 0.955, 0.997])
COV = {
    "SPIN":      [0.1095, 0.399,  0.526 ],
    "CHEIGHT":   [0.2745, 0.542,  0.8565],
    "Z_Q":       [0.354,  0.663,  0.887 ],
    "INC_ANG":   [0.2865, 0.578,  0.7515],
    "BETA":      [0.502,  0.9185, 0.9515],
    "eddingtons":[0.422,  0.775,  0.7785],
    "MASS":      [0.5955, 0.8925, 0.9505],
    "log_tau":   [0.6575, 0.9005, 0.967 ],
    "SFinf":     [0.8495, 0.978,  0.9955],
}
PRETTY = {
    "SPIN": r"$a$",
    "CHEIGHT": r"$h/r_g$",
    "Z_Q": r"$z_q$",
    "INC_ANG": r"$\theta_{\rm inc}$",
    "BETA": r"$\beta$",
    "eddingtons": r"$\lambda_{\rm Edd}$",
    "MASS": r"$\log_{10} M$",
    "log_tau": r"$\log_{10}\tau$",
    "SFinf": r"$SF_\infty$",
}

fig, ax = plt.subplots(figsize=(6, 5))
ax.plot([0, 1], [0, 1], "k--", lw=1, label="ideal")
markers = ["o", "s", "^", "v", "D", "p", "*", "X", "P"]
for (name, vals), m in zip(COV.items(), markers):
    ax.plot(NOMINAL, vals, m + "-", ms=8, lw=1.2, label=PRETTY[name])
ax.set_xlabel("Nominal coverage (Gaussian quantile)")
ax.set_ylabel("Empirical coverage on test set")
ax.set_xlim(0, 1.02)
ax.set_ylim(0, 1.02)
ax.set_xticks(NOMINAL)
ax.set_xticklabels([f"{q:.3f}" for q in NOMINAL])
ax.grid(alpha=0.3)
ax.legend(ncol=3, fontsize=8, loc="lower right")
ax.set_title("Per-parameter calibration (v2 run)")
out = Path(__file__).resolve().parent.parent / "figures" / "calibration.pdf"
fig.tight_layout()
fig.savefig(out)
print("wrote", out)

# overall-LC summary numbers from log
lc = {
    "1$\\sigma$": (0.733, 0.683),
    "2$\\sigma$": (0.945, 0.955),
    "3$\\sigma$": (0.990, 0.997),
}
fig2, ax2 = plt.subplots(figsize=(4.5, 4))
nom = [v[1] for v in lc.values()]
emp = [v[0] for v in lc.values()]
ax2.plot([0, 1], [0, 1], "k--", lw=1)
ax2.plot(nom, emp, "o-", ms=10, color="C3")
for (lab, (e, n)) in lc.items():
    ax2.annotate(lab, (n, e), xytext=(6, -2), textcoords="offset points")
ax2.set_xlabel("Nominal coverage")
ax2.set_ylabel("Empirical coverage")
ax2.set_xlim(0.5, 1.02); ax2.set_ylim(0.5, 1.02)
ax2.grid(alpha=0.3)
ax2.set_title("Overall light-curve reconstruction calibration")
out2 = Path(__file__).resolve().parent.parent / "figures" / "lc_calibration.pdf"
fig2.tight_layout()
fig2.savefig(out2)
print("wrote", out2)
