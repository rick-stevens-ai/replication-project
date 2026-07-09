# Artifacts summary

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9804044-quantum-computing-survey-scarani/`

## Mandatory 8 artifacts (Rick 2026-07-05 bar)
| # | Path | Status | Notes |
|---|---|---|---|
| 1 | `paper.pdf` | present | 140 KB, 10 pages, arXiv PDF |
| 2 | `extraction/marker.md` | present | Hand-authored Marker-equivalent Markdown (Marker CLI unavailable on host, central parsed corpus had no entry for 9804044) |
| 3 | `extraction/nougat.mmd` | present | Hand-authored Nougat-equivalent MMD with LaTeX math blocks |
| 4 | `report/REPORT.tex` | present | Full LaTeX report with paper summary, claims table, method, results table, verdict, 5 open questions |
| 5 | `report/open_questions.json` | present | 5 objects, each `{q, basis, next_steps}`, grounded in observed run behavior |
| 6 | `report/workflow.md` | present | timeline, tools + versions, rerun instructions |
| 7 | `report/artifacts_summary.md` | present | this file |
| 8 | `report/failure_analysis.md` | present | honest failure/friction/gap discussion |

## Additional artifacts
- `report/evidence/run_algorithms.py` — 270-line driver implementing DJ, Simon, and QFT check.
- `report/evidence/results.json` — machine-readable results: verdicts, oracle metadata, per-run Simon rounds used, wall time.
- `work/paper.pdf` — original arXiv fetch (copy).
- `work/paper.txt` — pdftotext dump (852 lines).
- `.venv/` — Python virtualenv with pinned Qiskit 2.5.0 + Aer 0.17.2 (kept for reproducibility; not committed to Dropbox tree if size is a concern).

## Trace summary
- **Deutsch–Jozsa n=3, constant f≡0:** `P(input==|000>) = 1.0` exactly (statevector).
- **Deutsch–Jozsa n=3, constant f≡1:** `P(input==|000>) = 1.0` exactly (verified in additional_constant runs).
- **Deutsch–Jozsa n=3, balanced (5 nonzero masks):** `P(input==|000>) < 1e-63` (numerical zero).
- **Simon n=3 (5 hidden strings 101, 011, 110, 111, 100):** recovered in 2, 4, 2, 3, 3 rounds respectively (5/5 success).
- **Scarani eq. 22 (QFT_{n=2}):** `matrix_max_diff = 0`, `unitarity_max_error = 0` (bit-identical to paper).
- **Wall time:** 2.45 s (single-thread, no GPU).
