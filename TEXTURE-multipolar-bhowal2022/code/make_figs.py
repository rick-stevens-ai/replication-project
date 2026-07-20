#!/usr/bin/env python3
"""Generate comparison figures for the replication report."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import tb_mnf2 as m

a = m.a
kmax = np.pi / a

# --- Fig A: spin splitting along (0.5,-0.5,0)->G->(0.5,0.5,0), reproducing Fig 3(d) ---
# path: from M'(kx=ky=-... actually (0.5,-0.5)) to Gamma to M(0.5,0.5)
fs = np.linspace(-1, 1, 401)
exact = []
approx = []
full8 = []
for f in fs:
    kx = f * kmax
    ky = f * kmax   # along [110]/[1-10] handled by sign of f through both
    # Fig3d x-axis: (0.5,-0.5,0) -> G -> (0.5,0.5,0). Represent left half as (kx,-ky).
    if f < 0:
        kxx, kyy = abs(f) * kmax, -abs(f) * kmax
    else:
        kxx, kyy = f * kmax, f * kmax
    exact.append(m.spin_split_eq6_exact(kxx, kyy, 0.0) * 1000)
    approx.append(m.spin_split_eq6_approx(kxx, kyy, 0.0) * 1000)
    f8 = m.spin_split_full8(kxx, kyy, 0.0) * 1000
    # sign: full8 returns |split|; assign sign from exact
    full8.append(np.sign(exact[-1]) * f8)

fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ax[0].plot(fs, exact, "b-", lw=2, label="Eq.(6) exact = full 8x8 diag")
ax[0].plot(fs, approx, "r--", lw=1.5, label=r"Eq.(6) approx $\frac{32}{\epsilon}t_3t_4\sin(k_xa)\sin(k_ya)$")
ax[0].plot(fs[::12], full8[::12], "g.", ms=7, label="full 8x8 diag (pts)")
ax[0].axhline(0, color="k", lw=0.5)
ax[0].axvline(0, color="k", lw=0.5)
ax[0].set_xlabel(r"k along (0.5,-0.5,0) $\leftarrow\Gamma\rightarrow$ (0.5,0.5,0)")
ax[0].set_ylabel(r"$\Delta E_s$ (meV)")
ax[0].set_title("Reproduction of Fig. 3(d): d-wave spin splitting")
ax[0].legend(fontsize=8)

# --- Fig B: 2D d-wave map in kz=0 plane ---
kg = np.linspace(-kmax, kmax, 201)
KX, KY = np.meshgrid(kg, kg)
Z = np.vectorize(lambda x, y: m.spin_split_eq6_exact(x, y, 0.0) * 1000)(KX, KY)
im = ax[1].pcolormesh(KX / kmax, KY / kmax, Z, cmap="RdBu_r", shading="auto",
                      vmin=-np.max(np.abs(Z)), vmax=np.max(np.abs(Z)))
ax[1].set_xlabel(r"$k_x\, a/\pi$")
ax[1].set_ylabel(r"$k_y\, a/\pi$")
ax[1].set_title(r"$\Delta E_s(k_x,k_y)$ in $k_z=0$ plane (d-wave, $B_{1g}$)")
fig.colorbar(im, ax=ax[1], label="meV")
fig.tight_layout()
fig.savefig("../work/fig_spin_splitting.png", dpi=140)
print("wrote ../work/fig_spin_splitting.png")
print(f"peak |split| = {np.max(np.abs(exact)):.2f} meV")
