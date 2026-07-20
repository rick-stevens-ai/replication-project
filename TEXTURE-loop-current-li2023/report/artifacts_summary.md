# Artifacts Summary — li2023

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Marker extraction | `extraction/marker.md` | Interim pdftotext extraction + curated header with transcribed Eq.(2)-(6) and Fig.4 params |
| 2 | Nougat extraction | `extraction/nougat.mmd` | Interim stand-in: header + verbatim paper body (906 lines pdftotext) |
| 3 | Report | `report/REPORT.tex` | Full LaTeX replication report (claim, method, results table, agreement, verdict) |
| 4 | Open questions | `report/open_questions.json` | 5 questions {question, why_it_matters, next_step} + next_steps list |
| 5 | Workflow | `report/workflow.md` | Step-by-step replication procedure + reproduce command |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | Honest limitations, what didn't match, why |
| 8 | Evidence (code+data) | `report/evidence/li2023_patch_model.py`, `report/evidence/li2023_result.json` | From-scratch 6×6 patch model + all scan results |

## Result files
- **Primary data:** `work/li2023_result.json` (SAVE-EARLY), mirrored to
  `report/evidence/li2023_result.json`.
- **Code:** `report/evidence/li2023_patch_model.py`.

## Verdict
**REPLICATED** (mechanism + λ² scaling + instability condition);
**PARTIAL** on the closed-form Eq.(4) absolute prefactor.
- Coverage: **8/10**
- Agreement: **8/10**

## Key numeric evidence
- λ=0 → CBO⁻/LCBO degenerate (Δf ≈ −2×10⁻¹⁶). ✓ gauge argument
- Δf ∝ λ^1.98 (predicted λ²). ✓
- sign(Δf) matches δε < 4(|b|²+|b'|²)|Δ| in 7/7 tested |Δ|. ✓
- Eq.(4) prefactor magnitude ≠ full-diagonalization Δf. ✗ (SM normalization gap)

## Kernel credit
TEXTURES-100 shared kernels `loop_current_meanfield_kernel.py` and
`loop_current_kagome_kernel.py` (imaginary bond order = loop current = Peierls
flux current convention).
