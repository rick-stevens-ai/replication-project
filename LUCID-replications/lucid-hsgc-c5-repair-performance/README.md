# LUCID replication — HSGc-C5 repair performance (Sakata et al., Cancers 13:6046, 2021)

Re-implements the **two-lesion kinetics (TLK) curve-fit** portion of
Sakata et al. 2021, "Performance Evaluation for Repair of HSGc-C5 Carcinoma
Cell Using Geant4-DNA" (DOI [10.3390/cancers13236046](https://doi.org/10.3390/cancers13236046)),
from the paper's open MDPI supplements.

> **Scope:** the TLK ODE / SF / FAR curve-fit (Eqs 3–7, Figure 5, Table 1).
> The upstream Geant4-DNA track-structure Monte Carlo (Figure 4) is **not**
> re-executed — we consume the paper's reported DSB yields.

## Layout

```
lucid-hsgc-c5-repair-performance/
├── REPORT.md                 ← verdict, coverage, agreement scores
├── README.md                 ← this file
├── PROGRESS.md               ← timestamped work log
├── data/
│   ├── paper.pdf             ← target paper
│   ├── paper.txt             ← pdftotext -layout extract
│   ├── supplement.zip        ← open MDPI supplement (3.5 KB)
│   └── supplement/
│       ├── SF.csv            ← HSG + NB1 cell surviving fractions
│       ├── FAR.csv           ← relative DNA fragment-activity-released kinetics
│       └── DepthDose.csv     ← proton depth-dose (Figure 2)
├── code/
│   ├── tlk_model.py          ← TLK ODE system + random-breakage FAR model
│   ├── replicate.py          ← forward run with paper's Table 1 parameters
│   ├── refit.py              ← joint NLS refit (analogue of paper's Ceres Solver step)
│   └── finalize.py           ← combined run + comparison figures + summary
├── results/
│   ├── sf_pred_Table1.csv    ← model vs measured SF (paper params)
│   ├── sf_pred_refit.csv     ← model vs measured SF (our refit)
│   ├── far_pred_Table1.csv   ← model vs measured FAR (paper params)
│   ├── far_pred_refit.csv    ← model vs measured FAR (our refit)
│   ├── refit.json            ← fitted parameters + diagnostics
│   └── metrics_summary.json  ← RMSE / R² / log10-RMSE per condition + overall
└── figures/
    ├── sf_curve.png          ← SF replication of Fig 5 (left)
    ├── far_curve.png         ← FAR replication of Fig 5 (right)
    └── params_compare.png    ← TLK params: paper vs refit (log bar chart)
```

## Reproduce

```bash
cd code
python finalize.py
```

Requires Python 3.10+ with `numpy`, `scipy`, `pandas`, `matplotlib`.
Tested on Python 3.14 / numpy 2.4 / scipy 1.17 / pandas 3.0 / matplotlib 3.10.

Runtime: ~5 s on a single CPU core.

## Headline results

| Metric (HSGc-C5, 0 + 32 mm PMMA) | Paper Table 1 verbatim | Joint refit |
| --- | --- | --- |
| SF R² | 0.91 | **0.96** |
| SF RMSE | 0.106 | **0.067** |
| SF log₁₀-RMSE | 0.32 | **0.13** |
| FAR R² | 0.72 | **0.96** |
| FAR RMSE | 0.080 | **0.029** |

The paper's published TLK parameters reproduce the measured SF / FAR curves
to within ~30 % log-SF error. A direct refit to the same data improves
agreement to < 15 % log-SF error, at the cost of TLK parameter values that
differ from Table 1 by factors of 0.3 – 5.5 — consistent with the known
degeneracy of the TLK parameter space (only the products γ·η and β·λ are
tightly constrained by SF + FAR data alone).

See `REPORT.md` for the full verdict, evidence, and caveats.
