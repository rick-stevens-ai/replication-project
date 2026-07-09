# Artifacts inventory — quant-ph/0511148 replication

Root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0511148-limitations-coset-states-graph-iso-hallgren/`

## Top-level

| Path | Bytes | Role |
|------|-------|------|
| `paper.pdf` | 276 503 | Original arXiv PDF (fetched 2026-07-05) |

## `extraction/`

| Path | Role |
|------|------|
| `marker.md` | Marker surrogate (PyMuPDF 1.27.2.3 full-text) |
| `nougat.mmd` | Nougat surrogate (`pdftotext -layout`) |
| `README.md` | Notes on surrogate choice |

## `work/`

| Path | Role |
|------|------|
| `paper.txt` | Plain-text extraction used to locate Theorem 12 |

## `report/`

| Path | Role |
|------|------|
| `REPORT.tex` | Detailed LaTeX report, section-by-section |
| `REPORT.pdf` | Compiled report (if pdflatex present at replication time; otherwise skip — .tex is authoritative) |
| `open_questions.json` | 5 heavy-duty follow-on questions with next steps |
| `workflow.md` | Full workflow narrative, tools, effort estimate |
| `artifacts_summary.md` | (this file) |
| `failure_analysis.md` | Honest analysis of friction / residual gaps |

## `report/evidence/`

| Path | Role |
|------|------|
| `coset_state_sim.py` | Character tables (Murnaghan–Nakayama), Δ_char sweep, exact ρ_H tensor-power trace distance |
| `wreath_and_pgm.py` | GI-setting sweep (S_{2n}, h = 2^n), Helstrom/PGM P_succ, n=5 exact |
| `make_plots.py` | 3 figures |
| `results.json` | Full grid: S_n character sweep + exact trace-distance verification + scaling |
| `results_wreath_pgm.json` | GI setting: character sweep, PGM sweep, t* growth |
| `fig_delta_char_gi.png` | Δ_char vs t for GI setting, log scale, per-n curves |
| `fig_t_star_scaling.png` | t*(n) vs n·log₂ n with linear-fit-through-origin |
| `fig_lhs_vs_rhs.png` | Exact LHS trace distance vs Thm-12 RHS, log scale |

## Numerical outputs (headline numbers)

- **Δ_char(n=8, t=1) = 0.286** (S_n setting): exponentially small in n.
- **Δ_char(n_graph=6, t=1) = 0.0127** (GI setting S_{2n}): factor ~80 smaller than n_graph=2 case.
- **t*(n)/(n·log₂ n) ratio ∈ {0.500, 0.506, 0.476, 0.473, 0.471}** for n_graph=2..6 — flat, confirming Θ(n log n).
- **Linear-fit slope c ≈ 0.475** for t*(n) = c·n·log₂ n.
- **Exact LHS ≤ RHS** for every one of the 7 tested (n,t) pairs.
- **Helstrom P_succ ≤ 0.750** even at n=2,t=1 (small group, most favorable), drops to 0.558 at n=5,t=1 and stays close to 0.5 as n grows.

## Verification checksums

Character-table sanity (paper does not tabulate these, but they are
textbook):
- `dim(S_4) = [1,3,2,3,1]`, Σd² = 24 = 4! ✓
- `dim(S_5) = [1,4,5,6,5,4,1]`, Σd² = 120 = 5! ✓
- `χ(transposition, S_4) = [1,1,0,-1,-1]` ✓
- `χ(transposition, S_5) = [1,2,1,0,-1,-2,-1]` ✓

## Traces / logs

Because deterministic and short, no separate log files were produced;
`results.json` and `results_wreath_pgm.json` each record every input row
and every derived numerical value, along with `wall_clock_seconds`.

## Provenance

- All numerical work executed on CherryRd (macOS 25.3, Python 3.13.7,
  numpy 2.4.3, sympy 1.14.0) between 16:56–17:05 CDT on 2026-07-05.
- No external computation, no LLM inference.
- No paid API calls.
