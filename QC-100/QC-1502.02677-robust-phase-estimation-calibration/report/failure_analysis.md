# Failure analysis — QC-100 / arXiv:1502.02677

Honest catalog of what this replication does **not** establish, and where the
work is weaker than the summary suggests. Written 2026-07-06 as part of the
backfill. **This section is deliberately unfriendly to our own verdict.**

## What was actually tested

- **C1 (Heisenberg scaling `σ ∝ 1/N`):** tested quantitatively via a
  14-generation Monte-Carlo sweep with 500 trials/point. Fitted slope
  **−0.98**, R² = 0.997 vs theoretical −1.0. **Robust match.**
- **C2 (Shot-noise baseline `σ ∝ 1/√N`):** tested at the same query budget.
  Fitted slope **−0.50**, R² = 0.9997. **Robust match.**
- **C3 (cos/sin quadrature identity, Eq. V.3):** verified against exact
  Qiskit `Statevector` for `k ∈ {1,...,256}` to a max absolute diff of
  `1.8e-14`. **Machine-precision match.**

## What was NOT tested (and this matters)

### 1. Heisenberg scaling was verified qualitatively, not proven

- Fitted slope −0.98 vs theory −1.0 is close enough to be visually
  indistinguishable on log-log, but we did **not** verify the analytic
  **constant** in front of the `1/N` (the KLY Sec. V.5 constant, which
  the 2021 erratum tightened to `π/(3 k_j)` from Higgins et al.).
- We did **not** probe the crossover `N` where the ladder starts to beat
  shot noise. The small-`N` region (`K < 4`) is dominated by
  range-unwrap noise; we bypassed it by restricting the RPE fit to
  `K ≥ 4`. A cleaner replication would characterize the crossover
  behavior explicitly.
- Only **one** value of the over-rotation `ε = 0.037` was tested. A
  proper scaling study would sweep `ε` and check that the −1 slope is
  independent of `ε` over the paper's stated regime.

### 2. Robustness to SPAM error was NOT tested (paper's Sec. IV; C4)

- The KLY paper's stronger and arguably more novel claim is that RPE
  survives realistic state-preparation and measurement errors, with an
  additive-error model `(δ_prep, δ_meas)` (Sec. IV). **We ran a
  noiseless simulator.** The SPAM claim is confirmed here only in the
  trivial sense of "theory says so; nothing in our data contradicts it."
- To close this gap: parameterize `δ_prep`, `δ_meas` (and/or a Qiskit
  noise model with T1/T2/readout confusion) and rerun the sweep.
- Impact on verdict: **REPLICATED is defensible for scaling** but the
  reader should NOT infer that SPAM robustness was empirically shown by
  this replication. It was not.

### 3. NO head-to-head comparison against standard RB

- KLY Sec. VI positions RPE as a sample-efficient alternative to
  randomized benchmarking (RB, Magesan et al. 2011). One of the paper's
  practical selling points is fewer samples for the same precision.
  **This replication does not run RB and therefore does not verify the
  sample-efficiency advantage.**
- To close this gap: implement Clifford-RB on the same
  `R_x(π/2 + ε)` circuit, measure the sample count required for
  3-σ detection of `ε`, and compare against the RPE sweep on a common
  (samples, precision) axis.
- Impact on verdict: the "beats RB" story is **completely untested here**
  even though we say REPLICATED for the scaling claim.

### 4. Range-unwrap heuristic differs slightly from paper's literal prescription

- We use "pick the multiple of `2π/k` closest to the previous
  generation's estimate" instead of KLY's literal range restriction
  `Â_{j+1} ∈ (Â_j − π/2^j, Â_j + π/2^j]`. Under the assumption of no
  > 1-period jumps between consecutive generations, these are
  algorithmically equivalent — but that equivalence only holds when
  each generation's local error is well within its `π/2^j` window.
- Not stress-tested at higher `ε` values or with adversarial noise.
  Could fail silently if `ε` is close to a multiple of `π/k` for some
  early generation.

### 5. Binomial sampler shortcut vs live `qc.measure()` loop

- We replace `qc.measure()` loops on the Qiskit simulator with
  `np.random.binomial(M, p)`, on the grounds that the two are
  mathematically identical when the state prep + measurement is exactly
  the analytic circuit (proven by `qiskit_verify.py`'s `1.8e-14`
  agreement).
- This saves minutes of wall-clock but adds one layer of abstraction
  between the report and a "real" Qiskit backend. If someone wanted to
  reproduce our exact bitstreams via the Qiskit simulator, they would
  need to re-run through `qc.measure()` and match seeds.

### 6. No noisy backend / no hardware execution

- Everything ran on a noiseless statevector simulator. There is no
  evidence in this replication that RPE works on:
  - A Qiskit `FakeBackend` with real IBMQ noise snapshots;
  - Actual IBM Quantum / IonQ / Rigetti hardware;
  - Any device with realistic T1/T2/leakage/readout confusion.
- A stronger replication would run against at least `FakeManila` or
  `FakeGuadalupe`. This is the natural next step; captured as Open
  Question #4.

### 7. No two-qubit or multi-qubit extension

- The paper's abstract restricts to a **universal single-qubit
  gate-set**, and we tested only the single-qubit RPE core. The
  2-qubit extension (Rudinger et al. 2017 and follow-ons) is entirely
  out of scope of this replication.
- Captured as Open Question #1.

### 8. The 2021 erratum was noted but not exploited

- We flag the erratum in the summary (constant in Sec. V.5 tightens to
  `π/(3 k_j)`), but we do not re-derive or plot the tightened bound.
- A stricter replication would overlay the tightened analytic constant
  on `figures/precision_vs_N.png` and check whether the empirical RMSE
  saturates the bound.

## Bottom line

- The **scaling law** claim (C1 + C2 + C3) is **genuinely reproduced**
  at the exponent level with high statistical confidence
  (500 trials/point over 4 decades of N, R² > 0.997 both curves).
- The **robustness** and **RB-comparison** claims that motivate the
  paper's practical relevance are **NOT tested** here.
- Verdict **REPLICATED** is defensible **for the headline scaling
  claim only**. A reader who takes "REPLICATED" to mean "the paper's
  full story is confirmed" is being misled. The SPAM-robustness and
  RB-beating claims remain untested and are captured as open questions
  (see `open_questions.json`, entries #2, #3, #4).
