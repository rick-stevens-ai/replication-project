# FNO / NeuralOperator — Replication Bundle

**Target:** [`neuraloperator/neuraloperator`](https://github.com/neuraloperator/neuraloperator)
(Fourier Neural Operator library, MIT License, PyTorch Ecosystem project).

**Task:** Reproduce the *FNO-on-Darcy-Flow* tutorial — a non-climate
2-D PDE benchmark (Darcy permeability → pressure field) — and verify two
canonical FNO claims:
1. FNO learns a PDE solution operator with low relative L2 from a modest
   number of supervised samples.
2. FNO is **resolution-invariant**: a model trained at 16×16 evaluates
   without retraining at 32×32 (zero-shot super-resolution).

## Quickstart

```bash
cd "$(dirname "$0")"
uv venv --python 3.12 .venv          # one-time
source .venv/bin/activate
uv pip install neuraloperator matplotlib torch
uv pip install "numpy<2"             # neuraloperator pins torch==2.2.2 (NumPy 1.x ABI)
python scripts/train_fno_darcy.py --epochs 20 --seed 0
```

Outputs land in `results/metrics.json`, `figures/darcy_16.png`,
`figures/darcy_32_zeroshot.png`, and `logs/train_20ep.log`.

## Files

| Path | Purpose |
|------|---------|
| `scripts/train_fno_darcy.py` | Self-contained training/eval script (adapted from upstream `examples/models/plot_FNO_darcy.py`). |
| `logs/train_20ep.log` | Console log of the 20-epoch run (CPU, ~184 s). |
| `logs/sanity_2ep.log` | Initial 2-epoch sanity check. |
| `results/metrics.json` | Machine-readable metrics: config, pre/post relative-L2 at 16² and 32². |
| `figures/darcy_16.png` | Train-resolution predictions (3 samples × {input, GT, prediction}). |
| `figures/darcy_32_zeroshot.png` | Zero-shot super-resolution at 32² for the model trained on 16². |
| `PROGRESS.md` | Time-stamped progress log. |
| `REPORT.md` | Full replication report (claim-by-claim, agreement score, limitations). |

## License notes

NeuralOperator: MIT (verified 2026-05-28 via GitHub API).
This bundle is also MIT-compatible: all training data ships inside the
`neuraloperator` package as a small public sample.
