# Artifacts Summary — Wernert et al. 2024

**Verdict: REPLICATED** | Coverage 8/10 | Agreement 9/10

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Extraction (marker) | `extraction/marker.md` | Metadata + key equations extracted (Eqs.1,2,5,7,11,12,13) + headline |
| 2 | Extraction (nougat) | `extraction/nougat.mmd` | pdftotext interim text layer + Nougat-compatible header (844 lines) |
| 3 | Report | `report/REPORT.tex` | REVTeX PRL-style replication report |
| 4 | Open questions | `report/open_questions.json` | 5 Qs {question, why_it_matters, next_step} + global next_steps |
| 5 | Workflow | `report/workflow.md` | End-to-end replication workflow |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | What was NOT reproduced + why |
| 8 | Evidence | `report/evidence/wernert2024_result.json`, `report/evidence/wernert2024_replication.py`, `report/evidence/replication_recipe.json` | Result JSON + from-scratch code + recipe |

## Physics summary (3 lines)
1. A static twist of the noncollinear kagome AFM order (∂_x n_α = (∂_x φ) n_x×n_α) produces a **purely transverse** Noether spin current J^y = ±(√3/8)JS²(∂_x φ)n_y — reproduced **exactly** by symbolic re-derivation, with J^x≡0.
2. The dynamical d.c. Hall spin current ⟨J_y^y⟩=Γ_yx^{yx}P_x^x **flips sign** between direct (Mn₃Ir) and inverse (Mn₃Sn) triangular order, matching Fig.2.
3. In a polycrystal the isotropic **Hall mass g_H** splits the transverse and longitudinal magnon velocities (split = 2g_H/ρ), is O(3)-invariant, and is therefore a generic classifier of all noncollinear AFMs.

## Kernel credit
Kubo/Berry itinerant-texture sibling method: `gobel2024_sd_skyrmion_kubo_Lz_kernel.py` (Göbel 2024, arXiv:2410.00820).

## Reproduce
```bash
/home/stevens/comfyui-env/bin/python work/wernert2024_replication.py
```
Runtime ~0.06 s (sympy 1.14.0 + numpy 2.3.5).
