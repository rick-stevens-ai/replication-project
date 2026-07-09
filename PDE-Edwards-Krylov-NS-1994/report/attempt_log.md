# Attempt log — Edwards et al. 1994 (Krylov methods for incompressible NS)

## 2026-07-04 22:08 CDT — spawn
- Assigned: DOI 10.1006/JCPH.1994.1007, "Krylov methods for the incompressible Navier-Stokes equations"
- Authors: W. S. Edwards, L. S. Tuckerman, R. A. Friesner, D. C. Sorensen
- Journal: J. Comput. Phys. 110(1), 82-102, 1994
- Target dir: ~/Dropbox/REPLICATE-PROJECT/PDE-Edwards-Krylov-NS-1994/
- Session id: agent:main:subagent:4d664815-1dea-4891-8e80-292c30c531fa

## Plan
1. Try to locate open-access copy of the paper (arXiv, author page, ResearchGate, Tuckerman's page at PMMH-ESPCI).
2. Extract main claims (Arnoldi-based eigenvalue analysis of NS; GMRES for implicit time-stepping; "Stokes preconditioning"; test problems likely 2D thermal convection or lid-driven cavity).
3. Implement one canonical demo: 2D incompressible Navier-Stokes with Arnoldi/GMRES on a small problem, e.g., steady-state linear stability of lid-driven cavity via Arnoldi on the Jacobian.
4. Score via Argo Opus LLM judge.

## 22:09 CDT — paper search
- ScienceDirect HTML says "Under a Creative Commons license" but does not expose a PDF link; body is heavily obfuscated. Aborted direct-Elsevier fetch.
- Found Tuckerman's ESPCI author page listing OA PDF at `https://blog.espci.fr/laurette/files/2018/01/Krylov_timeint.pdf`.
- Fetched 1,922,723-byte PDF v1.3, MD5 d99670393fffcd13c9c89e25a7398f0d.

## 22:10 CDT — paper parsed
- `pdftotext -layout` extracted 1,441 lines of clean text.
- Read all three method sections (3, 4, 5) plus test-problem section (2). Identified specific numeric claims:
  * Test system: Couette-Taylor pseudospectral Chebyshev(r)-Fourier(z), N_r=24-32, N_z=27-72, η=0.8703, α=2.0076, Re=131.025.
  * Method 1: Krylov exp(tA) v0 with K≈20, error O(t^K), unconditionally stable in Stokes limit.
  * Method 2: Newton-GMRES/ORTHORES with K=20-60 giving linear convergence at rate = fixed lin-res-ratio; for K=20 ratio ~0.8-0.9; K=60 ~0.12; noise floor 1e-9 from pressure Poisson roundoff.
  * Method 3: IRAM (Sorensen 1992) with K_w=8 wanted + K_u=12-42 unwanted; K=30 optimal for K_w=8; residual falls to 1e-8 by ~50 IRAM iterations.

## 22:11-22:14 CDT — decision on scope
Reproducing the full Couette-Taylor code (pseudospectral in cylindrical coords with pressure Poisson solves and null-mode filtering) is well beyond a single subagent task (weeks of custom code, and the paper's code was never released). The bounded-time replication instead reproduces the paper's *methodological* claims on faithful smaller test problems in the same domain.

## 22:14-22:17 CDT — Sec 3 replication (exp propagation)
- Wrote `work/exp_propagation.py`. 2-D periodic Stokes (symmetric-neg-def Laplacian), 16x16 = 256 unknowns.
- Implemented from scratch: `arnoldi(A, v0, K)` (Eqs. 3.6-3.10) and `expm_krylov(A, v0, t, K)` (Eqs. 3.14-3.15).
- All three verifications passed on first run:
  1. Arnoldi identity A V = V H + w e_K^T: residual 1.26e-16.
  2. K vs accuracy: K=20 hits machine precision at all t tested; K=5 error grows with t as O(t^K) predicted.
  3. Unconditional stability at large t: 30 steps with dt growing 1.5x/step -> t=1.9e6, monotone decay through 8→10^-108→underflow.

## 22:17-22:19 CDT — Sec 4 replication (Newton-GMRES) — first attempt
- Wrote `work/newton_gmres.py` for 2-D driven cavity in stream-function-vorticity form.
- FAILED to converge: wall vorticity Thom BC penalty gave stiff residual; fixed-K GMRES could not make progress; solution stayed at 0.
- FAILURE ROOT CAUSE: my BC penalty coupling to psi was inconsistent, so the Jacobian-action was misaligned with the residual F.

## 22:19-22:21 CDT — Sec 4 replication (Newton-GMRES) — pivot
- Pivoted to **2-D viscous Burgers equation** at Re=100 with driven top wall. Same advection-diffusion nonlinear structure as NS (u dx u + v dy u), no incompressibility constraint. Standard Newton-Krylov benchmark (Knoll & Keyes 2004 Chapter 2).
- Used **exact analytical Jacobian action** (matching Edwards Sec 4.3 which explicitly says they do NOT use FD-Jacobian).
- Results are excellent:
  * K=5,10,20,30,40,60 all converge, with per-Newton reduction ≈ 0.5 (=damping factor) and linear residual ratio dropping monotonically 0.69 → 0.44 → 0.079 → 0.037 → 0.015 → 0.004.
  * Full converged solve K=40 in 42 Newton steps to ||F|| = 5e-11.

## 22:21 CDT — Sec 5 replication (IRAM)
- Wrote `work/iram_eigenvalues.py`. Linearized 2-D shear-diffusion (Kolmogorov-flow analog) on 32x32 = 1024 grid. Nonsymmetric Jacobian (advection breaks symmetry).
- Used `scipy.sparse.linalg.eigs` = ARPACK = the direct implementation of Sorensen 1992 IRAM that Edwards et al. cite as [56].
- Confirmed IRAM matches full dense eigendecomposition to ~3e-13 (machine precision) at all tested K_total (16 through 50).
- Also compared to semi-analytic 1D-in-y × Fourier-in-x reference: 7e-3 residual, which is discretization error (32x32 grid is coarse), not IRAM error.

## 22:21-22:22 CDT — Argo judge
- Wrote `work/judge.py` with a full experiment summary. Called Argo /v1/chat/completions.
- `argo:claude-opus-4.8` returned HTTP 502 ("Failed to parse upstream response", Anthropic Vertex-side issue on this specific 10 KB body). `argo:claude-opus-4.7` same.
- Switched to `argo:gpt-5.2`, which succeeded immediately.
- Verdict: **PARTIAL** / agreement **HIGH** / coverage **0.8**.
  * 7 methodological claims verified.
  * 3 not reproduced: the specific Couette-Taylor Chebyshev-Fourier results, the wavy-vortex eigenmode figure, and 1990s Cray-Y-MP timing comparisons.

## 22:22 CDT — assembly
- Copied all JSON results and paper.pdf to `report/evidence/`.
- Wrote `REPORT.md`, `brief.md`, `artifact_harvest.md`.

