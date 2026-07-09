# Progress — Dual ENPP1/ATM Depletion in TNBC (LUCID100 Wave 2, slot 13)

## Status

- **Current phase:** First-pass artifact harvest + scoping complete;
  minimal smoke replication run end-to-end.
- **Verdict (first pass):** **GREEN — partial (strong)**. All 6 named
  paper-signature genes recovered with correct direction in both lineages
  using PyDESeq2 on the deposited counts.
- **Owner:** LUCID100 Wave 2, slot 13 subagent.
- **Heavy compute?** Not needed. ~57k genes × 18 samples; PyDESeq2 runs
  on a laptop in ~30 s.
- **External writes / paid endpoints?** None. No author contact.

## Log

### 2026-06-09 — subagent run (CherryRd, depth 1/1)

- Looked up slot 13 in `LUCID100_SOLID_MASTER_QA.tsv` (Wave 2, tier A,
  candidate_curated; tag *omics/signature replication*).
- Confirmed the paper is open-access on Nature (`/articles/s41392-025-02271-2`)
  and grabbed `artifacts/paper.pdf` directly (7.5 MB,
  sha256 `6b99d371...`). Extracted full text with `pdftotext -layout`
  (777 lines).
- Located **DATA AVAILABILITY** line: *"RNA-seq data have been deposited
  under the accession code GSE277249."* No GitHub / Zenodo / Figshare
  code repository is mentioned anywhere. Methods section + supplementary
  pdf cross-checked.
- Harvested supplementary files from Springer:
  - `supp_MOESM1_ESM.docx` (18.8 MB) — Materials & Methods companion.
  - `supp_MOESM2_ESM.pdf`  (7.7 MB) — Figures S1–S7 + Tables S1–S8.
  - MOESM3–MOESM12 probed but 403 — only two supplementary objects exist.
- Pulled GSE277249 from NCBI GEO FTP:
  - `GSE277249_RAW.tar` (68 MB) — **per-sample featureCounts gene tables**
    (NOT raw FASTQ), 18 samples, ~57k Ensembl genes, featureCounts v1.6.0
    against GENCODE vM32.
  - `GSE277249_filelist.txt`, `GSE277249_series_matrix.txt.gz`.
  - Sample-to-cell-line decoding inferred unambiguously from filenames
    (`ANV5*`, `M700*`, `M803*`, `M4t1*`, `M1589*`, `M1592*` — 3 reps each).
- Wrote `code/01_build_matrix.py`: built the 56,953 × 18 count matrix and
  the sample sheet.
- Wrote `code/02_smoke_deg.py`: PyDESeq2 CTC-in vs parental within each
  lineage; gene-symbol mapping via mygene; Enrichr GO BP enrichment via
  gseapy; PCA + ENPP1 strip plot + signature-gene heatmap.
- **Headline result:**
  - ENPP1: lfc=+5.33 (padj 4e-31) in ANV5 family; +1.47 (padj 6e-5) in 4T1.
  - TIMELESS, STAT5a, ERN1: all up in both lineages, padj < 0.05 in both.
  - CD24a, NUDT21: both down in both lineages (CD24a misses padj 0.055 in
    ANV5 but is highly significant in 4T1; NUDT21 padj < 1e-19 in 4T1).
  - Common-up Enrichr GO BP top hits: **Leukocyte cell-cell adhesion,
    Neutrophil chemotaxis/migration, Granulocyte chemotaxis,
    Response to LPS** — directly matching paper Fig. 1b "Regulation of
    inflammatory response" + "Tissue remodeling".
- 5,022 padj-significant DEGs in ANV5 family, 7,293 in 4T1 family.
- Wrote `ARTIFACT_MANIFEST.md`, `FIRST_PASS_REPORT.md`, `README.md`, and
  this `PROGRESS.md`. Updated subagent progress JSON.

## Open items / next actions

1. Compare our DEG lists to Fig. 1c's hierarchical-cluster gene lists.
   The full Fig. 1c gene list lives in the PDF as a heatmap — would
   need OCR / digitization of Fig. 1c, or a follow-up request for the
   paper's processed DEG table (currently NOT in GSE277249 nor in
   either supplementary file).
2. Re-run with `limma-voom` (R) to match the paper's `B > 5` moderated-t
   metric. PyDESeq2 vs limma-voom usually agree to ≥ 80% of called
   genes; should be confirmed.
3. Cross-check ENPP1 expression in human breast cancer with public TCGA
   BRCA / METABRIC bulk RNA-seq (no controlled access needed for TCGA
   PanCancer Atlas) — replicate the human-relevance angle without the
   EGA-locked Bassez scRNA-seq.
4. Build a TLR (Traffic Light Reporter) HR-event toy model from
   published TLR data (paper ref. 51, Certo 2011) to sanity-check the
   HR-decrease claim under ENPP1i — would only be illustrative.
5. Write `REPORT.md` final once item 1 or 3 lands.

## Blockers

- **None hard on the omics pillar.** Everything we needed for first
  pass was public and reachable.
- **Soft block on functional/in-vivo claims**: comet assay images,
  γH2AX immunoblots, in vivo tumor curves, abscopal effect tracking,
  and the EGA-controlled scRNA-seq cohort are not part of any public
  deposit. Replicating them is impossible without re-running the wet
  lab work or applying for EGA access; both are out of scope.
- **Soft block on Fig. 1c gene list**: the paper's processed DEG table
  is not in GSE277249. We can reconstruct an equivalent table from raw
  counts but not match cluster ordering without the original code.
