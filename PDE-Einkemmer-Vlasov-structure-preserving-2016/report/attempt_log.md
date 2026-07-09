# Attempt Log — PDE-Einkemmer-Vlasov-structure-preserving-2016

## Paper
- Title: "Structure preserving numerical methods for the Vlasov equation"
- Author: L. Einkemmer (SOLO)
- Year: 2016
- Type: Oberwolfach Report / workshop proceedings (DOI 10.4171/OWR/2016/18)
- Actual location in volume: pp. 899–902 (4-page talk in workshop volume "Geometric Numerical Integration" edited by Faou, Hairer, Hochbruck, Lubich)
- **Assignment note (important)**: DOI 10.4171/OWR/2016/18 points to the *whole* workshop volume, not a standalone Einkemmer paper. Einkemmer's contribution is the specific 4-page talk inside. The task treats the talk as the replication target.

## Timeline

**2026-07-05T07:10:05Z** — Setup: created target directory `PDE-Einkemmer-Vlasov-structure-preserving-2016/{report/evidence,work}`. Read the WAVE brief. Verified sibling dir `PDE-Einkemmer-Lubich-lowrank-VlasovPoisson-2018` exists and is DIFFERENT paper.

**2026-07-05T07:10:15Z** — Fetched OWR volume PDF (`ems.press/content/serial-article-files/46621`, 3.6 MB, 80 pages). Extracted text; located Einkemmer's talk at lines 1392–1510. Verified authorship, title, references list.

**2026-07-05T07:11:30Z** — Located author's public code. Tried `github.com/lukaseinkemmer` (404). Discovered correct GitHub user is `leinkemmer`, personal site `einkemmer.net`, primary Vlasov code repo is `bitbucket.org/leinkemmer/sldg` (SLDG framework). Cloned successfully to uicgpu.

**2026-07-05T07:14:00Z** — Assessed SLDG production code: 4D/6D distributed-memory Vlasov-Poisson framework with MPI + CUDA. Requires Boost, GSL, PnetCDF submodules (~1 GB) plus cluster module setup. Building end-to-end estimated 30–90 min plus significant risk on custom uicgpu module system. Decided to build a from-scratch reference Python solver instead to actually test the claims independently.

**2026-07-05T07:15:00Z** — Wrote `vp1d_solvers.py`:
- Strang-splitting SL with cubic-spline interpolation (periodic in x, natural spline zero-BC in v)
- Strang-splitting SL with first-order upwind interpolation (mass-conservative, positivity-preserving, dissipative)
- Modal Legendre sLdG (orders 1–5) with L2 projection, tensor-product Gauss-Legendre quadrature, periodic/zero BC
- FFT Poisson solver
- Diagnostics: mass, L1, L2, momentum, kinetic energy, electric energy, total energy, entropy

**2026-07-05T07:17:00Z** — Local sanity check on 16×16, T=2 works. Cubic spline mass conserved to 3e-15 (machine precision), entropy already trending negative (potential match to Einkemmer C1 for spline). sLdG order-3 works pointwise but has ~1e-3 mass leak from Poisson piecewise-constant E — flagged for fix.

