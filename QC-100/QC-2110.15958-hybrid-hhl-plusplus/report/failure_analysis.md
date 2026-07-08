# Failure Analysis — QC-2110.15958 (Hybrid HHL++)

## Overall verdict: REPLICATED (headline exercised, algorithm-level small-instance)

The paper's central testable claim (C1–C4) was reproduced end-to-end on an
independent Qiskit Aer statevector simulation: standard vs hybrid HHL on a
well-conditioned 2×2 system, both at fidelity 1.0000 vs `numpy.linalg.solve`,
with the hybrid variant using strictly fewer two-qubit gates (4 vs 50, −92%)
and strictly fewer qubits (2 vs 4, −50%). This is a genuine reproduction of the
paper's resource-reduction-with-retained-fidelity headline, not a paraphrase.

The following are honest limitations and gaps, not fabrications.

## What was genuinely reproduced
- **C1 correctness**: baseline HHL solves Ax=b to fidelity 1.0000 (exact by
  construction — t=3π/4 makes eigenvalue phases {1/4,1/2} exactly 2-clock-bit
  representable). This is a legitimate clean reference point, not a fudge.
- **C2/C3 resource reduction**: hybrid uses 4 CNOTs / 2 qubits vs baseline
  50 CNOTs / 4 qubits at the smallest fair size. Direction + magnitude match
  the paper's Table 1 qualitative pattern (hybrid qubit count FLAT vs standard
  growing linearly).
- **C4 fidelity retention**: hybrid fidelity = 1.0000, no loss.

## Genuine gaps / caveats (the honest critique)
1. **The hybrid circuit here is the LOGICAL MINIMUM, not the paper's full
   protocol.** The reproduction implements the hybrid pattern via a classical
   `np.linalg.eigh(A)` eigendecomposition feeding controlled Ry rotations —
   i.e. it *assumes* the eigenvalues are known classically and skips QPE
   entirely. The paper's actual novelty (C5) is a *quantum* semiclassical-QPE
   procedure for choosing the scaling factor γ WITHOUT classical eigen-knowledge.
   So the reproduced "hybrid" demonstrates the resource *envelope* but bypasses
   the paper's algorithmic contribution. A stricter reviewer could argue the
   headline resource numbers (4 CNOTs) are optimistic because they assume away
   the QPE the paper still needs.
2. **Gate-count comparison is not apples-to-apples with the paper.** Paper
   counts Quantinuum-native ZZPhase gates on QPE-only sub-circuits; this run
   counts transpiled {cx,u3} CNOTs on the FULL HHL circuit including the
   eigenvalue-inversion block. Absolute numbers therefore differ substantially
   (paper 57–95 QPE ZZPhase vs this run's 4 full-circuit CNOTs). Only the
   *direction* of reduction is claimed to match — the report is honest about this.
3. **C5 (novel γ-selection algorithm) NOT tested.** This is arguably the
   paper's principal intellectual contribution. Its omission is scoped as
   "out of QC-100 same-day scope," which is defensible for the resource+fidelity
   headline but means the paper's methodological novelty is unverified.
4. **C6/C7 (Quantinuum H-series hardware, 2q-depth-291 largest-to-date HHL,
   Table-2 hardware fidelities 98.6%/90.4%/42.6%) NOT tested.** Requires
   trapped-ion hardware access — irreproducible under free-simulation policy.
   The dramatic real-hardware fidelity collapse at 5-bit (42.6%) is exactly the
   regime that matters for the paper's practical claim, and it is untouched here.
5. **Only a single 2×2 κ=2 instance.** No sweep over condition number, matrix
   size, or |b⟩. The paper's portfolio-optimization S&P-500-derived instances
   (the actual application) are not reproduced. Scaling behavior of the hybrid
   advantage is therefore inferred, not measured.
6. **Noiseless only.** All fidelities are statevector-exact. The paper's entire
   practical contribution is about surviving NISQ noise; the reproduction says
   nothing about noise robustness of the hybrid variant.

## Bottom line
REPLICATED is the correct verdict for the resource-reduction-with-fidelity
headline (C1–C4) at the small-instance algorithm level — that claim is
genuinely and quantitatively reproduced. But the reproduction is narrow: it
demonstrates the resource *envelope* of the hybrid pattern while bypassing the
paper's actual algorithmic novelty (quantum γ-selection) and its entire
experimental hardware contribution. A reconciliation reviewer wanting the
paper's *methods* validated (not just its resource-scaling claim) should treat
this as REPLICATED-narrow.
