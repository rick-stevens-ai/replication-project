# 2587945 — Spatiotemporal forecasting of ELMs in tokamak plasmas

**Paper:** Samaddar, Madireddy, Gong, Hansen, Smith, Balapraksh et al., "Spatiotemporal forecasting of the edge localized modes in tokamak plasmas using neural networks," *Mach. Learn.: Sci. Technol.* 6 (2025) 035041. doi:10.1088/2632-2153/adfb41 — OSTI 2587945.

**Affil:** ANL / ORNL / Columbia / U-Wisconsin / PPPL.

## What the paper does
Forecasts future frames (8×8 BES Beam-Emission-Spectroscopy intensity images at 1 MHz) over a horizon H = 30/50/80 µs from DIII-D Type-I ELM events. Compares:
- Constant baseline (predict last value)
- Chronos-T5 (foundation model, fine-tuned)
- 2D Fourier Neural Operator (FNO)
- Adaptive FNO (AFNO)
- Temporal VAE
- **LSTM encoder-decoder with attention + 3D conv + smoothing layers (best, ρ_pred=0.959 @30µs).**

Metric: per-event Pearson correlation between predicted and real series, plus residual correlation against the constant baseline. No ROC reported (regression task).

## What this replication does
- Generates a **synthetic 8×8×T BES-like ELM dataset** with realistic onset (10→90% rise), peak, and exponential relaxation, plus background turbulence and per-channel saturation clipping. Multiple events per shot, 1 MHz sample rate.
- Trains and compares **three models** identical in spirit to the paper's lineup:
  1. **Constant baseline** (no learning).
  2. **FNO-2D forecaster** — minimal Fourier neural operator over 8×8 spatial grid, with δ history channels in / 1 out, autoregressive rollout for H=30 steps.
  3. **ConvLSTM encoder-decoder** with attention + smoothing layer (the paper's best architecture, simplified).
- Evaluates with the paper's prediction-correlation and residual-correlation, plus MSE vs. lead time.
- Adds a **derived classification ROC** for "ELM-onset within next H steps" since the task brief asked for ROC. The classifier is trained on the *forecasted* future window — i.e., does the forecaster's output enable downstream onset detection?

## Honesty notes
- The real BES dataset is **not publicly released** (paper §Data Availability: "available upon reasonable request"). No author code repo was published. So this is a *methodological* replication on synthetic data with the same shape (8×8, 1 MHz, ELM-like events).
- Synthetic data means absolute correlation numbers are not directly comparable to the paper. We report relative ranking of models and qualitative behavior.

See `replication_plan.md`, code in `code/`, results in `results/`, score in `REPORT.md`.
