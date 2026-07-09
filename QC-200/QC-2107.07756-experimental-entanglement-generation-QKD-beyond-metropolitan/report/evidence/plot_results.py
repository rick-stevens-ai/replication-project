#!/usr/bin/env python3
"""Plot replicated key-rate curves alongside paper claims."""
import json, csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"

# Load CSVs
scenarios = {}
with (OUT / "key_rate_vs_power.csv").open() as f:
    r = csv.DictReader(f)
    for row in r:
        name = row["scenario"]
        scenarios.setdefault(name, []).append(
            (float(row["pump_mW"]), float(row["key_rate_bps"])))

paper_points = {
    # (name, pump_mW, R_bps)
    "100GHz": (400, 1.2e9),
    "50GHz": (660, 2.0e9),
    "25GHz": (900, 3.0e9),
    "12.5GHz": (800, 3.0e9),
}

fig, ax = plt.subplots(figsize=(8, 6))
colors = {"200GHz": "#888", "100GHz": "tab:blue", "50GHz": "tab:orange",
          "25GHz": "tab:green", "12.5GHz": "tab:red"}
for name, pts in scenarios.items():
    pts.sort()
    x = [p[0] for p in pts]
    y = [p[1] for p in pts]
    ax.plot(x, y, "o-", color=colors.get(name, "gray"), label=f"replica {name}")

for name, (P, R) in paper_points.items():
    ax.plot(P, R, "*", markersize=18, color=colors.get(name, "black"),
            markeredgecolor="black",
            label=f"paper {name} claim ({R/1e9:.1f} Gbit/s @ {P} mW)")

ax.axhline(1.0e9, color="k", linestyle=":", alpha=0.5)
ax.text(50, 1.05e9, "1 Gbit/s", fontsize=9)
ax.set_xlabel("Pump power [mW]")
ax.set_ylabel("Secure key rate [bit/s]")
ax.set_yscale("log")
ax.set_title("Replication of Neumann et al. (arXiv:2107.07756) Fig 6:\n"
             "Secure key rate vs pump power at various WDM spacings")
ax.legend(fontsize=8, loc="lower right")
ax.grid(True, which="both", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "fig6_replication.png", dpi=140)
print(f"saved {OUT / 'fig6_replication.png'}")

# Distance plot
d = []
with (OUT / "key_rate_vs_distance.csv").open() as f:
    r = csv.DictReader(f)
    for row in r:
        d.append((float(row["distance_km"]), float(row["key_rate_bps"])))

fig, ax = plt.subplots(figsize=(7, 5))
xs = [p[0] for p in d]
ys = [p[1] for p in d]
ax.semilogy(xs, ys, "o-", color="tab:blue", label="replica (100 GHz, n=66, 400 mW)")
paper_10km = ys[0] * 0.63    # paper says 10 km => 63% of value
ax.plot(10, paper_10km, "*", markersize=18, color="tab:red",
        label=f"paper claim: 10 km => 63% of 0 km value")
ax.set_xlabel("Fiber distance [km]  (alpha = 0.2 dB/km, both arms)")
ax.set_ylabel("Secure key rate [bit/s]")
ax.set_title("Fiber-loss sensitivity of secure key rate")
ax.legend()
ax.grid(True, which="both", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "distance_replication.png", dpi=140)
print(f"saved {OUT / 'distance_replication.png'}")
