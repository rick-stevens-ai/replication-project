# Artifact Harvest — OSTI 2976249

## Primary artifact (paper)
| Artifact | Source | Size | Notes |
|---|---|---|---|
| paper.pdf | https://www.osti.gov/servlets/purl/2976249 (via uicgpu, CherryRd times out on osti.gov) | 38,455,968 B (36.7 MB) | PDF v1.5, 55 pp. incl. Appendix Table A1 |
| paper.txt | `pdftotext -layout paper.pdf paper.txt` on uicgpu | 244,795 B, 4,071 lines | Full text extraction, used for claim scan |

## Availability spot-checks (referenced frameworks / repos)
| Resource | URL | HTTP status | Notes |
|---|---|---|---|
| DeepXDE (paper's flagship PIML library, ref [174]) | https://github.com/lululxvi/deepxde | 200 | pip-installable; installed `deepxde==1.10.1` on uicgpu |
| NVIDIA PhysicsNeMo (fka Modulus, ref [409]) | https://github.com/NVIDIA/physicsnemo | 200 | Active repo (Modulus rebranded) |
| NeuralPDE.jl (ref [408]) | https://github.com/SciML/NeuralPDE.jl | 200 | Active |
| Shukla et al. cPIKAN (ref [17], CMAME 431:117290) | https://arxiv.org/abs/2406.02917 | 200 | Preprint of the cPIKAN paper |
| Public cPIKAN implementations | GitHub code-search `cPIKAN` | 2 hits | e.g. sfaroughi3/Pub_Scaled_cPIKAN |
| Public PIKAN implementations | GitHub code-search `PIKAN physics informed` | 12 hits | xgxgnpu/J-PIKAN (10★), USTC-AI4EEE/DS-PIKAN, yanpeng-gong/PIKAN-MultiMaterial, etc. |

## Reference data pulled for the sanity experiment
| Artifact | Source | Size | Notes |
|---|---|---|---|
| Burgers_ref.npz | https://raw.githubusercontent.com/lululxvi/deepxde/master/examples/dataset/Burgers.npz | 208,318 B | Raissi's spectral reference solution used across the PINN literature; shape usol=(256,100) over x=(256,), t=(100,) |

## Compute environment
| Host | Purpose | Details |
|---|---|---|
| CherryRd (m1 laptop) | Coordination, report writing | osti.gov fetch times out here → all fetches routed via uicgpu |
| uicgpu (8×A100, 2 TB RAM) | PDF fetch, pdftotext, PINN training | Python 3.8, `torch 1.11.0 + CUDA`, `deepxde 1.10.1`, PyTorch backend |

## LLM judge
| Endpoint | Model | Cost |
|---|---|---|
| Argo proxy localhost:44497 | `argo:gpt-5.2` | FREE (per standing rule) |

---

## Wave-3 deepening artifacts (2026-07-04)

### Code written for the matched-budget MLP-PINN vs cPIKAN head-to-head
| File | Purpose | Size |
|---|---|---|
| `work/pinn_vs_pikan_burgers.py` | v2 attempt (kept for provenance; superseded by v3) | ~11 kB |
| `work/pinn_vs_pikan_burgers_v3.py` | v3 fair head-to-head: MLP [2,20,20,20,20,1] + cPIKAN [2,10,10,1] deg=6, matched budget (Adam 20k + 3×L-BFGS 500), IC/BC weighted, gradient-clipped | ~12 kB |
| `work/judge_v2.py` | Argo `argo:gpt-5.2` strict-judge script with anti-inflation prompt + full v1+v3 raw numbers | ~6 kB |

### Deepened evidence (real numbers from real training)
| Artifact | Content | Size |
|---|---|---|
| `report/evidence/pinn_vs_pikan_result_v3.json` | Raw per-model per-slice numerical results (final loss, params, wall time, global L2, snapshot L2 at t=0.25/0.50/0.75/0.99) | 1.8 kB |
| `report/evidence/mlp_vs_cpikan_train_v3.log` | Complete training log with per-iter loss decomposition for both models (Adam + all L-BFGS bursts) | 6.9 kB |
| `report/evidence/mlp_vs_cpikan_slices_v3.png` | 3-panel overlay of spectral reference vs MLP-PINN vs cPIKAN at t=0.25/0.50/0.75 | 96 kB |
| `report/evidence/mlp_vs_cpikan_error_heat_v3.png` | 2-panel \|error\|(t,x) heatmap for both models on the same colour scale | 48 kB |
| `report/evidence/judge_v2.json` | Argo `argo:gpt-5.2` verdict: PARTIAL, confidence 0.78, coverage 60 %, agreement 67 % | 1.7 kB |
| `work/out/mlp_pred_v3.npz` / `work/out/kan_pred_v3.npz` | Full 256 × 100 grid predictions from each model + reference | 311 kB each |

### Compute
| Host | Purpose | Wall time |
|---|---|---|
| uicgpu (A100 GPU 1, torch 1.11.0 + CUDA) | MLP-PINN training | 318.2 s |
| uicgpu (A100 GPU 1, torch 1.11.0 + CUDA) | cPIKAN training | 392.6 s |
| CherryRd | Argo judge call, report writing | seconds |
