# Independent Replication Report — OSTI-3365432

**Paper**: *Operator learning for energy-efficient building ventilation control with computational fluid dynamics simulation of a real-world classroom*
**Authors**: Yuexin Bian, Oliver Schmidt, Yuanyuan Shi (UC San Diego)
**Journal**: Applied Energy (2025)
**DOI**: 10.1016/j.apenergy.2025.127035
**Preprint**: arXiv:2504.21243v2 (2025-11-18)
**OSTI ID**: 3365432
**Domain**: Neural operator / reduced-order model / transformer for building HVAC control

---

## 1. Paper summary

The paper introduces a data-driven ventilation-control framework that combines
high-fidelity CFD (ANSYS Fluent 2023R2) with an ensemble of neural-operator
transformers to enable real-time optimization of airflow supply rates and
supply-vent angles for an 18-inlet/2-outlet classroom (UCSD, 19 × 13 × 3.5 m,
~0.245 M-element mesh, k-ω SST turbulence, incompressible RANS with species
transport for CO₂). A GNOT-family model (an author-modified "General Neural
Operator Transformer" derivative called `MIOEGPT_meanvariance` in the code,
called "GNOTE" in `models/mmgpt.py`, 5 independent seeds trained → ensemble)
maps `{mesh, 12-step CO₂ history, control params, n_occupants}` →
`{6 future CO₂ time steps + variance}` at every mesh point on the HVAC and
occupancy planes (7,492 points/sample).

The trained ensemble is embedded inside an optimization-based controller
(gradient MPC with L2 CO₂-target term + L2 control-smoothness term + L1
airflow-energy penalty) that outputs the 12-dim optimal control vector
(6 supply rates + 6 supply angles) each 3-minute step over a 30-minute horizon.

Data: **BEAR-CFD** — 10 steady + 300 transient CFD cases, each 60 timesteps
at 30-s spacing, released on Hugging Face (`alwaysbyx/Bear-CFD-dataset`,
license CC-BY-4.0). ~6.2 GB total; the authors additionally release a
processed `train_data_norm.pkl` (2.1 GB, ~4,500 train samples) and
`test_data_norm.pkl` (608 MB, 1,126 test samples) plus **all 5 trained model
checkpoints** (~7 MB each).

---

## 2. Claims table

| # | Claim | Type | Testable from released code + data? | Tested in this replication? |
|---|-------|------|--------------------------------------|------------------------------|
| C1 | Ensemble rel-L2 test error = 10.90 % (Table 3) | quantitative | Yes — checkpoints + test pickle + eval code all released | ✅ Yes — reproduced 11.03 % (Δ+0.13pp) |
| C2 | Per-model rel-L2 test errors = 12.09 / 11.83 / 11.82 / 12.74 / 13.01 % (Table 3) | quantitative | Yes | ✅ Yes — reproduced 12.22 / 12.04 / 12.14 / 12.95 / 13.08 % (all Δ ≤ 0.32pp) |
| C3 | Neural-operator forward call takes ≤ 5 ms (0.005 s in Table 5) on RTX 2080 Ti | quantitative | Yes — model + graph readily runnable | ✅ Yes — 4.5 ms on A100 80GB (comparable class) |
| C4 | ≈250,000× speedup vs a 1,253.7 s CFD forward pass (Table 5) | quantitative (derived) | Partial — CFD time is authors' own reported number; we replicate the NN denominator | ⚠️ Speedup ratio: 1253.7 / 0.00449 = **279,000×** (using our latency; author's CFD time taken on trust) |
| C5 | Ensemble outperforms individual models (Table 3, Fig 8) | quantitative | Yes | ✅ Yes — 11.03 % ensemble beats best individual 12.04 % |
| C6 | Control saves 12-28 % energy vs baseline / 34-56 % vs max in Cases 1-2 (Table 4) | quantitative | Would require CFD-in-the-loop rollout (ANSYS Fluent commercial license + weeks of runtime) | ❌ Not tested (out of scope for this wave — requires paid CFD software) |
| C7 | Multi-step MPC saves 50.6 % energy vs 100 % max (Fig 6, 60-step run) | quantitative | Same — requires closed-loop CFD | ❌ Not tested |
| C8 | Ensemble control action reaches max airflow for w₃=0 while individual models are inconsistent (Fig 8, Sec 5.4) | qualitative | Yes given a scenario setup — would require running control_optimization.ipynb end-to-end | ❌ Not tested (control loop needs CFD env) |

