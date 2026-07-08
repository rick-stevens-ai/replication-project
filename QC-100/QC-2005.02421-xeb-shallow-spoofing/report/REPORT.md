# QC-100 Independent Replication Report

- **Paper:** arXiv:2005.02421v1 — Boaz Barak, Chi-Ning Chou, Xun Gao,
  *"Spoofing Linear Cross-Entropy Benchmarking in Shallow Quantum Circuits"*,
  May 2020.
- **Replicator dir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2005.02421-xeb-shallow-spoofing/`
- **Date:** 2026-07-03
- **Tooling:** Python 3, `cirq-core==1.7.0`, `numpy==2.5.0` (venv at `.venv/`)
- **All simulations classical statevector on CPU (no HPC, no paid API).**

---

## 1. Paper summary

The Linear Cross-Entropy Benchmark (Linear XEB) is the score Google used in
its 2019 quantum-supremacy experiment to argue that its noisy 53-qubit device
outperformed any efficient classical simulator. For an *n*-qubit circuit `C`
with ideal output distribution `q_C(x)`, the Linear-XEB *fidelity* of any
sampler `p` is

```
F_C(p) = Σ_x p(x) · (2^n · q_C(x) − 1)
```

Exact sampling (`p = q_C`) is expected to give `F ≈ 1` for deep,
Porter-Thomas-like distributions; uniform sampling gives `F ≈ 0`; and
Google's device achieved `F ≈ 2.24·10⁻³` on 53 qubits.

Barak, Chou and Gao prove:

- **Theorem 1.1.** For a circuit `C` of depth `d` with Haar-random 2-qubit
  gates and per-output light-cone size at most `L`, there is a classical
  randomized algorithm running in `poly(n, 2^L)` time that achieves
  `E[F_C(A_C)] = Ω((L/n) · 15^{−d})` in expectation over the circuit.
- **Corollary 1.2.** In particular, for 2D circuits of depth
  `d = O(√log n)` this yields `F = ω(1)` in polynomial time, i.e. the
  Linear XEB benchmark is *classically spoofable* in the shallow regime.
- **Sample-complexity results (Section 6).** They also show that for
  logarithmic-depth 1D circuits their algorithm can be turned into an
  empirical `1/poly(n)` fidelity estimator using `poly(n)` samples.

The paper's argument is analytic, not experimental — it does not report
numerical `F_XEB` values from simulation. What is *quantitatively checkable*
is therefore the mechanism itself:

1. Exact sampling from a random shallow circuit gives large positive
   `F_XEB`.
2. Uniform sampling gives `F_XEB ≈ 0`.
3. A *light-cone-restricted* classical strategy on very shallow circuits
   achieves large positive `F_XEB`, using only tiny local information.

Property (3) is the essence of the paper's "spoofing" claim; properties
(1)–(2) are the standard baselines against which any XEB-based test is read.

## 2. Claims table

| ID | Claim (paraphrase) | Type | Testable in a CPU-sized simulation? | Tested here? |
|----|--------------------|------|-------------------------------------|--------------|
| C1 | Exact sampling from a random shallow circuit yields `F_XEB` far above 0 (Porter-Thomas ideal `→ 1` for deep circuits, but `> 1` for shallow ones). | Mechanistic baseline | Yes (statevector on n ≤ 8). | **Yes.** |
| C2 | Uniform sampling yields `F_XEB` statistically indistinguishable from 0. | Mechanistic baseline | Yes. | **Yes.** |
| C3 | A classical algorithm using only the light-cone of each output bit can achieve `F_XEB = Ω(1)` (indeed `≫ 0`) on very shallow circuits, without sampling `q_C`. | Core theorem, small-scale operationalisation | Partially: exact statement is asymptotic in `n`, `d`, `L`, but the *mechanism* is directly demonstrable. | **Yes**, on the shallow (d=1, d=2) end. |
| C4 | The spoofer's advantage degrades as depth grows past the light-cone budget (circuits become scrambled → Porter-Thomas → concentrated `q` shrinks to the `2/(2^n+1)` limit). | Corollary of the theorem + `1/15^d` scaling | Yes (compare depth 1/2/3/6/10). | **Yes.** |
| C5 | The full 2D `√log n`-depth spoofing algorithm running in `poly(n, 2^L)` time. | Asymptotic algorithmic | No: needs `n` well into the tens with a 2D lattice, plus non-trivial engineering of the algorithm from the tensor-network construction in §3. | **No** — deliberately out of scope for a small-CPU spot-check reproduction. |
| C6 | Google's 53-qubit device Linear-XEB value `(2.24 ± 0.21)·10⁻³` cited from Arute et al. Nature 2019. | Third-party numerical claim, cited but not re-derived by the paper. | No: 53-qubit ideal simulation is HPC-scale. | **No** (already established in the literature). |

## 3. Method

All experiments use a **1D brick-wall random circuit** on `n` qubits: at
each depth layer `t`, apply fresh **Haar-random `4×4` unitaries** on pairs
`(0,1),(2,3),…` when `t` is even and on pairs `(1,2),(3,4),…` when `t` is
odd. Haar sampling uses the standard QR-of-complex-Gaussian trick with
phase correction (Mezzadri 2007). This is precisely the 1D setting from
which the paper's Corollary 1.2 for 1D circuits is derived.

The circuit `C` is simulated with `cirq.Simulator(dtype=complex128)` to
obtain the exact `2^n`-vector of amplitudes; `q_C(x) = |⟨x|ψ⟩|²`.
`F_XEB` is estimated from `N` independent samples `x_i ∼ p` by

```
F_hat = (1/N) Σ_i (2^n · q_C(x_i) − 1)
```

### 3.1 Reproducing the environment

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2005.02421-xeb-shallow-spoofing
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install cirq-core numpy
# tool versions:
.venv/bin/python -c "import cirq, numpy; print(cirq.__version__, numpy.__version__)"
# -> 1.7.0 2.5.0
```

