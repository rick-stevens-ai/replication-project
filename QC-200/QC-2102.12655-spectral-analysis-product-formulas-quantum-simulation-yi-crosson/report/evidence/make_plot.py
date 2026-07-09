#!/usr/bin/env python3
"""Log-log plot of Trotter error vs dt for S1/S2/S4, plus state-infidelity panel."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "trotter_scaling.json").read_text())

fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))

for ax, kind, title in (
    (axes[0], "op_err", r"Operator-norm error $\|U_{ex}-U_{approx}\|_2$"),
    (axes[1], "infid",  r"State infidelity $1-|\langle\psi_{ex}|\psi_{ap}\rangle|^2$ (from H ground state)"),
):
    for nkey, res in data["results_by_n"].items():
        n = res["n"]
        dts = [r["dt"] for r in res["rows"]]
        for order, marker in (("S1", "o"), ("S2", "s"), ("S4", "^")):
            errs = [r[f"{kind}_{order}"] for r in res["rows"]]
            ax.loglog(dts, errs, marker=marker,
                      label=f"n={n} {order}")
    ax.set_xlabel(r"Trotter step $\delta t$")
    ax.set_ylabel(kind)
    ax.set_title(title)
    ax.grid(True, which="both", ls=":")
    ax.legend(fontsize=8, ncol=2)

fig.suptitle("Independent replication — arXiv:2102.12655 (Yi & Crosson 2021)\n"
             "TFIM n∈{4,6}, J=h=1, t=1; expected slopes: S1=1, S2=2, S4=4 in op-norm")
fig.tight_layout()
out = HERE / "trotter_scaling.png"
fig.savefig(out, dpi=140)
print("wrote", out)
