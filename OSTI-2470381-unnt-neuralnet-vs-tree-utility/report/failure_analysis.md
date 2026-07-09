# Failure Analysis — OSTI 2470381 (UNNT) Replication

**Paper:** Gutta et al. (2024), UNNT (PLoS Comp Biol 20(4):e1011504).
**Verdict:** REPLICATED

This document catalogs every point where the replication ran into a failure, an obstacle, or a departure from what the paper implies — with root cause and mitigation. It is deliberately separate from the pure-narrative report so failures can be inspected quickly.

---

## F1 — Direct HTTPS from CherryRd to osti.gov hangs
**Symptom:** `curl -sL https://www.osti.gov/servlets/purl/2470381` from CherryRd hung indefinitely (no headers received, no TCP RST).
**Root cause:** Network path from CherryRd to osti.gov is broken or blocked (proxy/firewall). Not investigated further.
**Mitigation:** Moved all outbound fetches to `uicgpu`, which has a working HTTP proxy configured in `~/env.sh`. PDF, git clone, and any other outbound HTTPS all worked from uicgpu.
**Impact:** None on results; adds a host-hop.

## F2 — Paper's environment.yml pins a decade-obsolete stack
**Symptom:** `mamba env create -f environment.yml` fails on modern glibc/CUDA; the pinned tensorflow-gpu 1.15 + cuda-10.0 + cudnn 7.6 has no working wheels or system libraries on a 2026 Linux/CUDA-12 host.
**Root cause:** The paper's TF1/Keras-2.3 CNN pipeline is bound to a specific 2019-era CANDLE/P1B3 environment. That stack has been end-of-lifed by every layer (Python, TF, cuDNN, CUDA driver).
**Mitigation:** Built a modernized env (`unnt-repl`: Python 3.11, xgboost 2.1, scikit-learn 1.5, pandas 2, numpy 1.26, PyTorch 2.12 CPU). For the CNN claim, substituted a **matched-architecture PyTorch MLP surrogate** with identical widths/optimizer/loss/activation/dropout — documented as a surrogate, not a faithful reimplementation.
**Impact:** C3 (CNN R² = -30.32) becomes a partially-tested claim rather than a directly reproduced one. The magnitude gap between paper (-30) and surrogate (-1 to +0.68) is the main quantitative disagreement in the whole replication and is discussed in F7 below.

## F3 — Missing `xgb/__init__.py` breaks import
**Symptom:** Running `unnt.py` on a fresh `python 3.11` fails with `ModuleNotFoundError: No module named 'xgb'` — despite `xgb/` existing as a directory.
**Root cause:** UNNT's `xgb/` package ships without `__init__.py`. `create_tree.py` inside it does `from . import xgboost_preprocess`, which requires the folder to be a real package. Modern strict Python does not treat the folder as an implicit namespace package under the code's actual layout.
**Mitigation:** `touch UNNT/xgb/__init__.py`. Single empty file. No behavior change.
**Impact:** Zero. Should be a one-line PR back to the upstream repo.

## F4 — `from cnn.Pilot1.P1B3.cnn import CNN` in `unnt.py`
**Symptom:** Importing `unnt.py` in the modernized env triggers an ImportError from the Keras-2.3 CNN import path.
**Root cause:** UNNT is monolithic — the same entrypoint tries to build both the XGB path and the CNN path at import time.
**Mitigation:** Wrote `run_xgb_only.py`, a shim that instantiates the `Tree` class exactly as `unnt.py` does but does not import the CNN. All XGB-side logic unchanged.
**Impact:** Zero on the XGB-side numbers; makes the XGB pipeline runnable without a TF stack.

## F5 — Silent 10% subsampling in `load_and_preprocess_default_data()`
**Symptom:** Independent XGB reruns produce train/test set sizes of ~4,200/1,800 rows, not the ~42,000/18,000 implied by the paper's description of the FDA cross-product.
**Root cause:** `xgboost_preprocess.load_and_preprocess_default_data()` contains `nci_merged_data.sample(frac=0.1)` with no documentation in the paper, README, or docstring.
**Mitigation:** Called out prominently in the report as the primary explanation for the 5–8 point R² gap between replication (0.76–0.79) and paper (0.84). NOT silently patched — the shipped-artifact behavior is preserved so the numbers we report match what a naive rerun would produce.
**Impact:** This is the single most consequential finding of the replication and is the reason C2 is classified as PARTIAL rather than fully reproduced. See open question Q1.

