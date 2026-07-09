# Attempt log

Chronological, honest.

## 2026-07-04 23:49 CDT — task received
Subagent spawned. Assigned Treeby & Cox 2010 k-Wave JBO paper. Read `WAVE_BRIEF_2026-07-01.md`. Target dir created.

## 23:50 — paper retrieval
- Attempted download of the paper PDF from UCL `medphys.ucl.ac.uk`: server timed out. Killed.
- Second attempt from SPIE Digital Library "download" endpoint: got only a 212 B HTML redirect. Discarded.
- Third attempt from `bug.medphys.ucl.ac.uk/papers/2010-Treeby-JBO.pdf`: **got 414 kB PDF, 12 pages**. Confirmed via `file`.
- Extracted text with `pdftotext`; grep-scanned for the k-space equations, PPW claim, and stability language. Confirmed:
  - Eq. (1): coupled first-order acoustic equations (`du/dt = -(1/rho0) grad p`, `drho/dt = -rho0 div u`, `p = c^2 rho`).
  - Sec 2.2: "only two nodes per wavelength are required, rather than the six to ten required in other methods."
  - Sec 2.2: "By comparing a simple PS time domain model … to an exact solution … it is possible to find replacement expressions … such that the numerical solutions are exact for arbitrarily large time-steps."
  - Staggered grid + first-order FD in time + FFT-based spatial derivative with κ correction.
- Cross-referenced Tabei/Mast/Waag 2002 (JASA 111, cited in Treeby-Cox ref 23) for exact form of κ = sinc(c₀ Δt |k|/2).

## 23:51 — implementation
Wrote `work/kspace_pstd.py`:
- `solve_1d`: staggered `p`(n) / `u`(n+1/2) leapfrog, FFT-based ∂/∂x with κ correction, half-grid `exp(±i k dx/2)` shifts.
- `solve_2d`: 2D analogue with two velocity components.
- `analytic_1d_traveling_gaussian`: exact d'Alembert.
- `analytic_2d_gaussian`: Hankel quadrature (converges very quickly for a Gaussian).
- `analytic_2d_disk`: Hankel quadrature (converges slowly — see below).

Smoke test: 1D Gaussian → **first version gave 1.9 % L2 error** (linear in CFL) — indicating first-order-in-time error in my staggered init.

## 23:53 — bug: staggered initialization
Recognized cause: for a staggered leapfrog with `u` at half-integer times and initial condition `u(t=0) = 0` (zero initial velocity), the very first update should use `Δt/2` (not `Δt`) to properly place `u` at `t = +Δt/2`. Without that shift, the whole simulation is offset by `Δt/2` in time — a 1st-order error that survives the κ correction (because κ corrects the temporal FD assumption, not the initial-condition placement).

Applied the fix (`step_dt = dt if n > 1 else 0.5*dt` in both `solve_1d` and `solve_2d`).

## 23:54 — C1 (temporal dispersion / stability sweep) run
`exp_C1_temporal_dispersion.py`: 1D Gaussian, T = 6 μs, CFL ∈ {0.1..5.0}.

- k-space: L2 rel err **≈ 2.5e-15 across all CFLs including 5.0** (machine precision).
- Plain PSTD: 8.4e-5 at CFL=0.1, quadratic growth, **blows up (>1e30) at CFL ≥ 0.7**.

C1 unambiguously replicated.

## 23:55 — C3 (PPW convergence) run
`exp_C3_ppw_convergence.py`: single-freq traveling wave, 20 wavelengths of propagation, CFL fixed at 0.3, PPW ∈ {2, 2.5, 3, 4, 5, 6, 8, 10, 16, 32}. Added a naive 2nd-order FD (`solve_1d_fd2`) for comparison.

- k-space: L2 rel err **~3e-15 at PPW = 2** and unchanged as PPW increases (spectral, at machine precision).
- Plain PSTD: chaotic at PPW ≤ 6 (temporal FD instability at the highest-frequency mode), converges only at PPW ≥ 8.
- FD2: >0.1 error even at PPW = 32.

C3 replicated. **k-space PSTD literally hits the Nyquist limit at PPW = 2, exactly as claimed.**

## 23:55 — C2 (2D disk) first attempt
`exp_C2_2d_disk.py`: 2D disk radius 3 mm, snapshot at 3 μs.
- Got sim vs "analytic" L2 rel err = **11%** — surprisingly poor.
- Investigated with `check_analytic.py`: the hard-edged disk in 2D generates a **logarithmic caustic** at `r = c t ± R`. My Hankel quadrature was not converged there — pushing kmax and Nk from (60/R, 8000) to (200/R, 40000) shifted the analytic minimum from -0.98 to -1.25 (still not converged). This is a fundamental limitation: the caustic is a distribution in 2D, not a smooth function.

## 23:57 — C2 revised
Switched to a **smooth Gaussian initial condition** (`exp_C2_2d_gaussian.py`): σ = 0.5 mm = 5 dx.

- k-space PSTD L2 rel err vs analytic Hankel = **1.07e-5**.
- Plain PSTD same setup = 9.4e-3 (**880× worse**).

C2 (accurate wave propagation vs analytic) cleanly replicated.

## 23:58 — 00:02 — C2b (disk self-convergence)
Added `exp_C2b_disk_selfconv.py`: same disk PSA but a Cauchy self-convergence sweep with N = {128, 256, 512, 768}. First tried N = 1024 too but the initial `record_snapshots=True` on that grid × ~600 time steps was too slow; killed and switched to N = 768 top grid.

Results:
- Leading-front peak x-location converges to **7.467 mm** (exact physical value = c₀·t + R = 4.5 + 3.0 = 7.5 mm) — sub-Δx accuracy.
- L2 rel err vs N = 768 reference: 0.20 (N=128) → 0.13 (N=256) → 0.085 (N=512), monotone decreasing. Residual error is the physical caustic.

C2b (self-convergence for the hard-edged canonical case) replicated.

## 00:02 — write-up
Wrote REPORT.md, brief.md, attempt_log.md, artifact_harvest.md.
