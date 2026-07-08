import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open("../report/evidence/depth_scan.json") as f:
    d = json.load(f)

fig, ax = plt.subplots(1, 1, figsize=(6, 4.5))
ax.plot(d["Ns"], d["seq_depth"], "o-", label="Sequential (one plaquette at a time)")
ax.plot(d["Ns"], d["par_depth"], "s-", label="Parallel (LHZ shift-classes)")
ax.axhline(28, color="k", linestyle="--", alpha=0.5, label="Paper claim: 28")
ax.set_xlabel("N (logical spins)")
ax.set_ylabel("Circuit depth (basis {cx, rz, u})")
ax.set_title("LHZ constraint-layer depth vs system size\n"
             "arXiv:1802.01157 (Lechner 2018) — replication")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("../report/evidence/depth_vs_N.png", dpi=150)
print("Wrote depth_vs_N.png")
