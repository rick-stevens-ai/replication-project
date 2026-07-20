# Artifacts Summary

| Artifact | Path | Description |
|---|---|---|
| Paper | `paper.pdf` | arXiv:1807.09258 (fetched; dir was empty at task start) |
| Extracted text | `work/paper.txt` | pdftotext of the paper (main + Supplemental) |
| Model code | `code/model.py` | spin-1 ops, quadrupoles, d-vector maps, Gell-Mann generators |
| Algebra checks | `code/verify_claims.py` | C1-C5, 12 sub-checks |
| ED surrogate | `code/ed_structure_factor.py` | sparse ED of BLBQ model, structure factors |
| Algebra results | `work/verification_results.json` | machine-readable PASS/FAIL + residuals |
| ED results | `work/ed_structure_factor.json` | m_S^2(q), m_Q^2(q), peaks per cluster |
| Report (LaTeX) | `report/REPORT.tex` | full writeup |
| Report (PDF) | `report/REPORT.pdf` | compiled (if TeX toolchain present) |
| Open questions | `report/open_questions.json` | exactly 5, {q, basis, next_steps} |
| Workflow | `report/workflow.md` | reproduction steps |
| Failure analysis | `report/failure_analysis.md` | what broke, root cause, fixes |
| This summary | `report/artifacts_summary.md` | index |

## Claims verified (all in-scope PASS)

- **C1** biquadratic operator identities — residual ~1e-15
- **C2** d-vector -> spin/quadrupole maps (Eqs. S16-S22) — residual ~5e-16; gs directors carry zero dipole
- **C3** (pi,pi)-AFQ gs: staggered <Q^{x2-y2}>=∓1; nn energy minimized, 2nd-nbr overlap maximized
- **C4** Gell-Mann U(phi) unitary; SU(3)-point energy invariant (flat/marginal direction) — residual ~1e-15
- **C5** two-site SU(3) multiplet degeneracies {6,3}; splits away from J=K
- **C6** ED: dominant quadrupolar peak at (pi,pi), weak dipole at (pi,0)/(0,pi) on 2x2 and 2x4

## Verdict
**REPLICATED (core algebra + qualitative numerics).**
Coverage **7/10**, Agreement **9/10**.

Out-of-scope (marked, not attempted numerically): full DMRG magnitudes / thermodynamic-limit
finite-size scaling; field-theoretic momentum-shell RG derivation of the sqrt(Λ/K_F)
Kondo-vertex suppression; conduction-electron Fermi-surface-jump dynamics.
