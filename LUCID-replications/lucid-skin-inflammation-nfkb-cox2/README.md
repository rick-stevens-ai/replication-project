# Spot-check replication — Acheva et al. 2017 (3D organotypic skin, NF-κB / COX-2)

**Target paper.**
Acheva A, Schettino G, Prise KM. *Pro-inflammatory signaling in a 3D organotypic
skin model after low LET irradiation — NF-κB, COX-2 activation, and impact on
cell differentiation.* Frontiers in Immunology 8:82 (2017).
DOI: [10.3389/fimmu.2017.00082](https://doi.org/10.3389/fimmu.2017.00082).
Open access (CC-BY).

## What this is

The paper is **almost entirely wet-lab** (3D organotypic raft cultures of
N/TERT-1 keratinocytes + J2-3T3 fibroblasts on collagen, 225 kVp X-ray
irradiation with partial Pb shielding, qRT-PCR / western / IHC / ELISA /
MTT). There is **no public dataset** to re-analyze, no equations of motion
to integrate, and no genomic deposit (GEO/ArrayExpress/etc.) referenced. We
classified this as a **SPOT-CHECK** target: we cannot re-run the experiments,
but we *can*:

1. Digitize the published bar charts (Figs 1, 2, 7) and reconstruct samples
   that match the printed means + SEMs + Ns.
2. Re-do the authors' one-way ANOVA + Tukey HSD on the reconstructed data
   and verify that the printed significance asterisks survive.
3. Re-fit the dose-response curves (MTT cytotoxicity) with a 4-parameter
   logistic to estimate IC50 values that the paper does not report
   explicitly, and confirm that the authors' chosen working concentrations
   (5 µM sc-236, 1 µM Bay 11-7085) sit on safe parts of those curves.
4. Verify the explicit text claim that PGE2 at 72 h post-2 Gy is **6.5× over
   the non-irradiated baseline**.
5. Confirm the 2^-ΔΔCT identity used for relative qPCR quantification.

## Repo layout

```
.
├── README.md                  this file
├── PROGRESS.md                running log
├── REPORT.md                  full replication verdict
├── source.pdf                 local copy of the open-access PDF
├── code/
│   ├── digitized_figures.py   means/SEMs/Ns read from Figs 1, 2, 7
│   ├── replicate_stats.py     ANOVA+Tukey audit, 4PL fit, fold check
│   └── make_figures.py        side-by-side overlay plots
├── figures/
│   ├── extracted/             pdfimages output (raw figure rasters)
│   ├── pages/                 200-dpi page renders used for digitization
│   ├── fig1_digitized_overlay.png
│   ├── fig2_dose_response_fits.png
│   └── fig7_pge2_overlay.png
└── results/
    └── spotcheck_results.json
```

## How to reproduce

```bash
python3 code/replicate_stats.py     # writes results/spotcheck_results.json
python3 code/make_figures.py        # writes figures/fig{1,2,7}*.png
```

Dependencies: `numpy`, `scipy>=1.7` (for `scipy.stats.tukey_hsd`), `matplotlib`.

## Honesty disclaimer

- All input numerical values were **digitized visually** from the published
  figures, with no access to author raw data. SEMs were estimated from
  error-bar half-heights against the y-axis gridlines. Typical uncertainty
  on each digitized value is on the order of one minor gridline (~5 % of the
  axis range).
- The Ns and statistical tests we use match what the authors print in their
  figure captions verbatim (`n = 3` for Fig 1, `n = 2` for Figs 2 and 7,
  ANOVA + Tukey, SEM error bars).
- We did **not** contact the authors and did not use any non-public data.

See `REPORT.md` for the full verdict and what we found.
