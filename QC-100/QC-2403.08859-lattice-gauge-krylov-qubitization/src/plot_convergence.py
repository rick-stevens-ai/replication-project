#!/usr/bin/env python3
"""Plot the Krylov-QSE convergence data produced by schwinger_krylov.py."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

here = Path(__file__).resolve().parent.parent
evdir = here / "report" / "evidence"
with open(evdir / "summary.json") as fh:
    data = json.load(fh)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: Lanczos-form convergence (numerically stable)
for case in data["cases"]:
    N = case["N"]
    Ds = [r["D"] for r in case["rows"]]
    frac = [max(r["frac_err_Lanczos"], 1e-16) for r in case["rows"]]
    axes[0].semilogy(Ds, frac, "o-", label=f"N={N}")
axes[0].axhline(1e-4, ls="--", c="grey",
                label=r"$\Delta E/E_{int}=10^{-4}$ (paper Fig 3)")
axes[0].set_xlabel("Krylov basis dimension D")
axes[0].set_ylabel(r"fractional energy error $|\Delta E| / E_{int}$")
axes[0].set_title("Krylov-QSE convergence (Lanczos, stable)\n"
                  r"Schwinger, $\mu=1.5$, $x=0.5$")
axes[0].legend()
axes[0].grid(True, which="both", alpha=0.3)

# Panel B: Hankel condition number (paper's ill-conditioning story)
for case in data["cases"]:
    N = case["N"]
    Ds = [r["D"] for r in case["rows"]]
    conds = [r["cond_S"] for r in case["rows"]]
    axes[1].semilogy(Ds, conds, "s-", label=f"N={N}")
axes[1].axhline(1e16, ls="--", c="red",
                label=r"double-precision limit $\sim 10^{16}$")
axes[1].set_xlabel("Krylov basis dimension D")
axes[1].set_ylabel(r"condition number $\kappa(S)$")
axes[1].set_title("Ill-conditioning of Hankel overlap matrix\n"
                  "(paper Sec. 4: QSE breaks down for large D)")
axes[1].legend()
axes[1].grid(True, which="both", alpha=0.3)

plt.tight_layout()
out = evdir / "convergence.png"
plt.savefig(out, dpi=120)
print(f"wrote {out}")
