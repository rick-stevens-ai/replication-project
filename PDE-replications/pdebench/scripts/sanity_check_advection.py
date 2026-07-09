"""Sanity check: the 1D linear advection eq u_t + beta*u_x = 0 on periodic [0,1]
has exact solution u(x, t) = u0(x - beta*t). Compare PDEBench-generated solution
to this analytic shift at multiple times and compute L2 error.
"""
from __future__ import annotations
from pathlib import Path

import h5py
import numpy as np
import matplotlib.pyplot as plt


SRC = Path(__file__).resolve().parents[1] / "data" / "1D_Advection_Sols_beta1.0.hdf5"
FIG = Path(__file__).resolve().parents[1] / "figures"
RES = Path(__file__).resolve().parents[1] / "results"
BETA = 1.0


def main() -> None:
    with h5py.File(SRC, "r") as f:
        u = f["tensor"][:]
        x = f["x-coordinate"][:]
        t = f["t-coordinate"][:]
    print("shapes:", u.shape, x.shape, t.shape)

    # Build exact reference from each initial condition u[:, 0, :] shifted by beta*t.
    u0 = u[:, 0, :]                       # (b, nx)
    nx = x.size
    dx = x[1] - x[0]

    # Periodic shift via spectral interpolation (FFT) is exact for any beta*t
    k = 2.0 * np.pi * np.fft.fftfreq(nx, d=dx)  # (nx,)
    U0 = np.fft.fft(u0, axis=-1)               # (b, nx)

    err_rel = np.zeros_like(t)
    for it, tt in enumerate(t):
        # Shift by -beta*tt  =>  multiply spectrum by exp(-i*k*beta*tt)
        Uref = U0 * np.exp(-1j * k * BETA * tt)
        u_ref = np.real(np.fft.ifft(Uref, axis=-1))
        diff = u[:, it, :] - u_ref
        l2_diff = np.sqrt(np.mean(diff ** 2))
        l2_norm = np.sqrt(np.mean(u_ref ** 2))
        err_rel[it] = l2_diff / max(l2_norm, 1e-12)

    print(f"relative L2 error  t=0 -> {err_rel[0]:.3e}")
    print(f"relative L2 error  t={t[-1]:.2f} -> {err_rel[-1]:.3e}")
    print(f"max relative L2 error over time = {err_rel.max():.3e}")

    FIG.mkdir(parents=True, exist_ok=True)
    RES.mkdir(parents=True, exist_ok=True)
    np.save(RES / "sanity_relL2_vs_t.npy", np.stack([t, err_rel], axis=0))

    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    # error curve
    ax[0].plot(t, err_rel)
    ax[0].set_xlabel("t"); ax[0].set_ylabel("relative L2 error vs exact shift")
    ax[0].set_title("PDEBench 1D advection β=1.0 vs analytic shift\n(small subset, nx=256)")
    ax[0].grid(alpha=0.3)
    # snapshot comparison sample 0
    ax[1].plot(x, u[0, 0, :], label="t=0 (IC)", alpha=0.7)
    ax[1].plot(x, u[0, len(t)//2, :], label=f"t={t[len(t)//2]:.2f} (numerical)")
    ax[1].plot(x, u[0, -1, :], label=f"t={t[-1]:.2f} (numerical)")
    # analytic at final time
    U0_one = np.fft.fft(u[0, 0, :])
    u_exact = np.real(np.fft.ifft(U0_one * np.exp(-1j * k * BETA * t[-1])))
    ax[1].plot(x, u_exact, "--", label=f"t={t[-1]:.2f} (exact shift)", alpha=0.8)
    ax[1].set_xlabel("x"); ax[1].set_ylabel("u")
    ax[1].set_title("Sample trajectory, batch 0")
    ax[1].legend(fontsize=8); ax[1].grid(alpha=0.3)
    fig.tight_layout()
    out = FIG / "sanity_advection.png"
    fig.savefig(out, dpi=120)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
