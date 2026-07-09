# Artifacts summary — QC-1711.11336 (Portugal 2017)

## Directory layout
```
QC-1711.11336-element-distinctness-revisited-portugal/
├── paper.pdf                           (arXiv:1711.11336v3, 14 pp, 184 425 B, PDF 1.4)
├── extraction/
│   ├── README.md                       (documents pdftotext fallback)
│   ├── marker.md                       (pdftotext -layout output; marker not installed)
│   └── nougat.mmd                      (identical to marker.md; nougat not installed)
├── work/
│   ├── paper.pdf                       (original download)
│   └── paper.txt                       (pdftotext -layout extraction)
└── report/
    ├── REPORT.tex                      (LaTeX source, 8 sections + open-Qs)
    ├── REPORT.pdf                      (compiled: 8 pp, 317 901 B)
    ├── workflow.md                     (this-run tools/versions/commands)
    ├── open_questions.json             (5 open Qs, each {q, basis, next_steps})
    ├── artifacts_summary.md            (this file)
    ├── failure_analysis.md             (honest gaps & friction log)
    └── evidence/
        ├── replicate_portugal.py       (u_alpha/u_beta/R/psi_0 + sweep; deterministic seed 20260705)
        ├── make_plots.py               (log-log Q vs N + p_succ vs N)
        ├── replicate_portugal.log      (stdout of the sweep)
        ├── results.json                (full sweep + classical baseline + slopes)
        ├── sweep.csv                   (compact CSV: N, r, t1, t2, Q, p_succ, ...)
        ├── portugal_replication.png    (figure, 140 dpi)
        └── portugal_replication.pdf    (figure, vector)
```

## Provenance & hashes
- Source PDF: `sha256=d3a036b6f68569555347abfcaa33150c59c38d82995259742a21b6147de48de4` (paper.pdf and work/paper.pdf, identical)
- Results: `sha256=98e8d238acc83040ef4ab60bc1a42e6ba0d0c6145746e81cd95a5d131d53b7b3` (results.json)
- Figure: `sha256=8150cf7cc4b04743490b518a61d2b67b5699d4fae642f46bd80556de9c2dbb4c` (portugal_replication.pdf)
- Report: `sha256=eb307fcfcdeb9812dc61d112f2492e057a86398bdcc9299f4cd760f4957bbd60` (REPORT.pdf)

## 8-artifact QC wave-brief bar

| # | Required | Present? | Path |
|---|---|---|---|
| 1 | `paper.pdf` | ✓ | `paper.pdf` |
| 2 | `extraction/marker.md` | ✓ (pdftotext fallback, documented) | `extraction/marker.md` |
| 3 | `extraction/nougat.mmd` | ✓ (pdftotext fallback, documented) | `extraction/nougat.mmd` |
| 4 | `report/REPORT.tex` (compiled if possible) | ✓ + compiled `REPORT.pdf` | `report/REPORT.tex`, `report/REPORT.pdf` |
| 5 | `report/open_questions.json` (5 heavy items) + `## Open Questions` in report | ✓ (5 items, each with `q`/`basis`/`next_steps`) + Section 7 of REPORT.tex | `report/open_questions.json` |
| 6 | `report/workflow.md` (comprehensive workflow + tools/versions + effort) | ✓ | `report/workflow.md` |
| 7 | `report/artifacts_summary.md` (inventory) | ✓ | `report/artifacts_summary.md` |
| 8 | `report/failure_analysis.md` (honest friction/gaps) | ✓ | `report/failure_analysis.md` |

## Evidence trail for the REPLICATED verdict

- **Reduced-subspace matrices** verified unitary AND Hermitian to machine precision (max `||A A^T - I||_∞ = 2.2e-16`, max `||B - B^T||_∞ = 0`). Confirms Theorem 3.1's invariant-subspace claim.
- **Log-log slope of Q vs N**: fitted = **0.6646**, theory = 0.6667. Below the wave brief's threshold of `slope ≈ 2/3` — satisfied.
- **Classical baseline**: brute-force collision search recovers the planted (i,j) pair in all 3 requested small-N instances (N=6, 9, 12).
- **Success probability**: monotonically approaches 1 (0.556 at N=6 → 0.975 at N=3000), consistent with Portugal's improved 1 - O(r^{-1/k}) bound vs Ambainis' 75% asymptote.
- **Reproducibility**: single-file numpy program, deterministic seed 20260705, <1 s wall time, no LLM calls, no GPU, no network access beyond the initial arxiv fetch.
