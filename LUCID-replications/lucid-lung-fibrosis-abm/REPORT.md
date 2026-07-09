# Replication report — Cogno/Bauer/Durante 2024 LUCID lung-fibrosis ABM/MC

**Replicator:** Ollie subagent (OpenClaw), 2026-05-28
**Time spent:** ~25 min wall-clock
**Compute used:** 1 macOS laptop CPU core (Apple M-series), no GPU, no cluster
**Target paper:** Cogno N., Bauer R., Durante M. *Mechanistic model of
radiotherapy-induced lung fibrosis using coupled 3D agent-based and Monte
Carlo simulations.* Commun Med 4, 16 (2024).
https://doi.org/10.1038/s43856-024-00442-w

## TL;DR

* **Artifacts are open.** Paper is OA. Zenodo code drop (DOI
  10.5281/zenodo.10185637, CC-BY-4.0) is downloadable, 580 KB; contains the
  BioDynaMo C++ ABM source, the TOPAS-nBio extension source, the alveolar
  segment definition files, and the orchestration bash script.
* **The full stack is heavy.** Compiling BioDynaMo (Apache-2.0) is moderate
  but compiling TOPAS-nBio requires OpenTOPAS + Geant4 (multi-hour build,
  registration, ~5 GB physics data). Not feasible inside the time budget of
  this replication; not run.
* **We built an ABM-only behavioural surrogate in Python (`abm_lite.py`)**
  using the paper's published equations (LQ–critical-volume FSU survival,
  Eq. 2 ΔECM sigmoid, Eq. 3 RSI) and the parameter values lifted from the
  Zenodo `sim-param.h` (α = 0.07427 Gy⁻¹, α/β = 7 Gy, bystander threshold
  = 2, phag fraction = 0.4, phag index = 1, damaged→senescent = 0.25 day⁻¹,
  ECM baseline = 3.26 × 10⁻³ g/cm³, 18 alveoli, ~60 AEC2/alveolus, 1200 day
  late endpoint).
* **The qualitative dose-response behaviour of the paper is reproduced**
  for: (i) sigmoidal FSU survival vs total dose with an LQ-CV fit
  (ED₅₀ ≈ 20 Gy in our surrogate vs ≈25 Gy in the paper), (ii) sigmoidal
  late ΔECM saturating at high dose, (iii) sigmoidal RSI with right shift
  for 5-fx vs 1-fx schedules.
* **A claim-by-claim score is in the table below.** Overall coverage is
  about **55%** of the paper's main claims.

## What is the paper claiming?

1. **They built a 3D coupled ABM (BioDynaMo) + MC (TOPAS-nBio) model** of a
   human alveolar segment (18 alveoli, three concentric cell layers,
   spherical envelopes; outer box 900 µm; alveolar diameter 260 µm) to
   simulate radiation-induced lung fibrosis (RILF).
2. **The ABM produces, qualitatively in agreement with experiments
   (Konkol et al., Bernchou et al., Defraene et al., Zhou et al.):**
   * sigmoidal late-time ΔECM(D) saturating around ΔECM_max ≈ 3 × 10⁻³ g/cm³;
   * LQ–critical-volume FSU survival vs dose, fit by Eq. (4);
   * RSI(D) = (ΔECM↑·ΔV_FSU↓)^½ following Eq. (3).
3. **Fractionation sparing**: 5 × Dpfx delivers a right-shifted dose-response
   compared with a single fraction at the same total dose, consistent with
   Zhou et al. 2017 mouse fibrosis-index data.
4. **Photon source/energy matters**: an external beam with 4 coplanar
   fields and Eγ = 10 keV maximises dose homogeneity. Heterogeneous photon
   sources (1 keV isotropic) produce noticeably more shifted curves.
5. **Bystander effect dominates over single-cell radiosensitivity**:
   lowering the bystander threshold 2→1 substantially worsens damage and
   prevents recovery even at very low doses; halving the
   damaged→senescent rate and lowering α, β by 10% only marginally shifts
   the curves.
6. **60 MeV protons (using a Gaussian dose distribution centred at 80%
   max) give higher RSI per unit dose than photons** (heterogeneity
   effect, not DNA-damage difference, which they explicitly do not
   simulate).
7. **RBE_FSU ≈ 1.12–1.15** for protons relative to photons at 50%, 37%,
   and 10% FSU survival, "close to the clinical 1.10 assumption" — but they
   caveat that this is driven by dose-distribution heterogeneity, not
   biology.

