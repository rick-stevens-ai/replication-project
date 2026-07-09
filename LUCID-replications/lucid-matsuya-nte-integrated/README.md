# LUCID Replication: Matsuya et al. 2018 — IMK (Integrated MK) Model

Independent open replication of:

> Matsuya Y, Sasaki K, Yoshii Y, Okuyama G, Date H.
> *Integrated Modelling of Cell Responses after Irradiation for
> DNA-Targeted Effects and Non-Targeted Effects.*
> Scientific Reports 8: 4849 (2018).  DOI: 10.1038/s41598-018-23202-y.

## What's in this directory

```
lucid-matsuya-nte-integrated/
├── README.md                       this file
├── REPORT.md                       claim-by-claim agreement table + verdict
├── PROGRESS.md                     phase log + friction tags
├── paper.pdf                       the target paper (CC-BY, local copy)
├── source-paper.txt                pdftotext extraction
├── artifacts/
│   ├── MOESM1.pdf                  Springer ESM #1 (supplementary information)
│   └── MOESM1.txt                  pdftotext extraction of supplement
├── code/
│   ├── imk_model.py                NumPy/SciPy implementation of IMK Eqs. 1-26
│   ├── reference_data.py           digitised data from paper figures (~5-10% precision)
│   └── make_figures.py             generates all figures and results/summary.json
├── figures/
│   ├── fig0_signal_vs_dose.png     LQ-weighted hit probability (claim 1)
│   ├── fig1_signal_kinetics.png    calcium & NO temporal profiles (paper Fig 2A)
│   ├── fig2_dsb_kinetics.png       DSB kinetics TE-only vs TE+NTE (paper Fig 2B)
│   ├── fig3_survival_HRS.png       V79-379A & T-47D survival w/HRS (paper Fig 2C-D)
│   ├── fig4_mtbe.png               HPV-G & E48 MTBE (paper Fig 3)
│   ├── fig5_cho_repair_inhibition.png  CHO sham vs PARP-inhibited (paper Fig 4)
│   └── fig6_hrs_repair_scan.png    HRS depth vs c_b factor (paper Fig 5B)
├── results/
│   └── summary.json                R² metrics + fitted parameters
└── logs/
    └── run1.log, run2.log          stdout from figure runs
```

## TL;DR result

- **Coverage:** 10/10 explicit paper claims attempted.
- **Agreement:** ~70% (4 REPLICATED, 1 REPLICATED-qualitative, 2 SPOT-CHECK,
  2 PARTIAL, 1 CONTRADICTED — see REPORT.md).
- **Central claim** (lower repair efficiency in non-hit cells reproduces
  HRS + MTBE) is **REPLICATED** at the qualitative + structural level.
- Three numerical inconsistencies found *inside the paper* (Claims 1, 5, 10).

## How to reproduce

```bash
cd code/
python3 make_figures.py
```

CPU only. Runtime ~4 s. Requires numpy, scipy, matplotlib.
