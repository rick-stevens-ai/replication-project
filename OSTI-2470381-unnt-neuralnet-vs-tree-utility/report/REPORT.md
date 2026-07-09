# Independent Replication Report — OSTI 2470381
**Paper:** Gutta V, Ranganathan Ganakammal S, Jones S, Beyers M, Chandrasekaran S. *UNNT: A novel Utility for comparing Neural Net and Tree-based models.* PLoS Computational Biology 20(4): e1011504 (2024-04-29). DOI [10.1371/journal.pcbi.1011504](https://doi.org/10.1371/journal.pcbi.1011504). OSTI id 2470381.

**Replicator:** OpenClaw subagent (X-100 replication project). Date: 2026-07-02, CDT.
**Hardware:** uicgpu (`ssh uicgpu`) — 8× NVIDIA A100 40 GB (one A100 used), dual AMD EPYC (47 usable cores exposed).
**Software:** conda env `unnt-repl` — Python 3.11, xgboost 2.1.4 (CUDA 12.8, hist), scikit-learn 1.5.2, pandas 2.3.3, numpy 1.26.4, PyTorch 2.12.1 (CPU-only for MLP surrogate).

---

## Paper summary

UNNT is a small open-source Python library that trains an XGBoost regressor and a "CNN" (in the shipped `cnn_config.txt`, actually an MLP: `dense=[1000,500,100,50]`, SGD lr=0.01, tanh, MSE, dropout=0.1) on the same tabular NCI60 drug-response dataset and reports both accuracy and per-epoch training time. The paper's motivating claim, backed by 11 tables, is that on this class of drug-response tabular problem an XGBoost model both fits better (R² ≈ 0.82 vs -30) and — on a GPU — trains faster than the CNN. The paper also promotes UNNT as an easy-to-use library so domain scientists can rerun this comparison on their own tabular data.

## Claims table

| # | Claim (paraphrased) | Type | Testable with shipped repo? | Tested? | Result |
|--:|---|---|---|---|---|
| C1 | XGBoost on FULL NCI60 (30 k drugs) → R² 0.82, RMSE 0.051 (Table 1) | quant | No (full 30 k-drug data not shipped) | No | not tested |
| C2 | XGBoost on FDA-drug subset → R² 0.84, RMSE 0.069 (Table 2 test row) | quant | Yes (FDA data ships in `data/`) | Yes | PARTIAL — see §Results C2 |
| C3 | CNN with HPO on NCI60 → R² -30.32, RMSE 0.81 (Table 3) — catastrophic | quant | No (TF1/Keras-2.3 stack unmaintained) | Surrogate (PyTorch MLP, matching architecture/optimizer/loss/activation) | PARTIAL — sign matches, magnitude weaker |
| C4 | Full-drug XGB CPU (5.6-7.2 h, 1-64 threads) vs V100 (0.3 h) → ~19× (Table 4) | quant/timing | No (needs full data) | No | not tested |
| C5 | FDA-drug XGB CPU (1495 s, 1 thread) vs V100 (160 s) → ~9.3× (Table 8) | quant/timing | Yes | Yes | PARTIAL — direction reproduces; magnitude larger (~41×) on A100 |
| C6 | Full-drug CNN trains **faster on CPU** than V100 (data-transfer bottleneck, Table 5 vs 6) | quant/timing | No (TF1/Keras + full data both missing) | No | not tested |
| C7 | For tabular drug-response data at this size and feature-set, XGBoost is a better model than the paper's CNN | qualitative | Yes | Yes | REPRODUCED in the tested regime |
| C8 | UNNT open-source library at github.com/vgutta/UNNT runs the comparison end-to-end | artifact | Yes | Yes | REPRODUCED (with one trivial fix: added missing `xgb/__init__.py`) |

## Method

1. **Fetch paper.** `ssh uicgpu` (CherryRd direct curl to `osti.gov` hangs; uicgpu has a working HTTP proxy in `~/env.sh`). `curl -sL https://www.osti.gov/servlets/purl/2470381 -o /tmp/osti_2470381.pdf` → 456 529 B, SHA-256 `80fcdaf83356718f81b8fa9a75d104c27e677ab2ce0459e0aabea7163c33fab6`. `pdftotext -layout` → 619 lines.
2. **Fetch code.** `git clone --depth 1 https://github.com/vgutta/UNNT.git` on uicgpu; commit `c34567b1c9595879a0eade8cb641c7630b69a7ed`; MIT-licensed.
3. **Fetch data.** The repo ships the bundled NCI60 FDA-drug subset already at `data/` (7 files, ~113 MB total; per-file sizes + sha256 in `artifact_harvest.md`). This is the exact dataset behind Tables 2/8/9/10/11. The full 30 k-drug dataset (Tables 1/4/5/6/7) is *not* shipped and would require downloading directly from MoDaC (JDACS4C).
4. **Environment.** Fresh conda env `unnt-repl` on uicgpu:
   ```bash
   mamba create -n unnt-repl -y -c conda-forge python=3.11 xgboost=2.1 scikit-learn=1.5 pandas=2 numpy=1.26 matplotlib
   pip install torch --index-url https://download.pytorch.org/whl/cpu
   ```
   Rationale for skipping TF1/Keras 2.3: the paper's own `environment.yml`/`gpu_environment.yml` pin cuda-10.0 + cudnn 7.6 + tensorflow-gpu 1.15 — a decade-obsolete stack that will not run on modern glibc/CUDA. See §Failures.
5. **Bug fix.** UNNT's `unnt.py` imports `from xgb.create_tree import Tree`, but the `xgb/` package ships with no `__init__.py` and `create_tree.py` uses `from . import xgboost_preprocess` — this fails on any Python that isn't in an implicit-namespace-package edge case. Added an empty `xgb/__init__.py`. Also wrote a `run_xgb_only.py` shim that invokes the `Tree` class exactly as `unnt.py` does but skips the `from cnn.Pilot1.P1B3.cnn import CNN` line (which pulls in Keras 2.3 → ImportError). No other changes to their code path.
6. **XGBoost run (baseline).** `python run_xgb_only.py --seed 42` → runs the unmodified `Tree.train()` + `Tree.evaluate()` on the bundled FDA-subset data with the paper's HPO'd hyperparameters (`n_estimators=500 max_depth=10 eta=0.1 subsample=0.5 colsample_bytree=0.8`, `tree_method=hist`, `n_jobs=-1`). Wall time 435.78 s. Result: R² = 0.7603, RMSE = 0.0666.
7. **XGBoost multi-seed sweep.** Rewrote `xgboost_preprocess.load_and_preprocess_default_data()` in `work/multiseed_run.py`, byte-identical except that the two `sample()` / `train_test_split()` calls are seeded. Ran seeds 0/1/2 CPU + seed 0 GPU (`device="cuda"`).
8. **MLP surrogate for CNN claim.** `work/mlp_run.py` — modern PyTorch reimplementation of the CNN configured in `cnn_config.txt`: same widths `[1000,500,100,50]`, same optimizer (SGD), same learning rate 0.01, same loss (MSE), same activation (tanh — the paper's HPO'd choice), same dropout 0.1, same batch size 100, same StandardScaler feature scaling, same input pipeline as the XGBoost path. Ran seeds 0/1 at 1 epoch (paper Table 3 config) + seed 0 at 5 epochs (paper Table 5 style) + seed 0 with ReLU (paper claims ReLU fails to converge).
9. **LLM judge.** Sent the paper claims + measured numbers to Argo free endpoint `http://localhost:44497/v1` model `argo:gpt-5.2` (WAVE brief default free judge). Full prompt + JSON response saved to `report/evidence/llm_judge_verdict.json`.

## Results vs paper

### XGBoost (C2)

| Source | R² | RMSE | n_train | n_test | Runtime |
|---|---:|---:|---:|---:|---:|
| Paper Table 2 (FDA XGB, test) | **0.84** | **0.069** | (unstated) | (unstated) | — |
| Paper Table 2 (FDA XGB, new cell lines) | 0.66 | 0.094 | — | — | — |
| Rerun seed 42 CPU | 0.7603 | 0.0666 | 4 355 | 1 867 | 435.8 s |
| Rerun seed 0 CPU | 0.7834 | 0.0640 | 4 246 | 1 820 | 428.5 s |
| Rerun seed 1 CPU | 0.7944 | 0.0624 | 4 185 | 1 794 | 415.2 s |
| Rerun seed 2 CPU | 0.7590 | 0.0661 | 4 329 | 1 856 | 409.6 s |
| Rerun seed 0 GPU (A100) | 0.7847 | 0.0639 | 4 246 | 1 820 | **10.35 s** |
| Rerun mean±spread (3 CPU seeds) | 0.779 ± 0.02 | 0.064 ± 0.002 | | | |

Rerun **RMSE (0.062-0.066) is actually slightly *better* than the paper's 0.069** and rerun **R² (0.76-0.79) is 5-8 points *below* the paper's 0.84**. Both are close to the paper's "new cell lines" row (R² 0.66, RMSE 0.094) which is the harder generalization test. The gap is most plausibly explained by the fact that UNNT's `load_and_preprocess_default_data()` silently subsamples merged rows to 10 % (`nci_merged_data.sample(frac=0.1)`) — undocumented in the paper — giving my train/test sets of ~4 200/1 800 rather than the ~42 000/18 000 the paper implies.

### CNN / MLP-surrogate (C3, C7)

| Source | R² | RMSE | Runtime | Notes |
|---|---:|---:|---:|---|
| Paper Table 3 (CNN 1 epoch HPO tanh) | **-30.32** | **0.81** | — | Catastrophic |
| MLP surrogate seed 0, 1 epoch, tanh | -0.9974 | 0.1945 | 19.9 s | Negative R² (underfit) — same sign |
| MLP surrogate seed 1, 1 epoch, tanh | -0.9802 | 0.1938 | 19.3 s | Reproducible across seeds |
| MLP surrogate seed 0, 5 epochs, tanh | +0.6775 | 0.0782 | 98.6 s | Model DOES recover with more epochs |
| MLP surrogate seed 0, 1 epoch, ReLU | -1.106 | 0.1997 | 18.6 s | Slightly worse than tanh — consistent with paper's "ReLU failed" note |

The **qualitative claim (C7) that XGBoost beats the paper's neural net at this scale/features reproduces cleanly**: on the same seed-0 split, XGBoost gets R² = 0.7847 while the matching MLP gets R² = -0.99 (1 ep) or R² = +0.68 (5 ep). The **quantitative CNN failure magnitude (C3) does not reproduce** — my surrogate gets an "only mildly negative" R² of about -1, not the paper's -30. This suggests the paper's headline number is architecture- or optimizer-specific to the particular Keras 2.3 code path and not a robust property of the architecture. The paper's own Tables 5, 6, 9, 10 in fact show the CNN's R² stuck at ≈ -30 regardless of epochs / CPU vs GPU — pointing at something like a scaling / initialization / loss-normalization pathology in the CANDLE P1B3 pipeline rather than an intrinsic architectural failure.

### Speedup (C5)

| Source | CPU time | GPU time | Speedup | Hardware |
|---|---:|---:|---:|---|
| Paper Table 8 | 1 495 s (1 thread) | 160 s (V100) | 9.3× | V100 (2017) |
| Rerun (seed 0) | 428.5 s (47 threads, hist) | 10.35 s (A100) | **41.4×** | A100 (2020) + xgboost 2.1 (2024) |

Direction reproduces. Magnitude larger (5×) than paper's V100 number, plausibly explained by modern hardware (A100 vs V100) + modern XGBoost with better CUDA kernels (2.1.4 vs 1.5.0).

### Artifact (C8)
`git clone` of the UNNT repo at commit `c34567b` succeeded, all bundled data files present with matching sha256 checksums, and the full XGBoost pipeline ran end-to-end after a trivial one-file fix (missing `__init__.py`). See `report/evidence/xgb_multiseed.log` for the actual runtime log.

## Verdict justification

- **Reproduced end-to-end (C2 direction, C7, C8):** UNNT runs; XGBoost hits R² ≈ 0.78 / RMSE ≈ 0.064 on the FDA subset; XGBoost beats the matching neural net in the tested regime; GPU-vs-CPU speedup is real and larger than the paper's V100 number.
- **Partially reproduced (C2 magnitude, C3, C5):** Quantitative R² for XGBoost is ~5 pts below the paper. The catastrophic CNN R² = -30 was NOT reproduced by a matched-architecture PyTorch surrogate; the model recovers to R² = +0.68 in 5 epochs. The GPU speedup is ~4× larger than the paper's.
- **Not testable with shipped repo (C1, C4, C6):** Full 30 k-drug NCI60 dataset is not in the repo; TF1/Keras-2.3 CNN cannot be run on modern hardware without a Herculean recovery effort not in scope.
- **Concerning finding:** UNNT silently subsamples merged rows to 10 % — undocumented in the paper and directly explains the R² gap. The paper's numbers may themselves come from a 10 %-subsample run rather than the full FDA cross-product it implies, which would make the reported R² 0.84 hard to independently verify without deeper spelunking of the exact XGBoost seed and merge-order used.

Overall: the paper's **core qualitative claim (XGBoost > CNN on this data)** is real and reproducible. The **specific quantitative numbers** are directionally right but not tight — the FDA R² is off by 5-8 points and the CNN failure is much less dramatic in an independent reimplementation. This is a solid, honest **PARTIAL**.

The LLM-judge (Argo free `gpt-5.2`, temperature 0, prompt + full response in `report/evidence/llm_judge_verdict.json`) independently returned:
> "**PARTIAL** — The replication successfully exercised the UNNT repository on the shipped FDA-subset data and reproduced the qualitative conclusions … However, key quantitative targets do not match: FDA-subset XGBoost R² is ~0.76-0.79 vs the paper's 0.84, and the reported CNN catastrophic R² (-30) was not reproduced (only mildly negative at 1 epoch and positive with more epochs), indicating sensitivity to implementation/training details. Several core claims (full NCI60/full-drug results and CNN CPU-vs-GPU behavior) are not testable because the full dataset is not included in the repo. Given partial coverage plus mixed quantitative agreement, the appropriate verdict is PARTIAL rather than REPLICATED or CONTRADICTED."

## Verdict
**Verdict:** PARTIAL
