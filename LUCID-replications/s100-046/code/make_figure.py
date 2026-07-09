"""Generate Figure: model-predicted X-ray survival curves for V79 and Normal
human, on a semi-log plot. Counterpart to McMahon 2017 Fig. 7."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from medras_xray import (V79_HAMSTER, NORMAL_HUMAN, survival_xray,
                          nuclear_radius_um, E_DSB_KEV, SIGMA_FRAC, Y_DSB)

dose = np.linspace(0, 10, 41)
out_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(out_dir, exist_ok=True)

fig, ax = plt.subplots(figsize=(6, 4.5))
colors = {"V79 (Chinese hamster)": "tab:blue",
          "Normal human fibroblast": "tab:red"}
for cell in (V79_HAMSTER, NORMAL_HUMAN):
    res = survival_xray(cell, dose, n_samples=200_000)
    S = np.array(res["S"])
    label = f"{cell.name}: α={res['alpha']:.2f}, β={res['beta']:.3f}, MID={res['MID']:.2f} Gy"
    ax.semilogy(dose, S, "o-", color=colors[cell.name], ms=4, lw=1.4, label=label)

ax.set_xlabel("Dose (Gy)")
ax.set_ylabel("Surviving fraction S(D)")
ax.set_title("Reproduction of McMahon 2017 mechanistic model — X-ray\n"
             f"(E_DSB={E_DSB_KEV} keV → r_nuc={nuclear_radius_um(E_DSB_KEV):.2f} μm, "
             f"σ={SIGMA_FRAC}·R_nuc)")
ax.set_ylim(1e-4, 2)
ax.set_xlim(0, 10)
ax.grid(True, which="both", alpha=0.3)
ax.legend(loc="lower left", fontsize=8)
plt.tight_layout()
out_path = os.path.join(out_dir, "fig_xray_survival_reproduction.png")
plt.savefig(out_path, dpi=140)
print("Wrote:", out_path)