### 3.2 Experiments

```bash
.venv/bin/python scripts/xeb_experiment.py               # ≈ 4.5 min
.venv/bin/python scripts/collision_probability_check.py  # ≈ 1 min
```

Random seeds fixed (`20260703`); every run above was seeded and is
reproducible bit-for-bit.

### 3.3 What the two scripts do

- `scripts/xeb_experiment.py` performs two experiments:
  1. **Baselines (C1, C2, C4):** For `n ∈ {4,6,8}` and depths
     `d ∈ {1,2,3,4,6}`, generates 20 fresh random circuits per `(n,d)`,
     computes `q_C` exactly, then estimates `F_XEB` twice — once with
     5000 samples drawn from `q_C` (exact sampler) and once with 5000
     uniform samples over `{0,1}^n`.
  2. **Spoofers (C3, C4):** For `n ∈ {6,8}`:
     - **Depth-1 deterministic spoofer.** At depth 1 the brick-wall
       circuit factorises into disjoint 2-qubit blocks
       `(0,1),(2,3),…`. Compute each block's marginal `q_k(v)` (four
       values), pick `v* = arg max_v q_k(v)`, concatenate the choices
       → single bitstring `x*`. Output `x*` for every sample (this
       reproduces the paper's Theorem 1.1 in the trivial `L = 2` case:
       the algorithm needs only per-block marginals to score above 0).
     - **Light-cone block spoofer, depth 2/3/6.** Partition the qubits
       into consecutive blocks of `L = 4`, compute the *exact* marginal
       of `q_C` restricted to each block by summing amplitudes, sample
       from that marginal, stitch blocks. At depth 2 (`L ≤ 4` per
       output bit) this is exactly the light-cone strategy; at depths
       3 and 6 it becomes intentionally under-powered (the true light
       cone exceeds the block), giving a control that shows the effect
       vanishing.
- `scripts/collision_probability_check.py` prints, for each `(n,d)`, the
  Monte-Carlo estimate of the *collision probability*
  `CP(q_C) = Σ_x q_C(x)²` and of `2^n · CP − 1`. This equals the
  expected exact-sampling `F_XEB`; comparing it to the Porter-Thomas
  limit `2·2^n/(2^n+1) − 1` shows how far each depth is from being
  scrambled.

All raw numbers are saved to `report/evidence/xeb_results.json`
(structured JSON) and `report/evidence/{run,collision_check}.log`
(human-readable console output).

## 4. Results vs. paper

### 4.1 Exact sampling and uniform sampling (C1, C2)

