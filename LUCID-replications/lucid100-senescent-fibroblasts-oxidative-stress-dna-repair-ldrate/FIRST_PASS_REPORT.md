# FIRST PASS REPORT — Sangsuwan et al. 2023 (FBL 28(11):296)

**Slot:** LUCID100 Wave 6 backfill, slot 56 (master rank 87)
**DOI:** 10.31083/j.fbl2811296
**Date:** 2026-06-09
**Verdict:** **PARTIAL — numerical-claim consistency replication completed; full pipeline replication NOT feasible without author data.**

## Top-line
- **Worktype is mis-tagged in master TSV.** Listed as `simulation/model replication`; **it is wet-lab radiobiology** (γH2AX foci, FISH co-loc, 8-oxo-dG ELISA, SA-β-gal, qPCR T/S, P21 WB). Recommend retag to **wet-lab assay / radiobiology · DNA repair kinetics + oxidative stress + senescence**.
- **Open-access paper + supplement harvested** (PDF, supplement ZIP with Figs 1–6 JPEGs, supplement PDF with ANOVA tables S1/S2). No raw data deposited; author statement is "available upon request."
- **All headline qualitative claims reproduce** under independent t-tests on the published means±SE:
  - P8 fibroblasts return to γH2AX baseline by 24 h post 1 Gy; P19 and P23 retain damage (4/4 qualitative checks PASS).
  - TIFs rise monotonically with cellular age (P8 < P19-C < P19-IR ≈ P19-ST < P23) at baseline and at 48 h post 1 Gy.
- **Reported p-values are only reproducible if effective n > 3** (n_eff ≈ 6–14 across all 7 probed comparisons), which is **fully consistent with standard foci scoring** (cells, not experiments, as the unit) and longitudinal slope tests across 8 weeks × 3 replicates. No statistical red flags.

## What works
| Item | Status |
|---|---|
| Paper PDF + supplement download | ✅ |
| Figure JPEGs (supplement) | ✅ |
| ANOVA tables S1 (PD) and S2 (8-oxo-dG) | ✅ extracted, text |
| γH2AX qualitative ordering replication | ✅ 4/4 PASS |
| TIF Table 1 ordering and "soft" significance | ✅ 17/24 soft pass |
| Effective-n sensitivity analysis | ✅ n_eff ∈ [6,14] consistent |
| Reconstructed Figs 3A, 5A/B, 6A | ✅ 3 PNG figures |

## What blocks full replication
| Block | Why | Mitigation |
|---|---|---|
| Per-replicate raw values (foci counts, ELISA OD, T/S ratios, P21 band intensities) | Author statement "available upon request"; no public deposit | Out of scope: no author contact this pass |
| Microscopy image stacks | Not deposited | Out of scope |
| No code / pipeline | Authors did not release any | N/A |

## Recommendation
1. **Retag worktype** in master TSV (row 110) from `simulation/model replication` to `wet-lab assay / radiobiology` and **set status to `partial_numerical_check (KEEP_REDUCED)`**.
2. **Do not** schedule this for full Wave 6 replication unless author raw data become available.
3. **Cross-link** with related LUCID slots: Acheva 2017, Mariotti split-dose γH2AX, Grandt fibroblast RNA-seq.
4. No heavy compute warranted; this is CherryRd-CPU-friendly. **No HPC job plan required.**

## Files
- `README.md`, `PROGRESS.md`, `ARTIFACT_MANIFEST.md`, `REPORT.md`
- `code/01_smoke_replication.py`, `code/02_sensitivity_n.py`, `code/03_figures.py`
- `results/smoke_replication_results.json`, `results/table1_tif_replication.csv`, `results/sensitivity_n.json`
- `figures/fig3_oxodg.png`, `figures/fig5_gh2ax_kinetics.png`, `figures/fig6_tifs.png`
