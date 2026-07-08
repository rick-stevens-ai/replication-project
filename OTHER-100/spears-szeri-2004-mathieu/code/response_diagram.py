"""
response_diagram.py
===================

Spears & Szeri (2004), Fig. 12 — z_inf vs ωf response diagram for
alpha=0.05, gamma=-0.10, mu=delta=chi=1, eps=1e-3.

Paper claim: there is a stable large-amplitude branch between two
topological-torus bifurcations near ωf ≈ 0.6375 and ωf ≈ 0.6405,
with two trivial (decay) branches outside.

Strategy
--------
For each ωf in a fine sweep, integrate Eq. (2) (rescaled form, see
simulate.py) for a long time starting from a finite-amplitude initial
condition (z0 = 1.0, zdot0 = 0).  Record the maximum |z| over the
last few periods after a generous transient cutoff.

Plot z_inf vs ωf and locate the lower / upper edges of the large-
amplitude branch by detecting where the branch amplitude drops below
a small fraction of its peak value.

Output:
    figures/fig12_response_diagram.png
    evidence/response_sweep.csv
    evidence/response_diagram.json

Run:  python3 response_diagram.py
"""
from __future__ import annotations

import json
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mathieu_beta import solve_beta
from simulate import simulate


def measure_amplitude(alpha, gamma, mu, chi, delta, eps, wf,
                      t_end=25000.0, transient_frac=0.6,
                      y0=(1.0, 0.0), n_samples=1201,
                      rtol=1e-8, atol=1e-10):
    """Integrate to t_end and return the max |z| in the last (1-transient_frac)
    portion of the trajectory."""
    t_eval = np.linspace(0.0, t_end, n_samples)
    try:
        t, z, zdot = simulate(alpha, gamma, mu, chi, delta, eps, wf,
                              t_end=t_end, y0=y0, t_eval=t_eval,
                              rtol=rtol, atol=atol)
    except Exception as e:
        return float("nan")
    i_cut = int(n_samples * transient_frac)
    return float(np.max(np.abs(z[i_cut:])))


def sweep_wf(alpha, gamma, mu, chi, delta, eps, wfs,
             t_end=25000.0, y0=(1.0, 0.0)):
    amps = np.zeros_like(wfs)
    for i, wf in enumerate(wfs):
        amps[i] = measure_amplitude(alpha, gamma, mu, chi, delta, eps, wf,
                                    t_end=t_end, y0=y0)
        print(f"  wf={wf:.5f}  z_inf={amps[i]:.4f}")
    return amps


def main():
    here = Path(__file__).resolve().parent
    figdir = here.parent / "figures"; figdir.mkdir(exist_ok=True)
    evdir = here.parent / "evidence"; evdir.mkdir(exist_ok=True)

    alpha, gamma = 0.05, -0.10
    mu = delta = chi = 1.0
    eps = 1e-3
    beta = solve_beta(alpha, gamma)
    print(f"beta = {beta:.6f}")

    # Coarse sweep across a wide window first to locate the peak,
    # then a finer sweep through the peak region.  The paper says the
    # peak sits between 0.6375 and 0.6405.
    wfs_wide = np.concatenate([
        np.linspace(0.630, 0.6370, 5),
        np.linspace(0.6372, 0.6410, 21),
        np.linspace(0.6412, 0.648, 5),
    ])
    print(f"Sweep grid: {len(wfs_wide)} points")
    print("Sweeping with large-amplitude seed (z0=1.0)...")
    amps_large = sweep_wf(alpha, gamma, mu, chi, delta, eps, wfs_wide,
                          t_end=12000.0, y0=(1.0, 0.0))
    print("Sweeping with small-amplitude seed (z0=0.01)...")
    amps_small = sweep_wf(alpha, gamma, mu, chi, delta, eps, wfs_wide,
                          t_end=12000.0, y0=(0.01, 0.0))

    # Write CSV
    csv_path = evdir / "response_sweep.csv"
    with csv_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["wf", "amp_seed_large", "amp_seed_small"])
        for wfv, aL, aS in zip(wfs_wide, amps_large, amps_small):
            w.writerow([f"{wfv:.6f}", f"{aL:.6f}", f"{aS:.6f}"])
    print(f"wrote {csv_path}")

    # Identify the large-amplitude branch edges.
    # A point is on the large-amplitude branch if amp_seed_large > 0.2,
    # and on the trivial branch if amp_seed_small < 0.05 (decayed).
    on_branch = amps_large > 0.2
    if on_branch.any():
        lo_idx = np.argmax(on_branch)        # first True
        hi_idx = len(on_branch) - 1 - np.argmax(on_branch[::-1])
        wf_lo = float(wfs_wide[lo_idx])
        wf_hi = float(wfs_wide[hi_idx])
    else:
        wf_lo = wf_hi = float("nan")

    paper_lo, paper_hi = 0.6375, 0.6405
    print(f"\nResonance peak edges from sweep:  wf in [{wf_lo:.4f}, {wf_hi:.4f}]")
    print(f"Paper-quoted edges:               wf in [{paper_lo:.4f}, {paper_hi:.4f}]")
    print(f"max z_inf on large branch:        {np.nanmax(amps_large):.4f}")

    diag = dict(alpha=alpha, gamma=gamma, mu=mu, chi=chi, delta=delta,
                eps=eps, beta=beta,
                wf_lower_edge=wf_lo, wf_upper_edge=wf_hi,
                paper_lower=paper_lo, paper_upper=paper_hi,
                max_amplitude_on_branch=float(np.nanmax(amps_large)),
                n_points=len(wfs_wide))
    (evdir / "response_diagram.json").write_text(
        json.dumps(diag, indent=2) + "\n")

    # Plot
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(wfs_wide, amps_large, "o-", color="tab:red", lw=1.2, ms=3.5,
            label="z_inf (large-amplitude seed z0=1.0)")
    ax.plot(wfs_wide, amps_small, "s-", color="tab:blue", lw=1.0, ms=2.5,
            alpha=0.7, label="z_inf (small-amplitude seed z0=0.01)")
    ax.axvline(beta, color="grey", ls=":", lw=0.8,
               label=f"central resonance β={beta:.4f}")
    ax.axvline(paper_lo, color="green", ls="--", lw=0.8,
               label=f"paper bifurcation ωf≈{paper_lo}")
    ax.axvline(paper_hi, color="green", ls="--", lw=0.8,
               label=f"paper bifurcation ωf≈{paper_hi}")
    ax.set_xlabel("ωf")
    ax.set_ylabel("z_∞ = max |z| over late times")
    ax.set_title(f"Fig 12 — response diagram (α={alpha}, γ={gamma}, μ=δ=χ=1, ε={eps})")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    out_png = figdir / "fig12_response_diagram.png"
    fig.savefig(out_png, dpi=160)
    plt.close(fig)
    print(f"wrote {out_png}")


if __name__ == "__main__":
    main()
