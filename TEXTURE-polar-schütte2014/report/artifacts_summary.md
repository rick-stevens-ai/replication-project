# Artifacts Summary — Schütte & Garst (arXiv:1405.1568)

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Replication code | `code/schutte2014_replication.py` | End-to-end: skyrmion relaxation → magnon operator → bound states → scattering → Thiele proxy |
| 2 | Results (machine-readable) | `work/results.json` | Per-claim expectation/reproduced/match/note + numbers |
| 3 | Report (LaTeX) | `report/REPORT.tex` | Full write-up |
| 3 | Report (PDF) | `report/REPORT.pdf` | Compiled PDF |
| 4 | Open questions | `report/open_questions.json` | 5 open questions {q, basis, next_steps} |
| 5 | Workflow | `report/workflow.md` | Step-by-step method + environment |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | Failures, fixes, residual limitations |
| 8 | Metadata | `META.json` | Status + verdict |

## Figures (`figs/`)
- `skyrmion_profile.png` — relaxed axisymmetric θ(r) and n_z(r).
- `bound_state_wavefunctions.png` — radial wavefunctions of the breathing (m=0) and quadrupolar (m=±2) sub-gap modes.
- `cross_section_polar.png` — dσ/dθ polar plot showing left-right skew.
- `cross_section_cartesian.png` — dσ/dθ vs angle with skew asymmetry annotated.

## Headline results (B=0.4, gap Δ=0.4, dimensionless units)
- **Claim 1 (bound states) — REPLICATED (structure):** breathing m=0 at ω=0.158; quadrupolar m=+2 at ω=0.318; both below gap 0.4, correct ordering (breathing < quadrupolar).
- **Claim 2 (skew scattering) — REPLICATED (qualitative):** phase shifts asymmetric in ±m (e.g. δ_{+1}−δ_{−1}=+1.42), left-right asymmetry A=−0.29, multi-peak (rainbow) dσ/dθ.
- **Claim 3 (Thiele/Hall, stretch) — qualitative:** transverse momentum-transfer σ_perp=−4.08, Hall-angle proxy −0.34 (nonzero ⇒ sideways force on skyrmion).
