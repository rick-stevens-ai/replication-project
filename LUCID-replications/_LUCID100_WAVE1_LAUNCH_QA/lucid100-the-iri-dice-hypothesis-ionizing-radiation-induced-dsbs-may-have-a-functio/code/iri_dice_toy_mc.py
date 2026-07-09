#!/usr/bin/env python3
"""
iri_dice_toy_mc.py — Minimal toy Monte Carlo of the IRI-DICE hypothesis.

Paper: Langen, Helou & Forssell-Aronsson (2020), "The IRI-DICE hypothesis...",
       Radiat Environ Biophys 59:349-355, doi 10.1007/s00411-020-00854-x.

This is a *qualitative* smoke-test of the IRI-DICE conceptual model. The paper
itself proposes no equations, supplies no code or data, and explicitly states
that direct experimental testing is not currently possible. The authors outline
a computational approach (radiation transport + chromatin model + per-gene
sequence functionality) as the only feasible supportive test. We implement the
most stripped-down version of that program:

  * Genome model: N genes, each with a small functional-element budget made up
    of {promoter, gene_core, enhancer, NRE} with relative sequence lengths
    drawn from typical mammalian-genome rough estimates. Most of the cell's
    DNA is "other / non-functional-for-IRI-DICE" so a DSB has only a small
    probability of hitting a functional element.
  * DSB induction: per cell, number of DSBs ~ Poisson(mu) where mu scales
    linearly with absorbed dose D (the paper assumes the standard ~35 DSB/Gy
    per diploid mammalian cell for low-LET X-rays).
  * Per-DSB outcome on a randomly-hit position:
      - promoter hit  -> strong suppression of that gene
      - gene_core hit -> partial suppression (truncated transcript)
      - enhancer hit  -> moderate suppression
      - NRE hit       -> *increase* in transcript level (rare)
      - other         -> no transcriptional effect
  * Repair threshold: if total DSBs in the cell exceed ATM/repair activation
    threshold T_repair, repair is initiated and a fraction f_restore of cis
    effects is restored to baseline (transcript returns to ~1). This encodes
    the paper's central claim that IRI-DICE manifests *particularly* in the
    very-low-dose regimen below the repair threshold.

Outputs (written under ../artifacts/figs/):
  - fig_doseresponse_diversity.png : cell-population transcript-change distribution
                                     across multiple doses (the diversity claim)
  - fig_suppression_dominance.png  : fraction of suppression vs overexpression
                                     across dose (paper claim: suppression
                                     exceeds overexpression at very low dose)
  - fig_repair_threshold.png       : mean perturbation per cell vs dose,
                                     showing the non-monotonic / threshold
                                     behaviour the paper hypothesises

This is a TOY model. It is not a quantitative replication. It exists to show
that the qualitative claims of IRI-DICE are *consistent with* the proposed
mechanism under reasonable parameter choices, and to provide a runnable
scaffold for any future quantitative replication.

Run:
  python3 iri_dice_toy_mc.py [--ncells 5000] [--seed 0] [--out ../artifacts/figs]
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass

import numpy as np


# ---- model parameters ----------------------------------------------------

@dataclass
class IriDiceParams:
    n_genes: int = 20_000           # protein-coding genes, rough mammalian
    n_cells: int = 5_000
    dsb_per_gy: float = 35.0        # canonical low-LET ~35 DSB/Gy/cell
    # Fractions of the genome (by sequence length) that fall in each functional
    # element. ENCODE et al. suggest >>2% is "functional"; for IRI-DICE only the
    # cis-regulatory + gene-body fractions matter. These are deliberate
    # order-of-magnitude estimates, not measured values.
    frac_promoter: float = 0.005     # ~1.5 kb x 20k / 3 Gb ~ 0.01
    frac_gene_core: float = 0.02     # exonic+intronic of expressed genes
    frac_enhancer: float = 0.03
    frac_nre: float = 0.002          # negative regulatory elements, small
    # Effect sizes (log2 fold-change applied to baseline expression 1.0)
    eff_promoter: float = -3.0
    eff_gene_core: float = -1.0
    eff_enhancer: float = -1.5
    eff_nre: float = +1.5            # NRE disruption derepresses target gene
    # Repair threshold: above this DSB count, repair restores a fraction
    # f_restore of the IRI-DICE perturbations.
    t_repair: int = 20
    f_restore: float = 0.9
    # Detection threshold for "perturbed gene" call
    detect_log2fc: float = 0.5

    @property
    def frac_other(self) -> float:
        return max(
            0.0,
            1.0 - (self.frac_promoter + self.frac_gene_core
                   + self.frac_enhancer + self.frac_nre),
        )


# ---- core simulation -----------------------------------------------------

def simulate_population(dose_gy: float, p: IriDiceParams, rng: np.random.Generator):
    """Simulate `n_cells` cells at `dose_gy` Gy. Return per-cell perturbation log2FC matrix.

    For performance we do not allocate the full n_cells x n_genes matrix.
    We return per-cell *summary statistics*: number suppressed, number
    overexpressed, mean |log2fc| over perturbed genes, and net suppression
    minus overexpression count.
    """
    mu = p.dsb_per_gy * dose_gy
    n_dsbs = rng.poisson(mu, size=p.n_cells)

    # Per-DSB element categorical draw
    fracs = np.array([
        p.frac_promoter, p.frac_gene_core, p.frac_enhancer,
        p.frac_nre, p.frac_other,
    ])
    effects = np.array([
        p.eff_promoter, p.eff_gene_core, p.eff_enhancer, p.eff_nre, 0.0
    ])

    suppressed = np.zeros(p.n_cells, dtype=np.int32)
    overexpr = np.zeros(p.n_cells, dtype=np.int32)
    sum_abs_logfc = np.zeros(p.n_cells, dtype=np.float64)

    for i in range(p.n_cells):
        k = int(n_dsbs[i])
        if k == 0:
            continue
        # Draw element class for each DSB
        cats = rng.choice(5, size=k, p=fracs)
        # Repair restoration
        if k > p.t_repair:
            keep = rng.random(k) > p.f_restore
            cats = np.where(keep, cats, 4)  # category 4 == "other / no effect"
        fcs = effects[cats]
        nz = fcs[fcs != 0.0]
        if nz.size == 0:
            continue
        suppressed[i] = int((nz < 0).sum())
        overexpr[i] = int((nz > 0).sum())
        sum_abs_logfc[i] = float(np.abs(nz).sum())

    return {
        "dose_gy": dose_gy,
        "n_dsbs": n_dsbs,
        "suppressed_per_cell": suppressed,
        "overexpr_per_cell": overexpr,
        "sum_abs_logfc": sum_abs_logfc,
    }


def run_dose_scan(doses_gy, p: IriDiceParams, rng):
    out = []
    for d in doses_gy:
        out.append(simulate_population(d, p, rng))
    return out


# ---- plotting ------------------------------------------------------------

def _ensure_matplotlib():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def plot_diversity(results, outpath):
    plt = _ensure_matplotlib()
    fig, axes = plt.subplots(1, len(results), figsize=(3 * len(results), 3),
                             sharey=True)
    if len(results) == 1:
        axes = [axes]
    for ax, r in zip(axes, results):
        net = r["suppressed_per_cell"] - r["overexpr_per_cell"]
        ax.hist(net, bins=40, color="steelblue", edgecolor="black", alpha=0.85)
        ax.set_title(f"D = {r['dose_gy']:.3g} Gy")
        ax.set_xlabel("net suppressed - overexpressed (per cell)")
    axes[0].set_ylabel("cell count")
    fig.suptitle("IRI-DICE toy MC: per-cell response diversity")
    fig.tight_layout()
    fig.savefig(outpath, dpi=140)
    plt.close(fig)


def plot_suppression_dominance(results, outpath):
    plt = _ensure_matplotlib()
    doses = [r["dose_gy"] for r in results]
    mean_supp = [r["suppressed_per_cell"].mean() for r in results]
    mean_over = [r["overexpr_per_cell"].mean() for r in results]
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(doses, mean_supp, "o-", color="C0", label="mean suppressed / cell")
    ax.plot(doses, mean_over, "s-", color="C3", label="mean overexpressed / cell")
    ax.set_xscale("log")
    ax.set_xlabel("Absorbed dose D (Gy)")
    ax.set_ylabel("perturbed genes per cell")
    ax.set_title("IRI-DICE: suppression dominance vs dose")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(outpath, dpi=140)
    plt.close(fig)


def plot_repair_threshold(results, p: IriDiceParams, outpath):
    plt = _ensure_matplotlib()
    doses = np.array([r["dose_gy"] for r in results])
    mean_abs = np.array([r["sum_abs_logfc"].mean() for r in results])
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(doses, mean_abs, "o-", color="C2")
    ax.axvline(p.t_repair / p.dsb_per_gy, ls="--", color="grey",
               label=f"repair threshold ~ {p.t_repair / p.dsb_per_gy:.3g} Gy")
    ax.set_xscale("log")
    ax.set_xlabel("Absorbed dose D (Gy)")
    ax.set_ylabel("mean Σ|log2FC| per cell")
    ax.set_title("IRI-DICE: persistent perturbation vs repair onset")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(outpath, dpi=140)
    plt.close(fig)


# ---- main ----------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ncells", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=None,
                    help="output figure directory (default ../artifacts/figs)")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = args.out or os.path.normpath(os.path.join(here, "..", "artifacts", "figs"))
    os.makedirs(out_dir, exist_ok=True)

    p = IriDiceParams(n_cells=args.ncells)
    rng = np.random.default_rng(args.seed)

    doses_gy = [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 2.0]
    results = run_dose_scan(doses_gy, p, rng)

    plot_diversity(results, os.path.join(out_dir, "fig_doseresponse_diversity.png"))
    plot_suppression_dominance(
        results, os.path.join(out_dir, "fig_suppression_dominance.png"))
    plot_repair_threshold(
        results, p, os.path.join(out_dir, "fig_repair_threshold.png"))

    summary = {
        "params": p.__dict__,
        "doses_gy": doses_gy,
        "per_dose": [
            {
                "dose_gy": r["dose_gy"],
                "mean_dsbs": float(r["n_dsbs"].mean()),
                "mean_suppressed": float(r["suppressed_per_cell"].mean()),
                "mean_overexpressed": float(r["overexpr_per_cell"].mean()),
                "mean_abs_logfc_sum": float(r["sum_abs_logfc"].mean()),
                "frac_cells_any_perturb": float(
                    ((r["suppressed_per_cell"] + r["overexpr_per_cell"]) > 0).mean()),
            }
            for r in results
        ],
    }
    with open(os.path.join(out_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
