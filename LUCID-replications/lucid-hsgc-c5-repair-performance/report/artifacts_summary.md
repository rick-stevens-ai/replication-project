# Artifacts Summary — Sakata et al. 2021 (HSGc-C5)

## Directory layout

```
lucid-hsgc-c5-repair-performance/
├── REPORT.md                          # top-level narrative (2026-05-30 + 2026-06-23 re-pass)
├── PARSER_PROVENANCE.md               # Marker parse provenance
├── data/
│   ├── paper.pdf                      # 737,445 B, sha-named
│   ├── paper.txt                      # 930 lines, pdftotext -layout
│   ├── marker/
│   │   ├── paper.md                   # 380 lines, Marker output
│   │   └── paper_meta.json            # TOC + page stats
│   ├── supplement.zip                 # 3590 B from MDPI
│   └── supplement/
│       ├── SF.csv                     # 25 rows (HSG + NB1, both PMMAs)
│       ├── FAR.csv                    # 18 rows
│       └── DepthDose.csv              # 15 rows (0-35 mm)
├── code/
│   ├── tlk_model.py                   # TLK ODE + Eq 7 FAR model
│   ├── replicate.py                   # forward run w/ paper Table 1
│   ├── refit.py                       # joint NLS refit
│   ├── finalize.py                    # combined + figures
│   └── repass/
│       ├── m1_halflives.py
│       ├── m2_bragg_peak.py
│       ├── m3_dsb_arithmetic.py
│       └── m9_nb1rgb_appendixA.py
├── results/
│   ├── sf_pred_Table1.csv
│   ├── sf_pred_refit.csv
│   ├── far_pred_Table1.csv
│   ├── far_pred_refit.csv
│   ├── metrics_summary.json
│   ├── refit.json
│   └── repass/
│       ├── m1_halflives.json
│       ├── m2_bragg_peak.json
│       ├── m3_dsb_arithmetic.json
│       └── m9_nb1rgb_appendixA.json
├── figures/
│   ├── sf_curve.png
│   ├── far_curve.png
│   ├── params_compare.png
│   └── repass/
│       ├── m2_depth_dose.png
│       └── m9_nb1rgb_figA1.png
├── extraction/
│   └── nougat.mmd                     # stub (Marker used instead)
└── report/                            # this backfill pass, 2026-07-05
    ├── REPORT.tex
    ├── open_questions.json            # 5 open questions, machine-readable
    ├── open_questions_section.tex     # \input'd by REPORT.tex
    ├── workflow.md
    ├── artifacts_summary.md           # this file
    └── failure_analysis.md
```

## Artifact provenance

| Artifact | Size / rows | Origin | sha256 or verifier |
|---|---|---|---|
| `data/paper.pdf` | 737,445 B | LUCID sha-named target | pinned in REPORT.md |
| `data/marker/paper.md` | 65,254 B | uicgpu Marker batch 2026-06-22 | `8bc885e4…` |
| `data/supplement.zip` | 3,590 B | MDPI open supplement, 200 OK | `res.mdpi.com` |
| `data/supplement/SF.csv` | 25 rows | zip extraction | rows verify against paper Fig 5 |
| `data/supplement/FAR.csv` | 18 rows | zip extraction | rows verify against paper Fig 5 |
| `data/supplement/DepthDose.csv` | 15 rows | zip extraction | argmax = 33 mm (matches paper claim) |
| `results/metrics_summary.json` | JSON | `code/finalize.py` | SF R²=0.91 (Table 1), 0.96 (refit) |
| `results/refit.json` | JSON | `code/refit.py` | 22 nfev, TRF, converged |
| `results/repass/m1_halflives.json` | JSON | `code/repass/m1_halflives.py` | 12.378 min / 70.015 h |
| `results/repass/m2_bragg_peak.json` | JSON | `code/repass/m2_bragg_peak.py` | 33.0 mm (exact) |
| `results/repass/m3_dsb_arithmetic.json` | JSON | `code/repass/m3_dsb_arithmetic.py` | 6/7 pass, 1 near-miss |
| `results/repass/m9_nb1rgb_appendixA.json` | JSON | `code/repass/m9_nb1rgb_appendixA.py` | Table A1 forward: SF R²=-3.20 |

## Backfill artifacts (2026-07-05, this pass)

7 files added under `report/` and `extraction/`:

1. `report/REPORT.tex` — LaTeX report with genuine Critique section (6 critiques) and `\input{open_questions_section.tex}` at end.
2. `report/open_questions.json` — bare JSON list of 5 open-question objects `{q, basis, next_steps}`.
3. `report/open_questions_section.tex` — 5 enumerated open questions matching the JSON.
4. `report/workflow.md` — stage-by-stage pipeline documentation.
5. `report/artifacts_summary.md` — this file.
6. `report/failure_analysis.md` — honest critique of what was done vs paper's headline.
7. `extraction/nougat.mmd` — stub (Marker was used instead of Nougat; noted).

Top-level `REPORT.md` is PRESERVED unchanged.

## Reproduction one-liner

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-hsgc-c5-repair-performance
python3 code/finalize.py                       # HSGc-C5 core
python3 code/repass/m1_halflives.py            # half-life arithmetic
python3 code/repass/m2_bragg_peak.py           # Bragg-peak
python3 code/repass/m3_dsb_arithmetic.py       # DSB / lethality arithmetic
python3 code/repass/m9_nb1rgb_appendixA.py     # NB1RGB Appendix A
```

Deps: numpy, scipy, pandas, matplotlib.
