# Artifact Manifest — LUCID100 Wave 2, slot 13

**Paper.** Ruiz-Fernández de Córdoba, Valencia, Welch, Moreno *et al.*
*Dual ENPP1/ATM depletion blunts DNA damage repair boosting radioimmune
efficacy to abrogate triple-negative breast cancer.*
Signal Transduction and Targeted Therapy 10:185 (2025). DOI:
[10.1038/s41392-025-02271-2](https://doi.org/10.1038/s41392-025-02271-2).
Licence: CC BY 4.0.

**Harvest date:** 2026-06-09 (CDT). **Harvester:** subagent slot 13.

## Primary artifacts (locally held)

| Path | Kind | SHA-256 | Source | Notes |
| --- | --- | --- | --- | --- |
| `artifacts/paper.pdf` | PDF | `6b99d371c40d6f56689a2781682a65a347a69a5a6114ef211bb4bd735cecf02b` | `https://www.nature.com/articles/s41392-025-02271-2.pdf` | Full main text. Open access. |
| `artifacts/paper_layout.txt` | text | (regenerated) | `pdftotext -layout paper.pdf` | 777 lines. |
| `artifacts/supp_MOESM1_ESM.docx` | DOCX | `ff101b6f2c0db53f01dad7e7a1066d47498dd34dfe30c9285ed3d0c0e7d7dd63` | Springer static-content | Materials & Methods companion + EndNote citations. 18.8 MB (heavy with embedded fonts/citations). |
| `artifacts/supp_MOESM1_ESM.txt` | text | (regenerated) | XML-stripped from the docx | 221 lines of usable text. |
| `artifacts/supp_MOESM2_ESM.pdf` | PDF | `60e55f2d5a8a36f3cb675009ed10903bdb4ac3e6832363b2491b98507564d452` | Springer static-content | Supplementary Figures S1–S7 + Tables S1–S8 (antibody list, IHC conditions, **drug screen list S5/S6**, shRNA target sequences, primer sequences). |
| `artifacts/supp_MOESM2_ESM.txt` | text | (regenerated) | `pdftotext -layout` | 668 lines. |
| `data/GSE277249_RAW.tar` | TAR (uncompressed featureCounts inside) | `93ae9f92a4325274560fe50316cd6225cca4981ff210cb0d544050df17347a89` | NCBI GEO FTP, `ftp.ncbi.nlm.nih.gov/geo/series/GSE277nnn/GSE277249/suppl/GSE277249_RAW.tar` | 68 MB. Despite the *RAW* label, contents are 18 **gene-level featureCounts** files (one per sample), produced by the authors with featureCounts v1.6.0 against GENCODE vM32. No FASTQ. |
| `data/GSE277249_filelist.txt` | text | `d32e1dcfaccc79e9259695d5fd389be550d15e32d3b3f6a69879ec5a2ba2af42` | same FTP dir | Lists the 18 GSM-prefixed count files. |
| `data/GSE277249_series_matrix.txt.gz` | gzipped text | `06a7c9715a2a059c65d4e32b23d1649fd92ff0e3efdb1f3549bf0775fb80ed4d` | NCBI GEO FTP `matrix/` | Series-level metadata only (no expression data — the matrix file is only 2.5 kB). |
| `data/counts/GSM851711[3-9]…GSM851713[0]_*.counts.txt` | text | n/a | extracted+gunzipped from `GSE277249_RAW.tar` | 18 files, each `Geneid Chr Start End Strand Length COUNTS`. |

## Derived files (regenerable from `code/`)

| Path | Source | Notes |
| --- | --- | --- |
| `results/counts_matrix.tsv` | `code/01_build_matrix.py` | 56,953 genes × 18 samples + a `Length` column. |
| `results/sample_sheet.tsv` | `code/01_build_matrix.py` | sample, cell_line, group (parental \| CTC_in), parental (ANV5 \| 4T1), lineage. |
| `results/ensembl_symbol_mouse.tsv` | `code/02_smoke_deg.py` (mygene cache) | Ensembl→symbol map for all 56,953 genes. |
| `results/deg_ANV5.tsv` | `code/02_smoke_deg.py` | PyDESeq2 contrast (CTC_in vs parental) in ANV5 family. |
| `results/deg_4T1.tsv` | `code/02_smoke_deg.py` | PyDESeq2 contrast (CTC_in vs parental) in 4T1 family. |
| `results/hypothesis_check.json` | `code/02_smoke_deg.py` | Per-hypothesis pass/fail summary. |
| `results/enrichr_common_up/` | `code/02_smoke_deg.py` | gseapy.enrichr output on the up-DEG intersection. |
| `figures/fig1_pca.png` | `code/02_smoke_deg.py` | PCA on top-2000 variable genes. |
| `figures/fig2_enpp1_counts.png` | `code/02_smoke_deg.py` | ENPP1 raw counts (log scale), grouped by cell line. |
| `figures/fig3_signature_heatmap.png` | `code/02_smoke_deg.py` | Row-z-score heatmap of the paper's Fig. 1c signature genes. |

## Sample → cell line decoding (GSE277249)

Decoded unambiguously from filename prefixes (`{prefix}1`, `{prefix}2`, `{prefix}3`):

| Filename prefix | Cell line | Group | Parental |
|---|---|---|---|
| `ANV51 / ANV52 / ANV53` | ANV5_parental | parental | ANV5 |
| `M7001 / M7002 / M7003` | CTC700 | CTC_in | ANV5 |
| `M8031 / M8032 / M8033` | CTC803 | CTC_in | ANV5 |
| `M4t11 / M4t12 / M4t13` | 4T1_parental | parental | 4T1 |
| `M15891 / M15892 / M15893` | CTC1589 | CTC_in | 4T1 |
| `M15921 / M15922 / M15923` | CTC1592 | CTC_in | 4T1 |

Cross-referenced against the paper's per-cell-line nomenclature
(700Cy1 / 803Cy1 / 1589Cy1 / 1592Cy1) and against `GSE277249` series
metadata (`!Series_overall_design = Triplicates of each different cell
line or derivatives were used`).

## External dependencies needed for STRICT replication (not bundled)

| Resource | Used for | Access |
| --- | --- | --- |
| **R / Bioconductor `limma`** | Reproduce the paper's `B > 5` moderated-t statistic exactly. The paper does NOT specify the exact pipeline (likely STAR → featureCounts → limma-voom). | Free, public; can run locally. |
| **EGAD00001006608** (Bassez *et al.* *Nat. Med.* 2021 scRNA-seq) | Replicate Fig. 6 (UMAP of 31 human breast cancer tumors, ENPP1 expression by cell compartment). | **EGA controlled access** — requires data-access committee (DAC) request. NOT done in this pass. |
| **ctcRbase** (Zhao *et al.* 2020) + GSE41245 (Lang *et al.* 2017) | Supp. Fig. 1a ENPP1 levels in breast cancer CTCs vs primary tumors. | Free; GSE41245 is public on GEO. Not yet retrieved. |
| **TCGA-BRCA bulk RNA-seq** (PanCancer Atlas) | Cross-check ENPP1+ signature in human TNBC. Paper text claims correlation; can be done via cBioPortal API or GDC. | Free, public. |
| **GENCODE vM32 GTF** | Re-run featureCounts from raw FASTQ if needed (NOT in scope — raw FASTQ is not deposited at GEO, would need SRA pull via BioProject **PRJNA1161492**). | Free, public. |

## What is NOT available

- **No raw FASTQ on GEO.** The "RAW" tar contains processed gene-level
  counts only. Raw reads live in SRA under BioProject `PRJNA1161492`
  (referenced in the GEO record). A full alignment re-run would
  require ~50–200 GB of FASTQ and would not change any biological
  conclusion in this scope.
- **No code repository.** No GitHub, Zenodo, Figshare, OSF link
  anywhere in the paper or supplementary files. Confirmed by full-text
  grep of `paper_layout.txt` and both supplementary text dumps.
- **No published DEG / signature tables.** Fig. 1c is a heatmap; the
  underlying gene lists are not deposited as a supplementary table.
- **No raw functional data.** Clonogenic assays, comet-assay tail
  moments, γH2AX immunoblots, in vivo tumor measurements, IHC
  quantifications, and the drug-synergy plate readouts (Fig. 3) are
  embedded as figure panels only; raw numeric data are not deposited.

## Cross-reference to LUCID100 master row

| LUCID100 field | Value |
|---|---|
| Wave / slot | Wave 2 / 13 |
| Tier | A |
| Source | semantic_scholar |
| DOI | 10.1038/s41392-025-02271-2 |
| Year | 2025 |
| Journal | Signal Transduction and Targeted Therapy |
| Themes | DNA repair / DDR; radiation quality / RBE; omics / signatures; immune / inflammation / senescence |
| LUCID tag | omics/signature replication |
| LUCID TODO | artifact harvest; brief; run; report |
| QA tag | KEEP: relevant and replication-plausible |
