# PROGRESS — LUCID replication: Cordoni 2023, *Entropy* 25(9), 1322

DOI: 10.3390/e25091322
Source: `/data/stevens/lucid-corpus-extracted/LUCID-papers/b60a4945a319af54.md` (uicgpu)

Subagent session: `agent:main:subagent:399e71f4-...` (2026-05-29, CherryRd)

## Chronology

### 2026-05-29 — kickoff (Ollie subagent)

- 16:33 — Created project skeleton under `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-stochastic-poisson-dna-damage/`.
- 16:34 — Pulled the full paper markdown from uicgpu (506 lines). Confirmed it is a
  purely theoretical/short-numerical paper:
  - Builds on the *Generalized Stochastic Microdosimetric Model* (GSM²) master
    equation of Cordoni, Missiaggia et al. 2021 (Phys. Rev. E 103, 012412).
  - Performs a van-Kampen system-size expansion → recovers the deterministic
    MKM ODEs at order √K and a 2-D linear Fokker–Planck (Gaussian linear-noise)
    equation at order 1 for the fluctuations (ξ around X, v around Y).
  - **Headline claim:** variance of lethal lesions Y is `c_vv(t) = ȳ(t) - δ(t)`
    with `δ(t) ≥ 0`, i.e. *sub-Poissonian* (variance strictly less than mean).
- 16:35 — Confirmed **no published code** (Data Availability: "No new data have
  been created"). This is **friction tag F1** (missing/unreleased code). The
  derivation is fully explicit, so re-implementation from text is feasible.
- 16:35 — Numerical section uses *one* parameter set:
  `x₀=100, y₀=0, r=4, a=0.1, b̃_K = b/K = 0.01` (consistent with
  Missiaggia et al. 2022 GSM² Part II [20]). Three figures:
  - Fig 1 — sublethal+lethal histograms at t∈{0.5, 0.7, 0.9} a.u. (SSA) vs FPE Gaussian.
  - Fig 2 — time evolution of means (x̄, ȳ) and (co)variances (c_ξξ, c_vv, c_ξv).
  - Fig 3 — 10 sample paths for SSA vs OU-process linear-noise approximation.
- 16:36 — Plan:
  1. Gillespie SSA for the GSM² CTMC with reactions
     `X→∅ (r·X)`, `X→Y (a·X)`, `2X→Y (b̃·X·(X-1))`.
  2. Deterministic ODE integration of the macroscopic Eq. (11) for (x̄, ȳ).
  3. ODE integration of the moment equations (16) for (c_ξξ, c_ξv, c_vv).
  4. Time-dependent Ornstein–Uhlenbeck simulator from Remark 3 (matrices A(t), Q(t)).
  5. Compose Figures 1–3 + a Fano-factor / Poisson-deviation plot.
- 17:00 — Implementation, runs, and figure generation completed locally on CherryRd
  (lightweight; pure NumPy + matplotlib). All artefacts saved under
  `code/`, `results/`, `figures/`. See `REPORT.md` for the claim-by-claim table
  and verdict.

## Blockers / friction

- **F1** — no code released by author. Re-implemented from equations only.
- No data to fetch (theoretical paper). No data-availability friction.
- The paper does *not* publish raw numerical values for the moment trajectories
  or the histograms; visual+structural comparison is the only available check.
  This bounds the replication verdict to **REPLICATED-STRUCTURAL** (qualitative
  agreement on all reported behaviours) rather than a numeric-tolerance match.