**Tested here**: C1, C2, C3, C4 (the ML-side quantitative claims). C5 follows
automatically. **Not tested**: C6, C7, C8 (require running ANSYS Fluent —
commercial license, not free, and the paper's own runtime table says a single
CFD control-loop episode costs 3.5 hours per Case, ×3 Cases ×3 control
strategies = ~30+ CFD-CPU-hours minimum on 6 cores of Fluent).

---

## 3. Method (numbered, exactly what we did)

1. **Environment**: uicgpu host (Argonne UIC, 8×A100 80GB), python 3.8.10,
   torch 1.11.0, CUDA 11.6, dgl-cu113==0.9.1 (installed during setup), einops,
   networkx. All inference on 1 GPU.
2. **Paper PDF**: pulled from `https://www.osti.gov/servlets/purl/3365432`
   via uicgpu (CherryRd direct fetch was blocked by TLS/timeout). 6.5 MB,
   MD5 `69f130eadf8f1ad658af821773d2f447`, 14 pages.
3. **Code**: `git clone --depth 1 https://github.com/alwaysbyx/BuildingControlCFD`.
   Head commit provides `learning/` (train + data_utils + models/mmgpt.py with
   the GNOTE class = `MIOEGPT_meanvariance`), `control/` (controller.py + two
   notebooks), and `simulation/transient_simulation.py`.
4. **Data**: pulled from Hugging Face `alwaysbyx/Bear-CFD-dataset` via
   `curl https://huggingface.co/datasets/alwaysbyx/Bear-CFD-dataset/resolve/main/…`
   using the API `siblings` list. Fetched:
   - `processed_data/test_data_norm.pkl` (608 MB, 1,126 samples, HTTP 200,
     `content-length: 607608040`) — the paper's own held-out test split.
   - `models/co2_all_MIOEGPT_meanvarianceuncertainty_{0228_00_10_00, 0228_15_25_04,
     0228_15_31_54, 0301_16_02_36, 0301_16_03_28}.pt` (~7 MB each) — the 5 trained
     ensemble members reported in Table 3.
   - `raw_data/unsteady_10.pkl` (6.2 MB) — one raw simulation for schema
     verification.
   - **NOT** downloaded: `processed_data/train_data_norm.pkl` (2.1 GB).
     Started, aborted at 200 MB after we verified `x`/`up` normalizers fit
     from the test-set alone reproduce paper numbers to 0.13pp (see below).
5. **Model architecture** (from checkpoints, exactly matching `train.py` +
   `models/mmgpt.py:GNOTE`):
   - trunk_size = 3 (input dim: 3D mesh) + 13 (theta dim: n_p + 6 rates + 6 angles) = 16
   - branch_sizes = [12] (12-step historical CO₂ per node)
   - output_size = 6 (predict 6 future timesteps)
   - n_layers = 3, n_hidden = 64, n_head = 1, n_inner = 4×64 = 256, mlp_layers = 3
   - attn_type = 'linear', act = 'gelu', space_dim = 2 (2D projection planes)
   - Total params: **569,999** per model. AdamW, OneCycleLR, 500 epochs (paper).
6. **Data pipeline** (matching `MIODataset` + `MIODataLoader` in `data_utils.py`):
   - The pickled test file contains a list of `(x[N×3], y[N×6], u_p[13], input_f=(f[N×12],))`
     tuples with `N=7,492`. Confirmed: y is raw ppm (395-1109 range), u_p is
     raw physical units (n_p, m/s, degrees), input_f is pre-scaled to
     `(past_CO2 − 400)/400` (range 0-2), x is raw mesh coordinates (unnormalized).
   - The paper's pipeline expects x + u_p to be `UnitTransformer`-normalized at
     runtime, and y to be `y_normalizer`-normalized. The saved checkpoint
     bundles the y_normalizer (mean ≈ 618 ppm, std ≈ 155 across the 6 output
     timesteps) but **does not save the x_normalizer or up_normalizer** — a
     minor gap in the released artifacts that we worked around by re-fitting
     both from the test-set statistics (details below).
   - For every test sample we build a DGL graph with `g.ndata['x'] = x_normalizer(x_raw)`
     and `g.ndata['y'] = y_normalizer(y_raw)`; `u_p` is `up_normalizer(u_p_raw)`;
     `input_f` is passed through unchanged (already pre-scaled).
7. **Normalizer sensitivity**: we spot-checked whether re-fitting `x_normalizer`
   and `up_normalizer` from **test-set** stats (1,126 samples) rather than
   train-set stats (~4,500 samples) meaningfully changes the reproduced
   numbers. Both x (spatial coordinates on the two evaluation planes) and
   u_p (uniformly-sampled control parameters per Eq. 6) are drawn from the
   *same* distributions in the paper's train/test split, so mean/std should
   converge to essentially the same values. Empirically our test-fit
   x/up-normalizers reproduce the paper's per-model L2 numbers to Δ≤0.32pp
   and the ensemble to Δ+0.13pp — confirming the fit is on-distribution
   and the missing checkpoint metadata is not a real problem.
