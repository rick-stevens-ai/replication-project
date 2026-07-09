#!/usr/bin/env python3
"""Plot mean-absolute-error vs epsilon for raw / ZNE1 / ZNE2, from zne_results.json.
Reproduces the qualitative shape of Fig. 1(a) of Temme-Bravyi-Gambetta (2017)."""
import json, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
data = json.loads((d / "zne_results.json").read_text())
agg = data["aggregate_by_eps"]

eps = [a["eps"] for a in agg]
raw = [a["mean_err_raw"]  for a in agg]
z1  = [a["mean_err_zne1"] for a in agg]
z2  = [a["mean_err_zne2"] for a in agg]

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.loglog(eps, raw, "o-", label="raw noisy  E(eps)")
ax.loglog(eps, z1,  "s-", label="ZNE n=1 (linear, c=1,2)")
ax.loglog(eps, z2,  "^-", label="ZNE n=2 (Richardson, c=1,2,3)")
ax.set_xlabel(r"depolarizing-noise rate $\epsilon$")
ax.set_ylabel(r"mean $|E - E_{ideal}|$   (avg over 8 random 4-qubit depth-6 circuits)")
ax.set_title("Replication of Temme-Bravyi-Gambetta (arXiv:1612.02058)\nZero-Noise Extrapolation vs raw noisy expectation value")
ax.grid(True, which="both", alpha=0.4)
ax.legend()
fig.tight_layout()
out = d / "zne_error_vs_eps.png"
fig.savefig(out, dpi=150)
print(f"[saved] {out}")
