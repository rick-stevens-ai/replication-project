# Artifacts Summary — TEXTURE-polar-agarwal2024

Paper: Agarwal, Jankowski, Bennett, Slager — *Shift photocurrent vortices from
topological polarization textures*, arXiv:2408.04017.
Replication type: **reduced 2-band k·p model, mechanism-level. Verdict: PARTIAL (4/4 reduced-model checks pass).**

## Files

| Path | Description |
|---|---|
| `paper.pdf` | Original paper (pre-existing) |
| `extraction/marker.md` | Full-text extraction (pre-existing) |
| `report/method_extract.md` | Distilled method + key equations (pre-existing) |
| `code/agarwal2024_replication.py` | Full replication driver (numpy/scipy/matplotlib, CPU) |
| `work/results.json` | Machine-readable results for all claims + verdict |
| `figs/fig1_P_texture_and_sigma_vortex.png` | Meron P(r) texture + σ(r) vortex over vorticity |
| `figs/fig2_sigma_vs_P_correlation.png` | P vs σ overlay + cos-angle map |
| `report/REPORT.tex` / `report/REPORT.pdf` | Write-up |
| `report/open_questions.json` | 5 open questions (q/basis/next_steps) |
| `report/workflow.md` | Step-by-step workflow |
| `report/failure_analysis.md` | Failures + fixes + honest limitations |
| `report/artifacts_summary.md` | This file |
| `META.json` | Status + verdict (updated) |

## Claims reproduced (numbers)

- **Claim 1 — meron quantization:** skyrmion charge Q = +0.498 (meron) / −0.498
  (antimeron); integer in-plane director winding = ±1. **PASS**
- **Claim 2 — shift vortex:** winding of σ(r) around meron core = −1 (co-located vortex).
  **PASS**
- **Claim 3 — σ ∥ P:** ⟨|cos∠(σ,P)|⟩ = 1.00 over 1680 masked points; fraction |cos|>0.8
  = 1.0. **PASS** (parallel in the lower resonance window)
- **Claim 3b — antiparallel window:** ⟨cos∠⟩ = −1.00 at the upper resonance branch,
  reproducing the paper's antiparallel-to-P fingerprint as a frequency-window property.
  **PASS**

## Not reproduced (scope)
Full four-band SU(4) moiré model; DFT cross-check; quantitative ω_M≈6 eV / ω_K≈5 eV
spectrum; individual tensor components σ_{a,bc} per AA/AB/DW stacking.
