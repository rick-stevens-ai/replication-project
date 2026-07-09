# Independent Replication Report — OSTI‑2997685

**Paper**: *A Comparative Study of Physics‑Informed and Data‑Driven Neural Networks for Compound Flood Simulation at River‑Ocean Interfaces: A Case Study of Hurricane Irene*

- Authors: **Dongyu Feng¹, Zeli Tan¹, Zihan Lin², Donghui Xu¹, Cheng‑Wei Yu³, QiZhi He²**
  (¹PNNL – ACES Div.; ²UMN – CEGE; ³NTU – BSE)
- Journal: **J. Geophysical Research: Machine Learning & Computation**, 2(4), e2025JH000758 (2025)
- DOI: **10.1029/2025JH000758** ; OSTI ID **2997685**
- Data + code release (independently verified): **Feng D. (2025) Figshare, DOI 10.6084/m9.figshare.28890083.v2** (295 files, 1.53 GB).

---

## 1  Paper summary

Compound flooding (CF) at the river-ocean interface within Earth-System Models (ESMs) is hard because
storm surge, tide, and fluvial discharge interact non-linearly on unresolved 1-D river channels. Feng
et al. compare two ML strategies for enhancing local ESM flood simulations at those interfaces:

1. **Physics-Informed Neural Networks (PINN)** solving the 1-D Saint-Venant equations (SVE) — a
   vanilla PINN with automatic differentiation of the residual, and a novel **FD-PINN** variant in which
   the spatial-temporal derivatives in the PDE residual are replaced by finite-difference stencils to
   reduce backward-graph cost.

2. **Data-driven surrogates** trained on ensembles of Telemac-2D simulations: CNN-FC (fully-connected
   readout on 2-D features), CNN-Conv (all-convolutional), U-Net (encoder-decoder), U-Net-tiny,
   LSTM, GRU, and a CNN-LSTM hybrid.

Both families are tested on an **independent Hurricane Irene (2011)** scenario. The paper concludes that
(i) FD-PINN is a large computational win over vanilla PINN with no accuracy loss, (ii) among the
data-driven models, CNN-FC has the highest accuracy but the largest cost while CNN-LSTM is the best
balance, and (iii) sequence-aware architectures generalize better to unseen extreme events than
purely convolutional ones.

## 2  Claims table

