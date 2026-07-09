#!/usr/bin/env python3
"""Plot lowest-4 eigenvalues along the adiabatic schedule for each instance."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(__file__)
with open(os.path.join(HERE, "results.json")) as f:
    data = json.load(f)

fig, axes = plt.subplots(1, len(data["results"]), figsize=(4 * len(data["results"]), 3.6),
                         sharey=False)
if len(data["results"]) == 1:
    axes = [axes]

for ax, res in zip(axes, data["results"]):
    s = np.array(res["spectrum_s"])
    spec = np.array(res["spectrum_lowk"])
    for j in range(spec.shape[1]):
        ax.plot(s, spec[:, j], lw=1.4, label=f"E{j}" if j < 4 else None)
    ax.set_title(f"{res['label']}  (N!={res['N_dim']})", fontsize=10)
    ax.set_xlabel("s")
    ax.set_ylabel("Energy")
    ax.legend(fontsize=8, loc="best")
    ax.grid(alpha=0.3)

plt.tight_layout()
outpath = os.path.join(HERE, "spectra.png")
plt.savefig(outpath, dpi=140)
print(f"[+] wrote {outpath}")

# gap plot
fig2, ax2 = plt.subplots(figsize=(6, 3.6))
for res in data["results"]:
    s = np.array(res["spectrum_s"])
    spec = np.array(res["spectrum_lowk"])
    gap = spec[:, 1] - spec[:, 0]
    ax2.plot(s, gap, lw=1.5, label=res["label"])
ax2.set_xlabel("s")
ax2.set_ylabel("E_1(s) - E_0(s)")
ax2.set_title("Spectral gap along adiabatic path")
ax2.legend(fontsize=8)
ax2.grid(alpha=0.3)
plt.tight_layout()
outpath2 = os.path.join(HERE, "gap.png")
plt.savefig(outpath2, dpi=140)
print(f"[+] wrote {outpath2}")
