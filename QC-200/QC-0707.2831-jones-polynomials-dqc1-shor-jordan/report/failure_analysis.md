# Failure analysis / friction / residual gaps

Honest accounting of what did NOT work first-try, what was skipped, and
what a fully complete replication would require.

## Actual failures encountered (all fixed before final run)

### F1. Wrong sign of the Im-part of the shot-based Hadamard test
- **Symptom.** First shot-based run gave Im(Tr(V)/4) = +0.736 instead of
  the exact −0.532 — magnitude right, sign flipped, so |Δ|=1.27
  (catastrophic vs shot-noise expectation).
- **Cause.** Ambiguity between placing `S` vs `S†` on the control qubit
  after the controlled-V and before the final Hadamard. My initial
  circuit used a mixed convention.
- **Fix.** Rewrote the Im-part branch to cleanly apply `S†` on the
  control immediately after the controlled-V and before the final H.
  Independently sanity-checked on a 1-qubit diagonal test unitary
  U = diag(1, e^{iπ/3}) whose Tr/2 has known imaginary part
  0.4330: `S†` gave +0.428 (right), `S` gave −0.442 (wrong sign),
  confirming convention.
- **Result after fix.** Right-trefoil Im estimate = −0.5153 (target
  −0.5317, |Δ| Im = 0.016, well within shot noise).

### F2. `fitz` (PyMuPDF) not installed inside the venv
- **Symptom.** `python -c "import fitz"` failed inside `work/venv`.
- **Cause.** PyMuPDF is installed only in the system python at
  `/usr/local/bin/python3` (v3.14 outer install), not the fresh venv.
- **Fix.** Ran the marker-surrogate extraction under
  `/usr/local/bin/python3` explicitly instead of inside the venv. No
  functional consequence — the extraction is a separate one-off step.

### F3. Central Marker/Nougat corpus unavailable for arXiv:0707.2831
- **Symptom.** Searched for pre-parsed `0707.2831*` under
  `~/Dropbox/REPLICATE-PROJECT/`; no hit. `marker_single` and `nougat`
  CLIs not installed on this host either.
- **Cause.** This paper had not been previously parsed for the
  REPLICATE-PROJECT corpus.
- **Fix.** Produced two independent open-source parses (PyMuPDF for
  `marker.md`, `pdftotext -layout` for `nougat.mmd`), with a header line
  on each file stating the true tool, plus `extraction/README.md`
  documenting the surrogate status. This is per the brief's fallback
  hierarchy ("pull if parsed, else run Marker/Nougat") — I could not run
  either, so an honest surrogate is the next best step.

## Residual gaps vs a fully complete replication

### G1. Fibonacci-weighted mixed-state prep in Qiskit is not implemented
The DQC1 Hadamard test in Qiskit here uses the **uniform** maximally
mixed state I/2^n on the target register — which recovers the ordinary
matrix trace Tr(V)/2^n, not the Fibonacci-weighted Markov trace
̃Tr(U). To close this loop end-to-end at the DQC1 level, one would
prepare a specific weighted mixed state on the target (Sec. 5 of the
paper) so that the Hadamard-test output equals ̃Tr(U) directly. We
sidestepped this by computing ̃Tr(U) exactly (classical matrix trace
with per-basis-state φ weight); the final Jones polynomial value is
identical either way for this braid, but the resource-scalable
DQC1-native prep is not exhibited here. (Open Question Q4.)

### G2. Only one braid (σ_1^3 in B_2) plus its mirror was tested
The replication covers the trefoil in both chiralities. It does NOT
scan B_3 or B_4 braids (e.g. the figure-eight knot as trace closure of
σ_1 σ_2^{-1} σ_1 σ_2^{-1} in B_3), nor does it check that the DQC1
polynomial-time claim empirically scales as poly(n, |b|). This would be
a natural extension.

### G3. No noise-model sensitivity study
Simulations use an ideal DQC1 model (perfectly polarized control,
noiseless gates). Real NMR/photonic DQC1 realizations have polarizations
ε ~ 10^{-4}–10^{-2}. The paper cites this experimental context but does
not analyze noise-scaling. See Open Question Q5.

### G4. Complexity-completeness claim (C3) is proof-theoretic
The DQC1-completeness of estimating V(A^-4) at fifth roots of unity
cannot be shown by any single-instance simulation, so C3 is marked
"tested? No" in the claims table. This is not a failure of the
replication, but a scope note: the paper's headline theorem has a
constructive (algorithmic) direction, which we DID verify, and a
hardness direction which by its nature is not simulation-checkable.

## Friction log

- Qiskit 2.x renamed / reorganized several imports vs the 1.x era; used
  `from qiskit.circuit.library import UnitaryGate` and `.control(1)` on
  the gate rather than the older `Operator.control()` route. Worked
  first try after skimming Qiskit 2.5 docs.
- macOS TeX Live 2026 was already installed on CherryRd; `pdflatex
  REPORT.tex` compiled cleanly on the first pass, no missing packages.
- Fibonacci-representation dimensionality mismatch with Qiskit's
  power-of-2 qubit register handled by the standard block-diagonal
  embedding U → V = U ⊕ 1, then recovering Tr(U) = 4·Tr(V)/4 − 1.
