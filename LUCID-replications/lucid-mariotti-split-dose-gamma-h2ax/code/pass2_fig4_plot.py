"""Render the Fig-4 (net foci induced by 2nd exposure) reproduction as a bar
chart, using the model + Table-S1 parameters."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
res = json.load(open(ROOT / "results" / "pass2_claims.json"))
t8 = next(c for c in res["claims"] if c["claim_id"] == "T-8")
single_peak = t8["single_acute_1Gy_peak"]
gaps = []
net = []
for r in t8["per_gap"]:
    gaps.append(r["gap_h"])
    net.append(r["net_foci_from_2nd_exposure"])

fig, ax = plt.subplots(figsize=(6.5, 4.0))
labels = ["20 min", "1 h", "2 h", "5 h", "12 h"]
x = np.arange(len(labels))
bars = ax.bar(x, net, color=["#888"] * 4 + ["#3a3"])
ax.axhline(single_peak, color="r", linestyle="--",
           label=f"Single-acute 1 Gy peak = {single_peak:.1f}")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("Net foci/cell induced by 2nd exposure\n(model: total − 1st-exposure residual at gap+0.5 h)")
ax.set_xlabel("Time gap between exposures")
ax.set_title("Pass-2 reproduction of Fig 4 (Mariotti 2013)\nNet foci from 2nd 1-Gy exposure vs single-acute 1-Gy reference")
for xi, v in zip(x, net):
    ax.text(xi, v + 0.5, f"{v:.1f}", ha="center", fontsize=9)
ax.legend(loc="upper left", fontsize=9)
ax.set_ylim(0, max(max(net), single_peak) * 1.2)
plt.tight_layout()
out = ROOT / "figures" / "fig4_reproduction.png"
plt.savefig(out, dpi=150)
print("Wrote", out)
