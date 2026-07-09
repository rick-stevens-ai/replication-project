# Independent Replication Report

**Paper:** Martin J. Gander & Andrew M. Stuart, *"Space-Time Continuous Analysis of Waveform Relaxation for the Heat Equation."* SIAM J. Sci. Comput. **19**(6):2014–2031, November 1998. DOI [10.1137/S1064827596305337](https://doi.org/10.1137/S1064827596305337).
**Set:** PDE-100 (top-up list rank 77; 208 citations).
**OA source used:** author copy at `stuart.caltech.edu/publications/pdf/stuart39.pdf` (MD5 `a5aebcbf1b51887995c676f3bbf44439`). Publisher (SIAM) version paywalled.
**Replication date:** 2026-07-02. **Verdict: REPLICATED.**

---

## 1. Paper summary

Waveform relaxation (WR) is a parallel method for time-dependent problems in which the
space-time domain is split and each piece is solved over the *whole* time interval, iterating
until the interface data converges. Classically, WR for a PDE is obtained by discretizing in
space and then *algebraically* splitting the discrete operator; for the heat equation this gives
linear (unbounded-time) and superlinear (bounded-time) convergence, **but the rate degrades as
the mesh is refined**.

Gander & Stuart instead split in the **physical domain** using **overlapping domain
decomposition** (an overlapping Schwarz iteration applied in space-time). Their contributions:

- A **space-time continuous** convergence theory. For two overlapping subdomains
  Ω₁=[0,βL], Ω₂=[αL,L] (0<α<β<1) of the 1D heat equation, the interface error contracts
  **linearly on the infinite time interval** with per-double-iteration factor
  **ρ = α(1−β) / (β(1−α))** (Lemma 2.3, Thm 2.4; semidiscrete Thm 2.8).
- This rate is **robust to mesh refinement** provided the *physical* overlap is held fixed —
  the key advantage over algebraic-splitting WR.
- Generalization to **N equal-overlap subdomains** with rate bounded above by
  **1 − 4 r(1−r) sin²(π/(2(N+1)))** (Thm 3.10), plus an initial *stagnation* phase while
  boundary information propagates inward.
- Numerical experiments (§4, test problem 4.1) confirming the theory.

### Test problem (paper eq. 4.1), L = 1
```
u_t = u_xx − exp(−(t−1)² − (x−1/4)²),   0<x<1, 0<t<3
u(0,t) = e^{−2t},   u(1,t) = e^{−t},   u(x,0) = 1
```
Discretization: centered 2nd-order finite differences in space (Δx=1/(n+1)); **backward Euler**
in time; Δx = Δt = 0.01.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? |
|----|-------|------|-----------|---------|
| C1 | 2-subdomain SWR error contracts linearly at per-double-iteration rate ρ = α(1−β)/(β(1−α)) | quantitative theorem + numerics | yes | ✅ yes |
| C2 | The convergence rate is robust to mesh refinement at fixed physical overlap | quantitative | yes | ✅ yes |
| C3 | N equal-overlap subdomains converge with rate ≤ 1−4r(1−r)sin²(π/(2(N+1))); initial stagnation while info propagates | quantitative bound + qualitative | yes | ✅ yes |
| C4 | Larger overlap ⇒ faster convergence; §4 numerics confirm the theory | quantitative/qualitative | yes | ✅ yes |

## 3. Method (independent, from scratch)

All code in `work/`; no code was taken from the authors (none is distributed). Language: Python
3, numpy only for the solver (matplotlib for figures). Tool versions logged in the venv.

1. **Reference full-domain solver** (`solve_full`): backward-Euler heat solver on the whole
   interval [0,1], Dirichlet BCs g₁,g₂ applied at all times, custom Thomas tridiagonal solve
   per step. This is the "true" solution the DD algorithm is compared against (as in the paper:
   "the difference between the numerical solution on the whole domain and the solution obtained
   from the domain decomposition algorithm").
2. **Subdomain solver** (`solve_subdomain`): same discretization on a sub-interval, with
   time-dependent Dirichlet data at both ends supplied from the neighbor's *previous iterate*
   interface trace over the entire time strip — i.e. the space-time-continuous overlapping
   Schwarz waveform-relaxation update (eqs 2.4–2.7, 2.21–2.24, 3.2–3.3).
3. **Experiment 1** (`run_two_subdomain`): Ω₁=[0,β], Ω₂=[α,1], initial guess constant-in-time =
   IC value (as the paper states). Measured the interface error at grid point *b* vs the full
   solution per iteration; fit the geometric decay to obtain the per-double-iteration factor and
   compared to ρ. Overlaps (α,β) ∈ {(0.4,0.6),(0.45,0.55),(0.48,0.52)}, Δx=Δt=0.01.
4. **Experiment 2** (`run_N_subdomain`): 8 equal subdomains with 35% overlap, snapped to grid;
   Jacobi-style parallel sweeps; measured max interface error (proxy for ‖ξᵏ‖∞) vs the Thm 3.10
   bound.
5. **Mesh robustness** (`mesh_robust.py`, C2): fixed overlap (0.4,0.6), Δx refined 0.02→0.0025.
6. **Judging**: three independent free-Argo LLM referees (gpt-5.2, gemini-2.5-pro, gpt-4.1)
   scored claims C1–C4 from the numeric evidence.

Reproduce: `cd work && python3 -m venv .venv && . .venv/bin/activate && pip install numpy scipy matplotlib && python swr_heat.py && python mesh_robust.py && python make_figs.py`.

## 4. Results vs paper

### C1 — Two-subdomain contraction rate (Fig 4.1)

| (α, β) | overlap | ρ predicted = α(1−β)/(β(1−α)) | measured (per double iter) | rel. error |
|--------|---------|-------------------------------|----------------------------|------------|
| (0.40, 0.60) | 0.20 | **0.4444** | **0.4439** | 0.11% |
| (0.45, 0.55) | 0.10 | **0.6694** | **0.6690** | 0.06% |
| (0.48, 0.52) | 0.04 | **0.8521** | **0.8518** | 0.04% |

The measured per-double-iteration contraction factor matches the theoretical ρ to **~0.1% or
better** across all three overlaps. Error decays cleanly geometrically (e.g. (0.4,0.6): interface
error 0.65 → 1.3×10⁻⁴ over 22 iterations). **C1 reproduced.** (Fig `evidence/fig41_two_subdomain.png`.)

### C2 — Mesh robustness (headline claim)

Fixed overlap (α,β)=(0.4,0.6), ρ_pred = 0.4444:

| Δx | Δt | measured (per double iter) |
|----|----|----------------------------|
| 0.02   | 0.02   | 0.4439 |
| 0.01   | 0.01   | 0.4439 |
| 0.005  | 0.005  | 0.4439 |
| 0.0025 | 0.0025 | 0.4439 |

The contraction factor is **invariant to four significant figures across an 8× mesh refinement**,
exactly confirming the paper's central claim that the overlapping-Schwarz WR rate is robust to
mesh refinement (in contrast to classical algebraic-splitting WR, whose rate degrades). **C2
reproduced.**

### C3 — N-subdomain bound + stagnation (Fig 4.2)

8 subdomains, 35% overlap:
- Predicted upper bound (per double iter) = **0.9726**; measured decay = **0.9327**.
- Measured ≤ bound, as Thm 3.10 requires (it is an *upper* bound, not an equality).
- Observed **~4 iterations of stagnation** (error ≈ 0.99) before clean geometric decay — precisely
  the paper's remark that "the error stagnates since information has to be propagated across
  domains."

**C3 reproduced** (consistent with the bound and the qualitative stagnation behavior; a single
(N,r) case tested). (Fig `evidence/fig42_eight_subdomain.png`.)

### C4 — Overlap vs. speed

From the C1 table, larger overlap ⇒ smaller ρ ⇒ faster convergence: overlap 0.20 gives ρ=0.444
(fast), overlap 0.04 gives ρ=0.852 (slow). This monotone relationship, and the tight agreement
with theory throughout, confirms §4's numerical conclusions. **C4 reproduced.**

## 5. LLM-judge panel (free Argo, localhost:44497)

| Judge | Verdict |
|-------|---------|
| argo:gpt-5.2 | **REPLICATED** (C1,C2 SUPPORTED; C3,C4 SUPPORTED/consistent) |
| argo:gemini-2.5-pro | **REPLICATED** (all four claims supported) |
| argo:gpt-4.1 | **REPLICATED** (all four claims SUPPORTED) |

Unanimous REPLICATED. Full referee texts in `evidence/judges/`. (argo:claude-opus-4.8/4.7 were
attempted but hit an Argo chat-endpoint response-serialization quirk; the gpt/gemini panel was
used instead — all free endpoints.)

## 6. Discussion & limitations

- The replication is **quantitatively tight** on the paper's two headline analytic results (C1
  contraction formula, C2 mesh robustness), matching to ~0.1% / 4 sig-figs. These are the paper's
  core contributions.
- Test problem, discretization (centered FD + backward Euler), overlaps, and mesh are exactly as
  specified in §4, so this is a faithful, not approximate, reproduction of the paper's own
  experiments.
- C3 is verified for a single (N=8, r=35%) configuration against an *upper bound*; the measured
  rate correctly lies below it and the stagnation phase appears. A fuller sweep over N and r would
  strengthen C3 but is not needed to confirm the claim.
- Compute was trivial (1D, ~99 interior nodes × 300 time steps × tens of iterations), run locally;
  no GPU/HPC needed.
- No fabricated numbers: every figure in §4 above comes from `evidence/results.json` /
  `evidence/mesh_robust.json` produced by the from-scratch solver.

## Verdict
**Verdict:** REPLICATED

---

`WAVE_RESULT set=PDE-100 paper=Gander-Stuart-1998-waveform-relaxation-heat(DOI:10.1137/S1064827596305337,rank77) verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/PDE-Gander-Stuart-waveform-relaxation-heat-1998 one_line=From-scratch numpy backward-Euler overlapping-Schwarz WR solver reproduces the 2-subdomain contraction rate rho=alpha(1-beta)/(beta(1-alpha)) to ~0.1% for three overlaps, confirms mesh-robustness (factor 0.4439 invariant across 8x refinement), and matches the 8-subdomain Thm 3.10 bound with the predicted stagnation phase; 3/3 free-Argo LLM judges say REPLICATED.`
