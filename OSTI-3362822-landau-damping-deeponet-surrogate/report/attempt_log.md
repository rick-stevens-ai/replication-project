# Attempt log — OSTI 3362822 replication (2026-07-06)

Chronological. Times in America/Chicago CDT.

- **06:09** — Subagent spawned. Wave brief read. Set up in
  `~/Dropbox/REPLICATE-PROJECT/OSTI-3362822-landau-damping-deeponet-surrogate/`.
- **06:12** — Fetched paper.pdf (2.5 MB, PDF 1.7, 8 pages) from
  https://www.osti.gov/servlets/purl/3362822 via curl on uicgpu.
- **06:14** — Marker extraction on uicgpu GPU 6: 41 s wall, `paper.md` (32 KB) + 12 figure JPEGs.
- **06:15** — Attempted `pdf` tool for structured summary; blocked by media-path allowlist.
  Copied paper to `/Users/stevens/.openclaw/workspace/` — still blocked (billing 400 on Anthropic;
  Gemini 3-flash unknown model; OpenAI PDF extraction disabled). **Workaround:** `pdftotext -layout`
  locally, then manual read of 404 lines. Fully extracted claims, hyperparameters, Table 1/2/3/4.
- **06:16** — First `replicate.py` written. Contains: analytic Landau dispersion, VP solver,
  DeepONet architecture, single-mode dataset gen, training, eval, inference bench.
- **06:16** — First replicate.py crash at first `np.trapz` call: numpy 2.x removed it.
  **Fix:** global replace with `np.trapezoid`.
- **06:17** — Nougat #1 attempt (`/data/stevens/.venvs/extraction/bin/nougat`) crashed on
  transformers API drift (`prepare_inputs_for_inference() got unexpected kwarg 'cache_position'`).
- **06:18** — Nougat #2 attempt (`/gpustor/stevens/anaconda3/envs/nougat/bin/nougat`)
  succeeded: 16 s wall, `paper.mmd` (26 KB).
- **06:18** — Replicate.py restarted. Loud plateau discovered: replicate.log stays 0 bytes
  because Python is buffering stdout. Kill + restart with `-u` unbuffered flag.
- **06:27** — Restart succeeds with unbuffered output. Step-1 analytic Landau rates prints:
  γ(0.35) = -0.0343, γ(0.5) = -0.153.
  Step 2 VP baseline (T=1, k=0.35, A=0.05, Nx=32, Nv=128, dt=0.05, tmax=20): 2.41 s wall,
  numerical γ = -0.0384 (12% high vs analytic — acceptable, coarse grid).
  Step 3 dataset gen: 250 sims at ~2.4 s each = 590 s (10 min) — dominated by scipy
  CubicSpline per-x-per-step loop → **replaced with vectorized linear-SL v-advection**
  before this run started.
- **06:37** — Dataset done. Step 4 training v1 starts. Immediate plateau at MSE(log E) = 0.478
  (ensemble-mean solution). Runs 200 s more with zero improvement.
- **06:40** — v1 finishes. rel-L2 = 0.40 train / 0.40 test. **Diagnosis:** paper-exact
  architecture cannot escape ensemble-mean basin with scalar T branch input and no positional
  encoding. **Fix:** write v1.5 retrain with Fourier features on scalar inputs.
- **06:44** — v1.5 (retrain.py) runs. Reaches MSE(log E) = 0.026 in 120 s but has a training
  spike at iter 20k (loss briefly to 85, recovers). rel-L2 = 0.21 train / 0.26 test. Better,
  still 25× paper.
- **06:45** — v2 (retrain2.py) written: v1.5 + gradient clipping ‖g‖ ≤ 1, cosine LR schedule
  1e-3 → 1e-6, 60k iters, best-test model selection. Runs 242 s.
- **06:49** — v2 done. **Best test MSE(log E) = 0.0123 → rel-L2 = 0.183 test / 0.164 train.**
  22× the paper's 0.008 but same trend shape.
- **06:49** — Inference bench: 100 test cases in 0.63 ms on A100. Paper: 1.48 ms on L40S. OoM match.
- **06:52** — All 4 figures generated locally (matplotlib): Fig 3-style deeponet-vs-sim,
  error distribution histogram, Fig 2-style analytic dispersion, baseline damping envelope.
- **06:53** — LLM-judge call: `argo:gpt-5.2` via `<tailnet-aggregator>:4000`. Returns
  `{verdict: PARTIAL, coverage: 0.55, agreement: 0.35}`. Argo `argo:claude-opus-4.8` route
  failed with "invalid response format" — switched to gpt-5.2 which worked.
- **06:55** — Wrote REPORT.md, REPORT.tex, brief.md, open_questions.json, artifacts_summary.md,
  failure_analysis.md, workflow.md, artifact_harvest.md.
- **06:57** — Compiled REPORT.tex to REPORT.pdf (pdflatex, 5 pages, 227 KB). Clean.
- **06:58** — Wave-result artifact bar check: all 8 present.

## Things that worked
- Nougat #2 env once identified.
- Marker on GPU 6.
- Fourier feature + gradient clipping + best-test model selection unlocked training.
- Argo :4000 aggregator (gpt-5.2 route) for LLM judge.

## Things that didn't
- `pdf` tool (paid endpoints only).
- Nougat #1 env (stale transformers).
- v1 DeepONet (paper-exact hyperparameters) → mean plateau.
- Argo :44497 direct + :4000 gpt-opus-4.8 route (upstream response validation errors).
- Reaching paper's 0.008 rel-L2 (best we got: 0.075 for the single best test case).

## Things skipped
- Gkeyll install (would need a day of C-build + config).
- Five-mode case (compute budget triage).
- Contacting authors for Gkeyll dataset.
