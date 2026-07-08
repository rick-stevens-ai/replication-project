import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open("results.json") as f:
    data = json.load(f)

by_d = {}
for r in data["results"]:
    by_d.setdefault(r["distance"], []).append(r)

fig, ax = plt.subplots(figsize=(6, 4.5))
for d, rows in sorted(by_d.items()):
    rows.sort(key=lambda r: r["p_physical"])
    xs = [r["p_physical"] for r in rows]
    ys = [max(r["p_logical"], 1e-6) for r in rows]
    es = [r["stderr"] for r in rows]
    ax.errorbar(xs, ys, yerr=es, marker="o", label=f"d={d}", capsize=3)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Physical error rate  p")
ax.set_ylabel("Logical error rate  $p_L$  (per memory experiment)")
ax.set_title("Rotated surface-code memory (Stim + PyMatching)\n"
             "TISCC replication SPOT-CHECK — arXiv 2311.10687")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig("plot_pL_vs_p.png", dpi=140)
print("wrote plot_pL_vs_p.png")
