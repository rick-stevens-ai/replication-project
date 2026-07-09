#!/usr/bin/env python3
"""Plot 15-to-1 distillation scaling curve."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

evdir = Path(__file__).parent
with open(evdir / "results_analytic.json") as f:
    R = json.load(f)
with open(evdir / "qiskit_sanity.json") as f:
    Q = json.load(f)

pin_ana = [s["p_in"] for s in R["claim1_15to1_cubic_scaling"]["sweep"]]
pou_ana = [s["p_out"] for s in R["claim1_15to1_cubic_scaling"]["sweep"]]

pin_mc  = [s["p_err_injected"] for s in Q["B_noisy_T_gate_monte_carlo"]["sweep"]]
pou_mc  = [max(s["raw_measured"], 1e-20) for s in Q["B_noisy_T_gate_monte_carlo"]["sweep"]]
pou_dis = [s["distilled_15to1"] for s in Q["B_noisy_T_gate_monte_carlo"]["sweep"]]

fig, ax = plt.subplots(figsize=(7, 5))
# Analytic 15-to-1 curve
ax.loglog(pin_ana, pou_ana, "b-", label=r"analytic $p_{out}=35\,p_{in}^{3}$")
# MC-verified raw error rate (linear scaling)
ax.loglog(pin_mc, pou_mc, "ks", markersize=8, label="Qiskit MC raw error rate")
# Line p=p (identity)
ax.loglog(pin_ana, pin_ana, "k--", alpha=0.5, label=r"$p_{out}=p_{in}$ (no distillation)")
# Distilled points from MC sweep
ax.loglog(pin_mc, pou_dis, "r^", markersize=8, label="15-to-1 distilled (from MC $p_{in}$)")

ax.set_xlabel(r"$p_{in}$  (raw T-state error rate)")
ax.set_ylabel(r"$p_{out}$  (output error rate)")
ax.set_title("O'Gorman-Campbell 2016 (arXiv:1605.07197)\n"
             "15-to-1 magic-state distillation scaling")
ax.legend(loc="upper left", fontsize=9)
ax.grid(True, which="both", alpha=0.3)
plt.tight_layout()
outfile = evdir / "distillation_scaling.png"
plt.savefig(outfile, dpi=150)
print("wrote", outfile)
