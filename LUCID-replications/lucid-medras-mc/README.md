# LUCID Replication — Medras-MC

Replication of:

> **McMahon SJ, Prise KM (2021).** *A Mechanistic DNA Repair and Survival Model
> (Medras): Applications to Intrinsic Radiosensitivity, Relative Biological
> Effectiveness and Dose-Rate.* Frontiers in Oncology 11:689112.
> [doi:10.3389/fonc.2021.689112](https://doi.org/10.3389/fonc.2021.689112)

Public code: <https://github.com/sjmcmahon/Medras-MC> (BSD-2-Clause, declared in
per-file headers).

## What we did

1. Cloned `Medras-MC` and verified the license/data are open.
2. Ran the shipped example entry point `damagegenerator.damageModel.basicXandIon()`
   to generate **23 SDD damage files** spanning X-rays (1–8 Gy), protons (10
   LETs from 1.77 to 29.78 keV/μm), and carbon ions (7 LETs from 20.3 to
   512 keV/μm).
3. Ran `repairanalysis.medrasrepair.repairSimulation(..., 'Fidelity')` with the
   default model parameters (`repeats=50`, `repairFailure=True`,
   `addFociDelay=True`).
4. Parsed the per-file summary lines and the per-0.1-h kinetics traces,
   generated three figures, and benchmarked against numbers quoted in the
   paper.

## Headline result

| Observable | Paper value | Medras-MC (our run) |
|---|---|---|
| DSBs per Gy per cell (X-ray, 1 Gy) | 35 | **33.0** |
| Complex-damage fraction p_complex | 0.43 ± 0.02 | **0.40 – 0.45** across all conditions |
| Misrepair fraction, X-ray 1 Gy | low single-digit % | **4.4 %** |
| Misrepair, Carbon 152 keV/μm, 1 Gy | high (drives RBE peak) | **44 %** |
| Misrepair, Carbon 512 keV/μm, 1 Gy | very high (Bragg overkill) | **87 %** |
| Inter-chromosome misrepair fraction | falls with LET (track confinement) | 0.107 (X-ray) → 0.0006 (Carbon 512) ✅ |

All trends in the paper's mechanistic narrative are reproduced.

## Layout

```
lucid-medras-mc/
├── README.md                  # this file
├── PROGRESS.md                # phase tracker
├── REPORT.md                  # full claim-by-claim replication report
├── mcmahon_prise_2021.pdf     # local copy of the target paper
├── Medras-MC/                 # upstream public repo (BSD-2-Clause)
├── scripts/
│   ├── run_generate_damage.py # step 1: produce 23 SDD files
│   ├── run_repair_analysis.py # step 2: Fidelity analysis
│   └── parse_and_plot.py      # step 3: parse log, write CSV & plots
├── logs/
│   ├── 01_generate_damage.log
│   ├── 02_repair_fidelity.log
│   └── 03_parse_and_plot.log
├── results/
│   ├── sdd_basicXandIon/      # 23 SDDv1.0 damage files
│   └── fidelity_summary.csv   # tidy per-condition summary
└── figures/
    ├── misrepair_vs_LET.png
    ├── repair_kinetics.png
    └── misrepair_vs_dose_xray.png
```

## Reproduce

```bash
cd lucid-medras-mc
python3 scripts/run_generate_damage.py        # ~2 min
python3 scripts/run_repair_analysis.py        # ~2.5 min
python3 scripts/parse_and_plot.py             # <5 s
```

Python deps: `numpy scipy openpyxl matplotlib` (already in any LUCID env).
No GPU. No external network access required after the initial `git clone`.
