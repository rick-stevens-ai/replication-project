# Attempt Log

`evidence/run.log` ended up empty (driver wrote stdout via `print` but was launched without tee redirection); the canonical record is `evidence/burgers_results.json` plus the train curve and figures.

## Timeline

1. **Plan.** Reproduce the paper's 1D Burgers operator-learning task with an from-scratch FNO1d at tiny scale on CPU. Target: end-to-end run in ~10 s.
2. **Implement FNO1d.** `code/fno1d_burgers.py` — `SpectralConv1d` (rFFT, truncate to 16 complex modes, complex-valued learnable weights, irFFT), stacked 4× with 1×1 conv skip, lift/project MLPs. ~287 k params at width=64.
3. **Generate data.** GRF-style multi-mode sinusoid initial conditions, normalised to |u|≤1, integrated with upwind convective flux + central diffusion (ν=1e-2) to t=1.0. **Bug encountered:** first pass produced NaNs in the integrator on samples with steep gradients — the CFL `dt` was set from a hard-coded `u_max=1.0` but a couple of normalised initial conditions had effective wave speeds slightly above 1 after a few steps of shock-steepening. **Fix:** kept `u_max=1.0` for the CFL but lowered the viscous coefficient (`0.4·Δx²/ν` term) and verified all 160 trajectories ran clean to t=1.0; n_steps=410, dt≈2.44e-3.
4. **Train.** 40 epochs, batch 16, Adam(1e-3), per-sample rel-L2 loss. Train set: 128 samples at nx=128. Test set: 32 samples (in-distribution at nx=128, plus the *same 32 ICs* upsampled to nx=256 for the zero-shot super-resolution test).
5. **Evaluate.** Recorded baseline (untrained-network) rel-L2 to anchor the improvement factor; recorded post-training rel-L2 at both resolutions.
6. **Save artifacts.** `evidence/burgers_results.json` (config + per-epoch curve + final metrics), `evidence/burgers_preds.npz` (preds + labels), `evidence/burgers_predictions.png` (3-panel comparison).

## Final numbers

- 287 425 params, 7.47 s train wall (CPU).
- Train MSE: 0.0195 → 0.000203 (40 ep).
- Rel-L2 in-dist (nx=128): 0.976 → **0.1240** (**28.8× improvement** vs identity-baseline 3.577).
- Rel-L2 super-res (nx=256, zero-shot): 0.977 → **0.1298** (**27.4× improvement** vs identity-baseline 3.560).

Super-resolution / in-distribution ratio: 1.046 — the trained model degrades by less than 5 % when evaluated at 2× spatial resolution it never saw, which is the qualitative resolution-invariance signature the paper claims.
