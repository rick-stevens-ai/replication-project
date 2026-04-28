# Deep Learning of Atomically Resolved Scanning Transmission Electron Microscopy Images: Chemical Identification and Tracking Local Transformations

- **OSTI ID:** 1427646
- **Rank:** #10
- **Replication Score:** 9/10 (plan) — achieved **7/10** with synthetic physics surrogate
- **Replication date:** 2026-04-24
- **Compute:** uicgpu, NVIDIA A100 80GB (GPU 4)
- **Wall time:** ~2 min end-to-end (data gen + 30 epochs + eval + figures)

## Why This Paper
Structured STEM image datasets + deep learning for quantitative atomic classification — a clear computational pipeline suitable for AI-driven replication.

## What the paper does
Trains a fully convolutional network on multislice-simulated HAADF-STEM images of SrTiO3 / La0.7Sr0.3MnO3 [001] heterostructures; applies it to experimental STEM frames to produce per-pixel chemical identity maps (Sr, Ti, La/Sr, Mn, vacuum) and track antisite / vacancy transformations.

## What we replicated
- **Model:** 7.76M-param U-Net (5 encoder stages, BN+ReLU, skip connections, softmax head) — PyTorch 2.5.1 / CUDA 12.1.
- **Training protocol:** AdamW, cosine LR, cross-entropy with class weighting, on-the-fly flip/rotate/brightness aug — 30 epochs, batch 16.
- **Data:** Physics-motivated synthetic surrogate (not full multislice) — perovskite [001] square lattice with A/B sublattice offsets, Z^1.7 HAADF-like intensity, random interface diffuseness, Poisson noise, scan-line jitter, A-site/B-site vacancies + antisite defects. 512 train / 64 val / 128 test frames (256×256).
- **Evaluation:** Pixel-level accuracy + per-class precision/recall/F1; peak detection vs. ground-truth column centres (RMSE + det. precision/recall).

## Results (held-out test, 128 frames, 8.4M pixels)
- Pixel accuracy: **0.988**
- Per-class F1: Sr 0.994, Ti 0.949, La/Sr 0.998, Mn 0.958
- Column-centre RMSE (at ~0.2 Å/px): Sr 0.11 px, Ti 0.47 px, La/Sr 0.06 px, Mn 0.45 px — sub-pixel for all classes
- Detection recall ≥ 0.98 for every atom class

Consistent with the paper's qualitative claim that an FCN trained purely on simulation produces quantitatively useful chemical mapping of perovskite interfaces.

## Status
- [x] Paper reviewed
- [x] Plan identified (plan PDF in this directory)
- [x] Code implemented (`replication/src/`)
- [x] Trained on A100 (uicgpu)
- [x] Results validated on synthetic test set
- [x] Report written (`replication/report/report.pdf`)
- [ ] *(future)* Swap synthetic surrogate for full Prismatic/abTEM multislice
- [ ] *(future)* Apply model to real experimental HAADF-STEM frames

## Repo layout
```
replication/
  src/
    synth_stem.py     # synthetic perovskite STEM + label generator
    unet.py           # small U-Net (5 levels, 7.76M params)
    train.py          # train/eval loop with per-class metrics
    make_figures.py   # figures + peak-finding / RMSE analysis
  figures/            # fig_data, fig_pred, fig_history, fig_confmat, fig_peaks, peak_stats.json
  logs/               # train.log, history.json, test_metrics.json
  report/
    report.tex / .pdf # full replication report
```

Mirror on uicgpu: `~/projects/replicate-1427646/`.

## How to reproduce
```bash
ssh uicgpu
cd ~/projects/replicate-1427646/src
CUDA_VISIBLE_DEVICES=4 ~/projects/replicate/.venv/bin/python train.py \
  --n-train 512 --n-val 64 --n-test 128 --epochs 30 \
  --batch-size 16 --base-ch 32 --out ../runs/unet
CUDA_VISIBLE_DEVICES=4 ~/projects/replicate/.venv/bin/python make_figures.py
```

## Key limitations (see report §5)
- Image formation is a physics-motivated Gaussian-column surrogate, not true multislice — this is the biggest gap vs. the paper.
- Defect pixels are not directly argmaxable under the current label encoding (antisite defects are still captured implicitly through cation-class confusion). Would want a multi-label / auxiliary defect head.
- Not validated on true experimental STEM frames.
