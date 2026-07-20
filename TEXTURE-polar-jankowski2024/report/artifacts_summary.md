# Artifacts summary — jankowski2024

**Paper:** Jankowski, Bennett, Agarwal, Chaudhary & Slager (2024), "Polarization
textures in crystal supercells with topological bands", arXiv:2404.16919v2.
**Verdict: REPLICATED** (mechanism-level, 4/4 sub-claims). Coverage 7/10, Agreement 9/10.

## The 8 artifacts
| # | Artifact | Path | Purpose |
|---|----------|------|---------|
| 1 | Extraction (marker) | `extraction/marker.md` | Headline + equations extracted (pdftotext interim for Marker) |
| 2 | Extraction (nougat) | `extraction/nougat.mmd` | Structured .mmd body (pdftotext-layout interim + header) |
| 3 | Report | `report/REPORT.tex` | Full LaTeX replication report |
| 4 | Open questions | `report/open_questions.json` | 5 questions + next_steps |
| 5 | Workflow | `report/workflow.md` | Step-by-step method + reproduce command |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | Scope limits + fixed pitfall |
| 8 | Evidence | `report/evidence/` | result JSON + code + both kernels |

## Physics result (`work/jankowski2024_result.json`)
- T1 meron winding: Q_relaxed = **+0.457** (target +½) ✓
- T2 magnitude drop across TPT: 0.833 → 0.585 (**−29.8%**) ✓
- T3 non-vanishing in topological phase: |P|=0.585 > 0.05 ✓
- T4 winding preserved: |ΔQ| = **0.016** < 0.12 ✓
- Runtime ≈ 1.1 s, grid 81×81, CPU.

## Provenance (both kernels credited)
- `ollie_tdgl_phasefield_polar_skyrmion_kernel.py` — TDGL polar phase-field relaxation.
- `ollie_berg_luscher_topological_charge_kernel.py` — Berg–Lüscher topological charge Q.
