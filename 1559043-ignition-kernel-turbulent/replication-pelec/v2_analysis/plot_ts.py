#!/usr/bin/env python3
"""Plot time-series of ignition diagnostics for the 4-phi sweep (v2)."""
import sys, csv
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

infile = sys.argv[1] if len(sys.argv) > 1 else "timeseries.csv"
outprefix = sys.argv[2] if len(sys.argv) > 2 else "v2"

data = defaultdict(lambda: {"t":[], "Tmax":[], "OH":[], "H2O":[], "CO2":[], "CH4":[]})
with open(infile) as f:
    r = csv.DictReader(f)
    for row in r:
        try:
            phi = float(row["phi"])
            t = float(row["t"])
            data[phi]["t"].append(t*1e6)  # μs
            data[phi]["Tmax"].append(float(row["Tmax"]))
            data[phi]["OH"].append(float(row["OHmax"]))
            data[phi]["H2O"].append(float(row["H2Omax"]))
            data[phi]["CO2"].append(float(row["CO2max"]))
            data[phi]["CH4"].append(float(row["CH4max"]))
        except Exception:
            pass

phis = sorted(data.keys())
colors = {0.6:'#1f77b4', 0.8:'#2ca02c', 1.0:'#ff7f0e', 1.2:'#d62728'}

fig, axs = plt.subplots(2, 2, figsize=(10,7), sharex=True)

for phi in phis:
    d = data[phi]
    idx = np.argsort(d["t"])
    t = np.array(d["t"])[idx]
    for key, ax, title, ylab in [
        ("Tmax", axs[0,0], "Max temperature", "T_max [K]"),
        ("OH",   axs[0,1], "Max OH mass fraction", "Y(OH)_max"),
        ("H2O",  axs[1,0], "Max H2O mass fraction", "Y(H2O)_max"),
        ("CO2",  axs[1,1], "Max CO2 mass fraction", "Y(CO2)_max"),
    ]:
        v = np.array(d[key])[idx]
        ax.plot(t, v, '-o', ms=3, color=colors[phi], label=f"φ={phi}")
        ax.set_title(title); ax.set_ylabel(ylab); ax.grid(alpha=0.3)

axs[0,0].legend(loc="best", fontsize=9)
for ax in axs[1,:]: ax.set_xlabel("time [μs]")
fig.suptitle("PeleC ignition kernel replication v2: 4-φ sweep", fontsize=12)
fig.tight_layout()
fig.savefig(f"{outprefix}_timeseries.png", dpi=140)
print(f"Wrote {outprefix}_timeseries.png")

# Also plot bar summary: last-timepoint products vs phi
fig, ax = plt.subplots(figsize=(7,4.5))
width = 0.2
xs = np.arange(len(phis))
for i, key in enumerate(["OH","H2O","CO2"]):
    vals = []
    for phi in phis:
        d = data[phi]
        if d[key]: vals.append(d[key][-1])
        else: vals.append(0)
    ax.bar(xs + (i-1)*width, vals, width, label={"OH":"Y(OH)","H2O":"Y(H2O)","CO2":"Y(CO2)"}[key])
ax.set_xticks(xs); ax.set_xticklabels([f"φ={p}" for p in phis])
ax.set_ylabel("Max mass fraction at t_end")
ax.set_title("Combustion products vs φ (monotonic trend → kernel ignites fuel)")
ax.legend(); ax.grid(alpha=0.3, axis='y')
fig.tight_layout()
fig.savefig(f"{outprefix}_phi_trend.png", dpi=140)
print(f"Wrote {outprefix}_phi_trend.png")
