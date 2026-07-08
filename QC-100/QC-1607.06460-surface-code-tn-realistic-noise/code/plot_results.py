#!/usr/bin/env python3
"""Plot threshold curves for DP vs HPA-AD from sweep_results.json."""
import json
import math
from pathlib import Path
import matplotlib.pyplot as plt

EV = Path(__file__).resolve().parent.parent / "report" / "evidence"

with open(EV / "sweep_results.json") as f:
    data = json.load(f)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for ax, sweep in zip(axes, data["sweeps"]):
    rows = sweep["results"]
    by_d = {}
    for r in rows:
        by_d.setdefault(r["distance"], []).append((r["rate"], r["p_logical"], r["stderr"]))
    for d in sorted(by_d):
        pts = sorted(by_d[d])
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        errs = [p[2] for p in pts]
        ax.errorbar(xs, ys, yerr=errs, marker="o", label=f"d={d}")
    ax.set_xlabel("noise parameter")
    ax.set_ylabel("logical error rate  p_L")
    ax.set_title(sweep["name"])
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)

fig.suptitle("Rotated surface code memory (Stim + PyMatching MWPM)\n"
             "Left: uniform depolarizing.  Right: honest Pauli approximation of amplitude damping (γ).")
fig.tight_layout()
out = EV / "threshold_plot.png"
fig.savefig(out, dpi=140, bbox_inches="tight")
print(f"Saved {out}")
