# Failure Analysis — quant-ph/9903071 (Mosca & Ekert 1998)

**Verdict was REPLICATED (9/9 checks pass), but this file honestly enumerates the friction, partial mismatches, assumptions, and residual gaps.**

## What actually failed / had to be worked around

### F1. Marker and Nougat parsers not installed on host
- **Symptom:** `which marker_single` and `which nougat` both return not-found on `CherryRd`.
- **Impact:** The REPLICATION_DIR_STANDARD_2026-07-05 requires `extraction/marker.md` and `extraction/nougat.mmd` as the canonical extractions.
- **Workaround:** Produced pdftotext-based fallbacks with an explicit banner in each file identifying it as a fallback. Central corpus for QC-200 not consulted (no manifest visible from this host).
- **Residual gap:** True Marker/Nougat parses (with math-aware LaTeX passthrough) would be higher-fidelity for this paper's inline math. The prose and section structure are captured; math expressions appear as ASCII glyphs.

### F2. Qiskit `QFT` circuit-library class is deprecated in 2.5.0
- **Symptom:** DeprecationWarning on both QPE circuit builders using `qiskit.circuit.library.QFT`.
- **Impact:** Functional; no result affected. The class still runs correctly.
- **Workaround:** Left as-is (behavior guaranteed until Qiskit 3.0). Migrating to `QFTGate` / `synth_qft_full` is a mechanical follow-up.

### F3. Naive comparison of Fourier-view vs shift-QPE-from-|0>
- **Symptom:** Direct comparison of `hsp_period_finding_distribution` (Fourier view) with `qpe_shift_distribution(target=|0>)` (QPE view) shows LARGE pointwise differences. Fourier view has support only on multiples of N/d; QPE from |0> has support on ALL bins.
- **Root cause:** The two are equivalent as *algorithms*, not as identical output distributions with default target-register preparation. Fourier-view already includes the coset-superposition-forming step (function oracle + partial trace). QPE with |0> does not.
- **Fix:** Ran the analytical comparison correctly by predicting the QPE output when the target register is prepared as a *coset superposition*, and showing that this matches the Fourier-view exactly. Both distributions verified to agree pointwise to `<1e-9` on Z_8 with d ∈ {2,4}.
- **Documented in:** REPORT.tex §7 and code comments.

### F4. Non-power-of-2 Z_N (N=6) required embedding in dim-8
- **Symptom:** The cyclic shift T on Z_6 is a 6×6 unitary; qiskit works on qubit registers of dim 2^k.
- **Workaround:** Embedded as an 8×8 matrix with identity on the extra 2 basis states (|6>,|7>). This does NOT change the eigenspectrum on the 6-dim subspace; measured phases are the 6 correct j/6 values (approximated on the k/64 grid).
- **Residual gap:** For strict compliance with the paper's "no wasted qubits" thesis, an amplitude-encoded implementation on a strictly log2(N)-qubit register would need a Grover-like preparation step; not attempted.

### F5. No continued-fractions post-processing
- **Symptom:** For Z_6 the shift-QPE outputs are k/64 not j/6. Recovery of the true j/N requires Shor-style continued fractions.
- **Impact:** We did not implement CF because the clustering was already unambiguous at n_count=6. For real HSP recovery on unknown N this would be required.
- **Documented in:** Open Question Q1.

### F6. Section 5 (single control qubit) not directly reproduced
- **Symptom:** The paper's §5 argues certain HSP instances need only one control qubit (Kitaev iterative QPE) or flying qubits.
- **Impact:** We verified the equivalent statement (coset-input QPE reproduces Fourier view) but did NOT build a Kitaev iterative circuit end-to-end.
- **Documented in:** Claim C5 marked "Partial"; Open Question Q2.

## What was NOT reproduced (out of scope)

- The paper's survey claim (C6) that the framework unifies factoring, discrete-log,
  order-finding, and Simon's problem is structural. We did not run Shor on a
  specific N or Simon on a specific f; those are separate replications (and
  covered by other QC-200 papers, e.g. quant-ph/0301141 for elliptic-curve Shor).
- No noise / decoherence sensitivity (Open Question Q5).

## What went smoothly

- Qiskit statevector semantics matched the paper's algebra exactly on the
  dyadic instances (φ=1/4, 1/8; Z_8 shift eigenphases; Z_8 period finding).
  No numerical fuss.
- Reusing the sibling QC-200 venv avoided any install friction.
- LaTeX compiled first try (no missing packages on this host).

## Assumptions made

- **Assumption 1:** QPE with `|1>` target on `diag(1, e^{2πiφ})` is exactly the
  paper's phase-estimation primitive (it is; textbook Kitaev/Nielsen-Chuang setup).
- **Assumption 2:** For Z_6 the embedding into an 8-dim register preserves the
  spectrum of interest (it does, since T is block-identity on the extra 2 basis
  states and their eigenvalues (1,1) do not lie in the target spectrum {e^{2πij/6}}).
- **Assumption 3:** Coset-input QPE and Fourier-view produce identical outputs
  when N is a power of 2 (verified analytically and numerically; this is the
  crux of the reduction).

## Would-need-to-close-gaps

- Install Marker + Nougat on CherryRd (F1) OR pull cached extractions from the central corpus.
- Implement the Kitaev iterative 1-control-qubit variant (F6 / Q2).
- Add CF post-processing for non-dyadic N (F5 / Q1).
- Sweep AQFT truncation levels for Z_N with N not a power of 2 (Q3).
- Add Qiskit Aer noise-model sweep to answer Q5.
