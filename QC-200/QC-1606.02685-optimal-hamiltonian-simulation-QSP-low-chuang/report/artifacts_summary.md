# Artifacts summary

## Required 8-artifact bar (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | Original PDF | `paper.pdf` (also `work/paper.pdf`) | ✅ 414 kB |
| 2 | Marker parse | `extraction/marker.md` | ⚠️ fallback (pdftotext, header explains) |
| 3 | Nougat parse | `extraction/nougat.mmd` | ⚠️ fallback (pdftotext, header explains) |
| 4 | REPORT.tex | `report/REPORT.tex` | ✅ 13 kB, full section-by-section |
| 4b | REPORT.pdf | `report/REPORT.pdf` | see build attempt (may not compile if no LaTeX) |
| 5 | open_questions.json | `report/open_questions.json` | ✅ 5 entries, `{q, basis, next_steps}` each |
| 6 | workflow.md | `report/workflow.md` | ✅ |
| 7 | artifacts_summary.md | this file | ✅ |
| 8 | failure_analysis.md | `report/failure_analysis.md` | ✅ |

## Evidence dir (`report/evidence/`)
- `qsp_replication.py` — 287-line replication driver
- `plot_results.py` — 3-panel plotter
- `results.json` — full JSON of all numeric results
- `trunc_err_vs_K.csv` — C1 truncation-error decay data
- `min_K_vs_eps.csv` — C2 K_min(t,eps) scaling data
- `fig_A_truncation_vs_K.png` — C1 semilog plot
- `fig_B_Kmin_vs_x.png` — C2 scaling plot
- `fig_B_intercept_vs_t.png` — C2 secondary intercept-vs-t plot

## Work dir (`work/`)
- `paper.pdf` — cached PDF (duplicate of top-level)
- `paper.txt` — pdftotext dump

## Key numeric results (headline)
| Claim | Metric | Value | Verdict |
|---|---|---|---|
| C1 | ||exp(-iHt) - A_K||_2 at K=25, t=5 | 8.7e-16 | super-exp decay to machine epsilon ✅ |
| C2 | intercept b(t) slope in t | 0.696 · t - 2.10 | linear in t as predicted ✅ |
| C2 | slope a(t) at t=1..10 | 1.67 → 3.24 | weak drift; open question Q1 |
| C3 (scalar) | max |ReU_00(x) - T_d(x)|, d=6 | 5.0e-16 | ✅ machine precision |
| C3 (matrix) | ||<0|U(H)|0> - T_d(H)||_2, d=6 | 3.8e-15 | ✅ machine precision |

## Reproducibility
- Deterministic: `np.random.default_rng(1606)` builds the test H.
- Single command: `cd report/evidence && python3 qsp_replication.py`.
- Expected wall time: ~2 seconds.
- No external endpoints, no downloads besides `paper.pdf` (already cached).
