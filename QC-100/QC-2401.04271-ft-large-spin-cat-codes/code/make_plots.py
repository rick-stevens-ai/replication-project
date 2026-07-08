#!/usr/bin/env python3
"""Generate summary plots from spin_cat_results.json."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent.parent
EV = HERE / "report" / "evidence"

with (EV / "spin_cat_results.json").open() as f:
    R = json.load(f)

thetas = np.asarray(R["thetas"])
Js_labels = ["J=0.5(d=2)", "J=1.5(d=4)", "J=2.5(d=6)", "J=3.5(d=8)", "J=4.5(d=10)"]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

ax = axes[0]
for lab in Js_labels:
    p = [x["p_flip"] for x in R["bitflip_coherent"][lab]]
    # avoid log(0)
    p_arr = np.asarray(p)
    p_arr = np.where(p_arr < 1e-300, 1e-300, p_arr)
    ax.semilogy(thetas, p_arr, marker="o", ms=3, label=lab)
ax.set_xlabel(r"noise angle $\theta$ [rad]")
ax.set_ylabel(r"P(bit flip) = $|\langle 1_L | e^{-i\theta J_x} | 0_L \rangle|^2$")
ax.set_title(r"Bit-flip probability under $U_X(\theta)$: exponentially suppressed in $J$")
ax.set_ylim(1e-32, 2.0)
ax.grid(alpha=0.3)
ax.legend(loc="lower right", fontsize=8)

ax = axes[1]
for lab in Js_labels:
    p = [x["p_flip"] for x in R["phaseflip_coherent"][lab]]
    ax.plot(thetas, p, marker="o", ms=3, label=lab)
ax.set_xlabel(r"noise angle $\theta$ [rad]")
ax.set_ylabel(r"P(cat phase flip) = $|\langle -_L | e^{-i\theta J_z} | +_L \rangle|^2$")
ax.set_title(r"Cat phase-flip under $U_Z(\theta)$: amplified $\propto J^2$")
ax.grid(alpha=0.3)
ax.legend(loc="upper left", fontsize=8)

fig.suptitle("arXiv:2401.04271 — bias-preservation of spin-cat encoding (small-instance verification)")
fig.tight_layout()
out = EV / "spin_cat_bias.png"
fig.savefig(out, dpi=140)
print("wrote", out)

# Second figure: dephasing channel comparison
fig, ax = plt.subplots(figsize=(7, 5))
gammas = np.asarray(R["gammas"])
for lab in Js_labels:
    p = [x["p_flip"] for x in R["bitflip_dephasing"][lab]]
    p_arr = np.asarray(p)
    p_arr = np.where(p_arr < 1e-300, 1e-300, p_arr)
    ax.loglog(gammas, p_arr, marker="o", ms=3, label=lab)
ax.set_xlabel(r"$J_x$ Lindblad rate $\gamma$ (t=1)")
ax.set_ylabel(r"P(bit flip) under $L=\sqrt{\gamma}J_x$ dephasing")
ax.set_title(r"Stochastic bit-flip under $J_x$ dephasing (arXiv:2401.04271 encoding)")
ax.grid(alpha=0.3, which="both")
ax.legend(loc="lower right", fontsize=8)
fig.tight_layout()
out2 = EV / "spin_cat_dephasing.png"
fig.savefig(out2, dpi=140)
print("wrote", out2)
