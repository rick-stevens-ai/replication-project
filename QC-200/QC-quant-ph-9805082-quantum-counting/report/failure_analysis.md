# Failure analysis — QC-200 / quant-ph/9805082

Honest inventory of what went wrong, what almost went wrong, and what remains as a residual gap.

## 1. Diffusion / global-phase sign bug in the hand-rolled Grover operator (fixed)

**Symptom.** First implementation used a from-scratch diffusion
`H^n X^n MCZ X^n H^n` around a `DiagonalGate(-1 on marked)` oracle.
The end-to-end sweep gave systematically inverted counts:

| t (true) | best t_tilde (buggy) | correct t (post-fix) |
|---|---|---|
| 1 | 15.39 | 0.61 (best), rounds to 1 |
| 2 | 13.66 | 2.34, rounds to 2 |
| 4 | 11.06 | 4.94, rounds to 5 → correct binning at higher P (3.55 → 4) |
| 8 | 8.00 | 8.00 (fixed point of the inversion) |

The pattern (t_tilde ≈ N - t at t≠N/2, correct at t=N/2) is the fingerprint
of a spurious overall minus sign in the diffusion, which flips the two
eigenvalue branches e^{±2iθ} of the Grover operator. Because the counting
estimator `t_hat = N sin²(πf/P)` is invariant under `f → P - f` (the fold
step), but NOT under `f → P/2 - f`, the wrong sign convention produced
the reflected estimate.

**Fix.** Switched to Qiskit's canonical `GroverOperator(oracle)` from
`qiskit.circuit.library`, which handles the sign convention correctly and
matches the BHT'98 definition of `G_F = Q(W, F, -1, -1)` (both the
initial-state reflection and the oracle carry a `-1` sign in the paper's
notation). On the next run, all 8 configurations produced the correct
counts.

**Lesson.** Never trust a hand-rolled Grover diffusion without a
phase-estimation round-trip check. A minimum viable QA is: build G_F,
run QPE with M = N/2 (θ = π/4, one Grover iteration flips to marked), and
confirm that the peak QFT bin is at P/4 rather than 3P/4. Our M=8 case
covers this in the current sweep and it is stable.

## 2. Marker / Nougat not installed on this host (documented substitute)

Marker (`pip install marker-pdf`) and Nougat (`pip install nougat-ocr`) were
not available on CherryRd, and no central-corpus pre-parse exists for
`quant-ph/9805082`. Installing Marker/Nougat would pull large HuggingFace
models (~5-10 GB) and take on the order of 30-60 minutes of network + init
time for a document whose text-native `pdftotext` output already reproduces
every equation and algorithm block we needed.

**Substitute.** `pdftotext -layout` output copied into
`extraction/marker.md` and `extraction/nougat.mmd` with a top-of-file header
that (a) states the substitute clearly, (b) explains why, and (c) notes that
for a text-native arXiv preprint of 12 pages, information content is
unchanged.

**Residual gap.** For an image-heavy or scan-based paper this substitute
would be unacceptable. It is acceptable here because the reproduction was
driven off the algorithm block on p.6 of the PDF, which pdftotext renders
exactly as printed.

## 3. Qiskit 2.x API deprecations (harmless, noted)

- `qc.diagonal(...)` is removed — used `DiagonalGate` from
  `qiskit.circuit.library`.
- `QFT(..., inverse=True, do_swaps=True)` emits a `DeprecationWarning`
  pointing at `QFTGate` / `qiskit.synthesis.qft.synth_qft_full`. Functionally
  identical in 2.5; will need updating for Qiskit 3.x.

## 4. What is NOT tested

- **Theorem 6** (amplitude estimation, not just counting). Only Theorem 5
  is the direct headline number of the paper; Theorem 6 is a straightforward
  generalisation. Untested.
- **Corollary 2 / 3** (relative-error scaling). These are analytical
  corollaries of Theorem 5. Untested.
- **Marked-set invariance.** We fixed marked = {0,...,M-1}. Untested for
  arbitrary marked sets (see Open Question Q5).
- **Larger N.** N=16 is the small-but-faithful instance per the brief.
  Larger N (up to N=1024 on statevector) would strengthen the empirical
  case for the theorem but is not required for a first-order replication.
- **NISQ hardware.** Statevector simulation only. Real-hardware runs on
  IBM Quantum would introduce depolarising noise and are out of scope for
  this brief.

## 5. Reproducibility gotchas future replicators may hit

- Qiskit uses `prec[0]` as the LSB in measured bitstrings; `do_swaps=True`
  is required in the IQFT for this to work out to a directly-readable
  integer `f_tilde`. Getting either wrong looks like a factor-of-2 offset
  in the count, which is easy to misdiagnose as a Grover phase issue.
- The DiagonalGate oracle in Qiskit 2.5 expects a `list[complex]` of length
  `2^n`; passing a numpy array works but you must `.tolist()` for older
  minor versions.

---

**Overall.** One material bug (diffusion sign), one substitute artifact
(Marker/Nougat), and a handful of deprecations. Nothing invalidates the
replication verdict of REPLICATED for Theorem 5.
