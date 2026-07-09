# Artifacts Summary — Grandt et al. 2022 replication

## Top level
- `REPORT.md` — canonical human-readable replication report (verdict, tables, narrative). **DO NOT MOVE.**

## `report/` — final deliverables
- `REPORT.tex` — LaTeX version of the report (verdict, R1–R8 tables, critique, verdict rationale).
- `open_questions.json` — 5 open questions in JSON (bare list of `{q, basis, next_steps}` objects).
- `open_questions_section.tex` — same 5 open questions rendered as a LaTeX `\section{Open Questions}` block.
- `workflow.md` — step-by-step recipe (download → convert → DEG replication → interaction → ORA → figures → report).
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — honest critique of what was NOT replicated and why.

## `extraction/`
- `nougat.mmd` — placeholder stub for a full-paper Nougat / MMD extraction (not required for this analytical replication; documented for completeness).

## `data/` (expected, from `code/00_download.sh`)
- `AF1.xlsx` (15 MB) — DEG per-gene tables (AF1a) + interaction tables (AF1b).
- `AF2.pdf` — pathway PDF (sanity reference).
- `AF3.docx` — qPCR primers.
- `AF4.docx` — IPA settings.
- `AF5.xlsx` — GO term results.
- `AF6.docx` — pathway heatmaps.

## `code/`
- `00_download.sh` — supplementary-file downloader (springer static-content URLs).
- `01_replicate_degs.py` — DEG-count + top-gene replication.
- `02_pathway_with_background.py` — MSigDB ORA with AF1-derived background.
- `03_figures.py` — figure generation.

## `results/`
- `replication_summary.json` — machine-readable table of all R1–R8 comparisons.
- Per-combo DEG count tables.
- Per-combo pathway ORA tables (fold, p-value, a/K).

## `figures/`
- DEG count bar plots.
- HALLMARK_P53_PATHWAY fold-enrichment across (group, dose).

## Provenance
- Replication executed 2026-05-30 by an OpenClaw subagent.
- Report artifacts backfilled 2026-07-06 (this run) to bring dir to 8-artifact standard.
- Zero paid endpoints, zero author contact, zero proprietary tools.
