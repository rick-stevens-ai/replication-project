#!/usr/bin/env python3
"""Generate replication figures from work/results.json (matplotlib, Agg)."""
import os, sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))
work = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "work")
with open(os.path.join(work, "results.json")) as f:
    R = json.load(f)

fig, ax = plt.subplots(1, 2, figsize=(10, 4))

# --- C3: transition sweep (mirror of Fig 1c) ---
sw = R["C3_transition_sweep"]["sweep"]
gy = [r["gy"] for r in sw]
Q = [abs(((r["Q"] + 0.5) % 1.0) - 0.5) for r in sw]  # |Q| folded
mag = [r["absU"] for r in sw]
ax[0].plot(gy, Q, "o-", label=r"$|Q_{xy}|$ (ref.)", color="C0")
ax[0].axvline(1.0, ls="--", color="gray", lw=1)
ax[0].set_xlabel(r"$\gamma_y$  ($\gamma_x=0.5,\ \lambda=1,\ \delta=0$)")
ax[0].set_ylabel(r"$|Q_{xy}| = |{\rm Im}\ln\langle \hat U_2\rangle|/2\pi$")
ax[0].set_title("C3: sharp quadrupole transition at $\\gamma_y=1$")
ax[0].set_ylim(-0.05, 0.55)
ax[0].legend()

# --- C5: Thouless pump (mirror of Fig 2a) ---
pump = R["C5_thouless_pump"]["pump"]
th = [r["theta"] for r in pump]
Qp = [((r["Q"] + 0.5) % 1.0) - 0.5 for r in pump]
ax[1].plot(th, Qp, "s-", color="C3", label=r"${\rm Im}\ln\langle\hat U_2\rangle/2\pi$")
for t in [np.pi/2, 3*np.pi/2]:
    ax[1].axvline(t, ls=":", color="gray", lw=1)
ax[1].set_xlabel(r"$\theta$ (isotropic Thouless pump, Eq. 9)")
ax[1].set_ylabel(r"$Q_{xy}$")
ax[1].set_title("C5: pump; quantized at $\\delta=0$ ($\\theta=\\pi/2,3\\pi/2$)")
ax[1].legend()

fig.tight_layout()
out = os.path.join(work, "replication_figures.png")
fig.savefig(out, dpi=140)
print("wrote", out)
