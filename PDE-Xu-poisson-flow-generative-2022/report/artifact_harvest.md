# Artifact Harvest

All artifacts are public and free.

| Artifact | URL | Size | Notes |
|---|---|---|---|
| Paper PDF | https://arxiv.org/pdf/2209.11178 | 13.4 MB | v4 (20 Oct 2022) |
| Official code repo | https://github.com/Newbeeer/poisson_flow | ~500 KB (excl. .git) | MIT license; PyTorch |
| Pretrained CIFAR-10 DDPM++ checkpoint | https://drive.google.com/drive/folders/1UBRMPrABFoho4_laa4VZW733RJ0H_TI0 (`checkpoint_500000.pth`) | 990 MB | step=500001, ema_decay=0.9999; downloaded via `gdown` |
| CIFAR-10 dataset | https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz | ~163 MB | Used pre-existing local copy at `/gpustor/stevens/hcdgx2-archive/DeepSpeed/DeepSpeedExamples/cifar/data/cifar-10-batches-py/`. Test set (10K) + train set (50K). |
| pytorch-fid Inception weights | https://github.com/mseitzer/pytorch-fid/releases/download/fid_weights/pt_inception-2015-12-05-6726825d.pth | 91 MB | Auto-downloaded by pytorch-fid |
| torchvision Inception-v3 | https://download.pytorch.org/models/inception_v3_google-0cc3c7bd.pth | 104 MB | Auto-downloaded for our IS script |
| Follow-up paper (PFGM++) | https://arxiv.org/abs/2302.04265 | — | Not used in this replication (author-recommended for new work). |

## Software stack

Ran on **uicgpu** (8× A100 80GB PCIe). Installed to `~/pfgm_replication/venv_pfgm` on that node.

- Python 3.8
- torch 1.13.1+cu116
- torchvision 0.14.1+cu116
- tensorflow 2.9.0 (needed for the paper's original loss/utils imports; only used at model-instantiation time via `ml_collections`)
- tensorflow_probability 0.17.0
- tensorflow_gan (indirect dependency of the paper's `run_lib.py`)
- ml_collections 0.1.0
- ninja 1.11.x (for the C++ extension compilation attempt — **not used**, we patched away the CUDA op via a native-PyTorch fallback)
- pytorch-fid 0.3.0
- scipy (RK45 ODE integrator)
- gdown 5.2.2 (Google Drive folder download)
- Pillow 9+, numpy 1.22+, matplotlib

## Local patches applied to the official repo

- `poisson_flow/op/fused_act.py` — replaced the CUDA-extension `torch.utils.cpp_extension.load()` call with a native PyTorch fused-LeakyReLU implementation (source in `work/op_fused_act_patch.py`). The CUDA extension refused to build against the local CUDA/torch combination.
- `poisson_flow/op/upfirdn2d.py` — replaced likewise with the reference native-PyTorch implementation (source in `work/op_upfirdn2d_patch.py`). Both patches are drop-in fallbacks used by rosinality/stylegan2-pytorch and produce numerically-equivalent results.

## Custom drivers (all in `work/`)

- `sample_pfgm_v2.py` — minimal sampler that loads the pretrained checkpoint and runs either forward-Euler-in-log-z or the paper's `scipy.integrate.solve_ivp` RK45 path in log-z. Reproduces `methods.Poisson.ode()` + `sampling.get_rk45_sampler_pfgm()` byte-for-byte.
- `gen_samples_bulk.py` — batches sampling, writes per-image PNGs into an output directory for use with pytorch-fid.
- `compute_is.py` — Inception-Score using torchvision's Inception-v3 with the standard 10-split protocol.
- `pfgm_2d.py` — auxiliary self-written 2D-toy PFGM attempt (see attempt log).

## Public artifacts of THIS replication run

Stored in `report/evidence/`:
- `pfgm_grid_5k_top64.png` — 8×8 grid of the first 64 PFGM samples from the 5K generation (RK45 path).
- `pfgm_cifar_rk45.png`, `pfgm_cifar_rk45.pt` — 64-image grid + raw tensor from the RK45 smoke run.
- `pfgm_cifar_euler200.png`, `pfgm_cifar_euler200.pt` — 64-image grid + raw tensor from a 200-step Euler run.
- `pfgm_euler40_sample0.png`, `pfgm_euler40_sample1.png` — individual 32×32 samples from the Euler-40 ablation.
- `gen_2k_rk45.log`, `gen_5k_rk45.log` — batch generation logs (per-batch NFE, throughput).
- `metrics.json` — machine-readable summary of all measurements.
