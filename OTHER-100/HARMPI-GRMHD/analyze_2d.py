#!/usr/bin/env python3
"""
analyze_2d.py — post-process HARMPI 2D Fishbone-Moncrief torus dumps.

Computes:
  - Mdot(t)  = -integral_{theta,phi} rho * u^r * sqrt(-g) dtheta dphi   at horizon
  - Phi_BH(t) = (1/2) integral_{theta,phi} |B^r| * sqrt(-g) dtheta dphi at horizon
  - <rho>_max(t), <bsq/2>_max(t)  diagnostic min/max

Writes:
  - mdot_phi.csv    time-series
  - mdot_phi.png    Mdot(t), Phi(t), Phi/sqrt(Mdot)
  - state_final.png panel of log10(rho), beta_inv, log10(bsq) at last dump

Run from /data/stevens/harmpi/harmpi/run_2d   (where dumps/ lives).
Requires harm_script.py on sys.path  (../harm_script.py).
"""
import os, sys, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# pull in HARMPI utilities
sys.path.insert(0, "..")
import harm_script as hs

def horizon_index(r_grid, rhor):
    """Return the i-index of the first cell with r >= rhor along axis 0."""
    # r_grid shape: (nx, ny, nz). Use j=0,k=0.
    r1d = r_grid[:, 0, 0]
    # find first i with r >= rhor (use the cell just outside horizon)
    idx = np.argmax(r1d >= rhor)
    return idx

def compute_mdot_phi(dump_name):
    """Read one dump, return (t, Mdot, Phi_BH, rho_max, bsq_max)."""
    hs.rd(dump_name)
    rho = hs.rho            # shape (nx,ny,nz)
    uu  = hs.uu             # shape (4,nx,ny,nz)
    bu  = hs.bu             # shape (4,nx,ny,nz)
    bsq = hs.bsq
    gdet = hs.gdet
    rhor = hs.rhor
    r = hs.r
    _dx2 = hs._dx2
    _dx3 = hs._dx3
    nz = rho.shape[2]
    # integration element in code units: dx2 * dx3 (per cell), gdet provides volume jacobian
    i_h = horizon_index(r, rhor)
    # Mdot through horizon (sign so accretion is positive)
    # integrand = rho * u^r * gdet ; integrate over j,k at fixed i=i_h
    integrand_m = (rho[i_h, :, :] * uu[1, i_h, :, :] * gdet[i_h, :, :])
    Mdot = - integrand_m.sum() * _dx2 * _dx3
    # Magnetic flux on horizon  Phi = 0.5 * integral |B^r| * gdet * dtheta dphi
    integrand_p = np.abs(bu[1, i_h, :, :]) * gdet[i_h, :, :]
    Phi = 0.5 * integrand_p.sum() * _dx2 * _dx3
    return hs.t, Mdot, Phi, float(rho.max()), float(bsq.max()), i_h

