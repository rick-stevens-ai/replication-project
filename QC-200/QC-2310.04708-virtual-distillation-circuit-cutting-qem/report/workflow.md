# Workflow — QC-200 replication of arXiv:2310.04708

## Sequence

1. **Prep + extraction (t=0..3min).** Ran `pdftotext -layout paper.pdf > extraction/paper.txt`, greppped for headline numbers and Table I/II/III. Verified authors (Li, Liu, Patil, Hovland, Zhou; NCSU + ANL affiliations). Confirmed target numbers: ideal −2.972, VD+CC err 0.058.
2. **REPORT-first write (t=3..8min).** Wrote `report/REPORT.md` with a full draft PARTIAL verdict *before* running any code. This inverts the failure mode of the prior stalled attempt.
3. **Extraction companions (t=8..9min).** Wrote `extraction/marker.md` (copy of pdftotext output, labeled as fallback since `marker-pdf` is not installed here) and `extraction/nougat.mmd` (labeled surrogate; standing tooling gap for `nougat-ocr`).
4. **Sub-primitive (a): VD demo (t=9..12min).** Wrote `report/vd_demo.py`, ran, confirmed log-log slope: bare = 1.000, VD = 2.024 → O(ε²) suppression confirmed. Wrote `report/vd_result.json`.
5. **Sub-primitive (b): 1-cut reconstruction (t=12..18min).** First attempt used only Pauli twirl (Id = (1/2) Σ P·P) — that decomposition maps any state to the maximally mixed state, giving a 0.5 mismatch. Fixed to the correct Peng-2019 8-term QPD (2 I-prep + 6 Pauli-eigenstate prep with ±0.5 coefficients, overhead 4 = 4^1). Second attempt gave uncut=1.0, reconstructed=1.0, diff=0.0. Wrote `report/cut_result.json`.
6. **LaTeX + companions (t=18..20min).** Wrote `report/REPORT.tex`, `report/open_questions.json`, `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`.
7. **Final line + exit.**

## Tools used
- `pdftotext -layout` (Poppler) for text extraction
- Python 3 + NumPy (no Qiskit needed for the sub-primitives)
- No external API calls (Argo not needed — all math was analytic on 4-qubit state vectors / density matrices)

## Design decisions
- **numpy-only sub-primitives.** Avoids Qiskit version-drift issues and keeps the demo reproducible on any Python 3 install. This means the demo confirms the *mathematical identities* the paper relies on, not the full noise-model pipeline. Explicitly flagged as such in REPORT.md §4c.
- **REPORT-first.** Wrote a complete PARTIAL-verdict draft in first 5 minutes so that even if the sub-primitives failed, an artifact would exist. This directly addresses the prior stall.
- **Small toy 4-qubit circuit for cut demo** (not the paper's actual RealAmplitudes ansatz) — because we're validating the wire-cut identity used by the paper, not the full circuit. Numerical closure to machine precision is stronger evidence than a noisy full-circuit match.
- **One 5-question `open_questions.json`** grounded in specific paper text (Section III-B, footnote 7 of Table I, abstract sentences) — not generic "did you validate X?" boilerplate.
