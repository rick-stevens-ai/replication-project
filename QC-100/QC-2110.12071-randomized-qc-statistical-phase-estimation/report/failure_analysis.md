# Failure Analysis — QC-2110.12071 replication

**Purpose:** an honest, uncharitable-to-self critique of what this replication did and did not
demonstrate. Kept separate from `REPORT.md` so the failure/gap ledger is scannable in isolation.

## Verdict: REPLICATED (backbone-only). A stricter reviewer could argue for PARTIAL.

The `REPLICATED` verdict is defensible **only** under the QC-100 wave brief's
"small-but-faithful instance, minutes-on-laptop" scope, which explicitly targets the paper's
statistical estimator (Alg. 1 + Eq. 6) and does **not** demand reproduction of the paper's
algorithmic novelty (Lemma 2) or its headline numerical claim (FeMoco resource estimate).
The label reflects the wave brief scope, not full paper reproduction.

## Gap 1 (largest) — Lemma 2 LCU compilation was BYPASSED, not reproduced

- **What the paper claims:** Lemma 2 gives a randomized LCU construction of $e^{i\hat H t_j}$
  whose gate cost is $\tilde O(\lambda^2 t^2/\delta)$ *independent of the number of Pauli
  terms $L$*. This is the paper's **key algorithmic novelty** — the property that
  differentiates it from Lin & Tong 2020 (which uses block-encoding and is $L$-dependent).
- **What this replication did:** substituted an **exact statevector oracle**
  ($U_j$ computed via `expm(iH t_j)` from the full eigendecomposition of $\hat H$) in place
  of Lemma 2. Every claim about gate counts, $L$-independence, or compilation-error suppression
  is therefore **entirely bypassed**.
- **Consequence:** the replication verifies the *statistical wrapper* around the oracle, not
  the *oracle itself*. A hypothetical adversarial reader could correctly say: "this
  replication proves nothing about the paper's algorithmic contribution; only about the
  Lin–Tong CDF backbone the paper builds on."
- **Mitigation:** flagged explicitly in REPORT.md §5 ("Not tested"), in REPORT.tex critique
  section, and enumerated as Open Question #1 with concrete next steps.

## Gap 2 — No head-to-head vs. canonical QPE or Bayesian QPE

- **Missing baseline:** textbook Kitaev QPE with $t\sim 8$ ancilla qubits gets $\ll 1\%$ error
  on a 2-qubit TFIM in one shot. Bayesian QPE (Wiebe–Granade 2016) commonly needs $10$–$100\times$
  fewer shots than fixed-schedule estimators. Neither was implemented.
- **Consequence:** we cannot say whether the randomized SPE scheme is competitive on a small
  Hamiltonian; we only verified its scaling matches its own predicted rate. The **relative**
  advantage over baseline QPE variants at matched circuit-depth-×-shots budget is
  **unmeasured**.
- **Mitigation:** flagged as Open Question #2.

## Gap 3 — Sample-complexity trade-off is only 1-D, not 2-D

- **What the paper does:** explicitly trades runtime vector $\vec r$ (gate depth per query,
  via truncation $d$ and $t_j$ grid) against sample count $N$ — the Pareto frontier over
  $(\vec r, N)$ is the paper's central resource statement.
- **What this replication did:** fixed $\vec r$ implicitly by choosing $d=20$ (and the
  standard $t_j$ grid), then swept only $N$. The 2-D Pareto surface is **unmapped**.
- **Consequence:** the quantitative trade-off that gives the paper its resource claim is not
  independently exercised — only one slice of it is.

## Gap 4 — Fourier construction is the *unimproved* Lin–Tong choice

- **What the paper does:** improves Lemma 1 constants over the naive truncated Heaviside
  Fourier series (tighter $A(\vec r)$ scaling for given target accuracy).
- **What this replication did:** used the naive truncated Heaviside series that Lin–Tong
  originally used. Reported $A(\vec r) = 2.094$ at $d=20$ matches an $O(\log d)$
  order-of-magnitude estimate but does **not** verify the improved-Lemma-1 constant.
