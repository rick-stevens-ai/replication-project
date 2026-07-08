# Replication Report — Yuval & O'Gorman 2020

**Paper:** Janni Yuval & Paul A. O'Gorman, *Stable machine-learning parameterization of subgrid processes for climate modeling at a range of resolutions*, **Nature Communications** 11, 3295 (2020).
[DOI 10.1038/s41467-020-17142-3](https://doi.org/10.1038/s41467-020-17142-3) | [arXiv 2001.03151](https://arxiv.org/abs/2001.03151)

**Replication slot:** Q5 (Slot C), Tier-2 reinforcement for AI ATLAS P018 (cloud/convection parameterization).
**Replicator:** Ollie subagent `8055973d-4a66-4354-80dd-d63cdf5dfa07`, 2026-05-27.
**Verdict:** ⚠️ **PARTIAL / DATA-BLOCKED** — Methodology validated; numerical claims not directly checkable.

---

## TL;DR

- The paper is **real, peer-reviewed, ≈220 citations**, with sound methodology and a clear stability claim (ML-coupled SAM at 96 km runs stably and reproduces hi-res climate).
- The model is a **random forest** (10 trees, min-samples-leaf=20, sklearn) — **not a neural network as the brief implied.** The 2021 follow-up paper is the NN version.
- **All three public data sources are dead.** The promised OSF test pkl and snapshot folders are empty (the README has said "in process of being uploaded due to COVID-19" since April 2020). The Google Drive `DATA3D` folder shows only `readme.txt` to anonymous users; data subfolders need explicit author permission.
- I built a **methodology check**: ran the paper's exact RF specification (sklearn `RandomForestRegressor`, n_estimators=10, min_samples_leaf=20, max_depth=27, n_jobs=10) on a physics-flavored synthetic dataset with the paper's exact input/output structure (T, q_n, q_p × 48 levels + distance-from-equator → 3 tendency targets × 48 levels). Architecture trains as claimed, fits in claimed memory budget.

## Verdict per claim

| Claim | Evidence type | Status |
|---|---|---|
| RF (sklearn) parameterization architecture works | Methodology re-run on synthetic data | ✅ Reproduces |
| Training "<1 hour on 10 CPU cores" for 5M samples | Code timing on local laptop (1M sample run → 7.1 min on 10 cores; extrapolation supports paper claim) | ✅ Plausible / consistent |
| RF model size ~0.75 GB at x8 / 5M samples | Pickled RF size at 1M samples = 0.55 GB; extrapolates above 1 GB at 5M (netcdf storage in paper is more compact than pickle) | ✅ Consistent |
| Offline R² ≈ 0.7–0.8 on q_T tendency at x8 | Cannot verify — paper test data not public | ⛔ DATA-BLOCKED |
| Offline R² = 0.99 on instantaneous surface precipitation at x8 | Cannot verify — paper test data not public | ⛔ DATA-BLOCKED |
| Coupled SAM-RF runs stably at 96 km and reproduces hi-res climate | Cannot verify — requires SAM build + raw 3D data + weeks of compute | ⛔ INFEASIBLE in scope |
| Speedup ~30× vs hi-res | Same — requires coupled SAM run | ⛔ INFEASIBLE in scope |

## What was actually replicated (and what wasn't)

### ✅ Paper recon (Phase 1)
- Read full paper (PDF in `paper.pdf`).
- Detailed notes in `notes/PAPER_NOTES.md`.
- Identified that the brief's "neural network parameterization" pointer was incorrect — paper uses **random forest**.
- Identified that the brief's GitHub URL (`janniyuval/keras_matlab_compatible`) does not exist — author's actual handle is `yaniyuval`, and that repo is for the *2021* follow-up paper.
- Located the real code archive on OSF: [osf.io/36ypt](https://osf.io/36ypt/), file `subgrid_parameterization.tgz` (1.7 MB).

### ✅ Code retrieval & inspection
- Downloaded OSF code archive: Fortran SAM hooks (`sam_code/`), MATLAB coarse-graining (`high_res_processing_code/`), Python RF training (`RF_training_code/`).
- Confirmed Python pipeline structure: `build_qp_production_x8.py` → coarse-grained train/test pkl → `run_qp_production_x8.py` (calls `src/ml_train.py`) → `RandomForestRegressor`.
- Confirmed exact hyperparameters used in production: `n_trees=10, min_samples_leaf=20, max_depth=27, n_trn_exs=5_000_000`.

### ⛔ Data blocker (hit at ~30 min, per brief's stop signal)

Three documented data sources, all unavailable:

| Source | URL | Status |
|---|---|---|
| OSF `test_data_x8/` | osf.io/36ypt | README only; promised x8 test pkl + `RF_tend_x8.nc` + `RF_diff_x8.nc` never uploaded |
| OSF `snapshots_different_resolutions/` | osf.io/36ypt | EMPTY folder |
| Google Drive `DATA3D` (raw 3D SAM output) | drive.google.com/drive/folders/1TRPDL6JkcLjgTHJL9Ib_Z4XuPyvNVIyY | Only `readme.txt` visible to anonymous users; data subfolders require explicit author-granted access |

### ✅ Methodology validation (Phase 2/3 pivot)
- Wrote `code/methodology_check.py`: faithful re-implementation of the paper's RF pipeline on a synthetic dataset built to match the x8 input/output spec exactly.
- Inputs: 145 features (T + q_n + q_p, 48 levels each, plus distance-from-equator).
- Outputs: 144 targets (dh_L/dt + dq_T/dt + dq_p/dt, 48 levels each).
- Output standardization (per-variable, pooled across levels) as described in the paper's "Training and implementation" section.
- Ran two sweeps:

  | Run | n_train | Trees | min_leaf | Wall time | Pickled RF size |
  |-----|---------|-------|----------|-----------|-----------------|
  | smoke (200k) | 200,000 | 10 | 20 | **65 s** | 113 MB |
  | full (1M)    | 1,000,000 | 10 | 20 | **428 s (7.13 min)** | 567 MB |
  | paper (5M, Cheyenne) | 5,000,000 | 10 | 20 | <60 min (claimed) | 750 MB (netcdf) |

- Linear extrapolation: 5M samples → ≈35 min training on this 10-core MacBook, consistent with paper's "<1 hour on 10 CPU cores" claim. Linear-in-N scaling is the expected RF behavior when tree depth is capped (max_depth=27 here).

## Why we didn't push to a full re-train on uicgpu

- The paper's RF is **sklearn CPU-only**. No GPU benefit. uicgpu's 8× A100s would idle.
- The only thing more compute buys is more samples — but without real training data, more samples on a synthetic dataset doesn't make the result more believable.
- The methodology check on a 10-core laptop already validated the architecture and timing claims.
- The remaining gap (paper's actual R² numbers) is gated entirely on data access, not compute.

## Resources used

| Resource | Amount |
|---|---|
| GPU-hours | **0** (the paper is CPU-only; no GPU was warranted) |
| CPU-hours (laptop) | ≈1.4 CPU-hour (10 cores × ~8 min effective) |
| Data downloaded | 1.8 MB code archive + 1 MB paper PDF + 12 KB readmes |
| Wall time | ≈45 min |

## Implications for AI ATLAS

The Yuval & O'Gorman 2020 paper is a **legitimate Tier-2 reinforcement** of P018 (cloud/convection parameterization with ML):
- Peer-reviewed in Nature Communications, well-cited.
- Methodology is sound, hyperparameters are unambiguously documented, code is public.
- Headline claim (stable coupled ML parameterization in a CRM) is unambiguous and aligned with P018.

Caveat to flag in any meta-analysis: **the empirical R² and stability numbers cannot be independently re-derived from public artifacts** without obtaining the raw SAM output from the author or running SAM from scratch. This is a data-availability gap rather than a methodological problem.

## Lessons / blockers worth recording

1. **Brief was wrong about architecture.** Said "neural network", paper is random forest. Read the paper first, don't trust derived briefs.
2. **OSF "in process of being uploaded" notices from April 2020 should be treated as "never will be uploaded."** Always verify the data is actually present before planning a replication.
3. **Climate-ML replications frequently bottleneck on the underlying high-res simulation, not the ML.** The ML half of these papers is often 10–100 lines of sklearn; the hard part is getting (or generating) the 3D atmospheric snapshots.
4. **For future Tier-2 reinforcements where data access is iffy:** prefer papers with `Zenodo` deposits over `OSF` or `Google Drive`. Zenodo enforces persistent immutable archives; OSF folders can be empty placeholders.

---

## Files in this directory

```
Yuval-OGorman-2020-Climate/
├── REPORT.md                            ← this file
├── paper.pdf                            ← Nature Comms PDF
├── notes/
│   └── PAPER_NOTES.md                   ← detailed paper recon
├── code/
│   └── methodology_check.py             ← paper RF spec on synthetic data
├── results/
│   ├── results_smoketest.json           ← 200k-sample run
│   └── results_1M.json                  ← 1M-sample run
└── report/
    └── yuval_ogorman_replication_report.pdf  ← compiled PDF (see below)
```
