# Yuval & O'Gorman 2020 — Paper Recon Notes

**Paper:** *Stable machine-learning parameterization of subgrid processes for climate modeling at a range of resolutions*
**Authors:** Janni Yuval, Paul A. O'Gorman (MIT EAPS)
**Venue:** Nature Communications **11**, 3295 (3 July 2020)
**DOI:** [10.1038/s41467-020-17142-3](https://doi.org/10.1038/s41467-020-17142-3)
**arXiv:** [2001.03151](https://arxiv.org/abs/2001.03151)

---

## What the paper actually does

The brief described this as a "neural network parameterization." **It is not.** The 2020 paper uses a **random forest (RF)** trained with `sklearn.ensemble.RandomForestRegressor` (sklearn 0.21.2). The NN version of the same idea is a follow-up paper (Yuval, O'Gorman & Hill 2021, GRL, arXiv:2010.09947) with code at `github.com/yaniyuval/Neural_nework_parameterization`. The brief's pointer to `janniyuval/keras_matlab_compatible` is also wrong — no such repo exists.

## High-level architecture

| Element | Spec |
|---|---|
| Algorithm | Random forest (sklearn 0.21.2 `RandomForestRegressor`) |
| Trees per forest | **10** (reduced to 5 post-hoc with no skill loss) |
| Min samples per leaf | **20** (7 for x32 due to fewer training samples) |
| Max depth | 27 (from code; not explicitly stated in paper) |
| Training samples | **5,000,000** for x4/x8/x16; fewer for x32 |
| RF file sizes | RF-tend x8 = 0.75 GB; RF-diff x8 = 0.20 GB (single-precision netcdf) |
| Training compute | **<1 hour on 10 CPU cores**. No GPU. |
| Two separate RFs | `RF-tend` (subgrid tendencies of hL, qT, qp + radiation) and `RF-diff` (turbulent diffusivity D) |

## Inputs and outputs (the x8 production RF, per OSF test_data_x8 README)

**Inputs (per atmospheric column):**
1. Temperature (48 levels)
2. Non-precipitating water q_n (48 levels)
3. Precipitating water q_p (48 levels)
4. Distance from equator (1 scalar)

**Outputs:**
5. Liquid/ice water static energy h_L tendency (48 levels)
6. Non-precipitating water q_T tendency (48 levels)
7. Precipitating water q_p tendency (48 levels)

Plus separate predictions for surface flux corrections, sedimentation, radiation, and (in RF-diff) the turbulent diffusivity D.

Outputs are standardized (zero mean, unit variance) before training; inputs are not (RF is scale-invariant).

## Source simulation

- **Model:** SAM (System for Atmospheric Modeling; Khairoutdinov & Randall 2003)
- **Domain:** Equatorial beta plane, zonal width 6912 km × meridional extent 17,280 km, aquaplanet
- **Grid:** 576 × 1440 × 48 (12 km horizontal, 48 vertical levels)
- **SST distribution:** qobs (zonally + hemispherically symmetric, max at equator)
- **Hypohydrostatic rescaling factor:** 4 (lets them use 12 km grid for what would otherwise need finer convection-resolving)
- **Duration:** 337.5 days of 3-hourly snapshots used for training/val/test (270/33.75/33.75 days)

## Coarse-graining factors evaluated

| Factor | Grid spacing | Notes |
|---|---|---|
| ×4  | 48 km   | Best offline + online R² |
| ×8  | 96 km   | Headline production simulation (x8-RF) |
| ×16 | 192 km  | |
| ×32 | 384 km  | Worst performance; fewer training samples available |

## Headline numbers

- **Offline R² of q_T tendency at x8:** ≈ 0.7–0.8 depending on level (Fig 3, Supp Fig 9, Supp Table 2)
- **Offline R² of instantaneous surface precipitation at x8:** **0.99** on test data
- **Stability:** x8-RF and x4-RF SAM simulations run **stably for the full simulation length** (multi-month integrations, no climate drift) and reproduce the mean precipitation and 99.9th-percentile extreme precipitation distributions of the hi-res simulation (Figs 1, 2)
- **Speedup:** x8-RF requires "roughly 30× less processor time" than the hi-res reference simulation
- **Failure mode:** Including RF radiative heating at all stratospheric levels causes a temperature drift; they hand-cap it at 11.8 km and fall back to SAM's radiation above

## Data and code availability

Both data and code on OSF: **[osf.io/36ypt](https://osf.io/36ypt/)** (DOI 10.17605/OSF.IO/36YPT).

### What's *actually* on OSF (verified 2026-05-27)

| Folder | Promised | Actually there |
|---|---|---|
| `subgrid_parameterization/` | Fortran SAM mods + MATLAB coarse-graining + Python RF training | ✅ `subgrid_parameterization.tgz` (1.7 MB) |
| `test_data_x8/` | Test pkl + `RF_tend_x8.nc` + `RF_diff_x8.nc` | ❌ README only, no data |
| `snapshots_different_resolutions/` | hi-res snapshot + 4 coarse-grained snapshots | ❌ EMPTY |

The READMEs in both data folders say "in process of being uploaded (due to COVID-19 I was unable to upload these folders due to their large size)." That was April 2020. Nearly 6 years later, **the data has never been uploaded.**

### Raw 3D SAM output on Google Drive

A successor (2021 NN) paper's repo points to `drive.google.com/drive/folders/1TRPDL6JkcLjgTHJL9Ib_Z4XuPyvNVIyY` ("DATA3D") for the underlying SAM output. **Only `readme.txt` is visible to anonymous users**; the actual data subfolders (`filesqobskm12x576/` etc.) require explicit Google Drive sharing permissions, which would need a request to the author. The subfolders contain 600 days of 3-hourly snapshots on a 576×1440×48 grid — order **terabytes**.

### Reproducing from raw output

Even with raw SAM output, one would have to:
1. Run their MATLAB coarse-graining pipeline (`high_res_processing_code/main.m`) on each snapshot to produce coarse-grained fields + resolved tendencies + subgrid contributions. Hardcoded for the Cheyenne supercomputer paths `/glade/scratch/janniy/...`.
2. Run `build_qp_production_x8.py` (Python) to assemble train/test pkls from those MATLAB outputs.
3. Run `run_qp_production_x8.py` to train the actual RF.
4. Re-implement the Fortran SAM hooks (provided as `sam_code/SRC/`) to run a coupled simulation for the online stability test — this requires a SAM build environment, MPI, and weeks of compute for a meaningful integration.

For a Tier-2 replication this end-to-end pipeline is far out of scope (weeks of compute + bespoke MATLAB + getting Google Drive access from the author).

## Verdict on replicability

- **Methodology:** Fully documented; RF architecture and hyperparameters reproducible in any modern sklearn.
- **Code:** Available (the 1.7 MB tgz on OSF); Python training scripts, MATLAB preprocessing, and Fortran SAM hooks all present.
- **Data:** **NOT available** through any of the three pointers (OSF test pkl, OSF snapshots, Google Drive DATA3D subfolders). Would require email-to-author and either Google Drive access or running SAM from scratch.
- **End-to-end re-run:** Practically infeasible within an 8-hour budget without prior coordination with the authors.

## Implications for the AI ATLAS P018 reinforcement

Reading the paper directly, it deserves the Tier-2 reinforcement: it's an unambiguous, peer-reviewed, well-cited (>200 citations) example of ML successfully producing a *stable* subgrid parameterization that runs coupled in a fluid-dynamics solver. The claim is real and the methodology is sound. What this replication attempt revealed is that the *empirical numbers* are not directly checkable against public artifacts without author cooperation — a not-unusual situation for 2020-era climate-ML papers.
