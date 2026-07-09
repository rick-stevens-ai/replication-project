# lucid-grandt-fibroblast-rnaseq

Replication study of Grandt et al. 2022 (KiKme), *Molecular Medicine* 28:105, DOI 10.1186/s10020-022-00520-6.

## Contents
- `data/paper.pdf` — local copy of target paper
- `data/AF1.xlsx … AF6.docx` — supplementary materials downloaded from BMC
- `data/AF1a_degs.tsv`, `data/AF1b_degs_interaction.tsv` — TSV extracts of the DEG tables (~50k + ~118k rows)
- `code/` — three Python scripts (no third-party deps except matplotlib + openpyxl)
  - `01_replicate_degs.py` — replicates DEG counts (R1–R6) and tabulates pathway memberships
  - `02_pathway_with_background.py` — independent Fisher right-tail over-representation analysis (R8)
  - `03_figures.py` — produces three figures
- `results/` — TSVs + JSON of every quantitative output plus the live console logs
- `figures/` — `fig1_deg_counts.{png,pdf}` (DEG bars), `fig2_volcano.{png,pdf}` (volcanos per group/dose), `fig3_p53_enrichment.{png,pdf}` (HALLMARK_P53_PATHWAY fold-enrichment headline)
- `REPORT.md` — full replication report with verdict & scoring
- `PROGRESS.md` — running log

## Verdict
**PARTIAL (strong)** — All checkable numerical claims replicate exactly (DEG counts, %up, all 7 interaction genes, top-FDR genes); the biological pathway narrative is independently confirmed via MSigDB ORA. The raw FASTQ are not publicly deposited (the paper's data-availability statement only points to the supplementary files), so the alignment + limma pipeline cannot be re-run.

- **Coverage:** 8/10
- **Agreement:** 9/10

See `REPORT.md` for the full breakdown.

## Reproducing
```bash
python3 code/01_replicate_degs.py   # ~2 s
python3 code/02_pathway_with_background.py
python3 code/03_figures.py
```
