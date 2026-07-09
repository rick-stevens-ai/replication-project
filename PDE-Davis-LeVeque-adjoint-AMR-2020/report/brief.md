# Brief — PDE-Davis-LeVeque-adjoint-AMR-2020

**What.** Independent replication of Davis & LeVeque (2020) "Analysis and Performance Evaluation of Adjoint-Guided AMR for Linear Hyperbolic PDEs Using Clawpack" (ACM TOMS, DOI 10.1145/3392775). We built Clawpack v5.9.2 from source on uicgpu (8×A100 host, gfortran+OpenMP), ran the paper's shipped `acoustics_1d_adjoint` and `acoustics_2d_adjoint` AMRClaw examples, compared adjoint-magnitude flagging against Richardson error-estimation flagging at multiple tolerances, and computed the functional-of-interest error against a fine-grid reference.

**Why.** Direct test of the central quantitative claim: adjoint-guided AMR concentrates refinement only on waves that reach the user-specified target region, thereby reducing refined-cell counts and CPU time relative to standard AMR while preserving accuracy in the functional of interest.

**Outcome.** REPLICATED (high confidence). In 1D, adjoint tol=0.01 achieves rel-err 1e-3 in J using 129,760 level-3 cell updates vs 209,184 for Richardson tol=1e-4 (~62%). In 2D, adjoint gives **5.65× fewer** total cell updates, **7.82× fewer** L3 cell updates, **2.97× faster** wall clock, and **1.63× less** CPU time than Richardson at matched final-time mass (<0.4% relative difference). LLM-judge (Argo claude-opus-4.7) verdict = REPLICATED, all four extracted claims reproduced.
