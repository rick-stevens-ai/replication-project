# Artifacts summary — QC-200 / arXiv:1605.07197

All paths are relative to
`~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1605.07197-magic-state-factories-obrien/`.

## 8 mandatory artifacts (per QC brief)

| # | Artifact | Path | Size | Status |
|---|---|---|---|---|
| 1 | Original PDF | `paper.pdf` | 7.4 MB | ✅ downloaded from arXiv:1605.07197v2 |
| 2 | Marker extraction | `extraction/marker.md` | ~7 KB | ⚠️ pdftotext-fallback (Marker not installed; central corpus absent) |
| 3 | Nougat extraction | `extraction/nougat.mmd` | ~3 KB | ⚠️ placeholder mmd-flavoured (Nougat not installed) |
| 4 | LaTeX report | `report/REPORT.tex` (+ `REPORT.pdf`) | ~14 KB tex | ✅ full section-by-section, includes verdict |
| 5 | Open questions | `report/open_questions.json` + `## Open Questions` in report | ~5 KB json | ✅ 5 questions, each with q/basis/next_steps |
| 6 | Workflow + tool list + effort estimate | `report/workflow.md` | ~3 KB | ✅ |
| 7 | Artifact inventory | `report/artifacts_summary.md` (this file) | | ✅ |
| 8 | Failure analysis | `report/failure_analysis.md` | | ✅ |

## Evidence directory contents

| File | Role |
|---|---|
| `report/evidence/reproduce_15to1.py` | Analytic reproduction of C1/C2/C3/C4. Emits `results_analytic.json`. |
| `report/evidence/qiskit_15to1_sanity.py` | Qiskit statevector Monte-Carlo. Emits `qiskit_sanity.json`. |
| `report/evidence/plot_scaling.py` | Log-log plot. Emits `distillation_scaling.png`. |
| `report/evidence/results_analytic.json` | Machine-readable analytic reproduction results. |
| `report/evidence/qiskit_sanity.json` | Machine-readable Qiskit MC results. |
| `report/evidence/distillation_scaling.png` | 15-to-1 scaling plot (analytic curve + MC points). |

## Work directory contents

| File | Role |
|---|---|
| `work/paper.txt` | 3169-line pdftotext extraction of the full paper. |
| `work/venv/` | Python 3.13 virtualenv with qiskit 2.5.0, numpy 2.4.3, matplotlib 3.10.8. |

## Traces / provenance

- **Random seed for Qiskit MC:** `np.random.default_rng(20250705)` in `qiskit_15to1_sanity.py` — the MC results are deterministic and re-runnable.
- **Every scalar in the LaTeX report** is either (a) quoted directly from `work/paper.txt` at a specific line number, or (b) computed by one of the scripts and stored in the JSON files under `report/evidence/`. Nothing is hand-typed from memory.
- **All commands** executed as of 2026-07-05 12:43 CDT on CherryRd (`Darwin 25.3.0 x86_64`).
