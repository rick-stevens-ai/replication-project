# Reproduction workflow — lucid100-pprm-small-rna-deinococcus

## Two-pass timeline

### Pass 1 (2026-06-09) — PASS-low smoke, 7/7 checks
1. Harvest paper PDF + supplements from Nature OA / Springer ESM (DOI 10.1038/s41598-021-91335-8).
2. Fetch quick-look metadata from Unpaywall, Europe PMC, Semantic Scholar → `artifacts/{unpaywall,europepmc,s2}.json`.
3. Download processed htseq counts from GEO GSE176207 (12 RNA-seq GSMs + 6 MAPS GSMs, ~215 KB tarball).
4. Metadata-only pull for PRIDE PXD026633 (proteomics raw not downloaded — tens of GB).
5. Run `code/smoke_test.py` (7 checks: paper cells load, count files parse, sample layout matches, sRNA Dsr2/PprS present, pprM/DR_0907 present with expression, MAPS smoke enrichment, cross-sheet consistency).
6. Result: `results/smoke_test_report.json` PASS 7/7; `figures/maps_pulldown_pprm_smoke.png` shows pprM highlighted at top of MAPS-enriched cloud.
7. Write `FIRST_PASS_REPORT.md`, `PROGRESS.md`, `ARTIFACT_MANIFEST.tsv`.

### Pass 2 (2026-06-22) — PASS-mid, full DESeq2 replication of published contrasts
1. Re-read all pass-1 artifacts (no re-download).
2. Create `.venv/` with PyDeseq2 0.5.4, pandas, numpy, scipy, matplotlib, openpyxl (Python 3.13.5, no R).
3. Write `code/deseq2_replication.py` (13 KB):
   - Load 12 RNA-seq htseq files, strip `__*` diagnostic rows.
   - Load 6 MAPS htseq files.
   - Fit PyDeseq2 with `~group` design (group = strain × dose) on RNA-seq; `~strain` on MAPS.
   - Extract 5 contrasts: S3 MAPS PprS vs blank, S4 PprSKD-0 vs WT-0, S5 PprSKD-10 vs WT-10, S6 WT-10 vs WT-0, S7 PprSKD-10 vs PprSKD-0.
   - Refit Cook's outliers, default independent filtering, BH FDR at α=0.05.
   - Join each contrast to paper's supplement Tables S3-S7; compute Pearson r, Spearman ρ, sign concordance, padj concordance.
   - Emit per-contrast TSVs, comparison-joined TSVs, per-contrast scatter plots, `results/deseq2_summary.json` machine-readable summary.
4. Run script (~25 s wall clock, single CPU on CherryRd).
5. Write `REPORT.md` with per-contrast verdict, scope audit, honest gaps, self-score.

### Pass 3 (2026-07-06) — Backfill to 8-artifact standard
1. Read existing `REPORT.md` and (if present) `FIRST_PASS_REPORT.md` — no other reads.
2. Write `report/REPORT.tex` (LaTeX version with headline critique).
3. Write `report/open_questions.json` (5 open questions, bare JSON list).
4. Write `report/open_questions_section.tex` (matching LaTeX section).
5. Write `report/workflow.md` (this file).
6. Write `report/artifacts_summary.md` (per-artifact inventory + provenance).
7. Write `report/failure_analysis.md` (honest critique).
8. Write `extraction/nougat.mmd` (stub for later Nougat OCR of paper PDF).
9. Preserve real verdict = PARTIAL; flag queue-verdict mismatch (queue records REPLICATED).

## Compute envelope

- Local Python-only on CherryRd (macOS, single CPU).
- No cluster jobs, no GPU work, no R install.
- No raw FASTQ / .raw downloads (only processed counts + supplements).
- Total wall clock: pass-1 ~30 min (mostly downloads), pass-2 ~1 hour (script + report writing), pass-3 ~20 min (backfill).

## Free-endpoint compliance

- LLM usage: Argo `argo:claude-opus-4.7` for all reasoning (free per standing rule).
- No paid API calls.
- No wet-lab.
- Public GEO + PRIDE + Nature OA + Semantic Scholar + Europe PMC + Unpaywall only.

## Repro one-liner

From the slot directory:

```bash
source .venv/bin/activate
python code/smoke_test.py            # PASS-low, 7 quick checks (~5 s)
python code/deseq2_replication.py    # PASS-mid, full DESeq2 redo (~25 s)
cat results/deseq2_summary.json      # canonical machine-readable output
```

Then read `REPORT.md` and `report/REPORT.tex` for the verdict.

## What is NOT in this workflow

- No R-DESeq2 verification pass for S4/S5 (open question #4).
- No PXD026633 raw proteomics re-analysis (compute envelope).
- No PANTHER GO enrichment re-run (out of scope).
- No re-alignment of raw FASTQ (trust published htseq counts).
- No wet-lab (EMSA, Northern, qRT-PCR, survival) — inherently unreproducible in silico.
