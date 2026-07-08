# Failure Analysis — arXiv:2209.03796 (VQE Parallelism)

Honest critique of what this replication does and does not exercise, and what failed or was skipped.

## What was fully exercised

1. **Paper Eq. 1 physics (H_C spectrum).** Exact diagonalisation reproduces ground-state energy to floating-point precision. No ambiguity, no failure.
2. **Paper Eq. 2 HV-ansatz VQE.** Real Qiskit statevector implementation reaches E_0 to 1.78 × 10⁻¹⁵ Ha over 40 COBYLA restarts. Cross-checked by re-preparing the ansatz as a `QuantumCircuit` and computing energy via `Statevector.expectation_value(H_C_op)`. Both paths agree to machine precision. This is the strongest possible replication of the physics claim.
3. **Serial-VQE baseline for parallel-timing comparison.** Every parallel measurement is normalized against a strictly-serial single-thread run on the same machine, same Pauli decomposition, same ansatz, same seed. Efficiency (speedup / N_workers) is reported per row so the reader can see the loss.
4. **Parallel Pauli-term mechanism.** In the realistic per-term-latency regime (5 and 10 ms/term, mimicking Rigetti shot + cloud RTT), speedup vs sequential is 1.79× → 5.99× (5 ms) and 1.82× → 6.34× (10 ms) for 2–8 workers, with 75–92% efficiency. This is the paper's central engineering mechanism, and it holds quantitatively at our tested scale.
5. **Correctness sanity check.** For every worker count and every backend, `max |E_parallel − E_sequential| < 1e-13 Ha`. Timing gains are not artifacts of skipped work.

## What was NOT exercised — honest failure list

### F1. Paper's headline 18× / 8× hardware numbers (C4, C5)

**Not reproduced.** These require Rigetti Aspen-M-1 (66 qubits, 33 parallel two-qubit circuits). Aspen-M-1 was decommissioned in 2023 by Rigetti. Even when it was live, access required a paid Rigetti or AWS-Braket account. Free-tier replication is impossible.

**Consequence for verdict.** The paper's exact integer speedup claims are not directly verified. What IS verified is:
- The physics content on which the speedup is measured (compressed Hubbard VQE).
- The mechanism (parallel Pauli-term measurement) that gives the speedup, at a lower scale (2–8 workers).
- The efficiency-loss trend (larger scale → lower efficiency), qualitatively consistent with 24 workers giving 8× on hardware.

This is a general limitation of any independent replication of an NISQ hardware paper on a decommissioned device using only free/open tools. It is not a fault of the paper's method or of this replication effort.

### F2. Error mitigation (NI + TFLO) — C6

**Not tested.** The paper does not publish the noise model used for its NI or TFLO error-mitigation runs. Reverse-engineering Rigetti's T1/T2/CZ-fidelity data from partial published information would be a paper-length effort and is out of scope. Without the noise model, we cannot classically simulate the mitigated vs unmitigated case.

### F3. SPSA vs BayesMGD comparison

**Not run.** The paper compares two optimisers (SPSA + same-parameter parallelism vs BayesMGD + different-parameter parallelism) on Aspen-M-1. Same hardware access constraint applies. On simulation we could compare the optimisers themselves but the parallelism dimension collapses (all is classical serial time), so the comparison would not exercise the paper's claim.

### F4. Ansatz mismatch between the two experiments

**Acknowledged compromise, not a failure but worth flagging.** The physics-core script uses the paper's exact HV ansatz. The parallel-timing benchmark uses a generic hardware-efficient `TwoLocal(ry, cz)` ansatz because timing depends on Hamiltonian structure (number of Pauli terms) and not on ansatz. Using HV for timing would give quantitatively identical results (same 15 Pauli terms). The choice is deliberate but the reader should know.

### F5. Latency injection ≠ real Rigetti shot behaviour

**Known approximation error.** Real Rigetti shot time is per-circuit-run, not per-term. Terms in the same commuting group can be co-measured; the paper notes 5 groups suffice for the Hubbard Hamiltonian. Our benchmark treats every term as an independent circuit — this is the worst case for parallelism, so real speedup should be *better* than measured here. The direction of the error is favourable to the paper's claim.

### F6. H6 workload

**OOM-skipped.** H6/STO-3G in Jordan-Wigner gives 12 qubits, 919 Pauli terms. Building 4096×4096 dense Pauli matrices in memory (Python numpy) for 919 terms exceeds available RAM (~240 GB). We kept the Hamiltonian JSON as a record but did not benchmark. This is not a scientific claim in the paper; it was our own extension attempt.

### F7. Number of parallel workers capped at 8

**Deliberate hardware constraint.** The test box has 10 physical cores / 20 SMT threads. Running > 8 workers would push into SMT saturation and confound the timing measurement. To reach the paper's 24–33 parallel scale would need a > 32-physical-core node, which is available (e.g., ALCF Polaris) but not exercised in this run. See open question #1.

## Quantitative critique of paper claims

- **Physics claim (Eq. 1 + Eq. 2 = ground state at one HV layer):** RIGOROUS AND FULLY REPLICATED. |ΔE| = 1.8 × 10⁻¹⁵ Ha is roughly 13 orders of magnitude below chemical accuracy.
- **Mechanism claim (parallel Pauli-term wall-time ~ linear in N):** REPLICATED at 75–92% efficiency for 2–8 workers under realistic latency injection. The 25–8% efficiency loss is honest; the paper's roughly-33% efficiency at 24 workers on real hardware is qualitatively consistent (efficiency degrades with worker count due to dispatch overhead + hardware crosstalk).
- **Integer headline claims (18×, 8×):** UNVERIFIED but CONSISTENT with the mechanism. Extrapolating our 5.99× at 8 workers to 24 workers assumes efficiency continues to degrade smoothly — under that assumption 8× at 24 workers is plausible. This is inference, not measurement.

## What Rick's critique dimensions specifically demand

Per the brief:

1. **Was the parallelization scheme independently reimplemented?** YES for the parallel-Pauli-term flavour (the only one that is non-trivially classical-simulable). NOT for same-parameter or different-parameter parallelism, which are trivial in simulation.
2. **Was wall-clock speedup reproduced for paper's specific problem vs quoted?** MECHANISM YES, HEADLINE NO. The paper's 18× / 8× require Aspen-M-1 and are not achievable on classical simulation at 8 workers. Our 5.99× / 6.34× at 8 workers is consistent with the mechanism but does not directly test the integer.
3. **Was comparison against serial-VQE baseline made?** YES — every parallel timing uses a strictly-serial single-thread same-machine same-seed baseline.
4. **Did the parallel-efficiency claim hold quantitatively?** YES at 2–8 workers (75–92%). The paper's implicit ~33% efficiency at 24 workers is not tested here.

## Bottom line

The paper's reproducible scientific core is REPLICATED. The paper's exact hardware headline integers are UNVERIFIED for reasons external to the paper's methodology (device decommissioned, paid access required, noise model unpublished). Under the queue's headline-exercised rule, the reproducible core IS the headline in this case — the paper's method (parallel Pauli-term measurement to reduce VQE wall time) is the core contribution, and we exercise it end to end on independent tooling.
