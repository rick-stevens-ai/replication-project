# Artifacts summary — QC-200 / quant-ph/0011067 replication

Complete inventory of every artifact in this directory, with provenance
and brief description.

```
QC-quant-ph-0011067-shifted-quadratic-character-vandam/
├── paper.pdf                                (1) original arXiv PDF
├── extraction/
│   ├── marker.md                            (2) surrogate Marker parse
│   └── nougat.mmd                           (3) surrogate Nougat parse
├── report/
│   ├── REPORT.tex                           (4) full replication report
│   ├── workflow.md                          (6) commands + versions log
│   ├── artifacts_summary.md                 (7) this file
│   ├── failure_analysis.md                  (8) honest gap analysis
│   ├── open_questions.json                  (5) machine-readable open Qs
│   └── evidence/
│       ├── shifted_legendre_algo.py         Algorithm 1 exact simulation
│       ├── shifted_legendre_results.json    105-instance sweep results
│       ├── classical_lower_bound.py         3 classical attacks
│       └── classical_lower_bound_results.json  sweep + correlations
└── work/
    ├── paper.pdf                            (dup of top-level paper.pdf)
    └── paper.txt                            pdftotext dump (1185 lines)
```

## 8-artifact completion checklist (per QC wave brief, Rick 2026-07-05)

| # | Required artifact | Location | Status |
|---|---|---|---|
| 1 | `paper.pdf` (original) | `./paper.pdf` (& `./work/paper.pdf`) | ✅ 173 KB, van Dam+Hallgren verified from PDF header |
| 2 | `extraction/marker.md` | `./extraction/marker.md` | ✅ surrogate (marker not on host; preamble discloses) |
| 3 | `extraction/nougat.mmd` | `./extraction/nougat.mmd` | ✅ surrogate (nougat not on host; preamble discloses) |
| 4 | `report/REPORT.tex` | `./report/REPORT.tex` | ✅ full section-by-section report with **VERDICT: REPLICATED** |
| 5 | `report/open_questions.json` + `## Open Questions` section | `./report/open_questions.json` + REPORT.tex §Open Questions | ✅ 5 questions, each `{q, basis, next_steps}`, grounded in this replication |
| 6 | `report/workflow.md` | `./report/workflow.md` | ✅ commands, tool versions, work estimate |
| 7 | `report/artifacts_summary.md` | `./report/artifacts_summary.md` | ✅ this file |
| 8 | `report/failure_analysis.md` | `./report/failure_analysis.md` | ✅ honest gaps + friction |

## Evidence traces

| File | Bytes | Content |
|---|---|---|
| `report/evidence/shifted_legendre_algo.py` | 5.7 KB | Full Alg 1 exact-QFT numpy implementation (single file, no deps except numpy) |
| `report/evidence/shifted_legendre_results.json` | ~20 KB | Per-instance measurement outcomes for 105 instances (p=13,31,61 × all s) |
| `report/evidence/classical_lower_bound.py` | 8.7 KB | 3 distinguisher-based attacks with docstring math |
| `report/evidence/classical_lower_bound_results.json` | ~5 KB | Sweep results: k*, marginal SNR, exact correlations |
| `work/paper.txt` | ~65 KB | Full paper as UTF-8 text (from pdftotext) |

## Verdict

**REPLICATED** — Algorithm 1 (Theorem 1, van Dam & Hallgren 2000)
reproduces perfectly on primes p ∈ {13, 31, 61}, all shifts, exact
2 oracle queries, success probability = 1 - 1/p to 6 decimals.
Classical hardness structure independently verified via 3 attacks.
Theorems 2 and 3 acknowledged out-of-scope for QC-200 budget.
