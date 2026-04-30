# Space-CAMELS Emulator

A neural network emulator for the cosmological matter power spectrum P(k), inspired by [CosmoPower](https://arxiv.org/abs/2106.03846) (Spurio Mancini et al. 2022) and the [CAMELS](https://arxiv.org/abs/2010.00619) project (Villaescusa-Navarro et al. 2021).

## What It Does

Replaces expensive Boltzmann solver calls (CAMB/CLASS, ~500ms each) with a neural network that predicts P(k) in ~2 microseconds — a **277,000× speedup** — while maintaining sub-1% mean accuracy.

Given 6 cosmological parameters (Ω_m, σ_8, Ω_b, h, n_s, w), the emulator predicts the linear matter power spectrum at 50 log-spaced wavenumbers k ∈ [10⁻⁴, 10] h/Mpc.

## Quick Start

```bash
# Generate training data (500 cosmologies via CAMB)
pip install camb scipy torch matplotlib
python replication/code/gen_dataset.py

# Train emulator (~25s on GPU)
python replication/code/train_emulator.py

# Evaluate and generate plots
python replication/code/eval.py
```

## Architecture

- **Input:** 6 cosmological parameters (standardized)
- **Network:** 4-layer MLP, 256 hidden units, GELU activations
- **Output:** log₁₀ P(k) at 50 k-bins (standardized)
- **Parameters:** ~212,000
- **Training:** AdamW, cosine annealing LR, 80/20 train/test split

## Results

| Metric | Value |
|--------|-------|
| Mean percent error | 0.93% |
| 95th percentile error | 3.4% |
| CAMB time per cosmology | 525 ms |
| Emulator time per cosmology | 0.002 ms |
| Speedup factor | 277,000× |
| Training cosmologies | 400 (of 500 total) |
| Model parameters | 212,018 |

## Project Structure

```
replication/
├── code/
│   ├── gen_dataset.py       # Generate P(k) dataset with CAMB
│   ├── train_emulator.py    # Train MLP emulator
│   └── eval.py              # Evaluate accuracy & speed, make plots
├── data/
│   ├── params.npy           # (500, 6) cosmological parameters
│   ├── pks.npy              # (500, 50) power spectra
│   ├── k_bins.npy           # (50,) wavenumber bins
│   └── emulator_best.pt     # Trained model checkpoint
├── figures/
│   ├── pred_vs_true.png     # P(k) predictions vs CAMB truth
│   ├── error_vs_k.png       # Error distribution vs wavenumber
│   └── speed_comparison.png # CAMB vs emulator timing
└── results/
    ├── eval_results.json    # Quantitative results
    └── training_history.json
```

## References

- Spurio Mancini, A. et al. (2022). "CosmoPower: emulating cosmological power spectra for accelerated Bayesian inference from next-generation surveys." *MNRAS*, 511(2), 1771–1788.
- Villaescusa-Navarro, F. et al. (2021). "The CAMELS project: Cosmology and Astrophysics with Machine-learning Simulations." *ApJ*, 915, 71.
- Villaescusa-Navarro, F. et al. (2023). "The CAMELS Multifield Dataset: Learning the Universe's Fundamental Parameters with Artificial Intelligence." *ApJS*, 265, 54.

## License

Research/educational use. Dataset generated with CAMB (Lewis & Challinor 2011).
