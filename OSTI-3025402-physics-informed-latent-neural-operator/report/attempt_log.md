# Attempt Log — OSTI 3025402

Chronological, terse. All times US/Central.

## 2026-07-04, evening
- 18:57 Read wave brief. Assigned paper: OSTI 3025402, PI-Latent-NO by Karumuri, Graham-Brady, Goswami (JHU, 2025).
- 18:58 Tried `curl` on OSTI PDF from CherryRd. Network unreachable to `www.osti.gov` (timeout at 75 s). Rerouted through **uicgpu** (has env.sh proxy) and downloaded successfully (8.7 MB, valid PDF v1.5). `scp` back to Dropbox target dir.
- 19:00 Tried the `pdf` tool. Anthropic backend rejected (credit balance low) and Gemini/GPT-5 backends unavailable. Fell back to `pdftotext -layout`, which gave a clean 2493-line text extract sufficient for extracting the abstract, method, Tables 1-5, and the computational-cost breakeven discussion (Section 5).
- 19:01 Extracted core numerical claims for the 1D Diffusion-Reaction case (Table 2):
    - `PI-Latent-NO, n_train=0: R^2 = 0.9999 ± 0.0000, RelL2 = 0.006 ± 0.001, train=1945 s ± 37, per-iter=0.039 s`
    - Inference ~0.01 s vs classical solver ~0.4047 s → breakeven at ~5,056 simulations (Section 5).
    - Also confirmed the paper's reported ~1500 iters ×~24k-total (per-iter 0.039) yields ~1945 s train time on A100 40GB.
- 19:02 Cloned author repo (`https://github.com/Centrum-IntelliPhysics/Physics-Informed-Latent-DeepONet`) to `/tmp/pi-latent-no-repo` on uicgpu for reference. 263 files. JAX-based. Decision: do NOT execute the author code — an *independent* replication is more informative for verifying the architectural claim, so I reimplement in PyTorch from the paper equations (5)-(7) and Algorithms 1-2.
- 19:03 Wrote `work/pi_latent_no_dr.py`: minimal PyTorch reimplementation with:
    - Latent-DeepONet: branch MLP on s(x) ∈ R^{nx} → R^{p_L·n_z}; trunk MLP on t → R^{p_L·n_z}; einsum `bpk,tpk->btk` gives z(s,t) ∈ R^{n_z}.
    - Reconstruction-DeepONet: branch MLP on z ∈ R^{n_z} → R^{p_R}; trunk MLP on x → R^{p_R}; dot in p_R gives u(s,t,x).
    - Physics loss: pointwise collocation-based residual (batch-of-1-per-sample loop to avoid mixing samples through the shared trunk), IC anchor at t=0, BC anchor at x∈{0,1}. Uses standard reverse-mode AD (torch 1.11 lacks functorch).
    - Independent FDM ground-truth solver (central-diff in x, forward-Euler in t with CFL sub-stepping) and Cholesky GP source sampler with the paper's kernel (ell=0.2, σ=1.0).
- 19:04 Smoke test on uicgpu (50 iters, 4 samples/batch, 256 collocation points): loss decreased 1.6 → 0.57, R² went from −3.7 → +0.04 in 4 s. Architecture works and is training. `physics_loss_pointwise` correctly demands B=1 (my note in code) because otherwise the shared-trunk AD would sum the per-sample residuals — instead I loop over the mini-batch of source functions.
- 19:05 Full training run: 3 seeds in parallel on GPU 0/1/2, each 8000 iters, 8 source functions per mini-batch, 512 collocation points, n_z=9 (paper's choice), p_L=p_R=64, hidden [128,128,128], Adam lr=1e-3, StepLR halving every 1600 iters.
- 19:12 R²_50 at 500 iters: {0.86, 0.78, 0.82}; L2: {0.28, 0.35, 0.31}. Trending correctly.
- 19:17 R²_50 at 3000 iters: ~0.92-0.97; L2 ~0.13-0.20.
- 19:19 R²_50 at 4500 iters: 0.988-0.991; L2 ~0.05-0.08.
- 19:22 Final (8000 iters): mean R² = **0.9952 ± 0.0011**, mean RelL2 = **0.0482 ± 0.0041**. Train time ~500 s per seed. Inference: 15 μs/sample batched (200 test cases in 3 ms), ~0.8 ms single-sample. Solver: ~0.3 ms/sample.
- 19:24 Made plots (`sample_prediction.png` — GT / pred / error triptych; `seed_summary.png` — per-seed R² and L2 vs paper). Pulled all artifacts to `report/evidence/`.
- 19:25 LLM judge call to Argo (localhost:44497). Claude Opus 4.7/4.8 returned upstream-parse errors; fell back to `argo:gpt-4o` (also free). Judge output: verdict **PARTIAL**, agreement **moderate** — C1 (method) and C4 (scaling) supported; C2 (accuracy) and C3 (speedup direction) partially supported; C5 (Burgers/2D) unaddressed. Saved to `report/evidence/llm_judge_output.txt`.

## Failures/gotchas
- CherryRd → osti.gov unreachable → routed through uicgpu.
- `pdf` tool broken (both Anthropic and Gemini backends unavailable) → `pdftotext` fallback.
- Argo Claude proxy returning schema-validation errors → fallback to Argo GPT-4o (still an Argo/free endpoint per the wave rules).
- Reverse-mode AD wrt shared trunk-input coordinates mixes samples across the mini-batch. Fix: loop `physics_loss_pointwise` over the mini-batch of source functions with B=1 per call. This is slower than a fully batched vectorized call but is *correct*; a forward-mode-AD version (available in modern torch via functorch/vmap+jvp) would be faster on newer stacks.
- My FDM ground-truth solver is ~1000x faster than the paper's reported 0.4047 s per sample on the 1D diffusion-reaction problem, most likely because the paper uses a stiffer/higher-order solver (or a different resolution). This means the paper's ~5056-sample breakeven does not translate directly; the *direction* of the claim (batched NN inference << classical solver per-sample at scale) does still hold with our numbers, but not by the exact same margin.
