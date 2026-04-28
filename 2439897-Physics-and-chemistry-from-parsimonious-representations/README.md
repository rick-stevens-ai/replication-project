# Physics and chemistry from parsimonious representations: image analysis via invariant variational autoencoders

- **OSTI ID:** 2439897
- **Rank:** #17
- **Replication Score (a priori):** 9/10
- **Achieved Replication Score:** **8/10**
- **Open-Source Tools:** Yes
- **Code Repository:** Yes (independent reimplementation — see `replication/code/`)
- **Tools:** Python, PyTorch 2.8, numpy, matplotlib

## Why This Paper
Open-source Python code (PyTorch), synthetic/public datasets, detailed
methodology, and quantitative results. End-to-end AI replication is
straightforward.

## Replication Summary (2026-04-23)

We independently re-implemented (no `atomai` dependency) a
rotationally-invariant VAE (rVAE) with:

- Conv encoder → (μ, logσ², θ, tₓ, tᵧ)
- Coordinate-MLP decoder with random Fourier positional features, applied
  on the **canonical grid** after the inverse SE(2) transform
- β-annealing over 10 epochs to prevent posterior collapse
- Gradient clipping + logvar clamping for stability

### Dataset
Synthetic hexagonal lattices (64×64, Gaussian atoms, σ=1.1 px).
Ground-truth factors:
- `a ~ U(6, 12)` px   — **physical** (lattice constant)
- `θ ~ U(−π, π)`       — nuisance (rotation)
- `(tₓ, tᵧ) ~ U(−3, 3)` px — nuisance (sub-pixel translation)

Train / val: 20 000 / 2 000 samples.

### Hardware
2× NVIDIA A100 40 GB (one per model) on `rbdgx1`. Total training time
≈ 9 min per model (80 epochs, ~6.5 s/epoch).

### Key Results (held-out Pearson |r|)

| Factor              | rVAE (zdim=2) | Vanilla VAE (zdim=5) |
|---------------------|:-------------:|:---------------------:|
| **Lattice `a`**     | **0.993**     | 0.862                 |
| Rotation `θ`        | 0.016         | 0.074                 |
| Trans `tₓ`          | 0.029         | 0.040                 |
| Trans `tᵧ`          | 0.004         | 0.038                 |
| Val recon MSE       | **79.1**      | 89.3                  |

- rVAE content latent z₁ essentially saturates correlation with the
  physical factor (|r|=0.993).
- rVAE content latent is invariant to pose (|r|≤0.03 for every nuisance).
- Reconstruction MSE ~12 % lower than parameter-matched vanilla VAE.
- z₀ collapsed (KL≈0) — correct, because only one physical factor
  exists in the dataset; this is the "parsimony" claim.

### Figures (in `replication/report/`)
- `fig_training.png` — per-epoch recon MSE + KL (log scale)
- `fig_latent_vs_a.png` — content latent vs ground-truth lattice
- `fig_nuisance.png` — pose-head predictions vs ground truth
- `fig_traversal.png` — decoded latent sweep
- `fig_reconstruction.png` — 8 inputs vs reconstructions

### Gaps (why 8 and not 10)
1. No experimental STEM/SPM data — we used controlled synthetic lattice.
2. The rVAE pose head did **not** recover pose at high correlation
   (|r|≈0.03) in this setting, because the hexagonal lattice itself has
   6-fold rotational and translation-periodic symmetry: the coordinate
   decoder learned an effectively pose-equivariant canonical template
   and achieved invariance by **symmetry exploitation** rather than pose
   estimation. This is explicitly discussed in the report.

## Layout

```
replication/
├── code/
│   ├── rvae.py                # independent PyTorch implementation
│   └── make_figures.py        # figure generator
├── results/                   # trained weights, JSON results, logs
│   ├── model_rvae.pt
│   ├── model_vae.pt
│   ├── results_rvae.json
│   ├── results_vae.json
│   ├── encoded_{rvae,vae}.npz
│   └── train_{rvae,vae}.log
└── report/
    ├── report.tex
    ├── report.pdf             ← ** main deliverable **
    └── fig_*.png
```

## Status
- [x] Paper reviewed
- [x] Code/tools identified
- [x] Code implemented (from-scratch PyTorch reimplementation)
- [x] Results reproduced (rVAE vs VAE ablation, quantitative disentanglement)
- [x] Results validated against paper's central claim
- [x] LaTeX report compiled → `replication/report/report.pdf`

## How to Rerun
```bash
# On any GPU host with PyTorch 2.x:
cd replication/code
python rvae.py --model rvae --epochs 80 --beta_warmup 10 --zdim 2 \
               --n_train 20000 --n_val 2000 --lr 1e-3 --outdir run
python rvae.py --model vae  --epochs 80 --beta_warmup 10 --zdim 5 \
               --n_train 20000 --n_val 2000 --lr 1e-3 --outdir run
python make_figures.py --outdir run
```
