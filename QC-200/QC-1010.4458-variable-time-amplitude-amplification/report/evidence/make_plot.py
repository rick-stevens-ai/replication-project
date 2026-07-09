#!/usr/bin/env python3
"""Plot Q_standard vs Q_variable in the HHL regime."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = Path(__file__).resolve().parent
data = json.loads((here / "vtaa_core_combined.json").read_text())
hhl_rows = data["HHL"]["rows"]
toy_rows = data["toy"]["rows"]

fig, axes = plt.subplots(1, 2, figsize=(11, 5))

for ax, rows, title in [
    (axes[0], toy_rows, "toy regime  (p_succ ~ O(1))"),
    (axes[1], hhl_rows, "HHL regime  (p_succ ~ 1/kappa)"),
]:
    kappas = [r["kappa"] for r in rows]
    ax.loglog(kappas, [r["Q_standard"] for r in rows], "o-",
              label="standard AA  ~ T_max/sqrt(p_succ)")
    ax.loglog(kappas, [r["Q_variable"] for r in rows], "s-",
              label="VTAA (Ambainis Thm 1)")
    ax.loglog(kappas, kappas, "k:", label="reference ~ kappa")
    ax.loglog(kappas, [k * k**0.5 for k in kappas], "k--",
              label="reference ~ kappa^1.5")
    ax.set_xlabel("kappa")
    ax.set_ylabel("query-count proxy")
    ax.set_title(title)
    ax.legend(fontsize=8)
    ax.grid(True, which="both", alpha=0.3)

fig.suptitle("Ambainis 1010.4458 -- VTAA vs standard AA (Qiskit statevector, real amplitudes)")
fig.tight_layout()
out = here / "vtaa_vs_standard.png"
fig.savefig(out, dpi=140)
print("wrote", out)
