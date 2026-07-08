# Failure Analysis / Honest Gap Catalog — W1 qDRIFT

This file exists to record what the replication did NOT do, so the
REPLICATED verdict is not confused with a full reproduction of every claim
in the paper.

## Verdict: REPLICATED (Coverage 8/10, Agreement 9/10)
The headline algorithmic claims were exercised and confirmed. The gaps
below are real but they are coverage gaps, not disagreements — every
quantitative claim we DID exercise was consistent with the paper.

## Gap 1 — Trotter baseline is minimal (Trotter-1 only)
- **What paper says:** qDRIFT's L-independence is the key advantage over
  deterministic product formulas. The paper discusses (and follow-ups
  quantify) the regime where higher-order Suzuki-Trotter of orders 2 and 4
  is competitive with qDRIFT for low-commutator / structured Hamiltonians.
- **What we did:** implemented and swept deterministic first-order Trotter
  only. Confirmed qDRIFT beats Trotter-1 in the many-terms regime.
- **What we did not do:** implement Trotter-2 or Trotter-4 (Suzuki
  fractals). Never generated a crossover phase diagram.
- **Impact on verdict:** does not invalidate the L-independence /
  1-over-N-scaling claims, which were fully exercised. But the "qDRIFT
  beats Trotter" claim in the report is only reproduced against the
  weakest baseline. Flagged in REPORT.tex Critique §1 and in open
  question #1.

## Gap 2 — Small qubit count
- Ran on n = 4 qubits (dim 16) because ground-truth `expm(-iHt)` is dense
  and exact simulation of larger systems is infeasible on the target
  free-Python-on-CherryRd envelope.
- Paper cares about the tens-to-hundreds-of-qubits regime (chemistry
  Hamiltonians with L in the thousands).
- Algorithmic scaling should be regime-independent, so this is a coverage
  limitation, not a disagreement. Explicitly acknowledged in the report.

## Gap 3 — Chemistry resource estimates unreproduced
- The paper's showcase application is molecular Hamiltonians
  (H_2, H_2O, and larger). Specific gate-count estimates are quoted.
- We did NOT reproduce any of those specific numbers. Two reasons:
  1. The exact Pauli coefficient sets for the paper's molecules are
     described but not deposited as machine-readable data at a stable URL.
     Regenerating them requires re-running an electronic-structure package
     (PySCF / OpenFermion) with the paper's basis + active space choices,
     which was out of budget.
  2. Even given the Hamiltonians, exactly simulating the resulting
     many-qubit dynamics classically is infeasible.
- **This is the largest substantive gap.** A follow-up with OpenFermion +
  the paper's stated basis choices could close it in isolation without
  needing to re-verify the algorithmic scaling.

## Gap 4 — Diamond-norm proxy, not true diamond norm
- We compute the average trace-norm error over Haar-random pure input
  states and compare it to the paper's diamond-norm (worst-case) bound.
- Our measured proxy lies strictly below the bound at every N — that is
  the *right sign* of consistency, but it is not a check on the tightness
  of the bound.
- A true diamond-norm computation would require solving an SDP over the
  qDRIFT channel's Choi matrix. This was not deployed.

## Gap 5 — No noise-robustness experiments
- The paper's error analysis is fully coherent / noiseless.
- We did not simulate qDRIFT under depolarizing noise, coherent
  overrotation, or cross-talk. Because qDRIFT typically needs more gates
  than an optimized high-order Trotter, its noiseless advantage may be
  eroded on real hardware. Flagged as open question #4.

## Gap 6 — Random Pauli Hamiltonians only
- Our test Hamiltonians are random Pauli strings with |Normal(0,1)|
  coefficients rescaled to fix lambda. Structured Hamiltonians (lattice
  models, molecular electronic-structure Hamiltonians) have very
  different commutator patterns and may give different Trotter-vs-qDRIFT
  crossovers.
- Flagged in the Critique and part of the next-step probe under open
  question #1.

## Gap 7 — Formal proof of the diamond-norm bound not re-derived
- We tested the numerical consequence of the paper's Theorem 1 bound
  (measured error < 2 lambda^2 t^2 / N at every N). We did not
  independently re-derive the proof.
- This is a common convention for numerical replications and is
  acknowledged rather than obscured.

## What the replication DID do (for balance)
- Independently reimplemented qDRIFT from the paper's specification in
  clean-room numpy + scipy (no qDRIFT primitive from an SDK).
- Confirmed 1/N scaling numerically over N = 16 ... 2048 (128× dynamic
  range), with error x N nearly constant.
- Confirmed L-independence at fixed N over L in {8, 24, 60}
  (7.5× dynamic range), with variation within Monte Carlo noise.
- Confirmed measured error < analytic bound 2 lambda^2 t^2 / N at every
  measured (N, L) point.
- Confirmed the qualitative Trotter-vs-qDRIFT crossover for many-term
  Hamiltonians (against the Trotter-1 baseline).

## Headline-exercised judgment
The paper's headline claims — the 1/N error scaling, the L-independence at
fixed N, and the explicit 2 lambda^2 t^2 / N bound — are the ones stated
in the abstract and Table I of the paper, and every one of them was
quantitatively exercised and matched. The chemistry resource estimates
and the more nuanced Trotter-2/4 comparison are second-order elaborations,
not the headline. Under the replication set's headline-exercised rule this
supports **REPLICATED** rather than PARTIAL.
