# Artifact Harvest

## Upstream code

- **Original repo:** `zongyi-li/fourier_neural_operator` — **renamed/moved** to `neuraloperator/neuraloperator` (and packaged on PyPI as `neuraloperator==2.0.0`). Both refs still resolve on GitHub via redirect.
- **Paper:** Li, Kovachki, Azizzadenesheli, Liu, Bhattacharya, Stuart, Anandkumar — *Fourier Neural Operator for Parametric Partial Differential Equations*, ICLR 2021 ([arXiv:2010.08895](https://arxiv.org/abs/2010.08895)).
- **License:** MIT (verified in sibling bundle `fno-neuraloperator/REPORT.md`, 2026-05-28).

## What we harvested vs built

The upstream `fourier_neural_operator/` repo ships canonical example scripts (`fourier_1d.py`, `fourier_2d.py`, `Adam.py`, `utilities3.py`) plus large pre-generated `.mat` datasets pinned in `README.md` (Burgers `burgers_data_R10.mat` ~1.7 GB, Darcy `piececonst_*.mat` similar, Navier-Stokes much larger). Running the upstream examples requires:

1. Downloading those `.mat` files from the authors' GDrive/Caltech mirror.
2. The author-specific `utilities3.LpLoss` + `Adam.Adam` glue, including a custom Adam variant.
3. ~30 min GPU training to hit the headline numbers.

**For a tiny-scale CPU replication of the *algorithm*, this round-trip is wasteful.** Instead we:

- **Re-implemented FNO1d from scratch** in `code/fno1d_burgers.py` (~270 lines): 4 stacked `SpectralConv1d` blocks (the rFFT → keep first `modes=16` complex coeffs → learnable complex weights → irFFT trick), 1×1 conv skip path, ReLU activations, lift/projection MLPs — architecture matches the paper's Section 5.1 spec.
- **Generated 128+32 Burgers (u₀, u₁) pairs in-house** via a simple upwind+central-diffusion scheme on the same family of multi-mode random initial conditions the paper uses (smooth low-mode sinusoids, |u|≤1), ν=1e-2, t_final=1.0. No GDrive download.
- **Trained on CPU for 40 epochs (~7.5 s)** with Adam(1e-3) and per-sample relative-L2 loss.

This trades absolute numerical match against the paper's headline (their 0.001–0.01 rel-L2 needs 1000+ samples on a GPU) for an **architecturally faithful**, **fast**, **reproducible-anywhere** check of the qualitative claims.

The upstream repos remain checked out under `code/{fourier_neural_operator,neuraloperator,zongyi-li-fno}/` for reference.
