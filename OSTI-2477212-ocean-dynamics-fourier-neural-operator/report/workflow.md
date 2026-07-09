# Workflow — OSTI 2477212 (Sun et al. FNO for Ocean Dynamics)

Independent replication workflow spanning two sessions:
1. **2026-07-02** (session 2ac90c8e) — SPOT-CHECK on synthetic ocean-tracer proxy.
2. **2026-07-04** (session 9edb930b) — promotion to PARTIAL via canonical 1D Burgers method-verification track.

Judge: free Argo `argo:gpt-5.2` via `localhost:44497`.

---

## Session 1: 2026-07-02 — SPOT-CHECK track

### Step 1 — Paper acquisition
- Attempted direct download from `osti.gov` via CherryRd home network → **blocked** (osti.gov unreachable from home ISP).
- Fallback: `ssh uicgpu` + `source ~/env.sh` (UIC HTTP proxy) then curl the OSTI PDF URL.
- Cache locally under `work/paper.pdf`, extract text with `pdftotext -layout > work/paper.txt`.

### Step 2 — Claims extraction
- Read paper.txt, enumerate testable claims → produce `report/REPORT.md` claims table (C1–C5).
- Identify **C5** as untestable without the SOMA κ_GM 100-member ensemble → check Data Availability Statement → confirmed **not public**.
- GitHub API keyword sweep for authors' training script:
  - `deephyper+FNO+ocean` → 0 hits
  - `SOMA+fourier+neural+operator` → 0 hits
  - `yixuan-sun FNO ocean` → 0 hits
- Result: no public code, no public dataset → cannot do bit-exact replication.

### Step 3 — Independent FNO implementation (from scratch)
- Write `work/fno2d_spotcheck.py`:
  - `SpectralConv2d` (rFFT2 → truncate to (modes1, modes2) → learnable complex multiplication → irFFT2).
  - `FNO2d` (lift → N × (spectral-conv + pointwise-conv + GELU) → 2-layer projection head).
