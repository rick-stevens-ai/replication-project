# Artifacts summary

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1312.1414-sparse-hamiltonian-simulation-exponential-berry/`

## 8-artifact completion bar (from `REPLICATION_DIR_STANDARD_2026-07-05`)

| # | Required artifact | Path | Status |
|---|---|---|---|
| 1 | `paper.pdf` | `paper.pdf` (+ mirror `work/paper.pdf`) | ✅ 383 KB, 28 pp, PDF v1.4 |
| 2 | `extraction/marker.md` | `extraction/marker.md` | ⚠️ present but Marker not installed on host; fallback = `pdftotext` output with banner-noted provenance |
| 3 | `extraction/nougat.mmd` | `extraction/nougat.mmd` | ⚠️ present but Nougat not installed on host; fallback = same pdftotext text with `.mmd` banner |
| 4 | `report/REPORT.tex` | `report/REPORT.tex` | ✅ full LaTeX report with claim table, methods, results, verdict, open questions |
| 5 | `report/open_questions.json` | `report/open_questions.json` | ✅ 5 grounded questions, `{q, basis, next_steps}` schema |
| 6 | `report/workflow.md` | `report/workflow.md` | ✅ full workflow, tool versions, work-time estimate |
| 7 | `report/artifacts_summary.md` | this file | ✅ |
| 8 | `report/failure_analysis.md` | `report/failure_analysis.md` | ✅ honest gap analysis |

## Additional evidence (under `report/evidence/`)

| File | Role |
|---|---|
| `report/evidence/lcu_taylor_sim.py` | Reproducible numpy/scipy implementation of the truncated Taylor-LCU vs 1st-order Trotter. Deterministic (seed 20260705). |
| `report/evidence/results.json` | Full raw run output: per-(t,K) LCU Frobenius/spectral/state errors, Trotter errors, LCU prepare-amplitude checks, analytic Taylor-remainder bound, fitted scaling slopes. |
| `report/evidence/eps_vs_K.png` | Semilog plot of ε vs. K for LCU, Trotter, and the (||H||t)^(K+1)/(K+1)! bound, at t=0.5 and t=1.0. |

## Provenance + integrity

- Paper source: `curl -sL https://arxiv.org/pdf/1312.1414` on 2026-07-05.
- Paper text: `pdftotext work/paper.pdf work/paper.txt` (poppler).
- Deterministic RNG seed everywhere: `20260705`.
- All numeric claims in `REPORT.tex` cross-check against `results.json` verbatim.
- No LLM was used for any load-bearing numeric claim; Argo endpoint was not invoked because the replication test is a deterministic numerical match-to-analytic-bound test, not a judgment call.

## Verdict location

`report/REPORT.tex` §Verdict: **REPLICATED**.
