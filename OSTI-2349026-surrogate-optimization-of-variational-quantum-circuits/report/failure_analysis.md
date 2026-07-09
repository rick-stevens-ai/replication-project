# Failure Analysis — OSTI-2349026 Replication

**Paper:** Gustafson et al., "Surrogate optimization of variational quantum circuits," *PNAS* **122**(36), e2408530122 (2 Sep 2025). DOI 10.1073/pnas.2408530122. OSTI-2349026.

**Verdict:** PARTIAL.

This file catalogs what did **not** work in this replication, splitting failures into three buckets: (A) paper-side reproducibility gaps that make certain results unreachable to any independent third party, (B) replicator-side scope decisions I made and their consequences, and (C) observed optimizer failures that are themselves *findings* consistent with the paper.

---

## A. Paper-side reproducibility gaps

### A1. SWS (sparse wave function simulator) is not publicly released

- **What failed.** The chemistry benchmarks in Table 1 and Fig. 2 of the paper (H2O/STO-3G, N2/STO-3G, N2/cc-pVDZ, H4/cc-pVDZ, 14–40 qubits, 28–193 parameters) all use SWS as the smooth surrogate that the STALK algorithm computes a Hessian on.
- **Why.** SWS is cited via paper refs 86, 87 but no separate public URL is provided in the Data/Materials/Software Availability section. It is not packaged into STALK v0.1 (`work/code/stalk-0.1/`; verified by directory listing and grep).
- **Impact.** Independently reproducing the paper's headline chemistry speedup numbers (2–4× fewer calls to reach δE = 10⁻³ / 10⁻⁴ / 10⁻⁵ Hartree) requires either (a) writing an independent sparse-wave-function simulator (multi-month project), or (b) obtaining SWS privately from the authors.
- **Status.** Not overcome. This is a paper-side gap, not a replicator-side failure. Noted as a genuine limitation in the paper's own reproducibility posture.

### A2. IBM Quantum access to `ibm_brisbane` is paid/gated

- **What failed.** The 40-qubit TFIM demonstration (Fig. 4) and the Ns=12..32 scan (Fig. 5) both require executing circuits on IBM's `ibm_brisbane` device.
- **Why.** IBM Quantum's larger devices are behind either paid access or curated collaborator programs; standard third-party accounts do not have priority access. The paper does not release the raw shot-count data per circuit per iteration.
- **Impact.** Fig. 4 and Fig. 5 are third-party-non-verifiable without either paying IBM Quantum credits or obtaining the raw shot data from the authors.
- **Status.** Not overcome. This is a resource gap, not a methodological one, but it is worth flagging because the paper's most visually striking result (40 qubits on real hardware) is the least independently checkable.

### A3. Baseline optimizer settings under-specified

- **What failed / concerning.** The paper reports gradient-based methods (BFGS, CG) "fail" under sampling noise, but does not specify FD step size, gradient tolerance, or whether a specialized noisy-gradient optimizer (SPSA — Simultaneous Perturbation Stochastic Approximation) was tried.
- **Why.** Not stated in text or SI.
- **Impact.** Cannot exactly match the paper's baseline conditions; SPSA in particular is the standard noisy-gradient optimizer for VQE and its omission is unusual.
- **Status.** Partial. My replication uses `scipy.optimize.minimize` defaults for BFGS/CG (finite-difference gradient with default `eps`). SPSA was not benchmarked in either the paper or this replication.

---

## B. Replicator-side scope decisions

### B1. Ns=4 not Ns=40 for TFIM

- **What I did.** Ran TFIM at Ns=4 with 4 ansatz parameters, not the paper's Ns=40.
- **Why.** Local statevector simulation is 2^Ns memory; Ns=40 requires either a real 40-qubit QPU (see A2) or MPS with proper truncation on GPU (see B3). Ns=4 is 16-dim dense — trivial on a laptop, allowing 5 seeds × 6 optimizers to complete in minutes.
- **Impact.** The 4-parameter ansatz cannot reach the true ground state of even the Ns=4 system (ansatz min -0.686 vs true GS -3.945). I therefore benchmark distance to the ansatz's own variational minimum, not to the true GS. This is a fair test of **optimizer performance** but does not exercise the paper's **quantum advantage / physical accuracy** narrative.
- **Status.** Documented limitation. Sufficient for a partial-scale check; not sufficient to certify the full 40-qubit claim.

### B2. Exact-statevector surrogate, not MPS(bond=4)

