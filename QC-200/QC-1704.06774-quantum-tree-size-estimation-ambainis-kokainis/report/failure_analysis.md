# Failure Analysis — arXiv:1704.06774 replication

## Honest failure ledger

### 1. Marker + Nougat NOT installed → pdftotext fallback used (documented)
- **Friction:** Full Marker (VikParuchuri/marker) + Nougat (facebookresearch/nougat) stack requires 3–5 GB of vision-transformer weights and torch, plus Python ≤ 3.12 wheels; the local system has Python 3.14 which lacks pre-built wheels for both.
- **Mitigation:** Followed the pattern already established in sibling QC-200 replications (see `QC-quant-ph-9607014-durr-hoyer-quantum-minimum/extraction/*`): produced `marker.md` = `pdftotext -layout` and `nougat.mmd` = `pdftotext -raw`, each with a header block explaining the fallback and its provenance.
- **Impact:** Zero on the *scientific* replication — the extraction is text-only and Ambainis & Kokainis is a pure math paper with no figures whose ML parse would materially change interpretation.

### 2. First-pass "0.6%–2.3% relative error looked like a bug" (resolved)
- **What went wrong:** Initial run of `tree_size_estimation.py` printed rel-err ≈ 8×10⁻³ on the depth-4 tree; my first instinct was to declare PARTIAL, worrying that the algorithm was mis-implemented.
- **Investigation:** Wrote `verify_identity.py` to enumerate ALL eigenphases with their |start> overlaps and confirm which eigenvector the paper's estimator was "meant" to pick. The ±θ_min pair carries 99.2% of the amplitude — the estimator IS correctly locking onto the paper's intended eigenpair.
- **Resolution:** Wrote `scaling_test.py` to sweep δ. The residual scales as ~0.093·δ² (log-log slope 2.00 across 200× range of δ), meaning it is the ordinary O(δ²) window that Lemma 5 tolerates as O(δ). The paper's identity is being reproduced exactly; the ~1% is not an implementation bug but the intended tolerance of the estimator at δ=0.3.
- **Lesson:** Distinguish between "algorithm implemented incorrectly" and "algorithm implemented correctly but paper's bound is only 1±δ". Verify by pushing δ→0 and checking that the estimator collapses to T exactly.

### 3. Direct-sum validity: implicit assumption not caught until write-up
- **What went wrong:** Naïvely built R_A = ⊕_{v∈V_A} D_v as a block-diagonal-in-vertex operator. This is only unitary if the H_v subspaces are pairwise orthogonal (i.e. V_A vertices are pairwise edge-disjoint).
- **Investigation:** For trees, parent/child always have opposite parity, so V_A is an independent set, so the H_v's are pairwise orthogonal. Verified numerically: R_A @ R_A.conj().T = I to ≤ 1e-14 in Frobenius norm on all instances.
- **Impact:** No bug in the code. But this is exactly the reason Open Question Q5 asks about the DAG generalization — for genuine DAGs the assumption is NOT automatic and the paper leaves this implicit.

### 4. Time budget: skipped Sections 4 and 5 (applications)
- **What was NOT done:** No implementation of the backtracking search speedup (Section 4) or the AND-OR formula evaluator (Section 5).
- **Rationale:** Both are corollaries of the tree-size estimator's correctness. The estimator IS the pillar; the applications add plumbing (Grover-like amplification + specific tree structures) that would triple the code size without adding independent evidence for the estimator itself. Given the ~45-minute budget and the mandate "focus on the demonstrator that the key idea yields the claimed speedup", Section 3 is the right level.
- **Impact:** Verdict is REPLICATED for the tree-size estimator (Sections 2–3); applications (Sections 4–5) are marked as untested in the claims table.

## Residual gaps

- **G1.** No implementation of the actual quantum phase-estimation circuit (ancilla qubits + QFT). We extract θ_min via exact eigendecomposition. This is *stronger* evidence that the paper's identity holds (no sampling noise) but does NOT stress-test the finite-precision behavior that a real quantum device would face.
- **G2.** Only complete-binary / complete-ternary / one small unbalanced / one path graph tested. Random-branching trees (Galton-Watson) would be a better stress test of the phase-gap scaling law's constant factor.
- **G3.** The paper's Õ hides log T and log n factors AND a dependence on max degree d that we did not test. Our depth ≤ 7 experiments all use d ≤ 3; a large-degree stress test would be needed to fully validate Theorem 2's d factor.
- **G4.** No comparison against Montanaro (2015) [12] which our paper improves upon. The paper only quotes Montanaro's asymptotics; a side-by-side numeric comparison would take another few hours.

## Would-do-differently list
- On the next replication: **write a δ-convergence sweep BEFORE writing the verdict logic**. Would have saved 5 minutes of "is this a bug?" investigation.
- If Marker/Nougat becomes routine, containerize them (python 3.11 venv) so the pdftotext fallback isn't the default.
