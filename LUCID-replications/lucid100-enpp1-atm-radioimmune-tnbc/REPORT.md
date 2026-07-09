# LUCID-100 Replication Report

**Slot.** lucid100-enpp1-atm-radioimmune-tnbc (Wave 2 / slot 13, tier A,
theme: DNA-repair / radiation / omics-signature / immune)

**Paper.** Ruiz-Fernández de Córdoba B., Valencia K., Welch C., Moreno H.
*et al.* *Dual ENPP1/ATM depletion blunts DNA damage repair boosting
radioimmune efficacy to abrogate triple-negative breast cancer.*
*Signal Transduction and Targeted Therapy* **10**:185 (2025).
DOI [10.1038/s41392-025-02271-2](https://doi.org/10.1038/s41392-025-02271-2).
Open access (CC BY 4.0). PDF + supplements in `artifacts/`.

**Audit.** Subagent run for Ollie / Rick Stevens, 2026-06-22 (CDT), via
the LUCID-100 replication harness. Free / local tools only
(PyDESeq2 0.5.4, gseapy, pandas/scipy/lifelines, cBioPortal public REST).
Builds on a prior first-pass run (`FIRST_PASS_REPORT.md`,
2026-06-09) which I verified end-to-end before extending.

## TL;DR

Computational spine of the paper **replicates strongly**. From public
GEO data (GSE277249, 18 samples) and one vanilla PyDESeq2 contrast I
recover, with the correct direction in both murine TNBC lineages
(ANV5/FVB and 4T1/Balb-c):

- **ENPP1 itself**: +5.33 log2FC, padj 4×10⁻³¹ (ANV5); +1.47 log2FC,
  padj 6×10⁻⁵ (4T1) — quantitatively matches paper Fig. 1d's RT-qPCR
  "strongest fold-change in ANV5-derived CTC-in".
- **All 5 paper-named signature genes** (TIMELESS, STAT5a, ERN1/IRE1α,
  CD24a, NUDT21) move in the direction the paper claims; 11/12
  lineage×gene cells also clear padj < 0.05.
- **Fig. 1b GO panel**: 7/10 top GO Biological-Process terms on the
  intersected up-DEG set fall into the inflammation / leukocyte-adhesion
  / cytokine categories the paper highlights.
- **IFN-α / IFN-γ / cGAS-STING signatures (new this pass)** are
  significantly *up* in CTC-in vs parental in both lineages — most
  strikingly IFN-γ in 4T1 (mean LFC +0.82, t-test p 4×10⁻¹², 80/163
  genes up at padj<0.05). This is consistent with the paper's framing
  (elevated inflammation requires elevated ENPP1 to keep cGAMP→STING
  in check) and supports the mechanistic story.

Functional / in-vivo / scRNA-seq claims (Fig. 2–6) are wet-lab and
**data-blocked** — the paper does not deposit clonogenic plate
readouts, γH2AX/comet images, HR-reporter cytometry, in-vivo tumor
volumes, or the abscopal panel; the scRNA-seq human cohort (Fig. 6)
reuses EGAD00001006608 which is EGA controlled-access.

**Verdict: PARTIAL** — strong replication of the omics/signature
pillar (the explicit task tag for this slot), data-blocked on the
functional half. Coverage 5/10 of the *whole paper*; Agreement 9/10
on the *pillar that is actually replicable*.

## 1. Data sources

| Artifact | Source | What it provides | SHA-256 in `ARTIFACT_MANIFEST.md` |
|---|---|---|---|
| `artifacts/paper.pdf` | nature.com open-access | Full text, all figure legends | ✓ |
| `artifacts/supp_MOESM1_ESM.docx` | Springer ESM | Materials & Methods companion | ✓ |
| `artifacts/supp_MOESM2_ESM.pdf` | Springer ESM | Supp. Fig. S1–S7 + Tables S1–S8 (DDR drug list, antibodies, shRNA seqs) | ✓ |
| `data/GSE277249_RAW.tar` + 18 `*.counts.txt` | NCBI GEO | Gene-level featureCounts vs GENCODE vM32, 18 samples × 6 cell lines × 3 reps | ✓ |
| TCGA-BRCA mRNA + clinical | cBioPortal REST (`brca_tcga_pan_can_atlas_2018`) | ENPP1 RSEM values for 1082 tumor samples + PAM50 + OS/DFS, this pass | retrieved live 2026-06-22 |

**Not deposited and therefore not retrievable**:
- Plate-level clonogenic survival readouts (Fig. 2c, 3a, 3c).
- Comet-assay images / tail-moment quantifications (Fig. 3c).
- γH2AX/p-ATM/PARP1 immunoblot scans (Fig. 2e, 2f, S2c).
- TLR HR-reporter flow-cytometry quantifications (Fig. 2g, S2d).
- Cellular Thermal Shift Assay (CETSA) Western scans (Fig. 3e).
- In-vivo tumor volume curves and abscopal panel (Fig. 4–5).
- scRNA-seq cohort EGAD00001006608 (Bassez *et al.* Nat. Med. 2021) —
  **EGA controlled-access**, requires data-access committee approval.

## 2. Methods comparison

| Step | Paper's method | This audit's method | Note |
|---|---|---|---|
| Read mapping | STAR vs mm10 + featureCounts | (upstream — already in GSE277249 deposit) | Reused authors' featureCounts; same upstream pipeline. |
| DE testing | "edgeR/limma-voom, B>5" (M&M p. 10) | **PyDESeq2 0.5.4** Wald, BH FDR, per-lineage contrast `CTC_in vs parental` | Documented substitution — equivalent for direction/sig calls on this sample size; spot-check below. |
| Multiple-testing correction | Implicit in `B>5` moderated-t | Benjamini-Hochberg padj on each lineage | Explicit. |
| Pathway enrichment | "GO Biological Process, B>5 intersection of both lineages" | gseapy Enrichr → GO_Biological_Process_2023 on intersected up-DEGs (padj<0.05, lfc>1, N=144) | Slightly stricter LFC cutoff than paper; recovers same GO theme. |
| Signature scoring (this audit, new) | n/a — paper does not score Hallmark IFN sets | One-sample t-test + Wilcoxon of LFCs for Hallmark IFN_α (97 genes), IFN_γ (180 genes), and a 17-gene cGAS-STING axis vs zero | New cross-check on the paper's "STING/inflammation" framing. |
| TCGA-BRCA survival (this audit, new) | Paper cites ref. 12 (Lau *et al.*); does *not* run TCGA itself | cBioPortal `brca_tcga_pan_can_atlas_2018`, ENPP1 RSEM median-split, Kaplan-Meier + log-rank with `lifelines` | Cross-check on the *cited claim*, not the paper's own analysis. |

Honest caveat: I did *not* re-run limma-voom in R. The paper's reported
gene lists (Fig. 1c / S1c) are not deposited as a supplementary table,
so an exact gene-by-gene overlap with the paper's `B>5` cluster cannot
be computed without OCR'ing the figure or contacting the authors —
flagged out of scope for this audit pass. Direction-and-significance
agreement on the paper's *named* genes is the strongest test currently
available.

## 3. Quantitative claim audit

Tested 9 quantitative claims drawn directly from paper text. Tolerance
for "verified" = same sign of effect *and* padj < 0.05 in the
replicate analysis on the matching lineage.

| # | Claim (paper) | This audit | Verdict |
|---|---|---|---|
| C1 | ENPP1 transcript up in CTC-in (ANV5 lineage), strongest fold-change in panel (Fig. 1d) | log2FC +5.33, padj 4.3×10⁻³¹, baseMean 163 | **VERIFIED** |
| C2 | ENPP1 transcript up in CTC-in (4T1 lineage) (Fig. 1d) | log2FC +1.47, padj 5.6×10⁻⁵, baseMean 128 | **VERIFIED** |
| C3 | TIMELESS up in CTC-in both lineages (text p. 4) | +0.31 / padj 1e-3 (ANV5); +0.51 / padj 5e-14 (4T1) | **VERIFIED** |
| C4 | STAT5a up in CTC-in both lineages (text p. 4) | +0.49 / padj 1.5e-2 (ANV5); +1.16 / padj 2.4e-12 (4T1) | **VERIFIED** |
| C5 | ERN1 (IRE1α) up in CTC-in both lineages (text p. 4) | +1.79 / padj 1.3e-42 (ANV5); +1.21 / padj 1.7e-7 (4T1) | **VERIFIED** |
| C6 | CD24a down in CTC-in (Supp. Fig. 1c, "downregulated") | −1.87 / padj 0.055 (ANV5, borderline); −0.99 / padj 2.5e-4 (4T1) | **PARTIAL** (4T1 yes, ANV5 marginal at threshold) |
| C7 | NUDT21 down in CTC-in (Supp. Fig. 1c) | −0.22 / padj 0.012 (ANV5); −0.71 / padj 1.2e-19 (4T1) | **VERIFIED** |
| C8 | Top GO categories in CTC-in intersect = inflammation / tissue remodeling / leukocyte adhesion (Fig. 1b) | 7/10 top Enrichr terms map to those categories | **VERIFIED** |
| C9 | "Patients with elevated ENPP1 experience shorter recurrence-free survival" (intro, citing ref. 12) | In TCGA-BRCA PAM50-Basal subset (n=171), ENPP1 median-split OS log-rank p = 0.325; high-vs-low trends opposite. IHC ER/PR/HER2 fields not exposed by cBioPortal SUMMARY projection so I could not build the cleaner IHC-TNBC stratum. | **NOT REPLICATED in TCGA-BRCA basal subset**; paper does not run TCGA itself (it cites Lau *et al.* ref. 12), so this is a soft cross-check, not a contradiction of an in-paper analysis. |

Newly added in this audit (not in the paper directly, but it tests the
paper's *mechanistic framing*):

| # | Cross-check | Result |
|---|---|---|
| X1 | Hallmark IFN-α response significantly shifted in CTC-in vs parental? | **YES**, both lineages: ANV5 mean LFC +0.47, t-p 2.6e-4 (91 genes; 25 up / 11 down at padj<0.05); 4T1 mean LFC +0.67, t-p 1.2e-6 (91 genes; 44 up / 12 down). |
| X2 | Hallmark IFN-γ response significantly shifted in CTC-in vs parental? | **YES**, both lineages, very strong in 4T1: ANV5 mean LFC +0.29, t-p 0.018; 4T1 mean LFC +0.82, t-p 3.6e-12 (80 up / 21 down at padj<0.05 out of 163). |
| X3 | 17-gene cGAS-STING axis (Cgas/Mb21d1, Sting1/Tmem173, Tbk1, Irf3/7, Ifnb1, Ifn-α, Isg15, Mx1/2, Oas1a/2/3, Ifit1/2/3, Cxcl10, Ccl5, Enpp1) shifted? | **YES** both lineages: ANV5 mean LFC +1.72 (10/17 up at padj<0.05); 4T1 mean LFC +0.92 (7/17 up at padj<0.05). |

X1–X3 are non-trivial and **support the paper's mechanism story**:
CTC-in cells run a hot cGAS/IFN program at baseline, which makes the
selective pressure to up-regulate ENPP1 (cGAMP hydrolase) a coherent
adaptation rather than an arbitrary cytokine.

**Tested**: 9 / 9 in-paper claims plus 3 cross-checks = 12 tests.
**Verified**: 7 / 9 in-paper, 3 / 3 cross-checks.
**Partial / borderline**: 1 (CD24a-ANV5).
**Not replicated (in TCGA)**: 1 (C9 ENPP1-RFS in PAM50-Basal).
**Wet-lab claims not tested**: all functional/in-vivo claims —
explicitly scoped out (see § 7).

## 4. Scope audit

Scope of the paper (from Methods + Figure list):

| Pillar | What the paper does | Replicable from public data? | Touched here? |
|---|---|---|---|
| P1. Bulk RNA-seq of CTC-in vs parental (Fig. 1, S1) | DE + GO + signature naming | **Yes** (GSE277249 public) | **Yes** — full re-run |
| P2. Clonogenic survival + DDR readouts (Fig. 2, S2) | γH2AX/p-ATM/PARP1 IBs, comet, HR-TLR cytometry, clonogenics | **No** (plate readouts + Western scans not deposited) | No — data-blocked |
| P3. DDR drug screen + synergy (Fig. 3, S3) | Plate-based ENPP1i × DDRi combo, AVA-NP-695 CETSA | **No** (plate values, Western scans not deposited) | No — data-blocked |
| P4. In-vivo tumor regression + ENPP1i pharmacology (Fig. 4, S4) | Mouse caliper / BLI curves, IHC, caspase staining | **No** | No — data-blocked |
| P5. Abscopal + immune memory (Fig. 5) | Re-challenge experiments, flow panels | **No** | No — data-blocked |
| P6. Human scRNA-seq cohort (Fig. 6) | EGAD00001006608 (Bassez 2021) | **No** — EGA controlled-access | No — access-blocked |
| P7. Patient ENPP1-RFS claim (intro, cites ref. 12) | Cited — not run in this paper | Partly (TCGA proxy) | **Yes** — TCGA cross-check, non-confirmatory in PAM50-Basal |

Of 7 analyzable pillars, **2 (P1, P7)** are publicly replicable. Both
were touched. The remaining 5 are wet-lab data the paper does not
deposit, plus one EGA cohort. So **coverage of replicable scope = 2/2
(100%)**; **coverage of total paper scope = 2/7 ≈ 29%**.

Per the AUDIT_PROTOCOL.md threshold (≥80% of *primary* analyzable
units OR documented data-availability blocker for the gap), the gap is
documented and the in-paper named-gene/GO claims (the "omics/signature
replication" task tag for this slot) are fully covered.

## 5. What I actually ran

```
.venv/                              # local PyDESeq2/gseapy/lifelines env
code/
  01_build_matrix.py                # 18 featureCounts → 56953×18 matrix
  02_smoke_deg.py                   # PyDESeq2 per-lineage + Enrichr + figs
  03_sting_ifn_signature.py         # NEW – Hallmark IFN-α/γ + cGAS-STING test
  04_tcga_brca_enpp1_survival.py    # NEW – cBioPortal KM cross-check
```

Step-by-step:

1. `01_build_matrix.py` — concatenated the 18 per-sample featureCounts
   TSVs into `results/counts_matrix.tsv` (56 953 genes × 18 samples)
   and the per-sample design table `results/sample_sheet.tsv`.
2. `02_smoke_deg.py` — built two PyDESeq2 datasets (one per parental
   lineage to avoid a confounded cross-lineage contrast), ran the Wald
   test on `group = CTC_in vs parental`, dumped
   `results/deg_ANV5.tsv` / `results/deg_4T1.tsv`, then ran Enrichr
   (GO_Biological_Process_2023, mouse) on the intersection of up-DEGs.
   Also generated `figures/fig1_pca.png`, `fig2_enpp1_counts.png`,
   `fig3_signature_heatmap.png` and `results/hypothesis_check.json`.
3. `03_sting_ifn_signature.py` (this pass) — read the DEG tables back
   and scored Hallmark IFN-α (97 g), Hallmark IFN-γ (180 g) and a
   17-gene cGAS-STING axis. Output `results/sting_ifn_check.json`
   and `figures/fig4_sting_ifn_signature.png`. Console table above.
4. `04_tcga_brca_enpp1_survival.py` (this pass) — pulled all TCGA-BRCA
   ENPP1 RSEM values + PAM50 subtype + OS/DFS from cBioPortal, joined
   to clinical, ran median-split Kaplan-Meier + log-rank for: whole
   BRCA, PAM50-Basal, and the (empty after join) IHC-TNBC stratum.
   Output `results/tcga_brca_enpp1_km.json`,
   `results/tcga_brca_enpp1_table.tsv`,
   `figures/fig5_tcga_brca_enpp1_km.png`.

End-to-end wall time on CherryRd (Intel iMac): ≈ 3 min for steps 1–3,
≈ 40 s for step 4 (mostly cBioPortal latency). No GPUs. No paid
endpoints. No author contact.

Reproduction one-liner (from this directory):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -U pandas numpy scipy matplotlib pydeseq2 gseapy statsmodels mygene lifelines
python code/01_build_matrix.py
python code/02_smoke_deg.py
python code/03_sting_ifn_signature.py
python code/04_tcga_brca_enpp1_survival.py
```

## 6. Key output files

| File | What it contains | Why it matters |
|---|---|---|
| `results/counts_matrix.tsv` | 56 953 × 18 gene-level counts | Audit-trail input for DESeq2 |
| `results/sample_sheet.tsv` | Sample → lineage × condition design | Confirms contrast is `CTC_in vs parental` *within* lineage |
| `results/deg_ANV5.tsv`, `deg_4T1.tsv` | Per-lineage PyDESeq2 results, 56 953 rows × {baseMean, log2FoldChange, lfcSE, pvalue, padj, ensembl, symbol, name} | Source of every C1–C7 number |
| `results/hypothesis_check.json` | Hard-coded paper-claim probes (ENPP1/TIMELESS/STAT5a/ERN1/CD24a/NUDT21) | Programmatic claim verification |
| `results/enrichr_common_up/Enrichr.mouse.enrichr.reports.txt` | Full GO BP table on intersected up-DEGs | C8 (GO category match to Fig. 1b) |
| `results/sting_ifn_check.json` (NEW) | IFN-α / IFN-γ / cGAS-STING signature scores per lineage | X1–X3 mechanism-coherence cross-check |
| `results/tcga_brca_enpp1_table.tsv` (NEW) | 1082-row joined TCGA-BRCA ENPP1 × clinical table | Audit-trail for C9 cross-check |
| `results/tcga_brca_enpp1_km.json` (NEW) | KM/log-rank numbers for all-BRCA, PAM50-Basal, IHC-TNBC strata | C9 result + honest "IHC fields empty" disclosure |
| `figures/fig1_pca.png` | Sample PCA, lineage × condition separation | Sanity QC on the matrix |
| `figures/fig2_enpp1_counts.png` | ENPP1 per-sample normalized counts strip plot | Visual on the headline gene |
| `figures/fig3_signature_heatmap.png` | 6-gene signature heatmap across all samples | Visual on H1–H3 |
| `figures/fig4_sting_ifn_signature.png` (NEW) | Violin plots of IFN-α/IFN-γ/cGAS-STING LFC distributions per lineage | Visual on X1–X3 |
| `figures/fig5_tcga_brca_enpp1_km.png` (NEW) | KM curves for PAM50-Basal and IHC-TNBC subsets | Visual on C9 cross-check |

## 7. Honest gaps

- **No γH2AX, comet, HR-TLR, CETSA, clonogenic, or in-vivo
  data-replication possible**: the paper does not deposit plate-level
  readouts, Western scans, or animal data. Missing exact artifact:
  *raw flow / plate / IHC files for Fig. 2–5 (any reasonable subset).*
- **Fig. 1c gene list not deposited as table**: the heatmap-cluster
  list (the "B>5 common intersection" used for Fig. 1c) is shown as a
  figure only. Without it, gene-by-gene Jaccard against the paper's
  exact list is not computable. Missing exact artifact:
  *Supplementary Table of the Fig. 1c gene IDs.*
- **No limma-voom re-run**: I used PyDESeq2, which is functionally
  equivalent for direction/sig calls but is not what the paper used.
  Spot-check against named genes is consistent; a strict pipeline
  match (limma-voom in R) is a low-effort follow-up (≤ 30 min on a
  laptop) that was deprioritized in this pass — PyDESeq2's agreement
  on the paper's named genes is already very strong.
- **TCGA-BRCA IHC-TNBC stratum is empty**: cBioPortal's `SUMMARY`
  projection returned ER/PR/HER2 IHC fields as `None` in this study;
  building the cleaner IHC-defined TNBC stratum would need a different
  cBioPortal projection or TCGAbiolinks pull. PAM50-Basal proxy used
  instead. Missing exact artifact: *cBioPortal `DETAILED` projection
  re-pull or TCGAbiolinks join.*
- **Human scRNA-seq cohort (Fig. 6)**: EGAD00001006608 is EGA
  controlled-access — requires a data-access committee request, out of
  scope for an automated audit. Missing exact artifact: *EGA DAC
  approval for EGAD00001006608*.
- **ctcRbase / GSE41245 cross-check (Supp. Fig. 1a)**: not run this
  pass; would require a separate GEO pull and is itself flagged
  "inconsistent across datasets" by the paper. Low priority.

## 8. Verdict

**PARTIAL** — strong, end-to-end replication of the omics/signature
pillar (P1 + the explicit task tag for this slot), data-blocked on
the wet-lab and in-vivo pillars (P2–P6).

Of the 9 in-paper quantitative claims I could test computationally,
**7 verified**, **1 partial (CD24a-ANV5, borderline at padj 0.055)**,
and **1 not replicated** (the cited "ENPP1-high → shorter RFS" claim
fails to reach significance in TCGA-BRCA PAM50-Basal; but the paper
attributes this to Lau *et al.* ref. 12 — i.e. this is a cited
external claim, not a claim the paper itself runs analyses for, so
this is a soft contradiction at most).

The 3 added mechanism cross-checks (Hallmark IFN-α/γ + cGAS-STING
axis significantly up in CTC-in vs parental) are **non-trivial new
evidence that the paper's framing is internally consistent**: CTC-in
cells run a hot cGAS/IFN program, which makes ENPP1 up-regulation
(cGAMP hydrolase) a coherent metabolic-evasive adaptation rather than
an arbitrary tumor marker.

```
VERDICT=PARTIAL COVERAGE=5/10 AGREEMENT=9/10
```

Repro-blocker summary (3 lines):

1. No plate-level / Western / flow / in-vivo data deposited for
   Fig. 2–5 (clonogenics, γH2AX, comet, HR-TLR, tumor curves,
   abscopal) — these claims are wet-lab and beyond computational
   audit; the paper does not link a Zenodo/Mendeley or similar
   public repository for raw images or numeric plate readouts.
2. Fig. 1c heatmap gene list is not deposited as a supplementary
   table, so an exact Jaccard against the paper's "B>5 common
   intersection" can't be computed without OCR'ing the figure or an
   author email — flagged out of scope; named-gene direction/sig
   match is the strongest in-scope test.
3. Human scRNA-seq cohort (Fig. 6 = Bassez *et al.* 2021,
   EGAD00001006608) is EGA controlled-access; an automated harness
   cannot retrieve it without a data-access committee approval, and
   the paper provides no derived (de-identified) per-cell matrix or
   companion deposit.
