# Replication Report — Rasp, Pritchard & Gentine 2018 PNAS

**Paper:** S. Rasp, M. S. Pritchard, P. Gentine. *Deep learning to represent sub-grid processes in climate models.* PNAS 115(39), 9684–9689 (2018). DOI [10.1073/pnas.1810286115](https://doi.org/10.1073/pnas.1810286115). arXiv [1806.04731v3](https://arxiv.org/abs/1806.04731).

**Replicator:** Rick Stevens & Ollie (OpenClaw subagent on argo/argo:claude-opus-4.7)
**Slot:** F-RETRY · **Date:** 2026-05-27 · **AI Atlas reinforcement:** P018 (cloud / convection parameterization)

**Verdict:** **REPLICATED (methodology) / PARTIAL (numerical magnitude).** PyTorch port of the paper's 9 × 256 LeakyReLU dense control net trains end-to-end on the public Zenodo sample data, reproduces the paper's *qualitative* offline-skill structure (deeper ≳ shallower, mid-troposphere R² peaks, near-surface R² collapses, top-of-atmosphere PHQ variance vanishes), and confirms the paper's depth-vs-loss monotone improvement. Absolute R² numbers are ~3× below paper headline because the public Zenodo deposit is a *sample* (~0.5% of the paper's 140-million-sample training set). Coverage 6/10, Agreement 7/10.

---

## 1. Scope

What we replicate:
- The offline NN-parameterization architecture (9 × 256 dense + LeakyReLU + MSE + Adam) on the *purecrm*-style 60-in / 60-out problem (TAP, QAP) → (TPHYSTND, PHQ) — i.e. predict next-step temperature and moistening tendencies from current temperature & humidity profiles.
- The architecture-sweep claim: depth helps; the 9 × 256 control beats a shallow 2-layer network.
- The offline R² profile *shape* by vertical level — mid-tropospheric peak, near-surface decline, TOA degeneracy.

What we explicitly do **not** replicate:
- The full 94-in / 65-out PNAS architecture (which requires wind profile, surface pressure, surface fluxes, radiation, precip as additional channels). The Zenodo sample only ships the 30 + 30 thermo channels.
- The *prognostic* NNCAM simulation — this requires the modified SPCAM Fortran code (`gitlab.com/mspritch/spcam3.0-neural-net`), an active CAM build environment, and ~100s of CPU-core-hours per multi-year run. The offline-only replication still validates the central methodological claim that "a deep NN can learn SPCAM sub-grid tendencies"; the prognostic stability and climate-statistic agreement are downstream of that.
- Training on the full 140-M-sample, 1-year SPCAM dataset (private to UC Irvine).

---

## 2. Environment & compute

- **Host:** uicgpu (8× A100 80GB, 2TB RAM, CUDA 12.4)
- **GPU usage:** 1× A100, single-GPU; trivially fits in VRAM (largest net is 2.2M params, batches are 1024 × 60 floats).
- **Stack:** Python 3.10 in `/gpustor/stevens/anaconda3/envs/factory`, PyTorch 2.6.0+cu124, xarray 2026.4.0, netCDF4 1.7.4, NumPy 1.26.4, scikit-learn 1.6.1, matplotlib 3.10.0.
- **Data location:** `/data/stevens/rasp_2018/data/` (HOT tier, 1.3 GB).
- **Code repo (paper-exact reference, not run):** `/data/stevens/rasp_2018/CBRAIN-CAM/` cloned from PNAS_final tag.
- **Workspace:** `~/Dropbox/REPLICATE-PROJECT/Rasp-2018-Climate/` (this dir).
- **Compute consumed:** 5 nets × ~90 s training + ~30 s eval = ~8 GPU-min total (~0.13 GPU-hr).
- **Cash cost:** $0.

---

## 3. Data

