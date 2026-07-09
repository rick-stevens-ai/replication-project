# Attempt Log — OSTI 3365789

All times CDT, 2026-07-02.

1. Read WAVE_BRIEF_2026-07-01.md + OSTI100_TOPUP50 priority list; enumerated already-done OSTI-* dirs (skipped 8).
2. Candidate triage: fetched 3 top undone candidates through `ssh uicgpu` OSTI purl proxy (CherryRd times out on osti.gov directly):
   - 3365789 (Parareal + operator learning, Allen-Cahn) — rank 25
   - 2526549 (fractional PINN) — rank 41
   - 3024991 (Vlasov-Poisson ROM) — rank 6
   `pdftotext` on all three.
3. Picked **3365789**: cleanest analytic/algorithmic validation targets (Allen-Cahn has exact steady/traveling-wave solutions; Parareal has hard algebraic invariants; MBP + energy dissipation are exact structural properties). Fully specified numerical scheme (Eqs. 6-14) + explicit test params (eps, domain, dt, IC Eq.16). No public code needed — reimplemented from equations.
4. Created target dir `OSTI-3365789-parareal-operator-learning-allen-cahn/` (verified non-colliding).
5. Wrote `work/replicate_ac.py`:
   - CN + 5-point-FD Laplacian fine solver, periodic BC, Picard iteration, FFT-exact Helmholtz solve for the linear system (exact for the FD stencil eigenvalues on a periodic grid).
   - V1 (first attempt): convergence vs continuous stationary kink `tanh(x/(sqrt2 eps))`. **FAILED** — errors grew under refinement. Root cause: the *continuous* steady state is not the *discrete* steady state; refining a sharp (eps=0.05) front reveals FD truncation of the interface, so this is not a clean order test. Logged; replaced with manufactured solution in part 2.
   - V2/V3 (MBP + energy) on merging-bubbles IC (Eq.16): PASSED.
   - C4/C5 Parareal with numerical CN coarse propagator, merging bubbles, T=1.0, s=10, dt_coarse=0.1, dtf=1e-3.
6. Ran part 1 on uicgpu (numpy 1.23.5), 55.4 s:
   - MBP holds (u in [-1,1] to 1e-13); energy strictly non-increasing (0.017419 -> 0.016830).
   - Parareal invariant holds to machine eps; converged to fine at rel-L2 = 4.3e-15; diff_inf 1.85e-3 -> 1.2e-14 over 10 iters.
7. Wrote `work/replicate_ac2.py` to (a) fix V1 with a **manufactured smooth solution** (isolates spatial/temporal order) and (b) test C5 on a **random IC**.
8. Ran part 2 on uicgpu, 67.4 s:
   - Spatial order: rates 1.999, 2.000, 2.000 -> clean **2nd-order in space** confirmed.
   - Temporal order: rate ~0 because spatial error is the floor at N=256 (temporal error already below it); does not contradict 2nd-order-in-time, just not isolated by this setup.
   - C5 random IC: numerical CN coarse converged to fine at rel-L2=6.5e-15, MBP not violated (amp stays 0.9). **Does not reproduce** the paper's claimed pathology.
9. LLM-judge (free Argo gpt-5.2, temp 0) scored claim-by-claim: C2/C3/C4 REPRODUCED, C1 PARTIAL, C5 CONTRADICTED -> OVERALL **PARTIAL**.
10. Pulled all evidence JSONs + paper PDF/txt to report dir; wrote REPORT.md / brief.md / artifact_harvest.md.

## Key honest finding
The paper's Sec 4.2.3 negative result — that a numerical CN coarse propagator makes AC-Parareal slow/blow up — was **not reproduced**. Our CN coarse propagator (unconditionally stable, FFT-exact linear solve, Picard converged to 1e-13 every step) drives Parareal to machine precision in ~10 iterations for both merging-bubbles and random ICs with no MBP violation. The paper itself attributes the failure to the correction step corrupting the nonlinear Picard iterations ("Picard solver reaches max iteration without convergence"); avoiding that implementation weakness removes the pathology. So C5 is implementation-dependent, not a fundamental property — a nuance the paper's framing understates.
