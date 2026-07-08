"""Plot Var vs N (log-y), fit exponential, compare to Thm 3 prediction."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = Path(__file__).parent
data = json.loads((here / "../report/evidence/qmps_variance.json").read_text())

Ns = np.array([r["N"] for r in data["results"]])
vmc = np.array([r["grad_var"] for r in data["results"]])
vth = np.array([r["var_theory_thm3"] for r in data["results"]])

# fits
sl_mc, in_mc = np.polyfit(Ns, np.log(vmc), 1)
sl_th, in_th = np.polyfit(Ns, np.log(vth), 1)

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.semilogy(Ns, vmc, "o-", label="MC estimate (1000 samples)")
ax.semilogy(Ns, vth, "s--", label=r"Thm 3: $11\cdot(1/8)^2 \cdot (3/8)^{N-1}$")

# reference lines
Nref = np.linspace(Ns.min(), Ns.max(), 50)
ax.semilogy(Nref, np.exp(in_mc) * np.exp(sl_mc * Nref), ":",
            label=f"MC fit: b={np.exp(sl_mc):.3f}", alpha=0.7)
ax.semilogy(Nref, (0.5) ** Nref * np.exp(in_mc + sl_mc * Ns[0]) / (0.5 ** Ns[0]), "-.",
            label=r"unstructured $2^{-N}$ ref", alpha=0.4)

ax.set_xlabel("N (qubits)")
ax.set_ylabel(r"Var$[\partial_{1,1}\,\langle X_N\rangle_{qMPS}]$")
ax.set_title("Barren plateau in qMPS: gradient variance decays\n"
             "exponentially with qubit count (arXiv:2209.00292, Thm 3)")
ax.legend(loc="best", fontsize=9)
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
out = here / "../report/evidence/variance_vs_N.png"
fig.savefig(out, dpi=140)
print(f"wrote {out}")

# text summary
lines = []
lines.append("Reproduction of Cervero Martin+ 2023 barren-plateau claim")
lines.append("=" * 60)
lines.append(f"MC decay base b = {np.exp(sl_mc):.4f}")
lines.append(f"Thm 3 base b   = 0.3750  (= 3/8)")
lines.append(f"Ratio          = {np.exp(sl_mc)/0.375:.3f}")
lines.append("")
lines.append(f"{'N':>3} {'Var_MC':>14} {'Var_Thm3':>14} {'ratio':>8}")
for r in data["results"]:
    lines.append(f"{r['N']:>3} {r['grad_var']:>14.4e} "
                 f"{r['var_theory_thm3']:>14.4e} {r['ratio_mc_over_theory']:>8.3f}")
summary = "\n".join(lines)
print(summary)
(here / "../report/evidence/summary.txt").write_text(summary + "\n")
