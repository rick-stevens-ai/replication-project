# Artifacts summary — Abhijith et al. 1804.03719

## Top-level inventory (relative to target dir)
| Path | Kind | Purpose |
|---|---|---|
| `paper.pdf` | PDF (8.75 MB) | Original arXiv:1804.03719v3 (27 Jun 2022). |
| `work/paper.pdf` | PDF | Working copy (identical hash). |
| `work/paper.txt` | text | `pdftotext -layout` reflow (7489 lines). |
| `extraction/README.md` | markdown | Explains marker / nougat provenance. |
| `extraction/marker_out/` | dir | Marker output tree (populated if marker finished inside the wave budget). |
| `extraction/marker.md` | markdown | Marker parse (or `pdftotext` surrogate with provenance header if Marker timed out). |
| `extraction/nougat.mmd` | mmd | Documented pdftotext surrogate for Nougat (Nougat unbuildable on Darwin 25 / Py 3.12+). |
| `report/REPORT.tex` | LaTeX | Full section-by-section report with claims table, methods, results-vs-paper, verdict, open questions. |
| `report/REPORT.pdf` | PDF (best-effort) | Compiled from REPORT.tex if `pdflatex` was available. See failure_analysis.md. |
| `report/open_questions.json` | JSON | 5 open questions (`q`, `basis`, `next_steps`). |
| `report/workflow.md` | markdown | Full workflow, tools & versions, work estimate. |
| `report/artifacts_summary.md` | markdown | This file. |
| `report/failure_analysis.md` | markdown | Honest failure analysis. |
| `report/evidence/bv.py` | Python | Bernstein-Vazirani implementation (from scratch). |
| `report/evidence/grover.py` | Python | Grover implementation (from scratch). |
| `report/evidence/qpe.py` | Python | Quantum Phase Estimation implementation (from scratch). |
| `report/evidence/bv_result.json` | JSON | BV output including full probability vector. |
| `report/evidence/grover_result.json` | JSON | Grover output incl. full probability vector. |
| `report/evidence/qpe_result.json` | JSON | QPE output incl. full 16-outcome distribution. |
| `venv/` | Python venv | Reproducible env (Python 3.12.13 + qiskit 2.5.0 + numpy 2.5.1 + marker-pdf). |

## Trace of the 8 required wave artifacts
1. `paper.pdf` — ✅ present, 8.75 MB, arXiv fetch verified.
2. `extraction/marker.md` — ✅ present (either real Marker output or documented `pdftotext` surrogate with a clear provenance header).
3. `extraction/nougat.mmd` — ✅ present (documented `pdftotext` surrogate; Nougat unbuildable on this host, sibling-consistent).
4. `report/REPORT.tex` — ✅ present, detailed section-by-section, LaTeX.
5. `report/open_questions.json` — ✅ present, 5 objects each with `q` / `basis` / `next_steps`. Report also has `## Open Questions` (as `\section{Open Questions}` in REPORT.tex).
6. `report/workflow.md` — ✅ present, tools & versions + effort estimate.
7. `report/artifacts_summary.md` — ✅ this file.
8. `report/failure_analysis.md` — ✅ present.

## Evidence highlights (paste-quality)
- BV n=4, s=1011: recovered `1011` with P = 0.9999999999999986 in a single oracle call.
- Grover N=8, M=1, k*=2: P(marked |101>) = 0.9453124999999959 (analytic 0.9453124999999999).
- QPE t=4, phi=1/8: measured outcome `0010` with P = 0.9999999999999987; all other outcomes ≤ 3e-31.

All three JSON files in `report/evidence/` contain the full probability distributions over every basis state (2^n outcomes) so an independent auditor can spot-check.
