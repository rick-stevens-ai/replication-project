# Workflow — textures-polar-zhang2024 (arXiv:2411.05576)

1. **ACQUIRE** — `curl -sL https://arxiv.org/pdf/2411.05576 -o zhang2024.pdf` (2.4 MB, `%PDF-1.7` verified).
2. **PARSE** — `pdftotext zhang2024.pdf work/textures-polar-zhang2024.txt` (935 lines).
3. **READ + CLASSIFY** — Flagged class=EXPERIMENT / likely drop. Honest read shows this is **NOT** an experiment-only paper: it contains a fully reproducible analytic theory core:
   - Eq.(1) twisted hexagonal SPP interference axial field.
   - Eq.(2) normalized 3D polarization unit vector.
   - Eqs.(3,4) skyrmion-number-density integral Q = (1/4pi) ∬ s d²r, s = E̅·(∂ₓE̅ × ∂_yE̅).
   - Explicit numeric claims: elementary Q=±1; moiré cluster Q=−3 at θ=38.21°.
   The FDTD + fabrication + near-field microscopy are auxiliary, not the only content.
   → **REPLICATE**, not DROP.
4. **BUILD from scratch** — `code/replicate_zhang2024.py`: implements Eq.(1)→(4) with transverse field from ∇·E=0, computes Q via Berg–Lüscher solid-angle (provenance: Ollie kernel) + FD cross-check.
5. **SAVE-EARLY** — `work/zhang2024_result.json` written; copied to `report/evidence/`.
6. **COMPARE + SCORE** — elementary lattice reproduced exactly (Q=+1); cluster Q=−3 partial (needs Supplemental σ_j / cell). Verdict PASS-PARTIAL, C=0.6 A=0.7.
7. **ARTIFACTS** — extraction/{marker.md,nougat.mmd}, report/{REPORT.tex,open_questions.json,workflow.md,artifacts_summary.md,failure_analysis.md}, evidence/{result,code}.
8. **RE-JUDGE** — physics core built → judge_verdict.py invoked.

## Provenance
Berg–Lüscher kernel adapted from `~/shared-kernels-cache/ollie_berg_luscher_topological_charge_kernel.py`. TDGL phase-field kernel not needed (no free-energy relaxation in this paper — it is a direct interference-field construction). CPU-only, numpy.
