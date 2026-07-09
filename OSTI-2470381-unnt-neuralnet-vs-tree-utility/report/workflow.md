# Replication Workflow — OSTI 2470381 (UNNT)

**Paper:** Gutta et al. (2024), UNNT: A novel Utility for comparing Neural Net and Tree-based models. PLoS Comp Biol 20(4):e1011504.
**Verdict:** REPLICATED
**Execution host:** `uicgpu` (8× NVIDIA A100 40 GB, dual AMD EPYC, 47 usable cores)
**Env:** conda `unnt-repl` — Python 3.11, xgboost 2.1.4 (CUDA 12.8, hist), scikit-learn 1.5.2, pandas 2.3.3, numpy 1.26.4, PyTorch 2.12.1 (CPU-only for MLP surrogate)

---

## Stage 0 — Access & network
1. From CherryRd, `ssh uicgpu`. Direct `curl` from CherryRd to `osti.gov` hangs — uicgpu has a working HTTP proxy in `~/env.sh`. All fetches were done from uicgpu.
2. Source `~/env.sh` on uicgpu to pick up the proxy for outbound HTTPS.

## Stage 1 — Fetch paper
```bash
curl -sL https://www.osti.gov/servlets/purl/2470381 -o /tmp/osti_2470381.pdf
# 456,529 B, SHA-256 80fcdaf83356718f81b8fa9a75d104c27e677ab2ce0459e0aabea7163c33fab6
pdftotext -layout /tmp/osti_2470381.pdf /tmp/osti_2470381.txt  # 619 lines
```

## Stage 2 — Fetch code
```bash
git clone --depth 1 https://github.com/vgutta/UNNT.git
# HEAD c34567b1c9595879a0eade8cb641c7630b69a7ed, MIT license
```

## Stage 3 — Fetch data
The repo already ships the bundled NCI60 FDA-drug subset at `data/` (7 files, ~113 MB total). This is exactly the dataset behind paper Tables 2/8/9/10/11. Per-file sizes and sha256 checksums are recorded in `artifact_harvest.md`. The full 30k-drug NCI60 dataset (Tables 1/4/5/6/7) is **not** shipped and would require MoDaC/JDACS4C credentials — deliberately out of scope for this replication.

## Stage 4 — Build environment
```bash
mamba create -n unnt-repl -y -c conda-forge \
  python=3.11 xgboost=2.1 scikit-learn=1.5 pandas=2 numpy=1.26 matplotlib
mamba activate unnt-repl
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

Rationale: the paper's `environment.yml` / `gpu_environment.yml` pin cuda-10.0 + cudnn 7.6 + tensorflow-gpu 1.15 — a decade-obsolete stack unbuildable on modern glibc/CUDA. Modernized deliberately.

## Stage 5 — One-line source fix
UNNT's `unnt.py` imports `from xgb.create_tree import Tree`, but `xgb/` ships with no `__init__.py`. Fix:
```bash
touch UNNT/xgb/__init__.py
```
Also wrote a `run_xgb_only.py` shim that instantiates the `Tree` class exactly as `unnt.py` does but skips the `from cnn.Pilot1.P1B3.cnn import CNN` import (which pulls in Keras 2.3 → ImportError). **No other code changes** to the upstream XGBoost path.

## Stage 6 — XGBoost baseline
```bash
python run_xgb_only.py --seed 42
# Wall time 435.78 s → R² 0.7603, RMSE 0.0666
```
Uses the paper's HPO'd hyperparameters (n_estimators=500, max_depth=10, eta=0.1, subsample=0.5, colsample_bytree=0.8, tree_method=hist, n_jobs=-1).

## Stage 7 — XGBoost multi-seed sweep
`work/multiseed_run.py` — byte-identical to `xgboost_preprocess.load_and_preprocess_default_data()` except the two `sample()` / `train_test_split()` calls are seeded. Ran:
- seed 0, 1, 2 on CPU (47 threads, `tree_method=hist`)
- seed 0 on GPU (`device="cuda"`, A100)

Results captured in `report/evidence/xgb_multiseed.log`.

## Stage 8 — MLP surrogate for CNN claim
`work/mlp_run.py` — matched-architecture PyTorch MLP reimplementing `cnn_config.txt`:
- Widths: `[1000, 500, 100, 50]`
- Optimizer: SGD lr=0.01
- Loss: MSE
- Activation: tanh (paper's HPO'd choice; ReLU also swept)
- Dropout: 0.1
- Batch: 100
- Same StandardScaler feature scaling and same input pipeline as the XGB path

Runs:
- seed 0, 1 at 1 epoch, tanh (paper Table 3 config)
- seed 0 at 5 epochs, tanh (paper Table 5 style)
- seed 0 at 1 epoch, ReLU (paper claims ReLU fails to converge)

## Stage 9 — LLM judge
Sent claims + measured numbers to Argo free endpoint `http://localhost:44497/v1`, model `argo:gpt-5.2` (WAVE brief default free judge). Prompt + JSON response archived at `report/evidence/llm_judge_verdict.json`.

## Stage 10 — Report writing
Composed:
- `report/REPORT.md` (canonical narrative)
- `report/REPORT.tex` (LaTeX with dedicated Genuine Critique section)
- `report/open_questions.json` (5 truly-open follow-up questions)
- `report/workflow.md` (this file)
- `report/artifacts_summary.md` (artifact inventory)
- `report/failure_analysis.md` (what did not work and why)

## Cross-cutting decisions
- **Single writer per file**, resume-only where possible; preserved seeds for every random operation.
- **Modernized stack over faithful stack**, on grounds that the TF1/Keras-2.3 stack is unrunnable on modern hardware — used a matched-architecture PyTorch surrogate for the CNN claim, and disclosed this prominently.
- **Free-tier compute only** (uicgpu A100, Argo `gpt-5.2`). No paid API calls made.
- **Documentation over silent workaround** — the undocumented 10% subsample discovered in `load_and_preprocess_default_data()` is called out as the primary quantitative-gap explanation rather than being silently corrected away.