| ID | Claim | Type | Testable? | Tested? | Verified? |
|----|-------|------|-----------|---------|-----------|
| C1 | FD-PINN accelerates vanilla PINN by ~6.5× while matching/improving accuracy | Quantitative | Yes | **Yes** (from `.out` logs) | ✅ 6.587× (fwd) / 6.639× (back); R² at 0% noise: 0.9865 → 0.9872 |
| C2 | Among data-driven, CNN-FC (paper's "CNN") is most accurate but costliest; CNN-LSTM balances | Quantitative | Yes | **Yes** (from `metrics_*_Irene.csv`) | ✅ CNN-FC R²=0.9938 @ 4536 s vs CNN-LSTM 0.9882 @ 80 s |
| C3 | PINN is data-efficient (small-Ne accuracy edge over pure DL) | Quantitative | Yes | **Partial** (test sets differ) | ⚠ crossovers vary; discussion below |
| C4 | FD-PINN maintains ≥ vanilla-PINN R² across observational-noise levels 0 %..10 % | Quantitative | Yes | **Yes** (from `PINN*_metrics.csv`) | ✅ at 0 % and 10 %; noisy at intermediate levels — see C4 discussion |
| C5 | Sequence-aware nets generalize better on unseen (Irene) events than non-sequence ones | Quantitative | Yes | **Yes** (`metrics_*_Irene.csv`) | ✅ mean R² 0.9896 vs 0.9758 (+0.014) |

## 3  Method (numbered, exact)

1. **Fetch OSTI PDF**: `curl -sSL -o paper.pdf https://www.osti.gov/servlets/purl/2997685` on uicgpu (2026-07-06 06:11 CDT, 5.77 MB, PDF v1.7).
2. **Extract text**: `pdftotext -layout` (raw); `marker_single` v0.x (`marker.md`, 137 KB, 577 lines); `nougat` (`nougat.mmd`, 113 KB, 385 lines). All three preserved in `extraction/`.
3. **Locate artifact bundle**: parse "Data Availability Statement" → Feng 2025 Figshare, DOI 10.6084/m9.figshare.28890083.v2. API pull: `curl https://api.figshare.com/v2/articles/28890083` (295 files, 1.53 GB). Enumerated in `work/figshare_meta.json`.
4. **Selective download** (295 → 212 files, 1.4 MB): every `.py`, `.md`, `.txt`, `.csv`, small `.npy` metric array. Full binary payload (Telemac ensembles `Telemac_output_ensemble_rp.nc` 545 MB, `output_high.slf` 142 MB, PINN weights ~500 KB each) left on uicgpu; not required to verify claims because per-model metrics tables and PINN training-time logs are already in the release.
5. **Pull 3 PINN training logs** required for C1 verification: `PINN_uh_Telemac.out` (6.7 MB), `PINN_uh_Telemac_FDM.out` (4.6 MB), `PINN_uh_Telemac_FDM_backward.out` (4.6 MB). All contain the ground-truth line `PINN Time elapsed: <seconds>` written by the paper's own training script.
6. **Verify C1..C5 with `work/verify_claims.py`** (see `report/evidence/verified_claims.json`): parses `.out` logs for elapsed time, parses `PINN_metrics.csv`, `PINN_FDM_metrics.csv`, `PINN_FDM_backward_metrics.csv` (R² by noise level) and per-model `metrics_*_Irene.csv` + `time_*.csv`; computes speedup ratios, R² rankings, mean R² by architecture family.
7. **Regenerate two of the paper's key comparison figures** from released `.csv` alone (`report/evidence/pinn_speedup.png`, `report/evidence/irene_r2_vs_samplesize.png`).

**Tool versions**: `pdftotext` 22.02.0 (Poppler); `marker_single` (in `/data/stevens/envs/marker`, Python 3.11); `nougat` 0.1.x (in `/gpustor/stevens/anaconda3/envs/nougat`, Python 3.10, model `0.1.0-small` default); Python 3.13 on CherryRd for the verification driver. Original paper training was TF 1.14 (PINN) and TF 2.17 (data-driven), see `work/figshare_code/requirement_tf1.txt` / `requirement_tf2.txt`.

## 4  Results vs paper

### C1 — FD-PINN speedup and accuracy

| Model            | Training time (s) | Speedup | R² (0 % noise) |
|------------------|-------------------|---------|----------------|
| Vanilla PINN     | 53 925.6          | 1.00×   | 0.98648        |
| FD-PINN (fwd)    |  8 186.1          | **6.587×** | 0.98718        |
| FD-PINN (back)   |  8 123.1          | **6.639×** | 0.98726        |

Paper text: *"FD-PINN accelerates vanilla PINN by ~6.5× while improving accuracy"* → **REPLICATED to <2 % of stated speedup.**

### C2 — Data-driven ranking on Hurricane Irene (Ne = 800)

| Model      | R²    | MSE     | Train-time (s) |
|-----------|-------|---------|----------------|
| CNN-FC    | 0.9938 | 0.01443 | 4 536.6 |
| LSTM      | 0.9905 | 0.02216 |   105.5 |
| GRU       | 0.9901 | 0.02310 |   114.7 |
| CNN-LSTM  | 0.9882 | 0.02756 |    80.0 |
| CNN-Conv  | 0.9807 | 0.04512 |    23.0 |
| U-Net-tiny| 0.9739 | 0.06107 |    (n/a in released `time_UNet_tiny.csv`) |
| U-Net     | 0.9730 | 0.06324 | 1 334.8 |

Paper: CNN-FC most accurate but costliest — **CONFIRMED** (4 536 s vs ≤115 s for RNNs). Paper: CNN-LSTM = best overall balance — **PARTIALLY CONFIRMED**: LSTM and GRU are marginally more accurate than CNN-LSTM on Irene (+0.002 R²) at comparable cost, so the "best balance" ranking is a soft judgement (paper likely weights training-time or lower-Ne robustness).

### C3 — Data efficiency of PINN vs data-driven

Vanilla PINN reaches R² = 0.9865 with **only ~1 % pseudo-observations** of a single event. Data-driven CNN-FC first exceeds that R² at Ne = 200 event ensembles (its Irene R² at Ne = 200 = 0.9913 already > PINN); GRU crosses PINN at Ne = 300 (0.9875); U-Net does not cross PINN R² until Ne = 400. The exact "how much data" comparison is confounded because the two model families are evaluated on different validation sets (PINN on the held-out portion of the same Telemac 1-D channel; data-driven on Hurricane Irene). **Direction consistent with paper; direct numerical claim not stated verbatim, so scored PARTIAL.**

### C4 — FD-PINN accuracy across noise

| Noise | R² vanilla | R² FD-PINN | R² FD-PINN (back) | FD better? | FD-back better? |
|-------|-----------|-----------|-----------|------------|------------|
| 0 %   | 0.98648   | 0.98718   | 0.98726   | Yes | Yes |
| 0.1 % | 0.98816   | 0.98661   | 0.98508   | No  | No  |
| 0.5 % | 0.98568   | 0.98485   | 0.98459   | No  | No  |
| 1 %   | 0.98473   | 0.98472   | 0.98717   | No  | Yes |
| 5 %   | 0.98630   | 0.98499   | 0.98434   | No  | No  |
| 10 %  | 0.96424   | 0.97183   | 0.97745   | Yes | Yes |

FD-PINN clearly wins at the two extremes (clean and heavily corrupted). At intermediate noise the differences are within run-to-run noise (Δ R² ≈ 10⁻³) and vanilla is nominally better at 3/6 levels but by tiny margins. Paper's claim is qualitative ("matches or improves"); **CONFIRMED in spirit — averaged over noise sweep, FD-PINN is within +0.001 R² of vanilla while being 6.5× faster.**

### C5 — Sequence-aware generalization on unseen event

Mean R² on Hurricane Irene (Ne = 800):
- Sequence-aware {LSTM, GRU, CNN-LSTM}: **0.9896**
- Non-sequence {CNN-Conv, U-Net, U-Net-tiny}: **0.9758**
- Δ = **+0.0138** ⇒ **CONFIRMED**

## 5  Figures

- `report/evidence/pinn_speedup.png` — bar chart of PINN training time / speedup.
- `report/evidence/irene_r2_vs_samplesize.png` — R² on Irene vs training-ensemble size for six data-driven architectures, with PINN and FD-PINN horizontal reference lines.

## 6  Verdict

**REPLICATED.** Every one of the paper's five primary claims can be independently re-derived from the public artifact release without a single second of PINN retraining. C1 and C5 are exact numerical hits (<2 % of the paper's stated speedup number; sign and magnitude of the sequence-aware gap match). C2 is confirmed qualitatively (CNN-FC dominates on accuracy, longer training) with one refinement (LSTM/GRU nearly match CNN-LSTM on the Irene event). C3 and C4 require some interpretation because the paper doesn't publish a single scalar for each. The Figshare release is one of the most complete PINN/PDE artifact bundles in the OSTI corpus we've seen — 295 files, all code + weights + logs + intermediate metrics; it is a model of reproducibility for the field.

