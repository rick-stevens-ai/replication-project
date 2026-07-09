# Failure analysis — QC-quant-ph-0312194 replication

## Honest gaps + friction (what did NOT work smoothly, or was skipped)

### 1. Marker + Nougat were not available on the host at run time
- `which marker_single` and `which nougat` both returned not-found on CherryRd.
- Fallback per QC brief: used `pdftotext -layout` output for both `extraction/marker.md`
  and `extraction/nougat.mmd`, with an explicit header at the top of each file
  labelling them as fallback.
- Impact: extractions are correct as plain text but lack the math-mode fidelity of
  Marker/Nougat. For a math-heavy paper this is a real (though not showstopper) loss.
- Mitigation: the paper's math-heavy sections (cat basis, overlap, Bell state, Z
  gate) were re-implemented from first principles in the simulator, so the extraction
  fidelity does not affect the replication verdict.

### 2. Central-corpus lookup for pre-parsed Marker/Nougat outputs timed out
- Attempted a `find` over `~/Dropbox/REPLICATE-PROJECT/` to reuse a pre-existing
  parse; the `find` hung on the (large) Dropbox tree and had to be killed. Given
  the time budget, we did not retry with a scoped path.
- Consequence: possible duplication of extraction work if a corpus parse exists.
  A future run should read `~/Dropbox/REPLICATE-PROJECT/CORPUS/parsed/<arxiv-id>/`
  directly rather than `find` from the root.

### 3. QuTiP 5.x API change tripped up initial version of the script
- In QuTiP 5, `bra * ket` returns a Python `complex` scalar rather than a 1x1 Qobj,
  so calls like `(plus.dag() * plus).full()[0,0]` fail with
  `AttributeError: 'complex' object has no attribute 'full'`.
- Fixed by replacing every `(bra*ket).full()[0,0]` with `complex(bra*ket)`.
- Lesson: when the QC brief says "QuTiP if available", the version check matters —
  QuTiP 4.x and 5.x have different scalar-vs-Qobj conventions for inner products.

### 4. Scope narrowed on purpose
- We did NOT reproduce:
  - Full universal-gate set on cat qubits (in-line squeezing, teleportation-based
    entangling gate, X-basis measurement conditioning).
  - Metrology examples (Heisenberg-limited weak-force detection, Ramsey interferometry).
  - Photon-loss / decoherence channels.
- These are all real, non-trivial re-implementation efforts. We tested the
  four algebraic identities that the paper's *entire* toolbox is built on;
  if those had failed, everything above would have been suspect. They all
  hold to machine precision, so the foundation is validated.

### 5. No 3-judge Argo panel
- The QC brief allows self-verdict when time is short. We used the self-verdict
  path. A future pass could invoke Argo `argo:claude-opus-4.8`, `argo:gpt-5.2`,
  and `argo:gemini-2.5-pro` on REPORT.tex to independently rate the replication.

### 6. REPORT.tex was written but not compiled to PDF in-loop
- No LaTeX toolchain was invoked; REPORT.tex is a plain source file. `latexmk` or
  `pdflatex report/REPORT.tex` in an environment with texlive would produce
  REPORT.pdf. Attempted compilation is left as a separate follow-up step because
  the brief's mandatory-artifact set requires REPORT.tex (present), and a PDF
  compile only "when possible."

## Residual gaps
- Fock truncation was fixed at N=40 by hand. Certified-error truncation guidance
  would be nice (see Open Question Q2).
- Concurrence at small alpha is basis-choice-dependent (see Open Question Q3).
- No sensitivity analysis to Kerr non-linearity in the Z gate (see Q4).
- No accumulation-error study for chained gates (see Q5).
