#!/usr/bin/env python3
"""Plot log-log RMSE(a) vs N_q for MLE-AE and classical sampling.
Also fit the power-law exponent for MLE-AE (excluding T=0) and classical."""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

if len(sys.argv) < 3:
    print("usage: plot_scaling.py <input.json> <output.png>", file=sys.stderr)
    sys.exit(2)

data = json.loads(Path(sys.argv[1]).read_text())

mle = data["rmse_vs_Tmax"]
cls = data["rmse_classical_vs_Nshot"]

mle_N = np.array(sorted([v["N_q"] for v in mle.values()]))
mle_R = np.array([mle[k]["rmse_a"] for k in sorted(mle, key=lambda x: mle[x]["N_q"])])
cls_N = np.array(sorted([v["N_q"] for v in cls.values()]))
cls_R = np.array([cls[k]["rmse_a"] for k in sorted(cls, key=lambda x: cls[x]["N_q"])])

# Log-log fits
def loglog_fit(N, R, mask=None):
    N = np.asarray(N, dtype=float); R = np.asarray(R, dtype=float)
    if mask is not None:
        N = N[mask]; R = R[mask]
    lN = np.log(N); lR = np.log(R)
    slope, intercept = np.polyfit(lN, lR, 1)
    return slope, intercept

# MLE: skip T=0 (that's just classical baseline)
mle_slope, mle_int = loglog_fit(mle_N[1:], mle_R[1:])
cls_slope, cls_int = loglog_fit(cls_N, cls_R)

print(f"MLE-AE log-log slope (T>=1): {mle_slope:.3f}  (Heisenberg: -1.0)")
print(f"Classical log-log slope    : {cls_slope:.3f}  (shot-noise: -0.5)")
print(f"MLE RMSE at max N_q ({mle_N[-1]}): {mle_R[-1]:.5f}  (paper claim: < 0.02)")

fig, ax = plt.subplots(figsize=(7, 5.5))
ax.loglog(mle_N, mle_R, "o-", color="C1", label=f"MLE-AE (slope={mle_slope:.2f})", ms=8, lw=2)
ax.loglog(cls_N, cls_R, "^--", color="C0", label=f"Classical sampling (slope={cls_slope:.2f})", ms=8, lw=2)

# Reference lines
Nref = np.logspace(np.log10(mle_N.min()), np.log10(mle_N.max()), 50)
# Heisenberg 1/N_q pinned to MLE T=1 point
ax.loglog(Nref, mle_R[1] * (mle_N[1]/Nref)**1.0, ":", color="C1", alpha=0.5,
          label="Heisenberg $1/N_q$")
# Shot-noise 1/sqrt(N_q) pinned to classical N=500 point
ax.loglog(Nref, cls_R[0] * (cls_N[0]/Nref)**0.5, ":", color="C0", alpha=0.5,
          label=r"Shot-noise $1/\sqrt{N_q}$")

ax.axhline(0.02, color="gray", linestyle="-.", alpha=0.6, label="Paper claim (< 0.02)")
ax.set_xlabel("Total oracle calls $N_q$")
ax.set_ylabel("RMSE of $\\hat a$")
ax.set_title("MLE-AE vs classical sampling (noiseless Qiskit-Aer, a=0.3, 25 trials)\n"
             "Replication of Giurgica-Tiron et al., arXiv:2109.09685 Fig. 5 (noiseless kernel)")
ax.legend(loc="lower left", fontsize=9)
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(sys.argv[2], dpi=140)
print(f"[plot] wrote {sys.argv[2]}")

# Also write the numeric fits
summary = {
    "mle_loglog_slope_T_ge_1": float(mle_slope),
    "classical_loglog_slope": float(cls_slope),
    "mle_rmse_at_max_Nq": float(mle_R[-1]),
    "mle_max_Nq": int(mle_N[-1]),
    "classical_rmse_at_max_Nq": float(cls_R[-1]),
    "paper_headline_threshold": 0.02,
    "mle_passes_paper_threshold": bool(mle_R[-1] < 0.02),
    "mle_beats_classical_at_max_Nq": bool(mle_R[-1] < cls_R[-1]),
    "slope_ratio_mle_over_classical": float(mle_slope / cls_slope) if cls_slope != 0 else None,
}
summary_path = Path(sys.argv[2]).with_suffix(".summary.json")
summary_path.write_text(json.dumps(summary, indent=2))
print(f"[summary] wrote {summary_path}")
print(json.dumps(summary, indent=2))
