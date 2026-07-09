#!/usr/bin/env python3
"""Make Fig-3/Fig-4-style plots from results.json."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "results.json")) as f:
    R = json.load(f)

rows = R["results"]
lambdas = R["lambda_ratios"]
distances = sorted({r["distance"] for r in rows})
ps = sorted({r["p"] for r in rows})

# --- Fig A: eps_per_round vs p, one line per distance -----------------------
fig, ax = plt.subplots(figsize=(6, 4.2))
markers = {3: "o", 5: "s", 7: "^"}
colors = {3: "#1f77b4", 5: "#d62728", 7: "#2ca02c"}
for d in distances:
    xs, ys, es = [], [], []
    for r in rows:
        if r["distance"] == d:
            xs.append(r["p"])
            ys.append(r["eps_per_round"])
            es.append(r["eps_per_round_se"])
    xs = np.array(xs); ys = np.array(ys); es = np.array(es)
    ax.errorbar(xs, ys, yerr=es, marker=markers[d], color=colors[d],
                label=f"d={d}", capsize=3, lw=1.2)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("Physical error rate p (circuit-level depolarizing)")
ax.set_ylabel(r"Logical error per round $\varepsilon_d$")
ax.set_title("Surface code memory: logical error per round vs p\n"
             "Replication of Google arXiv:2207.06431 (Stim + PyMatching)")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(here, "fig_eps_vs_p.png"), dpi=150)
fig.savefig(os.path.join(here, "fig_eps_vs_p.pdf"))
plt.close(fig)

# --- Fig B: Lambda_{3/5} and Lambda_{5/7} vs p -----------------------------
fig, ax = plt.subplots(figsize=(6, 4.2))
p_arr = np.array([L["p"] for L in lambdas])
L35 = np.array([L["Lambda_3/5"] for L in lambdas])
L57 = np.array([L["Lambda_5/7"] for L in lambdas])
ax.plot(p_arr, L35, "o-", color="#d62728", label=r"$\Lambda_{3/5}=\varepsilon_3/\varepsilon_5$")
ax.plot(p_arr, L57, "s-", color="#2ca02c", label=r"$\Lambda_{5/7}=\varepsilon_5/\varepsilon_7$")
ax.axhline(1.0, color="k", ls="--", lw=0.8, alpha=0.5, label=r"$\Lambda=1$ (threshold)")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("Physical error rate p")
ax.set_ylabel(r"Suppression factor $\Lambda$")
ax.set_title("Error suppression with code distance\n"
             r"Google claim: $\Lambda_{3/5}>1$ near their operating point")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(here, "fig_lambda_vs_p.png"), dpi=150)
fig.savefig(os.path.join(here, "fig_lambda_vs_p.pdf"))
plt.close(fig)

print("wrote fig_eps_vs_p.{png,pdf} and fig_lambda_vs_p.{png,pdf}")
