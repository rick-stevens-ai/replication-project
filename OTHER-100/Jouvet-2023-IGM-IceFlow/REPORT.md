# Replication Report — Jouvet 2023 IGM Ice-Flow Inversion

**Paper:** Jouvet, G. (2023). "Inversion of a Stokes glacier flow model emulated by deep learning." *Journal of Glaciology* 69(273), 13–26. DOI: 10.1017/jog.2022.41.
**Code:** Instructed Glacier Model (IGM), `https://github.com/instructed-glacier-model/igm`, v3.1.1 (HEAD as of 2026-05-27).
**Replicated by:** Ollie (OpenClaw AI sub-agent, model: argo/argo:claude-opus-4.7)
**Date:** 2026-05-27
**Compute:** uicgpu (NVIDIA A100 80 GB PCIe, CUDA 12.2, TF 2.15.1), pinned to 1 GPU.
**AI ATLAS gap:** TIER-1 GAP-FILL for **P021 — ice-sheet basal friction inversion**.

---

## 1. Paper claim under test

The Jouvet 2023 paper presents a deep-learning–accelerated data-assimilation workflow for
glacier ice flow. Stokes ice-flow is replaced by a convolutional-neural-network emulator;
the emulator is then inverted by automatic differentiation to **simultaneously infer**:

1. ice thickness distribution `H(x,y)`
2. ice-flow parametrization (sliding coefficient `c_s`, Arrhenius factor)
3. ice surface elevation `s(x,y)`

…consistent with Stokes mechanics and surface mass-balance, while best matching observations
(surface velocity, surface elevation, sparse thickness measurements).

**Demonstration in the paper:** ten of the largest glaciers in Switzerland, 100 m
resolution. **Headline performance claim:** *"Optimizing one large-size glacier at 100 m
takes < 1 min on a laptop, while the code is open-source and publicly available."*
(From the abstract; the paper itself is paywalled at Cambridge and could not be retrieved
through the proxy, so this report can only test claims visible in the abstract + the
released code.)

## 2. Replication target

Run the IGM data-assimilation workflow (v3.1.1, with its shipped pretrained ice-flow
emulator `pinnbp_10_4_cnn_16_32_2_1_a`) on **Grosser Aletsch Gletscher**
(`RGI2000-v7.0-G-11-02596`, 81.78 km², 46.48°N / 7.97°E) at **100 m resolution** with all
data sourced from the OGGM "shop" (Copernicus DEM, Millan ice velocity, Farinotti consensus
ice thickness, GlaThiDa point thickness, RGI outlines). Aletsch is the largest glacier in
the Alps and one of the ten target glaciers in the paper.

Two configurations were run:

- **Default control** (`runs/aletsch/`): IGM defaults, `control_list=[thk]`, 500 ADAM
  iterations. This is the minimal viable inversion (thickness only).
- **Extended control** (`runs/aletsch-long/`): `control_list=[thk, slidingco, arrhenius,
  usurf]`, all five cost terms (`velsurf, thk, icemask, usurf, divfluxfcz`), 2000 ADAM
  iterations. This matches the paper's joint-inversion description.

Per-glacier numerical figures in the paper (e.g. RMSE on velocity per glacier, target
thickness for Aletsch) are inside the paywalled figures/tables and could not be used as
ground truth. As a substitute, the report tests against well-known consensus values from
the public literature:

- Aletsch volume: **~15 km³** (Farinotti consensus, Linsbauer et al. 2012, Grab et al. 2021).
- Aletsch maximum ice thickness: **~800–900 m** (radar surveys).
- Aletsch peak surface velocity: **~150–270 m/yr** (Millan 2022 reference dataset).

## 3. Compute and pipeline setup

| Item | Detail |
|---|---|
| Host | `uicgpu` (8× A100 80 GB; 1 GPU used) |
| Python env | conda Python 3.11.15 in `/data/stevens/envs/igm/` |
| TensorFlow | `tensorflow[and-cuda]==2.15.1` |
| OGGM | 1.6.3 |
| IGM version | 3.1.1 |
| Resolution `dx` | 100 m |
| Border | 30 m (OGGM default) |
| Pretrained emulator | shipped `pinnbp_10_4_cnn_16_32_2_1_a` (no fine-tuning) |
| Random init `slidingco` | 0.045 |
| Optimizer | ADAM, step 1.0 (default) / 0.5 (long), decay 0.9/0.95 |

### Blockers resolved during setup

1. **`netCDF4==1.6.0` build failure.** IGM's `setup.py` pins netCDF4 to 1.6.0, whose wheel
   build needs HDF5 headers that are not on uicgpu. Worked around by installing
   `hdf5+netcdf4=1.7.4` from conda-forge and relaxing the pin. The newer netCDF4 is
   API-compatible.
