"""Reproduce Fig. 4.1: numerical convergence of MFMT hard-sphere chemical
potential with uniform ionic density c(x) = 1, parameters
(eps, q, a) = (0.2, 0.3, 0.15).
"""
from __future__ import annotations
import json
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from mpnp import Geometry, mu_hs_mfmt, mu_hs_bulk


def main(outdir):
    a = 0.15
    # Reference: analytic bulk mu_HS for c=1 (both species), equal-size
    mu_bulk = mu_hs_bulk(1.0, a)
    print(f"Analytic bulk mu_HS (CS, equal size, c=1) = {mu_bulk:.6f}")

    Ns = [50, 100, 200, 400, 800, 1600]
    errs_center = []
    profiles = {}
    for N in Ns:
        geom = Geometry(a=a, N=N)
        x, h = geom.grids()
        c_total = np.ones_like(x) * 2.0  # rho_total = c+ + c- = 2 for c0=1
        mu = mu_hs_mfmt(c_total, x, a)
        # Center value
        center_idx = np.argmin(np.abs(x))
        err = abs(mu[center_idx] - mu_bulk)
        errs_center.append(err)
        profiles[N] = (x.copy(), mu.copy())
        print(f"  N={N:5d}  h={h:.4e}  mu(0)={mu[center_idx]:.6f}  err={err:.3e}")

    # Save results
    np.savez(os.path.join(outdir, "fig41_data.npz"),
             Ns=np.array(Ns), errs=np.array(errs_center),
             mu_bulk=mu_bulk, a=a)
    with open(os.path.join(outdir, "fig41_summary.json"), "w") as f:
        json.dump({
            "Ns": Ns,
            "errs_center": errs_center,
            "mu_bulk_analytic": float(mu_bulk),
            "a": a,
            "note": "errs are |mu_hs(x=0) - mu_bulk_CS|; mu_bulk is the "
                    "Carnahan-Starling single-component result for equal-size "
                    "binary at packing fraction (8/3)*pi*a^3",
        }, f, indent=2)

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    for N in (100, 400, 1600):
        x, mu = profiles[N]
        ax1.plot(x, mu, label=f"N={N}")
    ax1.axhline(mu_bulk, color="k", ls="--", lw=1.0, label="bulk CS")
    ax1.set_xlabel("x")
    ax1.set_ylabel(r"$\mu^{hs}(x)$ at $c\equiv 1$")
    ax1.set_title("(a) MFMT HS chemical potential, uniform density")
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)

    h_arr = 2.0 * (1.0 - a) / np.array(Ns)
    ax2.loglog(np.array(Ns), errs_center, "o-", label="|error at x=0|")
    # Reference slopes
    ax2.loglog(np.array(Ns),
               errs_center[0] * (np.array(Ns) / Ns[0]) ** (-2.0),
               "k--", lw=1, label=r"$O(N^{-2})$")
    ax2.loglog(np.array(Ns),
               errs_center[0] * (np.array(Ns) / Ns[0]) ** (-1.0),
               "k:", lw=1, label=r"$O(N^{-1})$")
    ax2.set_xlabel("N")
    ax2.set_ylabel("error")
    ax2.set_title("(b) Convergence vs. N")
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3, which="both")

    fig.suptitle("Fig. 4.1 replication: MFMT hard-sphere convergence (a=0.15)")
    fig.tight_layout()
    out = os.path.join(outdir, "fig41_hs_convergence.png")
    fig.savefig(out, dpi=140)
    print(f"Saved {out}")


if __name__ == "__main__":
    outdir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          "..", "figures"))
    os.makedirs(outdir, exist_ok=True)
    main(outdir)
