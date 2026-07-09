#!/usr/bin/env python3
"""
Replication of Franken et al. 2012 (Oncology Reports 27: 769-774,
DOI 10.3892/or.2011.1604) — Table I RBE calculations and Figure 2
LQ / linear fits for SW-1573 lung tumour cells irradiated with
Am-241 alpha-particles (130 keV/um) vs Cs-137 gamma-rays.

What is replicable from the paper text + Table I (no digitization needed):

  1. RBE = alpha_alpha / alpha_gamma for each of the four endpoints
     (gamma-H2AX foci, survival, chromosomal fragments, colour junctions).
  2. Uncertainty propagation on RBE from the reported sigma(alpha) values
     under the assumption of independent normal errors:
        sigma(RBE)/RBE = sqrt( (sigma_a/alpha_a)^2 + (sigma_g/alpha_g)^2 )
  3. Sanity check that the "fraction of DSBs that lead to lethality" claim
     in the Discussion (~1% for gamma, ~10% for alpha) is consistent with
     Table I values.
  4. Reconstruction of the dose-effect curves implied by the published
     alpha values (linear for all but survival, LQ for survival —
     with the caveat that the paper reports only alpha for survival
     and does not tabulate beta).

What is NOT directly reproducible from the paper alone:

  - The individual data points (foci/cell, surviving fraction, aberrations/cell)
    used to fit Table I are not tabulated. They appear only in Fig. 2.
    A full refit would require figure digitization. We therefore do a
    PARTIAL replication: verify the RBE arithmetic, propagate uncertainties,
    and reconstruct the published curves.
"""

from __future__ import annotations
import math
import json
import os
from dataclasses import dataclass, asdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Table I (Franken et al. 2012, page 773) — verbatim
# alpha values in Gy^-1 with 1-sigma uncertainties
# ---------------------------------------------------------------------------

@dataclass
class AlphaPair:
    endpoint: str
    alpha_alpha: float       # alpha-particle irradiation
    sigma_alpha_alpha: float
    alpha_gamma: float       # gamma-ray irradiation
    sigma_alpha_gamma: float
    rbe_paper: float         # RBE value reported in Table I
    sigma_rbe_paper: float
    unit: str = "Gy^-1"


TABLE_I = [
    AlphaPair("gamma-H2AX foci (DNA DSBs)", 25.0,  8.20, 25.00, 3.000, 1.0,  0.3),
    AlphaPair("Survival",                    2.2,  0.38,  0.15, 0.045, 14.7, 5.1),
    AlphaPair("Chromosomal fragments",      16.8,  4.50,  1.10, 0.310, 15.3, 5.9),
    AlphaPair("Colour junctions",            9.2,  3.20,  0.69, 0.200, 13.3, 6.0),
]


