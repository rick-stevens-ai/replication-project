# Artifacts Summary — lee2025 (altermagnet spin splitting)

**Paper:** Lee, Kim & Kim (2025), *Microscopic origin of the spin-splitting in altermagnets.*
**Verdict:** REPLICATED (7/7 checks) · **Coverage 8/10** · **Agreement 10/10**

## 8 artifacts
| # | Artifact | Path | Purpose |
|---|----------|------|---------|
| 1 | Marker extraction (interim) | `extraction/marker.md` | pdftotext -layout body + header |
| 2 | Nougat extraction (interim) | `extraction/nougat.mmd` | MMD header + text body |
| 3 | Report | `report/REPORT.tex` | Full LaTeX replication report |
| 4 | Open questions | `report/open_questions.json` | 5 Qs (question/why/next_step) + next_steps |
| 5 | Workflow | `report/workflow.md` | End-to-end method log |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | Scope, approximations, caveats |
| 8 | Evidence | `report/evidence/lee2025_result.json`, `report/evidence/lee2025_replicate.py` | Result JSON + from-scratch code |

## Physics core (3-line summary)
- Built the minimal 2D square-lattice 4-band altermagnet Hamiltonian (Eqs 1–2) from scratch, diagonalized numerically with spin labels, and matched the analytic band formula Eq (3) to 1e-15.
- Confirmed the spin splitting ΔE ∝ 2·t_{k,z}·h_eff is a d_{xy}-wave form factor (nodal on k_x=0/k_y=0, sign-changing across quadrants) and is monotonic in both δt and h_eff (reproducing Fig 4d).
- Verified the paper's central "two-ingredient" rule: momentum-dependent (altermagnetic) spin splitting is nonzero ONLY when both δt≠0 AND h_eff≠0.

## Key numbers
- ΔE at (π/2,π/2) = 1.109 t₁; anisotropic splitting "both_on" = 1.174 t₁, all single-term cases = 0.
- Runtime ≈ 0.08 s (`comfyui-env/bin/python`).

## Credit
Kubo/Berry methodology reference: `gobel2024_sd_skyrmion_kubo_Lz_kernel.py` (shared-kernels-cache), cited for the AHE follow-up; core here is SOC-free direct diagonalization.
