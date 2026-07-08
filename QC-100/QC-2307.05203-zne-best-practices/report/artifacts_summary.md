# Artifacts summary — QC-2307.05203-zne-best-practices

## Location
`~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2307.05203-zne-best-practices/`

## Files

### Report (report/)
- `REPORT.md` — original markdown replication report (source of truth, authored during run 2026-07-03)
- `REPORT.tex` — LaTeX version with honest critique section (backfill 2026-07-06)
- `open_questions.json` — 5 bare-list open questions with basis + next_steps (JSON-safe strings)
- `open_questions_section.tex` — LaTeX \input{}-able rendering of the 5 open questions
- `workflow.md` — step-by-step reproduction workflow
- `artifacts_summary.md` — this file
- `failure_analysis.md` — honest critique of scope gaps and reproduction limits
- `evidence/zne_experiment.py` — exact code that produced the numbers
- `evidence/zne_results.json` — machine-readable results (5 cases × 4 families)
- `evidence/run.log` — stdout of the live run

### Code (code/)
- `zne_experiment.py` — canonical executable (duplicate of evidence copy)

### Work directory (work/)
- `paper.pdf` — arXiv:2307.05203v2 PDF
- `paper.txt` — pdftotext dump used for claim extraction

### Extraction (extraction/)
- `nougat.mmd` — stub / placeholder (nougat not rerun; paper.txt is authoritative for claim extraction)

### Environment (.venv/)
- Python 3.12 virtual environment with mitiq 1.0.0, qiskit 2.5.0, qiskit-aer 0.17.2

## What's reproducible from what
| To reproduce | Run |
|---|---|
| Full experiment | `source .venv/bin/activate && python code/zne_experiment.py` |
| Just the report | `cd report && pdflatex REPORT.tex` (2× for cross-refs) |
| Claim table | Read `REPORT.md` §2 |
| Per-case raw numbers | Read `report/evidence/zne_results.json` |

## Wall time & compute
- 17 s on Apple Silicon (CherryRd), single core
- No GPU, no HPC, no paid endpoints
- Deterministic (seed 42)

## Verdict
**REPLICATED (headline claim C1–C5).** Headline exercised = YES (5 cases
covering weak/shallow/wide, strong/deep/wide, moderate/wide, moderate/narrow,
strong/deep/narrow regimes; all 4 extrapolation families tested on identical
raw scans).

Not exercised:
- C6 (partial-fold σ-reduction measurement)
- C7 (full Fig. 6 phase-diagram sweep)
- C8 (composition with ROEM + Pauli twirling)
- Real IBM hardware runs
- Multi-seed ensemble error bars
