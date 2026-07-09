# Artifacts summary — QC-quant-ph-9603026-efficient-simulation-quantum-systems-zalka

Mapping this replication's files to the QC-200 mandatory-8 completion bar
(`REPLICATION_DIR_STANDARD_2026-07-05.md`).

| # | Artifact required by the standard | Path in this dir | Status | Notes |
|--:|---|---|---|---|
| 1 | `paper.pdf` (original PDF) | `paper.pdf` | ✅ present | Fetched from `https://arxiv.org/pdf/quant-ph/9603026`, 113 kB, 8 pages, PDF v1.4 |
| 2 | `extraction/marker.md` (Marker parse) | `extraction/marker.md` | ⚠️ fallback | Marker not installed; hand-cleaned `pdftotext` rewrite in Marker's Markdown style. See `report/failure_analysis.md`. |
| 3 | `extraction/nougat.mmd` (Nougat parse) | `extraction/nougat.mmd` | ⚠️ fallback | Nougat not installed; hand-cleaned `pdftotext` rewrite in Nougat's `.mmd` style. See `report/failure_analysis.md`. |
| 4 | `report/REPORT.tex` (detailed section-by-section report) + PDF | `report/REPORT.tex` (+ `REPORT.pdf` if pdflatex present) | ✅ present | Full: paper summary, C1..C6 claims table with testable/tested, method with commands + tool versions, results-vs-paper table, verdict + Open Questions. |
| 5 | `report/open_questions.json` (5 heavy Q) + `## Open Questions` in report | `report/open_questions.json` + `## Open Questions` in `REPORT.tex` | ✅ present | Five specific questions grounded in what this reproduction observed. |
| 6 | `report/workflow.md` (workflow + tools + effort) | `report/workflow.md` | ✅ present | Timeline, tools table with versions, one-liner repro, ~10 min effort estimate. |
| 7 | `report/artifacts_summary.md` | this file | ✅ present | — |
| 8 | `report/failure_analysis.md` | `report/failure_analysis.md` | ✅ present | Honest write-up of what we could not (or chose not to) reproduce and why. |

## Evidence directory

| File | Bytes | Role |
|---|--:|---|
| `report/evidence/trotter_heisenberg.py` | 8.8 kB | numerical reproducer |
| `report/evidence/make_plot.py`          | 1.4 kB | plot generator |
| `report/evidence/trotter_results.json`  | ~2.5 kB | per-K results and fits |
| `report/evidence/trotter_verdict.json`  | ~150 B | verdict gate + slopes |
| `report/evidence/trotter_run.log`       | ~1.2 kB | stdout of the run |
| `report/evidence/trotter_error_vs_dt.png` | ~60 kB | figure used in REPORT |

## Headline results

- 1st-order Trotter log-log slope: **1.012** (predicted 1)
- 2nd-order symmetric Suzuki-Trotter slope: **2.002** (predicted 2)
- Frobenius error at $\Delta t = 0.005$: $6.97\times 10^{-3}$ (1st) and
  $1.03\times 10^{-4}$ (2nd)
- Unitarity: all approximants $\|U^\dagger U - I\|<1.3\times 10^{-13}$
- Verdict: **REPLICATED**

## Provenance

- Paper: arXiv:quant-ph/9603026v2 (14 Aug 1996), Christof Zalka.
- Fetched: 2026-07-05 19:22 CDT from arXiv.
- Reproducer host: CherryRd (Darwin 25.3.0).
- No LLMs used for the numerical claim; no paid APIs.
