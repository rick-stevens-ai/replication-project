# Replication — OSTI 3003857

Paper: *Divide and Conquer: Learning Chaotic Dynamical Systems with
Multi-Step Penalty Neural ODEs*
(Chakraborty, Chung, Arcomano, Maulik — arXiv:2407.00568v5)

## Versions

| Version | Date | Coverage | Agreement | Notes |
|---|---|---|---|---|
| `v1/`          | Apr 21 2026 | 5/10 | 4/10 | Lorenz + partial KS, no Kolmogorov, no ERA5 |
| `v2_faithful/` | Apr 24 2026 | **7/10** | **5/10** | All three paper experiments implemented end-to-end |

## v2 summary

| Experiment | Ran | Key metric | Paper | Ours |
|---|---|---|---|---|
| Kuramoto–Sivashinsky | ✅ | NRMSE @ 1 $\tau_L$ | ~0.1–0.2 | **0.08** |
|                      |    | Forecast horizon | ≥2 $\tau_L$ | **1.7 $\tau_L$** |
|                      |    | Long-term attractor | bounded | slow drift (budget-limited) |
| Kolmogorov flow | ✅ | DNS correlation @ step 5 | >0.9 | 0.17 (under-trained) |
| ERA5 | ⚠️ synthetic proxy only | RMSE vs persistence | beats | beats (trivial proxy) |

**Gaps documented in `v2_faithful/report/report.pdf`** — ERA5 download blocked (TUM 401, GCS DNS). KS long-term and Kolmogorov skill need longer training plus the paper's Gaussian-SWA ensemble (not implemented here).

## Layout

```
v2_faithful/
├─ src/
│   ├─ mp_node.py         # shared MP-NODE module (MLP + Encoder-NODE-Decoder + dilated CNN)
│   ├─ ks.py              # Kuramoto–Sivashinsky experiment
│   ├─ ks_solver.py       # robust pseudospectral KS reference (BDF)
│   ├─ kolmogorov.py      # 2D Kolmogorov flow (custom GPU pseudospectral DNS + training)
│   ├─ era5.py            # ERA5 pipeline w/ WB download + synthetic fallback
│   └─ make_figures.py    # regenerates all report figures
├─ data/                  # cached reference trajectories (kept on training host)
├─ results/<exp>/         # best.pt, history.json, metrics.json, rollout.npz per experiment
└─ report/
    ├─ report.tex
    ├─ report.pdf         # 8-page report
    └─ figs/              # 8 PNG figures
```

## How to reproduce (uicgpu, merging env)

```bash
PY=/gpustor/stevens/anaconda3/envs/merging/bin/python
cd ~/mp_node_v2

# KS
env CUDA_VISIBLE_DEVICES=0 $PY src/ks.py \
  --T 2200 --n-traj 256 --epochs-per-mu 200 --K 8 --seg-len 16 --hidden 512

# Kolmogorov (runs ~15 min DNS + 15 min training on an A100)
env CUDA_VISIBLE_DEVICES=2 $PY src/kolmogorov.py \
  --T 800 --dt 2e-3 --n-traj 24 --K 12 --seg-len 5 --epochs-per-mu 200

# ERA5 (uses synthetic fallback; supply real WeatherBench .nc files in data/ to switch to real)
env CUDA_VISIBLE_DEVICES=3 $PY src/era5.py \
  --K 6 --seg-len 4 --n-traj 32 --epochs-per-mu 50

# Figures + PDF
python3 src/make_figures.py
cd report && pdflatex report.tex
```
