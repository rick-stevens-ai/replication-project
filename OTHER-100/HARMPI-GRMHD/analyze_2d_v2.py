#!/usr/bin/env python3
"""
analyze_2d_v2.py — extra plots: log Mdot, multi-time snapshot grid.
Run after analyze_2d.py.
"""
import os, sys, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, "..")
import harm_script as hs

def main():
    d = np.loadtxt("mdot_phi.csv", skiprows=1)
    t, mdot, phi, rmax, bmax = d.T
    # 1) log-scale Mdot showing MRI growth + saturation
    fig, axs = plt.subplots(2, 1, figsize=(8, 6.5), sharex=True)
    axs[0].semilogy(t, np.abs(mdot), lw=1.2)
    axs[0].set_ylabel(r"$|\dot M|$  (code units)")
    axs[0].grid(alpha=0.3, which="both")
    axs[0].set_title("HARMPI 2D Fishbone-Moncrief torus, a=0.9 — accretion through horizon")
    axs[0].axvspan(0, 100, alpha=0.15, color="C0", label="laminar")
    axs[0].axvspan(100, 400, alpha=0.15, color="C1", label="MRI linear growth")
    axs[0].axvspan(400, 1000, alpha=0.15, color="C2", label="transition")
    axs[0].axvspan(1000, 2000, alpha=0.15, color="C3", label="quasi-steady")
    axs[0].legend(loc="lower right", fontsize=8, ncol=2)
    axs[1].semilogy(t, bmax, lw=1.2, color="C1")
    axs[1].set_ylabel(r"$\max(b^2)$  (code units)")
    axs[1].set_xlabel(r"$t/M$")
    axs[1].grid(alpha=0.3, which="both")
    axs[1].set_title("Max magnetic energy density — MRI amplification")
    plt.tight_layout()
    plt.savefig("mdot_logscale.png", dpi=140)
    print("Wrote mdot_logscale.png")

    # 2) snapshot grid at multiple times
    print("Reading gdump...")
    hs.rg("gdump")
    a = hs.a
    rhor = 1.0 + (1.0 - a*a)**0.5
    hs.rhor = rhor
    snap_dumps = ["dump000", "dump020", "dump050", "dump100", "dump150", "dump200"]
    snap_dumps = [d for d in snap_dumps if os.path.isfile("dumps/" + d)]
    fig, axs = plt.subplots(2, len(snap_dumps), figsize=(3.0*len(snap_dumps), 6.5))
    for col, name in enumerate(snap_dumps):
        hs.rd(name)
        lrho = np.log10(np.maximum(hs.rho, 1e-20))
        lbsq = np.log10(np.maximum(hs.bsq, 1e-30))
        r2 = hs.r[:,:,0]; h2 = hs.h[:,:,0]
        x = r2 * np.sin(h2); z = r2 * np.cos(h2)
        for row, (field, ttl, cm, vmin, vmax) in enumerate([
            (lrho[:,:,0], r"$\log_{10}\rho$", "inferno", -6, 0),
            (lbsq[:,:,0], r"$\log_{10} b^2$", "viridis", -6, 0),
        ]):
            ax = axs[row, col]
            mask = r2 < 30.0
            ax.pcolormesh(x, z, np.where(mask, field, np.nan), cmap=cm,
                          shading="auto", vmin=vmin, vmax=vmax)
            ax.pcolormesh(-x, z, np.where(mask, field, np.nan), cmap=cm,
                          shading="auto", vmin=vmin, vmax=vmax)
            ax.set_xlim(-25, 25); ax.set_ylim(-25, 25); ax.set_aspect("equal")
            th = np.linspace(0, 2*np.pi, 100)
            ax.fill(rhor*np.cos(th), rhor*np.sin(th), color="black", zorder=10)
            if row == 0:
                ax.set_title(f"t = {hs.t:.0f} M\n{ttl}", fontsize=10)
            else:
                ax.set_title(ttl, fontsize=10)
            if col == 0:
                ax.set_ylabel("z [r_g]")
            ax.set_xticks([]); ax.set_yticks([])
    plt.tight_layout()
    plt.savefig("snapshot_grid.png", dpi=130)
    print("Wrote snapshot_grid.png")

if __name__ == "__main__":
    main()