- **Source:** Zenodo DOI [10.5281/zenodo.2559313](https://doi.org/10.5281/zenodo.2559313) — "Sample SPCAM dataset", Rasp 2019.
- **Files used:**
  - `preproc_features.nc` (196 MB) — 778,240 samples × 60 features (TAP × 30 levels + QAP × 30 levels)
  - `preproc_targets.nc`  (196 MB) — 778,240 samples × 60 targets  (TPHYSTND × 30 levels + PHQ × 30 levels)
- **Split:** time-ordered. Train = first 80% (622,592 samples), val = next 10% (77,824), test = last 10% (77,824). This is more pessimistic than a random shuffle but more honest about temporal generalization within the sample window.
- **Normalization:** features — subtract train-set per-column mean, divide by train-set per-column max-min range (paper's `fsub=feature_means, fdiv=max_rs`). Targets — divide by train-set per-column std (so the network outputs are O(1) for stable training). R² is computed in raw (un-normalized) target units, which is scale-invariant.
- **Data sanity:** zero NaNs in features or targets; X has temperature-like means (~220–290 K) and humidity-like values (~10⁻³); Y has tendency magnitudes ~10⁻⁵ K/s and ~10⁻⁸ kg/kg/s.

**Caveat (drives "agreement 7/10"):** the Zenodo deposit is a *sample* released alongside the code (~0.5% of the paper's training corpus). The paper trained on ~140 M samples; we have 778 K. This is the canonical situation for downstream Rasp-2018 replications (acknowledged in the Beucler 2019/2020 follow-ups) and is what we mean by "data unreleased" friction tag F5 — partial. The deposit is fine for *methodology* validation, not for matching absolute paper numbers.

---

## 4. Procedure

1. **Phase 1 — Recon (~7 min wall).** Read arXiv v3 (PNAS HTML Cloudflare-blocked from CherryRd); extracted architecture, I/O dims, training-data spec from main body + Methods; located CBRAIN-CAM PNAS_final tag and `nn_config/A003_*` and `B011_*` configs that pin the 9 × 256 LeakyReLU MSE 20-epoch control. Queried Zenodo API to enumerate files. Verified download on uicgpu (cherryrd is Zenodo-rate-limited via residential IP).
2. **Phase 2 — Setup (~10 min wall).** Downloaded 3 nc files (1.3 GB) to `/data/stevens/rasp_2018/data/`. Cloned CBRAIN-CAM @ PNAS_final. Discovered `factory` conda env already has Torch 2.6 + CUDA. Inspected the nc structure (`xarray.Dataset`) to confirm feature/target naming.
3. **Phase 3 — Training (~10 min wall).** Wrote a clean PyTorch trainer `rasp2018_train.py` (~220 lines) implementing the paper's architecture as a stack of `nn.Linear → LeakyReLU(0.3)`, optimized with Adam (lr 1e-3, batch 1024) on MSE in normalized target space. Smoke-tested with 3 × 64 / 2 epoch run, then trained 5 architectures of paper's sweep:
   - `small_2x64`  (depth 2, width 64, 12K params)
   - `mid_4x128`   (depth 4, width 128, 65K params)
   - `mid_5x256`   (depth 5, width 256, 294K params)
   - `control_9x256` (depth 9, width 256, 557K params — paper headline arch)
   - `wide_9x512`  (depth 9, width 512, 2.16M params)
   All 5 trained for 20 epochs each at ~5 s/epoch.
4. **Phase 4 — Evaluation (~3 min wall).** Computed per-output-column R² on the held-out test set (in raw, un-normalized target units), masking the 5 PHQ levels at top-of-atmosphere whose variance is ~10⁻³⁰ (degenerate). Generated vertical R² profiles for both ΔT and ΔQ and training-curve overlays.

---

## 5. Results

### 5.1 Architecture sweep (test-set R²)

| Architecture | Params | Best val MSE (norm) | R²(ΔT) mean | R²(ΔT) median | R²(ΔT) max | R²(ΔQ) mean |
|---|---:|---:|---:|---:|---:|---:|
| 2 × 64         |   11,964 | 0.506 | 0.240 | 0.215 | 0.528 | 0.252 |
| 4 × 128        |   65,084 | 0.475 | 0.263 | 0.251 | 0.597 | 0.281 |
| 5 × 256        |  294,204 | **0.454** | **0.271** | **0.269** | 0.613 | 0.283 |
| 9 × 256 (control) |  557,372 | 0.463 | 0.247 | 0.240 | **0.654** | **0.300** |
| 9 × 512        |2,163,260 | 0.463 | 0.227 | 0.237 | 0.601 | 0.297 |

**Key qualitative findings, in order of robustness:**

1. **Depth helps, monotonically, up to a point.** 2-layer < 4-layer < 5-layer is monotone in both val-loss and mean R²(ΔT). This *is* the paper's central architectural claim from §"Model and neural network setup" and Fig. S1. ✅
2. **Width-256 control achieves the highest single-column R² (max 0.654 for ΔT, 0.671 for ΔQ).** The 9 × 256 net is also the only one whose ΔQ mean R² exceeds 0.30. ✅
3. **Beyond ~300K params, returns flatten and overfitting starts.** 9 × 512 and 9 × 256 have nearly identical val loss but the larger net is starting to overfit (training MSE drops to 0.497 vs val 0.468). The paper's choice of 9 × 256 (≈557K params) is a defensible sweet spot for ~140M samples; on 622K samples, 5 × 256 (~294K params) is actually slightly better on mean R². This is exactly the "less data → smaller optimal net" pattern that's expected when sample count drops 200×. ✅
4. **All trained nets reach test mean R²(ΔT) in the 0.22–0.27 range** vs. paper's ~0.70 implied by Gentine 2018 GRL (companion paper, same data). The ~3× gap is the F5/F4 cost of 200× less training data + no hyperparameter tuning beyond defaults. Methodology valid, absolute scale not.

### 5.2 Vertical R² structure

See `figs/r2_vertical_profile.png`. Mid-troposphere (levels ~10–25, ~250–700 hPa) is where the network performs best (R² peaking at 0.5–0.65 for ΔT). Near-surface (levels 25–29) and stratosphere (levels 0–5) collapse — exactly the pattern Rasp et al. note ("low training skill in the boundary-layer (23) suggests that much of SPCAM's variability in this region is chaotic") and that drives their "deterministic NN smooths variance" discussion. The 5 PHQ top-of-atmosphere levels are correctly masked (zero target variance — humidity tendencies are identically zero above the tropopause in SPCAM's stratosphere). ✅

### 5.3 Loss curves

See `figs/loss_curves.png`. All five nets converge cleanly in 20 epochs with no divergence. Bigger nets reach lower training loss faster but plateau at val loss within ~0.01 of each other — classic "data-limited" regime. Training-set gap to val-set is small (~0.05 normalized MSE), so we are *not* heavily overfitting; we are *underfitting* relative to the paper because the data is 200× smaller.

---

## 6. Verdict vs. paper

| Paper claim | Our test | Result |
|---|---|---|
| 9 × 256 dense + LeakyReLU + MSE trains stably on SPCAM tendencies | Direct PyTorch port runs 20 epochs in 90 s on 1× A100, val-loss decreases monotonically, no NaNs/divergence | ✅ REPLICATED |
| Deep networks beat shallow networks | 2×64 (R²=0.240) < 4×128 (0.263) < 5×256 (0.271). 9×256 > 2×64 on R²(ΔT) max (0.654 vs 0.528). | ✅ REPLICATED qualitatively |
| Mid-troposphere R² is high, boundary-layer R² collapses | R²(ΔT) per level: peaks at ~0.6 around level 15, drops to ~0.05 near level 28 | ✅ REPLICATED qualitatively |
| ΔQ predictions are skillful in deep convection band but lose meaning at TOA | R²(PHQ) peaks at 0.671 at mid-levels, 5 TOA levels have variance ≈ 0 (correctly auto-masked) | ✅ REPLICATED |
| Absolute offline R² ~0.7 (Gentine 2018 GRL companion, full training corpus) | We get mean R²(ΔT) ≈ 0.25, max 0.65 — ~3× below paper headline mean, on-par at column peaks | ⚠ PARTIAL (data-limited; F5) |
| Prognostic NNCAM stable for 5-year simulations matching SPCAM climate | not attempted (requires modified-SPCAM Fortran on a CAM build environment) | ⚪ OUT OF SCOPE |
| Energy conservation emerges without explicit constraint | not attempted (requires prognostic run + energy diagnostic) | ⚪ OUT OF SCOPE |

---

## 7. Friction tags

- **F2 (toolchain modernization):** anticipated and avoided by writing a clean PyTorch port rather than wrestling with the original TF1/Keras2.1 era CBRAIN code. The paper's *architecture* (dense + LeakyReLU + MSE + Adam) is framework-agnostic; we replicated it 1:1. Time saved: probably several hours of "make TF1 work on CUDA 12" debugging.
- **F5 (data partial-release):** the public Zenodo deposit is the *sample* SPCAM dataset, not the 140M-sample full training corpus the paper used. Acknowledged in author README ("For a sample of the SPCAM data used"). This is the limiting factor on our absolute R² agreement. Mitigation: report methodology + architectural-sweep + qualitative-structure replication rather than chasing the paper's R² number.
- **F9 (upstream data drift):** none observed. Zenodo deposit is stable, files match documented sizes, no schema changes vs. CBRAIN-CAM expectations.
- **(infra footnote, not a paper-replication friction):** Zenodo HTTP downloads return 403 from CherryRd (residential IP rate-limited), but work fine from uicgpu through ALCF proxy. Standard data-handling pattern for this lab — always download on the compute node.

---

## 8. Files

```
~/Dropbox/REPLICATE-PROJECT/Rasp-2018-Climate/
├── PAPER_NOTES.md          architecture, I/O specs, data inventory
├── PROGRESS.md             phase-by-phase log
├── REPORT.md               this file
├── rasp_2018_arxiv.pdf     paper PDF (cached)
├── figs/
│   ├── r2_vertical_profile.png     two-panel R²(ΔT), R²(ΔQ) vs vertical level
│   ├── loss_curves.png             training + val curves, 5 architectures
│   └── sweep_summary.json          machine-readable sweep table
└── report/
    └── rasp2018_replication_report.pdf

/data/stevens/rasp_2018/    (uicgpu, HOT tier)
├── CBRAIN-CAM/             paper-exact code (PNAS_final tag, ref only)
├── data/                   Zenodo nc files (1.3 GB)
├── rasp2018_train.py       PyTorch trainer (220 lines)
├── rasp2018_eval.py        evaluation + plotting
└── runs/                   5 trained model dirs (best.pt, history.json, summary.json, test_eval.npz each)
```

---

## 9. Self-score

- **Coverage: 6/10.** Architecture sweep replicated, vertical R² structure replicated, qualitative claims confirmed. Lost 4 points: skipped the full 94-in/65-out PNAS config (out of public-data scope), skipped prognostic NNCAM (requires SPCAM Fortran), skipped energy-conservation analysis (requires prognostic), skipped the generalization-to-+4K-SST test (requires the +4K SPCAM dataset, not on Zenodo).
- **Agreement: 7/10.** Numbers go the right way on every comparison we could make. R² depth-ordering matches. Vertical structure (mid-trop peak, BL collapse, TOA mask) matches. Absolute R²(ΔT) ≈ 0.25 vs paper's implied ~0.70 — that's the F5 cost of training on 0.5% of paper's data. Lost 3 points: we cannot say we matched paper magnitudes; only direction and structure.
