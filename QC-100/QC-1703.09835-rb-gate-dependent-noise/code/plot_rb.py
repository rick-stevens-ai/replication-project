#!/usr/bin/env python3
"""Plot RB decay curves for uniform vs gate-dependent noise."""
import json, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

path = sys.argv[1] if len(sys.argv) > 1 else "data/rb_prod2.json"
outpng = sys.argv[2] if len(sys.argv) > 2 else "report/evidence/rb_decay.png"

with open(path) as f:
    r = json.load(f)

m = np.array(r["uniform"]["m_list"])
uni_means = np.array(r["uniform"]["fit"]["means"])
uni_stds = np.array(r["uniform"]["fit"]["stds"])
gd_means = np.array(r["gate_dependent"]["fit"]["means"])
gd_stds = np.array(r["gate_dependent"]["fit"]["stds"])

uni_A = r["uniform"]["fit"]["A"]; uni_p = r["uniform"]["fit"]["p"]; uni_B = r["uniform"]["fit"]["B"]
gd_A = r["gate_dependent"]["fit"]["A"]; gd_p = r["gate_dependent"]["fit"]["p"]; gd_B = r["gate_dependent"]["fit"]["B"]

mm = np.linspace(0, max(m)*1.05, 200)

fig, ax = plt.subplots(1, 1, figsize=(7,5))
ax.errorbar(m, uni_means, yerr=uni_stds, fmt='o', color='C0', label=f'Uniform depol (r_target={r["uniform"]["r_target"]:.3f}, r_fit={r["uniform"]["r_fit"]:.4f})')
ax.plot(mm, uni_A*uni_p**mm + uni_B, '-', color='C0', alpha=0.6)
ax.errorbar(m, gd_means, yerr=gd_stds, fmt='s', color='C3', label=f'Gate-dep coherent (mean r_g={r["gate_dependent"]["r_mean_per_gate"]:.4f}, r_fit={r["gate_dependent"]["r_fit"]:.4f})')
ax.plot(mm, gd_A*gd_p**mm + gd_B, '-', color='C3', alpha=0.6)
ax.set_xscale('log')
ax.set_xlabel('sequence length m (Cliffords)')
ax.set_ylabel(r'survival probability $\langle 0|G^\dag_{inv}\cdots G_1|0\rangle^2$')
ax.set_title('Single-qubit RB: uniform depolarizing vs. gate-dependent coherent noise\n'
             '(reproducing Wallman 2017, arXiv:1703.09835)')
ax.legend(loc='best', fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(outpng, dpi=140)
print(f"wrote {outpng}")