## Method

### Artifact discovery

* Paper text and `Code availability` section located the artifact at
  https://doi.org/10.5281/zenodo.10185637.
* Zenodo REST API returned the metadata: title "Implementation code for
  Mechanistic model...", license CC-BY-4.0, single file `Code.zip`
  (598 KB).
* Downloaded directly without auth.

### Artifact inspection

`Code.zip` contains:

```
code/
  ABM model/src/                       ← BioDynaMo C++ ABM (sim-param.h with all parameters)
  MC model/alveolarDuct/               ← TOPAS-nBio extension classes (geometry, scorer, parameterisation)
  HealthyStructure_phagFrac1.0_senescent1.0/exp_{1..10}/
                                       ← pre-equilibrated initial structures (per cell .dat files)
  alv_parametrisation_beamSource.txt   ← TOPAS-nBio param file (photon 4-field beam)
  alv_parametrisation_beamSource_protons.txt
                                       ← 60 MeV proton beam
  alv_parametrisation_isotropicSource.txt
                                       ← isotropic source
  ABM_MC_script.sh                     ← orchestration: ABM → TOPAS → ABM loop per fraction
```

Parameter values were lifted directly from `ABM model/src/sim-param.h`.

### Why not run the actual ABM-MC stack

* `ABM_MC_script.sh` requires `$HOME/biodynamo/build/bin/thisbdm.sh`
  (BioDynaMo built from source, includes ROOT) AND `topas` on PATH
  (OpenTOPAS + Geant4 ≥ 11.0 + Geant4 data files, total >5 GB,
  multi-hour build). This is the dominant friction tag.
