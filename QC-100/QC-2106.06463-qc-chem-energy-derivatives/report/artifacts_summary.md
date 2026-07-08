# Artifacts summary — arXiv:2106.06463

Set: QC-100. Dir: `QC-2106.06463-qc-chem-energy-derivatives/`. Verdict: **REPLICATED**.

## Artifact inventory

| # | Artifact | Path | Purpose |
|---|---|---|---|
| 1 | Replication report (Markdown) | `report/REPORT.md` | Main narrative: verdict, claim table, method, results, caveats. |
| 2 | Replication report (LaTeX) | `report/REPORT.tex` | Typeset version with critique / honest-assessment section. |
| 3 | Open questions (JSON) | `report/open_questions.json` | 5 truly-open questions w/ basis + concrete next steps. |
| 4 | Open questions (LaTeX) | `report/open_questions_section.tex` | Renderable §Open questions block. |
| 5 | Workflow log | `report/workflow.md` | End-to-end steps taken during replication. |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file. |
| 7 | Failure analysis | `report/failure_analysis.md` | Honest critique of gaps and threats to validity. |
| 8 | Nougat extraction stub | `extraction/nougat.mmd` | Marker/nougat text-extraction placeholder for parser stage. |

## Supporting evidence (already on disk from 2026-07-03 run)

| Path | What |
|---|---|
| `code/vqe_h2_gradients.py` | Independent PennyLane implementation (VQE + VQE-FD + VQE-HF). |
| `code/geom_opt_h2.py` | Gradient-descent geometry optimizer. |
| `report/evidence/vqe_h2_gradients.json` | Per-R energies, gradients, optimal params. |
| `report/evidence/geom_opt_h2.json` | Geometry-opt trajectory + final result. |
| `report/evidence/run_log.txt` | Stdout — 5-point scan. |
| `report/evidence/geom_opt_log.txt` | Stdout — geometry opt. |
| `work/paper.pdf` | Source arXiv preprint. |
| `work/paper.txt` | Plain-text extraction of paper (for claim-mining). |

## Headline result

- **5/5 bond lengths:** VQE energy matches FCI to <10⁻⁸ Ha residual.
- **5/5 bond lengths:** VQE-FD gradient matches FCI-FD gradient to ~10⁻⁸ Ha/Å.
- **Geometry opt:** converges in 7 iterations to (R=0.7349 Å, E=−1.137306 Ha)
  vs paper's (0.741 Å, −1.137 Ha). |ΔE| = 0.306 mHa, ~5× under chemical
  accuracy.

## Compute footprint

- 1 CPU core, macOS 25.3.0 / Python 3.14.6.
- 10.2 s (5-point scan) + 15 s (geometry opt) = ~25 s total.
- No GPU / HPC required. Free-endpoint replication (local classical sim only).
