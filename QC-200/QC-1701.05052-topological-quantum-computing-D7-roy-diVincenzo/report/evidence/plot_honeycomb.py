#!/usr/bin/env python3
"""Plot: Kitaev honeycomb phase diagram (gap vs coupling), for the report."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

# Sweep on the simplex Jx + Jy + Jz = 1  (paper Sec 2.2 phase diagram, Fig 3)
n = 240
gaps = np.zeros((n, n))
for i, jx in enumerate(np.linspace(0.001, 0.999, n)):
    for j, jy in enumerate(np.linspace(0.001, 0.999, n)):
        jz = 1.0 - jx - jy
        if jz < 0.001 or jz > 0.999:
            gaps[j, i] = np.nan
            continue
        # Exact analytic minimum of |Jx e^{ia} + Jy e^{ib} + Jz|
        s = sorted([abs(jx), abs(jy), abs(jz)])
        gap = max(0.0, s[2] - s[0] - s[1])
        gaps[j, i] = gap

fig, ax = plt.subplots(figsize=(6, 5.5))
im = ax.imshow(gaps, extent=[0, 1, 0, 1], origin="lower", cmap="viridis",
               vmin=0, vmax=0.5, aspect="equal")
ax.set_xlabel("$J_x$  (with $J_x+J_y+J_z=1$)")
ax.set_ylabel("$J_y$")
ax.set_title("Kitaev honeycomb spectral gap in the vortex-free sector\n"
             "Roy & DiVincenzo (arXiv:1701.05052), Eq. 11")
# Mark B phase interior
ax.plot([1/3], [1/3], "wo", markersize=8, markeredgecolor="black")
ax.annotate("B (isotropic, gapless)", xy=(1/3, 1/3), xytext=(0.42, 0.05),
            fontsize=9, color="white",
            arrowprops=dict(arrowstyle="->", color="white"))
ax.annotate("$A_x$ (gapped)", xy=(0.8, 0.1), color="white", fontsize=9)
ax.annotate("$A_y$ (gapped)", xy=(0.05, 0.8), color="white", fontsize=9)
ax.annotate("$A_z$ (gapped)", xy=(0.05, 0.05), color="white", fontsize=9)
cbar = plt.colorbar(im, ax=ax)
cbar.set_label(r"$\min_{q}\, |\epsilon(q)|$")
plt.tight_layout()
out = Path(__file__).parent.parent.parent / "figures" / "kitaev_phase_diagram.png"
out.parent.mkdir(exist_ok=True)
plt.savefig(out, dpi=140)
print(f"Wrote {out}")
