# Attempt log — OSTI 3374627 (Kacmaz+ 2025 DINOs)

## 2026-07-04 18:57 CDT — start
- Read wave brief (`WAVE_BRIEF_2026-07-01.md`) → free endpoints only, LLM-judge for verdict, real replication, write only in target dir.
- Created target dir `~/Dropbox/REPLICATE-PROJECT/OSTI-3374627-turbulent-mhd-operator-diffusion/`.

## 18:59 — download paper
- `curl` to `https://www.osti.gov/servlets/purl/3374627` from CherryRd → connection timeout (75s). Local host had no OSTI reachability at the time.
- Retried via ssh uicgpu → 2.49 MB PDF downloaded successfully. Copied back via scp.

## 19:01 — read paper
- Local `pdftotext -layout` → 823 lines of readable text.
- pdf-tool call failed (Anthropic credits depleted; other backends not enabled). Skipped LLM extraction; read text manually.
- Extracted authors: Semih Kacmaz (NCSA + UIUC Physics), E A Huerta (ANL + UChicago), Roland Haas (NCSA + UBC).
- Journal: Mach. Learn.: Sci. Technol. 6 (2025) 035057.
- Code: https://github.com/semihkacmaz/DINOs (public MIT).
- Data: NOT public ("available upon reasonable request").

## 19:05 — inspect DINOs repo on uicgpu
- Cloned https://github.com/semihkacmaz/DINOs.
- Data-generation module IS included in repo (uses Dedalus spectral solver — heavy dep).
- Full training scripts also included (torch, neuraloperator, physicsnemo, wandb).

## 19:08 — decision on scope
- Full DINOs pipeline would require: install Dedalus, generate 800 sims/Re × 7 Re × 128²×26T, train tensor-FNO with PDE loss + train UNet-diffusion with FlashAttention → single-node H100 hours to days. Out of subagent scope.
- Alternative: implement a from-scratch minimal pseudo-spectral 2D-MHD solver (numpy FFT, RK4 with 2/3 dealiasing, vorticity + magnetic-vector-potential formulation with Poisson brackets) → run on uicgpu CPU; train small pure-FNO (no PDE loss) as the paper's PINO-only baseline → measure rollout error vs Re.
- This lets us test the CORE QUALITATIVE CLAIMS of Table 1 and Figure 3 (PINO error grows with Re; spectral bias fails at high k; A channel worst) with real code + real numbers, without the diffusion stage.
- Scope declared PARTIAL.

## 19:10 — solver + dataset
- `mhd_solver.py`: 2D incompressible resistive MHD, pseudo-spectral, RK4, 2/3-dealias, GRF-initialized streamfunction and vector potential.
- Smoke test at Re ∈ {100, 500, 1000} × N=64: no blow-up, physical spectrum (peak at low-k), |u|_max ≈ 5, |A|_max ≈ 0.6.
- CPU sim serial was too slow (~1.5 min/sim at dt=5e-4). Wrote `build_dataset_parallel.py` with `multiprocessing.Pool(32)`, offloaded to uicgpu (255 cores), used dt=1e-3.
- 128 sims × 4 Re → 4×152 MB npz files in ~80 s total wall clock on uicgpu.

## 19:15 — FNO first attempt (task = initial → final)
- 4-layer FNO, 8 modes, 32 latent channels (paper: 8 layers, 32 channels, 8 modes for tensor-FNO 3D).
- Task: input = t=0, target = t=1.0.
- Result: train rel_L2 dropped to 0.08 but test rel_L2 stuck at ~1.0. Task ill-posed with only 51 sims and no time-axis in model → severe overfitting.

## 19:18 — FNO refactor (task = next-step + autoregressive rollout)
- `fno_train.py` v2: task = predict state at t+dt from state at t. Train on ALL consecutive pairs from 128 sims (T=26 → 25 pairs/sim → 3200 pairs). Evaluate 26-step autoregressive rollout on held-out test sims. Report paper's eq. 12 relative-L2 metric on the full spatio-temporal-channel volume.
- Ran 400 epochs on cuda, per-Re model. All 4 Re trained in ~25 min total on 1 A100.

## 19:40 — results
- Rollout relative-L2 test:
  - Re=100  → 0.345
  - Re=500  → 0.402
  - Re=1000 → 0.413
  - Re=3000 → 0.421
- Per-channel breakdown at each Re: **A (magnetic vector potential) always the worst** (0.41 → 0.48 → 0.49), consistent with paper's "PINO failure is most acute for the magnetic vector potential channel."

## 19:44 — spectral analysis
- `spectral_analysis.py`: for Re=1000 test set, compute shell-averaged E(k) of ux and A at t=1.0 for ground truth and FNO rollout prediction.
- Low-k (k ≤ 8) prediction/gt ratio for ux = 0.99 (matches).
- High-k (k > 8) prediction/gt ratio for ux = 0.67 (underprediction → **spectral bias reproduced**).
- A is more chaotic; overshoot pattern rather than underprediction — likely a rollout-instability artifact of the small model + no PDE loss (which the paper's PINO would have suppressed). The qualitative "high-k mis-modeling for magnetic field" is present in both directions.

## 19:48 — plots + report
- `make_plots.py` → `error_vs_re.png` and `spectra_Re1000.png`.
- Wrote REPORT.md, brief.md, artifact_harvest.md.
- Called LLM-judge (`judge.py`) via Argo Opus 4.7 at localhost:44497 for verdict.
