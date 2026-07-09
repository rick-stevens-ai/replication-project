# Artifact Harvest — OSTI-2396626

All artifacts were pulled through `ssh uicgpu` (CherryRd cannot resolve `osti.gov`; uicgpu has the CELS/UIC HTTP proxy in `~/env.sh`). Filenames below are as they landed on uicgpu.

| # | Artifact | Source URL | Size | Notes |
|---|----------|-----------|------|-------|
| A1 | Paper PDF | https://www.osti.gov/servlets/purl/2396626 | 10,093,235 B | OSTI OA full text of Bennett et al. 2024, *JAMES* 16, e2023MS004095 |
| A2 | Paper plaintext | pdftotext -layout of A1 | 84,023 B | 744 lines, used for claims extraction |
| A3 | Zenodo record JSON | https://zenodo.org/api/records/10730252 | ~1 KB | DOI 10.5281/zenodo.10730252, cited as Bennett (2024) code release |
| A4 | Code v0.0.3 zip | https://zenodo.org/api/records/10730252/files/HydroFrame-ML/hydrogen-emulator-configurable-0.0.3.zip/content | 29,256 B | Snapshot cited in the paper's Data Availability Statement |
| A5 | Code repo HEAD | https://github.com/HydroFrame-ML/hydrogen-emulator-configurable (main) | ~1.9 MB | Extended: adds `notebooks/`, `CONUS2_Data_Prep/`, and phased train scripts for FSTR/ResNet/UNet |
| A6 | hf_hydrodata PyPI metadata | https://pypi.org/pypi/hf_hydrodata/json | ~1 KB | Data-access package cited as Defnet et al. (2024, JOSS under review) |

## Model source of truth (verified in v0.0.3 archive)

- `emulator_configurable/models.py` — 794 lines; contains `ForcedSTRNN` (line 87), `ActionSTLSTMCell` (line 30), and UNet/ResNet baseline classes
- `train_scripts/fstr_train.sh` — canonical hyperparameters for the paper's `new_params_2l_64hd` variant: `num_layers=2, num_hidden=[64,64], img_channel=5, out_channel=5, act_channel=5, init_cond_channel=5, static_channel=15, sequence_length=14, patch_size=48, batch_size=16, max_epochs=1`

## Data availability

- Training data (ParFlow-CLM CONUS1 baseline zarr at `/hydrodata/PFCLM/CONUS1_baseline/simulations/daily/zarr/conus1_{2003,2004,2005,2006}_preprocessed.zarr`) is exposed via the `hf_hydrodata` Python package (Defnet et al. 2024).
- `hf_hydrodata` requires per-user account registration + API pin at https://hydrogen.princeton.edu/signup + `hf_hydrodata.register_api_pin()`. This is a per-researcher credential that a batch-replication subagent cannot honestly self-provision without leaving Rick a trail of an anonymous Princeton sign-up. **The data is public in principle but gated by account creation in practice.**
- HEAD's `CONUS2_Data_Prep/` contains genuinely public artifacts: precomputed pressure/ET/root-zone/static scalers as CSV+YAML, plus land-cover parameter tables — enough to instantiate the data-preprocessing pipeline for CONUS2 without pulling the raw zarr.

## Related HydroFrame-ML repos (context, not used for this replication)

`high-res-WTD-static` (⭐9), `inversion_model` (⭐4), `ML_GW_Digital_Twin`, `sandtank-ml`, `hydrogen-hydroml` (the `hydroml` package that provides `hydroml.loss` used by `models.py`).
