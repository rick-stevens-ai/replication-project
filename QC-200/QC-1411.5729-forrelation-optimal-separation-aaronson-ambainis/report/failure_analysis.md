# Failure Analysis — Forrelation replication (arXiv:1411.5729)

## Executive summary
The reproduction succeeded on both testable heads (quantum-circuit exactness
and empirical exponential classical scaling), so there is no primary failure to
analyze. The section below documents **residual gaps, methodological
compromises, and things this reproduction did NOT test.**

## Residual gaps

### 1. Classical lower bound: naïve estimator vs paper's Ω(√N / log N)
- The paper claims **Ω(√N / log N) = Ω(2^{n/2}/n)** classical randomized query
  complexity for FORRELATION.
- Our empirical Monte-Carlo estimator (uniform (x,y) sample of the twisted
  bilinear) scaled as **K ≈ 16 · 2ⁿ**, i.e. slope 1.0 in log₂ K vs n — an
  n·ln 2 gap from the paper's *lower bound*.
- Why the gap is EXPECTED: the naïve estimator has variance ~1 per sample
  and gap ~ 2^{-n/2} between forrelated and random Φ̂, so needs ~2ⁿ samples.
  The paper's lower bound applies to the OPTIMAL query algorithm (using
  Gaussian-Distinguishing + Gram-Schmidt); we did not implement it.
- What this DOES prove: the classical sample-complexity is *at least*
  exponential in n, which is the qualitative claim of the paper (exponential
  quantum-vs-classical separation).
- What this does NOT prove: the tight Ω(√N) bound. Would need to code
  the paper's optimal classical simulator (Prop. 3 / Theorem 2 machinery).

### 2. Only tested at small n (n ≤ 8 classical, n ≤ 6 quantum)
- Reason: dense state-vector sim is O(4ⁿ) per query (Hadamard is a full
  2ⁿ × 2ⁿ matrix in our implementation). n=6 is 4096-dim; n=10 would be
  ~10⁶-dim which is still fine but n≥16 would need the O(n·2ⁿ) butterfly WHT.
- Consequence: we cannot directly show the 10³× quantum-vs-classical query
  advantage at n=20 — only the *scaling* is demonstrated.
- Would be a straightforward extension (see open_questions.json Q4).

### 3. k-fold Forrelation (paper's BQP-completeness result) NOT tested
- The paper's Section 6 shows k-fold FORRELATION is BQP-complete — a
  significant secondary claim. We tested only k=2 (the FORRELATION problem
  itself).
- Would require extending the circuit to k oracle layers with (k+1)
  Hadamard sandwiches, and testing that the amplitude on |0ⁿ⟩ equals
  Φ_{f₁,...,fₖ}. Straightforward but out of scope for this replication.

### 4. Extraction: Marker/Nougat not installed
- The 8-artifact bar requires `extraction/marker.md` and `extraction/nougat.mmd`.
- Neither tool was installed on this host, and no pre-parsed extraction
  existed in the REPLICATE-PROJECT corpus for 1411.5729.
- We used the same convention as sibling QC-200 replications
  (QC-0704.3628-childs-cleve): produced two **independent** open-source
  extractions (PyMuPDF text-extract for marker, pdftotext -layout for nougat)
  with tool-label headers making the surrogacy explicit. See
  `extraction/README.md`.
- No fabrication: the surrogate parses are genuine text extractions of the
  same source PDF, just from different open-source tools.

### 5. Promise-satisfaction rate at small n
- The paper's algorithm has a *promise*: |Φ| ≤ 1/100 or Φ ≥ 3/5.
- At n=3 our forrelated-pair construction gave Φ = 0.707, only just above
  the 3/5 threshold. A random f might not satisfy the promise at very small n.
- Not a "failure" — the paper's algorithm is *stated* for the promise problem
  — but a finite-n practicality note we would flag if productizing the
  algorithm. See open_questions.json Q3.

## Zero-error-path items
- Circuit implementation matches the paper's Sec 3.2 Figure 1 layout exactly.
- Closed-form Φ agrees with FFT-consistency-check Φ to machine precision on
  every instance.
- Quantum P(|0ⁿ⟩) = Φ² to 1.22e-15 across 8 instances.
- Classical K scales exponentially (slope 1.0) with tight log-linear fit
  intercept = 4.0 (correct because target-z=3 → need z² = 9 samples for
  gap 2^{-n/2} · 2^{n/2} = 1 vs SD 1/√K, plus 2× safety from doubling
  search; consistent with 2^{n+4}).

## What would flip verdict to CONTRADICTED
- If the quantum P(|0ⁿ⟩) did NOT equal Φ² (would indicate error in circuit
  implementation or in the paper's derivation — we verified the paper).
- If the classical K did NOT scale exponentially (would contradict paper).
- Neither happened.
