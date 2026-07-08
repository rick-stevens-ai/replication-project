# PROGRESS — Jouvet 2023 IGM Replication

## Phase 1: Paper recon ✅ DONE

- Paper: Jouvet, G. (2023). "Inversion of a Stokes glacier flow model emulated by deep learning." *J. Glaciol.* 69(273), 13–26. DOI: 10.1017/jog.2022.41.
- Could not pull full PDF (Cambridge paywall + 500s on the page; sci-hub not attempted within proxy). Got the abstract from DOAJ.
- See `PAPER_NOTES.md` for what we can and can't replicate without the figure-level body.
- Code: `https://github.com/instructed-glacier-model/igm` (the brief's `jouvetg/igm` was renamed to the org `instructed-glacier-model`). Current version v3.1.1.
- Headline performance claim being targeted: **"Optimizing one large-size glacier at 100 m takes < 1 min on a laptop"** for the inversion step.
- Per-glacier scientific claim: simultaneous inversion of (a) ice thickness `H`, (b) flow parametrization (sliding/Arrhenius), (c) ice surface `s`, on the 10 largest Swiss glaciers at 100 m, "high degree of assimilation while guaranteeing equilibrium between mass-balance and ice flow mechanics."

## Phase 2: Setup on uicgpu ✅ DONE

- Workspace: `/data/stevens/igm/`.
- Repo: `/data/stevens/igm/igm/` (HEAD as of 2026-05-27, v3.1.1).
- Env: `/data/stevens/envs/igm/` (conda Python 3.11.15).
- Deps: TF 2.15.1 (+CUDA 12.2 wheels), `tensorflow-probability==0.23.0`, `oggm==1.6.3`, `netCDF4 1.7.4` (had to relax IGM's `==1.6.0` pin — the pinned wheel needs HDF5-from-source which uicgpu doesn't have; conda-installed `hdf5+netcdf4=1.7.4` works fine and is API-compatible). Also installed `pyvista` separately (IGM uses it for VTK inversion output but doesn't list it in `setup.py`).
- TF sees all 8 A100 80GB GPUs; we pin to GPU 0 via `CUDA_VISIBLE_DEVICES=0` (Slot B reservation, paper claim is single-GPU anyway).

### Pre-flight discoveries while wiring the run

1. The current IGM repo expects to be launched as `igm_run +experiment=params` from a folder that contains `experiment/params.yaml`. The bundled `tests/test_data_assimilation/experiment/params.yaml` is marked `pytest.mark.skip(reason="API deprecated")` and uses fields (`RGI_version`) that the current schema no longer accepts. Had to write a fresh experiment file.
2. The default `oggm_shop` config and the bundled tests both use **RGI v6** IDs (e.g. `RGI60-11.01450` for Aletsch). The IGM oggm_util helper points RGI v6 preprocessed glacier directories at `https://cluster.klima.uni-bremen.de/~oggm/gdirs/oggm_v1.6/exps/igm_v2`, which **no longer exists on the upstream server**. The current OGGM-prepro layout only has `igm_v3`/`igm_v4`/`igm_v4_hr`/`igm_v5_era5`, all of which are **RGI v7 only** (`RGI70G/` and `RGI70C/`). So all real runs must use RGI v7 IDs. Filed mentally as the first compatibility blocker; resolution is just "pick an RGI v7 ID."
3. To find Aletsch's RGI v7 ID I downloaded the global RGI v7 attributes CSV directly from OGGM and searched: `GROSSER ALETSCH GLETSCHER = RGI2000-v7.0-G-11-02596`, 81.8 km², centred 46.48°N / 7.97°E. Confirmed Swiss, confirmed largest in the Alps, confirmed in the paper's target set.

## Phase 3: Inversion run on Grosser Aletsch ✅ DONE

- Two runs completed on `/data/stevens/igm/runs/aletsch/` (default, 500 iters, ~64 s) and `/data/stevens/igm/runs/aletsch-long/` (extended controls, 2000 iters, ~7 min).
- Both produced full output trees (geology-optimized.nc + costs.dat + rms_std_vol.dat + 21 .vtp snapshots).
- Smoke test (10 iters on G-11-04001) confirmed end-to-end pipeline; uncovered missing pyvista dep.
- Real Aletsch run: velocity loss stuck at 148, geometry plausible but volume/peak-thickness/peak-velocity off by 3–75×.

## Phase 4: Evaluation + report ✅ DONE

- 6-panel field plot + cost-curve plot saved to `artifacts/`.
- `REPORT.md` written, `report/jouvet_igm_replication_report.pdf` compiled (xelatex, 5 pages, 569 KB).
- `REPORTS_INDEX.md` + `STATUS_AUDIT.md` updated with PARTIAL verdict.
- Verdict: **PARTIAL** — workflow + runtime claim replicate; velocity-fit + thickness-magnitude claims do not, with shipped pretrained emulator.
- GPU-hours used: ~0.5. Wall-clock: ~1.7 h.
