# Artifacts summary — Lubich (2008) replication

Root: `~/Dropbox/REPLICATE-PROJECT/PDE-Lubich-splitting-Schrodinger-Poisson-cubic-NLS-2008/`

## Paper source
- `speq.pdf` — Lubich preprint, 169616 B, md5 `608e48c81bd247f3d8beef9b420d68cb`. Fetched from `https://na.uni-tuebingen.de/pub/lubich/papers/speq.pdf`. Journal DOI: 10.1090/S0025-5718-08-02101-7. openAccess per Semantic Scholar.

## Code (in `work/`)
- `lubich_splitting.py` — 1D periodic Fourier-spectral Strang split-step solver for cubic NLS (± signs) and Schrödinger–Poisson (± signs). Convergence sweep over τ ∈ {1/50, 1/100, 1/200, 1/400, 1/800} against reference solution at τ_ref = 1/32000. Emits `convergence_results.json` and prints the results table. 13.7 s wall on a single mac core.
- `make_plot.py` — reads `convergence_results.json` and produces `evidence/convergence_plot.png` (log-log ‖e‖_L² and ‖e‖_Hᵐ vs τ, four problems, slope-2 reference line).
- `llm_judge.py` — packages claim table + observed rates + mass drifts, hits Argo proxy `http://127.0.0.1:44497/v1/chat/completions` (FREE), writes `report/evidence/llm_judge_output.md`. Actual model at run time: `argo:claude-sonnet-4.6` (Opus 4.8 and Opus 4.7 both 502'd — upstream flake).

## Numerical results (in `work/` and `report/evidence/`)
- `work/convergence_results.json` — JSON of τ, ‖e‖_L², ‖e‖_Hᵐ, observed orders, mass drift, for all 4 problems.
- `report/evidence/run_convergence.log` — text log of the convergence run.
- `report/evidence/convergence_plot.png` — the log-log plot referenced above.
- `report/evidence/llm_judge_output.md` — verbatim LLM-judge output (sonnet-4.6 via Argo), JSON verdict block reproduced in REPORT.md §6.

## Reports (in `report/`)
- `REPORT.md` — canonical human-facing report (this replication's source of truth). 14 KB.
- `REPORT.tex` — LaTeX version of the report with a dedicated GENUINE CRITIQUE section.
- `open_questions.json` — 5 truly-open questions about Lubich (2008) grounded in the replication.
- `workflow.md` — end-to-end procedure record.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — enumeration of what could have gone wrong and did/didn't (and the LLM-judge model-substitution incident).

## Compute
- All numerical work: single-core local mac, 13.7 s wall for the full convergence sweep.
- `ssh uicgpu` was used only as a Cloudflare-bypass fetch of the AMS PDF URL (not needed for numerics).
- LLM-judge: Argo proxy (FREE endpoint).

## Testable-claim coverage
6 of 6 testable claims (C1–C6 in REPORT.md §2) covered by numerical evidence:
- C1, C3 (L² order 2): reproduced exactly (obs. 2.000–2.042).
- C2, C4 (Hᵐ order 1 upper bound): consistent (obs. ~2, better than the theorem's upper bound, as expected on smooth periodic data).
- C5 (L² mass conservation): reproduced at machine precision (≤ 1.2·10⁻¹³).
- C6 (explicit + reversible): reproduced by construction and by the free-Schrödinger plane-wave sanity test (error 4.4·10⁻¹⁴).

## Verdict
REPLICATED. Human-authored and LLM-judge verdicts agree.
