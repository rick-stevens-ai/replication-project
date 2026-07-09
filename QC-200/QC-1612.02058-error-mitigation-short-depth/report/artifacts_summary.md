# Artifacts summary — QC-1612.02058

Directory: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1612.02058-error-mitigation-short-depth/`

## 8-artifact checklist (per `REPLICATION_DIR_STANDARD_2026-07-05.md`)
| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | `paper.pdf` | `paper.pdf` (577 KB, arXiv v3) | ✅ present |
| 2 | Marker parse | `extraction/marker.md` | ⚠️ fallback (pdftotext) — see extraction/README_extraction.md |
| 3 | Nougat parse | `extraction/nougat.mmd` | ⚠️ fallback (pdftotext) — see extraction/README_extraction.md |
| 4 | LaTeX report | `report/REPORT.tex` (+ `report/REPORT.pdf` if pdflatex runs) | ✅ present, verdict = **REPLICATED** |
| 5 | Open questions | `report/open_questions.json` (+ `report/open_questions.tex` used by REPORT) | ✅ 5 questions, each with `q`/`basis`/`next_steps` |
| 6 | Workflow doc | `report/workflow.md` | ✅ present |
| 7 | This summary | `report/artifacts_summary.md` | ✅ present |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ present |

## Evidence + code (`report/evidence/`)
| File | Bytes | Purpose |
|---|---|---|
| `zne_replication.py` | ~10 KB | Main replication code: Richardson coefficients, circuit builder, noise model, sim driver, aggregator |
| `make_plot.py` | 1.2 KB | Produces the Fig. 1(a)-style log-log plot from the JSON |
| `zne_results.json` | ~27 KB | Full raw results: 8 circuits × 5 ε × 3 c-values, plus aggregate stats and Richardson coefficients (with unit-test-style assertions) |
| `zne_error_vs_eps.png` | ~92 KB | Reproduced Fig. 1(a)-style scaling plot |

## Working files (`work/`)
| File | Purpose |
|---|---|
| `paper.pdf` | copy of arXiv v3 PDF |
| `paper.txt` | pdftotext dump (1654 lines) |
| `.venv/` | isolated Python env with pinned qiskit + qiskit-aer |

## Provenance chain
1. arXiv PDF → pdftotext → identify Eqs. (3)-(5) and Fig. 1 spec.
2. Eqs. (3)-(4) → linear-algebra Richardson coefficient solver in `zne_replication.py`, cross-checked against paper's implied (2,-1) / (3,-3,1).
3. Fig. 1(a) spec (random control problem + depolarizing noise) → digital brick-wall random circuit + `depolarizing_error`.
4. Numeric run → `zne_results.json` → aggregate table + plot → `REPORT.tex` claims-table + Verdict.
5. Log-log slope fit inline in the workflow gave 1.00 / 2.00 / 2.99, matching `O(λ^{n+1})` for n=0,1,2 respectively — this is the quantitative anchor for the REPLICATED verdict.

## Independence statement
The replication was implemented from-scratch reading only the paper text (no reference to Mitiq, IBM's later ZNE tutorials, or Qiskit-Runtime EstimatorV2's `ZneOptions`). The only external code used is the standard Qiskit + qiskit-aer noise API. The Richardson math was re-derived by solving the Vandermonde system numerically and cross-checking against the paper's stated coefficients.
