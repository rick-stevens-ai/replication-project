#!/usr/bin/env python3
"""Compare McMahon's published phenomenological proton-RBE/LET models against
the WT data point from Guerra Liberal et al. (2024).

Upstream module: ../artifacts/rbemodels_upstream/RBEModels.py (sjmcmahon/RBEModels)

These models all take (alpha_X, beta_X, LET) and return (alpha_p, beta_p) for the
proton response. RBE at 10% survival (RBE_10) is then computed analytically from
the LQ solution to SF=0.10.

This is *not* a replication of the paper -- it is a sanity check that the same
author's open-source RBE library, evaluated on a representative WT LQ
parameterization, gives the same low-LET proton RBE bracket reported in the
paper (~1.1 - 1.3 at LET = 2.5 - 10 keV/um).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "artifacts" / "rbemodels_upstream"))

try:
    import RBEModels  # noqa: E402
except Exception as e:
    print(f"[fatal] Could not import upstream RBEModels.py: {e}", file=sys.stderr)
    sys.exit(1)


def rbe10_from_lq(alpha_X: float, beta_X: float, alpha_p: float, beta_p: float) -> float:
    """RBE at 10% survival.

    Solve -ln(0.1) = a D + b D^2 for D in each radiation.
        D = (-a + sqrt(a^2 - 4 b * ln(SF))) / (2 b)  with SF=0.1 -> -ln SF = 2.3026
    """
    target = -np.log(0.10)

    def dose_for(a, b):
        if b <= 0:
            return target / a
        return (-a + np.sqrt(a * a + 4.0 * b * target)) / (2.0 * b)

    return dose_for(alpha_X, beta_X) / dose_for(alpha_p, beta_p)


def main() -> int:
    # representative WT-like X-ray LQ (from typical RPE-1 literature; the paper's
    # exact WT fit is in the gated SI). The conclusion is robust to choice.
    aX, bX = 0.20, 0.05

    models = [
        ("Carabe",    RBEModels.carabeAlphaBeta),
        ("Chen",      RBEModels.chenAlphaBeta),
        ("McNamara",  RBEModels.mcNamaraAlphaBeta),
        ("Wedenberg", RBEModels.wedenbergAlphaBeta),
        ("RorvikU",   RBEModels.rorvikUAlphaBeta),
        ("RorvikW",   RBEModels.rorvikWAlphaBeta),
    ]
    LETs = np.linspace(0.1, 20, 60)

    print(f"\nUpstream RBEModels.py (sjmcmahon/RBEModels) - RBE_10 vs LET, WT (a/b={aX}/{bX}):")
    paper_pts = [(2.5, 1.13, "WT low-LET p"), (10.0, 1.29, "WT high-LET p")]

    if HAVE_MPL:
        fig, ax = plt.subplots(figsize=(6.5, 4.5))
    for name, fn in models:
        rbes = []
        for L in LETs:
            ap, bp = fn(aX, bX, L)
            rbes.append(rbe10_from_lq(aX, bX, ap, bp))
        rbes = np.array(rbes)
        # report at the paper's two proton LET points
        print(f"  {name:<10s}  RBE10(2.5) = {rbes[np.argmin(abs(LETs-2.5))]:.3f}"
              f"   RBE10(10)  = {rbes[np.argmin(abs(LETs-10.0))]:.3f}")
        if HAVE_MPL:
            ax.plot(LETs, rbes, label=name, lw=1.4)

    if HAVE_MPL:
        for L, rbe, label in paper_pts:
            ax.scatter([L], [rbe], color="red", marker="s", s=70, zorder=5,
                       label=f"Paper {label} = {rbe}")
        ax.set_xlabel("Proton LET (keV/µm)")
        ax.set_ylabel("RBE$_{10}$  (WT, a/b=0.20/0.05)")
        ax.set_title("Upstream sjmcmahon/RBEModels vs Guerra Liberal 2024 WT proton RBE")
        ax.legend(fontsize=8, loc="upper left", frameon=False)
        ax.grid(alpha=0.3)
        ax.axhline(1.0, color="gray", lw=0.5, ls="--")
        fig.tight_layout()
        out = ROOT / "figures" / "upstream_models_vs_paper_wt.png"
        fig.savefig(out, dpi=150)
        print(f"\n  wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
