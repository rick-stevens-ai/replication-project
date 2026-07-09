# lucid-fukui-saga-lq-sldr-aldh

LUCID replication of:

> Fukui R., Saga R., Matsuya Y., et al. *Tumor radioresistance caused by
> radiation-induced changes of stem-like cell content and sub-lethal damage
> repair capability.* **Sci Rep 12, 1056 (2022)**. DOI: 10.1038/s41598-022-05172-4.

This package independently re-implements the **IMK (integrated microdosimetric-
kinetic) cell-killing model** (equations 1–15 of the paper) and:

1. Forward-predicts the Fig 5 acute-irradiation survival curves for SAS, SAS-R,
   HSC2, and HSC2-R from Table 1's mean parameters.
2. Compares to vision-digitized data from Fig 5 across ~5 orders of magnitude in
   surviving fraction; R² in −ln S ranges 0.96–0.997.
3. Independently re-runs a Metropolis-Hastings MCMC on the digitized Fig 5
   points (likelihood per Eq 15, uniform priors per Methods) and recovers the
   paper's central claim: **w_SLDR for HSC2-R = 1.93 ± 0.47** (paper: 1.90 ± 0.45),
   **w_SLDR for SAS-R = 1.11 ± 0.20** (paper: 1.06 ± 0.12).

## Layout

```
lucid-fukui-saga-lq-sldr-aldh/
├── README.md           — this file
├── REPORT.md           — full replication report with verdict and tables
├── PROGRESS.md         — running log
├── code/
│   ├── imk_model.py        — IMK equations (1, 2, 4, 6, 7, 12, 13, 14)
│   ├── params_table1.py    — Table 1 verbatim
│   ├── digitized_fig5.py   — vision-digitized Fig 5 survival points
│   ├── replicate_fig5.py   — forward-replicate Fig 5
│   ├── replicate_fig6.py   — forward-replicate Fig 6 split-dose
│   └── refit_mcmc.py       — independent MCMC refit per family
├── data/
│   ├── source-paper.pdf    — local copy of the Sci Rep paper
│   ├── source-paper.txt    — pdftotext extract
│   └── pages/p-*.png       — per-page renderings (used for figure digitization)
├── figures/
│   ├── fig5_replication.png  — model vs. digitized Fig 5
│   └── fig6_replication.png  — predicted split-dose curves
└── results/
    ├── fig5_replication_summary.md
    ├── fig6_replication_summary.md
    ├── mcmc_refit_summary.md
    └── mcmc_refit_summary.json
```

## How to reproduce

```bash
cd code
python3 replicate_fig5.py
python3 replicate_fig6.py
python3 refit_mcmc.py
```

Pure-Python; only `numpy` + `matplotlib` required.

## Verdict

**PARTIAL** (forward-replication strong; MCMC refit qualitatively confirms paper).
Coverage 7/10, agreement 8/10. See `REPORT.md` for details and honest caveats —
particularly that the paper provides no code/data and that the experimental
points are all vision-digitized from the published raster figures.
