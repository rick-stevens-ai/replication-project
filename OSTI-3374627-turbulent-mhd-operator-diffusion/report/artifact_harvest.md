# Artifact harvest — OSTI 3374627

## Paper
| Artifact | URL | Size | Notes |
|---|---|---|---|
| Full-text PDF | https://www.osti.gov/servlets/purl/3374627 | 2.49 MB | PDF v1.7. Downloaded via uicgpu (local CherryRd could not reach osti.gov at time of fetch). Saved to `work/paper.pdf`. |
| Published article | https://doi.org/10.1088/2632-2153/ae054c | web | Mach. Learn.: Sci. Technol. 6 (2025) 035057. Open access, CC-BY-4.0. |
| arXiv preprint | https://arxiv.org/abs/2507.02106 | web | Cited on the GitHub badge; not separately fetched. |

## Author's code
| Artifact | URL | Notes |
|---|---|---|
| DINOs GitHub repo | https://github.com/semihkacmaz/DINOs | MIT-licensed. Cloned to uicgpu `~/replicate-work/osti-3374627/DINOs`. Contains: `data_generation/` (Dedalus wrapper, GRF init), `src/neurops/`, `src/diffusion/` (score-based DDPM with UNet + FlashAttention), `configs/` per-Re yaml files, `run_training.py`. |
| DINOs Garden entry | https://thegardens.ai/#/garden/10.26311%2Fc4bj-8h61 | Trained model weights. NOT downloaded (would require running against paper's exact preprocessing pipeline; scope of this replication is method-core, not weight loading). |

## Author's data
| Artifact | Status |
|---|---|
| MHD simulation dataset (800/100/100 sims per Re × 7 Re values, N=128, T=26) | **NOT PUBLICLY RELEASED**. Paper's Data Availability Statement: "The data cannot be made publicly available upon publication because the cost of preparing, depositing and hosting the data would be prohibitive within the terms of this research project. The data that support the findings of this study are available upon reasonable request from the authors." |

## Replication-generated artifacts (all in this dir)
| Artifact | Path | Size | Notes |
|---|---|---|---|
| From-scratch MHD solver | `work/mhd_solver.py` | 7 KB | numpy FFT + RK4, 2/3-dealiased, vorticity + magnetic-vector-potential formulation, Prm=1 |
| Parallel dataset builder | `work/build_dataset_parallel.py` | 2 KB | `multiprocessing.Pool` over sims |
| FNO training + rollout eval | `work/fno_train.py` | 9 KB | 2-D FNO, 8 modes, 32 channels, 4 spectral layers, ~1.06M params; trained per-Re |
| Spectral-bias analyzer | `work/spectral_analysis.py` | 3 KB | Shell-averaged E(k) of gt vs FNO prediction |
| Plots | `work/make_plots.py` | 3 KB | Matplotlib |
| Simulation datasets | (on uicgpu) `~/replicate-work/osti-3374627/data/mhd_Re{100,500,1000,3000}.npz` | 152 MB each | 128 sims × 26 T × 64² grid × 3 channels (ux, uy, A); float32. Not copied back to Dropbox (600 MB total). |
| Per-Re training results | `report/evidence/fno_Re{100,500,1000,3000}.json` | 3.7 KB each | Final rel-L2, training history, per-channel breakdown |
| Spectral-bias results | `report/evidence/spectra_Re1000.json` | 4.5 KB | shell-averaged E(k) arrays |
| Error-vs-Re plot | `report/evidence/error_vs_re.png` | 60 KB | Reproduces the qualitative shape of paper Table 1 for PINO-only |
| Spectral-bias plot | `report/evidence/spectra_Re1000.png` | 102 KB | Reproduces the qualitative shape of paper Fig. 3 for the PINO-only curve |

## Software versions used
- Python 3.12.13 (CherryRd) / 3.10.12 (uicgpu system python)
- numpy 1.23.5 (uicgpu) / 1.26.4 (local)
- torch 1.11.0 with CUDA on uicgpu / 2.2.2 CPU on local
- scipy 1.18.0
- matplotlib (default from pip)
- No Dedalus (paper's solver) — replaced with the from-scratch spectral solver in `mhd_solver.py`.

## Judge
- `work/judge.py` calls Argo proxy `http://127.0.0.1:44497/v1/chat/completions` with model `argo:claude-opus-4.7`, key `stevens` (free endpoint per wave brief).
