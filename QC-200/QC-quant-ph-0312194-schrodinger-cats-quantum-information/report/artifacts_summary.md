# Artifacts summary — QC-quant-ph-0312194

Location: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0312194-schrodinger-cats-quantum-information/`

## 8 required artifacts (Rick 2026-07-05 standard)

| # | Artifact                          | Path                                    | Status |
|---|-----------------------------------|-----------------------------------------|--------|
| 1 | `paper.pdf`                       | `./paper.pdf`                           | present (173 kB, 10 pp, arXiv v1) |
| 2 | Marker parse                      | `./extraction/marker.md`                | present (fallback: pdftotext -layout; Marker not installed on host) |
| 3 | Nougat parse                      | `./extraction/nougat.mmd`               | present (fallback: pdftotext -layout; Nougat not installed on host) |
| 4 | REPORT.tex (+ compile to PDF)     | `./report/REPORT.tex`                   | present (11.9 kB); PDF compile attempted separately |
| 5 | Open Questions (JSON + REPORT section) | `./report/open_questions.json` + `## Open Questions` in REPORT.tex | present (5 questions, each with q/basis/next_steps) |
| 6 | Workflow                          | `./report/workflow.md`                  | present |
| 7 | Artifacts summary                 | `./report/artifacts_summary.md`         | this file |
| 8 | Failure analysis                  | `./report/failure_analysis.md`          | present |

## Evidence + code

| file                                       | purpose |
|--------------------------------------------|---------|
| `report/evidence/cat_replication.py`       | Full self-contained QuTiP simulation of C1..C4 |
| `report/evidence/results.json`             | Raw numerical results per alpha, per claim, plus PASS/FAIL summary |

## Intermediates + downloads

| file                     | purpose |
|--------------------------|---------|
| `work/paper.txt`         | pdftotext -layout output of paper.pdf |
| `work/venv/`             | Python 3.14 virtualenv with qutip 5.3.0, numpy 2.5.1, scipy 1.18.0 |

## Traces
- No LLM traces (no Argo call was made — no judge panel was necessary, self-verdict per QC brief).
- Deterministic simulation; re-running `cat_replication.py` reproduces `results.json` byte-for-byte.
