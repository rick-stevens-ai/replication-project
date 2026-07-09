# Brief — NodePy (Ketcheson et al. 2020, JOSS)

**What:** Independent re-run of the NodePy JOSS software paper (DOI 10.21105/joss.02515). NodePy is a Python package that computes theoretical properties of numerical ODE solvers (Runge–Kutta, linear multistep, two-step RK, IMEX): formal order via Butcher-tree conditions, absolute stability regions, SSP coefficients (radius of absolute monotonicity), rooted-tree enumeration, and empirical convergence via IVP integration.

**Why:** X-100 replication project (PDE set, rank 59 in PDE_NEXT50). Verify the published capability claims by installing the package from PyPI, exercising each advertised feature on canonical test cases, and comparing to theoretical/published values.

**Result:** REPLICATED. All 9 capability claims (C1–C9) tested and confirmed. nodepy 1.0.1 installed cleanly; formal orders match theory for 11 RK methods and 3 Adams–Bashforth LMMs; SSP coefficients recover 1, 1, 6 for SSP22/33/104 and 0 for RK44/DP5; RK44 stability polynomial coefficients match [1/24, 1/6, 1/2, 1, 1] exactly; rooted-tree counts match OEIS A000081 through order 7; empirical convergence slopes on y′ = y·cos(t) match or exceed formal order for 6 methods.
