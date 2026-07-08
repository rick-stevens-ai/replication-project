# PAPER_NOTES.md — Rasp, Pritchard & Gentine 2018 PNAS

**Slot:** F-RETRY · **Started:** 2026-05-27 16:13 CDT · **Agent:** Ollie (argo/argo:claude-opus-4.7)

## Bibliographic

- **Title:** Deep learning to represent sub-grid processes in climate models
- **Authors:** Stephan Rasp¹, Michael S. Pritchard², Pierre Gentine³
- **Venue:** PNAS, Sep 2018, vol. 115 no. 39, pp. 9684–9689
- **DOI:** [10.1073/pnas.1810286115](https://doi.org/10.1073/pnas.1810286115)
- **arXiv:** [1806.04731v3](https://arxiv.org/abs/1806.04731) (PDF cached at `rasp_2018_arxiv.pdf` in this dir)
- **Affiliations:** ¹ LMU Munich, ² UC Irvine, ³ Columbia

## Code (paper-exact)

- **Repo:** `https://github.com/raspstephan/CBRAIN-CAM`
- **Frozen release for PNAS:** [`PNAS_final` tag](https://github.com/raspstephan/CBRAIN-CAM/releases/tag/PNAS_final) — Zenodo DOI [10.5281/zenodo.1402384](https://doi.org/10.5281/zenodo.1402384)
- **Climate-model side (Fortran, modified SPCAM):** `https://gitlab.com/mspritch/spcam3.0-neural-net` (training-data branch: `fluxbypass`; NN-deploy branch: `revision`). **Out of scope for offline replication** — we only need the offline NN training/eval, not the prognostic GCM coupling.
- **Top-level python modules of interest:**
  - `cbrain/` — preprocessing, NN building, analysis
  - `nn_config/` — Keras config files for `run_experiment.py`
  - `notebooks/presentation/` — paper figures
  - `save_weights.py` — exports trained weights to text for Fortran ingestion

## Data — VERIFIED AVAILABLE (Zenodo, public, no auth)

DOI: **[10.5281/zenodo.2559313](https://doi.org/10.5281/zenodo.2559313)** ("Sample SPCAM dataset", Rasp 2019)

Five files, total ~4 GB:

| file | size | role |
|---|---|---|
| `sample_SPCAM_1.nc` | 923 MB | raw SPCAM model output (subset 1) |
| `sample_SPCAM_2.nc` | 923 MB | raw SPCAM model output (subset 2) |
| `sample_SPCAM_concat.nc` | 1.85 GB | concat of 1+2 — *don't need if you have 1 & 2* |
| **`preproc_features.nc`** | **205 MB** | **NN-ready inputs (X)** ← primary for our work |
| **`preproc_targets.nc`** | **205 MB** | **NN-ready targets (y)** ← primary for our work |

Direct download URL pattern:
`https://zenodo.org/api/records/2559313/files/<filename>/content`

**Download verified 2026-05-27 16:14 CDT on uicgpu** — pulled `preproc_features.nc` (196 MB) in ~6 s. cherryrd is rate-limited by Zenodo (403); all downloads must go through uicgpu (proxy via `source ~/env.sh`).

**Caveat:** this Zenodo deposit is a *sample* (a few days of SPCAM, not the full 1-year ≈140 M-sample training set used in the paper). The full training set was hosted on UCI cluster and is not publicly archived. **Implication for replication:** we can demonstrate the offline training pipeline end-to-end and reproduce the *qualitative* offline-skill profile and the *methodology*, but absolute R² values will be lower than the paper's because of the ~100× smaller training set. This is the standard situation for this paper (cited as such in the Beucler 2019/2020 follow-ups).

## Model setup (from §"Model and neural network setup", arXiv v3)

### Architecture — "control" network
- **9 hidden layers** (fully-connected)
- **256 nodes / layer**
- Activation: ReLU (standard in CBRAIN; not stated explicitly in the body, confirmed in repo `nn_config/`)
- **~500 K trainable parameters**
- Output layer: linear, dim 65
- **Loss:** mean-squared error between predicted ŷ and target y
- Optimizer: Adam (CBRAIN default; not in main text)
- Reasoning for depth: "deeper, larger networks achieve lower training losses; deep networks proved more stable in the prognostic simulations" (vs shallow networks of earlier work — Brenowitz/Bretherton 2018, Gentine et al. 2018)

### Inputs `x`, dim = 94
Stacked vector `x = [T(z), Q(z), V(z), Ps, Sin, H, E]`:
- `T(z)` — temperature, 30 vertical levels
- `Q(z)` — specific humidity, 30 levels
- `V(z)` — meridional wind, 30 levels (zonal wind omitted; aquaplanet is zonally symmetric)
- `Ps` — surface pressure, scalar
- `Sin` — incoming solar radiation, scalar
- `H` — sensible heat flux, scalar
- `E` — latent heat flux, scalar
- Total: 3×30 + 4 = **94** ✓

### Outputs `y`, dim = 65
Stacked vector `y = [ΔT_phy(z), ΔQ_phy(z), F_rad, P]`:
- `ΔT_phy(z)` — sub-grid heating tendency (CRM + radiative), 30 levels
- `ΔQ_phy(z)` — sub-grid moistening tendency, 30 levels
- `F_rad` — net radiative fluxes (TOA + surface), 4 scalars (LW/SW × TOA/SFC)
- `P` — surface precipitation, scalar
- Total: 30 + 30 + 4 + 1 = **65** ✓

### Normalization
"inputs and outputs are stacked to vectors … and normalized to have similar orders of magnitude (Supplemental Methods)". Standard CBRAIN normalization (per-variable scaling — see `cbrain/data_generator.py`).

## Training data (paper-default — NOT what's on Zenodo)
- **Source:** SPCAM v3.0 (super-parameterized CAM) in aquaplanet setup, zonally-invariant fixed SSTs, full diurnal cycle, no seasonal variation
- **GCM grid:** ~2° horizontal, 30 vertical levels, 30-min time step
- **Embedded CRM:** 8 columns × 4 km wide, 20-s time step
- **Training period:** 1 year of SPCAM output
- **Sample count:** ~140 million (every grid column × every time step)
- **Train/val/test split:** not explicitly given in body text — Supplemental Methods specifies; CBRAIN default is shuffle + 90/10 train/val with a held-out simulation period as test

## Headline offline metric
The paper's main results are climate-statistic comparisons of the *prognostic* NNCAM run (mean state, precip distribution, wave spectrum) — NOT offline R². For the offline metric we need to look at **Fig. S1** (architecture sweep, plots training loss vs depth/width) and cross-reference the 2018 Gentine et al. GRL companion paper which reports R² ~ 0.7 for ΔT_phy averaged over the tropics with similar networks. **Final replication target metric:** vertical profile of offline R²(ΔT_phy) vs paper's Fig. S1 / Gentine 2018 GRL Fig. 2 — even on the small Zenodo sample we should see boundary-layer R² < tropospheric R², and we should be able to demonstrate the depth-vs-loss monotone improvement they cite.

## Software stack
- Keras + TensorFlow backend (CBRAIN code is `from keras.models import Model` throughout). Paper era ≈ TF 1.x / Keras 2.1.
- **Modern port:** we will use PyTorch with the same architecture (9 × 256 dense + ReLU, MSE, Adam) — equivalent and the paper makes no Keras-specific choices. Document this substitution as friction tag F2 (toolchain modernization).

## Replication plan
1. **Phase 1 ✓ done:** paper recon, data verified.
2. **Phase 2:** uicgpu workspace, clone CBRAIN-CAM @ PNAS_final, fetch Zenodo `preproc_*.nc`, write minimal PyTorch trainer reading the same nc files.
3. **Phase 3:** train control 9×256 net; also train a "small" 4×128 net as paper's sensitivity sweep proxy. Save loss curves + checkpoints.
4. **Phase 4:** evaluate vertical R² profile on held-out time slice; compare to paper Fig. S1 / Gentine 2018 GRL Fig. 2; verdict + REPORT.md + PDF.

## Notes / friction so far
- **F5+F9 averted:** Zenodo data exists and downloads fine *from uicgpu*. From cherryrd Zenodo issues HTTP 403 ("unusual traffic from your network"). Lesson logged for future cherryrd→Zenodo work.
- **F2 anticipated:** TF1/Keras2.1 era code will not run cleanly on modern CUDA/Python; will document a PyTorch port rather than wrestle with the original Keras config.
- PNAS PDF itself is Cloudflare-blocked from my IP; arXiv v3 used in its place (content identical except for typesetting + supplement, which is paywalled at PNAS but methods detail is mostly in the body).
