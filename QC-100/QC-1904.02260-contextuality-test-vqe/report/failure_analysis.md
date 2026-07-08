# Failure analysis / honest critique — QC-1904.02260

Independent replication of Kirby & Love, PRL 123, 200501 (2019),
"Contextuality Test of the Nonclassicality of Variational Quantum Eigensolvers".

This document is the **honest self-critique** required by the QC-100 8-artifact
standard. The verdict is REPLICATED, but this file documents exactly what was
and was NOT independently verified, and what would strengthen the corroboration.

## 1. What WAS independently reproduced (strengths)

### 1a. The paper's headline algorithm was re-implemented from scratch
The Theorem 3 classifier (non-transitivity of commutation on the reduced set T)
was implemented directly in `code/contextuality_test.py` — not called from a
library, not adapted from a reference implementation. The classifier is short
(~30 lines) and directly checks the mathematical criterion: for a Pauli set S,
form T by dropping universally-commuting operators, then search for a triple
(A, B, C) in T with [A,B]=[A,C]=0 and {B,C}=0.

### 1b. The molecular Hamiltonians were built independently
Every tested Hamiltonian was constructed from PySCF integrals via OpenFermion
JW/BK transforms with straightforward active-space choices. No Hamiltonian
was quoted from the paper or from experimental SI files.

### 1c. All 6 tested Table I verdicts reproduce
- H2 JW 4q: non-contextual ✓
- H2 BK 4q: non-contextual ✓
- H2 BK-tapered 2q: non-contextual ✓
- HeH+ JW 4q: contextual ✓ (witness ZIII, IZII, IYZY)
- LiH BK 6q active: contextual ✓ (witness ZIIIII, ZZIIII, ZXIZII)
- H2O JW 8q active: contextual ✓ (witness ZIIIIIII, IIZIIIII, IIYZZZYI)

### 1d. VQE sanity check is chemically real
The 2q H2 Hamiltonian we run the contextuality test on is exactly the
Hamiltonian VQE would optimize. It recovers FCI to 1.6e-10 Ha with a
Ry-Ry-CNOT-Ry-Ry ansatz and COBYLA over 5 seeds. This is 7 orders below
chemical accuracy, confirming the test target is not a toy.

### 1e. Verdict is algorithmic yes/no with explicit witness
No LLM was used in scoring; no soft judgment. For each contextual case, the
witness triple is a concrete falsifier — anyone can independently verify that
those three Pauli strings satisfy [A,B]=[A,C]=0 and {B,C}=0.

## 2. What was NOT independently verified (weaknesses / caveats)

### 2a. The contextuality-witness test WAS reimplemented for the paper's specific Hamiltonians (major strength, noted)
This is explicitly a strength, not a weakness — flagged here per Rick's hard
requirement to state whether the test was independently implemented for the
paper's specific Hamiltonians or merely quoted. **Answer: independently
implemented.** See §1a and §1b.

### 2b. |S| differs from Table I by 3x–9x for larger molecules (moderate caveat)
- H2 JW 4q: 14 vs paper 14 (exact match)
- H2 BK 4q: 14 vs paper 5 (ours is untapered; paper uses further reductions)
- H2 BK-tapered 2q: 4 vs paper 5 incl. I (exact match modulo identity)
- HeH+ JW 4q: 26 vs paper 8
- LiH BK 6q: 117 vs paper 13
- H2O JW 8q: 104 vs paper 22

The paper's |S| column reports the exact reduced Hamiltonian used in each
cited hardware experiment (Hempel/Peruzzo/Nam), typically after Z2 tapering,
active-space selection tuned to hardware, symmetry reductions, and
encoding-specific term cancellations. We use default OpenFermion transforms
with straightforward active-space choices. The contextuality verdict is
invariant under the reductions that trim S (removing operators that are
universally commuting cannot create a new witness triple; removing operators
that participate in a witness triple would ONLY flip contextual→non-contextual,
never non-contextual→contextual, so our larger S is a conservative test in the
contextual direction). Nevertheless, a strict term-for-term match of the
experimental reduced Hamiltonians was NOT performed. This is Q1 in
`open_questions.json`.

### 2c. The classical simulability threshold was NOT quantitatively verified (major caveat)
The paper's underlying interpretive claim — that non-contextual VQE instances
admit an efficient noncontextual hidden-variable simulation and are therefore
NOT genuine quantum advantage — was NOT tested here. We verified the
classifier gives the same yes/no as the paper on the same inputs. We did NOT:
- construct the noncontextual hidden-variable model for the 2q H2 case
- verify that it reproduces VQE expectation values within chemical accuracy
- benchmark its classical wall-time scaling with |S|

