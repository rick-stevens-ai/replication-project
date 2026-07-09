# Artifacts summary — quant-ph/0001108 replication

## Directory tree

```
QC-quant-ph-0001108-modular-functor-universal-quantum/
├── paper.pdf                                (212 KB, arXiv:quant-ph/0001108v2)
├── extraction/
│   ├── marker.md                            (pdftotext fallback + header note)
│   └── nougat.mmd                           (pdftotext fallback + header note)
├── report/
│   ├── REPORT.tex                           (this replication's LaTeX report)
│   ├── open_questions.json                  (5 Q&A + basis + next_steps)
│   ├── workflow.md                          (narrative + tools + effort)
│   ├── artifacts_summary.md                 (this file)
│   ├── failure_analysis.md                  (honest gaps)
│   └── evidence/
│       ├── fibonacci_anyons.py              (Fibonacci anyon braiding simulator, ~500 LOC)
│       └── fibonacci_results.json           (all axiom checks + best braid words + matrices)
└── work/
    ├── paper.pdf                            (downloaded copy)
    ├── paper.txt                            (pdftotext -layout output)
    ├── fibonacci_anyons.py                  (working copy)
    └── fibonacci_results.json               (working copy)
```

## Artifact provenance

| # | Path | Source | Notes |
|---|---|---|---|
| 1 | `paper.pdf` | `https://arxiv.org/pdf/quant-ph/0001108` (v2, 2000-02-01) | 212114 bytes |
| 2 | `extraction/marker.md` | `pdftotext -layout` fallback (Marker CLI not installed; central corpus lookup did not surface this id) | 982 lines |
| 3 | `extraction/nougat.mmd` | `pdftotext -layout` fallback (Nougat CLI not installed) | 982 lines |
| 4 | `report/REPORT.tex` | agent-authored based on paper + simulation results | not compiled to PDF locally (no TeX toolchain invocation in this pass) |
| 5 | `report/open_questions.json` | agent-authored, 5 questions grounded in observed replication findings | machine-readable + mirrored in REPORT.tex |
| 6 | `report/workflow.md` | agent-authored | tools, versions, effort estimate |
| 7 | `report/artifacts_summary.md` | this file | full inventory |
| 8 | `report/failure_analysis.md` | agent-authored | limitations and gaps |

## Simulation evidence

| Quantity | Value | Location in evidence |
|---|---|---|
| Pentagon residual (all-tau, F^2 = I) | 1.11e-16 | `fibonacci_results.json` -> `checks.pentagon.residual_max` |
| Hexagon / Yang-Baxter residual | 1.76e-16 | `fibonacci_results.json` -> `checks.hexagon.residual_max` |
| sigma_1 unitarity residual | 1.19e-17 | `fibonacci_results.json` -> `checks.unitarity.sigma_1_UdU_residual` |
| sigma_2 unitarity residual | 2.22e-16 | `fibonacci_results.json` -> `checks.unitarity.sigma_2_UdU_residual` |
| Best Hadamard braid word (len 13) | dist = 2.915526e-02 | `fibonacci_results.json` -> `search.hadamard` |
| Best T-gate braid word (len 14) | dist = 3.185377e-02 | `fibonacci_results.json` -> `search.T` |
| Full sigma_1, sigma_2 matrices | complex 2x2 | `fibonacci_results.json` -> top-level `sigma_1`, `sigma_2` |

## Trace log (chronological)

1. `mkdir -p ... && curl -sL https://arxiv.org/pdf/quant-ph/0001108 -o work/paper.pdf` -- 212114 bytes.
2. `pdftotext -layout work/paper.pdf work/paper.txt` -- 980 lines.
3. `python3 fibonacci_anyons.py --max-len 14` -- axiom checks passed; braid search completed; JSON serialisation raised on complex numbers in hexagon dict.
4. Edited `cx()` serialiser into `check_hexagon`.
5. `python3 fibonacci_anyons.py --max-len 15 --out fibonacci_results.json` -- clean run; `fibonacci_results.json` produced.
6. `cp work/{fibonacci_anyons.py,fibonacci_results.json} report/evidence/`.
7. `extraction/marker.md` and `extraction/nougat.mmd` populated as `pdftotext` fallbacks with explicit provenance headers.
8. Wrote reports and this summary.
