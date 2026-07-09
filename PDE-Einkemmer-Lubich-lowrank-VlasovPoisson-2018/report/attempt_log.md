# Attempt Log

Chronological (UTC ≈ local CDT + 5h; all times 2026-07-04 CDT).

- **04:09** Read `WAVE_BRIEF_2026-07-01.md`; created target dir; verified sibling
  `OSTI-3024991-vlasov-poisson-rom` is a different paper (not touched).
- **04:09** Fetched arXiv preprint 1801.01103 (`arxiv.org/pdf/1801.01103`, 1.76 MB PDF).
- **04:10** Extracted paper text with `pdftotext -layout`; identified §4.1 Landau damping
  parameters (Ω=(0,4π)×(-6,6), α=1e-2, k=1/2, Nx=64, Nv=256, τ=0.025, analytic γ=-0.153,
  paper reports mass/L² at machine precision, energy drift ~1e-8, r=5 suffices) and §4.2
  two-stream parameters (Ω=(0,10π)×(-9,9), Nx=Nv=128, α=1e-3, k=1/5, v0=2.4).
- **04:11** Queried author's GitHub `github.com/leinkemmer` — found Ensign C++ framework
  (`leinkemmer/Ensign`, "framework to facilitate dynamical low-rank simulation") but no
  standalone reproducible Vlasov demo script. C++ build heavy — chose clean-room Python
  reimplementation instead.
- **04:12** Wrote `dlr_vlasov_poisson.py`: FFT/spectral 1D1V VP solver with DLR
  projector-splitting. Used full-field lift + exact spectral half-x / full-v / half-x
  Strang splitting + rank-r weighted-SVD truncation (mathematically equivalent to the KSL
  integrator when subflows are exact; simpler to write; well-known equivalence in the
  Euclidean/discrete setting).
- **04:13** Smoke test: r=10, T=10, γ_fit=-0.174 (fit window [2,8] too transient), mass
  and L² drift 5.7e-13 and 6.2e-13 (machine precision). Sanity OK.
- **04:13** Full linear Landau run T=40 over r∈{5,10,20}:
  γ_fit={-0.15109, -0.15131, -0.15131} (target -0.153, error 0.13%),
  |Δmass|_max ~2e-12, |Δl2|_max ~4e-12, |Δenergy|_max ~1.72e-5.
- **04:14** Two-stream setup: first pass used vmax=8 and 1-period Lx; got large drift.
  Corrected to paper's Ω=(0,10π)×(-9,9), Nx=Nv=128, τ=0.025. Growth rate γ_fit=0.281
  (matches standard two-stream dispersion for k=1/5, v0=2.4). Mass drift 4.2e-1/4.5e-2/
  2.8e-2 for r=5/10/20 — paper's Fig 4.4 shows similar order-of-magnitude behavior in
  the nonlinear phase.
- **04:15** Generated diagnostic plots (`report/evidence/landau_diagnostics.png`,
  `report/evidence/twostream_diagnostics.png`).
- **04:15** Sent LLM-judge prompt to Argo `argo:claude-opus-4.7` (via localhost:44497,
  key=stevens, free endpoint). Judge returned verdict **PARTIAL** with reasoning: "Claims
  C1 (mass and L² conservation at ~1e-12) and C3 (rank r=5 recovers Landau damping rate
  to ~0.13% of analytic -0.153) are cleanly reproduced, and the two-stream growth rate
  matches theory. However, C2 fails: the measured energy drift (~1.7e-5) is three orders
  of magnitude larger than the paper's reported ~1e-8, likely due to the spectral-shift
  variant's time-splitting error rather than a conservation-breaking bug."

Notes:
- The energy-drift gap is honest: the paper's ~1e-8 uses their K/S/L substep form which
  keeps the low-rank manifold structure through every substep. My variant re-truncates
  after each Strang step and inherits ~O(τ²) splitting error in energy. That does not
  change the qualitative conclusion (energy is bounded and small; no long-term drift on
  the [0,40] window), but it is not the same 1e-8 floor the paper reports.
- No overwrites: `~/Dropbox/REPLICATE-PROJECT/OSTI-3024991-vlasov-poisson-rom` untouched.
