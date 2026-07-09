# PDEBench Replication (1D Advection, non-climate)

Lightweight open-data/open-source replication of one slice of
**PDEBench** (Takamoto et al., NeurIPS 2022 Datasets & Benchmarks):
upstream repo at https://github.com/pdebench/PDEBench
(MIT for most files; NEC academic-use license for `data_gen_NLE/` &
`models/{fno,unet,inverse}` headers — see REPORT.md §3).

We verify:

1. The PDEBench data-generation code (`AdvectionEq/advection_multi_solution_Hydra.py`)
   runs and produces physically-correct 1D advection solutions (≤5% rel-L2
   error vs the analytic shift `u(x,t)=u0(x-βt)` at the longest time on
   `nx=256`).
2. Their FNO1d baseline (`pdebench/models/fno/fno.py`) trained on
   that data with PDEBench's autoregressive rollout protocol and
   their RMSE/nRMSE `metric_func` gives a sensible nRMSE that beats
   a persistence baseline by ≈2.8×, even on a 100× smaller dataset
   than the published runs.

All compute on CPU, total wall-clock ≈ 80 s on a macOS laptop.

## Layout

```
pdebench/
├── README.md             this file
├── REPORT.md             claim-by-claim replication report
├── PROGRESS.md           timeline
├── scripts/              all replication scripts
├── data/                 small HDF5 we generated (24 MB)
├── results/              JSON summaries + saved tensors
├── figures/              sanity-check + training plots
├── logs/                 captured stdout/stderr
└── repo/                 fresh clone of pdebench/PDEBench (read-only)
```

## How to reproduce

```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-replications/pdebench
python3.12 -m venv venv && source venv/bin/activate
pip install --upgrade pip wheel
pip install "jax[cpu]" h5py hydra-core omegaconf "numpy<2" matplotlib torch

# 1. Clone PDEBench and apply the .loc -> .at JAX-API patch (see REPORT §4)
git clone --depth 1 https://github.com/pdebench/PDEBench.git repo
sed -i.bak 's/\.loc\[/\.at\[/g' repo/pdebench/data_gen/data_gen_NLE/utils.py

# 2. Drop in our small config
cp scripts/small.yaml repo/pdebench/data_gen/data_gen_NLE/AdvectionEq/config/multi/

# 3. Generate (~2 s)
( cd repo/pdebench/data_gen/data_gen_NLE/AdvectionEq && \
  JAX_PLATFORMS=cpu python advection_multi_solution_Hydra.py +multi=small )

# 4. Pack into PDEBench-style HDF5
python scripts/npy_to_pdebench_hdf5.py \
  --src-dir repo/pdebench/data_gen/data_gen_NLE/save/advection_small \
  --beta 1.0 --out data/1D_Advection_Sols_beta1.0.hdf5

# 5. Physics sanity check (~0.5 s)
python scripts/sanity_check_advection.py

# 6. Train FNO1d (~80 s on CPU)
python scripts/train_fno_advection.py

# 7. Plots + persistence baseline
python scripts/plot_results.py
```
