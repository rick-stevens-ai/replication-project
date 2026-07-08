# Failure Analysis — QC-2203.04340 (Honest Critique)

## Overall
Verdict is REPLICATED and substantively earned: the paper's headline
Fig. 7 noiseless ordering is reproduced from a first-principles
numpy-only simulator, and the ordering holds on **every** one of 24
random instances (not just the median). That said, several substantive
gaps prevent this from being a comprehensive replication of the paper's
practical claims.

## Per-claim confidence

| Claim | Tested? | Status | Confidence |
|---|---|---|---|
| C1 monotone E_res(nr) | YES | REPRODUCED | HIGH |
| C2 inverse monotone fidelity(nr) | YES | REPRODUCED | HIGH |
| C3 implicit parity QAOA >> standard QAOA | YES (at p=3 only) | REPRODUCED | MEDIUM (see gap 3) |
| C4 driver-line depth scaling | STRUCTURAL only | CONFIRMED at N=6 | MEDIUM (see gap 6) |
| C5 CNOT noise scan | NO | NOT TESTED | N/A |

## Substantive gaps

### 1. Restricted problem class
Only the paper's exact instance family (`J_ij ~ U[-1,1]` on `K_6`) was
tested. The parity-QAOA advantage has NOT been re-verified in this
replication for weighted MaxCut, portfolio-like log-normal instances,
higher-order (k>=3) Ising, or graphs sparser than complete. The
encoding overhead could look very different on sparse or weighted
instances. → Open question 1.

### 2. No noise model — C5 not attempted
This is the biggest gap. C5 is the claim that most matters for NISQ
deployment: "the noiseless ordering carries over to modest CNOT error".
We did not touch it, because it requires Qiskit-Aer noise simulation
and would have broken the dependency-free simulator design. → Open
question 2 (with concrete ZNE + symmetry-verification plan).

### 3. Standard-QAOA baseline is a single-p data point
Our C3 comparison (implicit parity vs standard unencoded QAOA) was
done ONLY at p=3. The 8x E_res advantage is real at that depth but
we did not sweep p for the standard-QAOA baseline. It is plausible
standard QAOA closes some of the gap at larger p; the paper does not
address this either. → Would tighten Section 3 of REPORT.

### 4. Connectivity-overhead trade-off asserted, not quantified
C4 was verified STRUCTURALLY (5 driver lines × 5 qubits for implicit;
single-qubit-parallel for explicit) but was NOT compiled to a specific
hardware coupling map to count physical CNOT depth. The paper's real
device-level claim (parity encoding wins on connectivity-limited
hardware) therefore is not device-level replicated here. → Open
question 3.

### 5. Constraint penalty c is a hidden knob
Fixed at c=3.0 throughout. The fully-explicit variant's poor median
(E_res=0.479) may partly reflect a suboptimal c. Adaptive c(l) or
c(nr) schedules are unexplored. → Open question 4.

### 6. Modular depth scaling only confirmed at N=6
Fig. 5's asymptotic "system-size-independent depth ~lmax" claim is
structural. At N in {8, 10, 12, 15} the pattern-of-cycles overhead may
still grow sub-linearly with N before the asymptotic flatness kicks in.
That is the size range NISQ hardware actually operates in.  → Open
question 5.

### 7. Optimiser is deliberately weak
Paper's own stochastic accept-if-improves (8 starts × 150 moves).
Faithful to the paper, but a modern gradient / interpolation heuristic
(INTERP, TQA, ADAM on parameter-shift gradients) would change absolute
numbers. The ordering is very unlikely to flip (the per-instance gap
is ~15×) but the absolute residual energies would improve substantially.

### 8. Instance count 24 vs paper's 96
Medians are already tight at 24 (see IQRs in `evidence/results.json`)
so this does not change the verdict. Tail behaviour on the upper
quartile of nr=1.0 would firm up with 96 instances. Cheap to redo if
someone wants publication-grade error bars.

### 9. Fidelity is small in absolute terms
Best median fidelity is 0.20 (nr=0.0). This is faithful to the paper
but means the "ordering" is on the tail of a broad distribution. For
practical hardware certification one would want F >= 0.5, which
requires larger p or a better optimiser (see gap 7).

## What is NOT a failure

- Skipping Qiskit was deliberate and correct: the physical Hilbert
  space is only 2^15 = 32,768, direct statevector evolution is a
  4-line inner loop in numpy, and it's dramatically easier to audit
  than a Qiskit circuit tree. This is not a shortcut, it is the
  cleanest possible implementation.
- Skipping the noise scan (C5) is a scope decision, not a bug. The
  noiseless ordering IS the core physics of the plot's y-intercept
  and IS reproduced.
- Reading Fig. 7 y-values off the plot is unavoidable — the paper
  does not publish the underlying arrays. Our numbers land inside
  the visible bands cleanly for all four `nr`.

## Bottom line

Verdict REPLICATED is substantively correct for the headline
(noiseless Fig. 7 ordering + C3 vs standard QAOA). The paper's
device-level, noise-tolerant, and larger-N practical claims are
NOT independently verified here and are correctly listed as
follow-ups in `open_questions.json`.
