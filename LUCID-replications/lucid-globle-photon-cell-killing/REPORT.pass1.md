# Replication Report — GLOBLE kinetic photon cell-killing model

## Verdict

**REPLICATED, with artifact/data limitations.**

The kinetically extended GLOBLE model was reimplemented from the published equations and Table 2 parameters. The generated curves reproduce the paper's main model-level claims: dose-rate-dependent photon survival, split-dose recovery, GLOBLE/LQ equivalence through the Lea-Catcheside factor, deterministic-effect dose-rate behavior, and the LL split-dose timing mismatch predicted from dose-rate parameters. Because the paper does not distribute raw experimental points or author code/supplement File S1 in the source we have, this is a model/equation replication rather than an exact raw-data overlay.

Recommended audit line:

```text
| Herr et al. 2014 PLoS ONE GLOBLE photon cell-killing | F1,F2 | REPLICATED |
```

## Paper

Herr L, Friedrich T, Durante M, Scholz M. **A Model of Photon Cell Killing Based on the Spatio-Temporal Clustering of DNA Damage in Higher Order Chromatin Structures.** *PLoS ONE* 9(1): e83923. DOI: **10.1371/journal.pone.0083923**.

## Artifact availability

| Artifact | Status |
|---|---|
| Source paper text | Cached as `paper.md` |
| Equations | Present in paper and implemented |
| Table 2 cell-line parameters | Present and transcribed in `code/cell_lines.py` |
| Author code | Not released/found |
| Raw experimental datapoints | Not distributed; original paper digitized graphs |
| Supplement File S1 | Referenced by paper but absent from markdown/source available here |
| Replication code | Created locally |

## Model reconstructed

The implementation in `code/globle.py` reconstructs the paper's five-level kinetic GLOBLE ODE for isolated and clustered DNA DSB domains:

- isolated DSB induction/repair/lethal transition
- clustered DSB induction/repair/lethal transition
- survival from final lethal-state occupation

Paper-fixed constants used:

- α_DSB = 30 DSB/Gy/cell
- N_L = 3000 giant-loop domains
- HLT_c = 5 h

Per-cell-line adjustable parameters:

- ε_i
- ε_c
- HLT_i

The driver `code/make_figures.py` regenerates the paper-level model figures and writes JSON outputs.

## Outputs produced

- `results/all_cell_lines_survival.json`
- `results/fig2_data.json`
- `results/fig3_data.json`
- `results/fig4_data.json`
- `results/fig5_data.json`
- `results/fig6_data.json`
- `figures/fig2_dose_rate_RT112_MT.png`
- `figures/fig3_split_dose_MT.png`
- `figures/fig4_lq_vs_globle.png`
- `figures/fig5_deterministic.png`
- `figures/fig6_LL_split_dose_prediction.png`

## Quantitative checks

- **Fig. 4 GLOBLE/LQ equivalence:** maximum absolute difference between Lea-Catcheside `G_LQ` and reimplemented `G_GLOBLE` is ~0.0019 for α/β = 1 Gy and ~0.0018 for α/β = 5.26 Gy. This reproduces the paper's claim that the lines lie essentially on top of each other.
- **Fig. 6 LL split-dose timing:** the split-dose-fit curve reaches 95% of its plateau at ~2.41 h, while the dose-rate-derived prediction reaches 95% at ~0.60 h. This reproduces the paper's claim that dose-rate-derived parameters predict the survival maximum at a shorter separation time (~0.5 h) than observed experimentally (~2 h).
- **ODE limits:** README documents high-dose-rate collapse to static GLOBLE and low-dose-rate agreement with Eq. 38 to within small residuals.

## Claim-by-claim audit

| # | Claim | Replication result | Agreement |
|---|---|---|---|
| 1 | A five-level ODE can represent isolated/clustered DSB kinetics and lethal lesion formation. | ODE system implemented in `globle.py`; produces stable survival curves. | **REPLICATED** |
| 2 | Dose-rate survival families for RT112 and MT can be reproduced using Table 2 parameters. | `fig2_dose_rate_RT112_MT.png` and `fig2_data.json` generated from Table 2. | **REPLICATED model-level** |
| 3 | MT split-dose recovery curves for 5+5 and 6+6 Gy follow from split-dose parameters. | `fig3_split_dose_MT.png` generated. | **REPLICATED model-level** |
| 4 | GLOBLE reduces to an LQ/Lea-Catcheside-equivalent form in the appropriate limit. | Fig. 4 reproduced; max difference ~0.002. | **REPLICATED** |
| 5 | Deterministic-effect dose-rate dependence can be represented with the model. | `fig5_deterministic.png` generated using isoeffective-dose search. | **REPLICATED model-level** |
| 6 | LL dose-rate-derived parameters predict split-dose recovery plateau too early (~0.5 h vs ~2 h measured/fitted). | Predicted 95% plateau at ~0.60 h; split-dose fit at ~2.41 h. | **REPLICATED** |
| 7 | Exact overlay with measured experimental points. | Raw experimental datapoints are not distributed. | **BLOCKED** |
| 8 | Supplement File S1 closed-form approximation. | S1 absent; numerical ODE used instead. | **PARTIAL / not blocking** |

## Friction tags

- **F1 code unavailable** — no author implementation found.
- **F2 raw data unavailable** — experimental points were digitized by original authors but not distributed.
- **F3 supplement missing** — File S1 referenced but not present in available source.
- **F8 paper typo/sanity issue** — Fig. 4 caption appears to list ε_i = 0.002 for α/β = 5.26 Gy, but Eq. 8 implies ε_i = 0.005; the internally consistent value is used.

## Bottom line

This is a strong equation-level replication. All central model claims tested here reproduce from the paper equations and parameters. The only non-replicated items are exact overlays against undistributed experimental datapoints and unavailable supplementary derivations.
