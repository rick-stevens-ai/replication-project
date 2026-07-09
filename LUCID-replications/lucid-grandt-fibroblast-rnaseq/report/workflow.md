# Workflow — Grandt et al. 2022 KiKme RNA-seq replication

## 0. Provenance
- Paper: Grandt CL et al., Mol Med 28:105 (2022), DOI 10.1186/s10020-022-00520-6.
- All downloads: `https://static-content.springer.com/esm/art%3A10.1186%2Fs10020-022-00520-6/MediaObjects/10020_2022_520_MOESM{N}_ESM.{ext}`.
- Endpoints used: none paid. Zero author contact. Zero proprietary tools.

## 1. Triage
1. Read paper PDF.
2. Check Data Availability section — **no GEO/SRA accession**. Note this blocks raw-read replication.
3. Enumerate supplementary files (AF1–AF6). AF1 (15 MB xlsx) carries per-gene DEG statistics with embedded MSigDB pathway annotations — the key resource.
4. Scope decision: replicate **downstream** claims only (DEG counts, top genes, interaction, pathway ORA); flag raw-pipeline steps as NO-GO.

## 2. Data acquisition (`code/00_download.sh`)
```
wget -O data/AF1.xlsx  <springer static-content path AF1>
wget -O data/AF2.pdf   <... AF2>
wget -O data/AF3.docx  <... AF3>
wget -O data/AF4.docx  <... AF4>
wget -O data/AF5.xlsx  <... AF5>
wget -O data/AF6.docx  <... AF6>
```

## 3. Table conversion
- AF1.xlsx → AF1a.tsv (DEG table) + AF1b.tsv (interaction table) via `openpyxl` in read-only mode.

## 4. DEG replication (`code/01_replicate_degs.py`)
- Load AF1a.tsv. Filter rows on `adj.P.Val < 0.05` for each (group, dose) combo.
- Count total DEGs, count upregulated (`logFC > 0`), compute %up.
- Compare to paper Table/Fig 5 values → **exact match** (see REPORT R1–R3).

## 5. Top-gene extraction
- For each (group, 0.05 Gy) combo, sort by ascending `adj.P.Val`, take top 12.
- Compare to the paper's named LDIR set → **11/12 in every group**.

## 6. Interaction effects
- Load AF1b.tsv. Filter `adj.P.Val < 0.05` in each contrast column.
- Union across contrasts → **exactly the paper's 7 named genes** (LINC00601, COBLL1, SESN2, BIN3, TNFRSF10A, EEF1AKNMT, BTG2).

## 7. Pathway over-representation (`code/02_pathway_with_background.py`)
- Extract MSigDB Hallmark gene-set memberships from AF1 "In Geneset" column.
- Background = 8,134 unique genes in AF1 (conservative; true universe ~14.7k).
- For each (group, dose, gene-set): compute a/K, fold-enrichment, right-tailed Fisher's-exact p.
- Independently confirms paper's three central pathway claims (p53 strongest, DNA-repair only in N0 at low dose, E2F strongest in N2+ at 2 Gy).

## 8. Figures (`code/03_figures.py`)
- Matplotlib bar plots of DEG counts by group/dose.
- Fold-enrichment plot for HALLMARK_P53_PATHWAY across (group, dose).
- All saved to `figures/`.

## 9. Report generation
- `REPORT.md` (top-level) — human-readable narrative + tables.
- `report/REPORT.tex` — LaTeX version.
- `report/open_questions.json` — 5 open questions in machine-readable form.
- `report/open_questions_section.tex` — the same 5 as a LaTeX section.
- `report/artifacts_summary.md` — one-line-per-file artifact index.
- `report/failure_analysis.md` — what we did NOT do and why.
- `extraction/nougat.mmd` — stub for future full-paper mmd extraction.

## 10. What this workflow deliberately skips
- No FASTQ ingestion (no raw data available).
- No STAR/featureCounts/voom-limma re-run.
- No IPA re-run (proprietary; replaced by open MSigDB ORA).
- No qPCR wet-lab validation.
- No ConsensusPathDB GO clustering re-execution.

## 11. Reproducibility
- Python 3 stdlib + `openpyxl` + `scipy.stats` + `matplotlib`. No R, no proprietary tools.
- Deterministic: no RNG used. All results are analytical.
- Total wall time: ~2 min on a laptop.
