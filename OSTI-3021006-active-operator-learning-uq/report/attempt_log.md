# Attempt Log — OSTI 3021006

## 2026-07-04

- 22:xx — Downloaded paper PDF from OSTI 3021006 → `work/paper.pdf` (14MB).
- 22:xx — Wrote `repro.py`: FNO-2d backbone (spectral conv, modes=10, width=24) + mean head + logvar head; NLL loss (paper Eq. 1); 2D advection–diffusion FD solver (upwind + centered diffusion, forward Euler on 48×32×21 grid, T=0.7, kappa=0.01); active-learning loop with variance-based acquisition vs random baseline.
- 23:07 — Launched full run on uicgpu (`~/osti_3021006_repro/full/`) with args: n_pool=500, n_test=150, n0=60, n_rounds=6, add_per_round=30, n_trials=3, epochs=250, batch=16, lr=2e-3, seed=20260704 → PyTorch 1.11.0 on NVIDIA A100 80GB PCIe.
- 23:28 — Full run **finished cleanly** (21 min wall). Wrote `final_summary.json`, `al_curves.csv`, `al_curves.png`, `run_metadata.json`, `X_pool/Y_pool/X_test/Y_test.npy`.
- 23:28 — Driver subagent that had spawned the run **ran out of turn budget before writing the report**. Numbers already on disk.
- 23:28 (this session, finisher subagent) — SSH'd uicgpu, pulled `final_summary.json`, `run_metadata.json`, `al_curves.csv`, `al_curves.png` to `report/evidence/`; pulled `repro.py` to `work/repro.py`. Wrote report suite. Ran LLM judge via Argo :44497.

## What worked
- Direct SSH + scp from uicgpu to Dropbox target dir — no re-run needed, numbers are the real trained-model outputs from the completed 3-trial × 7-training-size sweep.
- Real PDE data (no fabrication): pool + test tensors saved as `.npy` on uicgpu; final metric = L2 relative error on held-out 150 solutions.
- 3 independent trials → std bars printed alongside median/mean.

## What didn't (scope caveats)
- Grid smaller than paper (48×32 vs ~96×64), pool smaller (500 vs paper's larger dataset), and only 6 AL rounds — so absolute L2 numbers and the "improvement %" are not directly comparable to paper Table 3–4.
- Only C1 (AL efficiency) tested; the paper's other UQ-calibration claims (e.g., CRPS scores, coverage curves) were not re-run.
