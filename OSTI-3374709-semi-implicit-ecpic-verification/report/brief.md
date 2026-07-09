# Brief

**Paper:** Hedlof, Barnes, Groenewald, et al., *"Verification of an energy-conserving
semi-implicit electrostatic particle-in-cell scheme for modeling high-density plasma
at scale"*, Phys. Plasmas **33**, 053902 (2026). DOI 10.1063/5.0315721. OSTI 3374709 (LBNL).

**What/why:** The paper introduces a semi-implicit ES-PIC (SIPIC) scheme whose central
verification claim is that a plasma-density-dependent *effective dielectric*
`eps_eff = eps0·(1 + C_SI·ωpe²·Δt²/4)` down-shifts the electron plasma oscillation to
`ωpe_SI = ωpe/√(1 + C_SI·ωpe²·Δt²/4)` (their Eqs. 12/16), letting the scheme stay stable
and second-order accurate even when `ωpe·Δt ≫ 1`. I independently re-implemented a
minimal 1D electrostatic leapfrog/CIC/spectral-Poisson PIC with exactly this modified
field operator, seeded a cold Langmuir mode, and measured its oscillation frequency by
FFT across `ωpe·Δt ∈ {1,2,4,8,16}` (C_SI=4). The measured frequencies track the analytic
down-shift (Eq. 16) to ~1–4% for `ωpe·Δt ≤ 8` and ~10% at 16 — and are decisively *not*
the classical `ωpe`, reproducing the paper's core verification result.
