# Artifact Manifest — LUCID100 Slot 56

**Paper:** Sangsuwan T, Khavari AP, Blomberg E, Romell T, D'Auria Vieira De Godoy PR, Harms-Ringdahl M, Haghdoost S. *Oxidative Stress Levels and DNA Repair Kinetics in Senescent Primary Human Fibroblasts Exposed to Chronic Low Dose Rate of Ionizing Radiation.* Frontiers in Bioscience (Landmark) 28(11):296, 2023.
**DOI:** 10.31083/j.fbl2811296
**Harvested:** 2026-06-09 (Wave 6 backfill, slot 56)
**Open access:** Yes (IMR Press, CC BY 4.0 per journal policy).

## Harvested artifacts (local cache)

| Path | Bytes | Source URL | Notes |
|---|---:|---|---|
| `data/fbl2811296.pdf` | 6,996,942 | https://www.imrpress.com/journal/FBL/28/11/10.31083/j.fbl2811296/pdf | Full article PDF (v1.5). |
| `data/fbl2811296.txt` | 74,213 | local pdftotext | Plain-text extraction. |
| `data/supplement.zip` | 4,093,504 | https://storage.imrpress.com/IMR/FBL19078/application/2768-6698-28-11-296.zip | Hi-res JPEGs of Figs 1–6 only. |
| `data/supplement_attachment.pdf` | 251,154 | https://storage.imrpress.com/journal/FBL/28/11/10.31083/j.fbl2811296/attachment/1ef747378810249a9847a834678a8676.pdf | Supplementary Material PDF: ANOVA tables S1 (PD) and S2 (8-oxo-dG). |
| `data/supplement_attachment.txt` | extracted | local pdftotext | Plain-text supplement. |

## Public data status
- **Raw image / foci / ELISA data:** NOT publicly deposited. Author statement: "The data are available upon request" (article §Availability of Data and Materials).
- **Repositories searched:** No GEO/SRA accession, no Zenodo/Figshare DOI, no GitHub repo mentioned in text.
- **Supplement contents:** Two ANOVA summary tables + 6 figure JPEG re-renders. No per-replicate raw values, no source data tables.

## Key reproducible numeric claims extracted from text
(See `data/extracted_numbers.json` produced by `code/01_extract_numbers.py`.)

1. **Population doubling (PD) totals over 9 weeks**, P8 vs P13, control vs 12 mGy/h:
   - P8 control: 18.05 ± 0.25 (n=3); P8 LDR: 11.52 ± 0.05
   - P13 control: 11.70 ± 0.40; P13 LDR: 6.17 ± 0.50
   - Reported tests: PD difference vs control becomes significant at week 8 (p=0.04) and week 9 (p=0.02) for the P13 LDR vs P13 control comparison.
2. **Mean weekly increment of extracellular 8-oxo-dG (ng / 10^6 cells / week)** by linear regression over 8 weeks (n=3 replicates per week):
   - P8 control 16 ± 4; P8 LDR 27 ± 7 (LDR vs control p = 0.003)
   - P13 control 26 ± 5; P13 LDR 45 ± 10
   - LDR P13 vs LDR P8: p = 0.035; control P13 vs control P8: p = 0.045
3. **γH2AX foci / cell** (acute 1 Gy, 0.75 Gy/min, kinetics at 0/45 min/24 h/48 h):
   - P8: 0.20 ± 0.05 → ~17 ± 2 → ~0.3 ± 0.1 (back to baseline by 24 h)
   - P23: 3.5 ± 1.3 → ~22 ± 2 → ~10 ± 1 (24 and 48 h; persistent damage)
   - P19-C/ST/IR: baseline ~3.5 ± 0.5, residual ~4.5 ± 0.7 at 24/48 h.
4. **Table 1 — TIFs (telomere dysfunction-induced foci) per cell**, baseline and 48 h after 1 Gy:
   - P8 baseline 1.91 ± 0.45; P8 1 Gy 48 h 3.88 ± 0.42
   - P19-C C 7.95 ± 1.13; P19-C 1 Gy 48 h 10.71 ± 1.58
   - P19-IR C 12.32 ± 1.52; P19-IR 1 Gy 48 h 14.75 ± 1.91
   - P19-ST C 11.55 ± 1.29; P19-ST 1 Gy 48 h 16.33 ± 2.26
   - P23   C 18.27 ± 2.72; P23   1 Gy 48 h 28.55 ± 2.55
5. **Supplementary Table S1 (PD ANOVA):** Week F=1239 df=7; Age F=1674 df=1; Treatment F=2999 df=1; all main and 2-way interactions p<0.0001; 3-way Week×Age×Treatment F=3.363 df=7 p=0.0041; MSE=0.09294 df=80.
6. **Supplementary Table S2 (8-oxo-dG ANOVA):** Week F=72.16 df=7 p<0.0001; Age F=61.42 df=1 p<0.0001; Treatment F=54.02 df=1 p<0.0001; Week×Age F=3.386 p=0.0039; Week×Treatment F=6.673 p<0.0001; Age×Treatment F=4.994 p=0.0289; Week×Age×Treatment F=0.5547 p=0.7895; MSE=989.6 df=64.

## Missing / out-of-scope
- Per-replicate raw counts (γH2AX foci, ELISA OD, telomere T/S ratios, SA-β-gal positives, P21 western band intensities).
- Microscopy image stacks for foci quantification (would enable end-to-end pipeline re-run, e.g., via the LUCID `lucid-autofoci-detection` companion).
- Three-way ANOVA raw long-format tables for direct SS recomputation.
- No software pipeline, no analysis code, no preprocessing scripts — the paper is entirely wet-lab.

## Worktype retag recommendation
**Master TSV (row 110 / rank 87) labels this `simulation/model replication`. That is INCORRECT.**
This is a **wet-lab radiobiology / DNA damage and repair kinetics assay study** — primary measurements are γH2AX immunofluorescence foci counts, FISH telomere co-localization, 8-oxo-dG competitive ELISA, SA-β-gal staining, qPCR T/S ratios, and western blot densitometry. No model, no Monte Carlo, no ODE/PDE, no Geant4/TOPAS/MCDS, no code released.
**Recommend retag → `wet-lab assay / radiobiology` (DNA repair kinetics + oxidative stress + senescence phenotype) with QA decision `KEEP_REDUCED: numerical-claim verification only` (statistical smoke replication is feasible from published means±SE; full pipeline re-run is not feasible without author data).**
