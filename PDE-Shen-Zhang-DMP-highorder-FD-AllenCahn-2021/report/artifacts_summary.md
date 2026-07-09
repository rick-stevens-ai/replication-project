# Artifacts summary

Every deliverable in this replication dir, with size and purpose.

## Top-level

| File | Purpose |
|---|---|
| `paper.pdf` | Shen & Zhang 2021 preprint (arXiv:2104.11813v1), 3.6 MB |

## `extraction/`

| File | Purpose |
|---|---|
| `marker.md` | pdftotext-layout extraction, marker-format wrapper (corpus convention when marker_single CLI unavailable) |
| `nougat.mmd` | pdftotext-layout extraction, nougat-format wrapper |

## `report/`

| File | Purpose |
|---|---|
| `REPORT.md` | Full report — paper summary, claims table, method, results, verdict, open questions |
| `REPORT.tex` | Same content, LaTeX version, section-by-section |
| `brief.md` | 1-paragraph what/why |
| `attempt_log.md` | Chronological log |
| `artifact_harvest.md` | Public artifacts pulled + code generated |
| `workflow.md` | Compute + tools + commands + effort estimate |
| `failure_analysis.md` | What went wrong (LiteLLM 502 on opus-4.7 for our judge prompt) |
| `artifacts_summary.md` | This file |
| `open_questions.json` | 5 grounded research questions arising from this replication |

## `report/evidence/`

| File | Purpose |
|---|---|
| `dmp_summary.csv` | 6-row summary of DMP dynamics runs |
| `conv_1d_o2.csv` | 1D order-2 spatial convergence table |
| `conv_1d_o4.csv` | 1D order-4 (compact) spatial convergence table |
| `conv_2d_o2.csv` | 2D order-2 spatial convergence table |
| `conv_2d_o4.csv` | 2D order-4 (compact) spatial convergence table |
| `dmp_and_convergence_results.json` | Master JSON with all numerical outputs |
| `dmp_over_time.png` | Figure 1: max\|u\| vs t for all 6 dynamics runs |
| `convergence_loglog.png` | Figure 2: log-log convergence plots, 1D + 2D, order 2 + 4 |
| `judge_prompt.txt` | Full prompt sent to LLM judge |
| `judge_raw.txt` | Raw model response |
| `judge_verdict.json` | Parsed JSON verdict (per-claim + overall) |
| `judge_used.txt` | Which model+endpoint the judge used (`argo:gpt-5.4` via aggregator) |

## `work/`

| File | Purpose |
|---|---|
| `allen_cahn_dmp.py` | Core numerical solver (350 LoC, from scratch — no paper code) |
| `make_figures.py` | Plot generation |
| `emit_csvs.py` | CSV export |
| `judge.py` | LLM-judge invocation |
| `dmp_and_convergence_results.json` | Same JSON as in `report/evidence/` (kept locally too) |

## 8-artifact completion bar (Rick 2026-07-05 standard)

| # | Required | Present |
|---|---|---|
| 1 | `paper.pdf` | ✅ |
| 2 | `extraction/marker.md` | ✅ |
| 3 | `extraction/nougat.mmd` | ✅ |
| 4 | `report/REPORT.tex` (detailed, section-by-section) | ✅ |
| 5 | `report/open_questions.json` (5 heavy-duty) + Open Questions section in REPORT | ✅ |
| 6 | `report/workflow.md` | ✅ |
| 7 | `report/artifacts_summary.md` | ✅ |
| 8 | `report/failure_analysis.md` | ✅ |
