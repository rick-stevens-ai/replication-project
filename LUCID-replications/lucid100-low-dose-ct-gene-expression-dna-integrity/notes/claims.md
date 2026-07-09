# Bulletised claims — Schmid et al. 2025 (IJMS 26:11869)

Anchors: `§N` = Results subsection number; `T1`/`T2` = Tables 1/2; `TA1`/`TA2`/`TA3` = appendix tables; `F1`–`F6` = figures.

## Cohort

- C1 (§2.1, T1) — 60 patients analyzed for gene expression. 61 enrolled; 1 dropped before second draw (provided γ-H2AX only).
- C2 (§2.1, T1) — 39 M (65 %), 21 F (35 %); mean age 65.2 ± 14.4 y (range 28–91).
- C3 (§2.1, T1) — Mean DLP across all 60 = 561.9 ± 384.6 mGy·cm; effective dose 8.3 ± 5.8 mSv (range 0.9–24.2).
- C4 (§2.1, T1) — γ-H2AX subset n=12, mean DLP 321.0 ± 149.3 mGy·cm, effective dose 4.3 ± 2.4 mSv.

## Gene expression — combined analysis (in vivo + ex vivo)

- G1 (§2.2) — All 9 target genes detected in all samples (no dropout).
- G2 (§2.2) — Highly significant (p ≤ 0.001) combined median DGE for EDA2R↑, MIR34AHG↑, WNT3↓.
- G3 (§2.2) — DDB2 and FDXR slightly downregulated combined (p ≤ 0.05).
- G4 (§2.2) — POU2AF1 significantly upregulated combined (p ≤ 0.001).

## Gene expression — in vivo only

- G5 (§2.2, F2) — In addition to above, in-vivo subset shows significant upregulation of DDB2, FDXR, AEN, PHLDA3 (p ≤ 0.001 to 0.041).
- G6 (§2.2, F2) — WNT3 no longer differential in vivo (p = 0.302).
- G7 (§2.2, F2) — POU2AF1 borderline (p = 0.049) in vivo.

## In vivo vs ex vivo difference

- G8 (§2.2, T2, F3) — All genes except WNT3 differ significantly between in vivo and ex vivo conditions (p ≤ 0.001–0.03).
- G9 (§2.2) — Apart from MIR34AHG, in-vivo samples show greater anticipated DGE than ex-vivo across all genes.
- G10 (§2.2, F3) — For 7/9 genes, ex-vivo samples show *reduction* in DGE at very low dose vs in vivo; FDXR, PHLDA3, EDA2R show ex-vivo *upregulation* at higher DLP.

## Dose–response

- G11 (§2.2, F3A) — Linear OLS DGE vs DLP in vivo: AEN, FDXR, DDB2, PHLDA3 all p < 0.0001.
- G12 (§2.2, F3) — In-vivo r² ≈ 0.66 (AEN), 0.56 (FDXR) (abstract + §2.2).
- G13 (§2.2, F3B) — BAX in vivo r² = 0.15, p = 0.043; EDA2R r² = 0.14, p = 0.055.
- G14 (§2.2, F3) — Ex-vivo regressions ~3.2× weaker (FDXR cited as exemplary); only FDXR and PHLDA3 ex vivo retain p = 0.009–0.016.
- G15 (§2.2, F3C) — EDA2R has stronger ex-vivo than in-vivo regression (p < 0.0001 ex vivo).
- G16 (§2.2, F4) — Stratify in-vivo into DLP <500 vs ≥500 mGy·cm: significant differences for several genes (specific genes deferred to figure).

## DSB

- D1 (§2.3, TA2) — n=12; mean foci/cell pre = 0.60 ± 0.25, post = 0.70 ± 0.29.
- D2 (§2.3, TA2) — Mean RIF = 0.10 ± 0.15 foci/cell.
- D3 (§2.3) — Pre vs post difference NOT significant: p = 0.37.

## Methods we can audit from XML

- M1 (§4.5) — TaqMan assays listed for each gene (Hs IDs); PUM1 reference; QuantStudio 12K OA; ΔΔCt with pre-exposure in-vivo sample as calibrator.
- M2 (§4.7) — log2 transform; one-sample t / Wilcoxon signed-rank for "differs from zero"; two-sample t / Mann-Whitney where applicable; linear regression for dose–response; α = 0.05.
- M3 (§4.6) — γ-H2AX + 53BP1 colocalized foci, 100 PBMC nuclei/sample, scored by H.S.; RIF = (post avg) − (pre avg) per patient.

## Data availability

- A1 (Data Availability Statement) — "available on request from the corresponding author. The data are not publicly available due to privacy and ethical restrictions."
- A2 — Despite A1, the per-patient DGE matrix and DSB foci counts **are** published inline in Tables A1 and A2 of the open-access JATS XML, which we have harvested. Only the per-patient in-vivo/ex-vivo *labels* are missing.
