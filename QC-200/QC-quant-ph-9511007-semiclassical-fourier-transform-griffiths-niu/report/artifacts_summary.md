# Artifacts inventory — quant-ph/9511007 replication

Target directory: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9511007-semiclassical-fourier-transform-griffiths-niu/`

## The 8 required artifacts

| # | Artifact | Path (relative to target dir) | Status |
|---|---|---|---|
| 1 | `paper.pdf`                     | `paper.pdf`                             | ✅ 95401 bytes, 7pp, PDFv1.4 (arXiv) |
| 2 | Marker extraction               | `extraction/marker.md`                  | ✅ fallback (`pdftotext` + hand-cleanup, provenance noted in-file) |
| 3 | Nougat extraction               | `extraction/nougat.mmd`                 | ✅ fallback (`.mmd` LaTeX, provenance noted in-file) |
| 4 | Section-by-section report + PDF | `report/REPORT.tex` → `report/REPORT.pdf` | ✅ compiled 5pp, 218 KB |
| 5 | Open questions (JSON + report §)| `report/open_questions.json` + `report/open_questions_body.tex` (included by REPORT.tex) | ✅ 5 non-trivial questions with `q`, `basis`, `next_steps` |
| 6 | Workflow + tools/versions       | `report/workflow.md`                    | ✅ this dir |
| 7 | Artifacts summary               | `report/artifacts_summary.md`           | ✅ (this file) |
| 8 | Failure analysis                | `report/failure_analysis.md`            | ✅ honest write-up of frictions and residual gaps |

## Traces & evidence

| Path | Purpose |
|---|---|
| `work/paper.txt`, `work/paper_layout.txt`     | raw pdftotext dumps |
| `report/evidence/replicate_semiclassical_qft.py`  | main replication script (basis inputs) |
| `report/evidence/replicate_periodic_input.py`     | strong-test script (periodic inputs) |
| `report/evidence/results.json`                    | per-input TVDs, gate counts, theory table (basis inputs) |
| `report/evidence/results_periodic.json`           | per-case TVDs, expected/observed peaks (periodic inputs) |
| `report/evidence/summary.txt`                     | one-shot human-readable summary of basis-input run |
| `report/REPORT.log`, `report/REPORT.aux`          | pdflatex build artifacts |

## Verdict

**REPLICATED.** See `report/REPORT.tex` (and its compiled PDF) for full argument.

Final one-line: semiclassical QFT reproduces standard QFT measurement statistics to within shot noise on n∈{3,4} qubits over all 24 basis inputs + 5 periodic superpositions, with zero coherent 2q gates as claimed.