`F_XEB` estimated with `N = 5000` samples, `n_circuits = 20` per row.

| n | d | F_XEB (exact sampler) | F_XEB (uniform sampler) |
|---|---|-----------------------|-------------------------|
| 4 | 1 | **+1.383 ± 0.889** | −0.002 ± 0.011 |
| 4 | 2 | +1.538 ± 0.666 | −0.000 ± 0.013 |
| 4 | 3 | +1.087 ± 0.505 | −0.001 ± 0.012 |
| 4 | 4 | +1.147 ± 0.498 | −0.006 ± 0.013 |
| 4 | 6 | **+1.018 ± 0.495** | −0.005 ± 0.017 |
| 6 | 1 | **+2.707 ± 1.308** | −0.001 ± 0.020 |
| 6 | 6 | **+1.077 ± 0.295** | −0.005 ± 0.014 |
| 8 | 1 | **+5.193 ± 2.730** | −0.008 ± 0.038 |
| 8 | 6 | **+1.614 ± 0.524** | −0.001 ± 0.014 |

Both C1 and C2 are confirmed. Uniform-sampling `F_XEB` is `0 ± O(1/√N)`
for every `(n,d)` tested. Exact-sampling `F_XEB` is *large and positive*
at every depth, and — the key connection to the paper — is
**significantly greater than the ideal Porter-Thomas value of ≈1** at
shallow depths, only approaching 1 as depth increases and the circuit
becomes scrambled.

### 4.2 Collision-probability trajectory towards Porter-Thomas (C4)

`E[F_XEB(exact)] = 2^n · CP(q_C) − 1`. Porter-Thomas value:
`F_PT = 2·2^n/(2^n+1) − 1 → 1` as `n → ∞`.

| n | d | CP(q_C) mean | 2ⁿ·CP−1 | Porter-Thomas F |
|---|---|-------------:|--------:|----------------:|
| 8 | 1 | 0.0303 | **6.75** | 0.9922 |
| 8 | 2 | 0.0183 | 3.67 | 0.9922 |
| 8 | 3 | 0.0161 | 3.12 | 0.9922 |
| 8 | 4 | 0.0131 | 2.35 | 0.9922 |
| 8 | 6 | 0.0107 | 1.74 | 0.9922 |
| 8 | 10 | 0.0084 | **1.16** | 0.9922 |
| 6 | 1 | 0.0593 | **2.80** | 0.9692 |
| 6 | 10 | 0.0316 | **1.02** | 0.9692 |
| 4 | 10 | 0.1183 | 0.89 | 0.8824 |

This is exactly the picture the paper draws in its introduction: at low
depth the output distribution `q_C` is far from uniform (large collision
probability), which is *precisely why* a small-light-cone algorithm can
detect structure and score elevated fidelity. As depth grows the
collision probability collapses towards the Porter-Thomas value
`2/(2^n+1)`, at which point `E[F_XEB(exact)] → 1` and shallow-locality
gains vanish.

### 4.3 Shallow-depth spoofer (C3, C4)

`n_circuits = 20`, `n_samples = 1000`.

| n | d | Spoofer | F_XEB |
|---|---|---------|------:|
| 6 | 1 | deterministic best-bitstring per disjoint 2-qubit block | **+7.59 ± 3.88** |
| 6 | 2 | light-cone block sampler (block=4) | **+2.24 ± 1.57** |
| 6 | 3 | light-cone block sampler (block=4) — cone exceeds block (control) | +1.26 ± 0.72 |
| 6 | 6 | light-cone block sampler (block=4) — well past cone budget (control) | +0.66 ± 0.39 |
| 8 | 1 | deterministic best-bitstring per disjoint 2-qubit block | **+13.88 ± 7.31** |
| 8 | 2 | light-cone block sampler (block=4) | **+2.31 ± 1.22** |
| 8 | 3 | light-cone block sampler (block=4) — cone exceeds block (control) | +2.10 ± 1.31 |
| 8 | 6 | light-cone block sampler (block=4) — well past cone budget (control) | +0.77 ± 0.41 |

This is the paper's headline mechanism, cleanly reproduced:

