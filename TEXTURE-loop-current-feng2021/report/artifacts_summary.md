# Artifacts Summary: feng2021 (Chiral Flux Phase in kagome AV3Sb5)

**Paper:** Feng, Jiang, Wang, Hu, "Chiral flux phase in the Kagome superconductor AV3Sb5", arXiv:2103.07097 (2021)
**Verdict:** PARTIAL (qualitative claim replicated; quantitative energetics ~15× off)

## 8-artifact package
| # | Artifact | Path | Contents |
|---|---|---|---|
| 1 | Extraction (marker) | `extraction/marker.md` | pdftotext-interim extraction + paper header (marker unavailable) |
| 2 | Extraction (nougat) | `extraction/nougat.mmd` | Mathpix-md interim: hand-transcribed Eqs.1,4,7,9,10 + full text (nougat unavailable) |
| 3 | Report | `report/REPORT.tex` | Full LaTeX report: claim, method, results table, assessment |
| 4 | Open questions | `report/open_questions.json` | 5 Qs {question, why_it_matters, next_step} + next_steps list |
| 5 | Workflow | `report/workflow.md` | Step-by-step reproduction recipe |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | Match/mismatch tables + root-cause hypotheses |
| 8 | Evidence dir | `report/evidence/` | result JSON + replication code + both kernels + recipe |

## Physics result (3-line summary)
- From-scratch NN kagome tight-binding on a 12×12 PBC cluster (432 sites) at 5/4 van Hove
  filling reproduces the paper's central result: the **chiral flux phase (imaginary 3Q bond
  order) has the lowest energy at λ=0.3** (E=−2.6770 t/cell) and wins for all λ≥0.2.
- CFP is the **only** time-reversal-breaking order (complex H) with machine-zero net site
  current (~1e-16), consistent with the loop-current / anomalous-Hall interpretation.
- Quantitative splittings (CBO−CFP=0.013 t, vCDW−CFP=0.007 t) are ~15× smaller than the
  paper's (0.195 t, 0.435 t) and the vCDW/CBO sub-ordering is reversed → **PARTIAL**.

## Self-score
- **Coverage: 7/10** — full model built from scratch, all 3 orders, energy sweep, TRS &
  current-conservation diagnostics, 8 artifacts. Not covered: Chern/σ_xy of folded bands,
  self-consistent U-V, real-space charge pattern (Fig.3).
- **Agreement: 6/10** — qualitative winner, symmetry classification, and TRS-breaking all
  match; absolute energy splittings and vCDW/CBO sub-order do not.

## Kernel credit
`loop_current_kagome_kernel.py` (geometry, half-bond Bloch convention, Peierls flux, FHS Chern)
and `loop_current_meanfield_kernel.py` (real-space cluster, J_ij=-2Im[H_ij ρ_ji]) — shared
TEXTURES-100 kernels. Reproduce: `cd work && /home/stevens/comfyui-env/bin/python feng2021_replication.py 12`
