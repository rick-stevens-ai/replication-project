# Failure Analysis — OSTI 2564727 Replication

**Paper:** Grimm & Eaves 2025, *Accurate Numerical Simulations of Open Quantum Systems Using Spectral Tensor Trains*. DOI `10.1063/5.0228873`.

**Verdict:** REPLICATED (core analytic anchor, Eqs. 16–17); PARTIAL (paper overall).

This file is the honest ledger of what did **not** get done in this replication, why, and what a follow-up would need. It is separate from `REPORT.tex §GENUINE CRITIQUE`, which focuses on interpretive caveats; here we focus on execution gaps.

---

## 1. Intrinsic-noise spin-boson comparison (Fig. 3, claim C3) — NOT REPRODUCED
**What was skipped:** Reproducing Fig. 3 with the App. A intrinsic-noise kernel (obeying fluctuation–dissipation) and cross-checking against PT-TEMPO on the exact biased-qubit spin-boson geometry with the paper's spectral density and inverse temperature β.

**What was done instead:** The Fig. 3 *geometry* was mimicked (`H₀ = Ωσx + εσz, V = ασz`, with `Ω=1, ε=0.5, α=0.75`), but driven by **white extrinsic noise**. Result: our SLE-MC matches our own Lindblad, not the published spin-boson dynamics.

**Root cause:** The App. A kernel is a nontrivial implementation effort (Chebyshev expansion + FDT-weighted correlation matrix + Trotter reassembly) and PT-TEMPO requires an OQuPy setup. Neither fits the fast-replication budget. Prioritized C1 (exact analytic anchor) instead, because a failure of C1 would have invalidated everything downstream.

**Impact:** The paper's central *non-Markovian* benchmark is untested by us. C3 remains open.

**Remediation (if extended):** Port the App. A kernel. Stand up OQuPy PT-TEMPO on the same geometry. Overlay both dynamics for population and coherence across a temperature and coupling sweep. Report L2 / L∞ deviations rather than visual agreement.

---

## 2. 32-site chain memory scaling (Fig. 4, claim C4) — NOT REPRODUCED
**What was skipped:** The `p ≈ 2.0` (Q-ASPEN) vs `p ≈ 8.3` (PT-TEMPO) memory-scaling result on the 2–32 site extrinsic-noise quantum chain.

**Root cause:** This is the paper's principal *practical* selling point but requires (a) a working STT implementation with bond-dim / rank policy, (b) PT-TEMPO as reference, and (c) repeated runs across ≥5 chain lengths with careful RSS instrumentation. All three exceed the scope of a fast independent replication.

**Impact:** The economic case for Q-ASPEN over PT-TEMPO is unverified by us.

**Remediation:** Re-implement Eqs. 10–14 (matrix-product of Chebyshev-expanded `Kα(ω)`). Sweep bond-dim to see how sensitive `p` is. Fit log-log slopes on peak RSS vs site count for both methods.

---

## 3. STT barren-plateau training pathology (Fig. 5, claim C5) — NOT REPRODUCED
**What was skipped:** Empirical verification that the STT training exhibits barren plateaus.

**Root cause:** Requires the full STT parameterization and SGD/importance-sampling training loop. Orthogonal to correctness (a training pathology, not an analytic-limit issue), so deprioritized.

**Impact:** Cannot judge whether Q-ASPEN is *usable* out of the box, only that it is *correct* in the analytic limit.

**Remediation:** Instrument gradient norms layer-by-layer under SGD/Adam/K-FAC. Try Xavier / spectral-norm initializations designed to defeat barren plateaus in tensor networks. Report gradient-variance-vs-depth curves.

---

## 4. Complete-positivity under STT truncation — NOT TESTED
**What was skipped:** Even for C1/C2 where we verified trace preservation to 1.0000, we did not test complete positivity of the reduced density matrix under finite STT bond-dim truncation.

**Root cause:** We never ran the STT approximation, only the exact Lindblad reference and its stochastic-Schrödinger ensemble; both are CP by construction. CP under truncation is a distinct question that only appears once STT compression is in play.

**Impact:** If Q-ASPEN can violate CP at low bond-dim, that is a physical-validity concern for practitioners; we cannot rule this in or out.

**Remediation:** Diagonalize ρ at each timestep, log min eigenvalue vs bond-dim. Construct the Choi matrix of the effective STT propagator and test positive-semidefiniteness on small systems.

---

## 5. Non-Markovian crossover regime — NOT MAPPED
**What was skipped:** A systematic sweep of the correlation time `τ_c` from the Markov limit (`τ_c → 0`) into the strongly non-Markovian regime (`τ_c ~ T_sys`).

**Root cause:** The exact anchor we verified (Eqs. 16–17) is precisely the white-noise limit; everything the STT is *for* lives outside that limit. Mapping the crossover requires driving the SLE with exponentially correlated noise and comparing Q-ASPEN vs direct SLE-MC (which stays exact). We did not do this.

**Impact:** The regime of validity of Q-ASPEN's STT compression is not independently characterized.

**Remediation:** Drive the biased qubit with `⟨ξ(t)ξ(s)⟩ = (γ/2τ_c)e^{−|t−s|/τ_c}` for tunable `τ_c`. Sweep `τ_c / T_sys` across two decades. Log STT bond-dim required for a fixed target error.

---

## 6. Trace of what nearly went wrong (execution-side)
- **Sampling floor confusion (avoided):** Early runs at N_traj = 2.5k gave 7.5e-3 residuals. It would have been tempting to interpret this as method disagreement rather than sampling. The convergence sweep (`convergence.py`) was added specifically to demonstrate `~1/√N` scaling and rule out systematic bias. Lesson: always sweep the stochastic axis before claiming a floor.
- **Trotter-order confusion (avoided):** Also ran a `τ` scan to confirm the residual is sampling + `O(τ²)` discretization, not model mismatch. Without this, a `τ`-dependent artifact could have been mislabeled as a Q-ASPEN limitation.
- **Analytic-anchor sanity check (essential):** The `9.6e-13` closed-form match for the dephasing case is what gave us confidence that our Lindblad conventions (Hermitian conjugation, sign of `i`, factor of 2 in `e^{−2γt}`) are correct. Skipping this step would have made all downstream disagreements ambiguous.

---

## 7. Net position
The replication succeeded on what it targeted (C1 + C2) and honestly declared C3/C4/C5 out of scope. Nothing in this run failed silently. The gaps above are all *scope-limited omissions*, not *failed experiments* — the distinction matters for downstream reuse.
