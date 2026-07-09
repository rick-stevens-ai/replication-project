# Failure analysis / friction / residual gaps

## What worked (no friction)

- **arXiv fetch** — one `curl` call; PDF was 220 kB and clean.
- **`pdftotext -layout`** — this is a math-heavy but text-dominant paper with no dense tables; the -layout dump preserved column structure well enough to identify Eqs. 4, 5, 6, 7, 11, 12 by eye in < 2 min.
- **Coppersmith → Qiskit transcription** — the paper's Eq. 7 is a textbook decomposition and maps 1:1 onto `qc.h(j); qc.cp(pi/2^(j-k), k, j)` for `j = n-1..0, k = j-1..0`. First-run code produced correct output.
- **Qiskit 2.5.0 install** — clean `pip install` into a fresh venv; no C-compilation issues.
- **All algorithmic verification** — every claim tested was reproduced to machine precision (worst ε = 5.6e-15).

## What didn't work / friction / gaps

### G1. Marker model weights not installed on replication host
The brief prefers a proper Marker parse. Marker pulls large ML weights (~2 GB); installing that transitive stack for a single 3-page PDF whose text layer was already clean would have been a time/disk overinvestment.
- **Mitigation:** used MarkItDown (pip package, no ML weights required) to produce `extraction/marker.md`. Content is faithful (equations rendered as their PDF text; PACS + author info + section text all present). Flagged explicitly at the top of the file.
- **Residual gap:** LaTeX equation reconstruction is coarser than what proper Marker/Nougat would give. Doesn't affect the replication outcome because we cross-verified against the paper directly, not the extraction.

### G2. Nougat model weights not installed on replication host
Same story — Nougat needs a GPU-hosted transformer model (`facebookresearch/nougat` ~1.3 GB). Not on this Mac.
- **Mitigation:** produced `extraction/nougat.mmd` as a hand-marked pdftotext dump with proper LaTeX math delimiters. Semantically Nougat-shaped, provenance-flagged at the top.
- **Residual gap:** not a real Nougat parse; would matter if a downstream corpus deduplicator relied on Nougat's ID-normalization.

### G3. Hardware claims (C5: F=87%, C6: >98%/gate) not tested
These are NMR spectrometer measurements. No 9.4 T alanine sample on the replication host.
- **Mitigation:** explicitly marked OUT-OF-SCOPE-BY-DESIGN in the report; not counted as MISMATCH.
- **Residual gap:** the reproducible open-system analog (T1/T2 open-system simulation via qiskit-aer's `thermal_relaxation_error`) would close a lot of the gap without needing hardware. Captured as open question Q1.

### G4. Bit-labeling ambiguity in paper Eq. 11 → Fig 1 assignment
The paper drops the SWAP by "reordering the bits at the appropriate interval" but doesn't print the permutation, so we can't reconstruct which of the six possible bit-permutations maps its A/B/C alanine C-13 spectra to Qiskit qubit indices 0/1/2.
- **Impact:** does not affect our correctness verdict (we verify against the analytic formula, which is a statement about the QFT as an abstract unitary and is invariant to which physical qubit gets which label). Would matter for a byte-for-byte reproduction of Fig. 1.
- **Captured as open question Q3.**

### G5. Missing check: approximate-QFT vs full-QFT tradeoff
Paper is not about approximate QFT; still, our clean n=3..5 ideal-statevector results made it obvious that the interesting modern question is "at what n does approximate QFT start to matter". Not tested here; captured as Q4.

### G6. No LLM-judge panel
Brief permits "3-judge Argo panel only if time remains; else self-verdict". Given the deterministic exact-arithmetic nature of the algorithmic verification (worst error 5.6e-15 out of unit-norm amplitudes; explicit paper-matrix agreement to 1.15e-16), the verdict is decidable without an LLM panel and no judge was invoked.
- **Residual gap:** no adversarial rereading of the report. Mitigated by the self-verifying nature of the numerical checks (any reader can re-run `qft_replication.py` in ~1 s and see the errors themselves).

## Confidence

- **C1, C2, C3, C4 verdict = REPLICATED:** high confidence. Errors are at machine precision; the code is short (~200 lines), single-file, and reproducible from a clean venv in one command.
- **C5, C6:** correctly labeled as untested, not fabricated.
