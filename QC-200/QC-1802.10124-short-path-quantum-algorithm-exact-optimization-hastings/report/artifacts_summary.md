# Artifacts Summary

**Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1802.10124-short-path-quantum-algorithm-exact-optimization-hastings/`

## Required 8 (per Rick 2026-07-05 completion bar)

| # | Path (relative to target dir) | Type | Status | Notes |
|--:|---|---|---|---|
| 1 | `paper.pdf` | Original PDF | ✅ | 537 kB, arXiv:1802.10124v3, downloaded from arxiv.org. |
| 2 | `extraction/marker.md` | Marker parse | ⚠️ fallback | Marker not installed on host; pdftotext-derived Markdown fallback, honestly labeled. |
| 3 | `extraction/nougat.mmd` | Nougat parse | ⚠️ fallback | Nougat not installed on host; pdftotext-derived .mmd fallback with hand-transcribed key equations, honestly labeled. |
| 4 | `report/REPORT.tex` | Detailed LaTeX report | ✅ | 17.8 kB, ~250 lines, section-by-section claims / method / results / verdict. Compile with `pdflatex report/REPORT.tex` if desired. |
| 5 | `report/open_questions.json` | 5 heavy-duty open questions (JSON) | ✅ | 5 objects with `{q, basis, next_steps}` fields. |
| 5b | `report/REPORT.tex` § Open Questions | Same 5 Qs in prose in the report | ✅ | Q1..Q5 present in \section{Open Questions}. |
| 6 | `report/workflow.md` | Workflow + tools + versions + work estimate | ✅ | 4.8 kB. |
| 7 | `report/artifacts_summary.md` | THIS file. Inventory of all artifacts. | ✅ | You are reading it. |
| 8 | `report/failure_analysis.md` | Honest failure/friction log | ✅ | 5.9 kB, 6 friction items (F1–F6) + residual gaps. |

## Additional / supporting artifacts

| Path | Type | Notes |
|---|---|---|
| `work/paper.pdf` | Original PDF (backup copy) | Same file as top-level `paper.pdf`. |
| `work/paper.txt` | Full plain-text extraction (`pdftotext`) | 1987 lines. Primary source used by REPORT.tex citations. |
| `work/paper_layout.txt` | Layout-preserving text extraction (`pdftotext -layout`) | 1421 lines. Useful when the two-column layout matters. |
| `report/evidence/short_path_sim.py` | Main simulation code | Python 3.14 + numpy 2.4 + scipy 1.18, ~250 LOC. Fixed seed 20260705. |
| `report/evidence/smoke_test.py` | Quick N=6 smoke test | Confirms mechanics before the full sweep. |
| `report/evidence/analyze_results.py` | Post-processing script | Reads results.json → summary.json + scaling.json + human-readable table. |
| `report/evidence/results.json` | Raw sweep output | 478 kB, 736 rows: one per (ensemble, N, instance, K, b) tuple. Fields include min_gap, P_ov_plus_psi01, P_ov_psi00_psi01, P_success_direct, ratio_short_over_grover. |
| `report/evidence/summary.json` | Aggregated medians | Per (ensemble, N, K, b). |
| `report/evidence/scaling.json` | Slope of log(ratio) vs N | Per (ensemble, K, b). Empirical vs. Theorem 2 slope. |
| `report/evidence/run.log` | Full run log | Timing per instance + printed summary. |

## Reproducibility

```
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1802.10124-short-path-quantum-algorithm-exact-optimization-hastings
# 1. Simulation (12-15 minutes wall on Intel Mac)
python3 report/evidence/short_path_sim.py > report/evidence/run.log 2>&1
# 2. Post-process
python3 report/evidence/analyze_results.py
# 3. Compile report (optional)
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex
```

## Traces (what was actually run, with wall times)

- 736 (ensemble, N, instance, K, b) tuples classically diagonalized.
- Wall time: 716 s (~12 min) on CherryRd single-machine, ~10 cores of BLAS-parallel numpy.
- Fixed seed: 20260705.
- No external network calls after paper fetch. No paid API usage.
