# LUCID100 #69 (Wave 4) — Scott 2011 Epicellcom DSB Repair Kinetics

**Paper.** Bobby R. Scott. *Modeling DNA Double-Strand Break Repair Kinetics as an Epiregulated Cell-Community-Wide (Epicellcom) Response to Radiation Stress.* Dose-Response **9**:579–601 (2011). **DOI:** [10.2203/dose-response.10-039.Scott](https://doi.org/10.2203/dose-response.10-039.Scott). PMCID: [PMC3315173](https://pmc.ncbi.nlm.nih.gov/articles/PMC3315173/).

**LUCID100 master row.** Rank 69 · Wave 4 · Tier A · priority 14 · `omics/signature replication` (master tag — **wrong, see QA retag below**).

**Verdict.** **REPLICATED (model + figures).** Pure-Python re-implementation of MULTISIG1 equations 3, 5, 6, 8, 10, 11, 12, 13, 14. All five model figures (Fig 1–Fig 5) reproduced from the published parameter values; 6 of 7 spot-checks agree exactly with paper-stated numbers, the 7th exposes an off-by-one labeling error in the paper text on p. 589 (see `REPORT.md`).

**QA retag recommendation.** **Change `worktype` from `omics/signature replication` → `model / equations replication` (computational kinetic model).** This paper has no -omics data, no signatures, no biomarker panels. It is a closed-form mathematical model (Poisson-gamma DSB repair kinetics) parameterised against γ-H2AX dissolution data from Rothkamm & Löbrich (2003). Master row 87 in `LUCID100_SOLID_MASTER_QA.tsv` should be updated.

## Replication target

Five model figures from the paper, all derivable from the closed-form equations using the parameter set quoted in the text (pp. 587, 592):

| Parameter | Value          | Source quoted in paper                          |
| --------- | -------------- | ----------------------------------------------- |
| `B_T`     | 0.10 foci/cell | Rothkamm & Löbrich 2003 (F_min)                 |
| `α`       | 0.035 / mGy    | Rothkamm & Löbrich 2003 slope                   |
| `T`       | 1.4 mGy        | Scott 2010 (threshold)                          |
| `β`       | 2.5 h          | Scott 2010 fit (range 0.5–4.5 h)                |
| `m`       | 46             | DNA molecules per nucleus                       |
| `B_0`     | 0.05 foci/cell | R&L 2003 baseline (Fig 5 control line)          |

## Reproduce

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-epicellcom-dsb-repair-kinetics
python3 code/replicate_figures.py
```

Outputs land in `figures/` (PNGs) and `results/` (`summary.json`, `fig5_RB.csv`).

Pure Python + NumPy + Matplotlib. No GPU, no heavy compute, no external services.

## Layout

```
.
├── README.md                ← this file
├── PROGRESS.md              ← timeline + status
├── REPORT.md                ← scoping + first-pass results + paper-typo finding
├── ARTIFACT_MANIFEST.json   ← inventory
├── code/
│   ├── multisig1.py         ← model equations (Eq 3, 5, 6, 8, 10, 11, 12, 13, 14)
│   └── replicate_figures.py ← regenerates Fig 1–Fig 5
├── data/
│   ├── scott2011_epicellcom.pdf   ← author PDF (EuropePMC mirror, PMC3315173)
│   └── scott2011_epicellcom.txt   ← pdftotext extract used for equation/parameter audit
├── figures/
│   ├── fig1_phi_n.png       ← per-molecule repair-time densities φ₁..φ₄
│   ├── fig2_attributions.png← attributions Att_n(D) up to 1000 mGy
│   ├── fig3_Psi_n.png       ← cumulative per-molecule repair Ψ₁..Ψ₄
│   ├── fig4_Cum.png         ← Poisson-weighted Cum(t,D) at 100 and 1000 mGy
│   └── fig5_residual_DSBs.png ← residual DSBs/cell vs time, 0/5/20/100/200 mGy
└── results/
    ├── summary.json         ← parameters + spot-check values
    └── fig5_RB.csv          ← numerical table for Fig 5
```

## Status

* ✅ PDF harvested (EuropePMC mirror — Sage paywall blocked direct DOI fetch)
* ✅ Model fully re-implemented in pure Python (no external solver required)
* ✅ Five model figures regenerated
* ✅ 6/7 spot-checks against paper-stated numerics match exactly
* ⚠️ **Paper labeling typo identified** at Att_n(1000 mGy): paper text on p. 589 reports Att_2 = 46.7 % but Eq 10 with stated parameters yields Att_1 = 46.67 %, Att_2 = 35.57 %. Att_3 = 13.55 % and Att_4 = 3.44 % match the paper (13.6 %, 3.4 %), confirming the off-by-one is in the body text, not in the underlying calculation. Details in `REPORT.md`.
* ⛔ Wet-lab data (Rothkamm & Löbrich 2003 γ-H2AX foci curves) not digitised in this pass — the smoke replication validates the *model itself* against the paper's own stated numerics, not against R&L raw data. Curve overlay vs digitised R&L data is the obvious next step.

## Author contact / paid endpoints

None used. PMC mirror only.
