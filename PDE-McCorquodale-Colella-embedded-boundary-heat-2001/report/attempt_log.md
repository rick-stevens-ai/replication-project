# Attempt Log (chronological)

1. **Selection.** Read WAVE_BRIEF + PDE_TOPUP25 list. Ranks 52/61/63 already done. Ranks 68 (FVPM, mesh-free compressible) and 75 (McCorquodale-Colella embedded-boundary heat eqn) are the top undone. Rank 68 OA copy not locatable and method is very heavy (mesh-free particle). Rank 75 has an OA companion tech report and a crisp numerical PDE core + analytic test cases -> selected rank 75.

2. **OA fetch.** CherryRd cannot reach OSTI (HTTP 000) or eScholarship PDF (403). Routed through `uicgpu` with `source ~/env.sh` proxy: OSTI purl 878684 downloaded (702 KB, 6 pp). scp'd to `work/`. Extracted text with `pdftotext -layout`.

3. **Read method + test cases** from `osti.txt`: FV Laplacian Eq.(1), Dirichlet gradient stencils Eq.(8)/(10), L0-stable time scheme Eq.(16)/(17), Poisson test Eq.(21)-(22), heat test Eq.(23)-(24). Chose the 2D instantiation (tractable single-session; identical discretization).

4. **Geometry module** (`geometry.py`): circle domain, volume fractions (analytic 1D integration), face apertures, boundary arc. Verified `sum(kappa) h^2 -> pi R^2` to 1e-5..1e-6. (numpy 2.4 removed `trapz` -> switched to `trapezoid`.)

5. **First Poisson solve** — convergence STALLED (order dropped from 1.4 to negative at N=256). Diagnosed:
   - regular-cell 5-point Poisson is clean 2nd order (`diag_regular.py`) -> base assembly OK.
   - worst error always at smallest-kappa cut cell -> classic small-cell issue.

6. **Fix 1 (interpolation order).** Intrinsic EB gradient stencil measured only O(h) because bilinear interpolation errors don't cancel in the gradient. Upgraded `_interp_point` to **biquadratic (9-pt Lagrange)** with stencil-shift to stay inside the domain -> intrinsic gradient stencil became clean **O(h^2)** on exact fields. Solution still stalled.

7. **Fix 2 (the real bug): discrete divergence consistency.** Found `alphaB` (from angular arc sampling) violated the discrete Gauss identity `sum(+-alpha_face) + alphaB*nB = 0` by ~1e-2 -> operator inconsistent on cut cells. Enforced `alphaB*nB = -(net face-aperture vector)` from the identity (machine-precision divergence-free). Poisson solution error then converged monotonically, reaching order ~2.0 (L2 order 2.7, 2.1).

8. **Poisson convergence study** (`eb_poisson.py`), high & low stencils, N=64/128/256. L2 order ~2.1-2.7 both stencils (confirms C1 + the C2 "low stencil still 2nd-order solution" claim). Max-norm noisier due to sliver outliers; gradient error blows up at the finest grid on rare slivers (limitation).

9. **Heat solver** (`eb_heat.py`): built scaled operator `A = Minv Lrow`, time-dependent Dirichlet forcing extracted symbolically (`phiB=0` vs `phiB=1`). First L0 step gave large error -> bug in source handling. Verified operator `A phi + s ~ psi_t` to 8e-4 (correct) and that plain **backward-Euler** marches cleanly (L2 5e-5) -> isolated bug to the L0 two-stage source terms. Rederived Eq.(17) with `A_full x = A x + s(t)` substitution; physical f=0 so forcing term drops. Fixed.

10. **Heat convergence** (space+time, dt=0.5h): **low stencil clean 2nd order** (max 1.98/1.98/1.99, L2 2.11/2.07/2.04). High stencil ~20-100x smaller errors, noisier order (near floor). Spatial-only refinement (fixed dt) confirms 2nd-order spatial accuracy (1.98, 1.98). This reproduces the paper's headline C3.

11. **Plots** (`plot_conv.py`) -> `evidence/convergence.png`. JSON evidence saved.

12. **LLM judge** (free Argo): gpt-5.2 -> PARTIAL (flags gradient blow-up); sonnet-4.5 -> REPLICATED; gpt-5.1 -> REPLICATED; gpt-4o -> PARTIAL. Aggregate: PARTIAL, strongly reproducing C1 (L2) and C3, with C2 partially reproduced (intrinsic O(h^2)/O(h) verified but finest-grid sliver blow-up).
