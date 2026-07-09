# Artifact Harvest — OSTI 3003302

## Paper
| Item | URL | Bytes | Checksum |
|---|---|---|---|
| Paper PDF (Copernicus mirror) | https://gmd.copernicus.org/articles/18/5575/2025/gmd-18-5575-2025.pdf | 9,269,925 | md5 `b9dd778d801799c2dd7fa90b48f8c6a4` |
| Paper text (pdftotext -layout) | (local) `work/paper.txt` | 1,485 lines | — |
| OSTI PURL | https://www.osti.gov/servlets/purl/3003302 | 0 (failed) | — |
| DOI | https://doi.org/10.5194/gmd-18-5575-2025 | — | — |

## Code

| Item | URL | Notes |
|---|---|---|
| GitHub HENS branch | https://github.com/ankurmahesh/earth2mip-fork/tree/HENS | default branch = `HENS`; 11 stars; 19,401 KB; last push 2026-04-16 |
| `earth2mip/ensemble_utils.py` (bred-vector impl) | raw.githubusercontent.com/ankurmahesh/earth2mip-fork/HENS/earth2mip/ensemble_utils.py | 533 lines; contains `generate_bred_vector`, `generate_bred_vector_timeevolve`, `CorrelatedSphericalField` |
| `earth2mip/diagnostics.py` | same repo | 358 lines |
| `earth2mip/score_ensemble_outputs.py` | same repo | 189 lines |
| `modulus-makani-fork` (training) | https://github.com/ankurmahesh/modulus-makani-fork | referenced, not downloaded |
| NVIDIA modulus-makani upstream | https://github.com/NVIDIA/modulus-makani | referenced |
| NVIDIA Earth2Studio (current inference) | https://github.com/NVIDIA/earth2studio | referenced |

## Model checkpoints (open-source)

| Location | Contents |
|---|---|
| DataDryad DOI 10.5061/dryad.2rbnzs80n | 29 SFNO checkpoints + inference/scoring code |
| HuggingFace `maheshankur10/hens` (DOI 10.57967/hf/4200) | 29 SFNO checkpoints (each: `config.json`, `global_means.npy`, `global_stds.npy`, `land_mask.nc`, `metadata.json`, `orography.nc`, `training_checkpoints/best_ckpt_mp0.tar`); heat-index Zarr; percentile 95/99 climatology; total ~304 GB |
| NERSC portal | https://portal.nersc.gov/cfs/m4416/hens/earth2mip_prod_registry/ |
| Docker image | https://hub.docker.com/r/amahesh19/modulus-makani/tags — `amahesh19/modulus-makani:0.1.0-torch_patch-23.11-multicheckpoint` |

## Config independently verified

Retrieved: `earth2mip_prod_registry/sfno_linear_74chq_sc2_layers8_edim620_wstgl2-epoch70_seed16/config.json` (22.8 KB from HuggingFace).

Confirmed matches paper Table 1:

| Paper Table 1 | Retrieved config.json |
|---|---|
| Architecture: SFNO v0.1.0 | `wandb_group="sfno_linear_74chq_sc2_layers8_edim620_wstgl2-0.1.0"`, `nettype="SFNO"` |
| Horizontal resolution 0.25° | `img_shape_x=721`, `img_shape_y=1440` |
| Embedding dimension 620 | `embed_dim=620` |
| Scale factor 2 | `scale_factor=2` |
| 8 layers | `num_layers=8` |
| Training 70 epochs | `max_epochs=70` |
| 74 channels | `channel_names` has 74 entries: u10m,v10m,u100m,v100m,t2m,sp,msl,tcwv,2d + 5 pressure vars × 13 levels |
| Weighted-MSE loss | `loss="weighted squared temp-std geometric l2"` |
| Orography + landmask + zenith | `add_orography=true`, `add_landmask=true`, `add_zenith=true` |

## Files stored locally

```
work/
├── paper.pdf                        (paper, Copernicus mirror)
├── paper.txt                        (text extraction)
├── HENS_README.md                   (repo README)
├── methodology_replication.py       (independent bred-vec + diagnostics re-impl)
├── cm1_refined.py                   (Toth-Kalnay growth-rate test)
├── llm_judge.py                     (Argo verdict)
└── code_snapshot/
    ├── ensemble_utils.py            (from repo, for audit)
    ├── diagnostics.py               (from repo)
    ├── score_ensemble_outputs.py    (from repo)
    ├── hf_seed16_config.json        (from HuggingFace, model spec)
    └── hf_seed16_metadata.json      (from HuggingFace)

report/evidence/
├── cm1_bred_vector_alignment.json
├── cm1_refined.json
├── cm2_spread_error.json
├── cm23_verdict.json
├── cm4_spectra.json
├── cm4_verdict.json
└── llm_judge.json
```
