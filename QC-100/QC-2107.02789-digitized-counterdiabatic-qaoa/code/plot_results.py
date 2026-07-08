#!/usr/bin/env python3
"""Plot approximation ratio vs p for QAOA and DC-QAOA (replication of arXiv:2107.02789 Fig. 3b)."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "report" / "evidence" / "maxcut_results.json").read_text())
results = data["results"]

graphs = sorted({r["graph"] for r in results})
fig, axes = plt.subplots(1, len(graphs), figsize=(4 * len(graphs), 3.5), squeeze=False)
for ax, g in zip(axes[0], graphs):
    for variant, style in [("qaoa", "-o"), ("dc", "-s")]:
        rs = [r for r in results if r["graph"] == g and r["variant"] == variant]
        rs.sort(key=lambda x: x["p"])
        ax.plot([r["p"] for r in rs], [r["approx_ratio"] for r in rs],
                style, label=("QAOA" if variant == "qaoa" else "DC-QAOA"))
    ax.set_xlabel("Depth p")
    ax.set_ylabel("Approx. ratio R")
    ax.set_title(g)
    ax.set_ylim(0.6, 1.02)
    ax.grid(True, alpha=0.3)
    ax.legend()

plt.suptitle("Replication: DC-QAOA vs QAOA (MaxCut, arXiv:2107.02789 Fig. 3b)")
plt.tight_layout()
out = ROOT / "report" / "evidence" / "approx_ratio_vs_p.png"
plt.savefig(out, dpi=150)
print(f"Wrote {out}")