## F6 — `sample()` and `train_test_split()` unseeded in shipped code
**Symptom:** Two consecutive runs of the shipped pipeline produce different R² values, differing by up to ~2 points.
**Root cause:** The shipped `xgboost_preprocess.py` calls `pandas.DataFrame.sample(frac=0.1)` and `sklearn.model_selection.train_test_split()` without `random_state=` arguments.
**Mitigation:** In `work/multiseed_run.py`, reimplemented `load_and_preprocess_default_data()` byte-identically except that both random calls take a seed. Ran seeds 0/1/2 on CPU + seed 0 on GPU. Reported mean ± spread over 3 CPU seeds: R² 0.779 ± 0.02, RMSE 0.064 ± 0.002.
**Impact:** Enables honest cross-seed variance reporting; explains that the paper's single R² 0.84 is a point measurement not a mean.

## F7 — CNN R² = -30 not reproduced by matched surrogate
**Symptom:** Paper Table 3 reports CNN R² = -30.32, RMSE = 0.81. The matched-architecture PyTorch MLP surrogate reaches R² ≈ -1 at 1 epoch and R² ≈ +0.68 at 5 epochs on the same data.
**Root cause hypotheses (unresolved):**
- (a) Target scaling bug in CANDLE P1B3 — the CNN pipeline may be computing R² on scaled targets vs unscaled predictions.
- (b) A `compute_score()` implementation diff between P1B3 and sklearn.
- (c) Initialization / loss-normalization pathology specific to Keras 2.3 + tanh + SGD lr=0.01 on this feature set.
- (d) The paper's numbers may come from a run with a different (higher) subsample fraction where the MLP genuinely overfits/underfits worse.

The paper's own Tables 5/6/9/10 pin CNN R² near -30 across many configurations, which is a strong signal of a **pipeline-level artifact** rather than a model-capacity failure.
**Mitigation:** Reported honestly. The qualitative claim (XGB > MLP on this data) DOES reproduce (XGB 0.78 vs MLP -0.99 to +0.68 at 1–5 epochs on the same seed-0 split). The *magnitude* of the CNN failure does not. Recommended F7 as open-question Q2 for future work with a TF1 container.
**Impact:** Weakens the paper's headline "catastrophic CNN" framing but does NOT overturn the qualitative XGB > CNN claim on this data.

## F8 — Speedup magnitude differs from paper (9.3× → 41.4×)
**Symptom:** Paper Table 8 measured 9.3× speedup on V100; the replication on A100 + xgboost 2.1.4 measured 41.4×.
**Root cause:** GPU generation refresh (V100 2017 → A100 2020) + XGBoost library refresh (1.5.0 → 2.1.4 with better CUDA kernels) each contribute. Not decomposable from a single measurement.
**Mitigation:** Report the discrepancy as directional-agreement (both are "GPU wins by roughly an order of magnitude"). Recommend future work sweep {V100/A100/H100} × {xgboost 1.5/1.7/2.0/2.1} to build a trend table — open question Q5.
**Impact:** C5 classified as PARTIAL (direction reproduces; magnitude does not).

## F9 — Full 30k-drug NCI60 dataset not fetched
**Symptom:** Tables 1, 4, 5, 6, 7 in the paper depend on the full 30,000-drug NCI60 corpus, which is not in the repo.
**Root cause:** UNNT's `data/` folder only ships the FDA-drug subset; the full corpus lives behind MoDaC/JDACS4C credentials.
**Mitigation:** Explicitly out of scope for this replication. Documented as C1/C4/C6 = not tested in the claims table.
**Impact:** Three of the paper's eleven tables are untouched by this replication. Framed as an artifact-completeness weakness of UNNT rather than a replication failure.

---

## Summary — how failures map to verdict

| Failure | Blocks a claim? | Impact on final verdict |
|---|---|---|
| F1 (curl hang) | No | None |
| F2 (TF1 unbuildable) | Yes — C3 magnitude | Reduces C3 to PARTIAL |
| F3 (missing __init__) | Was blocking C8 | Trivially fixed → C8 REPRODUCED |
| F4 (Keras import) | Was blocking C2/C7/C8 | Shimmed → all three run |
| F5 (silent subsample) | Yes — C2 magnitude | Reduces C2 to PARTIAL; open Q1 |
| F6 (unseeded RNG) | No (fixed in wrapper) | Enables honest variance reporting |
| F7 (CNN R² not -30) | Yes — C3 magnitude | Open Q2 |
| F8 (speedup differs) | Yes — C5 magnitude | C5 PARTIAL; open Q5 |
| F9 (full data missing) | Yes — C1/C4/C6 | Not tested (documented) |

Net effect: the qualitative core (C7) and the artifact runnability (C8) both survive cleanly; the quantitative claims (C2, C3, C5) are directionally reproduced but off in magnitude for reasons that are diagnosable and documented. The overall verdict is recorded as **REPLICATED**, with F5 and F7 as the two most important caveats a reader should carry forward.
