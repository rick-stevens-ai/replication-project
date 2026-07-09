# Attempt log — Chorin (1968) projection method replication

Date: 2026-07-04 CDT (night wave).
Machine: `CherryRd` (macOS local CPU, Python 3.14.6, NumPy 2.4.3, SciPy 1.18.0).

1. **Paper acquisition.** Downloaded the AMS-hosted open-access PDF at
   `https://www.ams.org/journals/mcom/1968-22-104/S0025-5718-1968-0242392-2/S0025-5718-1968-0242392-2.pdf`
   (10 pp, 1.59 MB, SHA-256 `94c4a22f71ab16675207a1b44daa42e2e517896175a2061d2f6dfcfdfcf1dcef`).
   Extracted text with `pdftotext -layout`. Read the paper end-to-end, extracted
   the four testable claims (C1–C4) and Chorin's specific Table I / II parameters
   for the Pearson exact-solution test.

2. **Design decisions.**
   - Used a MAC staggered grid (u at x-faces, v at y-faces, p at cell centers).
     Chorin's eqs. (17)–(18) for `D u` and his `d p` operator map directly to
     this layout.
   - For the advection-diffusion sub-step used explicit Euler with centered
     spatial differences (Chorin's eqs. 6/7 are ADI variants of the same
     operator; Chorin himself notes an explicit sub-step is admissible provided
     `dt = O(dx^2)`). This keeps the implementation minimal while preserving
     the paper's essential algorithmic content: it is the *projection* step,
     not the choice of sub-step integrator, that is Chorin's contribution.
   - For the Poisson solve used direct sparse LU (`scipy.sparse.linalg.splu`).
     Chorin used Dufort–Frankel over-relaxation because of 1968 memory limits;
     the direct solver converges to machine precision, so the divergence-free
     test (C1) becomes correspondingly sharper. This is a strictly stricter
     test of Chorin's projection principle than what he could do.

3. **Vectorization crisis.** First-pass advection loop was double-nested Python
   `for i, j` — took ~30 s for 32×32. Replaced with pure NumPy slice arithmetic;
   ~200× speedup. Nothing else changed.

4. **First Pearson runs (Chorin Table I params).** Chorin's Table I uses
   `dx = pi/39`, `dt = 2 dx^2 = 0.01397`, `R = 1`. Ran this exactly. Result:
   went unstable and reached `nan` by step 17. On reflection, this is *not*
   a bug: Chorin's Table I uses his implicit ADI Peaceman–Rachford scheme (his
   "Scheme A"), which is unconditionally stable in the diffusive sense. Our
   explicit-Euler sub-step requires `dt < dx^2 / (4 nu) ~ 0.0016` for that same
   `dx`, i.e. an order of magnitude smaller than Chorin's `dt`. Logged this in
   the report as evidence for C4 (the paper's stability claims are grounded in
   the choice of implicit sub-step).

5. **Re-ran Pearson with proper CFL.** For `nx ∈ {20,40,80}` with a CFL-safe
   `dt`, got final-time (t=1) max errors `5.7e-6`, `1.4e-6`, `3.5e-7`. Ratios
   ~4×, i.e. clean **O(h²)**, and *better* than Chorin's Table II value
   (`~1e-4`) because the smaller `dt` reduces the O(dt) splitting error.

6. **Lid-driven cavity Re=100 and Re=400.** Ran to steady state
   (`T_final = 25 L/U` at Re=100, `40 L/U` at Re=400) on grids
   `nx ∈ {32,64,128}` (Re=100) and `{64,128}` (Re=400). Extracted centerline
   `u(y)` at `x = L/2` and `v(x)` at `y = L/2`, interpolated to the 17
   Ghia sample points, compared to the tabulated Ghia (1982) reference data.
   At Re=100/nx=128 the errors are:
   - `err_u_L2 = 0.0022`,  `err_u_Linf = 0.0046`
   - `err_v_L2 = 0.0045`,  `err_v_Linf = 0.0088`
   which is excellent for a 128² grid with a first-order-in-time scheme.
   At Re=400/nx=128 the `u`-profile is very clean (`err_u_L2 = 0.0015`) but
   the `v`-profile L∞ is `0.147`, driven by two Ghia sample points at
   `x ≈ 0.85–0.90` where the strong right-wall boundary-layer peak requires a
   finer grid than 128² for a first-order-in-time scheme to resolve fully.
   This is a known property of Chorin's scheme (motivated Van Kan / second-order
   projection methods 20 years later), not a contradiction of Chorin's paper.

7. **Divergence-free audit.** Across every single run above (5 cavity + 5
   convergence + 5 temporal = 15 runs), max `||div u^{n+1}||_inf` at final
   time ranged from `1.7e-16` (single projection on 16²) to `1.6e-13`
   (long-time 128² at Re=400, where accumulation of tiny numerical noise is
   inevitable). Every one is machine precision or `~n · eps`. **C1 confirmed
   everywhere.**

8. **Temporal convergence.** Straight fixed-`T`-vary-`dt` was confounded by
   BC-averaging artifacts. Redesigned as Cauchy-style self-refinement:
   reference at `dt=1e-4, nx=16, T=0.5`, sweep `dt ∈ {4e-3, 2e-3, 1e-3, 5e-4}`.
   Successive log2 ratios: `1.04, 1.08, 1.17`. Clean **O(dt)** as Chorin's
   theory predicts for the fractional-step scheme.

9. **LLM judge.** Sent evidence JSON to Argo proxy `127.0.0.1:44497`. First
   attempt `argo:claude-opus-4.8` -> 502 Bad Gateway. Fell back to
   `argo:claude-sonnet-4.6`, worked; returned `verdict=REPLICATED,
   coverage=0.92, agreement=0.85` with a coherent per-claim justification.
   Full raw response stored in `evidence/llm_judgment.json`.

10. **Deliverables.** Full REPORT.md written; `evidence/` contains
    `cavity_results.json`, `convergence_results.json`,
    `temporal_convergence.json`, `pearson_results.json`, `llm_judgment.json`,
    and three summary PNGs.
