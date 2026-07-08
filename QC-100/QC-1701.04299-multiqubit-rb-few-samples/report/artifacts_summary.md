# Artifacts summary — QC-1701.04299-multiqubit-rb-few-samples

## Directory layout
```
QC-1701.04299-multiqubit-rb-few-samples/
├── work/
│   ├── 1701.04299.pdf                  # source paper (arXiv v3)
│   └── 1701.04299.txt                  # pdftotext extract
├── extraction/
│   └── nougat.mmd                      # ML-OCR stub (see note below)
├── code/
│   ├── rb_2qubit.py                    # 2q Clifford RB sim + bootstrap
│   ├── paper_bound.py                  # eq. (10) closed-form + Chebyshev
│   └── plot_results.py                 # figure generation
├── report/
│   ├── REPORT.md                       # human-readable canonical report
│   ├── REPORT.tex                      # LaTeX packaged version (this backfill)
│   ├── workflow.md                     # pipeline provenance
│   ├── artifacts_summary.md            # THIS FILE
│   ├── failure_analysis.md             # honest critique + untested items
│   ├── open_questions.json             # 5 open follow-up questions (bare list)
│   ├── open_questions_section.tex      # LaTeX rendering of open questions
│   └── evidence/
│       ├── rb_raw_survivals.json       # 900 survival probabilities (9m × 100N)
│       ├── rb_bootstrap_summary.json   # bootstrap table + full-N fit
│       ├── paper_bound_comparison.json # eq. (10) vs paper's N=173
│       ├── rb_decay.png                # A f^m + B decay fit figure
│       ├── r_vs_N.png                  # bootstrap r vs N figure
│       ├── rel_std_vs_N.png            # relative std vs N figure
│       ├── rb_run.log                  # rb_2qubit.py stdout
│       └── bound_run.log               # paper_bound.py stdout
└── venv/                               # local Python 3.13 env (not committed)
```

## Artifact-by-artifact table

| Artifact | Purpose | Author | Provenance |
|---|---|---|---|
| `work/1701.04299.pdf` | Source paper | arXiv | Downloaded 2026-07-03 |
| `code/rb_2qubit.py` | 2q RB sim + bootstrap | Replication subagent | Hand-written 2026-07-03 |
| `code/paper_bound.py` | Eq. (10) closed-form | Replication subagent | Hand-written 2026-07-03 |
| `code/plot_results.py` | Figures | Replication subagent | Hand-written 2026-07-03 |
| `report/evidence/rb_raw_survivals.json` | 900 survivals | Aer simulator | Direct output of rb_2qubit.py |
| `report/evidence/rb_bootstrap_summary.json` | Bootstrap table | scipy | Direct output of rb_2qubit.py |
| `report/evidence/paper_bound_comparison.json` | Bound reproduction | numpy | Direct output of paper_bound.py |
| `report/evidence/*.png` | Figures | matplotlib | Direct output of plot_results.py |
| `report/REPORT.md` | Canonical report | Replication subagent | Hand-written 2026-07-03 |
| `report/REPORT.tex` | LaTeX version | Backfill subagent | 2026-07-06, no numeric changes |
| `report/open_questions.json` | 5 follow-ups | Backfill subagent | 2026-07-06 |
| `extraction/nougat.mmd` | ML-OCR of paper | Backfill stub | Not run (nougat unavailable in scope; see note) |

## What each JSON evidence file contains
- **rb_raw_survivals.json** — dict keyed by m, value = list of 100 survival probabilities.
- **rb_bootstrap_summary.json** — dict with `full_N_fit: {A,B,f,r}` and `bootstrap: [{N, r_mean, r_std, rel_std}]`.
- **paper_bound_comparison.json** — dict with `paper_example: {d,m,r,epsilon,delta,N_paper,N_ours}` and `our_data: {r,m_grid,N_worst}`.

## Notes
- `extraction/nougat.mmd` is a placeholder. Nougat ML-OCR was not run for this paper; `work/1701.04299.txt` (pdftotext extract) served the equation-extraction need for this replication. See stub file for detail.
- The `venv/` directory is ephemeral and not tracked; recreate via commands in `workflow.md`.
- All numeric claims in REPORT.md/REPORT.tex trace back to the JSON files in `report/evidence/`.
