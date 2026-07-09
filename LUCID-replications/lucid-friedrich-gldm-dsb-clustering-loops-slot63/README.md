# LUCID slot 63 — Friedrich, Durante, Scholz 2012 (RR2964) static GLOBLE

**Paper:** Friedrich T, Durante M, Scholz M. *Modeling Cell Survival after Photon
Irradiation Based on Double-Strand Break Clustering in Megabase Pair Chromatin
Loops.* **Radiation Research** 178(5): 385–394 (Nov 2012).
**DOI:** [10.1667/RR2964.1](https://doi.org/10.1667/RR2964.1) · **PMID:** 22998227
**Affiliation (corresponding):** GSI Helmholtzzentrum für Schwerionenforschung,
Department of Biophysics, Darmstadt, Germany.

This is the **foundational static** version of the Giant-LOop Binary-LEsion
(GLOBLE) model that the GSI Darmstadt biophysics group later extended into the
kinetic, dose-rate-aware GLOBLE in Herr et al. 2014 PLoS ONE
(slot covered separately by `lucid-globle-photon-cell-killing/`).

LUCID master row: rank 94, Wave 7, tier B, priority 12, themes "DNA repair /
DDR; computational model / simulation", worktype "simulation/model
replication", verdict TODO. Confirmed against
`/Users/stevens/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv`.

## What the paper claims

A simple, mechanistic Poisson dose-response model for cell survival after
photon irradiation. Per-cell-line ingredients:

- DSBs are induced uniformly across `N_L = 3000` *giant chromatin loops* per
  nucleus, at a fixed `alpha_DSB = 30` DSB / Gy / cell.
- Two damage classes per loop, processed *independently*:
  - **isolated** (exactly one DSB in a loop) with lethality probability `eps_i`.
  - **clustered** (≥ 2 DSBs in a loop) with lethality probability `eps_c`.
- Cell-survival probability `S(D) = exp[-(eps_i n_i + eps_c n_c)]`, with
  `n_i, n_c` from the Poisson statistics of DSBs/loop.

Main predictions the paper highlights:

1. The dose-response curve `-ln S(D)` shows **LQ behaviour at low D and a
   transition to a straight line at high D**.
2. The LQ coefficients are derivable: `alpha = eps_i alpha_DSB`,
   `beta = (eps_c - 2 eps_i) alpha_DSB^2 / (2 N_L)`.
3. The model predicts an **intrinsic anti-correlation** between `beta` and
   `alpha` (small-`alpha` cells get most of their kill from clustered damage,
   hence relatively large `beta`).

## What this replication contains

- A clean-room Python implementation of the static GLOBLE equations
  (`code/globle_static.py`), with paper-fixed `alpha_DSB`, `N_L`, and 17
  cell-line `(eps_i, eps_c)` pairs transcribed from the kinetic-GLOBLE paper
  (Herr 2014 PLoS ONE Table 2), which uses the same per-cell-line fits.
- A figure-reproduction script (`code/make_figures.py`) that emits three
  diagnostic figures:
  - `fig1_dose_response_RT112.png` — dose-response with low-D LQ tangent and
    high-D asymptote, illustrating claim (1).
  - `fig2_alpha_beta_anticorr.png` — GLOBLE-derived `(alpha, beta)` for the 17
    cell lines plus the `alpha/beta` ratio diagnostic, addressing claim (3).
  - `fig3_class_decomposition_RT112.png` — isolated vs clustered DSB
    contributions to `-ln S(D)`, showing how the clustered class takes over at
    larger D, addressing claim (1) mechanistically.
- JSON dumps for downstream comparison
  (`results/static_globle_survival_curves.json`,
  `results/static_globle_alpha_beta_table.json`,
  `results/alpha_beta_correlation.json`).

## How to rerun

Requires Python ≥ 3.10 with `numpy`, `matplotlib`, optionally `scipy`
(only for Spearman correlation diagnostics).

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-friedrich-gldm-dsb-clustering-loops-slot63
python3 code/globle_static.py     # numerical smoke + tables
python3 code/make_figures.py      # figures + correlation JSON
```

Runtime: well under 5 seconds on CherryRd. No GPU / HPC required. No paid
endpoints accessed. No author contact made.

## Cross-references

- Sibling kinetic-GLOBLE replication: `../lucid-globle-photon-cell-killing/`
  (Herr 2014 PLoS ONE e83923) — its `code/globle.py::survival_static()`
  implements an identical static reduction and is the cross-check witness for
  this slot.
- Source of truth (master TSV): `~/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv`, row rank=94.
- Progress JSON: `~/.openclaw/workspace/memory/subagent-progress/slot63-friedrich-rr2964-static-globle.json`.

## Layout

```
.
├── README.md                  this file
├── PROGRESS.md                chronological work log
├── REPORT.md                  verdict + claim-by-claim audit
├── artifact_manifest.json     enumeration of all in-folder artifacts
├── code/
│   ├── globle_static.py       static GLOBLE equations + cell-line catalogue
│   └── make_figures.py        figures + LQ correlation analysis
├── figures/                   PNGs (generated)
└── results/                   JSON dumps (generated)
```
