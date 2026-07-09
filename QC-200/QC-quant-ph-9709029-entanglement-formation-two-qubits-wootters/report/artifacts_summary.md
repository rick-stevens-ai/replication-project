# Artifacts inventory — Wootters (1998) 2-qubit E_F replication

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9709029-entanglement-formation-two-qubits-wootters/`

## Top-level (the 8 mandatory artifacts)
| # | Artifact | Path | Purpose |
|--|--|--|--|
| 1 | Original PDF | `paper.pdf` | Source paper as fetched from arXiv (117 kB, 13 pp) |
| 2 | Marker parse | `extraction/marker.md` | Markdown extraction (structured) |
| 3 | Nougat parse | `extraction/nougat.mmd` | Academic-Markdown extraction (see extraction/README.md re: env-driven surrogate) |
| 4 | LaTeX report | `report/REPORT.tex` (+ `REPORT.pdf` if LaTeX available) | Section-by-section report with verdict |
| 5 | Open questions | `report/open_questions.json` (+ `## Open Questions` in report) | 5 heavy-duty follow-on questions |
| 6 | Workflow | `report/workflow.md` | End-to-end reproduction recipe + versions + work estimate |
| 7 | Artifacts summary | `report/artifacts_summary.md` | THIS FILE — inventory |
| 8 | Failure analysis | `report/failure_analysis.md` | Honest gaps / bugs / residual issues |

## Evidence + code (`report/evidence/`)
| File | Purpose |
|--|--|
| `wootters_concurrence.py` | Core implementation: concurrence, E_F, reference states, random-state generator, HJW brute-force upper bound, 12-test suite |
| `plot_werner.py` | Generates the two plots below |
| `results.json` | Machine-readable results of all 12 tests + full Werner sweep + random-state summary + Bell-diagonal comparison |
| `werner_sweep.png` | Werner-state C(p) and E(p) with p=1/3 separability line |
| `random_states_E_vs_C.png` | 1000 Haar-random 2-qubit mixed states on the Wootters E(C) curve |

## Working intermediates (`work/`)
| File | Purpose |
|--|--|
| `paper.txt` | `pdftotext paper.pdf` output for quick text search |

## Traces
- `report/evidence/results.json` — complete numerical trace, human-readable.
- Stdout of `python report/evidence/wootters_concurrence.py` — one-line
  per-test PASS/FAIL summary; captured in `work/run.log`.

## Verdict
See `report/REPORT.tex` and `report/failure_analysis.md`. **REPLICATED**
— 12 of 12 quantitative checks pass at machine precision.

## Reproduction command
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9709029-entanglement-formation-two-qubits-wootters
python3 -m venv .venv && source .venv/bin/activate
pip install numpy scipy qiskit matplotlib
python report/evidence/wootters_concurrence.py
python report/evidence/plot_werner.py
```
