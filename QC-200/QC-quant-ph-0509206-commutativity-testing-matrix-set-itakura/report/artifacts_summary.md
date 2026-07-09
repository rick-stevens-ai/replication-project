# Artifacts summary

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0509206-commutativity-testing-matrix-set-itakura/`

## Mandatory 8-artifact bar

| # | Artifact | Path | Present? | Notes |
|---|----------|------|----------|-------|
| 1 | Original PDF | `paper.pdf` | Y | 445104 bytes, 70 pp, arXiv:quant-ph/0509206v1 |
| 2 | Marker parse | `extraction/marker.md` | Y | **Surrogate**: PyMuPDF 1.27.2.3 (Marker not installed on host) |
| 3 | Nougat parse | `extraction/nougat.mmd` | Y | **Surrogate**: `pdftotext -layout` (Nougat not installed on host) |
| 4 | REPORT.tex + REPORT.pdf | `report/REPORT.tex`, `report/REPORT.pdf` | Y | LaTeX report with verdict; PDF compiled if `pdflatex` available |
| 5 | Open questions | `report/open_questions.json` + REPORT `## Open Questions` | Y | Five heavy-duty questions, each `{q, basis, next_steps}` |
| 6 | Workflow | `report/workflow.md` | Y | Chronological workflow + tool versions + reproduction command |
| 7 | Artifacts summary | `report/artifacts_summary.md` | Y | This file |
| 8 | Failure analysis | `report/failure_analysis.md` | Y | Honest gaps, k=8 anomaly, single-defect construction fiddle, un-implemented quantum walk |

## Evidence & code

| Path | Description |
|------|-------------|
| `report/evidence/commutativity_replication.py` | ~350 LOC driver: ensembles, classical scan, Grover statevector, sweep, fit, plot |
| `report/evidence/results.json` | Per-k JSON: classical + quantum + single-defect + fits |
| `report/evidence/scaling_loglog.png` | Log-log figure with fitted slopes for four scaling series |

## Work directory

| Path | Description |
|------|-------------|
| `work/paper.pdf` | Same as top-level `paper.pdf` (working copy) |
| `work/paper.txt` | `pdftotext -layout` dump for grepping |

## Extraction notes

| Path | Description |
|------|-------------|
| `extraction/README.md` | Surrogate provenance explanation |
| `extraction/marker.md` | PyMuPDF text with page markers (~110 KB) |
| `extraction/nougat.mmd` | pdftotext layout dump (~150 KB) |

## Traces of what was done

- `stdout` from the sweep is captured in `report/workflow.md` §9 (one row per k).
- Full JSON of every classical + quantum measurement, including intruder indices and defect pair, is in `report/evidence/results.json`.
- Every fit slope is stored under `results.json.fits` for machine consumption.
