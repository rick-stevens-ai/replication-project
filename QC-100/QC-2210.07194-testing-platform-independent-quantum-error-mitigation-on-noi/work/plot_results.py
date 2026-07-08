#!/usr/bin/env python3
"""Plot improvement factor vs depth for both noise levels."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "report" / "evidence"

with open(OUT / "zne_results_v2.json") as f:
    data = json.load(f)

fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
for ax, (key, rows) in zip(axes, data["per_noise"].items()):
    d = [r["d"] for r in rows]
    muR = [r["mu_ZNE_R"] for r in rows]
    muL = [r["mu_ZNE_L"] for r in rows]
    ax.plot(d, muR, "o-", label="ZNE Richardson", color="green")
    ax.plot(d, muL, "s-", label="ZNE Linear", color="blue")
    ax.axhline(1.0, color="black", linestyle="--", alpha=0.5, label="mu=1 (no benefit)")
    pct = int(key.replace("depol_", "").replace("pmil", ""))
    ax.set_title(f"{pct/10:.1f}% 2Q depolarizing")
    ax.set_xlabel("Depth d (Clifford layers)")
    ax.set_ylabel("Improvement factor mu")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    ax.legend()

plt.suptitle("Independent Replication of Russo et al. 2210.07194 (Fig 2 style)\n"
             "n=3 RB circuits, 10^4 shots, kZNE=3, global unitary folding")
plt.tight_layout()
plt.savefig(OUT / "improvement_factor_vs_depth.png", dpi=120)
print(f"Wrote {OUT/'improvement_factor_vs_depth.png'}")

# Also plot expectation values
fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
for ax, (key, rows) in zip(axes, data["per_noise"].items()):
    d = [r["d"] for r in rows]
    A0 = [r["A0_mean"] for r in rows]
    AR = [r["AZNE_R_mean"] for r in rows]
    AL = [r["AZNE_L_mean"] for r in rows]
    ax.plot(d, A0, "s-", label="Unmitigated", color="orange")
    ax.plot(d, AR, "^-", label="ZNE Richardson", color="green")
    ax.plot(d, AL, "v-", label="ZNE Linear", color="blue")
    ax.axhline(1.0, color="black", linestyle=":", alpha=0.5, label="Ideal")
    pct = int(key.replace("depol_", "").replace("pmil", ""))
    ax.set_title(f"{pct/10:.1f}% 2Q depolarizing")
    ax.set_xlabel("Depth d")
    ax.set_ylabel("<A> = P(z=0..0)")
    ax.grid(True, alpha=0.3)
    ax.legend()

plt.suptitle("Expectation values, unmitigated vs ZNE — replication of 2210.07194 Fig 2 (bottom)")
plt.tight_layout()
plt.savefig(OUT / "expectation_vs_depth.png", dpi=120)
print(f"Wrote {OUT/'expectation_vs_depth.png'}")
