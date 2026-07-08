#!/usr/bin/env python3
"""Generate scaling / suppression plots from surface_code_results.json."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
EVID = HERE.parent / "report" / "evidence"

with open(EVID / "surface_code_results.json") as fh:
    payload = json.load(fh)
results = payload["results"]

# ---- Plot 1: d=3 vs d=5 corrected & raw εL per round vs p ----
sweep = [r for r in results if r["experiment"] == "B_scaling_sweep"]
p_values = sorted({r["p_physical"] for r in sweep})

fig, ax = plt.subplots(figsize=(6.5, 4.6))
for d, marker in ((3, "o"), (5, "s")):
    subset = sorted([r for r in sweep if r["distance"] == d], key=lambda r: r["p_physical"])
    ps = [r["p_physical"] for r in subset]
    corr = [r["eps_per_round_corrected"] for r in subset]
    raw = [r["eps_per_round_raw"] for r in subset]
    ax.plot(ps, corr, marker=marker, linestyle="-", label=f"d={d} MWPM-corrected")
    ax.plot(ps, raw, marker=marker, linestyle="--", alpha=0.35, label=f"d={d} uncorrected")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Physical error rate p per gate")
ax.set_ylabel("Logical error rate per round  ε_L")
ax.set_title("Surface-code memory (Stim + PyMatching): d=3 vs d=5 scaling")
ax.grid(True, which="both", alpha=0.3)
ax.legend(loc="lower right", fontsize=8)
fig.tight_layout()
fig.savefig(EVID / "scaling_d3_vs_d5.png", dpi=150)
plt.close(fig)

# ---- Plot 2: below-threshold suppression ratio (corrected) ----
by_p = {}
for r in sweep:
    by_p.setdefault(r["p_physical"], {})[r["distance"]] = r["eps_per_round_corrected"]

ps = sorted(by_p.keys())
ratios = [by_p[p][5] / by_p[p][3] if by_p[p].get(3, 0) > 0 else np.nan for p in ps]

fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.axhline(1.0, color="k", linestyle=":", label="ε_L(d=5) = ε_L(d=3)")
ax.plot(ps, ratios, "o-", label="ε_L(d=5) / ε_L(d=3), corrected")
ax.set_xscale("log")
ax.set_xlabel("Physical error rate p")
ax.set_ylabel("Logical error suppression ratio")
ax.set_title("Below-threshold check: ratio<1 ⇒ larger code helps")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(EVID / "suppression_ratio.png", dpi=150)
plt.close(fig)

# ---- Threshold estimate: p where ratio crosses 1 ----
ratios_arr = np.array(ratios)
ps_arr = np.array(ps)
crossing = None
for i in range(len(ps_arr) - 1):
    if ratios_arr[i] < 1.0 <= ratios_arr[i + 1]:
        # log-linear interp
        lp1, lp2 = np.log10(ps_arr[i]), np.log10(ps_arr[i + 1])
        r1, r2 = ratios_arr[i], ratios_arr[i + 1]
        crossing = 10 ** (lp1 + (1.0 - r1) * (lp2 - lp1) / (r2 - r1))
        break
print(f"Estimated pseudo-threshold (ratio crosses 1): p ≈ {crossing:.4f}" if crossing else "no crossing seen")

with open(EVID / "threshold_estimate.txt", "w") as fh:
    fh.write(f"Empirical pseudo-threshold (d=3 vs d=5, Stim uniform depol, MWPM):\n")
    fh.write(f"  p ≈ {crossing:.4f}\n" if crossing else "  no crossing observed in sweep\n")
    fh.write("Reference: surface-code threshold for circuit-level depol noise ~ 0.5-1% (published).\n")

print("Wrote plots to", EVID)
