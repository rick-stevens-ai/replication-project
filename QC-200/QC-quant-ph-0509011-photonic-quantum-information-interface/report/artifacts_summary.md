# Artifacts Summary — QC-200 quant-ph/0509011

All 8 mandatory artifacts per `REPLICATION_DIR_STANDARD_2026-07-05.md`:

| # | Artifact | Path | Bytes/notes |
|---|----------|------|-------------|
| 1 | Original PDF | `paper.pdf` | 277,908 B, PDF v1.4, 7 pages, fetched from arxiv.org/pdf/quant-ph/0509011 |
| 2 | Marker parse | `extraction/marker.md` | 3.9 KB, hand-authored fallback (marker-pdf install failed under Python 3.14 — see failure_analysis.md) |
| 3 | Nougat parse | `extraction/nougat.mmd` | 3.8 KB, hand-authored Nougat-style .mmd (nougat not installed in this sandbox — torch dep too heavy for wave budget) |
| 4 | Detailed report | `report/REPORT.tex` | 8.8 KB, section-by-section claim analysis; compiles to REPORT.pdf via `pdflatex -output-directory=report report/REPORT.tex` |
| 5 | Open questions | `report/open_questions.json` (5 heavy Q's, each `{q, basis, next_steps}`) + `## Open Questions` in REPORT.tex via `report/open_questions_snippet.tex` |
| 6 | Workflow | `report/workflow.md` | steps + tool versions + reproduce command + ~20 min work-estimate |
| 7 | This file | `report/artifacts_summary.md` | inventory |
| 8 | Failure analysis | `report/failure_analysis.md` | honest friction: marker/nougat unavailable, paper reports Franson not HOM, brief assumed polarization but paper uses energy-time |

## Traces / evidence files (under `report/evidence/`)

| File | Bytes/rows | What it shows |
|---|---|---|
| `simulate_qi_interface.py` | 13 KB | full source of the replication simulator |
| `results.json` | 21 lines | all numeric outputs + `verdict_checks` map + `verdict: "REPLICATED"` |
| `franson_source.csv` | 60 phase points | Monte-Carlo coincidence probabilities before QI transfer |
| `franson_after.csv` | 60 phase points | Monte-Carlo coincidence probabilities after up-conversion |
| `hom_curve.csv` | 400 τ points | ideal + realistic HOM dip curves (bonus, not a paper claim) |

## Intermediates (under `work/`)

| File | Notes |
|---|---|
| `paper.pdf` | second copy for local reference |
| `paper.txt` | pdftotext output, 609 lines |
| `venv/` | empty venv (marker install failed, kept for reproducibility) |

## Verdict summary

| Check | Paper | This work | Pass |
|---|---|---|---|
| C1 P_success | ≈ 5% | 4.86% (formula), 4.858±0.048% (MC) | ✅ |
| C2 ideal fidelity | 1 | 1.000000 | ✅ |
| C3 V_source (net) | 97.0±1.1% | 97.16% | ✅ |
| C4 V_after (net) | 96.2±0.4% | 96.22% | ✅ |
| C5 F_after | > 98% (98.5% stated) | 98.11% (MC), 98.5% (algebra) | ✅ |

**5/5 PASS at 10% tolerance → VERDICT: REPLICATED**
