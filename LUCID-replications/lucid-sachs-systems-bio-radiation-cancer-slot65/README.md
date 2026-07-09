# LUCID100 Slot 65 — Systems Biological & Mechanistic Modelling of Radiation-Induced Cancer

- **DOI:** 10.1007/s00411-007-0150-z
- **Citation:** Little MP, Heidenreich WF, Moolgavkar SH, Schöllnberger H, Thomas DC.
  "Systems biological and mechanistic modelling of radiation-induced cancer."
  *Radiation and Environmental Biophysics* (2008) 47:39–47.
- **Type:** Workshop overview / review (5 talks at the 1st Int'l Workshop on Systems Radiation Biology,
  GSF Neuherberg, 14–16 Feb 2007).
- **LUCID worktype assigned:** simulation/model replication
- **LUCID rank:** 96 (Wave 7, slot 65) — backfill.
- **Master TSV note:** "KEEP: relevant and replication-plausible".

## Paper character — important framing

This paper is **not a primary modelling paper**. It is a 9-page narrative summary of *five*
distinct presentations, each of which references its own previously published primary model:

| § | Presenter | Model | Primary citation in paper |
|---|-----------|-------|---------------------------|
| 1 | Moolgavkar | Stochastic clonal expansion / TSCE (MVK) examples (gestational mutations; heterogeneity; in-host cell dynamics) | Refs [1,2,4,5] |
| 2 | Heidenreich | Two-step TSCE applied to radon-exposed rats, JANUS mice, Thorotrast — initiation vs initiation+promotion (I vs IP) | Refs [15–27] |
| 3 | Little | Generalized MVK with *k* cancer-stage + *m* destabilizing mutations; fit to SEER colon cancer | Refs [36, 40] |
| 4 | Schöllnberger | State-Vector Model (SVM) — deterministic multistage with protective bystander apoptosis (rate `kap`) | Refs [50, 51] |
| 5 | Thomas | Hierarchical logistic regression of ATM/BRCA variants × radiation in the WECARE bilateral breast-cancer case-control study | Refs [64–66] |

The paper itself contains:
- Schematic of generalized MVK (Fig. 3) with k×m grid of states.
- Two data-fit figures from Heidenreich's primary work (Figs 1, 2 — rat radon ERR; mouse JANUS lung-cancer counts).
- One data-fit figure from Little & Li 2007 (Fig. 4 — SEER colon-cancer hazards by sex, 5 model variants).
- One data-fit figure from Schöllnberger et al. 2007 (Fig. 5 — CGL1 transformation freq vs γ dose for delayed vs immediate plating, showing direct, bystander, total).
- **No fully written equation sets** (only the single Thomas logistic-regression skeleton:
  `logit Pr(Yᵢ = 1) = α + Σⱼ βⱼ Xᵢⱼ + γ Zᵢ`).
- One isolated numerical parameter: SVM `kap = 0.054 /day` (delayed plating, 95% CI 0.031–0.078)
  and `kap = 0.022 /day` (immediate plating, 95% CI 0.007–0.036).

→ A full replication of any *one* of the five primary models is a slot in itself
(in fact, several of those primary papers — Schöllnberger 2007 *Radiat Res* 168:614,
Little & Wright 2003 *Math Biosci* 183:111, Luebeck-Moolgavkar 2002 *PNAS* 99:15095 —
are independent candidates already curated or coverable elsewhere in LUCID).
This slot's *minimum-useful* replication is therefore:
1. Reproduce the **two-stage MVK survival-hazard formulation** (the workhorse common
   to all three stochastic talks) and produce a synthetic age-incidence curve qualitatively
   matching the shape of Fig. 4 (Little & Li 2007 SEER colon cancer).
2. Reproduce the **SVM single-parameter behaviour** of `kap`: an analytical sketch
   showing how a protective bystander-apoptosis rate can drive transformation frequency
   below the no-radiation baseline at low doses (the Redpath/U-shape phenomenon).

Both are smoke-scale, finish in seconds on a laptop, and do not need CherryRd heavy compute.

## Repository layout

```
lucid-sachs-systems-bio-radiation-cancer-slot65/
├── README.md                         # this file
├── PROGRESS.md                       # chronological journal
├── ARTIFACT_MANIFEST.md              # what we have, where it came from
├── FIRST_PASS_REPORT.md              # verdict, scope, retag recommendation
├── artifacts/
│   ├── paper.pdf                     # full open-access PDF (Springer)
│   ├── paper.txt                     # pdftotext extract
│   └── page_headers.txt              # HTTP headers from springer probe
├── code/
│   └── smoke_replication.py          # MVK hazard + SVM bystander sketch
└── reports/
    └── smoke_run.txt                 # captured stdout from the smoke script
```

## Reproduce

```bash
cd code
python3 smoke_replication.py | tee ../reports/smoke_run.txt
# produces ../reports/mvk_hazard.png and ../reports/svm_bystander.png
```

Requires only numpy + matplotlib (no GPU, no licensed code, no internet).

## Status (one-liner)

First-pass artifact harvest + minimal smoke replication complete; verdict **PARTIAL**
(scoping-quality reproduction only; full per-talk replication out of scope —
recommend QA retag to `done-partial / scope=review-paper`).
