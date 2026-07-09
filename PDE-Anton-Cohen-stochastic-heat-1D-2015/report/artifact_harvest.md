# Artifact Harvest

| Artifact | Source | Size | Notes |
|---|---|---|---|
| `anton_cohen_2015.pdf` | https://arxiv.org/pdf/1711.08340v1 | 351 KB, 36 pp | Open-access arXiv PDF (math.NA), the paper itself |
| `arxiv_src.tar.gz` | https://arxiv.org/e-print/1711.08340v1 | 60 KB | LaTeX source bundle |
| `src/acqsHeat.tex` | extracted | 82 KB | Full LaTeX source (scheme + experiments) |
| `src/acqsHeat.bbl` | extracted | 12 KB | Bibliography |
| `src/msSupHeat.eps` | extracted | 40 KB | Figure 1 source (strong-convergence loglog plot) |
| `src/compcost.eps` | extracted | 22 KB | Figure 2 source (computational cost) |
| `src/prof1.eps` | extracted | 72 KB | Figure 3 source (almost-sure convergence) |

- No external data needed: the paper's numerical experiments are fully specified by
  the test problem (u0, f, σ, domain, BC) and discretization parameters. All numbers
  reproduced from a from-scratch solver — no downloaded datasets.
- Published DOI on the priority list (10.1093/IMANUM/DRV006) corresponds to the journal
  version; the arXiv preprint (1711.08340) is the OA artifact used here. Content of the
  scheme, theorems, and numerical experiments matches.
- Verdict basis: our own code outputs in `report/evidence/`.

## arXiv identity check
- Title (arXiv API + PDF): "A fully discrete approximation of the one-dimensional
  stochastic heat equation" — Rikard Anton, David Cohen, Lluís Quer-Sardanyons. Match.
