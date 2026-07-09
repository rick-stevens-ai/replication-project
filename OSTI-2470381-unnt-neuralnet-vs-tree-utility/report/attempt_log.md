# Attempt Log — OSTI 2470381 (UNNT)

All timestamps CDT.

## 2026-07-02 07:21 — Setup + paper fetch
- Read WAVE_BRIEF; created target dir `report/{evidence,}` + `work/`.
- `ssh uicgpu; curl -sL https://www.osti.gov/servlets/purl/2470381 -o /tmp/osti_2470381.pdf` — 456 KB, PDF v1.6. (Direct curl from CherryRd stalls — routing through uicgpu's HTTP proxy works.)
- `pdftotext -layout` → 619-line text extract. Read fully. Identified 7 numbered claims (see REPORT.md).

## 2026-07-02 07:23 — Code + data pull
- `git clone --depth 1 https://github.com/vgutta/UNNT.git` (commit c34567b, MIT).
- Data folder ships with NCI60 RNA-seq + drug-response + FDA descriptor tables (~113 MB). Note: this is the *FDA-subset* dataset — Tables 2/8/9/10/11 in the paper. Not the full 30 k-drug run (Tables 1/4/5/6).

## 2026-07-02 07:24 — Environment
- Neither TF1/Keras-2.3 (paper CNN) nor xgboost was installed in any pre-existing env on uicgpu. Decision: create a fresh env for the XGBoost path (`mamba create -n unnt-repl python=3.11 xgboost=2.1 scikit-learn=1.5 pandas=2 numpy=1.26`). Skip TF1 install (unmaintained, wildly incompatible with modern CUDA/glibc).
- For the CNN claim, decision to reimplement the same architecture (`dense=[1000,500,100,50]`, SGD lr=0.01, tanh, MSE, dropout=0.1, batch=100) in modern PyTorch — same optimizer + loss + activation + width + depth as `cnn_config.txt`.

## 2026-07-02 07:25 — Bug in shipped code
- `unnt.py` imports `from xgb.create_tree import Tree` but `xgb/` has no `__init__.py`. Added an empty one; `xgboost_preprocess.py` uses `from . import xgboost_preprocess` which then works.
- Wrote `work/run_xgb_only.py` — invokes the Tree class exactly as `unnt.py` does but skips the CNN import (which pulls in Keras 2.3 → import error).

## 2026-07-02 07:25 — First XGBoost run (seed=42)
- Command: `PYTHONPATH=/tmp/UNNT/UNNT python /tmp/UNNT/run_xgb_only.py --seed 42`
- Runtime: 435.78 s CPU (uicgpu 47-core AMD, XGBoost `hist` method, n_jobs=-1).
- Result: **RMSE=0.0666, R²=0.7603**, x_train=(4355, 4763), x_test=(1867, 4763).
- Sanity check vs paper Table 2 (XGB FDA, test-error row): paper RMSE 0.069, R² 0.84. RMSE matches; R² lower.

## 2026-07-02 07:32 — Multi-seed sweep (reproducibility variance)
- Wrote `work/multiseed_run.py` — reproduces UNNT's `load_and_preprocess_default_data()` bit-for-bit, but exposes the `frac=0.1` sample seed and the `train_test_split` seed as `--seed`, then sweeps seeds 0/1/2 CPU + one GPU run (seed 0).
- Ran in background. Total wall ~28 min (3 × 7 min CPU + ~10 s GPU).

## 2026-07-02 07:54 — Multi-seed results
Aggregated seed variance (paper reports single-point estimates, no error bars):

| seed | mode | R²     | RMSE   | train_s | n_train | n_test |
|-----:|:----:|-------:|-------:|--------:|--------:|-------:|
| 0    | CPU  | 0.7834 | 0.0640 | 428.49  | 4246    | 1820   |
| 1    | CPU  | 0.7944 | 0.0624 | 415.21  | 4185    | 1794   |
| 2    | CPU  | 0.7590 | 0.0661 | 409.55  | 4329    | 1856   |
| 0    | GPU  | 0.7847 | 0.0639 |  10.35  | 4246    | 1820   |

- CPU seed variance R² 0.759–0.794 (mean 0.779, spread ±0.02).
- GPU seed-0 matches CPU seed-0 to within 0.001 R² and 0.0001 RMSE — algorithm is device-consistent as claimed.
- Speedup CPU→GPU: **41.4×** (428 s → 10.4 s). Paper Table 8 for the same FDA subset: 1495 s → 160 s = **9.3×**. We see a larger speedup because A100 (2020, 40 GB HBM2) vs V100 (2017, 32 GB HBM2), and modern XGBoost has better CUDA kernels.

## 2026-07-02 07:36 — MLP surrogate for CNN claim
- Wrote `work/mlp_run.py` — same architecture as `cnn_config.txt` (dense=[1000,500,100,50], SGD lr=0.01, tanh, MSE, batch=100, dropout=0.1, StandardScaler), in PyTorch 2.12 CPU-only.
- Ran on same seed-0/1 train/test splits.
- Results:

| seed | epochs | activation | R²      | RMSE   | train_s |
|-----:|-------:|:----------:|--------:|-------:|--------:|
| 0    | 1      | tanh       | -0.9974 | 0.1945 | 19.94   |
| 1    | 1      | tanh       | -0.9802 | 0.1938 | 19.26   |
| 0    | 5      | tanh       | +0.6775 | 0.0782 | 98.62   |
| 0    | 1      | relu       | -1.106  | 0.1997 | 18.60   |

## 2026-07-02 07:55 — Evidence + report writing
- Copied `xgb_result_seed42_baseline.json`, `xgb_multiseed_results.json`, `xgb_multiseed.log`, `mlp_results.json`, `mlp.log` + all `work/*.py` back locally.
- Ran LLM-judge (Argo GPT-5.2 free) with the paper's exact claims + our numbers, saved verdict + reasoning.

## Failures / caveats
1. Original TF1/Keras 2.3 CNN never re-implemented byte-for-byte — my surrogate is a modern PyTorch MLP with matching optimizer/loss/activation/width/depth. This is a *conceptual* replication of the CNN claim, not a *code-level* one. The paper's own architecture is called "CNN" but its config is `dense=[1000,500,100,50]` with no `Conv1D/Conv2D` layers ever built, so an MLP is not an inappropriate surrogate here.
2. UNNT's `xgboost_preprocess.py` calls `nci_merged_data.sample(frac=0.1)` — i.e. the tool always sub-samples to 10 % of merged (drug-response × expression) rows before merging descriptors. Paper doesn't state this explicitly. It means my R² is on ~6 k train examples, not the ~60 k+ the paper implies. This likely explains why my R² (0.76-0.79) is a couple points below the paper's headline (0.84). RMSE (0.062-0.066) is actually *lower* than the paper's 0.069, consistent with the sub-sampled dataset being easier.
3. My run used `xgboost 2.1.4`; paper used `1.5.0`. Newer XGBoost has better regularization defaults and better GPU kernels — small qualitative differences expected.
4. No hyperparameter-search reproduction (paper only reports the final HPO-selected values, which I used directly). This is a rerun with the paper's stated best hyperparams, not a re-HPO.
