# Artifacts Summary

Root: `~/Dropbox/REPLICATE-PROJECT/PDE-Ethridge-Greengard-FMM-Poisson-2D-2001/`

## Mandatory 8-artifact bar (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path | Status | Notes |
|---|----------|------|--------|-------|
| 1 | Paper PDF | `paper.pdf` | ✔ present | 2.86 MB, PDF 1.2, from `math.nyu.edu/faculty/greengar/poiss2d.pdf` (Green OA), SHA-256 `6634e8d832c85a546a5ef4fe2c08edc5db235195d181b07edde8979e411c091e` |
| 2 | Marker extraction | `extraction/marker.md` | ✔ present | pdftotext -layout fallback (marker not installed locally), with backfill header |
| 3 | Nougat extraction | `extraction/nougat.mmd` | ✔ placeholder | pending central Nougat parse (no local GPU + no nougat binary on CherryRd) |
| 4 | LaTeX report | `report/REPORT.tex` | ✔ present | Section-by-section, includes figure references and detailed critique |
| 5 | Open questions JSON | `report/open_questions.json` | ✔ present | 5 heavy-duty questions each with `q`, `basis`, `next_steps`. Summary also in REPORT.md §6 |
| 6 | Workflow | `report/workflow.md` | ✔ present | Full stage-by-stage narrative + tool list + effort estimate |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✔ present | This file |
| 8 | Failure analysis | `report/failure_analysis.md` | ✔ present | What broke and why (M2L sign bug, Argo Opus 502) |

## Additional artifacts

| Path | Purpose |
|------|---------|
| `report/REPORT.md` | Canonical human-readable report |
| `report/brief.md` | 1-paragraph what/why |
| `report/attempt_log.md` | Chronological log |
| `report/artifact_harvest.md` | Data/artifact provenance |
| `report/evidence/C1_accuracy_vs_p.json` | Raw C1 numbers (p, rel_L2, rel_Linf, N, nlev) |
| `report/evidence/C1_accuracy_vs_p.png` | C1 log-scale plot |
| `report/evidence/C2_scaling.json` | Raw C2 numbers (N, T_fmm, T_direct, rel_err, rate) |
| `report/evidence/C2_scaling.png` | C2 log-log plot |
| `report/evidence/C3_gaussians.json` | Raw C3 numbers (N_side, N, rel_L2, rel_Linf, T, offset) |
| `report/evidence/C3_gaussians.png` | C3 plot + overlay of paper's Table 2 |
| `report/evidence/C4_fft_poisson.json` | Raw C4 numbers (N_side, T, rel_L2_interior) |
| `report/evidence/C4_fft_poisson.png` | C4 timing + convergence plot |
| `report/evidence/llm_judge_verdict.json` | Argo GPT-5.4 verdict (PARTIAL) |
| `work/fmm2d.py` | Pure-Python 2D FMM engine (from scratch) |
| `work/run_experiments.py` | C1-C4 driver |
| `work/make_plots.py` | Figure generator |
| `work/llm_judge.py` | Argo-based verdict script |
| `work/run.log` | Full experiment stdout |
| `work/paper_layout.txt` | pdftotext dump used for extraction |
