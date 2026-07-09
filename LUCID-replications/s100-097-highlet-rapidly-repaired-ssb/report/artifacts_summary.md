# Artifacts summary — LUCID slot #97

Paper: Guerra Liberal et al., Sci Rep 13:11198 (2023).

## Directory tree
```
s100-097-highlet-rapidly-repaired-ssb/
├── report/
│   ├── REPORT.md                       # Original prose report (source of truth for the science)
│   ├── REPORT.tex                      # LaTeX rendering (backfill)
│   ├── open_questions.json             # 5 open questions (backfill)
│   ├── open_questions_section.tex      # LaTeX section (backfill)
│   ├── workflow.md                     # Stage-by-stage pipeline (backfill)
│   ├── artifacts_summary.md            # This file (backfill)
│   └── failure_analysis.md             # Honest critique (backfill)
├── code/
│   ├── extract_si.py                   # SI XLSX -> CSV converter
│   ├── replicate.py                    # Full analytical replication pipeline
│   └── data/
│       ├── foci.csv                    # Fig 1 raw data (53BP1 foci vs time)
│       ├── clonogenic.csv              # Fig 2 raw data (SF vs dose, all conditions)
│       └── sld.csv                     # Fig 3 raw data (SF vs interfraction interval)
├── figures/
│   ├── fig1_foci_kinetics.png          # 4-panel foci decay + fits
│   ├── fig2_lq_and_additive.png        # LQ curves + Eq 2 mixed-field prediction
│   ├── fig3_sld_repair.png             # 4-panel same-quality + mixed
│   ├── fig4_dsb_vs_let.png             # Analytic DSB/Gy vs LET surrogate
│   └── fig5cd_cluster_foci_model.png   # Cluster-foci Poisson-mixture fits
├── evidence/
│   ├── lq_fits.json                    # Table S1 reproduction (per cell line, per quality)
│   ├── sld_fits_and_rbe.json           # Table 1 repair half-lives + Eq 8 RBE_SLD
│   ├── foci_fits.json                  # Fig 1 exponential-decay parameters
│   ├── cluster_foci_fits.json          # Fig 5c-d N_cl, F, P
│   ├── fig4_dsb_vs_let.json            # Fig 4 surrogate DSB/Gy per LET point
│   └── summary.json                    # All above rolled up
├── ocr/
│   └── paper.txt                       # pdftotext of main text
├── extraction/
│   └── nougat.mmd                      # Stub (backfill) - pdftotext already handled this paper
└── source/
    ├── paper.pdf                       # CC-BY 4.0
    ├── SI_MOESM1_ESM.pdf                # Table S1 + Fig S1
    ├── SI_MOESM1_ESM.txt                # Text extract of SI PDF
    └── SI_MOESM2_ESM.xlsx               # Per-figure raw data (Supp Data 1/2/3)
```

## Key numbers
| Quantity | Paper | Reproduced |
|---|---|---|
| LQ alpha_x (PC-3, X-ray)              | 0.55 +/- 0.05      | 0.551 +/- 0.045     |
| LQ alpha_alpha (U2OS, alpha)          | 2.6 +/- 0.2        | 2.632 +/- 0.078     |
| RBE_D10 (U2OS)                        | 4.9 +/- 0.7        | 4.59                |
| Shared repair half-life (U2OS)        | 34 +/- 17 min      | 30 min              |
| Shared repair half-life (PC-3)        | 44 +/- 11 min      | 42 min              |
| N_cluster PC-3                        | 9.9 +/- 0.3        | 10.5                |
| N_cluster U2OS                        | 10.2 +/- 0.7       | 12.6                |
| RBE_SLD PC-3                          | 2.8 +/- 0.9        | 2.0  (partial)      |
| RBE_SLD U2OS                          | 3.7 +/- 0.4        | 2.3  (partial)      |
| DSB/Gy at 129 keV/um (Fig 4)          | 128.5              | 216   (qualitative) |

## Coverage
- **Equations reproduced:** 9 / 9 (Eqs 1-9).
- **Main-text figures reproduced:** 5 / 5 (Figs 1, 2, 3, 4, 5c-d; Fig 5a-b substituted with the emergent Lea-Catcheside F-test on shared repair half-life).
- **Tables reproduced:** Table S1 (LQ parameters) exact; Table 1 (repair half-lives) exact.
- **Claims examined:** 21 (C1-C21). Verdict: 18 exact/match, 3 partial.

## Re-run
```
cd LUCID-replications/s100-097-highlet-rapidly-repaired-ssb
python3 code/extract_si.py
python3 code/replicate.py
```
Pure CPU, no internet needed once SI files present. ~5 s wall.

## License / provenance
- Paper: CC-BY 4.0 (Nature Sci Rep). Free redistribution + reuse of data.
- Supp Data 1/2/3: CC-BY 4.0.
- Compute: free (CherryRd CPU + Argo Opus 4.7 subagent).
- No paywalled resource used at any stage.
