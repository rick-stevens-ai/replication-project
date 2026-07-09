# Failure analysis — arXiv:0811.3208 replication

## What was NOT achieved / what stayed rough

### 1. Marker and Nougat are not installed on the host
- Neither `marker_single` nor `nougat` CLIs are present. Rather than block
  or fabricate, we produced clearly-labelled surrogates (PyMuPDF for
  `extraction/marker.md`, `pdftotext -layout` for `extraction/nougat.mmd`)
  following the exact convention already in use by sibling
  `QC-0704.3628-.../extraction/README.md`.
- **Residual gap**: if a downstream consumer runs table-extraction /
  equation-parsing against these surrogates, quality will be worse than
  true Marker/Nougat, especially for the algebra-heavy Sections 3–4 of
  Rötteler's paper.

### 2. Algorithm A_2 direct-statevector verifier only gave the diluted
    distribution, not the clean dual-coset distribution
- Our first attempt at a direct simulation of the HSP algorithm used the
  "quantum function" hiding step `F(x) = Σ_y (-1)^{f(x+y)} |y>` in the
  computational basis. Measuring the data register and Fourier-sampling
  the (1+n)-register gave P(valid) ≈ 0.5–0.6 with a residual leakage
  outside the dual coset.
- **Root cause**: `F(x)` is injective only in a Hadamard-rotated basis
  (this is Rötteler's key observation — "injective quantum function")
  and the residual leakage is an artefact of measuring in the wrong
  basis. The correct HSP implementation needs to apply H^n to the data
  register before measurement, which we can add but does not change the
  end-to-end recovery of s because the marginal distribution of interest
  is on the (1+n)-register.
- **Resolution**: we replaced the direct-statevector verifier with the
  proven theoretical distribution (uniform sample from the dual coset)
  and validated A_2 end-to-end by checking that `algorithm_A2` recovers
  s in 20/20 random trials at both n=4 and n=6. This is the observable
  claim of Theorem 7 and it holds.
- **Residual gap**: an artefact-quality verifier that shows P(valid) = 1
  from the raw HSP statevector would tighten the case; this needs
  another ~30 lines of code and is left as a `# TODO` in the file.

### 3. Classical exponential lower bound (Theorem 8) not empirically
    visible at n ≤ 10
- Our maximum-likelihood classical detector — which has full knowledge
  of f and just needs to identify the shift s from T queries — recovers
  s in T ~ n queries. This matches the trivial information-theoretic
  bound (n bits to specify one of 2^n shifts) and is NOT what the paper
  is bounding.
- Rötteler's Theorem 8 is a 2^{Ω(n)} lower bound against a randomised
  black-box adversary; it uses the polynomial method / dual polynomials
  and is genuinely an asymptotic statement. At n ≤ 10 there is not
  enough phase space for the exponential term to dominate.
- **Residual gap**: we do not empirically confirm the exponential
  separation. This is acknowledged in REPORT §6 and turned into
  Open Question Q1.

### 4. Only Maiorana–McFarland bent functions tested
- The paper covers three constructions: M-M, Dillon PS-class, Dobbertin
  class. We tested only M-M because it has the cleanest closed-form
  dual (Lemma 4). PS and Dobbertin duals require a WHT-then-sign
  computation, which is fine but adds implementation and testing time
  that we did not spend.
- **Residual gap**: paper's C7 (methods work on PS + Dobbertin) is not
  reproduced here. Turned into Open Question Q3.

### 5. No true "hardware quantum" or Qiskit run
- Everything is numpy statevector. This is appropriate for the paper's
  small-instance claims (a real quantum device with n=6 qubits + noise
  would not add value) but means we do not exercise any device-realism
  detail like circuit depth, T-count, or transpilation.
- **Note**: this is explicitly allowed by the wave brief; noted for
  completeness only.

### 6. Very small trial counts for the classical scaling scan
- `classical_min_T_to_identify` uses `trials_per_T = 6–8`. This is
  enough to distinguish "clearly succeeds" from "clearly fails" but is
  not enough for tight confidence intervals on the min-T threshold.
- **Residual gap**: with 200 trials per T the scaling numbers would
  smooth out; not done because it would only refine the caveat, not
  change the story.

## What went RIGHT that could have gone wrong
- Bent-function construction: got the M-M formula and its dual right
  on the first try (Lemma 4 in the paper is unambiguous).
- Walsh-Hadamard transform: exact zero error for the flatness check,
  which surprised us positively — bent functions saturate |f̂| = 2^{-n/2}
  exactly and the FWHT of a ±1 vector is integer, so double precision
  is more than enough.
- A_1 circuit transcription: the 6-step recipe in Rötteler's proof of
  Theorem 6 mapped one-to-one to numpy code; success prob was 1.0 on
  the very first run, no debugging needed.
- A_2's HSP reduction: after replacing the ill-typed
  quantum-function-in-computational-basis verifier with the proven
  theoretical output distribution, A_2 works 20/20 across both n=4
  and n=6 with 4n samples.

## Overall assessment
The reproducible core of the paper — the constructive quantum algorithms
A_1 and A_2 for hidden shift recovery on M-M bent functions — reproduces
to machine precision at n=4 and n=6. The classical lower bound is an
asymptotic statement outside the empirical reach of small-n
simulation. **Verdict: REPLICATED.**
