# LUCID100 — Slot 56 (Wave 6 backfill)

**Paper:** Sangsuwan T, Khavari AP, Blomberg E, Romell T, D'Auria Vieira De Godoy PR, Harms-Ringdahl M, Haghdoost S. *Oxidative Stress Levels and DNA Repair Kinetics in Senescent Primary Human Fibroblasts Exposed to Chronic Low Dose Rate of Ionizing Radiation.* Frontiers in Bioscience (Landmark) **28(11):296** (2023). DOI **10.31083/j.fbl2811296**.

**Master TSV row:** 110 (original rank 87, Wave 6, Tier B, priority 13)
**Replication folder:** `lucid100-senescent-fibroblasts-oxidative-stress-dna-repair-ldrate`
**Started:** 2026-06-09 14:35 CDT · **Completed (first pass):** 2026-06-09 14:40 CDT
**Verdict:** **PARTIAL — numerical-claim consistency replication completed; wet-lab pipeline re-execution NOT feasible.**

## What this study does
Primary VH10 human diploid fibroblasts cultured at three "age" categories:
- **Young (P8)**
- **Middle-aged (P13/P19)**: includes premature-senescent (PS) variants P19-IR (chronically irradiated 8 wk) and P19-ST (6 wk irradiation + 2 wk recovery), with non-irradiated control P19-C
- **Replicatively senescent (P23)**

Chronic low-dose-rate (LDR) γ exposure via a custom 137-Cs incubator at **12 mGy/h** for up to 8 weeks. Endpoints:
1. Population doublings under LDR (P8 vs P13)
2. Extracellular **8-oxo-dG** ELISA in conditioned medium (oxidative stress)
3. **HO1** and **hMTH1** Western blot
4. **γH2AX foci / cell** at 0, 45 min, 24 h, 48 h post acute 1 Gy (DNA repair kinetics)
5. **FISH-telomere / γH2AX** co-localization → telomere dysfunction-induced foci (TIFs)
6. **SA-β-gal** staining, **P21** Western, **T/S ratio** qPCR (senescence characterization)

## Worktype retag (important)
Master TSV labels this as `simulation/model replication`. **That label is incorrect.** This paper is **wet-lab radiobiology** — no model, no code, no Monte Carlo, no Geant4/TOPAS/MCDS. **Recommended retag → `wet-lab assay / radiobiology · DNA repair kinetics · oxidative stress · senescence phenotype`** with QA decision **`KEEP_REDUCED: numerical-claim verification + sensitivity analysis`**.

## Public artifacts
- Full PDF (open access, CC BY 4.0): `data/fbl2811296.pdf` (7.0 MB)
- Supplement ZIP (Figs 1–6 hi-res JPEGs only): `data/supplement.zip` (4.1 MB)
- Supplementary Material PDF (ANOVA tables S1, S2): `data/supplement_attachment.pdf` (251 KB)
- **Raw data:** NOT publicly deposited; author statement says "available upon request." No GEO/SRA/Zenodo/Figshare/GitHub.
- **Code:** None released by authors.

## What was replicated
| Endpoint | Approach | Outcome |
|---|---|---|
| γH2AX repair kinetics — qualitative ordering | Re-test of published means±SE | **4/4 PASS** (P8 returns to baseline; P23 & P19 retain damage) |
| Table 1 — 24 pairwise TIF comparisons | Welch t-test from means±SE assuming reported n=3 | 0/24 exact-bin match · 17/24 "soft" agreement (right direction) |
| 8-oxo-dG slope tests (3 reported comparisons) | Welch t-test from means±SE assuming n=3 | 0/3 reproduce reported p directly at n=3 |
| Effective-n sensitivity analysis | Search min `n` for reported bin to reproduce | **n_eff ∈ [6,14]** for all reported bins ⇒ entirely consistent with foci scoring on tens of cells per "experiment", or 8 weeks × 3 reps per group for slope tests |
| Figure reconstruction | Replot Figs 3A, 5A/B, 6A from text values | 3 PNG figures match published shapes/orderings |

## Layout
```
.
├── README.md                       ← this file
├── PROGRESS.md                     ← time-stamped log
├── ARTIFACT_MANIFEST.md            ← every file + URL + extracted numeric claims
├── FIRST_PASS_REPORT.md            ← top-line verdict
├── REPORT.md                       ← full replication report
├── data/
│   ├── fbl2811296.pdf, .txt
│   ├── supplement.zip
│   └── supplement_attachment.pdf, .txt
├── code/
│   ├── 01_smoke_replication.py     ← Welch t-tests for Table 1, 8-oxo-dG; qualitative kinetics check
│   ├── 02_sensitivity_n.py         ← effective-n needed to reproduce reported significance bins
│   └── 03_figures.py               ← reconstruct Figs 3A, 5A/B, 6A
├── figures/
│   ├── fig3_oxodg.png
│   ├── fig5_gh2ax_kinetics.png
│   └── fig6_tifs.png
└── results/
    ├── smoke_replication_results.json
    ├── table1_tif_replication.csv
    └── sensitivity_n.json
```

## Repro
```bash
cd lucid100-senescent-fibroblasts-oxidative-stress-dna-repair-ldrate
python3 code/01_smoke_replication.py
python3 code/02_sensitivity_n.py
python3 code/03_figures.py
```
Only `numpy`, `scipy`, `matplotlib`. No heavy compute; runs in seconds on CherryRd CPU.

## Next actions (if expanded)
1. **Author contact** (per master policy: **NOT done in this pass**) — would unlock per-replicate foci counts, 8-oxo-dG ELISA OD, T/S ratios.
2. **Pipeline twin** — if microscopy images become available, hook into `lucid-autofoci-detection` for γH2AX foci counting and recompute kinetics from images.
3. **Compare to companion LUCID papers** — Acheva (LUCID-Acheva-2017), Mariotti (lucid-mariotti-split-dose-gamma-h2ax), Grandt (lucid-grandt-fibroblast-rnaseq) all touch the same fibroblast / γH2AX / dose-rate biology and could be cross-validated for consistent slow-repair / persistent-damage signatures.
4. **Update master QA**: change worktype to wet-lab radiobiology; status `partial_numerical_check`.
