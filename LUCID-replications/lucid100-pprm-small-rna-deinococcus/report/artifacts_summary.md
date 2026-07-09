# Artifacts summary — lucid100-pprm-small-rna-deinococcus

Slot: `lucid100-pprm-small-rna-deinococcus` (LUCID100 rank 66, Wave 4, slot 35, tier A, priority 14).
Paper: Villa et al., *Sci. Rep.* 11:12949 (2021). DOI `10.1038/s41598-021-91335-8`.
Backfilled: 2026-07-06.

## Report artifacts (this backfill)

| File | Kind | Purpose |
| --- | --- | --- |
| `report/REPORT.tex` | LaTeX | Compilable single-file report with headline verdict, quantitative table, critique |
| `report/open_questions.json` | JSON list | 5 open questions with basis + concrete next_steps (bare list, not wrapped) |
| `report/open_questions_section.tex` | LaTeX | Section rendering of the 5 open questions (input by REPORT.tex) |
| `report/workflow.md` | Markdown | Three-pass reproduction pipeline (smoke → DESeq2 → backfill) |
| `report/artifacts_summary.md` | Markdown | This inventory |
| `report/failure_analysis.md` | Markdown | Honest critique of what went wrong and why |
| `extraction/nougat.mmd` | MMD stub | Nougat OCR placeholder for the paper PDF |

## Existing (preserved) artifacts

### Top-level reports
- `REPORT.md` — PASS-mid bench report from 2026-06-22 (canonical prose evidence, preserved intact)
- `FIRST_PASS_REPORT.md` — PASS-low smoke report from 2026-06-09
- `PROGRESS.md` — running task log
- `ARTIFACT_MANIFEST.tsv` — 50-row sha256-16 fingerprint inventory

### Paper + supplements (in `artifacts/`)
- Paper PDF (Nature OA, ~1.9 MB)
- `supplement1.xlsx` — S1-S9 tables, 264 KB (the comparison reference for DESeq2 redo)
- `supplement2.pdf` — 8.1 MB supplement
- Provenance JSONs: `unpaywall.json`, `europepmc.json`, `s2.json`, `pxd026633.json`

### Public data (in `artifacts/geo/`)
- 12 × RNA-seq htseq.gz files (GSM5360101-112, ~10 KB each, 215 KB tarball)
- 6 × MAPS htseq.gz files (GSM5360113-118, ~14 KB each)
- Total: 18 htseq count tables, all with 3132 D. radiodurans gene rows + 5 htseq diagnostic rows

### Code (in `code/`)
- `smoke_test.py` — pass-1 7-check smoke (PASS 7/7 on 2026-06-09)
- `deseq2_replication.py` — pass-2 PyDeseq2 full DESeq2 redo of 5 contrasts

### Results (in `results/`)
- `smoke_test_report.json` — pass-1 machine-readable smoke output
- `deseq2_summary.json` — **canonical pass-2 machine-readable result** (5 contrasts × 4 metrics)
- `deseq2_S3_MAPS_PprS_vs_blank.tsv` — full 3132-gene MAPS DEG table
- `deseq2_S4_PprSKD0_vs_WT0.tsv` — full 3132-gene S4 DEG table (failed contrast)
- `deseq2_S5_PprSKD10_vs_WT10.tsv` — full 3132-gene S5 DEG table (failed contrast)
- `deseq2_S6_WT10_vs_WT0.tsv` — full 3132-gene S6 DEG table (perfect replication)
- `deseq2_S7_PprSKD10_vs_PprSKD0.tsv` — full 3132-gene S7 DEG table (perfect replication)
- `deseq2_comparison_*.tsv` — paper-vs-repro joined tables (evidence rows)

### Figures (in `figures/`)
- `deseq2_S3_MAPS_PprS_vs_blank_scatter.png` — MAPS L2FC paper vs repro (strong positive)
- `deseq2_S4_PprSKD0_vs_WT0_scatter.png` — scrambled (failed contrast)
- `deseq2_S5_PprSKD10_vs_WT10_scatter.png` — scrambled (failed contrast)
- `deseq2_S6_WT10_vs_WT0_scatter.png` — perfect 1:1 line
- `deseq2_S7_PprSKD10_vs_PprSKD0_scatter.png` — perfect 1:1 line
- `maps_pulldown_pprm_smoke.png` — pprM highlighted at top of MAPS-enriched cloud (pass-1)

## Provenance

- Paper: DOI `10.1038/s41598-021-91335-8`, CC BY 4.0. sha256 in `ARTIFACT_MANIFEST.tsv`.
- RNA-seq + MAPS counts: GEO GSE176207 (GSM5360101-118). All files sha256-fingerprinted.
- Proteomics metadata only: PRIDE PXD026633. Raw .raw not downloaded (compute envelope).
- LLM: Argo `argo:claude-opus-4.7` (free per standing rule).
- No paid APIs, no wet-lab.

## Not-in-scope artifacts (documented gaps)

- No R-DESeq2 verification of S4/S5 (open question #4)
- No PRIDE PXD026633 raw .raw analysis (Table S1 proteomics — compute envelope, ~tens of GB + FragPipe/MaxQuant)
- No PANTHER GO enrichment re-run (Table S2)
- No re-alignment of raw FASTQ from SRA (published htseq counts trusted)

## Verdict

**PARTIAL** (queue mismatch flagged — LUCID-100 queue records REPLICATED, real verdict is PARTIAL). See `report/failure_analysis.md` and `REPORT.md` §8.
