# Artifacts Summary

## Public artifacts pulled

| Item | Source | Size | sha256 (16) |
|------|--------|------|-------------|
| `paper.pdf` | https://arxiv.org/pdf/quant-ph/0503205 | 138,309 B | 2ec4612be55f2cda |
| `extraction/marker.md` | Central QC-200 corpus (pdftotext-fallback parse produced 2026-07-05) | 24,715 B | d4a2517b43c61014 |
| `extraction/nougat.mmd` | Central QC-200 corpus (Nougat parse produced 2026-07-05) | 31,534 B | 42a7c4f0dbad44c9 |

## Code / scripts produced (this run)

| File | LOC | Size | sha256 (16) | Purpose |
|------|----:|------|-------------|---------|
| `work/pi3_search.py` | ~240 | 10,887 B | f8025b66d66b8388 | Main replication driver (statevector sim, both algorithms, figures) |
| `work/llm_judge.py`  | ~130 |  5,088 B | b04decda557cf73f | Argo free-endpoint LLM-judge scoring |

## Evidence / outputs

| File | Size | sha256 (16) | Description |
|------|------|-------------|-------------|
| `report/evidence/numeric_results.json` | 1,536 B | a67481da345bb68b | All measured probabilities + query counts; central numeric result |
| `report/evidence/run_log.txt` | 1,626 B | — | Console log of `pi3_search.py` run |
| `report/evidence/monotonicity_check.txt` | 148 B | — | Numpy diff of successive P values + boolean |
| `report/evidence/fig_probability_trajectory.png` | 105,044 B | d137e490438897d2 | Paper Fig-1 analogue: std Grover oscillation vs π/3 monotone staircase |
| `report/evidence/fig_failure_scaling.png` | 80,356 B | 2612f3b987b641cd | Semilog `1 − P` vs `m` overlaid with `ε^(3^m)` prediction |
| `report/evidence/llm_judge.json` | 3,554 B | 87ec4869545bb8a3 | Full LLM-judge output: model, endpoint, raw response, parsed verdict |
| `report/evidence/llm_judge_run.log` | 1,776 B | — | Console log of `llm_judge.py` run |

## Reports / narrative

| File | Size | sha256 (16) | Content |
|------|------|-------------|---------|
| `report/REPORT.md` | 10,210 B | 836d64eb28622179 | Full markdown report (paper summary, claims, method, results, verdict) |
| `report/REPORT.tex` | 9,177 B | 68145faa6a89bea3 | LaTeX detailed section-by-section report (compiles to REPORT.pdf) |
| `report/brief.md` | 851 B | 5047a1f1ceb6a41f | One-paragraph brief |
| `report/workflow.md` | 4,254 B | bfed92731b1bfe39 | Workflow narrative + tools/versions table + effort estimate |
| `report/open_questions.json` | 4,881 B | 5fad8d1d804e1c53 | 5 heavy-duty Q's each with `{q, basis, next_steps}` |
| `report/artifacts_summary.md` | (this file) | — | Artifact inventory |
| `report/failure_analysis.md` | (see file) | — | Honest what-failed / partial-mismatches / assumptions |
| `report/attempt_log.md` | (see file) | — | Chronological attempt log |
| `report/artifact_harvest.md` | (see file) | — | Every external artifact pulled |

## 8-artifact standard compliance

| # | Standard requirement | Path | Present |
|---|---------------------|------|:-------:|
| 1 | Original PDF | `paper.pdf` | ✅ |
| 2 | Marker text extraction | `extraction/marker.md` | ✅ |
| 3 | Nougat text extraction | `extraction/nougat.mmd` | ✅ |
| 4 | LaTeX detailed report | `report/REPORT.tex` | ✅ |
| 5 | 5 open questions (`{q,basis,next_steps}`) + section in report | `report/open_questions.json` + `## Open Questions` in REPORT.md/REPORT.tex | ✅ |
| 6 | Workflow + tools + effort | `report/workflow.md` | ✅ |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ |
