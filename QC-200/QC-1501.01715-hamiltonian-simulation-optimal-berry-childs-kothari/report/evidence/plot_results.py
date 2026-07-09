#!/usr/bin/env python3
"""Plot convergence + scaling from results.json."""
import json, math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = Path(__file__).parent
res = json.loads((D / "results.json").read_text())

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# --- (a) convergence
A = res["experiment_A_convergence"]
ks = [r["k"] for r in A]
errs = [r["op_error"] for r in A]
ax = axes[0]
ax.semilogy(ks, errs, "o-", label="||V_k - e^{-iHt}||_2")
ax.axhline(1e-3, ls="--", color="grey", label="ε = 1e-3 target")
ax.set_xlabel("truncation k")
ax.set_ylabel("spectral-norm error")
ax.set_title("(a) LCU/Bessel truncation error vs k\n(XY 4-qubit, t=1)")
ax.grid(True, which="both", alpha=0.3)
ax.legend()

# --- (b) k(eps) vs paper prediction
B = [r for r in res["experiment_B_scaling"] if r.get("k_needed") is not None]
eps = np.array([r["eps"] for r in B])
kneeded = np.array([r["k_needed"] for r in B])
pred = np.array([r["log_over_loglog"] for r in B])
ax = axes[1]
ax.semilogx(eps, kneeded, "o-", label="k needed (numerics)")
# Fit a proportionality constant
c = float(np.median(kneeded / pred))
ax.semilogx(eps, c * pred, "--", label=f"paper Thm 1: k ≈ {c:.2f} · log(1/ε)/loglog(1/ε)")
ax.invert_xaxis()
ax.set_xlabel("target ε")
ax.set_ylabel("k required for ||·||_2 ≤ ε")
ax.set_title("(b) BCK query-scaling matches Theorem 1\nk = O(log(1/ε)/loglog(1/ε))")
ax.grid(True, which="both", alpha=0.3)
ax.legend()

fig.tight_layout()
out = D / "convergence.png"
fig.savefig(out, dpi=140)
print(f"Wrote {out}")
