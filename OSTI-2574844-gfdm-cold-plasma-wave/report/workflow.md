# Workflow — OSTI 2574844 replication

Paper: Spencer et al., "An implementation of a high-order generalized finite
difference method for solving the time-harmonic cold plasma wave equation in
toroidal geometry," Phys. Plasmas 32, 063902 (2025). DOI 10.1063/5.0255884.

Replication date: 2026-07-02. Verdict: **REPLICATED**.

## Stage 0 — Paper ingestion
- OSTI record 2574844 downloaded; PDF used as the specification (no author code
  or data existed publicly, so the paper's equations were the reference).
- Focus locked on Sec. III (GFD construction: Eqs. 3–9, Table III) and
  Sec. V.A / Fig. 2 (convergence-order verification).

## Stage 1 — Claim triage
Four candidate claims were extracted (see REPORT.md §2):
- **C1** — per-node derivative operator order (2nd deriv → O(h^{m-1})).
- **C2** — full BVP solve order vs analytic plane wave (Fig. 2).
- **C3** — physics-informed monitor-function point generator.
- **C4** — ICRH/ECRH mock-tokamak qualitative demos.

C1 and C2 were selected as the falsifiable numerical core (they carry the
paper's only quantitative verification target). C3 is algorithmic; C4 has no
analytic ground truth. Both were declared out-of-scope for an efficient
replication and are flagged in the critique and open_questions.

## Stage 2 — Reimplementation from equations
Directory: `../work/` (all code lives here).

1. **`gfdm_core.py`** — the reusable GFD kernel.
   - `deriv_terms(m)`, `taylor_col()` build Taylor columns
     dx^{px} dy^{py} / (px! py!) up to total order m.
   - `gfd_weights(dxy, m)` assembles the star matrix S, applies the column
     scaling D_2 = diag(1/max_k |S_kl|), computes the TSVD Moore–Penrose
     pseudoinverse, and returns W = D_2 (S D_2)^+ and the condition number κ_i.
   - `build_cloud()` — jittered unit-square node distribution.
   - `select_star()` — nearest-neighbor star selection at
     ~3 × N_deriv nodes per Taylor order (17 / 31 / 41 for m = 2 / 3 / 4).
   - No distance weighting: D_i1 = I, matching Sec. III.C.

2. **`test_C1_derivative_order.py`** — derivative-operator convergence.
   - Manufactured field f = sin(2πx) cos(2πy).
   - For each m ∈ {2, 3, 4} and each n ∈ {15, 25, 35, 45, 65}, compute GFD
     approximations to f_x and f_xx at interior nodes, NRMSD vs exact,
     log–log slope over the 5 refinements.
   - Emits `evidence_C1.json`.

3. **`test_C2_planewave_solve.py`** — full BVP convergence.
   - Cartesian / infinite-cylinder reduction (n_u/R → k_z, drop 1/R terms).
   - Homogeneous dielectric tensor → E = exp(i(k_x x + k_y y)),
     k_x² + k_y² = k_⊥² is an exact solution.
   - Assemble sparse Laplacian–Helmholtz operator via GFD second-derivative
     weights; impose the analytic plane wave on the boundary; solve with
     `scipy.sparse.linalg.spsolve`; NRMSD vs analytic; log–log slope.
   - Well-resolved regime: 2 wavelengths across L = 1, 20–65 pts/λ
     (satisfies the paper's ≥10 pts/λ recommendation).
   - Emits `evidence_C2.json`.

## Stage 3 — Execution
- Environment: local Python 3 with numpy / scipy; no GPU, no exotic
  dependencies.
- Both drivers run in a couple of minutes wall-clock; the whole replication
  fits inside the <25 min "efficient replication" budget.
- Coarse first pass (<10 pts/λ) produced large noisy NRMSDs consistent with
  the pollution effect the paper describes; the reported numbers are from the
  well-resolved regime.

## Stage 4 — LLM judge
- Model: `argo:gpt-5.2` via the free Argo proxy (`localhost:44497`,
  Bearer stevens).
- Input: the C1 and C2 evidence tables and the paper's Fig. 2 rate claim.
- Verdict: "High agreement… VERDICT: REPLICATED." Coverage estimate ≈ 55%
  of the numerical core.

## Stage 5 — Reporting
- `REPORT.md` — canonical markdown replication report (~7 KB).
- `REPORT.tex` — LaTeX version with dedicated Genuine Critique section.
- `open_questions.json` — 5 genuinely open follow-ups grounded in what was
  NOT tested (resonance-crossing, monitor generator, TSVD tolerance,
  boundary stars, 3D solver scalability).
- `workflow.md` — this file.
- `artifacts_summary.md` — inventory of what lives where.
- `failure_analysis.md` — what almost went wrong, and what would falsify the
  REPLICATED verdict.

## Compute / provenance
- Host: local (CherryRd), no HPC needed.
- Endpoints used: Argo proxy for the LLM judge only. All numerical work was
  local scipy.
- No paid API calls. No proprietary data.
