# Artifacts Summary — QC-200 replication of arXiv:2401.06240

## Directory tree
```
QC-2401.06240-quantum-eigenvalue-processing-low-su/
├── paper.pdf                          [1] original arXiv PDF
├── extraction/
│   ├── marker.md                      [2] pdftotext -layout fallback (8082 lines)
│   └── nougat.mmd                     [3] pdftotext -raw fallback (13306 lines)
├── report/
│   ├── REPORT.tex                     [4] main LaTeX report (with verdict)
│   ├── REPORT.pdf                     [4] compiled PDF (if pdflatex succeeded)
│   ├── open_questions.json            [5a] 5 heavy-duty open questions (machine-readable)
│   ├── open_questions_include.tex     [5b] TeX \input for REPORT.tex (\section*)
│   ├── workflow.md                    [6] workflow + tool versions + effort
│   ├── artifacts_summary.md           [7] THIS FILE — inventory
│   ├── failure_analysis.md            [8] honest friction log
│   └── evidence/
│       ├── qsvt_sign_replication.py      main replication script (~15 KB)
│       ├── qsvt_results.json             all per-experiment numerics
│       ├── qsvt_summary.txt              short text summary
│       ├── qsvt_sign_response.png        response-function figure (3 subplots)
│       └── response_plot.py              figure-generation script
└── work/
    ├── venv/                          Python 3.14 virtualenv (qiskit/numpy/scipy/pyqsp/matplotlib)
    ├── paper.txt                      raw pdftotext (15232 lines)
    ├── paper_layout.txt               pdftotext -layout (8069 lines)
    ├── paper_raw.txt                  pdftotext -raw (13294 lines)
    ├── debug_convention.py            scalar-N=1 sanity check vs. pyqsp
    └── debug2.py                      Chebyshev-interpolant convention debug
```

## Coverage of the mandatory 8-artifact bar
1. `paper.pdf` — PRESENT (1.4 MB, 11 pages, arXiv 2401.06240v3)
2. `extraction/marker.md` — PRESENT (pdftotext-layout fallback, with header disclaimer)
3. `extraction/nougat.mmd` — PRESENT (pdftotext-raw fallback, with header disclaimer)
4. `report/REPORT.tex` — PRESENT (~12 KB, verdict + detailed method + results)
5. `report/open_questions.json` — PRESENT (5 objects with q/basis/next_steps)
    + `## Open Questions` section in REPORT.tex via `\input{open_questions_include.tex}`
6. `report/workflow.md` — PRESENT (workflow + tool versions + work estimate)
7. `report/artifacts_summary.md` — PRESENT (this file)
8. `report/failure_analysis.md` — PRESENT (three concrete failure modes documented)

## Evidence traces
All numerical results in the REPORT are backed by:
- `report/evidence/qsvt_results.json` — verbatim JSON dump of every
  per-experiment number (phases, per-eigenvalue expected vs. obtained
  polynomial values, absolute errors), timestamped and versioned.
- `report/evidence/qsvt_sign_replication.py` — deterministic main
  script; re-running with the pinned venv reproduces the JSON exactly.
- `report/evidence/qsvt_sign_response.png` — visual sanity plot.
- `work/debug_convention.py` — evidence that our qsvt_unitary matches
  pyqsp's own `SymmetricQSPProtocol.gen_unitary` at machine precision
  (independent implementation check).

## Verdict propagation
Main verdict: **PARTIAL / SPOT-CHECK** — the Hermitian-reduction of
QEVT (which the paper itself explicitly identifies as coinciding with
QSVT) is reproduced at machine precision on a small block-encoded H.
The full non-Hermitian QEVT/QEVE machinery is not exercised.
