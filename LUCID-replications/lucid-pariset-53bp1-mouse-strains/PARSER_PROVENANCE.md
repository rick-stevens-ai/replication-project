# Parser Provenance — Pariset et al. 2020 replication

**Paper DOI:** 10.1667/RADE-20-00122.1
**Source PDF:** `data/paper.pdf` (12 MB, 16 pages, downloaded from BioOne 29 Jan 2025)

## Canonical Marker / Nougat output
- Searched: `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/`
- **Result:** No directory matching `10_1667_RADE*` or `10.1667/RADE-20-00122.1`.
- Canonical Marker output is **NOT AVAILABLE** for this paper as of 2026-06-23.

## Parser actually used (re-pass 2026-06-23)
- **Tool:** `pdftotext` (Poppler), called twice:
  - `pdftotext -layout data/paper.pdf data/repass/paper_layout.txt` (preserves columns, used for table parsing)
  - `pdftotext data/paper.pdf data/repass/paper_plain.txt` (plain reading order, used for prose grep)
- Both extractions completed cleanly (no decode errors).
- Output sizes: layout 780 lines, plain 1223 lines.
- All paper-reported numbers used in the re-pass (LET values 104 / 170 keV/μm, prefactors b/Cl = 12.8 DSB/Gy, Eq. 3 prefactor 1.28, dose-response factors 7.2× and 1.7×, Table 1B r = −0.75, Table 2 4×4 cell assignments, Fig. 7B r = 0.61, Fig. 7C per-organ r values) were verified against `paper_layout.txt`.

## Original-pass parser (May 30)
- The original pass also used `pdftotext -layout` plus per-page image OCR for Fig. 4 (vision-digitized to `data/digitized_fig4.csv`) and Fig. 7C (vision-digitized to `data/fig7c_cancer_correlations.csv`).
- The pre-existing digitized CSV files were re-used by the re-pass (regression-checked: r(τ_4Gy, q_4Gy) = −0.758, identical to prior pass).

## Why no Marker re-parse
- The LUCID-100 admin Marker batch has not yet processed this DOI.
- `pdftotext -layout` already preserves every numerical claim needed for the re-pass (verified by manual spot-check against the source PDF for Eq. 3, Table 2, and Fig. 7B/7C captions).
- No additional information would be unlocked by re-running Marker on a fresh GPU pass for this paper.
