# Artifacts Summary — OSTI 2477212 (Sun et al. FNO for Ocean Dynamics)

Independent replication artifacts produced across two sessions
(spot-check 2026-07-02, PARTIAL promotion 2026-07-04). Host: CherryRd
(coordination) + uicgpu (1×A100 80GB PCIe, execution).

---

## Directory layout

```
OSTI-2477212-ocean-dynamics-fourier-neural-operator/
├── report/
│   ├── REPORT.md                       # canonical human-authored replication report
│   ├── REPORT.tex                      # detailed LaTeX + GENUINE CRITIQUE section (this backfill)
│   ├── open_questions.json             # 5 truly-open research questions (this backfill)
│   ├── workflow.md                     # end-to-end workflow (this backfill)
│   ├── artifacts_summary.md            # this file
│   ├── failure_analysis.md             # what did NOT replicate (this backfill)
│   ├── artifact_harvest.md             # paper acquisition log (URL, checksum, proxy path)
│   └── evidence/
│       ├── results_burgers_full.json   # canonical 1D Burgers benchmark, all metrics
│       ├── burgers_full.log            # full training log (15 min wall time)
│       ├── llm_judge_burgers.txt       # Argo gpt-5.2 verdict on Burgers rig
│       ├── results_run2.json           # synthetic ocean-tracer proxy metrics + rollout arrays
│       └── llm_judge_verdict.txt       # Argo gpt-5.2 verdict on ocean-proxy spot-check
└── work/
    ├── paper.pdf                       # OSTI 2477212 PDF (fetched via uicgpu proxy)
    ├── paper.txt                       # pdftotext -layout extraction
    ├── fno1d_burgers_benchmark.py      # from-scratch 1D FNO + pseudo-spectral RK4 solver
    ├── fno2d_spotcheck.py              # from-scratch 2D FNO + synthetic ocean ensemble generator
    ├── llm_judge_burgers.py            # 3-question rubric judge for Burgers rig
    └── llm_judge_ocean_proxy.py        # 3-question rubric judge for ocean proxy
```

---

## Key evidence files

### `report/evidence/results_burgers_full.json`
Canonical 1D viscous Burgers benchmark (ν = 0.01, s_train = 1024,
1000 train / 200 test, 500 epochs, AdamW cosine schedule). Two configs:

| Config | params | test rel-L2 @ s=1024 | test MSE @ s=1024 |
|---|---:|---:|---:|
| baseline_mse (modes=8, w=32, MSE)   |  74 209 | **2.962 %** | 1.48e-4 |
| optimized_lp (modes=16, w=64, LpLoss) | 549 569 | **2.997 %** | 1.82e-4 |

Resolution-invariance sweep (same trained weights, s_eval ∈ {256, 512, 1024, 2048, 4096}):
- baseline_mse spread: **0.17 pp** (max − min rel-L2)
- optimized_lp spread: **0.28 pp**

This is the money artifact: 16× resolution range, sub-percent variance
in rel-L2 → clean reproduction of the FNO family's central zero-shot
super-resolution claim (Li et al. 2021, arXiv:2010.08895).

### `report/evidence/burgers_full.log`
Full stdout log of the 15-min training run on uicgpu GPU 0. Includes
per-epoch training loss curves for both configs, per-resolution eval
times (~4 s), and final metric dump.

### `report/evidence/llm_judge_burgers.txt`
Verbatim free-Argo `argo:gpt-5.2` verdict on the Burgers rig:
- **Q1 YES** — rel-L2 ≈ 3.0e-2 is single-digit percent, meaningful operator learned.
- **Q2 YES** — same weights hold rel-L2 approximately constant across
  s ∈ {256, 512, 1024, 2048, 4096}.
- **Q3 NO** — LpLoss/higher-capacity does NOT beat MSE baseline
  (2.997e-2 vs 2.962e-2). Honest counter-signal.
- Overall verdict: **PARTIAL**.

### `report/evidence/results_run2.json`
Synthetic ocean-tracer proxy metrics from 2026-07-02 spot-check:
100 sims × 30 daily snapshots × 64² grid, per-sim κ ∼ U[200, 2000],
60/20/20 by-simulation split. Two configs (baseline vs optimized) with
composite MSE + neg-ACC loss on the optimized side.

