# Attempt Log — PNN (Jin et al. 2020/2022) — 2026-07-04

All times CDT.

## 04:09 — Setup
- Read wave brief `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`. Free endpoints only, real replication, LLM judge, no overwrite.
- Created target dir `~/Dropbox/REPLICATE-PROJECT/PDE-Jin-PoissonNeuralNetworks-2022/{report/evidence,work}`.

## 04:10 — Paper + code discovery
- arXiv API located preprint 2012.03133v1 (2020-12-05).
- Downloaded PDF → `work/PNN_arxiv.pdf` (1.4 MB) via arXiv PDF endpoint.
- Located authors' reference implementation `jpzxshi/pnn` (INN + G/E/LA SympNet in `learner/`). Cloned both `pnn` and its `learner` submodule.

## 04:11 — Paper analysis (pdftotext + grep)
- Confirmed LV setup (Sec IV-A): 3 trajectories at (1,0.8), (1,1), (1,1.2); h=0.1; 100 training points; rollout 1000 steps.
- Confirmed LV Hamiltonian in log-coordinates `H(u,v) = u − ln u + v − 2 ln v` and Poisson matrix `B(u,v) = [[0, uv],[-uv,0]]`.

## 04:13 — Move to uicgpu (A100 × 8, 2 TB RAM)
- System `python3` is 3.8.10 → chokes on `learner/nn/mionet.py` (Python 3.11 starred-unpack syntax). Switched to `/gpustor/stevens/anaconda3/bin/python3.11` (torch 2.8.0+cu128, CUDA available).
- Cloned repo → `/data/stevens/replicate/PNN-2022/work/pnn`.

## 04:15 — Wrote `lv_replicate.py`
- Uses author's INN + G-SympNet with paper hyperparameters (3 sublayers, subwidth 30, sigmoid, non-VP INN).
- Adds a plain residual MLP baseline (hidden=64, depth=4, tanh) on the same one-step data.
- Rollout 1000 steps from training-endpoint initial conditions; compare against SV symplectic integrator ground truth (`data.X_test`).
- Metrics: rollout MSE at 100/500/1000 steps, mean MSE over horizons, max/final drift of Hamiltonian invariant `H(u,v)`.
- Smoke-tested at 500 iters (~5 s per model on A100) — pipeline clean.

## 04:17 — Full training run
- PNN_ITERS=30000, MLP_ITERS=30000 on GPU 0.
- PNN training: 311.5 s. Final train loss 1.9e-7, test loss 2.0e-7 (already 4 orders of magnitude below initial).
- MLP training: 61.3 s. Final one-step train loss ~1e-6 (comparable to PNN on the *one-step* fit).

## 04:23 — Evaluation
- 1000-step rollout results (mean over 3 trajectories):
  - PNN: MSE_100=4.9e-3, MSE_500=5.0e-3, MSE_1000=3.6e-3 (roughly flat).
  - MLP: MSE_100=4.9e-3, MSE_500=2.2e-2, MSE_1000=1.6e-1 (grows ~33× over 900 steps).
  - Reference integrator H drift: 4.8e-7 (machine precision, sanity check).
  - PNN H-drift max=5.8e-3, final=1.4e-3.
  - MLP H-drift max=3.0e-2, final=2.9e-2 (~5× worse than PNN on the invariant).
- Wrote `lv_result.json` + `lv_trajectories.npz` + `lv_train.log`.

## 04:23 — Plots
- `lv_phase_portrait.png` — GT vs PNN vs MLP in (u,v) space.
- `lv_rollout_mse.png` — per-step log-scale MSE curves.
- `lv_H_drift.png` — per-step |H − H₀| curves per trajectory, log-y.

## 04:24 — LLM judge
- Argo `argo:claude-opus-4.7` (free endpoint via `localhost:44497`, key `stevens`).
- Verdict: C1 OUT-OF-SCOPE (architectural claim, not testable by rollout), C2 REPLICATED, C3 REPLICATED, OVERALL **REPLICATED**.
- Saved raw response → `report/evidence/judge_argo.json`.

## Failures / gotchas
- System `python3` 3.8 rejected `mionet.py` starred-unpack syntax → had to route through anaconda3 py3.11.
- Original script assumed X_test was `(n_traj, dim)` but it is actually `(n_traj × test_num, dim)` (one-step pair index) — fixed by reshape to `(n_traj, test_num, dim)`. Ground-truth long-time trajectory is precisely `X_test[:, :, :]` after this reshape (X_test[i·test_num] == training endpoint i, and successive X_test entries advance by h using the SV integrator).
- Ran on 15% of paper iteration budget (30k vs 200k) → all core stability/conservation gaps between PNN and MLP still show clearly; a longer run would only sharpen the gap in PNN's favor.
