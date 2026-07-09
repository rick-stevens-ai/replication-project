# Brief — OSTI 3374566 (arXiv 2409.03833)

**Paper:** Tiki, Pham, Huerta (2025) — *Sequence modeling of higher-order wave
modes of quasi-circular, spinning, non-precessing binary black hole mergers*.

**What:** A causal transformer that forecasts both plus and cross gravitational-wave
polarisations `(h+, h×)` — including higher-order spherical-harmonic modes up to
ℓ=4 plus (5,5) — through late inspiral, merger and ringdown, from an inspiral-only
input window. Trained on 14 M waveforms generated with the NRHybSur3dq8 surrogate.

**Why replicate:** The paper releases the trained checkpoint and inference code on
GitHub, and the training/test data can be regenerated for free with the public
`gwsurrogate` package. That makes it a genuinely re-runnable claim — the released
model.ckpt loads cleanly into their PyTorch architecture, we sample fresh
in-distribution `(q, sz1, sz2, θ)` points off the training grid, autoregressively
forecast the 115-timestep decoder window, and compute the same normalised
inner-product overlap against surrogate ground truth. Our 24-sample independent
run reproduces the paper's headline fidelity: mean overlap 0.977 (median 0.994)
vs. the paper's 0.996/0.997 on 840,000 samples.
