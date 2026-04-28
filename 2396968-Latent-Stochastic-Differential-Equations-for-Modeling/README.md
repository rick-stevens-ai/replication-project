# Latent Stochastic Differential Equations for Modeling Quasar Variability and Inferring Black Hole Properties

- **OSTI ID:** 2396968
- **Rank:** #27
- **Replication Score:** 9/10 (paper); **v1 (1-band, deprecated) 4-6/10**; **v2 (paper-faithful, 6-band, A100) 7/10**
- **v2 report:** [`replication/v2_faithful/report/report.pdf`](replication/v2_faithful/report/report.pdf)
- **v2 training:** 18.08 h on uicgpu A100, 8 epochs, 20k curves, 917,594 params, full 6-band + Sim5 GR + 9-param Cholesky head
- **v2 headline:** LC RMSE 0.1091 mag (paper 0.0959, 1.14×); 1σ/2σ/3σ coverage 73.3/94.5/99.0% (paper ~70/95/99.7%); per-parameter ranking matches paper exactly
- **Open-Source Tools:** Yes (PyTorch + torchsde)
- **Code Repository:** No (paper); this directory contains a from-scratch simplified replication

## What was replicated

A single-band simplification of Fagin et al. (2024): encoder → latent Itô SDE (learned prior drift,
diagonal diffusion) → decoder, trained with reconstruction NLL plus Girsanov KL via
`torchsde.sdeint(..., logqp=True)`. We skip the 6-band LSST pipeline, the physical accretion-disk
transfer functions, and the 9-parameter black-hole inference head.

## Quantitative summary

| Model | RMSE (mag) | MAE (mag) | NLL |
|---|---|---|---|
| Paper latent-SDE (6-band) | 0.0959 | 0.0695 | −1.14 |
| Paper GPR (Matern-½, 6-band) | 0.0978 | 0.0711 | −1.01 |
| **Ours latent-SDE (1-band, 512 train)** | 0.198 | 0.149 | +0.49 |
| **Ours GPR (Matern-½, LOO, 1-band)** | 0.048 | 0.034 | −1.85 |

The gap to the paper is driven by (i) single-band setup — the paper's edge over GPR largely comes
from sharing information across six bands, (ii) a ~2000× smaller training set, (iii) an ~17×
smaller model, and (iv) ~3000× less training compute (160 s CPU vs ~6 weeks V100).

## Layout

```
replication/
├── code/
│   ├── simulate.py      # DRW light curves w/ LSST-like seasonal gaps
│   ├── model.py         # Encoder + Latent-SDE (torchsde) + Decoder
│   ├── train.py         # training loop (KL annealing, grid binning)
│   ├── baseline_gp.py   # DRW GPR baseline (Matern-½)
│   └── evaluate.py      # test metrics + plots
├── data/                # pickled train/val/test datasets
├── results/             # history.json, best.pt, metric json files, train.log
├── figures/             # reconstructions.png, training_curves.png, latent_paths.png
└── report/report.{tex,pdf}
```

## How to reproduce (CPU, ~3 min total)

```
# one-time: pip install torch torchsde numpy scipy matplotlib
cd replication/code
python simulate.py                                           # ~5 s
python train.py --epochs 80 --batch_size 32 --T_grid 64      # ~160 s
python baseline_gp.py                                        # ~60 s
python evaluate.py                                           # ~40 s
```

## Status
- [x] Paper reviewed
- [x] Code/tools identified (PyTorch + torchsde)
- [x] Code implemented (from scratch — no public repo)
- [x] Simplified results reproduced (single-band DRW)
- [ ] Full-scale results validated against paper (out of scope: 6 weeks V100)

## Notes / Caveats

- `torchsde.sdeint(..., logqp=True)` is exactly the Li-et-al. 2020 / Fagin-et-al. formulation for
  the Girsanov KL between posterior and prior SDE paths.
- The learned prior drift is important: without it, the KL collapses the posterior to Brownian
  motion and the model can't encode information about the observed trajectory.
- The `hf` conda env on CherryRd (`/Users/stevens/opt/anaconda3/envs/hf`) has compatible versions
  (PyTorch 2.0.1, torchsde 0.2.6). System Python 3.14 is too new for current PyTorch wheels.
