# Attempt Log — PDE-Pearson-Stoll-Wathen-precond-2012

Chronological log.

**2026-07-04 18:08 CDT.** Task received. Created target dir `~/Dropbox/REPLICATE-PROJECT/PDE-Pearson-Stoll-Wathen-precond-2012/` with `report/evidence/` and `work/`. Confirmed sibling dirs untouched.

**18:09.** Confirmed paper metadata via Edinburgh Research Explorer (author-of-record page) — Pearson, Stoll, Wathen 2012, SIAM J. Matrix Anal. Appl. 33(4):1126–1152, DOI 10.1137/110847949. Abstract confirms: distributed heat control + Neumann boundary Poisson/heat control, Schur-complement approximation, MINRES, eigenvalue bounds proved, mesh/timestep/regularization-parameter-robust iteration counts claimed.

**18:10.** Set up local venv in `work/.venv` with numpy 2.5.1 + scipy 1.18.0 + matplotlib. All computations local (problem size ≤ 3600–63504 DoF), no need for uicgpu.

**18:11.** Wrote `fem2d.py`: 2D P1 FEM assembly on unit square with structured criss-cross triangulation, homogeneous Dirichlet BC, closed-form element mass and stiffness matrices, interior-node restriction. Verified `sum(M) → 1` as h → 0 (interior mass ≈ area) on three refinements — sanity OK.

**18:14.** Wrote `pde_ctrl.py` implementing:
- `build_kkt(...)`: all-at-once KKT system in the *u-eliminated* 2×2 symmetric saddle-point form
  `[[ τ M_all,  Lᵀ ]; [ L, -(τ/β) M_all ]]` where L is block-lower-bidiagonal with (M+τK) on the diagonal and −M on the subdiagonal (backward-Euler constraint operator, all time steps).
- `naive_mass_preconditioner`: diagonal-blocks-only preconditioner (control baseline).
- `pearson_schur_preconditioner`: the paper's block-diagonal preconditioner with `A_hat = τ·M_all` and Schur-complement approximation `S_hat = (1/√(βτ)) · L̂ · M_all⁻¹ · L̂ᵀ` where `L̂ = blkdiag(M + √(βτ)·K)` (per-timestep block-diagonal — this is the "matching" strategy from §3–4 of the paper). Both blocks solved with sparse LU factorization done once per problem (single M, single M+√(βτ)K).
- `run_experiment(...)` runs all three solvers on the same right-hand side and reports MINRES iterations to achieve *true* relative residual < 1e-6.

**18:15.** First smoke test: n=7, Nt=4, β=1e-4 → unprec 21 iters, naive 33, psw 12. Immediately noticed a bug: MINRES was terminating on scipy's internal Lanczos residual estimator rather than on the *true* residual. Fixed by tightening scipy's `rtol` to 1e-15 and adding a `ConvergedException`-based early stop from the callback triggered on true residual < 1e-6.

**18:16.** Re-ran smoke (n=15, Nt=8, β=1e-4): unprec 512 iters, naive 559, PSW **37**. Correct signature — PSW gives ~14× speedup.

**18:16.** Wrote `sweep.py`: full 4×4 grid over n ∈ {7, 15, 31, 63} and β ∈ {1e-2, 1e-4, 1e-6, 1e-8}, Nt = 8, T = 1. Ran (~3.5 min wall). Results saved to `sweep_results.json`, `sweep.log` (both copied to `report/evidence/`).

**18:20.** Wrote `eigenvalues.py`: dense eigenvalue analysis of both the KKT operator and the preconditioned operator P⁻¹A for the small case (n=7, Nt=4). Results saved to `evidence_eigenvalues.json`. Key finding:
- cond(A): 1.0e2 (β=1e-2) → 3.4e8 (β=1e-8), i.e. grows like 1/β.
- cond(P⁻¹A): 2.8 (β=1e-2) → 1247 (β=1e-8), i.e. grows only ~√(1/β), confirming the paper's eigenvalue-bound theory.

**18:22.** Wrote `plot.py`, produced `report/evidence/iterations.png` (log-log iterations vs 1/h and vs β) and `report/evidence/condition_number.png`.

**18:23.** Ran the LLM-judge (argo/argo:claude-opus-4.7) on the numerical evidence.

**18:24.** Wrote `report/REPORT.md`.