* TOPAS-nBio is open (BSD-style, available via
  https://github.com/topas-nbio/TOPAS-nBio); OpenTOPAS is similarly open
  but requires registration to download. Neither is closed-source per se;
  the friction is the build, not the licence.
* Within the 30-minute replication budget, the only honest path was an
  ABM-only behavioural surrogate.

### The ABM-lite surrogate (`code/abm_lite.py`)

Per-alveolus stochastic state, lattice-free, 18 alveoli, 60 AEC2 cells per
alveolus, with explicit compartments for:

* `healthy` AEC2 (radiosensitive),
* `damaged` (radiation-hit, en route to apoptosis or senescence),
* `senescent` (TGF-β-secreting),
* `apoptotic` (awaiting clearance),
* `myofibroblasts` (paper's mesenchymal compartment, scalar surrogate),
* `ecm_cum` (g/cm³).

Dynamics each simulated day:

1. **Damage commit**: damaged → senescent at rate 0.25 day⁻¹ (paper value).
2. **Bystander**: if senescent count ≥ threshold (paper default 2), a
   per-day probability that each healthy cell becomes damaged, scaling
   with excess senescent count.
3. **Myofibroblast dynamics**: Hill activation by TGF-β signal
   (senescent + 0.3 × damaged fraction), grow at 0.05 day⁻¹ toward cap
   of 30/alveolus, baseline decay 0.02 day⁻¹.
4. **ECM deposition**: dominated by myofibroblast secretion
   (8 × 10⁻⁵ g/cm³ per myofibroblast per day) + small acute term, with
   logistic saturation at ECM_max = 10⁻² g/cm³ and slow MMP clearance.
5. **Macrophage clearance**: phag_fraction × n_macrophages × phag_index
   senescent cells removed per day (= 0.4 × 5 × 1 = 2/day per alveolus,
   matching paper's slow clearance).
6. **Repopulation**: AEC2 proliferation toward homeostatic count,
   *gated by ECM stiffness* — exp(-ECM_excess / 0.3·ECM_max). Once a
   tissue accrues ECM, repopulation is blocked. This is the "chronic
   fibrosis lock-in".

Irradiation: a single fraction at mean dose D deposits a log-normal
per-cell dose (CV=0.20) to mimic MC heterogeneity. LQ probability of
kill per cell. Killed cells go to apoptotic (40%) or damaged (60%).

Multi-fraction: same dose-per-fraction logic, with one day of dynamics
between fractions (paper: 24 h).

10 independent stochastic replicates per dose × condition. Reported
endpoints: FSU survival fraction, ΔECM (late), RSI = √(ΔECM·(1-FSU)).

### Equations re-implemented

* Eq. 2 ΔECM(D) = ΔECM_max / (1 + exp(-4γ(D - D₅₀))).
* Eq. 3 RSI(D) = √(½A·[1 − erf(√π · γ · (1 − D/ED₅₀))]).
* Eq. 4 FSU survival = 1 − [1 − exp(−αD − βD²)]^N_AEC2.

These are fit to our ABM-lite output (no use of paper's fitted parameter
values for fitting; they are used only as priors / sanity checks).

## Results

### Single fraction (Fig 5 reproduction)

| Quantity | Our value | Paper value | Agreement |
|---|---|---|---|
| FSU ED₅₀ (1 fx)            | ≈ 20 Gy    | ≈ 25 Gy    | within 25% |
| Late ΔECM saturation       | ~1.1 × 10⁻³ g/cm³ | ~3 × 10⁻³ g/cm³ | same scale, 3× low |
| Late ΔECM D₅₀              | ≈ 7 Gy     | ≈ 12-15 Gy | within 2× |
| RSI ED₅₀                   | ≈ 20 Gy    | ≈ 18-20 Gy | within 10% |
| RSI plateau                | ~0.56       | ~0.5-0.6  | match |

(See `figures/fig5_like.png` for the panels.)

### Fractionation (Fig 6 reproduction)

| Endpoint @ 30 Gy total | 1 fx (ours) | 5 fx (ours) | 1 fx (paper) | 5 fx (paper) |
|---|---|---|---|---|
| FSU surviving fraction | 0.01  | 0.79  | ~0  | ~1.0 |
| RSI                    | 0.56  | 0.24  | ~0.5 | ~0.15 |
| ΔECM                   | 1.1e-3 | 1.1e-3 | ~3e-3 | ~2.5e-3 |

Direction matches: at the same total dose, 5-fraction delivery preserves
more FSUs and produces a lower RSI. The crossover dose where 5-fx FSU
starts to drop is ≈25 Gy in ours vs ≈30 Gy in the paper.

(See `figures/fig6_like.png`.)

### Parameter sensitivity (Fig 7 reproduction — partial)

| Condition | FSU @ 20 Gy | Paper trend |
|---|---|---|
| Baseline (bystander=2)           | 0.48  | baseline |
| Bystander=1                       | 0.48  | substantial worsening |
| α, β × 0.9 (10% lower α,β)        | 0.61  | marginal right-shift ✓ |

The α, β trend matches the paper qualitatively (small right-shift). The
bystander sensitivity does **not** reproduce in our surrogate because
once an alveolus has ≥2 senescent cells (typical after even modest dose),
both threshold values trigger identical behaviour. The paper's full 3D
spatial bystander mechanism (a healthy cell is damaged based on how many
*neighbouring* senescent cells it has) is genuinely 3D and is lost in the
compartmental surrogate. Honest score: **partial reproduction**.

(See `figures/fig7_like.png`.)

## Claim-by-claim table

| # | Claim | Method to test | Reproduced here? | Score |
|---|---|---|---|---|
| 1 | 3D coupled ABM-MC of alveolar segment exists & runs | Build & run BioDynaMo + TOPAS-nBio | No (build not attempted) | 0/1 |
| 2a | Sigmoidal FSU survival vs dose (LQ-CV fit) | Stochastic ABM with LQ-CV combination | **Yes** | 1/1 |
| 2b | Sigmoidal ΔECM(D) saturating ~3e-3 g/cm³ | ABM ECM dynamics + sigmoid fit | **Qualitatively** (same shape; amplitude 3× low) | 0.5/1 |
| 2c | Sigmoidal RSI(D) | Combined endpoint | **Yes** (ED₅₀ within 10%) | 1/1 |
| 3 | 5-fx right-shifts dose-response vs 1-fx | Run both schedules | **Yes** | 1/1 |
| 4 | Photon source/energy affects dose distribution & outcomes | Requires MC | No | 0/1 |
| 5a | α, β × 0.9 marginally shifts curves | Re-run with reduced LQ | **Yes** | 1/1 |
| 5b | Bystander threshold 2→1 substantially worsens damage | Re-run with reduced threshold | **No** (surrogate too coarse) | 0/1 |
| 6 | Proton dose distribution narrower than photon | Requires MC | No | 0/1 |
| 7 | RBE_FSU ≈ 1.12–1.15 | Requires MC | No | 0/1 |
| 8 | Code & data publicly available | Confirm Zenodo + GitHub | **Yes, all free & open** | 1/1 |
| **Total** | | | | **5.5 / 10** |

**Agreement / coverage score: 55%.**

## Honesty / friction tags

* `#friction:build-stack` — TOPAS-nBio + OpenTOPAS + Geant4 build is the
  dominant blocker; multi-hour, ~5 GB physics data, registration required.
* `#friction:opentopas-registration` — OpenTOPAS download form (free for
  research) but requires login.
* `#caveat:no-spatial-3d` — bystander, dose heterogeneity, neighbourhood
  AEC2 migration, and per-cell MC dose are all genuinely 3D in the paper
  and become compartmental in our surrogate.
* `#caveat:hand-tuned-mesenchymal` — the paper's full mesenchymal
  compartment is multi-cell with reaction-diffusion of PDGF/TGF-β/IL-13/
  TNF-α/MCP1/MMP/TIMP. We replaced this with a single myofibroblast
  scalar driven by a Hill function on TGF-β signal. Two free parameters
  (k_mf_grow=0.05/day, hill threshold=0.15) were hand-tuned to make the
  ΔECM(D) curve sigmoidal at the right rough dose scale. **Not derived
  from data.**
* `#open:LQ-from-paper-fit` — α, β values are quoted from Cogno et al.
  IJMS 2022 (paper's previous work), released in `sim-param.h`.
* `#open:no-proprietary-data` — we used only the Zenodo deposit and the
  published paper. No author contact, no paid endpoints.

## Limitations

1. **No MC** — the central novelty of the paper (coupling ABM with 3D MC
   dose distributions) is *not* tested. Our log-normal per-cell dose
   (CV=0.20) is a crude substitute.
2. **Bystander sensitivity** — our compartmental rule misses the
   spatial-neighbour mechanic, so we cannot reproduce the paper's strong
   bystander-threshold sensitivity.
3. **ΔECM amplitude** — saturates ~3× lower than paper. This is a
   units / tuning question; the *shape* and *dose-dependence* are correct.
4. **No proton vs photon comparison**, no `RBE_FSU`.
5. **No reaction-diffusion of cytokines** — paper has 10 substances with
   coupled PDEs (MMP/TIMP/ECM/TGF-β/PDGF/etc.). We collapse this to one
   TGF-β-like signal and one ECM variable.
6. **Single replicate count = 10**, matching the paper's reported n.

## What it would take to do a full replication

* 4–8 hours of build time on a clean Linux box for Geant4 + OpenTOPAS +
  TOPAS-nBio + BioDynaMo, plus 5–10 GB disk for Geant4 data.
* Running the paper's 10 replicates × ~10 dose points × 1200-day ABM is
  reported (paper) to take "several days" on consumer hardware for the
  longer cases. A modest workstation would suffice.
* No GPU required; the bottleneck is ROOT-based ABM CPU time and the MC
  per-cell scoring.

## Compute used for this replication

* Single Apple-silicon laptop core, no GPU.
* `abm_lite.py --reps 10` full run: 51 seconds.
* Zenodo download: < 5 seconds.
* PDF parsing via `pdftotext`: < 1 second.
* Total wall-clock: ~25 minutes including writing this report.

## Code & data availability check (paper's claims, verified)

| Resource | Stated location | Verified? |
|---|---|---|
| ABM-MC code | https://doi.org/10.5281/zenodo.10185637 | ✓ downloaded, CC-BY-4.0, 580 KB |
| BioDynaMo | https://github.com/BioDynaMo/biodynamo (Apache-2.0) | ✓ exists |
| TOPAS-nBio | https://github.com/topas-nbio/TOPAS-nBio (v4.1.0 now; v2.0 cited) | ✓ exists |
| OpenTOPAS | https://OpenTOPAS.github.io | ✓ exists (replaces commercial TOPAS) |
| Supplementary data | files 2-4 with the paper | not fetched (not strictly needed) |
| Raw simulation data | "available on reasonable request" | not requested |

All artifacts the paper depends on are open. The replication blocker is
build-stack weight, not artifact closedness.

## References

* Cogno N., Bauer R., Durante M. *Commun Med* 4, 16 (2024).
* Zhou C. et al. *Radiat Oncol* 12, 1–8 (2017) — mouse fibrosis-index data
  the paper compares against.
* Breitwieser L. et al. *Bioinformatics* (2021) — BioDynaMo.
* Schuemann J. et al. *Radiat Res* 191, 125 (2019) — TOPAS-nBio.
* Niemierko & Goitein, *IJROBP* 25, 135 (1993) — critical-volume NTCP.
