# FNO-Original (Wave 4) — Brief

**Bundle:** `~/Dropbox/REPLICATE-PROJECT/PDE-replications/fno-original-wave4/`
**Date:** 2026-06-16
**Author:** Ollie (OpenClaw subagent, Claude Opus 4.7 via Argo)

## What we're testing

The two headline claims of Li et al. *Fourier Neural Operator for Parametric PDEs* (ICLR 2021), reproduced directly on the paper's canonical **1D viscous Burgers** operator-learning task (map `u(x, t=0) → u(x, t=1)` for `u_t + u u_x = ν u_xx`, periodic BCs):

1. **C1 — Operator learning.** An FNO1d (4 spectral conv layers, 16 modes, width 64; ~287 k params) trained on (u₀, u₁) pairs achieves low relative-L2 test error.
2. **C2 — Discretization invariance.** The same trained model, evaluated zero-shot at a *higher* spatial resolution than it saw during training, still produces accurate predictions.

## Why this complements `fno-neuraloperator/REPORT.md`

The existing `fno-neuraloperator/` bundle (2026-05-28) exercises the **maintained downstream library** (`neuraloperator==2.0.0`) on its bundled **2D Darcy** tutorial — a downstream, productised version of FNO on a different PDE.

This Wave-4 bundle targets the **original paper's algorithm directly**, in a **from-scratch numpy/PyTorch implementation of FNO1d**, on the **paper's own 1D Burgers task**. The two together cover:

| Aspect | `fno-neuraloperator/` | `fno-original-wave4/` (this) |
|---|---|---|
| Source | maintained library | from-scratch reimpl of paper |
| PDE | 2D Darcy flow (elliptic) | 1D Burgers (hyperbolic+viscous) |
| Resolution test | 16² → 32² zero-shot | 128 → 256 zero-shot |
| Scale | 1 000 train, ~192 k params | 128 train, ~287 k params |
| Wall-clock | 184 s CPU (20 ep) | 7.5 s CPU (40 ep) |

The Wave-4 run is intentionally **tiny-scale** (128 samples, 40 ep, CPU) — a faithful re-implementation of the architecture and a qualitative test of the headline claims, not a numerical match of the paper's headline error bar (which used 1000+ samples on GPU).
