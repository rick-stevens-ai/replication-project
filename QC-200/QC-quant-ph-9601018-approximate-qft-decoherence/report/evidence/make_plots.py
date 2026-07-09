#!/usr/bin/env python3
"""Plot AQFT fidelity vs m and period-finding success vs m."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = os.path.dirname(__file__)

with open(os.path.join(here, "results_fidelity.json")) as f:
    fid = json.load(f)
with open(os.path.join(here, "results_period_finding.json")) as f:
    per = json.load(f)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

# (a) state fidelity
ax = axes[0]
for n_str, per_m in fid["experiment_A_fidelity"].items():
    n = int(n_str)
    ms = sorted(int(m) for m in per_m.keys())
    means = [per_m[str(m)]["mean_fidelity"] for m in ms]
    stds = [per_m[str(m)]["std_fidelity"] for m in ms]
    ax.errorbar(ms, means, yerr=stds, marker="o", label=f"n={n}")
ax.set_xlabel("AQFT truncation parameter m")
ax.set_ylabel(r"$|\langle QFT\,\psi\,|\,AQFT_m\,\psi\rangle|^2$")
ax.set_title("(a) State fidelity vs. m (100 random pure states)")
ax.set_ylim(0, 1.05)
ax.axhline(1.0, ls=":", c="gray")
ax.grid(alpha=0.3)
ax.legend()

# (b) period finding
ax = axes[1]
import math
for L_str, per_m in per["results"].items():
    L = int(L_str)
    ms = sorted(int(m) for m in per_m.keys())
    succ = [per_m[str(m)]["mean_success_prob"] for m in ms]
    ax.plot(ms, succ, marker="o", label=f"AQFT success, L={L}")
    lb = [(8.0/math.pi**2)*math.sin(math.pi*m/(4*L))**2 for m in ms]
    ax.plot(ms, lb, ls="--", label=f"paper LB (8/π²)sin²(πm/4L), L={L}")
ax.axhline(4/math.pi**2, ls=":", c="k", label=r"exact QFT LB $4/\pi^2$")
ax.set_xlabel("AQFT truncation parameter m")
ax.set_ylabel("Success probability (avg over offsets)")
ax.set_title("(b) Period finding of 7^x mod 15 (r=4)")
ax.set_ylim(0, 1.05)
ax.grid(alpha=0.3)
ax.legend(fontsize=8)

fig.tight_layout()
out = os.path.join(here, "figure_aqft_replication.png")
fig.savefig(out, dpi=150)
print(f"Wrote {out}")
