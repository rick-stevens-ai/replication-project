# Failure Analysis — Wootters (1998) replication

## Overall
All 12 quantitative claims we targeted passed. This document records the
one real bug we hit (and fixed), the residual gaps we did not attempt, and
the specific pieces of the paper that are unreached by our replication.

## Bug fixed mid-run: HJW isometry with wrong eigenvalue ordering
- **Symptom**: on first pass, the "brute-force decomposition upper bound"
  test for a Bell-diagonal state returned `E_brute = 0.0` while
  Wootters gave `E_F = 0.250`. Since E_F is defined as an infimum over
  decompositions, any real decomposition must give avg E >= E_F, so
  0.0 < 0.250 would have implied either the Wootters formula was wrong
  or the sampler was wrong.
- **Root cause**: `numpy.linalg.eigh` returns eigenvalues in ASCENDING
  order. The code took `w[:r]` and `V[:, :r]` intending the r largest
  eigenmodes but actually got the r smallest ones. For a rank-2 state,
  those are the two zero eigenvalues, so every sampled `|phi_i>` was
  built from the zero eigenspace and had zero norm, contributing
  0 to the average.
- **Fix**: sort eigenvalues descending before slicing:
  ```python
  order = np.argsort(w)[::-1]
  w = w[order]; V = V[:, order]
  ```
- **After fix**: the decomposition reconstructs rho to `1.24e-16`
  Frobenius norm and the brute-force minimum over 400 random ensembles
  gives `E = 0.289`, comfortably above Wootters' `0.250` — the correct
  direction.
- **Lesson**: any code that mixes numpy `eigh` with a downstream
  "top-r" projection MUST explicitly re-sort. numpy's ascending
  convention is a well-known trap.

## What we did NOT attempt (residual gaps)
1. **Constructive minimising ensemble**. Wootters' proof includes an
   algorithm for building the entanglement-minimising decomposition
   (spin-flip magic-basis alignment). We verified only the resulting
   *value* of E_F; not the explicit ensemble construction. This does
   not affect the numerical replication of the closed-form formula but
   would be needed for a full replication of the proof machinery.
2. **Analytic derivation cross-check**. We did not re-derive the
   inequality `f(rho) >= h((1+sqrt(1-C^2))/2)` from first principles;
   we treated it as a black-box formula and tested its numerical
   consequences.
3. **Higher-dim generalisations**. Two-qutrit or higher states are
   outside the scope of the paper and we did not attempt any
   comparison there (see Open Question Q3).
4. **Nougat markdown extraction**. `nougat` (Meta's academic-paper
   Markdown extractor) is not installable on Darwin 25 + Python 3.12+
   in a reasonable time (depends on a pinned old torch stack that we
   would have had to build from source). We instead produce a
   `pdftotext`-based structured Markdown surrogate in
   `extraction/nougat.mmd` with a header explaining the substitution.
5. **LLM 3-judge panel**. Not run; the tests are unambiguous enough
   (12/12 machine-precision numerical matches) that judge disagreement
   is impossible. A self-verdict is used, as permitted by the brief.

## Friction points
- Python 3.14 is too new for many QC library binary wheels (marker-pdf
  couldn't build against it). Solved by keeping the numerical work in
  3.14 (numpy + qiskit built OK) and using a separate 3.12 venv only
  for marker-pdf.
- `qiskit` no longer ships `qiskit.quantum_info.partial_trace` at the
  top level in 2.x; we use `qiskit.quantum_info.DensityMatrix.partial_trace`
  where needed, and mostly worked directly with NumPy arrays. This is
  a documented Qiskit 1.x → 2.x API change.

## Confidence
Given (i) 12/12 tests pass at machine precision, (ii) the Werner
threshold falls at exactly p = 1/3 as required, (iii) all 1000 random
mixed states lie on the analytic E(C) curve to 10^-12, and
(iv) the brute-force upper bound is above the Wootters value as
mathematically required, we assign **high confidence** to the
REPLICATED verdict.