def main():
    if not os.path.isdir("dumps"):
        sys.exit("run from a directory containing dumps/ subdir")
    # read grid first
    print("Reading gdump...")
    hs.rg("gdump")
    a = hs.a
    rhor = 1.0 + (1.0 - a*a)**0.5
    hs.rhor = rhor
    print(f"  a = {a:.4g},  rhor = {rhor:.4g}")
    print(f"  N1={hs.N1}, N2={hs.N2}, N3={hs.N3}")
    dumps = sorted(glob.glob("dumps/dump[0-9][0-9][0-9]"))
    if not dumps:
        sys.exit("no dump### files found")
    print(f"Found {len(dumps)} dumps")
    rows = []
    for d in dumps:
        name = os.path.basename(d)
        try:
            t, mdot, phi, rmax, bmax, ih = compute_mdot_phi(name)
            rows.append((t, mdot, phi, rmax, bmax))
            print(f"  {name}  t={t:8.2f}  Mdot={mdot:+.4e}  Phi={phi:.4e}  ih={ih}  rho_max={rmax:.3e}  bsq_max={bmax:.3e}")
        except Exception as e:
            print(f"  FAILED on {name}: {e}")
    rows = np.array(rows)
    np.savetxt("mdot_phi.csv", rows,
               header="t Mdot Phi_BH rho_max bsq_max", comments="")
    # Plot time-series
    t, mdot, phi, _, _ = rows.T
    fig, axs = plt.subplots(3, 1, figsize=(8,9), sharex=True)
    axs[0].plot(t, mdot, lw=1.2)
    axs[0].set_ylabel(r"$\dot M$  (code units)")
    axs[0].axhline(0, color="k", lw=0.4)
    axs[0].set_title("HARMPI 2D Fishbone-Moncrief torus, a=0.9")
    axs[1].plot(t, phi, lw=1.2, color="C1")
    axs[1].set_ylabel(r"$\Phi_{\rm BH}$  (code units)")
    # MAD-normalized flux ~ Phi / sqrt(|Mdot|*r_g^2*c) ; in code units rhor and c=1
    with np.errstate(divide="ignore", invalid="ignore"):
        phi_norm = phi / np.sqrt(np.abs(mdot) + 1e-30)
    axs[2].plot(t, phi_norm, lw=1.2, color="C2")
    axs[2].set_ylabel(r"$\Phi_{\rm BH}/\sqrt{|\dot M|}$ (MAD param.)")
    axs[2].axhline(15.0, color="r", ls="--", lw=0.7, label="MAD threshold ~15")
    axs[2].legend(loc="best")
    axs[2].set_xlabel(r"$t/M$")
    for ax in axs:
        ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("mdot_phi.png", dpi=140)
    print("Wrote mdot_phi.png and mdot_phi.csv")
    # Final-state snapshot
    final_dump = os.path.basename(dumps[-1])
    print(f"Reading final dump {final_dump} for snapshot...")
    hs.rd(final_dump)
    lrho = np.log10(np.maximum(hs.rho, 1e-20))
    bsq = hs.bsq
    lbsq = np.log10(np.maximum(bsq, 1e-30))
    beta_inv = bsq / (2.0 * (hs.gam-1.0) * np.maximum(hs.ug, 1e-20))
    # 2D run: take k=0 slice; convert r, theta to cylindrical (x, z)
    r2 = hs.r[:,:,0]
    h2 = hs.h[:,:,0]
    x = r2 * np.sin(h2)
    z = r2 * np.cos(h2)
    fig, axs = plt.subplots(1, 3, figsize=(15, 6))
    titles = [r"$\log_{10}\rho$", r"$\log_{10}(b^2)$", r"$2 p_g / b^2 \;(1/\beta_{\rm gas})$"]
    fields = [lrho[:,:,0], lbsq[:,:,0], beta_inv[:,:,0]]
    cmaps = ["inferno", "viridis", "plasma"]
    for ax, f, ttl, cm in zip(axs, fields, titles, cmaps):
        # show only inner ~40 r_g for clarity
        mask = r2 < 40.0
        im = ax.pcolormesh(x, z, np.where(mask, f, np.nan), cmap=cm, shading="auto")
        # mirror across z-axis for visual symmetry
        ax.pcolormesh(-x, z, np.where(mask, f, np.nan), cmap=cm, shading="auto")
        ax.set_xlim(-30, 30); ax.set_ylim(-30, 30)
        ax.set_aspect("equal")
        ax.set_title(ttl + f"  (t={hs.t:.1f} M)")
        ax.set_xlabel("x  [r_g]")
        ax.set_ylabel("z  [r_g]")
        # black hole horizon
        th = np.linspace(0, 2*np.pi, 100)
        ax.fill(rhor*np.cos(th), rhor*np.sin(th), color="black", zorder=10)
        plt.colorbar(im, ax=ax, shrink=0.7)
    plt.tight_layout()
    plt.savefig("state_final.png", dpi=140)
    print("Wrote state_final.png")

if __name__ == "__main__":
    main()