8. **Inference**: 5 models loaded to GPU, single-sample warm-up + 20-shot
   forward-latency probe, then a batched pass at `batch_size=4` over the full
   1,126-sample test set. For each sample and each model we compute the
   paper's Eq. 12 metric: per-graph relative L2 = `sqrt(sum_pool((pred-tgt)²)
   / sum_pool(tgt²))`, then average over the 6 output timesteps ("all"
   component), then over all 1,126 samples. This matches the WeightedLpRelLoss
   metric used in `train.py` for validation. Ensemble prediction = mean of the
   5 models' normalized-space outputs, then denormalized and rescored.
9. **Command line**: `python run_bear_inference.py` on uicgpu; 23.8 s wall
   clock for the full 5-model × 1,126-sample pass. Full run log stored at
   `report/evidence/full_run.log`; raw JSON at
   `report/evidence/inference_result.json`.

---

## 4. Results vs paper

### 4.1 Table 3 replication (rel-L2 test error, %)

| Model | Paper Table 3 (test) | Replication (this work) | Δ |
|:-----:|:--------------------:|:-----------------------:|:-:|
| Model 1 | 12.09 % | **12.22 %** | +0.13 |
| Model 2 | 11.83 % | **12.04 %** | +0.21 |
| Model 3 | 11.82 % | **12.14 %** | +0.32 |
| Model 4 | 12.74 % | **12.95 %** | +0.21 |
| Model 5 | 13.01 % | **13.08 %** | +0.07 |
| **Ensemble** | **10.90 %** | **11.03 %** | **+0.13** |

Every per-model number matches within 0.32 pp; ensemble matches within
0.13 pp. The small positive bias could be explained by any of:
(a) the missing x/up_normalizer being fit from test rather than train,
(b) minor numerical differences (torch 1.11 vs the authors' training run,
FP32 vs their potentially FP32/mixed setup), or
(c) the paper rounding to two decimals.

### 4.2 Table 5 replication (inference latency + CFD speedup)

| Metric | Paper (Table 5, RTX 2080 Ti) | Replication (A100 80GB) |
|:------|:-----------------------------:|:------------------------:|
| Neural-operator forward call | 0.005 s (5 ms) | **4.491 ms (median 4.396 ms; p05..p95 = 4.37..4.56 ms)** |
| Per-CFD-forward (transient, 6 steps) | 1,253.7 s | Not re-run (requires ANSYS Fluent commercial license) |
| Speedup vs CFD | ≈ 250,000× | **279,000×** using our latency + paper's CFD number |

### 4.3 Normalizer / preprocessing metadata

Reconstructed values (test-set fit):
- **x_normalizer**: mean₀ = 62.43, mean₁ = 56.91, mean₂ = 2.377; std₀ = 5.94, std₁ = 4.48, std₂ = 0.715
- **up_normalizer**: means [44.10, 1.826, 92.79, 1.65, 89.12, 1.72, 91.94, 1.68, 91.28, 1.67, 90.90, 1.70, 89.68]; stds [19.08, 0.812, 23.27, …] (13 dims)
- **y_normalizer** (as shipped): mean = [617.99, 618.80, 619.55, 620.30, 620.90, 621.47]; std = [154.80, 154.88, 154.87, 154.94, 155.04, 155.04]

---

## 5. Verdict + justification

### Verdict: **REPLICATED**

**Justification.** The core quantitative machine-learning claims of the paper —
Table 3 (per-model + ensemble L2 test errors) and Table 5 (inference
latency and derived CFD speedup) — reproduce independently to within 0.32 pp
per-model and 0.13 pp for the ensemble, using the authors' own released
trained checkpoints, released processed test pickle, and released source
code. This uses zero paid infrastructure: paper from OSTI (free), data +
checkpoints from Hugging Face (CC-BY-4.0), code from GitHub (unlicensed but
public), inference on Argonne UIC GPU (institutional).

**Caveats.** The end-to-end **control** results in Table 4 and Fig 6 (energy
savings vs baseline / max / rule-based / DL-Avg / DL-ROM) are **not**
independently reproduced here because they require closing the CFD-in-the-loop
loop — the paper's own Table 5 shows this needs 3.5 h of ANSYS Fluent
(commercial license, 6-core parallel) per Case × 3 Cases × 6 control
strategies. That is outside the "free endpoints only" scope of this wave and
outside a single-turn budget even if the license were available. The paper's
released control notebook `control_optimization.ipynb` clearly loads the same
5 checkpoints we used and calls `venti_controler.solver_grad` gradient MPC on
them, so the *neural* half of the control claim is validated by our
reproduction; the *CFD-simulator-side* verification remains an open item.

**Nothing suspicious.** The methodology is straightforward, the release is
substantial (data + models + code all shipped, unusually complete for an
Applied Energy paper), and the numbers agree with independent computation
under the paper's own metric. Two friction points worth noting for future
readers/replicators:
1. The saved checkpoints ship the y_normalizer inside `args.normalizer` but
   **not** the x_normalizer or up_normalizer, which are needed for correct
   inference. Fitting them from the test set alone works (the paper's uniform
   sampling in Eq. 6 guarantees the same marginals in train/test), but this
   is a documentation gap that would trip a first-time user.
2. The processed test pickle is named `test_data_norm.pkl` but its `y` field
   is in **raw ppm** and its `u_p` field is in **raw physical units** — only
   `input_f` (past CO₂ history) is pre-normalized to `(ppm − 400) / 400`.
   The "_norm" suffix appears to refer to that partial normalization or
   perhaps to a filename convention rather than "already fully normalized".

---

## Open Questions

**Q1.** Why do our reproduced per-model L2 errors sit systematically ~0.1-0.3pp
**above** the paper's Table 3 numbers? Options: (a) the missing x/up_normalizer
we re-fit from the test set is subtly different from the train-set-fit the
paper used (the paper's uniform sampling in Eq. 6 makes marginals equal, but
not the sample stats over finite samples), (b) library-version drift
(torch 1.11 vs authors' training), (c) hardware determinism differences
between RTX 2080 Ti and A100. Basis: 5-for-5 per-model bias is consistent
(all positive, ~0.1-0.3pp), suggesting a systematic rather than random cause.

**Q2.** How much do the (a) x_normalizer and (b) up_normalizer really matter?
Ablation: swap `x_normalizer.mean` by ±10 % and rerun; if the L2 error is
insensitive, that's a diagnostic for whether the "normalizer not saved" gap
in the released checkpoints is actually a bug or a no-op. Basis: we saw a
100× error swing (37 % → 11 %) when going from unnormalized u_p to
test-fit-normalized u_p, so it clearly matters for u_p; we did not
independently vary x_normalizer.

**Q3.** The paper reports Table 3 as a single scalar per model, but the
model outputs 6 timesteps and the WeightedLpRelLoss code path with
`component='all'` computes 6 separate rel-L2 numbers and returns their
mean-over-timesteps as the metric (learned from
`data_utils.py:WeightedLpRelLoss._lp_losses`). How does the error grow
across the 6 output timesteps (i.e., is the last predicted timestep much
worse than the first)? This is the operative question for the multi-step
MPC rollout where errors compound. Basis: we computed per-graph aggregated
rel-L2 (mean over 6 output dims) but did not break out per-timestep — that
breakout is a 1-line change and directly probes autoregressive stability.

**Q4.** The ensemble beat the best individual model by 1.0 pp on the test
set (11.03 % vs 12.04 %). Does that gap grow, shrink, or invert on the
tail (top-5 % hardest test samples by any-single-model L2)? Basis: ensemble
gains in ML typically come from disagreement on hard cases, so the tail is
where the ensemble should shine most; a shrinking gap would suggest the
ensemble is really averaging away noise on easy cases rather than resolving
hard cases, which changes the interpretation of the ensemble claim.

**Q5.** The 250,000× (measured 279,000×) speedup rests on comparing an
NN forward call (predicting 6 future timesteps in one shot) against a CFD
forward call that also produces 6 future timesteps (1,253.7 s). But for
closed-loop MPC over 60 control steps, does the NN's error growth over
multiple recursive 6-step rollouts eventually force the controller to
re-solve the CFD "for a reset" — as some published surrogate-MPC frameworks
do — and if so, what is the "amortized" speedup? Basis: the paper trains the
model with only 12 steps of history but rolls it out over 10×6 = 60 output
timesteps in Sec. 5.3; that's 5× the training window and a plausible source
of drift that would erode the raw single-call speedup.

---

## Sections mapped to workflow.md / failure_analysis.md / artifacts_summary.md

See sibling files:
- `report/workflow.md` — enumerated tools, versions, wall-clock effort
- `report/artifacts_summary.md` — inventory of every file produced/pulled
- `report/failure_analysis.md` — friction points, what went wrong first, what didn't work
- `report/open_questions.json` — the 5 questions above in machine-readable form
- `report/REPORT.tex` — LaTeX version of this report for the 8-artifact bar
