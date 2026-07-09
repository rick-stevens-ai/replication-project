# LUCID replication — Lung-fibrosis ABM/MC (Cogno et al. 2024)

Honest, reduced-scope replication of:

> Cogno N., Bauer R., Durante M. (2024). **Mechanistic model of radiotherapy-induced
> lung fibrosis using coupled 3D agent-based and Monte Carlo simulations.**
> *Communications Medicine* **4**:16. https://doi.org/10.1038/s43856-024-00442-w

## What this replication covers

| Component | Paper artifact | Status here |
|---|---|---|
| ABM (BioDynaMo, C++) | Released, Apache-2.0 | **Not built** (heavy deps); used as reference source |
| MC (TOPAS-nBio + OpenTOPAS + Geant4) | Released, registration + GEANT4 build chain | **Not built** (multi-hour install) |
| Simulation source code | Zenodo 10.5281/zenodo.10185637 (CC-BY-4.0) | **Downloaded & inspected** ✓ |
| Parameter values (LQ, geometry, rates) | sim-param.h in Zenodo drop | **Extracted & re-used** ✓ |
| FSU survival vs dose (Fig 5c) | LQ–critical-volume model | **Reproduced** with Python ABM-lite |
| ΔECM(D) sigmoid (Fig 5b) | Eq. (2) | **Qualitatively reproduced** |
| RSI(D) (Fig 5d) | Eq. (3) | **Qualitatively reproduced** |
| 1fx vs 5fx fractionation sparing (Fig 6) | normal-tissue sparing | **Reproduced** |
| Parameter sensitivity (Fig 7) | bystander, α/β | **Partially reproduced** (α,β trend ✓; bystander too weak) |
| 3D dose distribution (Fig 4, 8) | MC scoring per cell | **Not reproduced** (would need TOPAS-nBio) |
| Proton vs photon RBE_FSU (Fig 9) | depends on MC dose distributions | **Not reproduced** |

## Quick start

```bash
cd code
python3 abm_lite.py --quick --reps 3        # smoke test (~5 s)
python3 abm_lite.py --reps 10               # full run (~1 min)
```

Outputs land in `results/` (CSV) and `figures/` (PNG).

## Files

```
PROGRESS.md           — incremental progress log
REPORT.md             — full replication report with claim-by-claim table
README.md             — this file
code/abm_lite.py      — Python ABM-only reproduction
data/paper.pdf        — the target paper
data/Code.zip         — Zenodo artifact (BioDynaMo C++ source + TOPAS-nBio extension)
data/code/            — unpacked Zenodo source
results/*.csv         — per-replicate raw outputs
figures/fig5_like.png — single-fraction dose response (paper Fig 5)
figures/fig6_like.png — fractionation comparison (paper Fig 6)
figures/fig7_like.png — parameter sensitivity (paper Fig 7)
logs/run_summary.json — fitted parameters from this run
```

## Honesty caveats

* **Not a faithful binary reproduction**: we did not compile or run BioDynaMo /
  TOPAS-nBio. The Python `abm_lite.py` is a *behaviorally faithful surrogate*
  that uses the paper's published equations and a subset of its parameters
  (LQ α, β, α/β; bystander threshold; phagocytic fraction / index;
  damaged-to-senescent rate; ECM baseline) plus simplified compartmental
  dynamics for myofibroblast expansion and ECM deposition.
* **No spatial 3D mesh, no MC dose distribution**: we approximate cell-level
  dose heterogeneity with a log-normal at CV=0.20. The paper's central
  qualitative finding — that the *shape* of the dose distribution matters —
  is therefore *not* tested here.
* **No DNA damage**: we use the LQ model directly, like the paper, so this
  is not actually a limitation.
* **Bystander sensitivity is weaker** than the paper reports: paper Fig 7
  shows substantial impact of lowering threshold 2→1; our surrogate shows
  essentially no impact because once an alveolus has more than ~2 senescent
  cells the threshold rule fires identically.

## Coverage score

Overall replication coverage of the paper's main claims: **~55%** (see
`REPORT.md` Claim-by-Claim Table for the detailed scoring).
