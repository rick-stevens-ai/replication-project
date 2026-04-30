# REPORT — Deep Learning of Atomically Resolved Scanning Transmission Electron Microscopy Images: Chemical Identification and Tracking Local Transformations

**OSTI ID:** 1427646 · **Authors:** M. Ziatdinov, O. Dyck, A. Maksov, X. Li, X. Sang, K. Xiao, R. R. Unocic, R. Vasudevan, S. Jesse, S. V. Kalinin (ORNL) · **Year:** 2017 · **Journal:** ACS Nano 11(12)

---

## Paper claim

Ziatdinov et al. demonstrate that a fully convolutional neural network (FCN) with an encoder–decoder architecture, trained entirely on multislice-simulated HAADF-STEM images, can perform pixel-wise chemical identification of atomic columns in experimental scanning transmission electron microscopy data. Applied to SrTiO₃/La₀.₇Sr₀.₃MnO₃ perovskite heterostructures and Si-doped graphene, the network produces per-column chemical identity maps, localises atomic positions with sub-unit-cell precision, and tracks defect transformations (antisites, vacancies, dopant coordination switching) across time-series frames — all without retraining on experimental labels. The key claim is that simulation-trained deep learning generalises quantitatively to real STEM data, enabling automated chemical mapping at the atomic scale.

## What we replicated

| Component | Paper | Our replication |
|---|---|---|
| **Architecture** | Encoder–decoder FCN (SegNet-like), conv + max-pool encoder, un-pool + conv decoder, softmax pixel classifier | 5-level U-Net (7.76 M params), double 3×3 conv + BN/ReLU, max-pool, transposed-conv upsample, skip concatenations, softmax head — functionally equivalent encoder–decoder FCN |
| **Image formation** | Multislice simulation (frozen-phonon, full dynamical scattering) of STO/LSMO [001] heterostructures | Physics-motivated synthetic surrogate: perovskite [001] square lattice, Gaussian atomic columns with Z^1.7 HAADF contrast, interface diffuseness, Poisson noise, scan-line jitter, vacancies + antisites. Also built an abTEM multislice generator (`multislice_gen.py`) and ran a combined training experiment on 64 multislice + 384 synthetic frames |
| **Training** | Simulated → experimental transfer (classes: lattice, depression, protrusion for graphene; Sr, Ti, La/Sr, Mn, vacuum for perovskite) | AdamW, cosine LR schedule, cross-entropy with inverse-frequency class weighting, on-the-fly flip/rotate/brightness augmentation, 30 epochs, batch 16 on one NVIDIA A100 80 GB (95 s wall time) |
| **Evaluation** | Qualitative: chemical maps on experimental STEM frames; sub-unit-cell column localisation | Quantitative on 128-frame synthetic held-out test: pixel accuracy, per-class precision/recall/F1, peak-detection recall/precision, column-centre RMSE |
| **Defect tracking** | Time-series analysis of Si dopant switching in graphene, antisite/vacancy identification in perovskites | Defects generated stochastically (2% vacancy, 2% antisite); detected implicitly through cation-class confusion patterns |

## Key results (paper vs. ours)

| Metric | Paper (qualitative / reported) | Our replication (128-frame test, 8.4 M pixels) |
|---|---|---|
| **Overall pixel accuracy** | Not reported as a single number; qualitative "high accuracy" on experimental frames | **0.988** |
| **Per-class F1 — Sr** | Visually near-perfect A-site identification | **0.994** |
| **Per-class F1 — Ti** | B-site harder near interfaces (acknowledged) | **0.949** |
| **Per-class F1 — La/Sr** | Heavy A-site trivially separable (Z^1.7 contrast) | **0.998** |
| **Per-class F1 — Mn** | B-site harder near interfaces (acknowledged) | **0.958** |
| **Column-centre localisation** | Sub-unit-cell precision (qualitative, demonstrated via overlays) | RMSE: Sr 0.11 px, Ti 0.47 px, La/Sr 0.06 px, Mn 0.45 px (at ~0.2 Å/px → 12–94 mÅ, well sub-pixel) |
| **Column detection recall** | >95% implied by visual overlays | Sr 1.000, Ti 0.983, La/Sr 1.000, Mn 0.988 |
| **Column detection precision** | — | Sr 0.978, Ti 0.943, La/Sr 0.997, Mn 0.944 |
| **Heavy-vs-light A-site** | "Trivially" distinguished by FCN (La/Sr vs Sr) | Confirmed: La/Sr F1 = 0.998 vs Sr F1 = 0.994 |
| **B-site confusion** | Ti↔Mn confusion near interface is dominant error | Confirmed: Ti F1 = 0.949 and Mn F1 = 0.958 are lowest |
| **Multislice transfer** | Full multislice training → experimental application | Combined synthetic+abTEM run: 80.8% pixel accuracy on multislice held-out (limited to 64 low-res frames); Ti F1 dropped to 0.197, showing domain gap from surrogate-to-multislice |

