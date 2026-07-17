# Artifacts Summary — feng2026

**Paper:** feng2026, arXiv:2602.19076 — *Magnetic Orbital Hall Effect in d-wave altermagnets*
**Verdict:** PARTIAL (d-wave symmetry reproduced; MOHE magnitude method-limited; material DFT out of scope)

## Inventory
| Artifact | Path | Status |
|---|---|---|
| Original PDF | `paper.pdf` | ✅ |
| Marker extraction | `extraction/marker.md` | ✅ |
| Reproduction code | `work/reproduce.py` | ✅ |
| Results | `work/results.json` | ✅ |
| Band figure | `work/figs/bands.png` | ✅ |
| MOHE figure | `work/figs/mohe_vs_mu.png` | ✅ |
| LaTeX report | `report/REPORT.tex` (+ `.pdf`) | ✅ |
| Open questions | `report/open_questions.json` (5) | ✅ |
| Workflow | `report/workflow.md` | ✅ |
| Artifacts summary | `report/artifacts_summary.md` | ✅ |
| Failure analysis | `report/failure_analysis.md` | ✅ |

## Key-number trace
- **C1 d-wave altermagnet spin splitting:** 0.365 eV on the x-axis (kx,0); **0.0 eV on the BZ diagonal** (kx=ky). d-wave nodal structure confirmed (spin split ∝ cos kx − cos ky). **MATCH.**
- **C2 MOHE σ^{Lz}_xy:** ~1e-22 at μ=−0.04 and μ=0.06 → numerical zero under the linear intraband implementation. **METHOD-LIMITED** (not a paper refutation; see failure_analysis.md).
- **C3 symmetry-allowed components:** allowed xy ≈ forbidden xx ≈ numerical zero → not numerically resolved. **METHOD-LIMITED.**
- **C4/C5/C6 material DFT (CrSb, FeSb2):** **OUT OF SCOPE** — need Ref[50] SM DFT params + VASP/QE + Wannier90.

## Traces of the replication
- Model parameters read directly from the paper (Eqs.6–8 + stated values); no fitting.
- Band-symmetry result is parameter-exact and convention-independent (depends only on the τz(cos kx − cos ky) altermagnet term).
- MOHE cancellation reproduced deterministically across k-mesh sizes (60² and 90²), confirming it is a method limitation, not a convergence artifact.
