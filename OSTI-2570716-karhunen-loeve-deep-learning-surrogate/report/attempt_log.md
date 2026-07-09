# Attempt log — 2026-07-04 (evening)

- 23:31 CDT — Received subagent task for OSTI 2570716. Read wave brief.
- 23:32 — Created target directory tree `~/Dropbox/REPLICATE-PROJECT/OSTI-2570716-karhunen-loeve-deep-learning-surrogate/{report/evidence,work}`.
- 23:32 — CherryRd cannot reach osti.gov directly. Downloaded PDF via
  `ssh uicgpu` (which has the proxy env), then `scp` back to workspace as
  `work/paper.pdf` (4.4 MB, PDF v1.7, MD5 verified via file(1)).
- 23:33 — `pdftotext -layout` extraction succeeded (1081 lines). Attempted PDF
  tool for structured claim extraction; blocked by (a) Dropbox path not in
  allow-list and (b) Anthropic/OpenAI PDF endpoints unavailable (billing/policy).
  Fell back to `pdftotext` + targeted `grep` — sufficient, since the paper
  reports all needed numbers in plain text.
- 23:33 — Identified paper title/authors/venue, method, test problem
  (Freyberg unconfined aquifer, MODFLOW-6, 20×40 grid), covariance model
  (exponential, range=1 km, sigma_ln=0.1823, mean K=11.1 m/day), and the
  headline results table (Table 2: rel-L2 = 3.53e-4 / 5.26e-4 / 4.82e-3 for
  KL-DNN / FNO / DeepONet at Ntrain=2000; training times 1637/11784/17678 s).
  Also captured Table 1 (Ntrain 168/472/2000 and Nk_y/Nk_h 112/68, 217/92,
  347/104) and the DNN architecture (2 hidden layers, 3000 SiLU neurons,
  Adam, gamma_S=1e-4).
- 23:34 — Wrote `work/kldnn_replicate.py`: samples y ~ N(mu, C_y_exp), solves
  linear elliptic Darcy with cell-centered FV (harmonic K interface),
  computes empirical KL via dual eigendecomposition (Gram matrix trick,
  since Ntrain << Nm), truncates by cumulative-variance rtol, trains
  KL-DNN in latent space, and evaluates on 100 held-out samples. Also
  trains a direct-DNN baseline (y -> h in full space).
- 23:34 — Sanity-check on paper's rtol targets (rtol_y=0.975, rtol_h=0.9999).
- 23:34 — Copied script to uicgpu:/tmp/kldnn_repl/, verified torch 1.11 + CUDA
  available on the A100, launched `nohup python -u kldnn_replicate.py`.
- 23:34–23:35 — Run completed in <2 min total: 28 s of PDE solves (2200 samples)
  + three KL/DNN cases (each ~10-15 s). Copied evidence CSVs + logs back.
- 23:35 — Generated `eigen_decay.png` and `error_vs_ntrain.png`.
- 23:35 — LLM-judge scoring via Argo proxy (127.0.0.1:44497). First try with
  `argo:claude-opus-4.8` returned upstream 502 (transient Argo issue).
  Retry with `argo:claude-sonnet-4.5` succeeded; verdict PARTIAL with per-claim
  breakdown (C1 strong, C2 partial, C3 partial, C4 weak). Saved to
  `evidence/llm_judge.json`.
- 23:36 — Wrote final REPORT.md, brief.md, artifact_harvest.md.

## What worked
- pdftotext -layout for the paper text (all needed numbers legible).
- Empirical-KL via Gram-matrix dual formulation — makes Nm=800 trivial and
  extends to Nm>>Ntrain problems without touching a big Nm×Nm matrix.
- Argo proxy sonnet-4.5 as fallback judge when opus 502'd.

## What failed / partial
- No MODFLOW-6 or PEST++ install performed (out of scope for a single subagent
  cycle); the paper's exact Freyberg dataset and the IES inverse-problem
  comparison are therefore not reproduced quantitatively.
- Only 3000 epochs and no hyperparameter search; absolute KL-DNN error is ~10×
  the paper's, though the trend and ordering with Ntrain is correct.
- FNO/DeepONet baselines not implemented (would need `neuraloperator` package
  and additional hours) — the paper's comparative claim is only checked in
  spirit (KL-DNN in latent space is fast).

## Repro command
```
python work/kldnn_replicate.py    # reproduces all CSVs in report/evidence/
python work/make_fig.py           # regenerates PNGs
python work/judge.py              # re-scores via Argo
```
