# Artifacts Summary — arXiv:1704.06774 replication

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1704.06774-quantum-tree-size-estimation-ambainis-kokainis/`

## The 8 mandatory artifacts (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path (relative to target dir) | Status |
|---|---|---|---|
| 1 | Original PDF | `paper.pdf` | ✅ 372 KB, 38 pages, arXiv v3 (Dec 2022) |
| 2 | Marker parse | `extraction/marker.md` | ✅ pdftotext -layout fallback (2,123 lines) |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✅ pdftotext -raw fallback (2,606 lines) |
| 4 | LaTeX report | `report/REPORT.tex` + compiled `report/REPORT.pdf` | ✅ 5 pages, pdflatex clean |
| 5 | Open questions | `report/open_questions.json` + `## Open Questions` in REPORT.tex | ✅ 5 non-trivial questions with basis + next_steps |
| 6 | Workflow | `report/workflow.md` | ✅ step-by-step + tool versions + effort estimate |
| 7 | Artifacts summary | `report/artifacts_summary.md` (this file) | ✅ |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ |

## Evidence directory (`report/evidence/`)
| File | Purpose |
|---|---|
| `tree_size_estimation.py` | Main implementation of Algorithm 1 (numpy statevector, real R_A/R_B, exact eigendecomposition). |
| `verify_identity.py` | Enumerates all eigenphases with |start> overlaps; confirms the ±θ_min eigenpair carries >99% of the amplitude, validating the estimator's choice. |
| `scaling_test.py` | Sweeps δ ∈ {1.0…0.005}; empirically shows rel-err ~ 0.093·δ², all runs within Lemma 5 window. |
| `quadratic_speedup.py` | Sweeps depth n ∈ [1,7]; log-log fit of θ_min vs √(nT) gives slope −0.9988 (paper predicts −1); tabulates classical vs quantum query counts. |
| `results_algorithm1.json` | 8 tree instances × (T_true, T̂, θ_min, α, rel_error). |
| `results_complexity.json` | Classical vs quantum query counts for complete binary trees depth 2–14. |
| `scaling_test.json` | δ-sweep raw data. |
| `quadratic_speedup.json` | Depth-sweep raw data + complexity table. |
| `verdict.txt` | REPLICATED (max_rel_error = 2.25e-2 at δ=0.3, well inside Lemma 5's ±30% window). |

## Work directory (`work/`)
| File | Purpose |
|---|---|
| `paper.txt` | `pdftotext -layout` (used for section-by-section reading) |
| `paper_raw.txt` | `pdftotext -raw` (used for nougat.mmd fallback) |

## Reproducibility one-liner
```bash
cd report/evidence
python3 tree_size_estimation.py
python3 verify_identity.py
python3 scaling_test.py
python3 quadratic_speedup.py
```
All four scripts are self-contained (only depend on numpy) and complete in < 5 seconds each on a laptop CPU.

## Traces / logs
- `verdict.txt` records final REPLICATED verdict + max_rel_error.
- Each script prints a table to stdout that mirrors the JSON output for human inspection.
- LaTeX compile transcript: `report/REPORT.log`.
