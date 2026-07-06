# Artifact Manifest — LUCID100 slot 7

Paper: Wintenberg ME, Manglass LM, Martinez NE, Blenner MA. **Global Transcriptional Response of _Escherichia coli_ Exposed In Situ to Different Low-Dose Ionizing Radiation Sources.** *mSystems* 8:e00718-22 (Mar/Apr 2023). DOI: [10.1128/msystems.00718-22](https://doi.org/10.1128/msystems.00718-22). PMID 36779725 / PMC10134817.

Harvested 2026-06-09 by Ollie LUCID100 wave-1 slot-7 subagent.

## Primary literature

| File | Source | Bytes | SHA256 |
|---|---|---:|---|
| `artifacts/msystems_00718_22.pdf` | Europe PMC render (PMC10134817) | 2,888,980 | `2cb5444731d521ff9c6ca9a9fd6c05ce9b5f6a5b54beffb2cc80301287c9b565` |
| `artifacts/msystems_00718_22.txt` | `pdftotext -layout` of the above | 1,184 lines | `9be4a3406046341d80784a60cf6dc3c32ede5d3a6591748797503f26f085a832` |

ASM open-access PDF endpoint (`journals.asm.org/doi/pdf/...`) returns a Cloudflare-JS challenge HTML wrapper for unauthenticated `curl`; Europe PMC `?pdf=render` is the working programmatic mirror.

## Public transcriptomics data

| File | Source | Bytes | SHA256 |
|---|---|---:|---|
| `artifacts/GSE208658_quick.txt` | NCBI GEO SOFT (series-level) | 60 lines | `88326db471f0b98dfc41faaeca74d4a47db362616d52ffee876b126eaf8d1ad7` |
| `artifacts/GSE208658_samples.txt` | NCBI GEO SOFT (per-sample) | 1,500 lines | `6e0026139a2736a2b1a27e6f797cfa594901149043a4072e215d3bf41df94ae0` |
| `artifacts/GSE208658_Ec_count_matrix.txt.gz` | GEO supplementary | 1,355,105 | `540528a75401cbb6556d450a9bbbfb6b6e657300446ca7916cebb84e22e2aa99` |
| `artifacts/GSE208658_Ec_count_matrix.txt` | gunzipped | 3,404,437 / 4,566 rows × 91 cols | `de9e2b7dc875e4874b4e518854c02b480645ac00c7e5943db5597e5fd38dad55` |

**GEO accession:** [GSE208658](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE208658) (public 2023-02-08).
**BioProject:** [PRJNA860569](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA860569).
**PubMed:** 36779725. **PMC:** [PMC10134817](https://europepmc.org/articles/PMC10134817).

**Samples (n=30):** GSM6360726–GSM6360755. _E. coli_ DH10β, stationary phase. 5 conditions × 2 timepoints × 3 replicates:
- Control (untreated) — D1, D15
- Pu-239 exposure — D1, D15
- H-3 (tritium) exposure — D1, D15
- Fe-55 exposure — D1, D15
- FeCl₃ chemical control (stable-iron analog for Fe-55) — D1, D15

Absorbed dose rate ≈10 mGy/day.

**Count matrix format:** tximport-style produced from StringTie (per the paper's methods). 4,566 gene rows; 91 columns = gene-id + 30×`abundance.*` + 30×`counts.*` + 30×`length.*`. The replication uses only the `counts.*` block, rounded to integers for DESeq2.

## Supplementary materials

Paper mentions Table S1 (read counts) and Fig. S1, S2 inside the PDF supplement bundle. The text-extracted PDF contains the main 11 figures and 4 tables; ASM-hosted supplemental files (`-s001.pdf`, `-s002.xlsx`, etc.) are gated behind the same JS challenge as the PDF. The GEO-deposited count matrix supersedes Table S1 for replication purposes, so we did **not** chase the ASM supplements. Listed here for completeness, not blocked on.

## Code (paper)

No author code repository is cited. The pipeline is described prose-only (Methods, Lines 893–921 of `msystems_00718_22.txt`):
- Trim Galore (v0.6.x) + Cutadapt v2.8 — adapter/quality trimming
- FastQC v0.11.8 — QC
- HISAT2 v2.2.1 — alignment to E. coli K-12 MG1655 RefSeq GCF_000005845.2
- SAMtools v1.4 — BAM handling
- StringTie v1.3.3 — genome-guided assembly + counts
- tximport v1.20.0 — count tables
- DESeq2 v1.35.0 (R) — differential expression
- clusterProfiler — KEGG/GO overrepresentation

## Replication artifacts (this work)

| File | Purpose | SHA256 |
|---|---|---|
| `repro/smoke_de_pydeseq2.py` | PyDESeq2 reimplementation of the 6 paper contrasts | see `repro/sha256.txt` |
| `repro/deg_counts_replication.tsv` | DEG-count comparison vs paper Fig. 2 | see `repro/sha256.txt` |
| `repro/de_tables/<contrast>.tsv` | Full DESeq2 result table per contrast (4,566 genes × `baseMean,log2FoldChange,lfcSE,stat,pvalue,padj`) | see `repro/sha256.txt` |
| `repro/sha256.txt` | All hashes | self |

See `FIRST_PASS_REPORT.md` for the verdict and acceptance evaluation.
