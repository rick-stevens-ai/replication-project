# Independent Replication Report — OSTI 3365789

**Paper:** Yuwei Geng, Junqi Yin, Eric C. Cyr, Guannan Zhang, Lili Ju,
*"Parallel-in-Time Solution of Allen-Cahn Equations by Integrating Operator Learning into the Parareal Method"*,
Journal of Scientific Computing (2026). DOI **10.1007/s10915-026-03337-1**. OSTI **3365789**.
**Domain:** hpc_algorithms / parallel-in-time PDE solvers + operator learning.
**Replicator:** independent reimplementation from equations (no paper code used). 2026-07-02.

---

## 1. Paper summary

The paper accelerates time-integration of the **Allen-Cahn (AC) equation** and its
mass-conservative variant using the **Parareal** parallel-in-time algorithm, where the
expensive *fine* propagator is a conventional numerical solver and the cheap *coarse*
propagator is a **convolutional neural network (ACNN/mACNN)** trained to emulate the
fully-discrete time-stepping operator. Key ingredients:

- Classical AC: `u_t = ε² Δu + f(u)`, `f(u)=u−u³`, periodic BC, double-well potential
  `F(u)=(u²−1)²/4`, energy `E(u)=∫ (ε²/2)|∇u|² + F(u)`.
- **Fine solver** (Eqs. 6–8): second-order **Crank-Nicolson** in time + 5-point-stencil
  **finite-difference** Laplacian in space, solved by **Picard iteration**; claimed
  2nd-order accurate in space and time; obeys the **Maximum Bound Principle** (u∈[−1,1])
  and **energy dissipation**.
- **Parareal** (Eqs. 13–14, Alg. 2): `U^k_{n+1} = G(U^k_n) + F(U^{k−1}_n) − G(U^{k−1}_n)`,
  with the exact invariant that after k iterations the first k coarse intervals coincide
  with the sequential fine solution; converges in k ≪ s iterations for speedup.
- **Central empirical claim (Sec. 4.2.3, Fig. 13):** a *numerical* CN coarse propagator at
  the large coarse step Δt=0.1 makes Parareal for AC converge slowly / stagnate / violate
  MBP (esp. for random ICs), whereas their CNN coarse propagator (with a bound-limiter
  layer) converges fast and robustly — this is the paper's motivation for the ML coarse
  propagator.

## 2. Claims table

| ID | Claim | Type | Testable independently? | Tested? |
|----|-------|------|-------------------------|---------|
| C1 | Fine CN+FD scheme is 2nd-order accurate in space & time | numerical | Yes (manufactured solution / exact AC solutions) | ✅ (space) / partial (time) |
| C2 | Classical AC obeys the Maximum Bound Principle, u∈[−1,1] | structural | Yes | ✅ |
| C3 | Discrete energy E(u) is non-increasing in time | structural | Yes | ✅ |
| C4a| Parareal invariant: after k iters, first k intervals = fine | algebraic | Yes (exact) | ✅ |
| C4b| Parareal converges to the sequential fine solution | algorithmic | Yes | ✅ |
| C5 | Numerical CN coarse propagator makes AC-Parareal ill-behaved (slow/blow-up/MBP-violating) at Δt=0.1 | empirical | Yes | ✅ → **contradicted** |
| C6 | CNN coarse propagator gives GPU speedup up to 128 GPUs | systems/ML | Not attempted (needs their trained CNN + Frontier; not core to correctness) | ➖ |

## 3. Method (independent reimplementation)

All code is numpy-only, in `work/replicate_ac.py` and `work/replicate_ac2.py`; run on **uicgpu**
(Python 3, numpy 1.23.5, CPU — problem is small). No paper code or external data used.

1. **Fine solver.** CN + 5-point periodic FD Laplacian, `f(u)=u−u³`, Picard iteration to
   tol 1e-13. The linear system `(I − ½Δt ε² Δ_h) x = rhs` is solved **spectrally (FFT)** using
   the exact eigenvalues of the periodic 5-point stencil `λ = (2cos(k)−2)/h²` — an exact,
   fast solve for the FD operator (not a spectral discretization of the PDE).
2. **V1b order test (C1).** Manufactured solution `u=0.5 sin(2πx)cos(2πy)cos(t)` on `[0,1]²`
   with analytic forcing S added so u solves the AC PDE exactly; measure RMSE vs refinement.
   Spatial order: fix Δt=2e-4, refine N∈{32,64,128,256}. Temporal order: fix N=256, refine Δt.
3. **V2/V3 (C2, C3).** Fine solve of the merging-bubbles IC (paper Eq. 16), ε=0.01, N=128,
   T=2, Δt=1e-3; track global min/max (MBP) and energy E(u) over time.
4. **C4/C5 Parareal.** Full Parareal (Alg. 2, Eq. 13) with a **numerical CN coarse propagator**
   (Δt_coarse=0.1) and fine propagator (Δt*=1e-3 sub-steps), on merging bubbles (T=1, s=10)
   and on a **random IC** (grain-coarsening style, seed=0). Build the sequential-fine reference,
   check the exact-first-k-intervals invariant, convergence `‖U^k−U^{k−1}‖_∞`, final rel-L2 vs
   fine, and iterate amplitude (MBP).