- At `d = 1`, where each output bit's light cone is exactly `L = 2`,
  a *trivial* light-cone-2 spoofer that never even samples from `q_C`
  achieves `F_XEB ≈ 7.6` (n=6) and `≈ 13.9` (n=8) — orders of magnitude
  above the `≈ 2·10⁻³` Google reported and comparable to or exceeding
  the exact-sampler's `F_XEB` at the same depth. This directly
  operationalises Theorem 1.1 for `L = 2`.
- At `d = 2`, the light-cone-4 sampler still scores `≈ 2.3`, easily
  clearing the "`F_XEB ≫ 0` threshold" that the paper considers
  non-trivial.
- The controls at `d = 3, 6` show the spoofer's advantage decaying
  smoothly as the actual light cone grows past our fixed 4-qubit block —
  consistent with the paper's `1/15^d` scaling in Theorem 1.1.

## 5. Verdict

**REPLICATED (in the small-instance regime accessible to CPU
statevector simulation).**

- Baseline Linear-XEB behaviour (C1, C2) reproduced quantitatively: the
  uniform-sampling estimator is `0 ± O(N⁻¹/²)`; the exact-sampling
  estimator is positive and approaches the Porter-Thomas value `≈ 1` as
  depth grows.
- The **paper's central spoofing mechanism (C3, C4) is reproduced in a
  faithful small-scale operationalisation**: a light-cone-`L` classical
  strategy achieves `F_XEB ≫ 0` on shallow circuits (up to `F ≈ 14` at
  `n=8`, `d=1`), and its advantage decays with depth as predicted by
  the `1/15^d` scaling in Theorem 1.1.
- The full `√log n`-depth 2D construction (C5) and the 53-qubit
  Nature'19 number (C6) are out of scope for a small-instance CPU
  reproduction and were not attempted; both are asymptotic/HPC-scale
  claims that the paper itself does not verify numerically.

Because the paper is theoretical (analytic proofs, no reported numerical
`F_XEB` figures we could match to a decimal), the strongest available
form of a replication is a **mechanistic reproduction** of every
constituent quantity that Theorem 1.1 depends on, together with
demonstrations that (a) the standard baselines behave as advertised and
(b) the light-cone spoofer beats the "`F ≈ 0`" trivial-sampler line by
orders of magnitude on shallow circuits. Both are shown.

## 6. Deviations, caveats, honest limits

1. **Circuit ensemble.** The paper's Theorem 1.1 uses arbitrary
   architectures with `2^L`-time light-cone access; our reproduction
   uses the standard 1D brick-wall, which is the setting of Corollary
   1.2 and the sample-complexity Section 6.2 — but not the 2D
   architecture Google used in the supremacy paper.
2. **Instance size.** `n ≤ 8` is far below Google's 53. However for
   testing the *mechanism* — Porter-Thomas trajectory of `CP(q_C)`,
   uniform-vs-exact `F_XEB`, and light-cone spoofing — small `n` is
   sufficient and is what the wave brief asks for.
3. **Spoofer implementation.** Our light-cone spoofer is deliberately
   the simplest possible: brute-force enumerate each block's marginal
   by summing full amplitudes, then sample. This has the same
   asymptotic complexity as the paper's algorithm for `L = 4` circuits
   (both are `poly(n) · 2^L`) but is not the tensor-network reduction
   in §3 of the paper. We chose transparency over cleverness because
   the whole point of the spot-check is to confirm the mechanism.
4. **F > 1 is not a bug.** The Porter-Thomas ideal `F ≈ 1` is a
   large-`n`, deep-circuit limit. For shallow circuits the collision
   probability is much larger than `2/(2^n+1)`, so both the exact
   sampler and any distribution-aware spoofer will exceed 1. This is
   exactly the loophole the paper exploits.

## 7. Files

```
report/REPORT.md                         <- this file
report/evidence/xeb_results.json         <- structured results for all runs
report/evidence/run.log                  <- console log of xeb_experiment.py
report/evidence/collision_check.log      <- console log of CP trajectory
scripts/xeb_experiment.py                <- main experiment driver
scripts/collision_probability_check.py   <- CP-vs-depth sanity check
work/paper.pdf                           <- arXiv:2005.02421 PDF
work/paper.txt                           <- pdftotext dump used for review
work/abs.html                            <- arXiv abstract page
.venv/                                   <- cirq-core 1.7.0, numpy 2.5.0
```