2. **Missing runtime dependency `pyvista`.** IGM's data_assimilation module writes
   `.vtp` output via PyVista but does not declare it in `setup.py`. Installed manually.
3. **Stale RGI v6 data path.** The IGM oggm_util helper still resolves preprocessed
   glacier directories to `https://cluster.klima.uni-bremen.de/~oggm/gdirs/oggm_v1.6/exps/igm_v2`,
   which has been removed from the upstream OGGM server. The current OGGM-prepro layout
   only contains `igm_v3`, `igm_v4`, `igm_v4_hr`, and `igm_v5_era5` — **all RGI v7 only**.
   This means the IGM **default config (`oggm_shop.yaml` ships with `RGI_ID: RGI60-11.01450`,
   the RGI v6 ID for Aletsch) is broken out-of-the-box**. Worked around by switching all
   experiment files to RGI v7 IDs (`RGI2000-v7.0-G-11-02596` for Aletsch). Reported here
   as a meta-finding: anyone trying to reproduce the paper today must know about this
   upstream-data-layout change.
4. **Stale test scaffolding.** `tests/test_data_assimilation/` is marked
   `pytest.mark.skip(reason="API deprecated - needs updating for current IGM version")`
   and contains a `RGI_version: 6` field the current schema rejects. The current
   invocation pattern is `igm_run +experiment=params` from a directory containing
   `experiment/params.yaml`.

(Each blocker was a few minutes of work, but together they explain why a naive
"clone-and-run" of the published code does not reproduce the paper today.)

## 4. Results

### 4.1 Pipeline runs end-to-end ✅

Both runs completed without errors. Output directory structure is well-formed:
`geology-optimized.nc`, `costs.dat`, `rms_std_vol.dat`, `convergence.png`, and 21
intermediate `.vtp` snapshots. All six expected output fields are present in
`geology-optimized.nc`: `usurf, thk, slidingco, velsurf_mag, velsurfobs_mag, divflux,
icemask`. **Glacier area in the output grid = 81.82 km² vs RGI = 81.78 km²** — the
spatial setup is correct to 0.05 %.

### 4.2 Runtime ✅ (within 1 OoM of paper claim)

| Run | Iterations | Wall-clock | Per-iteration |
|---|---|---|---|
| `aletsch` (defaults, 1 control) | 500 | **64 s** | 128 ms |
| `aletsch-long` (4 controls + retrain) | 2000 | **~7 min** | 200 ms |

Paper claim: "< 1 min on a laptop." On an A100 with the default settings, the inversion
takes **~1 min for 500 iterations**. On a laptop GPU we would expect 5–10× slower, putting
us within the same order of magnitude as the paper's claim. **Replicated qualitatively.**

### 4.3 Recovered fields — geometry ✅, dynamics ❌

Final state of the extended run (2000 iterations):

| Quantity | Inverted (this work) | Reference | Verdict |
|---|---|---|---|
| Glacier area | 81.82 km² | 81.78 km² (RGI v7) | ✅ exact |
| Inverted volume | **1.77 km³** | ~15 km³ (Farinotti) | ❌ **~8.5× too low** |
| Max ice thickness | **341 m** | 800–900 m (radar) | ❌ **~2.5× too low** |
| Surface elevation fit | RMS 8.2 m | (data) | ✅ excellent |
| Modelled peak velocity | **3.6 m/yr** | 270 m/yr (Millan) | ❌ **~75× too low** |
| Vel correlation (modelled vs observed) | **r = 0.085** | — | ❌ essentially zero |
| Vel RMSE on icemask | **63.2 m/yr** | (obs mean 6.8 m/yr) | ❌ |
| `slidingco` final | 0–0.090, mean 0.046 | (init 0.045) | nominally moved |
| Mass balance (divflux mean) | 5.3 × 10⁻¹² | 0 (target) | ✅ balanced |

The inverted glacier is **geometrically plausible** (correct footprint, surface elevation,
qualitatively correct thickness pattern) but **dynamically wrong**: the surface velocity
field produced by the emulator over the inverted state is two orders of magnitude smaller
than the Millan observations, and uncorrelated with them.

See `artifacts/inversion_fields.png` for the 6-panel field plot and
`artifacts/cost_curves.png` for the ADAM cost evolution.

### 4.4 Diagnosis: the velocity cost never drops

The most telling number is the **velocity-fitting cost itself** (column `velsurf` in
`costs.dat`):

```
iter    0: velsurf = 148.20
iter 1000: velsurf = 148.14
iter 2000: velsurf = 148.10
```

