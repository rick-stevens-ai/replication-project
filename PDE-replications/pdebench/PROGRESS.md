# PDEBench Replication — PROGRESS

| time (CDT) | event |
| ---------- | ----- |
| 2026-05-28 12:11 | Workspace created at `~/Dropbox/REPLICATE-PROJECT/PDE-replications/pdebench/`. |
| 2026-05-28 12:11 | Shallow-cloned `https://github.com/pdebench/PDEBench` into `repo/`. |
| 2026-05-28 12:11 | Confirmed code MIT (LICENSE.txt at repo root); data CC BY 4.0 (DaRUS DOI 10.18419/darus-2986 v8). |
| 2026-05-28 12:11 | Confirmed climate datasets excluded (we use only 1D linear Advection β=1.0; PDEBench's "non-climate" suite includes advection / Burgers / diffusion-reaction / Navier-Stokes / shallow-water). |
| 2026-05-28 12:12 | Wrote `subagent-progress/pdebench.json` (within 10-min deadline). |
| 2026-05-28 12:13 | Created Python 3.12 venv, installed `jax[cpu] h5py hydra-core omegaconf torch numpy<2 matplotlib`. |
| 2026-05-28 12:14 | Added `config/multi/small.yaml` (nx=256, numbers=128, fin_time=2.0). |
| 2026-05-28 12:15 | Data gen failed: `AttributeError: DynamicJaxprTracer has no attribute loc` in `data_gen_NLE/utils.py`. 65 occurrences of `.loc[…].set(…)` need to be `.at[…].set(…)` for modern JAX. Patched with `sed`. |
| 2026-05-28 12:15 | Data gen succeeded in ~2 s; produced `1D_Advection_Sols_beta1.0.npy` shape `(128, 201, 256)`. |
| 2026-05-28 12:15 | Wrote `npy_to_pdebench_hdf5.py` (converts to the HDF5 layout `FNODatasetSingle` expects: `tensor`, `x-coordinate`, `t-coordinate`). HDF5 size 24 MB. |
| 2026-05-28 12:16 | Sanity check vs analytic shift via spectral FFT: max rel-L2 = 5.36e-2 at t=2.0 — consistent with 2nd-order finite-volume diffusion on a 256-pt grid. Plot saved. |
| 2026-05-28 12:17 | Wrote `train_fno_advection.py` — uses official `FNO1d` and `metric_func`; teacher-forced one-step training, autoregressive eval rollout, PDEBench's initial_step=10 protocol. |
| 2026-05-28 12:19 | Trained 40 epochs on CPU, 75.5 s. FNO1d (23,937 params, modes=12, width=20). Final TEST RMSE=2.14e-1, **nRMSE=3.08e-1**. |
| 2026-05-28 12:20 | Persistence baseline nRMSE=8.77e-1 on the same split — FNO beats it ≈2.85×, confirming the FNO learned the advection operator. |
| 2026-05-28 12:21 | Plots `training_curve.png` and `sample_rollout.png` written. |
| 2026-05-28 12:22 | Wrote `README.md`, `REPORT.md`. |

Status: **complete**.
