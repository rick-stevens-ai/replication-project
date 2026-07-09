# Artifacts Summary — Rusin et al. 2021 replication

## Directory layout (post-backfill)

```
lucid100-doserate-cellcycle-adsc-2021/
├── REPORT.md                              # original narrative (source of truth for verdict)
├── paper.pdf                              # source paper (PLoS OA, 1.8 MB)
├── paper.html                             # HTML render
├── paper.txt                              # text extract for grep
├── mendeley_data/                         # raw source data (5 xlsx + 7 tif + 1 page snap + api json)
├── replicate_prolif.py    replicate_prolif.log
├── replicate_cellcycle.py replicate_cellcycle.log
├── replicate_apoptosis.py replicate_apoptosis.log
├── replicate_gene_expr.py replicate_gene_expr.log
├── find_subset.py         find_subset.log     # diagnostic for row-index anomaly
├── replication_prolif_results.json
├── replication_cellcycle_results.json
├── replication_apoptosis_results.json
├── replication_gene_results.json
├── report/                                # BACKFILLED 2026-07-06
│   ├── REPORT.tex                         #   full LaTeX report + honest critique
│   ├── open_questions.json                #   5 grounded open questions
│   ├── open_questions_section.tex         #   LaTeX mirror of the 5 open questions
│   ├── workflow.md                        #   step-by-step replication workflow
│   ├── artifacts_summary.md               #   this file
│   └── failure_analysis.md                #   honest critique of scope + method limits
└── extraction/                            # BACKFILLED 2026-07-06
    └── nougat.mmd                         #   PDF extraction stub (sha256 of paper.pdf)
```

## Key numeric artifacts

- `replication_cellcycle_results.json` — 27/27 mean+SD cells reproduce (Day 1--3 × PC/LDR/HDR × G0/G1, S, G2/M).
- `replication_apoptosis_results.json` — 48/48 cells reproduce (12 h / D1 / D2 / D3 × 3 conditions × 4 stages).
- `replication_prolif_results.json` — MTS standard curve reproduces; 8/8 significance claims verified.
- `replication_gene_results.json` — CD44 + TP53 fold changes reproduce; 6/8 significance claims verified.

## Sources cited in replication

- Rusin M et al. 2021. PLoS ONE 16(4):e0250160. DOI 10.1371/journal.pone.0250160.
- Mendeley Data DOI 10.17632/8t594k4w8z.1 (17 files, ~52 MB).

## Compute footprint
- CPU-only (no GPU). Python 3.11, numpy, pandas, openpyxl, scipy.
- Total replication runtime <2 min.
- Backfill: Argo Claude Opus 4.7 (free endpoint) — narrative only, no re-simulation.

## Free endpoint compliance
- ✅ No paid endpoints touched. Argo (free) used for narrative composition only.
- ✅ No wet-lab / no external inference cost.
