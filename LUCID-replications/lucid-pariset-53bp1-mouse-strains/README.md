# LUCID replication: Pariset et al. 2020 — 53BP1 Repair Kinetics, 15 Mouse Strains

**Paper:** Pariset E, Penninckx S, Degorre Kerbaul C, Guiet E, Lopez Macha A,
Cekanaviciute E, Snijders AM, Mao J-H, Paris F, Costes SV.
*53BP1 Repair Kinetics for Prediction of In Vivo Radiation Susceptibility in 15
Mouse Strains.* Radiat. Res. 194, 485–499 (2020).
**DOI:** [10.1667/RADE-20-00122.1](https://doi.org/10.1667/RADE-20-00122.1)

**Verdict:** PARTIAL — analytical core replicated; wet-lab and in-vivo data not
deposited so not reproducible without author contact.

**Coverage / agreement:** 6 / 10  ·  8 / 10

## TL;DR

- The paper proposes a new exponential-decay model for 53BP1 repair kinetics
  in mouse fibroblasts (Eqs. 1–6). We re-implemented the model and verified its
  identifiability via Monte-Carlo simulation.
- The paper's headline correlation, **r = −0.75** between repair time constant τ
  and repaired fraction q at 4 Gy X-ray across 15 strains (Table 1B), is
  reproduced as **r = −0.76 (p = 0.001)** from per-strain values digitized from
  Fig. 4. Exact agreement.
- No supplementary data file is published with the paper. Per-strain numerical
  values exist only in Fig. 4 bar charts; raw 53BP1 foci counts and in-vivo
  outcome data are not deposited.

## Layout

```
.
├── README.md                    ← this file
├── REPORT.md                    ← full replication report (what / how / verdict)
├── PROGRESS.md                  ← work log
├── code/
│   └── replicate_pariset.py    ← model + replication
├── data/
│   ├── paper.pdf
│   ├── digitized_fig4.csv      ← per-strain τ, q (HZE and X-ray), n=15
│   ├── table1_paper_reported.csv
│   └── fig7c_cancer_correlations.csv
├── figures/
│   ├── fig4_recreated.png      ← our bar charts from digitized values
│   └── model_kinetics_examples.png
└── results/
    └── replication_results.txt
```

## Reproduce

```bash
cd code
python3 replicate_pariset.py
```

Requires numpy, scipy, matplotlib. No network calls.

## Caveats

1. Per-strain τ/q values are vision-digitized from Fig. 4 with ~10% uncertainty.
2. The paper makes no statistical correction for multiple comparisons in
   Fig. 7C (n=4 strains, 27 organs).
3. The MTB cancer-incidence data used in Fig. 7C is of unspecified vintage
   and cannot be re-derived exactly.
