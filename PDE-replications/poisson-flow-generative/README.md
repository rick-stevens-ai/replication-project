# PFGM Replication — Poisson Flow Generative Models

Methodological replication of [Xu et al. 2022](https://arxiv.org/abs/2209.11178) (NeurIPS 2022, 115+ citations) on a 2D toy dataset.

## Paper

**Poisson Flow Generative Models**  
Yilun Xu*, Ziming Liu*, Max Tegmark, Tommi Jaakkola  
MIT — NeurIPS 2022

The paper introduces a generative model based on the analogy between data distributions and Poisson's equation in an augmented (N+1)-dimensional space. Data points act as electric charges, and integrating backward along the resulting Poisson field maps uniform noise on a hemisphere to the data distribution.

## What's Here

```
paper.pdf                    # Original paper (arXiv 2209.11178)
REPORT.md                    # Detailed replication report with results
replication/
├── code/
│   ├── pfgm.py              # PFGM: training + sampling (from scratch)
│   ├── diffusion_baseline.py # VE score-based diffusion baseline
│   └── eval.py              # Full evaluation pipeline
├── figures/
│   ├── sample_quality.png   # PFGM vs diffusion sample comparison
│   └── step_size_robustness.png  # NFE robustness curves
└── results/
    ├── metrics.json          # Quantitative metrics (SWD, coverage)
    ├── pfgm_model.pt         # Trained PFGM model
    ├── diffusion_model.pt    # Trained diffusion model
    └── *.npy                 # Generated and training samples
```

## Quick Start

```bash
cd replication/code

# Full evaluation (trains both models + generates figures)
python eval.py --epochs 400 --device cpu

# Train PFGM only
python pfgm.py --epochs 400

# Train diffusion baseline only
python diffusion_baseline.py --epochs 400

# Re-evaluate with existing models (skip training)
python eval.py --skip_train
```

**Requirements:** Python 3.9+, PyTorch, NumPy, SciPy, Matplotlib

**Runtime:** ~20 min on CPU

## Key Results

| Metric | PFGM | Diffusion (VE-SDE) |
|--------|------|--------------------|
| Sliced Wasserstein Distance ↓ | **0.049** | 0.059 |
| Mode Coverage (8 modes) | 100% | 100% |

PFGM achieves slightly better sample quality than the diffusion baseline, supporting the paper's claim of competitive generation.

Step-size robustness is partially confirmed: PFGM with log-z ODE (Eq. 6) degrades less than diffusion at 20–50 NFE, but the advantage is smaller in 2D than in high dimensions.

## Scope & Limitations

**Replicated:** Core PFGM algorithm (Algorithm 1, 2, Eq. 6), training on 2D MoG, backward ODE sampling, comparison with VE diffusion baseline.

**Not replicated:** Image generation (CIFAR-10/CelebA/LSUN), large-scale FID/IS benchmarks, architecture comparisons (NCSNv2 vs DDPM++), likelihood evaluation.

See [REPORT.md](REPORT.md) for detailed analysis.
