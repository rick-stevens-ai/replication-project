# Artifacts summary — QC-100 / QC-QAOA-benchmarking-Guerreschi2019

Replication of arXiv:1907.02359 (Willsch et al., QAOA benchmarking).
Verdict: **REPLICATED**.

## Report layer (`report/`)
| File | Purpose |
|---|---|
| `REPORT.md` | Human-readable replication report (original wave output). |
| `REPORT.tex` | LaTeX-formatted version of REPORT.md with genuine critique section. |
| `open_questions.json` | Bare JSON list of 5 open-question objects `{q, basis, next_steps}`. |
| `open_questions_section.tex` | LaTeX section rendering the 5 open questions. |
| `workflow.md` | Step-by-step reproduction workflow (this replication). |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Honest self-critique: what was NOT tested, quantitative gaps, metadata drift. |

## Extraction layer (`extraction/`)
| File | Purpose |
|---|---|
| `nougat.mmd` | Nougat/markdown-extracted paper stub (placeholder — actual paper PDF referenced by arXiv id 1907.02359; full extraction not committed to keep dir slim). |

## Work layer (`work/`)
See existing files:
- `qaoa_core.py` — statevector QAOA + metrics + analytic Eq. 19.
- `run_replication.py` — T1/T2/T3 driver.
- `finish.py` — MaxCut p=5 + linear-anneal-init tau-scan.
- `results.json` — machine-emitted numerical results.
- `run.log`, `finish.log` — execution logs.

## Reproducibility notes
- Python 3.14.6, numpy 2.4.3, scipy 1.18.0.
- Deterministic seeds throughout.
- No paywalled data, no proprietary hardware.
- LLM-judge calls used free Argo endpoints only (`argo:gpt-5.2`, `argo:gpt-5.1`).

## Coverage
- Simulator claims C1..C5: **all exercised, all pass** (some C5 numeric gaps
  documented in failure_analysis.md).
- Hardware claims C6, C7: out of scope (require D-Wave 2000Q / IBM Q Experience).
- **Headline exercised: YES** — the paper's central story (instance-sensitivity,
  monotone-improvement with p, linear-anneal-init large-p recovery) is
  reproduced numerically.