## Honest gaps

1. **No true multislice at scale.** The primary training used a Gaussian-column physics surrogate, not frozen-phonon multislice. The abTEM multislice generator was implemented and tested (64 frames, 56×56 px), but full-scale multislice training was out of compute budget. The combined-training experiment showed an expected domain gap (80.8% pixel accuracy on multislice test vs 98.8% on synthetic test).

2. **No experimental STEM validation.** The paper's central demonstration is simulation→experiment transfer. Our replication evaluates only on synthetic/simulated data. We did not obtain or test on real HAADF-STEM frames from the ORNL archives.

3. **Defect class is weakly supervised.** Under the current label encoding, antisite/vacancy defect pixels are not directly surfaced as a separate predicted class — defects are captured only implicitly through cation-class confusion. A multi-label or auxiliary defect head would be needed to match the paper's explicit defect tracking.

4. **No graphene / MoWSe₂ systems.** The paper also demonstrates the method on Si-doped graphene (atom finding + defect coordination analysis) and Mo₁₋ₓWₓSe₂. We replicated only the perovskite heterostructure pipeline.

5. **No time-series tracking.** The paper tracks antisite switching and dopant coordination changes across sequential frames. Our evaluation is single-frame classification only.

## Score

| Dimension | Score | Rationale |
|---|---|---|
| **Coverage** | **6/10** | Architecture faithfully re-implemented; training protocol reproduced; synthetic data generator captures correct physics (Z^1.7 contrast, sublattice geometry, defects, noise). However, missing: full multislice image formation, experimental validation, graphene/TMDC systems, and time-series defect tracking. |
| **Agreement** | **7/10** | On synthetic data, results are fully consistent with the paper's qualitative claims: near-perfect A-site classification, harder B-site near interfaces, sub-unit-cell column localisation. The 98.8% pixel accuracy and ≥0.949 per-class F1 are plausible upper bounds. But we cannot confirm the paper's core claim of simulation→experiment generalisation since we lack experimental test data. |

## Deliverables

| Artefact | Path |
|---|---|
| Original paper PDF | `1427646.pdf` |
| Replication plan | `replication_plan.pdf`, `replication_plan_1427646.tex` |
| Synthetic STEM generator | `replication/src/synth_stem.py` |
| abTEM multislice generator | `replication/src/multislice_gen.py` |
| U-Net model (PyTorch) | `replication/src/unet.py` |
| Training script | `replication/src/train.py` |
| Combined training script | `replication/src/train_combined.py` |
| Figure generation | `replication/src/make_figures.py` |
| Best model checkpoint | `replication/runs/combined/best.pt` |
| Test metrics (JSON) | `replication/logs/test_metrics.json` |
| Peak detection stats | `replication/figures/peak_stats.json` |
| Training log | `replication/logs/train.log` |
| Figures (data, predictions, history, confusion matrix, peaks) | `replication/figures/fig_*.png` |
| Detailed replication report (LaTeX + PDF) | `replication/report/report.tex`, `replication/report/report.pdf` |
| Formal report (LaTeX + PDF) | `report/1427646_replication_report.tex`, `report/1427646_replication_report.pdf` |
| Multislice data (64 frames) | `replication/multislice_data/` |
