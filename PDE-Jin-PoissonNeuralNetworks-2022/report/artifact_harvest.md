# Artifact Harvest

## Paper
| item | URL / path | size |
|---|---|---|
| arXiv PDF (v1) | https://arxiv.org/pdf/2012.03133 → `work/PNN_arxiv.pdf` | 1.44 MB |
| arXiv abs | https://arxiv.org/abs/2012.03133 | — |
| Journal DOI | https://doi.org/10.1109/TNNLS.2022.3148734 | (paywalled, arXiv used instead) |

## Code
| item | source | size |
|---|---|---|
| Reference PNN implementation | `git clone https://github.com/jpzxshi/pnn` → `work/pnn` (+ bundled `pnn/learner/`) | 5 files + learner tree |
| Standalone `learner` fork | `git clone https://github.com/jpzxshi/learner` → `work/learner_repo` (unused, kept for reference) | — |

## Data
No external download needed. The Lotka–Volterra dataset is generated on the fly by `data.LVData` using a 4th-order symplectic-Stormer-Verlet integrator (`learner.integrator.hamiltonian.SV`) in the (p,q) = (log u, log v) coordinates that make LV canonically Hamiltonian; ground-truth long-time test trajectory is the SV integrator's output at 1000 steps of h=0.1.

## Compute
- Host: **uicgpu** (Tailscale-mesh), CPU 255 cores / 2 TB RAM, NVIDIA A100 80 GB PCIe × 8. Used GPU 0.
- Environment: `/gpustor/stevens/anaconda3/bin/python3.11`, torch 2.8.0+cu128, learner (bundled with `jpzxshi/pnn`).

## Outputs written by this rerun
| path | what |
|---|---|
| `report/evidence/lv_result.json` | headline JSON — per-model rollout MSE at steps 100/500/1000, H drift stats, wall-times |
| `report/evidence/lv_trajectories.npz` | full trajectories: `gt`, `pnn`, `mlp`, `H_gt`, `H_pnn`, `H_mlp` (shape `(3, 1000, 2)`) |
| `report/evidence/lv_train.log` | full training log (loss curves at every 2000 iters for both models) |
| `report/evidence/lv_phase_portrait.png` | (u,v) phase plot: GT vs PNN vs MLP |
| `report/evidence/lv_rollout_mse.png` | per-step rollout MSE, log-y |
| `report/evidence/lv_H_drift.png` | per-step |H − H₀| for reference vs PNN vs MLP, log-y |
| `report/evidence/judge_argo.json` | LLM-judge (Argo Opus 4.7) verdict JSON |
| `work/lv_replicate.py` | the driver script (also copied to `uicgpu:/data/stevens/replicate/PNN-2022/work/`) |
