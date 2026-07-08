"""Plot our replication analog of paper Fig 4 (max tensor rank / contraction
width vs depth for different grid sizes) plus a bonus plot: TN flops vs 2^n."""

import json
import math
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open("../report/evidence/sweep.json") as f:
    data = json.load(f)
results = data["results"]

per_grid = defaultdict(list)
for r in results:
    per_grid[(r["ell"], r["m"])].append(r)

# Plot 1: width vs depth for a subset of grids that spans ell = 1,2,3,4
fig, ax = plt.subplots(figsize=(6.5, 4.5))
grids_to_plot = [(1, 16), (2, 8), (3, 5), (4, 4)]
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
for (ell, m), c in zip(grids_to_plot, colors):
    if (ell, m) not in per_grid:
        continue
    pts = sorted(per_grid[(ell, m)], key=lambda r: r["depth"])
    ds = [r["depth"] for r in pts]
    ws = [r["contraction_width_log2"] for r in pts]
    ax.plot(ds, ws, marker="o", color=c, label=f"{ell}x{m} (n={ell*m})")
    # paper bound: min(d*ell, n)
    bs = [min(d * ell, ell * m) for d in ds]
    ax.plot(ds, bs, "--", color=c, alpha=0.4)
ax.set_xlabel("Circuit depth d")
ax.set_ylabel(r"Contraction width $\log_2(\max\;\mathrm{intermediate})$")
ax.set_title("Replication analog of Boixo+2017 Fig 4:\n"
             r"tensor-network width vs depth (dashed = bound $\min(d\ell,n)$)")
ax.legend(loc="best", fontsize=8)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig("../report/evidence/fig4_analog_width_vs_depth.png", dpi=140)
plt.close(fig)
print("wrote fig4_analog_width_vs_depth.png")

# Plot 2: TN flops vs 2^n at fixed depths
fig, ax = plt.subplots(figsize=(6.5, 4.5))
for d_target, marker in [(2, "o"), (4, "s"), (6, "^")]:
    ns = []
    ratios = []
    for r in sorted(results, key=lambda r: r["n"]):
        if r["depth"] == d_target:
            ns.append(r["n"])
            ratios.append(r["opt_cost_flops"] / (2 ** r["n"]))
    ax.plot(ns, ratios, marker=marker, linestyle="-", label=f"d={d_target}")
ax.axhline(1.0, color="k", linestyle=":", alpha=0.5, label="TN = statevector")
ax.set_yscale("log")
ax.set_xlabel("Total number of qubits n")
ax.set_ylabel("TN contraction FLOPs / $2^n$ (statevector cost)")
ax.set_title("Classical savings vs statevector for shallow circuits\n"
             "(below 1 = TN cheaper than full statevector)")
ax.legend()
ax.grid(True, alpha=0.3, which="both")
fig.tight_layout()
fig.savefig("../report/evidence/tn_vs_statevector_ratio.png", dpi=140)
plt.close(fig)
print("wrote tn_vs_statevector_ratio.png")
