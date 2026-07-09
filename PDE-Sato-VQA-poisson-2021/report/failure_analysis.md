# Failure Analysis — Sato 2021 VQA-Poisson Replication

Verdict is **REPLICATED**, but this file documents every part of the exercise
that did not succeed, was deliberately skipped, or produced a discrepancy from
the paper. Kept honest for future work.

## 1. Hard failures (things we tried and could not do)

### 1.1 Running the authors' reference code (`ToyotaCRDL/VQAPoisson`)
- **What happened.** The repo pins Qiskit 0.23 and imports from `qiskit.aqua`,
  which was retired in Qiskit 0.25.
- **Effect.** We could not execute the reference implementation on any modern
  Python environment.
- **Mitigation.** Reimplemented from scratch in NumPy (`work/vqa_poisson_replicate.py`).
  This turned out to be a positive: the replication is now an independent
  implementation of the paper's math, not a rerun of the authors' harness.
- **Residual risk.** If our reimplementation contains a bug that happens to
  match the paper's math but not the paper's *code*, we would not detect it
  through a code-vs-code diff. The Fig. 3(b) / Fig. 4 numeric matches make this
  unlikely but not impossible.

## 2. Discrepancies (numbers differed from the paper)

### 2.1 Periodic BC classical norm (Fig. 3(a))
- **Paper.** Classical norm at n=5, periodic BC ≈ 23.5.
- **This replication.** Classical norm 22.89 (mean of 5 trials).
- **Delta.** ~2.6 % low.
- **Likely cause.** The periodic 1D Poisson operator has a zero eigenvalue,
  and the classical solve requires an ε-regularization (`A + εI`) or a
  pseudoinverse. Neither the paper nor our code precisely specifies the
  regularization value used for the plotted "classical" curve. A small
  difference in ε changes the answer at the ~few-percent level.
- **Alternative cause.** Off-by-one in our periodic-tridiagonal construction
  (wrap terms in the wrong corners). Not ruled out.
- **Impact on verdict.** Non-fatal: the headline metric ε_tr = 0.0034 < 0.01
  still holds, and the quantum norm still matches (22.68 vs 22.9).
- **Fix.** Sweep ε ∈ {10⁻², 10⁻³, 10⁻⁴, 10⁻⁵} and see which value reproduces
  23.5. If none does, audit the periodic-tridiag construction.

## 3. Deliberate scope cuts (claims not tested)

### 3.1 C6 — scaling exponent T_it ∼ n^2.6 vs n^4.2
- **Why skipped.** Fitting an exponent requires sweeping n ≥ 6 (and ideally
  n = 7, 8) with hundreds of restarts each, and at n=5 we already saw
  L-BFGS-B iteration counts near 440. Wall-time budget would blow up.
- **What we did instead.** Recorded per-trial iteration counts at n = 2..5
  (8, ~30, ~80, ~440) and stated they are "consistent with" the paper's
  scaling — a directional check, not an exponent fit.
- **What would close it.** A dedicated n = 3..8 sweep, 40 trials each, both
  the Sato cost and the Liu cost in the same harness, with a hard eps_tr =
  0.01 stopping criterion. Multi-day job.

### 3.2 C7 — Neumann BC
- **Why skipped.** The paper reports Neumann converges but produces a
  qualitatively different solution because the singular-matrix regularization
  changes the effective operator. Reproducing this requires additional care
  with the nullspace projection, and the headline claim (< 0.01 trace distance)
  is already substantiated on Dirichlet and periodic.
- **Fix.** Add a Neumann branch to `vqa_poisson_replicate.py`. Straightforward.

### 3.3 C8 — theoretical asymptotic time-complexity claim
- **Why skipped.** Analytical argument in the paper's Sec. III.E; not
  replicable in code beyond spot-checking definitions.

### 3.4 NISQ-friendliness / real hardware
- **Not attempted.** No shot-noise sampler, no depolarizing-noise sampler,
  no IBM Quantum access. All results are noiseless NumPy statevector.
- **Why it matters.** The paper's motivation is that the O(1) measurement
  cost makes it NISQ-friendly. This replication does not test that motivation.
  The observed ~2.5% norm underestimation at n=5 is an expressibility artifact
  in the noiseless regime, NOT the NISQ error the paper is discussing.
- **Fix.** See open_questions.json Q4.

### 3.5 Head-to-head vs Liu 2020, VQLS, HHL
- **Not attempted.** Would substantiate the paper's comparative claim
  empirically. Deferred; see open_questions.json Q1 and Q5.

## 4. Methodological gaps (things we did differently from the paper)

### 4.1 Optimizer
- **Paper.** BFGS with analytic quantum-computed gradient.
- **This replication.** SciPy `L-BFGS-B` with numerical (finite-difference)
  gradient.
- **Consequence.** At the scale we ran (n ≤ 5, noiseless), optima agree. At
  larger n or with noise, the two setups could diverge — L-BFGS-B's line
  search behaves differently from vanilla BFGS, and finite-difference
  gradients pick up round-off that a quantum-computed analytic gradient
  would not.

### 4.2 Multi-start / best-of-k
- **Paper.** Sec. IV.B.2 initializes θ₀ ∈ [0, 4π]. Multi-start protocol not
  fully specified for Fig. 4.
- **This replication.** Single-shot per seed, mean over 10 seeds. No
  best-of-k pruning.
- **Consequence.** If the paper implicitly best-of-k'd, our reported means
  are pessimistic; if it did not, we agree.

### 4.3 Iteration count definition
- **Paper.** T_it = iterations to reach ε_tr = 0.01 (implicit stopping
  criterion).
- **This replication.** L-BFGS-B function evaluations, no ε_tr-based
  stopping. Numbers may differ by 2–3× because of line-search calls and the
  absence of a stopping test.
- **Consequence.** Our "consistent with n^2.6" statement is directional only.

### 4.4 Fig. 4 comparison is visual
- **What we did.** Read the paper's Fig. 4 log-scale curve by eye
  ("~0.001, ~0.001, ~0.002, ~0.007") and matched our per-n means to those
  visual targets.
- **What would be better.** Digitize Fig. 4 with WebPlotDigitizer and
  compare against certified target values.

## 5. Reproducibility risks

- **RNG.** We use `np.random.default_rng(seed=1000n+k)`. Fully reproducible on
  a fixed NumPy version.
- **BLAS.** L-BFGS-B calls BLAS; different BLAS backends can produce
  bit-different but scientifically identical results. Report values are means
  and should be BLAS-invariant to reported precision.
- **SciPy version.** Not pinned in the report; convergence path could shift
  slightly across SciPy releases but converged optimum should not.

## 6. Net honest assessment

The replication succeeds cleanly at what it actually tested (C1, C2, C3, and
C4 partial). It does NOT independently confirm:

- The scaling advantage over Liu 2020 (C6).
- The NISQ-friendliness argument (motivating rationale for the paper).
- Neumann-BC behavior (C7 partial).
- The Fig. 3(a) periodic classical-norm number (small discrepancy, un-diagnosed).

"REPLICATED" here means "the paper's operational headline for the tested
ranges is reproducible from scratch, from a from-scratch NumPy implementation
of the paper's equations," not "all eight claims independently confirmed."
