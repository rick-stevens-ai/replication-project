# Artifacts Summary — QC-2209.00292-barren-plateaus-tensor-network

## Top-level dir
`~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2209.00292-barren-plateaus-tensor-network/`

## Report artifacts (`report/`)
- `REPORT.md` — original narrative report (existing)
- `REPORT.tex` — LaTeX version with critique section
- `open_questions.json` — 5 open questions in structured JSON (bare list)
- `open_questions_section.tex` — LaTeX section rendering the same 5 questions
- `workflow.md` — end-to-end reproducible workflow, step-by-step
- `artifacts_summary.md` — this file
- `failure_analysis.md` — honest critique of what was NOT reproduced

## Evidence (`report/evidence/`)
- `qmps_variance.json` — full MC results: N, variance, sample count, Thm 3 prediction, ratio, elapsed time, fit params
- `variance_vs_N.png` — log-linear plot: MC estimates vs Thm 3 vs McClean 2^{-N} reference
- `summary.txt` — human-readable results table

## Code (`code/`)
- `qmps_barren.py` — qMPS staircase ansatz + parameter-shift + MC estimator (~200 LOC, self-contained, PennyLane)
- `plot_and_summarize.py` — plotting + summary table generation

## Extraction (`extraction/`)
- `nougat.mmd` — parsed paper text stub (source: pdftotext of arXiv PDF; nougat not run in this wave)

## Work (`work/`)
- `paper.pdf` — arXiv 2209.00292v3 PDF
- `paper.txt` — pdftotext -layout output

## Verdict
**REPLICATED** — headline barren-plateau claim (C1+C2, qMPS exponential decay in N, base ~ 3/8) reproduced on real state-vector simulation with 14,000 quantum-circuit evaluations. Auxiliary claims C3 (sum-of-local avoidance), C4 (qTTN/qMERA polynomial), C5 (complexity) explicitly not exercised — see failure_analysis.md.

## Compute footprint
- Single CPU core, ~95 s wall
- No GPU, no HPC, no paid services (free-endpoint-only compliant)
- Deterministic under seed 20260703

## Artifact count (Rick's 8-artifact standard)
1. REPORT.md
2. REPORT.tex
3. open_questions.json
4. open_questions_section.tex
5. workflow.md
6. artifacts_summary.md
7. failure_analysis.md
8. extraction/nougat.mmd

Plus supporting: evidence JSON + PNG + summary.txt + code + paper PDF/text.