- Deliberately DO NOT use Nvidia Modulus (paper's framework) → keeps replication independent of Modulus's Argonne-tuned defaults.

### Step 4 — Synthetic ocean-tracer ensemble generation
- 100 simulations × 30 daily snapshots × 64² grid.
- Rotating quasi-wind-driven velocity field; per-sim κ ∼ Uniform[200, 2000] (nondimensionalized for CFL stability).
- 60/20/20 by-simulation split (matching paper's protocol).

### Step 5 — Two configs (baseline vs optimized)
- **Baseline** (Modulus-default proxy): 2 channels, width 20, 8 modes, 2 blocks, pure MSE, bs 32.
- **Optimized** (HPO-winner proxy): 4 channels (field + κ + (x,y)), width 40, 16 modes, 4 blocks, composite MSE + neg-ACC (α = 0.5), bs 16.
- Both 40 epochs. AdamW lr 1e-3 wd 1e-4, cosine LR schedule.

### Step 6 — Metrics
- Single-step: log(RSE), log(1-ACC), RSE, ACC.
- Autoregressive rollout: per-day MSE + ACC over 5 test sims (Figure 6 analog).
- Save to `report/evidence/results_run2.json`.

### Step 7 — LLM-judge (Argo gpt-5.2)
- `python3 llm_judge_ocean_proxy.py results_run2.json > llm_judge_verdict.txt`.
- 3-question rubric: (Q1) does FNO learn useful operator? (Q2) does optimized improve in paper's direction? (Q3) does rollout match Figure 6?
- Result: Q1 YES, Q2 YES, Q3 YES → **SPOT-CHECK verdict** (correct label for a synthetic-only test).

---

## Session 2: 2026-07-04 — PARTIAL promotion via 1D Burgers

### Motivation
The 2026-07-02 spot-check verified the paper's qualitative story on synthetic dynamics but could not independently bound our confidence in the FNO **method itself**. To promote to PARTIAL, run the canonical Li et al. 2021 Section 5.1 FNO benchmark (1D viscous Burgers) from scratch and check the two central FNO claims:
1. Low relative-L2 test error.
2. Zero-shot resolution invariance.

### Step 8 — Ground-truth Burgers solver
- Pseudo-spectral integrating-factor RK4 for ∂ₜu + u∂ₓu = ν∂²ₓu on periodic [0,1].
- 2/3 dealiasing, 2000 substeps per (0→1) trajectory.
- GRF initial conditions u₀ ~ N(0, α(-Δ + τ²)⁻²) with α=625, τ=25; per-sample RMS-normalized.
- ν = 0.01 (STIFFER than Li et al.'s 0.1 → sharper gradients → strictly harder operator to learn → makes the "FNO works" claim strictly stronger).

### Step 9 — Independent 1D FNO implementation
- `work/fno1d_burgers_benchmark.py`:
  - `SpectralConv1d` (rFFT → truncate to `modes` → learnable complex multiplication → irFFT).
  - `FNO1d` (lift → N × spectral-conv + pointwise-conv + GELU → 2-layer projection).
- Same architecture philosophy as the 2D spot-check, pure PyTorch, `torch.fft.rfft/irfft`.

### Step 10 — Dataset
- 1000 train + 200 test samples per resolution s ∈ {256, 512, 1024, 2048, 4096}.
- Training on s = 1024 exclusively.
- **Evaluation on all five resolutions using the SAME trained weights** — this is the resolution-invariance test.

### Step 11 — Two Burgers configs
| | Baseline (small, MSE) | Optimized (large, LpLoss) |
|---|---|---|
| modes | 8 | 16 |
| width | 32 | 64 |
| blocks | 4 | 4 |
| loss | MSE | relative-L2 (LpLoss) |
| params | 74,209 | 549,569 |
| batch | 32 | 32 |
| optimizer | AdamW lr 1e-3 wd 1e-4 | AdamW lr 1e-3 wd 1e-4 |
| LR schedule | cosine → 0 | cosine → 0 |
| epochs | 500 | 500 |

### Step 12 — Run
```
ssh uicgpu
source ~/env.sh
cd ~/work/osti-2477212
CUDA_VISIBLE_DEVICES=0 python3 fno1d_burgers_benchmark.py \
    --n_train 1000 --n_test 200 --s_train 1024 \
    --s_eval 256 512 1024 2048 4096 \
    --epochs 500 --nu 0.01 \
    --out results_burgers_full.json
```
Wall time: 15 min (450 s data-gen, 465 s training, 4 s per resolution eval).

### Step 13 — Metrics
- Relative L2: `||pred − y||₂ / ||y||₂` mean over 200 test samples (Li et al. 2021 Table 1 convention).
- MSE.
- Save to `report/evidence/results_burgers_full.json`; log at `report/evidence/burgers_full.log`.

### Step 14 — LLM-judge (Burgers rubric)
- `python3 llm_judge_burgers.py results_burgers_full.json > llm_judge_burgers.txt`.
- Rubric:
  - **Q1** — Does test rel-L2 achieve single-digit percent (i.e. meaningful operator learned)?
  - **Q2** — Do same weights hold approximately constant rel-L2 across s ∈ {256,…,4096}?
  - **Q3** — Does the LpLoss/higher-capacity config beat the MSE baseline?
- Verdict: **Q1 YES, Q2 YES, Q3 NO → PARTIAL**.
- The Q3 NO is an HONEST counter-signal: LpLoss (2.997%) does not beat MSE (2.962%) on Burgers. We do NOT bury it; we report it in §4.4 and in the GENUINE CRITIQUE section of REPORT.tex.

### Step 15 — Reconcile and promote verdict
- SPOT-CHECK (2026-07-02, synthetic ocean proxy) + PARTIAL evidence (2026-07-04, Burgers method core + resolution invariance) → promote to **PARTIAL**.
- Update `report/REPORT.md` §0 verdict, §2 claims table (add C6), §3.3 method-verification track description, §4.1 Burgers results, §4.4 LLM judge, §5 what-verified/what-not, and final Verdict block.

---

## Data flow diagram
```
paper.pdf (osti.gov via uicgpu proxy)
      │
      ▼
work/paper.txt (pdftotext -layout)
      │
      ▼
claims table (C1..C6) in REPORT.md
      │
      ├─────────────────────────┐
      ▼                         ▼
[Ocean-proxy track]      [Burgers method-verification track]
      │                         │
synthetic κ-ensemble       Li et al. 2021 rig
      │                         │
fno2d_spotcheck.py         fno1d_burgers_benchmark.py
      │                         │
results_run2.json          results_burgers_full.json + burgers_full.log
      │                         │
llm_judge_verdict.txt      llm_judge_burgers.txt
      │                         │
      └─────────┬───────────────┘
                ▼
     REPORT.md verdict = PARTIAL
                │
                ▼
       Backfill: REPORT.tex, open_questions.json,
                 workflow.md, artifacts_summary.md,
                 failure_analysis.md
```

---

## Repro commands (single copy-paste block for future replicators)
```bash
# On uicgpu (needs UIC HTTP proxy env in ~/env.sh)
ssh uicgpu
source ~/env.sh
cd ~/work/osti-2477212

# --- Ocean-proxy spot-check (2026-07-02) ---
CUDA_VISIBLE_DEVICES=0 python3 fno2d_spotcheck.py \
    --out results_run2.json
python3 llm_judge_ocean_proxy.py results_run2.json > llm_judge_verdict.txt

# --- Canonical Burgers method-verification (2026-07-04) ---
CUDA_VISIBLE_DEVICES=0 python3 fno1d_burgers_benchmark.py \
    --n_train 1000 --n_test 200 --s_train 1024 \
    --s_eval 256 512 1024 2048 4096 \
    --epochs 500 --nu 0.01 \
    --out results_burgers_full.json 2>&1 | tee burgers_full.log
python3 llm_judge_burgers.py results_burgers_full.json > llm_judge_burgers.txt
```

Total wall time: ~15 min Burgers + ~20 min ocean-proxy on a single A100 80GB PCIe.
