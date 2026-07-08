# Artifacts Summary — QC-2204.13641

**Set:** QC-100 · **Verdict:** REPLICATED · **Backfilled:** 2026-07-06

## File inventory

### Report layer (`report/`)
| File | Purpose | Provenance |
|---|---|---|
| `REPORT.md` | Primary human-readable report | Original 2026-07-04 |
| `REPORT.tex` | LaTeX mirror with explicit Critique section | Backfill 2026-07-06 |
| `open_questions.json` | 5 open questions (bare list, `{q, basis, next_steps}` schema) | Backfill 2026-07-06 |
| `open_questions_section.tex` | LaTeX section input for REPORT.tex | Backfill 2026-07-06 |
| `workflow.md` | Chronological workflow | Backfill 2026-07-06 |
| `artifacts_summary.md` | This file | Backfill 2026-07-06 |
| `failure_analysis.md` | Honest critique of scope limits & unresolved claims | Backfill 2026-07-06 |
| `evidence/results.json` | Numeric outputs of all 600 experiments | Original 2026-07-04 |
| `evidence/judge_verdict.json` | LLM judge JSON (Argo Claude Opus 4.7) | Original 2026-07-04 |

### Code layer (`code/`)
| File | Purpose |
|---|---|
| `rqae.py` | RQAE + classical Hoeffding reference (~200 LOC) |
| `run_experiment.py` | 25-rep × 12-config sweep driver |
| `llm_judge.py` | Single Argo call for LLM-judge verdict |

### Extraction layer (`extraction/`)
| File | Purpose |
|---|---|
| `nougat.mmd` | Nougat extraction stub (paper.txt is the primary text source) |

### Work layer (`work/`)
| File | Purpose |
|---|---|
| `paper.pdf` | arXiv:2204.13641 v2 PDF |
| `paper.txt` | ASCII text extraction |

### Logs (`logs/`)
| File | Purpose |
|---|---|
| `experiment.log` | Full stdout/stderr from `run_experiment.py` |

## Headline metric (single number)

**RQAE log–log slope on `N_oracle` vs `1/eps` = 0.959** (paper claim: ~1.0; classical baseline: 2.000).

Confirmed at 25 reps × 3 amplitudes × 4 epsilons = 300 RQAE runs; coverage 100% (paper guarantees ≥95%); sign recovery on `a = -0.4` verified.

## Verdict provenance

- **REPLICATED** per `report/REPORT.md` §5 (2026-07-04).
- Cross-confirmed by local LLM judge (Argo Claude Opus 4.7, `overall_verdict: REPLICATED`, single call).
- Backfill (2026-07-06) preserved the verdict: the headline scaling plot (RQAE ~1/eps vs classical ~1/eps^2) is the paper's central claim and was quantitatively reproduced (slope 0.959 vs 1.000; slope 2.000 vs 2.000). Scope limits (no noise, no MLQAE/IQAE comparison, toy oracle only) are transparently declared but do not undermine the headline.

## What's NOT here (scope declaration)

- No noise-model runs (`AerSimulator()` is noiseless; only real Bernoulli shot noise).
- No side-by-side against MLQAE (Suzuki 2019) or IQAE (Grinko 2019).
- No multi-qubit finance/option-pricing oracle (single-qubit `R_y` toy oracle only).
- No hardware runs (CPU simulator only, no IBM Quantum backend).
- No adaptive-schedule variant.

All five gaps are captured as concrete follow-up experiments in `report/open_questions.json`.
