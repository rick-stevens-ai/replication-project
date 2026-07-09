"""Plot the epsilon vs cheat-probability trade-off curve."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader(open(HERE / "tradeoff_curve.csv")))
eps = np.array([float(r["epsilon_1_minus_F"]) for r in rows])
Pcheat = np.array([float(r["P_cheat_uhlmann"]) for r in rows])
theta = np.array([float(r["theta"]) for r in rows])

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
ax = axes[0]
ax.plot(eps, Pcheat, "o-", ms=4, lw=1.2, label="Uhlmann optimum")
ax.plot([0, 1], [1, 0], "k--", lw=0.7, label=r"$P_\mathrm{cheat}=1-\epsilon$ (reference)")
ax.set_xlabel(r"$\epsilon = 1 - F(\rho^B_0,\rho^B_1)$  (concealing imperfection)")
ax.set_ylabel(r"$P_\mathrm{cheat}$  (Alice's optimal cheating success)")
ax.set_title("Lo-Chau trade-off: perfect concealing $\\Rightarrow$ $P_\\mathrm{cheat}=1$")
ax.grid(alpha=0.3)
ax.legend(loc="best", fontsize=9)
ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02)

ax = axes[1]
one_minus = 1.0 - Pcheat
mask = eps > 0
ax.loglog(eps[mask], one_minus[mask], "o-", ms=4, lw=1.2,
          label=r"$1-P_\mathrm{cheat}$ (numerics)")
xs = np.logspace(-3, 0, 50)
ax.loglog(xs, xs, "k--", lw=0.7, label=r"$\epsilon$")
ax.loglog(xs, np.sqrt(xs), "r:", lw=0.9, label=r"$\sqrt{\epsilon}$ (paper's bound)")
ax.set_xlabel(r"$\epsilon$")
ax.set_ylabel(r"$1-P_\mathrm{cheat}$")
ax.set_title("Log-log: numerics tracks $1-P_\\mathrm{cheat}=\\epsilon$, well below $\\sqrt{\\epsilon}$")
ax.grid(alpha=0.3, which="both")
ax.legend(loc="best", fontsize=9)

fig.tight_layout()
fig.savefig(HERE / "tradeoff_curve.png", dpi=140)
print("Wrote", HERE / "tradeoff_curve.png")
