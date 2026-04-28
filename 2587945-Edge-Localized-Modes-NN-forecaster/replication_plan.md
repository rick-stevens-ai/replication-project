# Replication Plan — ELM NN Forecaster (OSTI 2587945)

## Target
Reproduce the *qualitative* finding that an attention-based RNN encoder–decoder beats FNO and a constant baseline at H=30-step ahead forecasting of 8×8 BES-like ELM intensity images.

## Compute
- spark-95fe (192.168.1.219), DGX Spark, NVIDIA GB10 (12.1), 128 GB unified memory.
- `~/comfyui-env/bin/python` — torch 2.10.0+cu130, CUDA available.
- Single-GPU PyTorch.

## Dataset (synthetic; real BES is non-public)
- 8×8 spatial grid, 1 µs sample step.
- Per "shot": 80,000 timesteps, ~30–60 ELM events. Each event = onset (rise 10→90 % in 200 µs) + peak (50 µs) + exponential relaxation (τ ≈ 250 µs).
- Spatial structure: peak amplitude varies smoothly across the 8×8 grid (radial gradient + ELM filament Gaussian) so the forecaster has to learn structure, not just per-channel time series.
- Background: low-amplitude broadband turbulence + slow MHD-like sinusoids per channel.
- Saturation: clip to 10.0 V (top half rows 0–3) and 5.0 V (bottom rows 4–7), as in the paper.
- 32 train shots, 4 val shots, 4 test shots. Sliding windows, history δ=30, horizon H=30.

## Models
1. **Constant**: ŷ_{t+i} = x_t for all i ∈ [1,H].
2. **FNO2D forecaster**:
   - Input: tensor (B, δ, 8, 8) (δ history channels).
   - 4 spectral conv2d layers, modes=4, hidden width 32, GELU.
   - Output: (B, 1, 8, 8) one-step prediction. Autoregressive rollout for H steps.
3. **ConvLSTM encoder–decoder + attention + smoothing** (≈ paper's best, simplified):
   - Encoder: 2-layer ConvLSTM (8×8 grid, hidden 32 channels), processes δ frames.
   - Decoder: ConvLSTM with Bahdanau-style attention over encoder hidden states; produces H frames autoregressively.
   - Smoothing layer: ŷ_i ← (1−α) ŷ_i + α x_t (learned scalar α), as Eq. 9 in paper.

## Training
- Two-stage: (a) pretrain with direct one-step MSE; (b) finetune with H-step autoregressive MSE.
- Adam lr 1e-3, batch 32, 8 epochs pretrain + 8 epochs finetune (FNO and ConvLSTM both).
- Mixed precision off (small model, GB10 capability cap).

## Evaluation (matches paper)
- Per-event prediction correlation ρ_pred (Pearson, full predicted vs real series).
- Residual correlation ρ_resid w.r.t. constant baseline.
- MSE vs. lead time (1…H).
- **Bonus (task brief): ROC for classifying onset-in-next-H-steps**. Onset label = max gradient of mean-channel signal over the next H steps exceeds threshold. Score = max gradient of *forecast* sequence. ROC-AUC reported per model.

## Success criteria
- Both NN models beat constant baseline on ρ_pred and ρ_resid.
- FNO and ConvLSTM ROC-AUC > 0.7 on onset classification.
- ConvLSTM ≥ FNO on ρ_pred (matches paper's qualitative ordering).

## Budget
- 6 h wall total. Code + train: ~3 h. Eval/plots/report: ~1 h. Buffer: 2 h.
