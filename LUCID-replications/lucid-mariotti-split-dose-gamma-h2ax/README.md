# LUCID replication — Mariotti et al. 2013 split-dose γ-H2AX

**Target paper.** Mariotti L.G., Pirovano G., Savage K.I., Ghita M., Ottolenghi A.,
Prise K.M., Schettino G. (2013). *Use of the γ-H2AX Assay to Investigate DNA
Repair Dynamics Following Multiple Radiation Exposures.* **PLOS ONE 8(11): e79541.**
DOI: [10.1371/journal.pone.0079541](https://doi.org/10.1371/journal.pone.0079541).

**What this replication covers.** A faithful re-implementation of the paper's
analytical γ-H2AX foci induction/decay model (eqs. 1–4) and a quantitative
comparison against the **published Table S1 fitted parameters** and against
**hand-digitized data** from Figs 1A and 5.

## Layout

| Path | Contents |
| --- | --- |
| `data/paper.pdf` | Local copy of the PLOS ONE article |
| `data/TableS1.docx` | PLOS supplementary Table S1 (downloaded fresh from PLOS) |
| `data/FigS1_*.tif`, `FigS2_*.tif`, `FigS3_*.tif` | PLOS supplementary figures (mock + 53BP1 co-localization images) |
| `data/digitized_fig1A.csv` | Hand-digitized 1 Gy / 2 Gy single-dose data points |
| `data/digitized_fig5.csv` | Hand-digitized split-dose data points (5 gap conditions) |
| `code/model.py` | The four equations + Table-S1 parameter dictionaries |
| `code/validate.py` | Forward-simulate with published params; compare to digitized data |
| `code/refit.py` | Independently re-fit the model to digitized data; compare to published |
| `results/single_dose_validation.csv` | Per-curve RMSE, model peak height & time |
| `results/split_dose_validation.csv` | Per-gap RMSE, peak metrics |
| `results/refit_single.csv`, `refit_split.csv` | Independent refit parameters vs published |
| `results/summary.json` | Machine-readable run summary |
| `figures/fig1A_replication.png` | Model vs digitized data, 1 Gy & 2 Gy 225 kVp |
| `figures/fig5_replication.png` | Model vs digitized data, 5 split-dose gaps |
| `figures/refit_overlay.png` | Refit vs published params overlay |
| `REPORT.md` | Verdict + agreement scores + notes |
| `PROGRESS.md` | Run log |

## Reproducing

```bash
cd code
python3 model.py        # sanity-check eq.(3) returns published peak heights
python3 validate.py     # generates fig1A_replication.png, fig5_replication.png
python3 refit.py        # generates refit_overlay.png, refit_*.csv
```

Dependencies: `numpy`, `pandas`, `matplotlib`, `scipy` (all standard).

## What was *not* attempted

- **Re-running the wet-lab experiment** (AG01522 fibroblasts + 225 kVp X-ray
  cabinet at CCRCB, Queen's University Belfast). The paper provides no raw
  foci-count tables; raw images are not in a public repository.
- **Cell-survival / clonogenic** modelling (Fig 6). The paper presents this as
  observational, no model fit reported.
- **Eu/hetero-chromatin** quantification (Fig 7). No quantitative model.
- **53BP1 co-localization** (Figs S2–S3). Qualitative only.
