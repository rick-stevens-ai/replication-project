# LUCID Replication — PyFoci foci-miscounting paper

Paper: *A computational approach to quantifying miscounting of radiation-induced double-strand break immunofluorescent foci*, DOI `10.1038/s42003-022-03585-5`.

## Scope

This is a **dataset/artifact-level partial replication**. The public PyFoci code, Colab, and datasets were cached successfully, but the full image-processing pipeline was not rerun because the local default Python 3.14 environment is incompatible with numba. Instead, `code/analyze_cached_pyfoci.py` analyzes the cached public parquet/count datasets to reproduce the paper's central quantitative point: foci counting can substantially misestimate true DNA break counts and the error depends strongly on microscope/magnification/marker configuration.

## Files

- `REPORT.md` — audit report and verdict
- `PROGRESS.md` — chronology and blockers
- `code/pyfoci/` — cached public PyFoci repository
- `code/PyFoci_Colab/` — cached Colab artifacts
- `code/analyze_cached_pyfoci.py` — lightweight dataset-level replication driver
- `data/*.zip` and `data/extracted/*.parquet` — cached public datasets
- `results/summary.json` — aggregate numerical findings
- `results/cached_dataset_error_summary.csv` — per-dataset error metrics
- `figures/*.png` — reproduced diagnostic plots

## Rerun

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-pyfoci-miscounting
python3 code/analyze_cached_pyfoci.py
```

Expected runtime: <30 seconds on laptop CPU.

Python dependencies: `pandas`, `pyarrow`, `numpy`, `matplotlib`.

For a full pipeline rerun, create a Python 3.11 environment and install the PyFoci repo dependencies; Python 3.14 is too new for numba.