**2026-07-05T07:19:00Z** — Full run on uicgpu Nx=Nv=64, T=40, dt=0.05:
- Spline works: mass 1e-15, entropy actually INCREASED (+2.3 total, opposite of Einkemmer's specific claim)
- sLdG (orders 2, 3, 4) all BLOW UP catastrophically: mass grows 10x-100x, L2 to 1e7, entropy explodes negative
- Root cause: my pointwise sLdG shift + zero-BC v-advection + piecewise-constant E interpolation loses positivity in nonlinear regime; without a Zhang-Shu / Qiu-Shu positivity limiter, negative values grow explosively.

**2026-07-05T07:23:00Z** — Diagnosed pure-advection sLdG separately (`test_advection.py`): mass conservation is machine-precision for Nc=32, small L1 spreading only from Gaussian bump under-resolution. So the sLdG **primitive itself is correct**; the instability comes from the coupled Vlasov-Poisson nonlinear regime where positivity is lost.

**2026-07-05T07:24:00Z** — Attempted a fix: evaluate E on the fine (per-quadrature-node) x-grid via Fourier synthesis instead of piecewise constant per cell. Improved short-time behavior but still blows up for T > 5 in the nonlinear regime. My scratch sLdG lacks a positivity limiter — this would take substantial engineering to add correctly.

**2026-07-05T07:27:00Z** — Pivoted strategy: instead of trying to fix a production-grade sLdG in-place, use a **first-order upwind SL** as the "dissipative reference" and compare against high-order spline. This is the classic pairing Einkemmer implicitly contrasts (spline vs. lower-order interpolants). Added `strang_upwind_step` with mass-conservative fractional-cell blending.

**2026-07-05T07:28:00Z** — Rebuilt experiment. Both schemes now stable. Verified locally on small grid: upwind mass to 1e-8, L2 dissipates faster than spline (as expected for a dissipative scheme), entropy INCREASES faster than spline (also consistent with dissipation).

**2026-07-05T07:29:00Z** — Full runs on uicgpu Nx=Nv=128, T=30, dt=0.05 for both Landau damping (α=0.01) and two-stream instability (α=0.05), both methods:
- landau/spline: mass 1e-6, L2 -13%, entropy +13%, energy ~6x (nonlinear)
- landau/upwind: mass 2e-4, L2 -35%, entropy +33%, energy ~5x
- two_stream/spline: mass 3e-6, L2 -16%, entropy +9%, energy ~0.9x
- two_stream/upwind: mass 9e-5, L2 -32%, entropy +20%, energy ~0.8x

**2026-07-05T07:34:00Z** — Additional test at α=0.001 (very linear Landau) with T=15: even here, spline entropy is essentially flat (17.83090 → 17.83090 to 5 digits), then grows slightly at t~12.5 when filamentation kicks in. **Did not observe the entropy DECREASE Einkemmer describes for spline** in any regime tested. This is either:
  (a) an artefact of my slightly different discretization (natural v-BC vs periodic v-BC, cell-center quadrature vs Simpson, etc.), or
  (b) a regime issue — his Fig 1 is at T=100, way past filamentation onset, where different mechanisms dominate.

**2026-07-05T07:35:00Z** — Generated diagnostic plots (`invariants_vs_time.png`, `landau_damping.png`).

**2026-07-05T07:36:00Z** — LLM-judge via Argo Sonnet 4.6 (FREE endpoint, not GPT-5 which returned 400): verdict = PARTIAL, coverage 0.5, agreement 0.5, one-line = "Spline SL mass/L1 conservation confirmed; entropy decrease claim contradicted; sLdG claims untestable due to instability of scratch implementation."

**2026-07-05T07:38:00Z** — Wrote up report/brief.md, report/artifact_harvest.md, report/attempt_log.md, report/REPORT.md.

## Lessons / failure notes
- Production-grade positivity-preserving sLdG requires a Zhang-Shu (2010) type limiter or a conservative flux-form implementation. My pointwise Legendre sLdG loses positivity and explodes in nonlinear Vlasov regimes. If we wanted to test the sLdG entropy claim rigorously, we'd need to actually build Einkemmer's SLDG code (Boost+GSL+PnetCDF + MPI, ~90 min if the modules cooperate).
- The specific "spline decreases entropy" claim in the report may hinge on details of the exact discretization (BCs, quadrature, exact vs approx v-shift) not fully specified in the 4-page abstract. My independent implementation instead shows entropy nearly flat in linear regime and growing in nonlinear regime for spline SL.
- Argo `argo:gpt-5.5` and `argo:gpt-5` returned HTTP 400 for tool-less chat; `argo:claude-sonnet-4.6` worked and served as the judge. Documenting for future runs.