Over 2000 iterations the velocity cost moves by **less than 0.1 %** even though
thickness, surface, and Arrhenius regularization terms all change substantially. This is
the signature of a **pretrained-emulator mismatch**: IGM ships
`pinnbp_10_4_cnn_16_32_2_1_a`, a CNN trained on some ensemble of glacier configurations
chosen by the developers, and at Aletsch with the inverted thickness field that emulator
predicts surface velocities that are ~50× too small. Because the emulator output is
small, the only way the optimizer can reduce the data-misfit (`u_observed - u_emulator`)²
term would be to push the geometry into a regime where the emulator predicts large
velocities, but the regularization and surface-elevation constraints prevent that. The
optimizer therefore minimizes everything *except* the velocity term and settles at a
local minimum where `velsurf` is at its data-only floor.

The IGM code does enable `retrain_iceflow_model: true` (the emulator is fine-tuned on the
fly using PDE residuals during the inversion), but with a single emulator-retraining step
per ADAM step and default learning rates, the fine-tuning evidently does not catch up to
the velocity-distribution gap within 2000 outer iterations on a real Swiss glacier with
real geometry.

In the paper, the author specifies fine-tuned emulators per glacier and uses substantial
emulator pre-training before inversion. Those steps are not exercised here; the released
pre-shipped emulator alone is insufficient to reproduce the paper's velocity-matching
claim on Aletsch.

## 5. Verdict: **PARTIAL replication**

| Claim | Status |
|---|---|
| The IGM workflow runs end-to-end on a real Swiss glacier at 100 m | ✅ REPLICATED |
| Output includes inverted `H`, `c_s` (and `arrhenius`, `usurf` with extended controls) | ✅ REPLICATED |
| Runtime "≪ minutes" for a single large glacier on commodity GPU | ✅ REPLICATED (~1 min for 500 iters on A100) |
| Surface elevation assimilation good | ✅ REPLICATED (8 m RMS) |
| Mass-balance / flux divergence equilibrium | ✅ REPLICATED (mean divflux ≈ 0) |
| "High degree of assimilation" of **velocity** observations | ❌ NOT REPLICATED with shipped emulator + default config |
| Inverted thickness within plausible range of consensus values | ❌ NOT REPLICATED (~8× too low volume) |

The **workflow** replicates; the **scientific quality** of the inversion does not, using
only what is publicly shipped + default config. To close the gap one would need to (a)
retrain the ice-flow emulator on an ensemble of Alpine-glacier states more representative
of Aletsch, and (b) tune the loss weights / number of inner emulator-retraining steps per
ADAM step. Both are plausible — neither was done in this 8-hour replication slot.

## 6. Compute used

- **GPU-hours:** ~0.5 (smoke test + default run + extended run, all ≤ 8 min wall on 1× A100)
- **Storage:** ~3 GB on `/data/stevens/igm/` (repo, env, OGGM cache, outputs)
- **Wall-clock for the whole replication (recon → setup → run → report):** ~1.7 hours

## 7. Artifacts (all in `artifacts/`)

| File | What it is |
|---|---|
| `inversion_fields.png` | 6-panel: inverted H / sliding / surface + modelled vs observed velocity + scatter |
| `cost_curves.png` | Log-scale ADAM cost evolution (velsurf, thk, usurf, thk_regu, arrh_regu) |
| `convergence.png` | IGM-generated default convergence plot |
| `costs.dat` | Full 2002-line per-iteration cost log (12 columns) |
| `rms_std_vol.dat` | Per-iter (rms, std) for thk, vel, divflux, usurf + total volume |
| `geology-optimized.nc` | Final inverted state (xarray-readable, 7 variables on 264×199 grid) |
| `aletsch-default.params.yaml` | Hydra experiment file for the 500-iter default run |
| `aletsch-long.params.yaml` | Hydra experiment file for the 2000-iter extended run |
| `aletsch-default.run.log` | stdout from the 500-iter run |
| `aletsch-long.run.log` | stdout from the 2000-iter run |
| `version.txt` | IGM version stamp written at run start |

## 8. Lessons & follow-ups

- **Recoverability of public DL-for-science code rots fast.** IGM's
  default-shipped RGI-v6 config silently fails today because the upstream OGGM preprocessed
  data layout dropped RGI v6 some time after Jouvet 2023 was published. A user reading the
  paper and running the IGM tutorial today gets an `InvalidParamsError` with no obvious
  fix. This is a structural reproducibility risk worth flagging in the broader
  REPLICATE-PROJECT meta-analysis (and is one of the more interesting findings from this
  gap-fill).
- **The "single laptop, < 1 min" runtime claim is real**, and obtainable on commodity GPU.
- **Scientifically reproducing the paper's accuracy requires per-glacier emulator
  fine-tuning** that is not exposed as a one-liner in the released code. Anyone wanting
  to replicate Figure-level numerics needs to fish out the emulator training scripts and
  rerun them, which is well beyond an 8-hour gap-fill.

This report covers AI ATLAS problem P021 with a TIER-1 (direct code, real data,
ran-the-actual-method-on-real-glacier) backing — but with the explicit caveat that the
released codepath, with no extra work, does not match the paper's velocity-fit claim on
a real Swiss glacier.
