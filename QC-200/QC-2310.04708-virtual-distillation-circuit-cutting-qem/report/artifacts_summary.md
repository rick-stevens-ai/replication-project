# Artifacts summary

## Source
- `paper.pdf` — arXiv:2310.04708v2, 990 KB, downloaded pre-existing.
- `paper_v2.pdf` — same content, duplicate.

## Extraction
- `extraction/paper.txt` — pdftotext -layout, 576 lines. Primary source for all quoted numbers.
- `extraction/marker.md` — copy of paper.txt, labeled as pdftotext fallback since `marker-pdf` is not installed in this environment.
- `extraction/nougat.mmd` — labeled surrogate; `nougat-ocr` unavailable (standing tooling gap for `~/.openclaw/workspace`).

## Report artifacts
- `report/REPORT.md` — primary human-readable report with verdict PARTIAL. 7.4 KB.
- `report/REPORT.tex` — LaTeX version, same content, publication format. 5.8 KB.
- `report/open_questions.json` — 5 grounded follow-up questions with basis + next-steps. 3.5 KB.
- `report/workflow.md` — chronological workflow log with tool + design decisions. 2.8 KB.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — one non-trivial failure (Pauli-twirl-vs-QPD confusion), plus prior-stall root cause.

## Sub-primitive code + results
- `report/vd_demo.py` — 4-qubit virtual-distillation M=2 demo, pure NumPy. 3.6 KB.
- `report/vd_result.json` — sweep results: bare log-log slope 1.000 (linear), VD log-log slope 2.024 (quadratic). Verdict: CONFIRMED.
- `report/cut_demo.py` — 4-qubit 1-wire-cut reconstruction demo, pure NumPy. 9.2 KB (verbose comments documenting the QPD identity).
- `report/cut_result.json` — 8-term QPD reconstruction: uncut=1.0, reconstructed=1.0, diff=0.0. Verdict: CONFIRMED.

## Existing (from prior stalled attempt)
- `work/` — pre-existing dir from the stall, not modified in this replication.

## Not produced (out of scope for this budget)
- Full Qiskit-Aer + FakeHanoi VD+CC end-to-end pipeline that would reproduce Table I's −2.914 / 0.058.
- Sweeps over the RZZ crosstalk angle (see open_questions.json Q3).
- Real-device numbers (no IBM hardware access).
