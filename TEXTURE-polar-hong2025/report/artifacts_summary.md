# Artifacts Summary — hong2025

**Paper:** Gupta, Tanwani, Xu, Du, ... Hong, Tian, Ramesh, Das (2025),
"Harnessing the polar vortex motion in oxide heterostructures" (PbTiO3/SrTiO3, TDGL phase-field).
**Verdict:** REPLICATED (mechanism-level) — 5/5 claim checks pass, runtime 4.5 s.

## Deliverables (8 artifacts)

| # | Artifact | Path | Contents |
|---|----------|------|----------|
| 1 | Marker extraction | `extraction/marker.md` | pdftotext `-layout` interim + header note (marker-pdf not run this pass) |
| 2 | Nougat extraction | `extraction/nougat.mmd` | pdftotext `-layout` interim + header note (nougat not run this pass) |
| 3 | Report (LaTeX) | `report/REPORT.tex` | Full write-up: claim, from-scratch model, results, agreement, provenance |
| 4 | Open questions | `report/open_questions.json` | 5 Qs {question, why_it_matters, next_step} + next_steps list |
| 5 | Workflow | `report/workflow.md` | Step-by-step method, the v1 failure + fix, pitfalls |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | What broke, limitations, honest scope |
| 8 | Evidence bundle | `report/evidence/` | result JSON + both runner scripts + BOTH credited kernels + figure |

## Evidence bundle contents (`report/evidence/`)
- `hong2025_result.json` — full run output, claim checks, verdict (SAVE-EARLY)
- `hong2025_runner.py` — from-scratch 2D TDGL phase-field runner
- `hong2025_figure.py` — snapshot/winding figure generator
- `hong2025_vortex_phase.png` — relaxed pure-vortex-phase visualization
- `ollie_tdgl_phasefield_polar_skyrmion_kernel.py` — credited method template (TDGL)
- `ollie_berg_luscher_topological_charge_kernel.py` — credited method template (topology)
- `replication_recipe.json` — original recipe

## Key result
- Run A (electric energy ON, eps=4.0): **+21 / -21** alternating polar vortices,
  periodic, `<|P|>`=1.18 → **pure vortex phase**.
- Run B (control, eps=0.05): collapses to near-uniform domain (3/7 stray cores).
- Vortex phase is **regime-selective** and **driven by the electric/bound-charge
  energy**, matching the paper's energy-competition argument.
- Period ~5 nm (right order; paper ~14 nm) — quantitative tuning left as next step.

## Provenance / credit
Both shared kernels credited in `REPORT.tex`, `hong2025_result.json`
(`provenance_credit`), and `workflow.md`.