def rbe_with_uncertainty(a_alpha: float, s_alpha: float,
                         a_gamma: float, s_gamma: float
                         ) -> tuple[float, float]:
    """Ratio of independent Gaussians, first-order (delta-method)."""
    rbe = a_alpha / a_gamma
    rel = math.sqrt((s_alpha / a_alpha) ** 2 + (s_gamma / a_gamma) ** 2)
    return rbe, rbe * rel


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_results = os.path.normpath(os.path.join(here, "..", "results"))
    out_figures = os.path.normpath(os.path.join(here, "..", "figures"))
    os.makedirs(out_results, exist_ok=True)
    os.makedirs(out_figures, exist_ok=True)

    # ------------------------------------------------------------------
    # (1) Recompute RBE from Table I and compare to printed values
    # ------------------------------------------------------------------
    rows = []
    print(f"{'Endpoint':<30s} {'RBE_calc':>10s} {'sigma':>8s}  "
          f"{'RBE_paper':>10s} {'sigma':>8s}  match?")
    for ap in TABLE_I:
        rbe, srbe = rbe_with_uncertainty(
            ap.alpha_alpha, ap.sigma_alpha_alpha,
            ap.alpha_gamma, ap.sigma_alpha_gamma)
        # Agreement: within 5% on RBE and within 25% on sigma_RBE
        match_rbe = abs(rbe - ap.rbe_paper) / ap.rbe_paper < 0.05
        match_sigma = abs(srbe - ap.sigma_rbe_paper) / ap.sigma_rbe_paper < 0.25
        rows.append({
            "endpoint": ap.endpoint,
            "alpha_alpha": ap.alpha_alpha,
            "sigma_alpha_alpha": ap.sigma_alpha_alpha,
            "alpha_gamma": ap.alpha_gamma,
            "sigma_alpha_gamma": ap.sigma_alpha_gamma,
            "rbe_recomputed": rbe,
            "sigma_rbe_recomputed": srbe,
            "rbe_paper": ap.rbe_paper,
            "sigma_rbe_paper": ap.sigma_rbe_paper,
            "rbe_match": bool(match_rbe),
            "sigma_match": bool(match_sigma),
        })
        print(f"{ap.endpoint:<30s} {rbe:10.3f} {srbe:8.3f}  "
              f"{ap.rbe_paper:10.3f} {ap.sigma_rbe_paper:8.3f}  "
              f"{'OK' if match_rbe else '!='} / {'OK' if match_sigma else '!='}")

    with open(os.path.join(out_results, "rbe_recomputed.json"), "w") as fh:
        json.dump(rows, fh, indent=2)

    # ------------------------------------------------------------------
    # (2) "1% of DSBs lethal under gamma, 10% under alpha" claim
    # ------------------------------------------------------------------
    # Discussion (p.773): alpha for DNA-DSBs (25 Gy^-1) >> alpha for cell kill.
    # Ratio of cell-kill alpha to DSB alpha at low dose ~ fraction of DSBs
    # that lead to lethal events.
    frac_lethal_gamma = 0.15 / 25.0  # cell kill / DSB induction, gamma
    frac_lethal_alpha = 2.2 / 25.0   # cell kill / DSB induction, alpha
    print("\nFraction of DSBs leading to lethality (alpha_kill / alpha_DSB):")
    print(f"  gamma:  {frac_lethal_gamma:.4f}   (paper says 'about 1%' -> 0.01)")
    print(f"  alpha:  {frac_lethal_alpha:.4f}   (paper says 'about 10%' -> 0.10)")

    consistency = {
        "fraction_lethal_DSBs_gamma": frac_lethal_gamma,
        "paper_claim_gamma_pct": 1.0,
        "consistent_gamma": abs(frac_lethal_gamma * 100 - 1.0) < 0.5,
        "fraction_lethal_DSBs_alpha": frac_lethal_alpha,
        "paper_claim_alpha_pct": 10.0,
        "consistent_alpha": abs(frac_lethal_alpha * 100 - 10.0) < 2.0,
    }
    with open(os.path.join(out_results, "lethal_dsb_fraction.json"), "w") as fh:
        json.dump(consistency, fh, indent=2)

    # ------------------------------------------------------------------
    # (3) Reconstruct the four published dose-response curves from
    #     Table I alpha values (linear model F(D)=alpha*D for the three
    #     non-survival endpoints; LQ for survival — alpha only for alpha,
    #     LQ with paper's note that gamma survival shows a quadratic
    #     contribution but beta is NOT reported in Table I).
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(11, 9))
    titles = [
        "DNA-DSBs (gamma-H2AX foci)",
        "Cell survival (clonogenic)",
        "Chromosomal fragments",
        "Colour junctions",
    ]
    # Dose ranges from Methods (p.770-771)
    dose_max_alpha = {0: 1.4, 1: 1.6, 2: 0.8, 3: 0.8}
    dose_max_gamma = {0: 1.4, 1: 8.0, 2: 4.0, 3: 4.0}

    for i, (ax, ap, title) in enumerate(zip(axes.flat, TABLE_I, titles)):
        Da = np.linspace(0, dose_max_alpha[i], 60)
        Dg = np.linspace(0, dose_max_gamma[i], 60)

        if i == 1:  # survival — LQ for gamma, exponential (linear-in-log) for alpha
            # Paper: only alpha for alpha-particle survival is significant;
            # for gamma, alpha=0.15 plus a small beta. Beta not tabulated,
            # so we plot the pure-alpha (linear in log) curves as drawn in Fig. 2.
            Sa = np.exp(-ap.alpha_alpha * Da)
            Sg = np.exp(-ap.alpha_gamma * Dg)
            ax.semilogy(Da, Sa, "k-", label="alpha (Am-241, 130 keV/um)")
            ax.semilogy(Dg, Sg, "r--", label="gamma (Cs-137)")
            ax.set_ylabel("Surviving fraction")
            ax.set_ylim(1e-3, 1.2)
        else:
            Ya = ap.alpha_alpha * Da
            Yg = ap.alpha_gamma * Dg
            ax.plot(Da, Ya, "k-", label="alpha (Am-241, 130 keV/um)")
            ax.plot(Dg, Yg, "r--", label="gamma (Cs-137)")
            ylab = {
                0: "gamma-H2AX foci per cell (above background)",
                2: "Chromosome 2 fragments per cell (genome-corrected)",
                3: "Colour junctions per cell (genome-corrected)",
            }[i]
            ax.set_ylabel(ylab)

        ax.set_xlabel("Dose (Gy)")
        ax.set_title(f"{title}\nRBE = {ap.rbe_paper:.1f} +/- {ap.sigma_rbe_paper:.1f}")
        ax.legend(fontsize=8, loc="best")
        ax.grid(alpha=0.3)

    fig.suptitle("Franken et al. 2012 — reconstructed dose-response from Table I alphas",
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(out_figures, "fig2_reconstructed.png"), dpi=150)
    plt.close(fig)

    # ------------------------------------------------------------------
    # (4) Coverage / agreement summary
    # ------------------------------------------------------------------
    n_total = len(TABLE_I)
    n_rbe_match = sum(r["rbe_match"] for r in rows)
    n_sigma_match = sum(r["sigma_match"] for r in rows)
    summary = {
        "rbe_endpoints_recomputed": n_total,
        "rbe_endpoints_matching_paper": n_rbe_match,
        "sigma_endpoints_matching_paper": n_sigma_match,
        "lethal_dsb_fraction_consistent_gamma": consistency["consistent_gamma"],
        "lethal_dsb_fraction_consistent_alpha": consistency["consistent_alpha"],
    }
    with open(os.path.join(out_results, "summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print("\nSummary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