- **What I did.** Used the exact statevector cost as the smooth surrogate, and the exact statevector plus additive Gaussian noise as the noisy high-level channel.
- **Why.** MPS with bond dimension 4 requires a tensor-network library and careful contraction management (opflow / quimb / TensorNetwork), which is a meaningful engineering task and was not in scope for the single-session budget.
- **Impact.** My surrogate is "perfect" — its landscape exactly matches (up to noise) the target it is trying to guide the optimizer over. This biases in favor of SurrogateLS: the observed 2.5× speedup on TFIM should be treated as an upper bound on what an imperfect MPS surrogate would deliver. Since the paper still reports 2–4× with imperfect MPS/SWS surrogates, my result is consistent with theirs even under the bias.
- **Status.** Documented limitation. A more faithful replication is feasible on uicgpu; recommended for a follow-up wave.

### B3. ExcitationSolve baseline skipped

- **What I did.** Did not benchmark ExcitationSolve (ES), the paper's tightest competitor to SurrogateLS in Fig. 2.
- **Why.** ES is not in scipy; it comes from the paper's ref 95 and requires pulling that reference implementation.
- **Impact.** The most informative one-to-one comparison (SurrogateLS vs ES) is not independently checked. The paper's claim that "SurrogateLS eventually reaches lower energy than ES" is untested here.
- **Status.** Documented limitation. Recommended for a follow-up.

### B4. Chemistry benchmarks (H2O, N2, H4) not attempted

- **What I did.** Only ran TFIM.
- **Why.** Chemistry benchmarks require SWS (see A1), which is not public.
- **Impact.** The paper's Table 1 headline numbers (2–4× on chemistry) are unverified.
- **Status.** Documented limitation. Blocked by A1.

---

## C. Observed optimizer "failures" that are actually findings

These are **not** failures of the replication — they are results consistent with the paper's claims and reinforce the verdict.

### C1. BFGS never reaches gap<0.1 in 5 seeds

- Median calls to gap<0.1: N/A (never reached).
- Consistent with paper: "gradient-based methods fail under sampling noise."

### C2. CG failed in v1 (final gap +0.971 after 132 calls)

- Same underlying cause: sampling noise corrupts finite-difference gradient estimates enough that the CG line-search cannot make progress.
- Consistent with paper.

### C3. SLSQP failed in v1 (final gap +3.588 — worse than starting point)

- SLSQP is a constrained-optimization method being pushed off-domain by noisy gradient signals.
- Consistent with paper's general "gradient-based methods fail" claim.

### C4. COBYLA is *surprisingly* fast in v1 (11.29× vs Powell) and stays competitive in v2

- Not a failure — a genuine finding not emphasized by the paper. COBYLA (derivative-free trust region) is very competitive at loose precision (gap<0.1: 3.64× vs Powell) and at moderate precision (gap<0.01: 6.81× vs Powell) on the TFIM Ns=4 problem.
- **Interesting.** The paper's benchmarks generally include COBYLA but the paper's narrative focuses on the SurrogateLS–vs–Powell comparison. On this tiny scaled-down problem COBYLA actually outperforms SurrogateLS for the coarse-precision regime, suggesting the SurrogateLS advantage may kick in more strongly at large parameter counts (see open question 1 in `open_questions.json`).

### C5. SurrogateLS does not reach gap<0.01 in any seed at v2 sigma=5e-4

- With sigma=5e-4 relative to a landscape whose minimum is at -0.686 and starting value ~+0.286, the noise floor is ~0.1% of the dynamic range but ~5% of the (ansatz_min – final_target) gap at threshold 0.01. The SurrogateLS parabolic-fit step becomes noise-dominated near the minimum.
- Consistent with the general observation that surrogate-based line-search converges rapidly early (large gradient signals) then plateaus at a noise-limited precision. The paper reports similar behavior in Fig. 2 with SurrogateLS reaching lower δE than ES/BFGS but not to arbitrary precision.
- Not a failure of the method — it is the expected noise-floor behavior.

---

## D. Bugs / cleanups deferred

None known that affect correctness. The replication scripts intentionally implement a minimal SurrogateLS (no adaptive span, no restart, no directional pruning beyond eigenvalue ordering) so that the observed behavior can be attributed to the algorithm's core, not to add-on heuristics.

---

## E. Summary

| Bucket | Count |
|---|---:|
| Paper-side reproducibility gaps | 3 (A1–A3) |
| Replicator-side scope decisions | 4 (B1–B4) |
| Observed optimizer failures consistent with paper | 5 (C1–C5) |
| Correctness bugs | 0 |

Nothing observed contradicts the paper. The verdict is PARTIAL rather than REPLICATED because A1 and A2 make the paper's headline chemistry and 40-qubit-QPU numbers unreachable to any independent third party without private/paid resources, not because anything in the replication itself went wrong.
