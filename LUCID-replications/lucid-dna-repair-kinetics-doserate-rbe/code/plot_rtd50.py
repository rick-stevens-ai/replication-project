"""
Plot R_TD50 vs dose-rate (this replication) vs paper Table 3 values.
"""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.abspath(os.path.join(HERE, "..", "results", "rtd50_results.json"))
FIG_DIR = os.path.abspath(os.path.join(HERE, "..", "figures"))
os.makedirs(FIG_DIR, exist_ok=True)

with open(RES) as f:
    r = json.load(f)

rates_1 = [row["dose_rate_Gy_per_min"] for row in r["rows_1Fr"]]
R_1     = [row["R_TD50"]               for row in r["rows_1Fr"]]
rates_2 = [row["dose_rate_Gy_per_min"] for row in r["rows_2Fr"]]
R_2     = [row["R_TD50"]               for row in r["rows_2Fr"]]

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(rates_1, R_1, "-o", color="black",
        label="This replication (1 fraction, S* matched at 20 Gy)")
ax.plot(rates_2, R_2, "--s", color="purple",
        label="This replication (2 fractions, S* matched at 12 Gy)")

# Paper Table 3 points (RSC photon-equivalent factor extracted directly)
t3 = r["paper_table3"]
def scatter(rates_dict, marker, color, label):
    xs = list(rates_dict.keys())
    ys = list(rates_dict.values())
    ax.scatter(xs, ys, marker=marker, color=color, s=90,
               edgecolors="white", linewidths=1.2, zorder=5, label=label)

scatter(t3["1Fr_proton"], "s",  "tab:blue",   "Paper Table 3 (1Fr, proton-SOBP rates)")
scatter(t3["2Fr_proton"], "D",  "tab:cyan",   "Paper Table 3 (2Fr, proton-SOBP rates)")
scatter(t3["1Fr_helium"], "^",  "tab:red",    "Paper Table 3 (1Fr, He-SOBP rates)")
scatter(t3["2Fr_helium"], "v",  "tab:orange", "Paper Table 3 (2Fr, He-SOBP rates)")

ax.set_xscale("log")
ax.set_xlabel("Photon dose rate [Gy/min]")
ax.set_ylabel(r"$R_{\mathrm{TD50}} = \mathrm{TD50}^\gamma(3.75)\, /\, \mathrm{TD50}^\gamma(\dot D)$")
ax.set_title("Figure 4 (left panel) reproduction — rat spinal cord, UNIVERSE with-repair params")
ax.axhline(1.0, color="grey", lw=0.5, ls=":")
ax.axvline(3.75, color="grey", lw=0.5, ls=":")
ax.text(3.75, 0.998, "  ref 3.75 Gy/min", fontsize=8, color="grey",
        rotation=90, va="bottom")
ax.legend(fontsize=8, loc="lower right")
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fp = os.path.join(FIG_DIR, "fig4_left_RTD50_replication.png")
fig.savefig(fp, dpi=150)
print("wrote", fp)
