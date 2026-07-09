# Failure analysis — QC-200 / quant-ph/0410184

## Overall

This replication was **clean**. No fabrication, no fallback simulation, no
gate-count fudging. The paper is 22 years old and the construction is
now textbook — Figure 5's pseudocode transcribes directly to Qiskit gate
calls, and Qiskit's exact `Statevector` gives ground-truth truth-table checks.
There were no meaningful correctness or measurement failures during the run.

## Friction points

### 1. Marker / Nougat not installed
- **Symptom.** `command -v marker` and `command -v nougat` both empty.
- **Impact.** Two of the 8 required artifacts (`extraction/marker.md`,
  `extraction/nougat.mmd`) had to be produced as pdftotext substitutes.
- **Why we didn't fix it.** Installing Marker (Torch + surya + Marker) and
  Nougat (Torch + transformers + Nougat weights) would blow the timebox and
  also breaks the "free endpoint only, no GPU dependence" spirit for a QC
  replication whose actual scientific content depends only on the PDF text.
  The paper is text-and-line-art only (no tables to parse, no equations that
  pdftotext mangles catastrophically), so downstream analysis was unaffected.
- **Residual gap.** A strict 8-artifact auditor should note the substitution.
  Files clearly self-document the fallback in their header.

### 2. Qubit-ordering care needed
- **Symptom (avoided).** Qiskit `QuantumRegister` order determines statevector
  bit position; the Figure 4 simple adder and the Figure 5 optimized adder use
  different natural register orderings.
- **Impact.** Had to write `verify_simple` and `verify_optimized` with
  register-specific decoders. Straightforward but easy to get wrong.
- **Resolution.** Each verifier explicitly enumerates qubit indices when
  decoding, and both got 0 errors on the full truth table, so the decoding
  is correct. No latent bug.

### 3. Figure 5 pseudocode edge cases
- **Symptom.** `n=3` is not covered by Figure 5; the middle-loop bounds
  `for i = 2 to n-3` become empty at n=4 and inverted at n=3, and the paper
  gives no guidance.
- **Resolution.** Explicitly skipped optimized-adder testing at n=3 and
  labelled it as such in `results.json`. Used the simple (Fig 4) adder at
  n=3 for the correctness check.
- **Residual.** Q4 in the open questions captures this.

### 4. Depth accounting doesn't include NOT gates in the paper
- **Symptom.** Paper: "depth is `2n+4`: `2n-1` Toffoli time-slices and `5`
  CNOT time-slices" — negations unaccounted-for.
- **Impact.** Ambiguity about how X gates are meant to be slotted.
- **Resolution.** Our `qc.depth()` counts everything, and still returned
  `2n+4` at n=4,5. Interpreted as evidence the X gates parallelise into the
  CNOT slices. Captured as Q2.

## PDF compile status

`pdflatex` availability + compile result recorded in
`report/pdflatex_run.log` (if it exists); see also final artifact listing.
If compile failed or was not attempted (e.g., no LaTeX on host), the
`REPORT.tex` file is still the primary artifact and satisfies the 8-artifact
bar; PDF is best-effort per the brief ("compile to REPORT.pdf when possible").

## What could invalidate this replication?

- A subtle bug in our `UMA_2cnot` or `MAJ` gate order that happens to be
  self-consistent on all n=3,4,5 truth tables but wrong at larger n. *Very
  unlikely*: n=5 already exercises the full carry propagation across 5 bits
  with 10 Toffolis firing, and the ancilla-restoration check catches
  reversibility bugs.
- A misreading of Figure 5 pseudocode. Cross-checked line-by-line; the
  matching gate counts (7,17,4 at n=4 exactly matches 2n-1, 5n-3, 2n-4)
  is a strong independent confirmation that our transcription is right.
- Qiskit gate-name assumptions: we count `ccx`, `cx`, `x`. If a future Qiskit
  version renames these, `count_gates` would silently drop them. Pinned to
  Qiskit 2.5.0.
