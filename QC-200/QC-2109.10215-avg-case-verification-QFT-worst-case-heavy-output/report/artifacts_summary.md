# Artifacts Summary

Directory: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2109.10215-avg-case-verification-QFT-worst-case-heavy-output/`

## Required 8 artifacts (per `REPLICATION_DIR_STANDARD_2026-07-05.md`)

| # | Artifact | Path | Status | Notes |
|---|---|---|---|---|
| 1 | Original PDF | `paper.pdf` | ✅ | 638 KB, 6 pages, arXiv v3 |
| 2 | Marker extraction | `extraction/marker.md` | ✅ (fallback) | pdftotext fallback; header discloses. See `workflow.md`. |
| 3 | Nougat extraction | `extraction/nougat.mmd` | ✅ (fallback) | pdftotext fallback; header discloses. See `workflow.md`. |
| 4 | Detailed LaTeX report | `report/REPORT.tex` + `report/REPORT.pdf` | ✅ | 7-page compiled PDF; section-by-section claims vs results; verdict = REPLICATED. |
| 5 | Open questions | `report/open_questions.json` (+ § in REPORT) | ✅ | Exactly 5 grounded questions with `q`, `basis`, `next_steps`. |
| 6 | Workflow doc | `report/workflow.md` | ✅ | Tool versions, execution log, extraction-fallback rationale, reproduction commands. |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ | This file. |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ | Bugs found + fixed, residual gaps, non-covered claims. |

## Additional evidence

| Path | Bytes | Description |
|---|---|---|
| `report/evidence/replicate.py` | ~24 KB | 585-LOC reproduction script; deterministic seed 20260705. |
| `report/evidence/results.json` | ~15 KB | All numeric outputs (C1..C4). |
| `report/evidence/replicate.log` | ~1.5 KB | Stdout tee'd during the full run. |
| `work/paper.txt` | ~52 KB | pdftotext -layout output used for reading. |
| `work/paper_plain.txt` | ~50 KB | pdftotext (no layout) for grep. |
| `work/venv/` | (large) | Python venv with qiskit/numpy/scipy pinned. |

## Verdict at a glance
| Claim | Description | Verdict |
|---|---|---|
| C1 | Theorem 1 estimator O(log(1/δ)/ε²) | **REPLICATED** — 0/60 fail in every ε,δ cell. |
| C2 | Theorem 3 λ-shift reduction (n-bit θ) | **REPLICATED** — shifted fail rate ≤ η in 4/4 channels. |
| C3 | Theorem 5 tolerable η at N=2¹⁰ | **REPLICATED** — matches paper to within 0.001 for K∈{2,3,4}. |
| C4 | Period-finding via noisy iQFT | **REPLICATED** — shifted success ≥ 0.86 vs paper bound 0.73–0.79 in 5/5 configs. |

**Overall wave verdict: REPLICATED.**
