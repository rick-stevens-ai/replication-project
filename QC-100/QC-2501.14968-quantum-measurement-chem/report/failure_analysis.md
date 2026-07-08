# Failure Analysis / Honest Critique — QC-2501.14968

Paper: Patel, Jayakumar, Yen, Izmaylov, *Quantum Measurement for Quantum
Chemistry on a Quantum Computer*, arXiv:2501.14968 (2025).
Verdict: **REPLICATED** (with the caveats below).

This document is deliberately hard on the replication. It exists so that
downstream readers do not overclaim what was actually verified.

---

## 1. The paper is a review, not a primary result

**Fact:** arXiv:2501.14968 is explicitly a review/tutorial article. The
abstract and intro state that it "emphasizes foundational concepts and
methodologies rather than numerical benchmarks." It contains essentially
no original quantitative benchmarks with associated data tables.

**Consequence for the replication:**
- There is no specific figure or table to reproduce.
- The most concrete quantitative statement it makes on its own authority is
  the **variance-decomposition Eq. 63** (a textbook CLT identity for
  Hamiltonian-partitioned estimators).
- The "2–4× grouping" statement is a **claim it quotes** from Crawford et al.
  and related sorted-insertion work, not a claim it derives afresh.

**Honest framing.** We reproduced the review's *analytical spine* on H2 and
LiH from scratch, and independently obtained a 3.03× QWC reduction for LiH
that lands inside the quoted 2–4× window. This is a real numerical check
(not a citation restatement), and the paper's central claims survive it —
but it is a narrower verification than what "REPLICATED" would mean for a
primary-benchmark paper.

## 2. Was the measurement scheme independently reimplemented?

**Yes, from scratch.** We:
- Built molecular Hamiltonians via PySCF (not from a canned qiskit-nature
  demo).
- Applied Jordan–Wigner mapping and enumerated Pauli terms independently.
- Ran greedy graph coloring for both QWC and FC (`measurement_grouping_v3.py`).
- Computed per-fragment variances Var(H_α) = ⟨H_α²⟩ − ⟨H_α⟩² directly.
- Assembled `M_opt = (Σ √Var_α)²` end-to-end.

The pipeline is not a wrapper around a library that already returns these
numbers.

## 3. Was the sample-cost / MSE-per-shot reproduced for the paper's specific molecule vs. quoted?

**Partially.**
- The paper does not itself table a specific molecule/shot-cost pair as its
  own result; it *quotes* prior work. Our LiH figure (3.03× QWC) reproduces
  the *magnitude* of the quoted 2–4× claim on the standard reviewer's
  benchmark molecule (LiH/STO-3G), which is the closest we can get to a
  like-for-like check.
- We did **not** re-derive Crawford et al.'s original tabled numbers on
  their exact molecule set; we re-derived the *class* of result on our
  standard benchmark and confirmed it lives in the quoted window.

## 4. Was the comparison against naive single-Pauli-per-shot baseline made?

**Yes.** "Ungrouped" in our tables is exactly single-Pauli-per-shot with
sqrt(Var) allocation — this is the reference against which QWC and FC are
compared. It is also the paper's explicit reference. The 3.03× / 53.8×
figures are ratios to this baseline.

**What we did NOT compare against:** locally-biased classical shadows,
derandomized shadows, unitary partitioning, symmetry-adapted groupings, or
low-rank factorization of the Hamiltonian. These are also reviewed in the
paper but are not part of the specific "grouping vs. naive" claim we
checked. (See Open Question 2.)

## 5. Did the sample-cost reduction hold quantitatively?

**Yes on LiH (the non-trivial system). No on H2 (correctly).**
- LiH QWC 3.03× — inside 2–4× window.
- LiH FC 53.8× — well beyond QWC (matches "FC > QWC" claim).
- H2 QWC 1.00× — **null result** — but this is *physically correct*: with
  only 15 Pauli terms and 4 qubits, the optimal-allocation bound is already
  near-saturated at the ungrouped level, so grouping cannot beat it. The
  review's 2–4× is a large-N property; H2 is not large-N.
- Monte-Carlo on H2 showed a modest 1.2–1.6× benefit at finite shots
  (weaker than the analytical claim, as expected when the ceiling is 1×
  in the optimal-allocation limit).

## 6. Known limitations and non-verifications

1. **Ground state, not VQE-ansatz state.** All variances computed at the
   exact diagonalized ground state, not at a parameterized trial state near
   a VQE minimum. Real VQE variance surfaces can differ.
2. **STO-3G minimal basis, 2 molecules.** No claim about scaling to
   cc-pVDZ / larger active spaces / strongly-correlated systems.
3. **Greedy graph coloring, not optimal.** Fragment counts and M_opt are
   upper bounds on what an optimal coloring would achieve.
4. **No hardware or noise model.** Statevector only. The FC>QWC advantage
   could invert on noisy hardware because FC groups require Clifford
   diagonalization circuits.
5. **MC cross-check only on H2.** LiH's analytical M_opt was not
   corroborated by finite-shot simulation (LiH statevector sampling was
   deemed too expensive for the 200-repeat MC loop within this budget).
6. **Reviewed methods not implemented:** classical shadows, derandomization,
   unitary partitioning, symmetry-adapted groupings. Only the grouping
   spine was reimplemented.

## 7. Bugs found and disclosed

- **LiH variance script v1/v2**: array-contiguity issue in the FC-fragment
  variance loop produced NaN for a subset of fragments. Fixed in v3.
  Final numbers come exclusively from `grouping_summary_v3.json`.
  Disclosed in REPORT §Assessment.

## 8. What would flip the verdict to PARTIAL

If a downstream check showed any of the following, the verdict should be
downgraded:
- The 3.03× LiH QWC number is a coloring-heuristic artifact and drops
  outside 2–4× under a different (optimal or alternative-greedy) coloring.
- FC>QWC inverts once realistic noise is included on hardware.
- The ground-state → VQE-ansatz transition breaks the M_opt ordering on
  LiH.

None of these were tested here.

## 9. Bottom line

**Verdict preserved: REPLICATED.** The paper's central quantitative claims
(Eq. 63, optimal-allocation metric, 2–4× grouping reduction, FC>QWC) were
independently reproduced on H2/LiH from scratch, with the LiH QWC figure
landing inside the reviewed 2–4× window. The reproduction is narrower than
the paper's full survey scope; readers should not overclaim that every
methodology in the review has been re-tested here.
