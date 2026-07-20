#!/usr/bin/env python3
"""Snapshot figure of the relaxed pure-vortex phase (Run A). Uses same field."""
import os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("r", os.path.join(HERE, "hong2025_runner.py"))
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

m = r.PolarVortexField(Nx=160, Nz=40, seed=1, a=-1.0, b=1.0, g=0.6, eps=4.0, Kz=0.8, film_frac=0.5)
for _ in range(12000): m.step(0.01)
Px, Pz = m.P[0], m.P[1]
w = m.winding_field()
FIGS = os.path.join(os.path.dirname(HERE), "figs"); os.makedirs(FIGS, exist_ok=True)

fig, ax = plt.subplots(2, 1, figsize=(9, 6))
s = 3
X, Z = np.meshgrid(np.arange(0, m.Nx, s), np.arange(0, m.Nz, s), indexing="ij")
im0 = ax[0].imshow(Pz.T, origin="lower", cmap="RdBu_r", aspect="auto",
                   vmin=-abs(Pz).max(), vmax=abs(Pz).max())
ax[0].quiver(X, Z, Px[::s, ::s], Pz[::s, ::s], color="k", scale=25, width=0.002)
ax[0].set_title("Relaxed polarization: pure vortex phase (Pz color + (Px,Pz) arrows)")
ax[0].set_xlabel("x (lateral)"); ax[0].set_ylabel("z (film normal)")
fig.colorbar(im0, ax=ax[0], label="Pz", shrink=0.8)
im1 = ax[1].imshow(w.T, origin="lower", cmap="PiYG", aspect="auto", vmin=-1, vmax=1)
ax[1].set_title("Winding number field (+1/-1 = alternating vortex cores)")
ax[1].set_xlabel("x"); ax[1].set_ylabel("z")
fig.colorbar(im1, ax=ax[1], label="winding", shrink=0.8)
fig.tight_layout()
fig.savefig(os.path.join(FIGS, "hong2025_vortex_phase.png"), dpi=130)
print("saved", os.path.join(FIGS, "hong2025_vortex_phase.png"))
