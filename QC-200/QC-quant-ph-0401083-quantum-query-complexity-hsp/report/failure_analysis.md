# Failure analysis — QC-200/QC-quant-ph-0401083

## What was NOT done, and why

### 1. Paper's `Test` and `ExactTest` unitary constructions were NOT implemented
The paper's `Test` operator (Section 2.1) is
```
Test_mu = Q_mu ⊗ P_{s,mu} + I ⊗ P_{s,mu}^⊥
```
where P_{s,mu} projects the s coset-state couplets onto the K_mu-coset subspace,
Q_mu is a per-subgroup register-swap+counter operator, and the whole thing is
compiled from per-subgroup Uμ (Kμ-superposition state prep) + Vμ (coset
translation) unitaries. Implementing this exactly requires:
- Enumerating all r subgroups K_1..K_r ordered by |K_μ| decreasing (we have this).
- Building each U_μ, V_μ as a (potentially exponential-size) explicit gate list.
- Applying Test_r ∘ ... ∘ Test_1 to |Ψ_init⟩ and measuring the first register.

We chose to substitute the **Pretty-Good Measurement (PGM)** for `Test`.
Rationale: PGM is operationally near-optimal (Barnum-Knill 2002:
`Pr_PGM_err ≤ 2 * Pr_opt_err`), which means PGM's success probability
*lower-bounds* Test's; consistency with the Theorem 2 bound follows.
This is a substantive replication choice and is why both judges (rightly)
called it PARTIAL/SPOT-CHECK rather than REPLICATED.

Implementing `Test` verbatim is a natural next step (see Open Question Q1)
but would have consumed the wave's time budget and produced an
implementation-level rather than information-theory-level check.

### 2. `ExactTest` + amplitude amplification (Section 2.2) was NOT implemented
The paper's exact algorithm needs the matrix inversion `M^{-1} y` (with y in
{1/4, 3/4}^r) to define per-subgroup ancilla rotations R_μ, then applies
amplitude amplification to boost {1/4, 3/4} to {0, 1}, then binary-searches
over Y^{3/4} vs Y^{1/4}. The `O(log^4 |G|)` exponent in Theorem 1 comes from
this pipeline. We did not test it.

### 3. Only groups of order 6 and 8 were tested
Larger groups (S_4 with |G|=24, S_5 with |G|=120) blow up N^s super-fast:
`24^4 = 331776` and PGM would need eigh on a 331776×331776 dense complex
matrix (~350 GB), infeasible on the sandbox. This is a fundamental limit of
the direct-simulation approach on a single machine and is called out in
Open Question Q2.

### 4. Marker + Nougat were NOT run natively
The QC-200 target dir standard requires `extraction/marker.md` and
`extraction/nougat.mmd`. Marker (`marker-pdf`) and Nougat both require a
torch + transformer-weights install (>1 GB download each) that was not
staged inside the QC-200 wave time budget. Following the QC-200 wave
convention already established in the sibling replication
`QC-quant-ph-0102014-nonabelian-hidden-subgroup/`, we substituted
pdftotext-based fallbacks with a clear header banner on each file so
downstream consumers know the provenance.

### 5. First-run OOM
The initial script version used `complex128` and included s=5 for S_3
(dim = 7776, 6 matrices ~967 MB each). RSS hit 1.7 GB and the run stalled
in the eigh call. Fix: switched all density matrices to `float64` (all
amplitudes are real non-negative in the group basis), capped s ≤ 4 for
all groups. Full run then completes in 110 s.

## Residual friction / minor issues

- **PGM slope on Z_2^3 (0.451 bits/query) is marginally below the paper's
  Theorem 2 slope of 0.500.** This is not a contradiction: PGM is
  near-optimal, not optimal, and the crossover into the asymptotic
  regime for a Z_2^3 with r=16 subgroups (many pairwise-distinguishable
  states) may lie beyond s=4. Both judges noted this and did not treat
  it as evidence against the paper. See Open Question Q1.

- **Theorem 2's numerical bound is vacuous for all (r,s) we can afford.**
  The bound `1 - 4r/2^(s/2)` becomes non-trivial only at `s >= 2 log2(4r)`
  ≈ 9-12 for our groups, whereas dense simulation caps out at s=4. This
  is characteristic of asymptotic bounds and doesn't invalidate the test;
  we test the *scaling* directly instead (log-slope fits).

- **No IEEE 754 exception in the eigh** despite regularising S at 1e-12:
  the coset density matrices are highly redundant (rank ≪ N^s for small
  s in a large-r problem), so S is genuinely rank-deficient. The
  regulariser holds, but it's worth noting that eigh's numerical
  determinism at rank-deficient boundaries is not guaranteed to be
  stable across numpy/LAPACK versions. All experiments here ran on
  numpy 2.x + Accelerate BLAS on macOS ARM64.

- **PDF-to-text loses the paper's math typography.** Both fallback
  extractions preserve character content but corrupt bold/italic
  distinctions in the operator names (e.g. `Test_μ` reads as
  `Test_µ` or `Testµ`). The math semantics are preserved for
  reasoners like Marker/Nougat but small readers should be aware.

## Nothing was fabricated
- Every number in the results tables is produced by the checked-in
  Python code with the seed `SEED=20260705`.
- The Monte-Carlo cross-check independently regenerates the confusion
  diagonals from shot-based sampling and matches analytic values within
  the Hoeffding 95% CI.
- Both judge outputs are the raw verbatim JSON returned by Argo, saved
  to `report/evidence/judge_panel.json`.
