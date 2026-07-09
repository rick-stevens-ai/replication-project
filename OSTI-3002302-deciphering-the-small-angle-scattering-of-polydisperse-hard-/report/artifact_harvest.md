# Artifact harvest — OSTI 3002302

All artifacts pulled during this replication.

## Paper

| Item | URL / Path | Size | Checksum |
|---|---|---|---|
| PDF (via OSTI purl) | https://www.osti.gov/servlets/purl/3002302 → `work/paper.pdf` | 7,118,161 B (6.8 MB) | MD5 `2b7c8c230cb802ab89cb25f2ec8eb14b` |
| pdftotext dump | `work/paper.txt` | 879 lines | — |
| DOI (paywalled OA-NC copy at AIP) | https://doi.org/10.1063/5.0290589 | — | — |

## Code + data + weights (GitHub, CC BY-NC 4.0)

Repo: https://github.com/ljding94/Polydisperse_Sphere (~35 MB clone).

Cloned to `work/Polydisperse_Sphere/`. Includes:

### Data
| File | Shape | Description |
|---|---|---|
| `data_used/L_18_pdType_1_train_data.npz` | log10Iq (4000,100), params (4000,4) [L,pdType,η,σ] | uniform-dist. train set |
| `data_used/L_18_pdType_1_test_data.npz` | log10Iq (1000,100), params (1000,4) | uniform-dist. test set |
| `data_used/L_18_pdType_2_train_data.npz` | same shapes | normal-dist. train |
| `data_used/L_18_pdType_2_test_data.npz` | same shapes | normal-dist. test |
| `data_used/L_18_pdType_3_train_data.npz` | same shapes | lognormal-dist. train |
| `data_used/L_18_pdType_3_test_data.npz` | same shapes | lognormal-dist. test |
| `data_used/L_18_pdType_{1,2,3}_train_stats.npz` | mean/std for I(Q) and params | normalization stats |
| `data_used/prec_data/20250613.zip`, `20250701.zip` | precomputed intermediates | not used |

### Trained weights (used here)
| File | Model | Purpose |
|---|---|---|
| `data_used/L_18_pdType_1_vae_state_dict.pt` | VAE (encoder+decoder) | pdType=1 |
| `data_used/L_18_pdType_1_gen_state_dict.pt` | Generator (P2L+decoder) | pdType=1 |
| `data_used/L_18_pdType_1_inf_state_dict.pt` | Inferrer (encoder+L2P) | pdType=1 |
| `data_used/L_18_pdType_2_{vae,gen,inf}_state_dict.pt` | same | pdType=2 |
| `data_used/L_18_pdType_3_{vae,gen,inf}_state_dict.pt` | same | pdType=3 |

### Code (used as reference — network arch reimplemented independently, PY reimplemented independently)
| File | Role |
|---|---|
| `analyze/VAE_model.py` | Encoder / Decoder / Converter / VAE / Generator / Inferrer definitions + training loops |
| `analyze/analyze_PY.py` | Reference PY implementation (not copied) |
| `analyze/main_VAE.py`, `analyze/main_ML_analyze.py` | Training entry points |
| `analyze/analyze.py`, `analyze/ML_analyze.py` | Data loading helpers |
| `code/calc_Iq.cpp`, `code/calc_Iq.py` | MD-config → I(Q) calculator |
| `code/*.lammps` | LAMMPS input scripts for MD ground-truth generation |
| `code/run_lmp.sh`, `code/local_run.sh` | Wrappers |
| `code/makefile` | Build calc_Iq |
| `plot/*.py` | Visualization scripts (not run here) |

## Compute host

| Host | Role |
|---|---|
| CherryRd (Mac Studio) | Orchestration, paper fetch (failed), text extraction, LLM-judge call, report authoring |
| uicgpu (8×A100 UIC cluster) | PDF fetch (proxy), all PyTorch inference + retraining |

## LLM endpoints used (all FREE)

| Endpoint | Model | Purpose |
|---|---|---|
| http://127.0.0.1:44497/v1 (Argo proxy, tunnel from studio-ts) | argo:gpt-5.2 | Final LLM-judge verdict |
