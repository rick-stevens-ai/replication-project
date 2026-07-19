# Artifacts summary --- fernandes2026 (arXiv:2606.26239)

Paper: **Anomalous Hall viscosity of altermagnets**, Jang, Aquino, Schmalian & Fernandes (2026).
Verdict: **REPLICATED** | Coverage 7/10 | Agreement 9/10.

## The 8-artifact completion bar

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-spin-fernandes2026.pdf` | present (2.0 MB) |
| 2 | Marker text extraction | `extraction/marker.md` | interim (pdftotext -layout; marker not installed) |
| 3 | Nougat math-text extraction | `extraction/nougat.mmd` | interim (pdftotext; nougat not installed) |
| 4 | Detailed report + critique | `report/REPORT.tex` | complete |
| 5 | Open questions + next steps | `report/open_questions.json` | complete (5 heavy Qs + next_steps) |
| 6 | Workflow / tools / effort | `report/workflow.md` | complete |
| 7 | Artifact inventory (this file) | `report/artifacts_summary.md` | complete |
| 8 | Failure / gap analysis | `report/failure_analysis.md` | complete |
| + | Evidence (real outputs) | `report/evidence/` | complete |
| + | Code + intermediates | `work/` | complete |

## Evidence traces (`report/evidence/`)
- `fernandes2026_result.json` --- full run output: converged eta^H(mu=0) at N=24/48/96/160,
  the mu sweep (Fig. 2e shape), peak values, unit conversion, verdict/coverage/agreement, gaps.
- `fernandes2026_replicate.py` --- the from-scratch numpy kernel (also in `work/`).

## Headline numbers (traceable to evidence JSON)
- `eta_mu0_N160` = **8.4142 hbar/v_uc** (converged; identical to N=48/96 to 4+ digits).
- `eta_mu0_uPa_s` = **7.10 uPa*s**  vs  paper **8.15 uPa*s** (`paper_claim_uPa_s`). Within ~13%.
- `hbar_over_vuc_in_uPa_s` = 0.8437 (conversion anchor, a0 = 5 A).
- `paper_claim_hbar_vuc` = 9.66 (paper "order 10").
- eta^H proportional to phi confirmed: 2.78 / 5.11 / 8.41 / 10.6 hbar/v_uc for phi = 1/2/4/6.
- Equal-sign d-wave relation eta_xxxy = eta_yyxy confirmed (vs FM opposite sign).

## Extraction tool note
marker-pdf and nougat are not installed on this host. Artifacts 2 and 3 were produced
with `pdftotext` (poppler) as the documented interim fallback; both files carry headers
stating this plus the exact regeneration commands. Equation transcriptions were done by
hand into `report/REPORT.tex`. This is flagged honestly rather than silently substituted.

## Reproduce
```bash
cd work/            # or report/evidence/
/home/stevens/comfyui-env/bin/python fernandes2026_replicate.py
# writes fernandes2026_result.json; ~3 s wall on a CPU node
```