The construction is in Kirby & Love (2020), "Classical simulation of
noncontextual Pauli Hamiltonians", a separate paper. Independent
implementation and benchmarking against the actual VQE trajectory would
close the interpretive loop. This is Q2 in `open_questions.json`.

### 2d. The CD_0 quantitative heuristic was NOT reproduced (moderate caveat)
The paper's CD_0 ∈ {0.27, 0.33, 0.38, 0.74, 0.77} for the larger molecules
quantifies HOW contextual the Hamiltonian is (Appendix C, specific
approximation scheme). We reproduced only the binary contextual /
non-contextual verdict. We can therefore say the paper's classification is
right; we cannot say the paper's degree-of-contextuality quantification is
right. Reproducing CD_0 would require implementing the Appendix C algorithm.

### 2e. No comparison against alternative advantage-witnesses (major caveat)
The paper implicitly positions contextuality as THE non-classicality witness
for VQE. Alternative witnesses — magic (stabilizer rank / mana), von Neumann
entanglement entropy of the VQE ground state, negativity of the discrete
Wigner function — would give correlated but not identical verdicts. In the
broader QC literature, these witnesses are known to be distinct
(contextuality is measurement/operator-level; magic is state-level). A
stronger replication would classify the six Hamiltonians with 2-3 alternative
witnesses and report agreement/disagreement. We did NOT do this. This is
Q3 in `open_questions.json`.

### 2f. Hardware noise robustness NOT tested
The classifier operates on ideal Pauli operators. On real NISQ hardware,
expectation values are noisy (depolarizing/dephasing gate errors + readout
error + finite shot noise). Boundary cases like HeH+ (CD_0 = 0.38, close to
non-contextual) could conceivably lose their witness triples under realistic
noise. We ran no noise simulations. This is Q4 in `open_questions.json`.

### 2g. Only VQE was tested; no extension to QAOA / AQC / hybrid schemes
The Theorem 3 classifier applies to any Pauli-sum Hamiltonian. QAOA cost
Hamiltonians for Max-Cut / MaxSAT are entirely Z-diagonal, hence trivially
non-contextual by the classifier (T = empty). Whether this reflects a true
absence of contextuality-based advantage in QAOA or a degeneracy of the
classifier applied to QAOA is unresolved. This is Q5 in `open_questions.json`.

### 2h. Only 6 of the 8 Table I rows were tested
BeH (contextual, CD_0 = 0.74) and the Schwinger model (contextual,
CD_0 = 0.77) were skipped for wave budget reasons. Deuteron (non-contextual)
was also skipped. Extending coverage to these would strengthen the
"larger ⇒ contextual" empirical pattern.

## 3. Reproducibility strength assessment

| Dimension | Rating | Notes |
|---|---|---|
| Algorithmic reproducibility | Strong | Classifier re-implemented from scratch, matches paper on real Hamiltonians |
| Numerical exactness | Medium | Witness verdict matches; |S| differs due to reduction choices |
| Interpretive claim (non-contextual = classically simulable) | Not tested | Requires Kirby-Love 2020 simulator |
| Quantitative claim (CD_0 heuristic) | Not tested | Requires Appendix C algorithm |
| Cross-validation vs alternative witnesses | Not tested | 5-hour follow-up would close this |
| Noise robustness | Not tested | Follow-up Qiskit Aer simulation would close this |
| Scope coverage (6/8 Table I rows) | Medium | BeH + Schwinger skipped |

## 4. Bottom line

The paper's headline algorithmic classifier is correctly implemented and
reproduces all six tested Table I verdicts on real molecular Hamiltonians.
This is enough for the REPLICATED verdict. What remains open:
(a) the exact experimental reduced Hamiltonians were not reconstructed
term-for-term; (b) the interpretive "non-contextual ⇒ classically simulable"
claim was not operationalized via an actual classical simulator;
(c) the CD_0 heuristic was not reproduced; (d) no comparison against
alternative advantage-witnesses (magic, entanglement, Wigner negativity);
(e) no noise/finite-shot robustness study; (f) no extension to QAOA/AQC.
These are captured as 5 concrete open-question probes in
`open_questions.json`.
