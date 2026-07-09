# Artifacts Summary — OSTI 2574844

Paper: Spencer et al., high-order GFD for the time-harmonic cold-plasma wave
equation (Phys. Plasmas 32, 063902, 2025).
Directory: `~/Dropbox/REPLICATE-PROJECT/OSTI-2574844-gfdm-cold-plasma-wave/`.
Verdict: **REPLICATED**.

## report/
| File | Purpose |
|---|---|
| `REPORT.md` | Canonical human-readable replication report (~7 KB). Source of truth for verdict, claims table, results table. |
| `REPORT.tex` | LaTeX version of the same, with an explicit Genuine Critique section. |
| `open_questions.json` | 5 genuinely open questions grounded in GFDM-for-cold-plasma follow-up work not covered by the current replication. |
| `workflow.md` | End-to-end workflow: paper ingestion → claim triage → reimplementation → execution → LLM judge → reporting. |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Near-misses, sensitivity notes, and what would falsify the REPLICATED verdict. |

## work/  (code — see REPORT.md §3 for full description)
| File | Purpose |
|---|---|
| `gfdm_core.py` | Reusable GFD kernel: `deriv_terms(m)`, `taylor_col()`, `gfd_weights(dxy, m)` (S → D_2 → TSVD Moore–Penrose pinv → W and κ_i), `build_cloud()`, `select_star()`. Faithful to Eqs. 3–9 and Table III; no distance weighting (D_i1 = I). |
| `test_C1_derivative_order.py` | C1 driver: manufactured f = sin(2πx) cos(2πy), NRMSD of GFD f_x and f_xx across 5 resolutions, log–log slope for m ∈ {2, 3, 4}. |
| `test_C2_planewave_solve.py` | C2 driver: homogeneous-tensor Cartesian reduction, plane-wave BVP, sparse Laplacian–Helmholtz assembled from GFD 2nd-derivative weights, `scipy.sparse.linalg.spsolve`, NRMSD vs analytic, log–log slope. |
| `evidence_C1.json` | Per-(m, n) NRMSDs and fitted convergence orders for the derivative test. |
| `evidence_C2.json` | Per-(m, n) NRMSDs and fitted convergence orders for the plane-wave BVP solve. |

## Key numerical results (from REPORT.md §4)
- **C1 — derivative order (paper: f_x ≈ m, f_xx ≈ m-1)**
  - m = 2 → f_x 1.99, f_xx 1.23
  - m = 3 → f_x 3.48, f_xx 1.97
  - m = 4 → f_x 4.02, f_xx 3.32
- **C2 — plane-wave BVP order (paper: p ≈ m-1), k_⊥ = 4π**
  - m = 2 → order 2.30, NRMSD 2.3e-1 → 1.5e-2
  - m = 3 → order 2.95, NRMSD 1.0e0  → 2.8e-2
  - m = 4 → order 3.92, NRMSD 5.5e-3 → 5.4e-5
- **LLM judge (`argo:gpt-5.2`)**: REPLICATED; coverage ≈ 55 %.

## Provenance
- No public author code or data existed; this is a from-equations
  reimplementation.
- All compute local (CherryRd). Argo proxy used only for the LLM judge
  (free endpoint).
- Wall-clock: entire replication fits in the <25 min efficient budget.

## What is NOT here
- The full anisotropic cold-plasma dielectric tensor implementation
  (out of scope; the paper's own verification target does not use it either).
- Physics-informed monitor-function point generator (C3 — see open Q2).
- ICRH / ECRH mock-tokamak demos (C4 — qualitative, no analytic target).
- Toroidal geometry / curvilinear coordinates (out of the Cartesian
  reduction used for C2).