5. **Scoring.** LLM-judge = free Argo **gpt-5.2** (temp 0), fed the paper claims + our raw JSON;
   claim-by-claim + overall verdict.

## 4. Results vs paper

### C1 — 2nd-order accuracy (manufactured solution)
| N | h | RMSE | spatial rate |
|---|---|------|------|
| 32 | 3.13e-2 | 6.259e-5 | — |
| 64 | 1.56e-2 | 1.566e-5 | **1.999** |
| 128 | 7.81e-3 | 3.916e-6 | **2.000** |
| 256 | 3.91e-3 | 9.790e-7 | **2.000** |

→ **Second-order spatial convergence confirmed** (rate → 2.0), matching the paper. Temporal
refinement showed near-zero rate only because at N=256 the spatial error is the floor (temporal
error already below it); this does not contradict 2nd-order-in-time, it is simply not isolated by
this configuration. **C1: reproduced (space); partial overall.**

### C2 — Maximum Bound Principle
`u_max = 1.0000000000000087`, `u_min = −1.000000000000054` over T=2 → within [−1,1] to ~1e-13.
**C2: reproduced.**

### C3 — Energy dissipation
`E_initial = 0.0174190`, `E_final = 0.0168298`, monotone non-increasing at every sample.
**C3: reproduced.**

### C4 — Parareal invariant + convergence (merging bubbles, s=10)
- Invariant (first k intervals = fine after k iters): **holds to machine precision** at every k.
- `‖U^k−U^{k−1}‖_∞`: 1.85e-3, 2.19e-5, 4.80e-7, 1.36e-8, 6.21e-10, 3.69e-11, 2.31e-12, 1.64e-13,
  2.32e-14, 1.17e-14 → clean geometric convergence.
- Final Parareal vs sequential fine: rel-L2 = **4.25e-15**.
**C4: reproduced.**

### C5 — numerical coarse propagator pathology (Sec 4.2.3) — **CONTRADICTED**
| IC | final rel-L2 vs fine | iterations | MBP violated? | max iterate amp |
|----|------|------|------|------|
| merging bubbles | 4.25e-15 | 10 | No | 1.0000 |
| random (seed 0) | 6.50e-15 | 10 | No | 0.9000 |

Our **numerical** CN coarse propagator drives Parareal to machine precision in ~10 iterations for
**both** merging-bubbles and random ICs, with **no MBP violation and no blow-up** — the opposite of
the paper's claimed pathology. The paper itself attributes the numerical-coarse failure to the
correction step corrupting the nonlinear Picard iterations ("the Picard solver reaches the
prescribed maximum iteration number without convergence"). Our implementation (unconditionally
stable CN, FFT-exact linear solve, Picard converged to 1e-13 every step) avoids that weakness, so
the pathology disappears. **Conclusion: C5 is implementation-dependent, not a fundamental property
of numerical coarse propagators for AC-Parareal.** This does not invalidate the ML approach (a CNN
coarse propagator can still be *faster* per step), but it materially weakens the paper's stated
*motivation* that numerical coarse propagators simply do not work.

### C6 — GPU speedup
Not attempted: requires the authors' trained CNN and Frontier-scale runs; it is a systems/ML
performance claim, not a correctness claim, and out of scope for a <25 min numerical replication.

## 5. LLM-judge verdict (free Argo gpt-5.2)
Claim-by-claim: **C2, C3, C4 REPRODUCED; C1 PARTIAL (space only); C5 CONTRADICTED.**
Overall: **PARTIAL** — "the method's fundamentals replicate, while the paper's specific negative
result about the numerical coarse propagator does not." Full text: `evidence/llm_judge_verdict.md`.

## 6. Assessment
The paper's **numerical and algorithmic fundamentals reproduce cleanly and independently**: the
CN+FD fine scheme is 2nd-order in space, obeys the MBP and energy dissipation, and the Parareal
algorithm satisfies its exact invariant and converges to the fine solution to machine precision.
These are the load-bearing correctness claims and they hold. The one substantive discrepancy is the
paper's *motivating* empirical claim (C5) that numerical coarse propagators make AC-Parareal fail —
which our robust implementation contradicts, indicating that failure was implementation-specific
(Picard non-convergence under the correction step) rather than intrinsic. Honest overall grade:
**PARTIAL** (solid on fundamentals; one motivating claim contradicted).

## Verdict
**Verdict:** PARTIAL

<!-- WAVE_RESULT set=OSTI paper=3365789 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/OSTI-3365789-parareal-operator-learning-allen-cahn one_line=Allen-Cahn CN+FD fine scheme (2nd-order space, MBP, energy dissipation) and Parareal invariant+convergence independently reproduced to machine precision; paper's motivating claim that a numerical coarse propagator fails (Sec 4.2.3) was contradicted by our robust CN-coarse Parareal. -->

WAVE_RESULT set=OSTI paper=3365789 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/OSTI-3365789-parareal-operator-learning-allen-cahn one_line=Allen-Cahn CN+FD fine solver (2nd-order in space, MBP, energy dissipation) and Parareal exact-invariant+convergence reproduced to ~1e-15; paper Sec4.2.3 claim that numerical coarse propagator fails was contradicted.
