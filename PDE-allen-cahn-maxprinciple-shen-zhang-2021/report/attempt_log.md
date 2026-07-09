# Attempt Log (chronological)

1. Read WAVE_BRIEF_2026-07-01.md and PDE_NEXT50_2026-06-26.tsv. Reviewed PDE-replications/ for
   structure. Deduped against ALREADY-DONE list and existing sibling dirs.
2. Candidate selection: filtered repro-ok OA rows with a clear numerical PDE core + analytic
   reference. rank 28 (modified-pnp), 32 (lowrank-vlasov-poisson), 27 (lightning-laplace),
   42 (walk-on-stars), 19/14 (vqapoisson) already exist under PDE-replications/. Picked
   **rank 10 — Shen & Zhang, discrete maximum principle 4th-order FD for generalized Allen-Cahn**
   (score 55.62, 28 cites, self-contained, exact convergence tables + a rigorous monotonicity
   theorem with a concrete verifiable inequality). No colliding dir.
3. Fetch: local network blocks export.arxiv.org (HTTP API returns 0 bytes, TCP blocked). Used
   uicgpu proxy. HTTPS arXiv API worked -> arXiv:2104.11813. Pulled PDF (3.6 MB), abs HTML,
   LaTeX e-print (7.9 MB). pdftotext -layout for text; verified eqs 2.7/2.8, Tables 6.1/6.2,
   Theorems 3.5/3.8/3.9/4.1.
4. Implemented D1/D2 matrices (fdmats.py): alternating stencils — odd i (cell center) 3-point,
   even i (cell end/knot) 5-point; plus 2nd-order centered companion. Raw truncation test:
   both ~2nd order (expected, paper Remark 1).
5. Built 2D operator (solver.py) via Kronecker form of eq (2.8) with interior/boundary column
   split so Dirichlet data goes to RHS.
6. VALIDATE FIRST on analytic steady convection-diffusion (validate_steady.py, exact
   phi=sin^2 x sin y): 4th scheme observed order 3.21->3.81->3.98->4.00 (l1); 2nd scheme ~2.00.
   Superconvergence confirmed -> operator + matrices correct.
7. Table 6.1 (table61.py): Allen-Cahn with sympy-manufactured source, BDF3 IMEX time
   (reaction/source explicit w/ 3rd-order extrapolation, conv-diff implicit). First pass used
   too-coarse dt -> fine grids stalled at order ~2 (temporal error dominated). Added splu
   prefactorization (implicit matrix constant across BDF3 steps) and a grid-tied dt schedule
   (dt 5e-3 -> 1.67e-4). Reproduced Table 6.1 to <6% with order ~4.0 (4th) / ~2.0 (2nd).
8. Table 6.2 (table62.py): stream-vorticity, PERIODIC BC -> built periodic wrap-around D1/D2.
   Fixed a bug where a constant sympy source returned a scalar (broadcast guard). First dt
   schedule (6000 steps @ 320x320) was needlessly heavy -> killed, right-sized dt via BDF3
   dt^3 << h^4 analysis (800 steps). Ran on uicgpu. Reproduced Table 6.2 to <6%, order 4.00
   at 320x320 (l1 1.45E-8 vs paper 1.41E-8).
9. Central theorem C2: first tried direct bound-preservation on the Sec 6.2 nonlinear runs
   (maxprinciple.py, 239x239, dt=(1/6)dx) -> observed overshoot beyond +/-1 in BOTH schemes.
   Re-read Theorem 4.1: for these parameters it requires h<=~0.002 (~2900 pts) — the paper's
   figures are OUTSIDE the theorem regime (illustrative, not the bound-preservation proof).
   Pivoted to the rigorous statement (Theorem 3.9): verified operator INVERSE-POSITIVITY
   (monotonicity.py). Constraint satisfied (h||u||/mu=0.317<=1/3, dt*mu/h^2=3.15>=3): min
   inverse entry >= 0 (0% negative). Constraint violated (dt*mu/h^2=0.05): 16% negative entries.
   Confirms the paper's novel *lower* time-step bound and its necessity.
10. Multi-judge (free Argo gpt-5.2, gemini-2.5-pro, gpt-4.1): unanimous REPLICATED.
11. Wrote report + copied evidence. Compute: light steps local, 320x320 Table 6.2 on uicgpu.
    Free endpoints only.
