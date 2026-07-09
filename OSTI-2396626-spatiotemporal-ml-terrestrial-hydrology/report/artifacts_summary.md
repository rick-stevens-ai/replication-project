# Artifacts Summary — OSTI-2396626 Replication

**Paper**: Bennett et al. (2024), *Spatio-Temporal Machine Learning for Regional to Continental Scale Terrestrial Hydrology.* JAMES 16(6), e2023MS004095.
**Host**: `uicgpu` (heavy artefacts); CherryRd Dropbox (report + evidence bundle).
**Verdict**: PARTIAL.

## Directory layout

### On CherryRd
```
~/Dropbox/REPLICATE-PROJECT/OSTI-2396626-spatiotemporal-ml-terrestrial-hydrology/
├── report/
│   ├── REPORT.md               # Primary hand-written report
│   ├── REPORT.tex              # LaTeX version + Genuine Critique section
│   ├── open_questions.json     # 5 open research questions
│   ├── workflow.md             # Stage-by-stage replication workflow
│   ├── artifacts_summary.md    # This file
│   ├── failure_analysis.md     # What didn't work + why
│   └── evidence/
│       ├── smoke_96_30d.json     # 96×96, 30-day timing
│       ├── smoke_96_365d.json    # 96×96, 365-day timing
│       ├── smoke_256_365d.json   # 256×256, 365-day timing (CONUS-relevant)
│       ├── smoke_512_365d.json   # 512×512, 365-day timing (CONUS-relevant)
│       └── smoke_640_365d.json   # 640×384, 365-day timing (CONUS-relevant)
```

### On uicgpu
```
~/replicate/osti-2396626/
├── venv/                       # Python 3.8.10, torch 2.4.1+cu121, pytorch_lightning 2.4.0
├── paper.pdf                   # OSTI purl 2396626, 10,093,235 B, PDF v1.7
├── paper.txt                   # pdftotext -layout output, 744 lines, 84 KB
├── code.zip                    # Zenodo v0.0.3 archive, 29 KB
├── code/                       # Unpacked HydroFrame-ML-hydrogen-emulator-configurable-5cb5b95
│   └── emulator_configurable/
│       ├── models.py           # ForcedSTRNN (class at line 87)
│       ├── model_builder.py
│       ├── forecast.py         # (contains the state-leak bug — see failure_analysis.md)
│       ├── datapipes.py        # (training-only, torchdata-dep)
│       └── ...                 # 8 modules, ~2,238 LOC total
├── repo/                       # git clone of HydroFrame-ML/hydrogen-emulator-configurable (HEAD)
│   ├── notebooks/              # (HEAD-only)
│   ├── CONUS2_Data_Prep/       # precomputed pressure/ET/root-zone/static scalers (CSV+YAML)
│   └── fstr_train_scripts/     # small_fstr_phase_{1..4}_train.sh
└── work/
    └── smoke_forward.py        # Instantiation + chunked 365-day forward timing
```

## Paper artefact
- **Source**: `https://www.osti.gov/servlets/purl/2396626`
- **Size**: 10,093,235 B
- **Format**: PDF v1.7
- **Text extraction**: 744 lines / 84 KB via `pdftotext -layout`
- **Data Availability Statement**: line 630 (references `hf_hydrodata`)

## Code artefacts
- **Zenodo release**: DOI 10.5281/zenodo.10730252, version v0.0.3, archive `HydroFrame-ML/hydrogen-emulator-configurable-0.0.3.zip` (29 KB).
- **GitHub HEAD**: `https://github.com/HydroFrame-ML/hydrogen-emulator-configurable.git`
  - Adds `notebooks/`, `CONUS2_Data_Prep/` (precomputed scalers), phased training scripts.
- **Model architecture**: `emulator_configurable/models.py:87` (`class ForcedSTRNN(pl.LightningModule)`).
- **Direct-instantiation route**: bypass package `__init__.py` (which pulls `forecast → datapipes → torchdata`) and load `models.py` + `model_builder.py` directly.

## Data artefacts (not fetched)
- **Source**: ParFlow-CLM CONUS1 baseline zarr archive under `/hydrodata/PFCLM/CONUS1_baseline/simulations/daily/zarr/…`.
- **Access wrapper**: `hf_hydrodata` 1.4.7 (Defnet et al. 2024, JOSS under review).
- **Gate**: per-user Princeton HydroFrame email + API pin (`https://hydrogen.princeton.edu/signup`).
- **Status**: `hf.get_datasets()` returns `ValueError: No email/pin was registered.` — not fetched by design.

## Measured artefacts

### Parameter count (C9)
- `n_params_total = 2,710,656` (all trainable)
- Config: `num_layers=2, num_hidden=[64,64], img_channel=5, out_channel=5, act_channel=5, init_cond_channel=5, static_channel=15`
- Matches `train_scripts/fstr_train.sh` variant `new_params_2l_64hd`.

### Forward-pass timing (C4) — 1× A100 80 GB PCIe, fp32, no torch.compile

| Patch $H\times W$ | $T$ (days) | Peak GPU MB | Wall (s) | CONUS-yr extrapolated (min) |
|---|---:|---:|---:|---:|
| 96 × 96 | 30 | 151.5 | 0.274 | 3.20 |
| 96 × 96 | 365 | 278.9 | 1.980 | 23.10 |
| 256 × 256 | 365 | 1,855.9 | 6.408 | **11.96** |
| 640 × 384 | 365 | 6,914.9 | 24.282 | **12.14** |
| 512 × 512 | 365 | 7,376.9 | 27.142 | **12.67** |

CONUS-relevant configurations (patches ≥ 256×256, T = 365) converge on **~12 min per full CONUS water year**.

## Verdict-linked evidence map
| Claim | Verdict | Evidence artefact(s) |
|---|---|---|
| C1 FSTR architecture | REPRODUCED | `code/emulator_configurable/models.py` line 87 (read + confirmed) |
| C2 Public code | REPRODUCED | `code.zip` (Zenodo) + `repo/` (GitHub HEAD) |
| C3 Public data | PARTIAL | `hf.get_datasets()` traceback (blocked); package install log |
| C4 <1 hr per water year | REPRODUCED (~5× margin) | `report/evidence/smoke_{256,512,640}_365d.json` |
| C5 >1,000× speedup | REPRODUCED (plausibility) | Measured emulator + Maxwell 2015 / O'Neill 2021 lit refs |
| C6 RMSE <1 m majority | NOT TESTED | Blocked by C3 |
| C7 FSTR > UNet/ResNet | NOT TESTED | Blocked by C3 |
| C8 ~24 hr training | NOT TESTED | Blocked by C3 |
| C9 Parameter count | NEW DATUM (2,710,656) | Direct measurement in `smoke_forward.py` |

## Preservation note
- **CherryRd Dropbox**: all report + evidence artefacts (this file, JSON evidence, LaTeX/MD reports).
- **uicgpu**: heavier artefacts (venv, code, paper, work scripts) — not synced back due to size; instructions in `workflow.md` fully reproducible.
