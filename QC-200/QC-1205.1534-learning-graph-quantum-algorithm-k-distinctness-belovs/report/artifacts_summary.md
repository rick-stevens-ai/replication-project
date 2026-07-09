# Artifacts Summary — Belovs 2012 k-distinctness replication

## Directory tree

```
QC-1205.1534-learning-graph-quantum-algorithm-k-distinctness-belovs/
├── paper.pdf                                     [434 KB, 19 pp, arXiv:1205.1534 v2]
├── extraction/
│   ├── marker.md                                 [2.9 KB — pdftotext fallback wrapped w/ headers]
│   ├── marker.raw.txt                            [full pdftotext dump, 1194 lines]
│   └── nougat.mmd                                [stub — Nougat not installed]
├── work/
│   ├── paper.txt                                 [source pdftotext, 1194 lines]
│   └── venv/                                     [Python 3.13 venv, numpy+scipy+matplotlib]
└── report/
    ├── REPORT.tex                                [12.7 KB — main report]
    ├── open_questions.json                       [5 questions, {q, basis, next_steps}]
    ├── workflow.md                               [step-by-step run log]
    ├── artifacts_summary.md                      [this file]
    ├── failure_analysis.md                       [honest failure analysis]
    └── evidence/
        ├── belovs_kdist.py                       [replication code — Eq. 12 optimizer]
        ├── plot_results.py                       [plotting driver]
        ├── belovs_results.json                   [full numerical results, 52 rows]
        └── belovs_replication_plot.png           [2100×900 log-log + bar plot]
```

## Key numerical artifacts

### `report/evidence/belovs_results.json`
- 52 rows: 4 values of k × 13 values of N
- Each row: `{k, n, C_opt, C_ambainis, C_random_best, C_random_mean, r_opt}`
- Per-k summary: `{fitted_rho1, paper_rho1, abs_err_rho1, fitted_ambainis_rho, paper_ambainis_rho, improvement_over_ambainis}`

### Bottom-line numbers

| k | paper ρ₁ | fitted ρ₁ | abs error |
|---|----------|-----------|-----------|
| 2 | 0.6667 (2/3) | 0.6667 | <1e-4 |
| 3 | 0.7143 (5/7) | 0.7143 | <1e-4 |
| 4 | 0.7333 (11/15) | 0.7333 | <1e-4 |
| 5 | 0.7419 (23/31) | 0.7419 | <1e-4 |

### Reproducibility

To rerun from scratch (assuming a fresh shell, no local artifacts):

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1205.1534-learning-graph-quantum-algorithm-k-distinctness-belovs
python3 -m venv work/venv
source work/venv/bin/activate
pip install numpy scipy matplotlib
python3 report/evidence/belovs_kdist.py   # → belovs_results.json  (~3 s)
python3 report/evidence/plot_results.py   # → belovs_replication_plot.png
# Optional: compile REPORT.tex
pdflatex -output-directory report report/REPORT.tex
```

All optimization uses `scipy.optimize.minimize` (Nelder-Mead) with fixed
per-point RNG seeds derived from `(k, n)`, so results are deterministic
across runs on the same machine.

## Provenance / lineage

- No external data sources beyond the arXiv PDF itself.
- No LLM calls (Rick's standing free-endpoints-only rule: N/A because we
  used no LLM at all).
- No paid APIs.
- All computation local on `CherryRd` (macOS Darwin 25.3.0 x64).

## Traces

- Terminal-session record of the sweep: printed to stdout by
  `belovs_kdist.py`, faithfully reproducible.
- `belovs_results.json` is the machine-readable snapshot of that stdout.
- `belovs_replication_plot.png` is the visual snapshot.
