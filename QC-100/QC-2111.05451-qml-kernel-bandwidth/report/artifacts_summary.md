# Artifacts Summary — QC-2111.05451

Working directory: `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2111.05451-qml-kernel-bandwidth/`

## Report layer

| File | Purpose | Size (approx) |
|---|---|---|
| `report/REPORT.md` | Original markdown replication report (verdict = REPLICATED) | ~10 KB |
| `report/REPORT.tex` | LaTeX version with expanded Critique + `\input{open_questions_section.tex}` | ~11 KB |
| `report/open_questions.json` | 5 open-question objects `{q, basis, next_steps}` (bare list) | ~5.6 KB |
| `report/open_questions_section.tex` | LaTeX \section rendering of the 5 questions | ~5 KB |
| `report/workflow.md` | Human+machine timeline of the replication + backfill | ~4 KB |
| `report/artifacts_summary.md` | This file — inventory of the 8-artifact set | ~2 KB |
| `report/failure_analysis.md` | Honest critique of what was NOT reproduced | ~5 KB |

## Evidence

| File | Purpose |
|---|---|
| `report/evidence/bandwidth_sweep.csv` | Single-seed sweep (7 λ values) |
| `report/evidence/bandwidth_sweep.json` | Same as CSV + config block + classical-baseline scores |
| `report/evidence/bandwidth_sweep_multiseed.json` | 5-seed × 7-λ raw runs + mean/std summary |

## Figures

| File | Purpose |
|---|---|
| `figures/accuracy_vs_bandwidth.png` | Train/test accuracy vs λ + classical RBF ref + 0.5 random-guess ref; off-diag K on twin axis |

## Code (independently reimplemented, no copy from authors)

| File | Purpose |
|---|---|
| `code/run_bandwidth_sweep.py` | Single-seed runner; contains build_data, feature_map, kernel_matrix |
| `code/multi_seed_confirm.py` | 5-seed averager |

## Logs

| File | Purpose |
|---|---|
| `logs/sweep_run.log` | stdout of single-seed run |
| `logs/multiseed_run.log` | stdout of multi-seed run |

## Extraction (backfill 2026-07-05)

| File | Purpose |
|---|---|
| `extraction/nougat.mmd` | Stub — nougat conversion of `work/paper.pdf` (placeholder; not run to avoid GPU/network dependencies) |

## Provenance

| File | Purpose |
|---|---|
| `work/paper.pdf` | Original arXiv PDF (v4, Sep 2022) |
| `work/paper.txt` | pdftotext extraction used for claim identification |

## 8-artifact checklist (project standard)

- [x] REPORT.md
- [x] REPORT.tex
- [x] open_questions.json (bare list of 5)
- [x] open_questions_section.tex
- [x] workflow.md
- [x] artifacts_summary.md
- [x] failure_analysis.md
- [x] extraction/nougat.mmd (stub)
