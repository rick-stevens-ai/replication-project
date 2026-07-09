# PROGRESS — Grandt et al. 2022 (KiKme) replication

- **Status:** **completed**
- **Started:** 2026-05-30 18:10 CDT
- **Completed:** 2026-05-30 18:25 CDT
- **Target:** Grandt CL et al., *Molecular Medicine* 28:105 (2022). DOI 10.1186/s10020-022-00520-6
- **Output dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-grandt-fibroblast-rnaseq/`

## Done
- [x] Read paper PDF (4 MB, full text)
- [x] Checked data availability — no GEO/SRA accession; only supplementary materials.
- [x] Downloaded all 13 BMC supplementary files (`code/00_download.sh`).
- [x] Converted Additional File 1 (50 k DEG rows + 118 k interaction rows) to TSV.
- [x] Replicated DEG counts: **exact match** for all 9 reported (group × dose × model 1) combinations.
- [x] Replicated %Up: **exact match** to 2 decimals.
- [x] Replicated top-FDR gene lists: 11/12 overlap in every group.
- [x] Replicated all 7 interaction genes at 2 Gy.
- [x] Independent pathway ORA (Fisher right-tail) using embedded MSigDB annotations.
- [x] Built 3 publication-quality figures.
- [x] Wrote REPORT.md, README.md, updated progress JSON.

## Verdict
**PARTIAL (strong)** — Coverage 8/10, Agreement 9/10.

Excellent within the scope allowed by the data the authors made public. Cannot touch raw FASTQ pipeline (none deposited) or proprietary IPA scores, but every numerical/biological claim checkable from the supplementary tables passes.
