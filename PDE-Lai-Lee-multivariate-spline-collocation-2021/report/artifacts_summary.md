# Artifacts summary

## Files produced in this replication

### Top-level
- `paper.pdf` — arXiv:2109.09698v5 preprint (1.4 MB)

### `extraction/`
- `marker.md` — VikParuchuri marker OCR/layout extraction (99 KB)
- `nougat.mmd` — Meta Nougat OCR extraction (87 KB)

### `work/` (code)
- `bb_spline_poisson.py` — first BB collocation attempt (failed; kept for provenance)
- `bb_spline_v2.py` — second BB attempt (failed)
- `bb_spline_v3.py` — third BB attempt (failed)
- `pk_fem_poisson.py` — **working** P^D Galerkin FEM implementation
- `multi_test.py` — multiple-test-function sweep with non-zero Dirichlet BC
- `test_bb_basics.py`, `test_derivs.py`, `debug_eval.py`, `debug_v2.py` — sanity/debug scripts
- `convergence_pk_fem.json`, `convergence_orders_pk_fem.json`, `multi_test_results.json`, `convergence_results_v2.json`, `convergence_results_v3.json`, `convergence_lagrange.json`, `convergence_orders_lagrange.json`, `convergence_orders_v3.json` — result JSONs

### `report/`
- `REPORT.md` — full replication report (this file)
- `REPORT.tex` — LaTeX-formatted version
- `brief.md` — one-paragraph what/why
- `attempt_log.md` — chronological trajectory + bugs
- `failure_analysis.md` — why the direct BB-collocation implementation failed and why we substituted P^D Galerkin
- `workflow.md` — pipeline + effort estimate
- `artifact_harvest.md` — external sources
- `artifacts_summary.md` — this file
- `open_questions.json` — 5 new research questions
- `evidence/`
    - `convergence_pk_fem.json` — 16-row table of D × n → (ndof, L², L∞, H¹, time)
    - `convergence_orders_pk_fem.json` — empirical convergence orders (L² and H¹) per degree
    - `multi_test_results.json` — us1/us3/us4/us5 error tables (with & without proper BC lifting)

## 8-artifact completion bar (Rick 2026-07-05)
1. ✅ `paper.pdf`
2. ✅ `extraction/marker.md`
3. ✅ `extraction/nougat.mmd`
4. ✅ `report/REPORT.tex`
5. ✅ `report/open_questions.json` (5 questions with `q`, `basis`, `next_steps`)
6. ✅ `report/workflow.md`
7. ✅ `report/artifacts_summary.md`
8. ✅ `report/failure_analysis.md`
