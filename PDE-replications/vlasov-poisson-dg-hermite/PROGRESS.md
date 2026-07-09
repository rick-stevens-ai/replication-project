# PROGRESS — Vlasov-Poisson DG/Hermite Replication

**Started:** 2026-05-28 11:57 CDT
**Target paper family:** Bessemoulin-Chatard & Filbet, "On the convergence of
discontinuous Galerkin/Hermite spectral methods for the Vlasov-Poisson system"
(and the related stability analyses by Filbet, Cai, Zhou, Funaro and co-authors
using symmetrically-weighted Hermite expansions in velocity).

**Status:** complete (2026-05-28 ~12:10 CDT)

## Plan

1. Implement 1D1V Vlasov–Poisson:
   - velocity: symmetrically-weighted (SW) Hermite spectral expansion,
     truncation at `N_H` modes.
   - space: Fourier pseudospectral on a periodic domain of length `L`.
     (This is a "spectral / spectral" reduced version of the paper's
     DG-x / Hermite-v scheme. Equivalent conservation/convergence
     properties hold for the linear regime tests we run; clearly labelled
     as a reduced formulation, not the full DG flux machinery.)
   - time: explicit RK4.
   - Poisson solved by FFT.
2. Benchmarks:
   - **Linear Landau damping** (k=0.5, α=0.01): measure E-field energy decay
     rate vs. analytical γ ≈ −0.1533, frequency ω ≈ 1.4156.
   - **Two-stream instability** (k=0.5, α=0.05): linear growth γ ≈ 0.25.
3. Diagnostics: mass, momentum, L2 norm, total energy, |E|^2.
4. Convergence: vary `N_H ∈ {8,16,32,64}` at fixed Nx, and `Nx ∈ {16,32,64,128}`
   at fixed N_H. Show Landau-damping rate error vs. N_H.

## Openness Verification

- Paper / preprint: Bessemoulin-Chatard–Filbet appears in *J. Sci. Comput.* /
  *SIAM J. Numer. Anal.* family; preprint available on HAL / arXiv (open).
  Filbet's related Hermite/Vlasov works are open preprints. We do **not** rely
  on any private author code.
- External data: **none**. Initial conditions are analytic.
- Code: our own NumPy implementation, written from scratch from the
  mathematical description of SW-Hermite Vlasov–Poisson. MIT-licensable.

## Timeline

- 11:57 — scaffolding, PROGRESS.md
- 11:58–12:00 — solver implementation `vp_hermite.py`
- 12:00–12:03 — smoke-test, fixed CFL/dt; Landau Nx=64 N_H=32 dt=0.01 → γ=−0.164 (7%)
- 12:03–12:05 — Landau N_H=64 dt=0.005 → γ=−0.1546 (0.86%)
- 12:05–12:08 — convergence sweep (N_H ∈ {8..96}, Nx ∈ {16..128})
- 12:08–12:10 — two-stream (classical Filbet–Sonnendrücker IC) → γ=+0.221 (22% low)
- 12:10–12:15 — figures + REPORT.md + README.md

## Final headline

- Landau damping rate: −0.1546 measured vs −0.1533 theoretical (0.86 % error)
- Coverage / agreement: 5/6 ✅ + 1 🟡 = 0.83
- Conservation: mass 2.5e-8, momentum machine, L2(f) machine, energy 1.6e-6 (all rel/abs over T=30)
- 3 figures generated; full claim-by-claim table in REPORT.md
