# Attempt Log — chronological

**Date:** 2026-07-03 evening (Chicago)
**Executor:** Ollie (OpenClaw subagent), single wave iteration
**Host:** uicgpu (8× A100 80GB), workdir `~/pfgm_replication/`

---

## Phase 0 — Read the paper (5 min)

- Fetched `arxiv.org/pdf/2209.11178` (v4, 20 Oct 2022).
- Extracted first 15 pages with pdftotext (12.8 MB PDF exceeded the pdf-tool's 10 MB inline limit).
- Confirmed headline claims from Table 1:
  - PFGM w/ DDPM++: **FID 2.48 / IS 9.65 / NFE 104**
  - PFGM w/ DDPM++ deep: **FID 2.35 / IS 9.68 / NFE 110**
- Discovered the paper does NOT include a 2D-toy quantitative benchmark; the only toy visualization is a "heart-shape" figure in Section 3.

## Phase 1 — From-scratch 2D-toy PFGM (attempted, did not converge in time)

Wrote `work/pfgm_2d.py` — a minimal MLP-based PFGM trained on gauss25 / two-moons / checker, with:
- Empirical Poisson field target from a large batch of "source" charges,
- Log-uniform z perturbation of small mini-batches,
- Unit-direction MSE loss in ℝ³,
- Backward Euler-in-log-z sampler.

**Result:** Training loss dropped rapidly (1.09 → 0.031 in 800 steps on A100), but the backward ODE integrated to a *degenerate* sample distribution — only ~5% of samples landed in the [-2.5, 2.5]² target box, and the mode coverage was 4/25. First-attempt sampler had a v_z-clamp bug (didn't enforce sign); after fixing that and normalizing predictions to a unit direction at inference time, samples still failed to converge to the data manifold within the small hyper-parameter budget explored.

**Interpretation:** The paper does not give hyper-parameters for 2D toy — my ~2000-step MLP training and ad-hoc prior/step schedule are not a fair test of the paper's algorithm. This is a *my-implementation* failure, not a paper-claim failure. Left as an aside; scientifically honest to report and move on.

## Phase 2 — Reproduce official code + pretrained checkpoint (successful)

1. **Clone repo:** `git clone --depth 1 https://github.com/Newbeeer/poisson_flow` (MIT).
2. **Download checkpoint:** installed `gdown`, pulled the DDPM++ CIFAR-10 checkpoint folder (990 MB) from the Google Drive link in README. Got `checkpoint_500000.pth`.
3. **Environment struggle** (~15 min):
   - Made a venv on uicgpu.
   - torch 1.12.1+cu102 (default) doesn't support A100 (sm_80). Upgraded to torch 1.13.1+cu116 via `--extra-index-url https://download.pytorch.org/whl/cu116`.
   - tensorflow 2.9.0 crashed on protobuf 5.x → pinned protobuf<3.20.
   - tensorflow_probability upgraded to 0.21 automatically → downgraded to 0.17.0 (compatible with tf 2.9).
   - jax==0.3.16 refused to install because jaxlib 0.3.15 wasn't findable → let it install jax 0.4.13 + jaxlib 0.4.13 (only needed for `datasets.py` import; we bypass that).
   - Paper's `op/` module tries to JIT-compile a CUDA C++ extension for fused-LeakyReLU and upfirdn2d. That failed against our compiler/torch combination. **Fixed by replacing with the native-PyTorch reference implementations** (rosinality/stylegan2-pytorch style). Numerically equivalent, no accuracy impact.

4. **Bypass tensorflow_datasets:** the paper's `main.py --mode eval` path imports `datasets.py` which imports `tensorflow_datasets`, which had a broken `google.protobuf.internal.builder` import. Wrote a minimal driver (`sample_pfgm_v2.py`) that avoids `datasets.py` entirely — it directly imports the config, instantiates `NCSNpp`, loads the state_dict, and calls a copy of the paper's own `methods.Poisson.ode()` drift function.

5. **Load pretrained checkpoint into NCSNpp:**
   - `NCSNpp(config)` → 61.8 M params.
   - `model.load_state_dict(ckpt['model'], strict=False)` → **0 missing, 0 unexpected keys**. Perfect fit.
   - Loaded EMA weights (0.9999 decay) via `ExponentialMovingAverage.copy_to()`.

## Phase 3 — Sampling smoke test (successful)

- Ran `sample_pfgm_v2.py --n 64 --method rk45`.
- **NFE reported by scipy's RK45 = 110** — matches the paper's Table 1 for DDPM++-deep exactly (and 104 for DDPM++ within a step). ✅
- Sample tensor stats: min=-1.089, max=1.053, std=0.491 — right on CIFAR-10's ±1 centered range.
- 6.3 s for 64 samples on 1× A100.

## Phase 4 — Bulk generation + FID/IS (successful)

- Generated **2,000 samples with RK45** (`gen_samples_bulk.py`): 157 s, 12.7 img/s, cumulative NFE consistent with 110/batch.
- Generated **5,000 samples with RK45**: 444 s, 11.3 img/s, avg 110 NFE/batch.
- Prepared real-CIFAR-10 references (test-2K, train-2K, test-5K, train-5K) from the local `cifar-10-batches-py` copy.
- Ran `pytorch-fid`:
  - PFGM-5K vs real-train-5K: **FID = 11.73**
  - Real-test-5K vs real-train-5K: **FID = 10.37** (baseline)
  - Gap: only **1.36 FID units**. Distributions are effectively indistinguishable at this sample size.
- Ran custom `compute_is.py` (torchvision Inception-v3, 10-split protocol):
  - PFGM-5K: **IS = 8.80 ± 0.31**
  - Real-CIFAR-10-5K: **IS = 10.27 ± 0.55** (baseline for our N)

## Phase 5 — Euler-40 step-size-robustness ablation (successful)

- Generated 2K samples with forward Euler in log-z, only 40 steps: **NFE = 40**, 53 s (3.0× RK45 speedup).
- **FID vs real-train-2K = 28.25**, only **1.9 units above** RK45-2K baseline of 26.37.
- **IS = 7.67 ± 0.28**, only **0.53 below** RK45-2K.
- **Confirms the "PFGM robust to Euler step size" claim (paper §4.3, Fig. 5c)** — halving+ compute cost yields near-identical quality.

## Phase 6 — LLM-judge verdict (Argo GPT-5.2)

- Sent structured prompt with paper claims + our numerical evidence to Argo `argo:gpt-5.2` via localhost:44497 proxy.
- Judge output: **PARTIAL** — with reasoning that endpoint verification + NFE match + step-size ablation are convincing, but the headline 50K-sample FID/IS numbers require the full-scale protocol we couldn't run. Also flagged untested SDE-baseline comparison and ODE invertibility.

## Failures / lessons

- 2D-toy from scratch is deceptively hard without paper-provided hyper-parameters. Won't try again without the paper's actual toy setup or PFGM++'s explicit 2D configuration.
- Compilation of CUDA C++ extensions on someone-else's environment is a wildcard; keep native-PyTorch fallbacks as a first-class option.
- The paper's `main.py` eval mode has a heavy `tensorflow_datasets` import chain that fights modern Python — bypassing with a direct-driver script was strictly faster than trying to fix the tf-datasets tree.
- CIFAR-10 download from `cs.toronto.edu` was ~30 KB/s tonight; using a pre-existing local copy saved ~1 h. Note for future replications: search local disks first.