Single-step:
- Baseline: log(RSE) = −5.092, log(1-ACC) = −5.798
- Optimized: log(RSE) = −7.725, log(1-ACC) = −8.713
- Δ opt − base: −2.63 in log(RSE), −2.92 in log(1-ACC)

Autoregressive rollout (Figure 6 analog):
- Baseline ACC: 1.000 (d0) → 0.088 (d29) — collapses
- Optimized ACC: 1.000 (d0) → 0.9299 (d29) — retains skill

### `report/evidence/llm_judge_verdict.txt`
Verbatim free-Argo `argo:gpt-5.2` verdict on the ocean-proxy
spot-check: Q1 YES / Q2 YES / Q3 YES → **SPOT-CHECK** (correct label
for a synthetic-only test; not promoted to PARTIAL by itself).

---

## Code artifacts (all in `work/`)

### `fno1d_burgers_benchmark.py`
~350 lines, pure PyTorch + `torch.fft.rfft/irfft`. Ships:
- `SpectralConv1d` (rFFT → mode truncation → complex learnable multiply → irFFT).
- `FNO1d` (lift 1→width channels → N × (spectral-conv + pointwise-conv + GELU)
  → 2-layer projection back to 1 channel).
- Pseudo-spectral integrating-factor RK4 Burgers solver with 2/3 dealiasing
  and GRF initial-condition generator (α=625, τ=25, RMS-normalized).
- Full training loop (both configs), evaluation across all resolutions, JSON output.

### `fno2d_spotcheck.py`
2D analogue: `SpectralConv2d`, `FNO2d`, plus a synthetic rotating
quasi-wind-driven advection-diffusion solver with per-sim κ sampling.
Handles the 100-sim × 30-day × 64² × 4-variable ensemble and both
single-step + autoregressive-rollout evaluation.

### `llm_judge_burgers.py`, `llm_judge_ocean_proxy.py`
Thin wrappers that load the JSON metrics, format them into a
paper-context prompt with a 3-question rubric, POST to
`localhost:44497/v1/chat/completions` with `model="argo:gpt-5.2"`, and
dump the verbatim response.

---

## Paper artifact

### `work/paper.pdf` + `work/paper.txt`
OSTI ID 2477212 (Sun et al., *Mathematics* 2024, 12, 1483, DOI
10.3390/math12101483). Fetched via `ssh uicgpu` (osti.gov unreachable
from CherryRd home network); pdftotext -layout extraction into
`paper.txt` for offline claim mining. Full acquisition trail (URL,
size, checksum, proxy path) in `report/artifact_harvest.md`.

---

## Compute + tool provenance
- Host: uicgpu (m1acbook-2-facing UIC node), 1×NVIDIA A100 80GB PCIe.
- CUDA 12.8, driver 570.207.
- Python 3.9.5, torch 1.11.0 (CUDA build), numpy 1.22.x.
- No `neuraloperator`, no `modulus` — pure PyTorch spectral-conv
  implementation. Ensures independence from the paper's Modulus-based
  reference stack.
- Judge: free Argo `argo:gpt-5.2` via `http://localhost:44497/v1`
  (Argo wrapper on cherryrd, `Authorization: Bearer stevens`).
- Total GPU wall time: ~15 min Burgers + ~20 min ocean-proxy = ~35 min
  on a single A100.

---

## What is NOT in this artifact set
- The paper's SOMA 100-member κ_GM ensemble (not public, per Data
  Availability Statement).
- The paper's DeepHyper HPO campaign checkpoints (500 evals × 80 A100
  × 6 h ALCF Polaris — out of budget).
- Nvidia Modulus training scripts / configs (deliberately avoided for
  independence).
- Multi-seed statistics (single-seed reporting — a known threat to
  validity we call out in REPORT.tex GENUINE CRITIQUE).

---

## Reuse pointers
- Anyone reproducing the Burgers half: `work/fno1d_burgers_benchmark.py`
  is a self-contained 350-line reference implementation and needs
  nothing beyond `torch>=1.11` + `numpy`.
- Anyone extending to the ocean-proxy: `work/fno2d_spotcheck.py` is the
  reference 2D FNO with synthetic ensemble generator.
- Anyone adapting the judge protocol: `work/llm_judge_burgers.py` is a
  template 3-question rubric — swap in a different LLM endpoint by
  changing the base URL / model name.