- **Consequence:** C3 is a structural / order-of-magnitude check, not a rate-and-constant
  match. If someone reads "REPLICATED" as claiming reproduction of the improved Lemma 1,
  that would be wrong.

## Gap 5 — Only one problem instance, only two visible eigenvalues

- **Problem:** 2-qubit TFIM with $\lambda=2$ is the smallest non-trivial instance. The paper's
  motivating regime is $\lambda \sim 1500$ Ha (FeMoco) with hundreds of eigenvalues in a
  chemistry Hamiltonian.
- **Missed edge cases:** near-degenerate eigenvalues, low-overlap ground states
  ($\eta \ll 0.1$), continuous-spectrum stress tests, chemistry-scale Hamiltonians.
- **Consequence:** the replication says nothing about robustness of the estimator in the
  regimes the paper actually cares about.

## Gap 6 — Binary-search extraction is a heuristic, not the paper's method

- The reproduction's low-$N$ energy-error RMS ≈ 1 (at $N \le 1000$) is a **binary-search
  heuristic artifact** (threshold occasionally crosses at the first-excited jump, not the
  ground-state jump). The paper's Lin–Tong multi-round binary search was **not implemented**.
- **Consequence:** the downstream energy-error scan (fig_scaling.png right panel) reflects
  the harness's threshold code, not the paper's extraction algorithm. Slope $-1.29$ in the
  higher-$N$ regime is real but not directly comparable to the paper's $E_\text{gs}$
  error scaling.

## Gap 7 — Noise: zero

- All simulations were noiseless statevector. Every real quantum device has depolarizing /
  amplitude-damping / measurement error on the Hadamard-test ancilla. The paper's
  error-suppression-by-sampling argument is a **compilation**-error argument, not a
  **hardware-noise** argument. This replication tests neither.

## Gap 8 — "Heisenberg scaling" — the paper does not claim it, but the brief asks

- The brief-critique prompt asks whether "Heisenberg-scaling was verified for a specific test
  unitary vs. quoted." Care needed: **the paper does not claim Heisenberg $1/T$ scaling** in
  the Kitaev/QPE sense. It claims Hoeffding shot-noise $N^{-1/2}$ scaling for the estimator,
  with total-cost scaling $\lambda^2/\Delta^2\eta^2$. We verified the $N^{-1/2}$ rate
  (slope $-0.451$ vs. $-0.500$). A "Heisenberg-limit" comparison against textbook QPE at
  matched query depth was **not made** — see Gap 2.

## Meta-gap — Verdict scope

- `REPLICATED` correctly describes the C1+C2 backbone.
- A reviewer who reads "REPLICATED" as endorsing the paper's full claim (including
  $L$-independent gate cost and FeMoco resource estimate) would be misled. The verdict is
  scoped by the QC-100 wave brief's explicit "small-but-faithful" envelope, which this
  replication honors. **The verdict does not endorse the paper's algorithmic novelty as
  reproduced.**
- A stricter labeling scheme (e.g. `REPLICATED-BACKBONE` or `PARTIAL`) would communicate
  this more crisply. Under the standing QC-100 verdict vocabulary, `REPLICATED` is retained
  with this failure log attached.

## What would move this from `REPLICATED (backbone)` to `REPLICATED (full)`
1. Implement Lemma 2 LCU compilation and verify $L$-independent gate scaling on a mid-sized
   molecular H (Open Q1).
2. Reproduce the Pareto surface over $(\vec r, N)$ on a real chemistry Hamiltonian (Open Q4).
3. Head-to-head vs. Bayesian QPE + shadows at matched shot budgets (Open Q2).
4. Noise robustness (Open Q3).
5. Even a *scaled-down* FeMoco (say, active-space 20–30 orbitals) resource estimate would
   move C5 from "not tested" to "partially tested".