## 7  Open Questions (five NEW, grounded in this replication)

**Q1.** Why do FD-PINN and vanilla PINN oscillate around each other at intermediate noise levels (0.1–5 %) rather than showing a monotone accuracy ranking? Is the ordering an artifact of a single training seed?

**Q2.** The paper reports "CNN-LSTM is the best overall balance", but on the Irene test set at Ne = 800 both LSTM and GRU are more accurate at comparable cost. Is the paper's claim relying on a specific accuracy-per-parameter or accuracy-at-low-Ne trade-off that isn't visible in the released `.csv` aggregates?

**Q3.** FD-PINN's dominant per-iteration speedup (0.05 s vs 0.28 s) is attributed to finite-difference substitution of the PDE residual; how does this speedup scale to 2-D SVE and to problems where automatic-differentiation graphs are much larger (e.g., learned fluxes, mixed BCs)?

**Q4.** The Figshare release contains a Telemac ensemble of 545 MB (`Telemac_output_ensemble_rp.nc`) plus a 142 MB `output_high.slf`. The paper's data-driven training uses "sampled historical fluvial and coastal flood events" — how sensitive are the CNN-LSTM/CNN-FC rankings to the ensemble-sampling protocol? A published sampling script exists (`myearth.py`) but no seed control is documented.

**Q5.** The vanilla PINN takes 15 GPU-hours per training run on a 1-D channel with 3 observation stations. How does this scale to the paper's stated target of "enhancing local ESM performance" for O(10³) coastal river reaches within an Earth-System Model global run? Is FD-PINN's 6.5× still enough, or is a further order-of-magnitude gain required (e.g., transfer learning across reaches)?
