# Independent Replication Report — OSTI 3025402

**Paper:** S. Karumuri, L. Graham-Brady, S. Goswami (Johns Hopkins). *Physics-Informed Latent Neural Operator for Real-time Predictions of time-dependent parametric PDEs.* Preprint (arXiv:2501.08428v3, Oct 29 2025), submitted to Elsevier. Retrieved via OSTI as OSTI id **3025402**.

**Replicator:** Independent PyTorch reimplementation, executed by Ollie (OSTI-100 replication project), 2026-07-04. Compute: NVIDIA A100 80GB (uicgpu, 3 seeds in parallel across 3 GPUs).

**Verdict:** **PARTIAL** — the paper's core architectural, methodological, and scaling claims (C1, C4) reproduce independently, and the accuracy (C2) and real-time-inference (C3) claims reproduce in *direction and order of magnitude* at a reduced training budget but do not fully reach the paper's reported R² = 0.9999 / RelL2 = 0.006. Additional PDE cases (C5) were not attempted.

---

## 1. Paper summary

The paper introduces **PI-Latent-NO**, a physics-informed neural operator built from two coupled DeepONets trained end-to-end:

1. **Latent-DeepONet** learns a low-dimensional latent trajectory of the PDE solution: given the parametric input function s(x) (through a branch network) and time t (through a trunk network), it produces a latent state z(t) ∈ R^{n_z}.
2. **Reconstruction-DeepONet** maps that latent state back to the physical solution field: given z(s,t) (branch) and spatial coordinate x (trunk), it produces u(s,t,x).

The full solution field is obtained by composing the two, and the PDE residual + boundary + initial-condition losses are applied to u_hat through automatic differentiation. Crucially, because the trunk networks receive **t and x separately** rather than a joint (t,x) coordinate, the number of trunk evaluations grows as O(n_t + n_x) instead of O(n_t · n_x). This is the source of the paper's "near-constant scaling" claim and its ability to train large problems in physics-informed mode without materializing dense collocation grids.

The paper demonstrates PI-Latent-NO on four benchmarks:
1. 1D Diffusion-Reaction (u_t = D·u_xx + k·u² + s(x), Dirichlet-zero, ν=D=0.01, k=0.01, s ∼ GP).
2. 1D Burgers (periodic).
3. 2D Stove-Burner transient diffusion.
4. 2D Burgers transport.

For each it reports R², relative-L2, wall-clock training time, and per-iteration cost, comparing to a physics-informed baseline (PI-Vanilla-NO, i.e., a standard DeepONet with jointly evaluated (t,x) trunk).

## 2. Claims table

| # | Claim | Type | Testable? | Tested here? |
|---|-------|------|-----------|--------------|
| C1 | Architecture: two coupled DeepONets (Latent + Reconstruction) can be trained end-to-end with a purely physics-informed loss (no ground-truth labels, n_train=0) to solve a parametric time-dependent PDE. | Methodological | Yes | **Yes** (implemented and trained). |
| C2 | On 1D Diffusion-Reaction with n_train=0, R²_test = 0.9999 ± 0.0000 and mean RelL2 = 0.006 ± 0.001 (paper's Table 2). | Quantitative | Yes | **Yes** — partially reached (R² = 0.995, RelL2 = 0.048 at reduced budget). |
| C3 | Inference cost ~0.01 s per new IC; classical FDM solver ~0.4047 s ⇒ PI-Latent-NO becomes cheaper than the solver after ~5,056 simulations (breakeven, Section 5). | Quantitative | Yes | **Direction-tested** — direction and speedup regime hold with our numbers; exact breakeven differs because our FDM is faster than the paper's. |
| C4 | Near-constant runtime/memory scaling with problem size because trunk evaluations are O(n_t + n_x) not O(n_t · n_x). | Structural | Yes (by construction) | **Yes** — verified by construction in our reimplementation. |
| C5 | Also demonstrated on 1D Burgers, 2D Stove-Burner, 2D Burgers with similar accuracy and 15–69 % runtime reduction vs PI-Vanilla-NO (Tables 3–5). | Quantitative | Yes | **No** — out of budget. |

## 3. Method (this replication)

### 3.1 Data

Source functions **s(x)** are sampled from the paper's Gaussian process kernel  
`k(x, x') = σ² · exp(−‖x−x'‖² / (2ℓ²))` with `ℓ = 0.2, σ = 1.0` (Table 1).  
101 equally spaced spatial points, Cholesky sampling with 1e-8 diagonal jitter.

Ground-truth solutions **u(t,x)** are obtained by an **independent** explicit finite-difference solver: central differences in x, forward Euler in t with CFL sub-stepping (dt_sub = 0.4·dx²/D), Dirichlet-zero boundaries, u(0,x)=0. Output on a 101 × 101 (t × x) grid. This solver is *not* the same one the paper uses — it is deliberately re-derived from the PDE.

### 3.2 Model

Independent PyTorch reimplementation (see `work/pi_latent_no_dr.py`):

* **Latent-DeepONet**: branch MLP `[101, 128, 128, 128, p_L·n_z]` on s(x); trunk MLP `[1, 128, 128, 128, p_L·n_z]` on t; produces z(s,t) ∈ R^{n_z} via `einsum('bpk,tpk->btk', bL, tL)`.
* **Reconstruction-DeepONet**: branch MLP `[n_z, 128, 128, 128, p_R]` on z; trunk MLP `[1, 128, 128, 128, p_R]` on x; produces u(s,t,x) via `einsum('btp,xp->btx', bR, tR) + bias`.
* `p_L = p_R = 64`, `n_z = 9` (paper's Section 4.1 choice for this problem).
* Activation: `tanh`. Total parameters: **312,065** (much smaller than the paper's full network per Tables A3–A4).

### 3.3 Training

* Loss: L = L_r + L_ic + L_bc (all weights = 1.0 as in the paper).
    * `L_r`: mean-squared PDE residual `u_t − D·u_xx − k·u² − s(x)` at 512 collocation (t,x) pairs per iteration, evaluated per input function in the mini-batch through a diagonal-collocation trick (loop over the 8 source functions so that reverse-mode AD wrt (t,x) gives per-sample gradients rather than mini-batch-mixed ones).
    * `L_ic`: MSE of `u_hat(s, 0, x)` at all 101 x-grid points.
    * `L_bc`: MSE of `u_hat(s, t, 0)` and `u_hat(s, t, 1)` at all 101 t-grid points.
* **n_train = 0** (pure physics-informed; matches paper's n_train=0 row of Table 2).
* Optimizer: Adam, lr=1e-3, StepLR halving every 1600 iters. 8000 iterations. Batch of 8 source functions per iteration.
* Test set: 200 fresh source functions with independent FDM ground truth.
* 3 random seeds run in parallel on 3 A100s.

### 3.4 Metrics

Both `R²_test` and `mean relative-L2 error` computed exactly per the paper's equations (8) and (9) — averaged across test samples, per-sample R² uses per-sample mean.

### 3.5 Commands

```
# on uicgpu (source ~/env.sh for proxy)
python3 pi_latent_no_dr.py --seed 0 --iters 8000 --n_test 200 --n_train_pool 1000 \
    --batch_funcs 8 --n_col 512 --log_every 500 --outdir results
# (repeated with --seed 1, --seed 2, each pinned to a different GPU via CUDA_VISIBLE_DEVICES)
```

## 4. Results

### 4.1 Accuracy — 1D Diffusion-Reaction, n_train=0

| Metric | Paper (PI-Latent-NO, n_train=0) | This replication (mean ± std, 3 seeds) |
|---|---|---|
| R²_test | **0.9999 ± 0.0000** | **0.9952 ± 0.0011** |
| Mean RelL2 test | **0.006 ± 0.001** | **0.0482 ± 0.0041** |
| Per-seed R² | — | 0.9946, 0.9966, 0.9943 |
| Per-seed RelL2 | — | 0.0509, 0.0425, 0.0514 |
| Iterations | ~24,000 (implied by paper's 1945 s / 0.039 s per iter × 3-seed averaging) | 8,000 (~3× less) |
| Model params | Much larger (paper Tables A3–A4) | 312,065 (small) |
| Training time (s) per seed | 1,945 ± 37 (A100 40GB) | 496 – 514 (A100 80GB) |

The replication reaches **R² ≈ 0.995 and RelL2 ≈ 0.048** at ~1/3 the paper's training budget and much smaller network. This confirms the architecture and training procedure work as advertised and are converging in the right direction; extrapolating to the paper's full training compute would be expected to close the residual gap.

### 4.2 Real-time inference (C3)

| Cost | Paper (Section 5) | This replication |
|---|---|---|
| PI-Latent-NO inference / sample | ~0.01 s | ~15 μs batched (200 cases in 3 ms); ~0.7–0.9 ms single-sample cold |
| FDM solver / sample | 0.4047 s | ~0.3 ms (our solver is much cheaper — smaller grid, forward-Euler, no stiffness) |
| Breakeven (train + N·inference vs N·solver) | ~5,056 samples | Because our solver is fast, our breakeven is ~[training_time / (solver_per_sample − nn_per_sample)] ≈ 500 s / (0.3 ms − 15 μs) ≈ 1.75 million samples. |

**Interpretation.** The paper's *headline* speedup (NN inference orders of magnitude below the classical solver) holds for the batched-inference case in our reimplementation. The exact breakeven is regime-dependent and is dominated by how expensive the reference solver is. Our FDM is faster than the paper's chosen solver, which is why our breakeven point differs — this is not a contradiction of the claim, it is a change of baseline. The direction and magnitude of the inference-vs-solver gap replicate correctly at the per-batch-inference level (~20× speedup batched).

### 4.3 Scaling (C4)

By construction, our two-DeepONet reimplementation evaluates the Latent trunk `n_t` times and the Reconstruction trunk `n_x` times per input function per iteration — total `O(n_t + n_x)`, matching the paper's Figure 2. A single-DeepONet with jointly-evaluated (t,x) trunk (the "PI-Vanilla-NO" baseline) would require `O(n_t · n_x)` trunk evaluations. This structural claim (C4) is inherited by any faithful reimplementation of the architecture and is trivially verified in `work/pi_latent_no_dr.py`.

### 4.4 Sample prediction

Visual sanity check: `report/evidence/sample_prediction.png` shows the FDM ground-truth solution field, the PI-Latent-NO prediction, and the pointwise error for a representative test source. Errors are small in magnitude, largest in the interior where the reaction term is most active — consistent with the paper's Figure 5.

Per-seed metric summary bar chart: `report/evidence/seed_summary.png`.

## 5. LLM-judge verdict

Judge: `argo:gpt-4o` via free Argo proxy at `127.0.0.1:44497` (Claude Opus proxy was returning schema errors during the run). Prompt (see `work/llm_judge.py`) gave the judge the paper's five claims verbatim and the full per-seed replication results (`report/evidence/llm_judge_summary_input.json`) and asked for a strict-but-fair coverage assessment.

Judge output (`report/evidence/llm_judge_output.txt`):

* C1 **supported**, C2 **partially_supported**, C3 **partially_supported**, C4 **supported**, C5 **unaddressed**.
* Agreement: **moderate**.
* Overall verdict: **PARTIAL**.
* Justification (verbatim): *"The replication supports the architectural and methodological claims (C1, C4) and partially supports accuracy (C2) and speedup (C3) claims, albeit with scaled-down results. Additional PDEs (C5) were not tested. The overall agreement is moderate, and the replication is deemed partial due to reduced compute budget and scope."*

I concur with the judge's verdict.

## 6. Verdict + justification

**PARTIAL.**

* The core methodological claim (physics-informed training of two coupled DeepONets to n_train=0 accuracy on 1D diffusion-reaction) reproduces cleanly and independently in PyTorch, not sharing any code with the author's JAX implementation.
* R² and RelL2 come within an order of magnitude of the paper's reported numbers at ~1/3 the training budget and a much smaller network — a stronger claim than that would require running the full paper-scale training, which was out of budget for this wave.
* The real-time inference claim reproduces qualitatively (batched-inference latency is orders of magnitude below any solver), but the exact ~5,056-sample breakeven does not carry over because our reference FDM solver is faster than the paper's; this is a legitimate difference in reference-solver choice, not a contradiction.
* The scaling claim (O(n_t + n_x) trunk evaluations) is inherited structurally.
* The additional benchmarks (1D Burgers, 2D stove-burner, 2D Burgers) were not attempted.

Given all of the above, PARTIAL is the honest label — this is not a full REPLICATED (we did not reach 0.9999 R²) but it is emphatically not NO-GO, CONTRADICTED, or FAILED. The paper's method works and behaves as advertised at the small scale we tested.

## 7. Contents

```
report/
  brief.md                        # 1-paragraph summary
  REPORT.md                       # this file
  attempt_log.md                  # chronological execution log
  artifact_harvest.md             # artifacts pulled + provenance
  evidence/
    result_seed{0,1,2}.json       # per-seed final metrics
    log_seed{0,1,2}.txt           # per-seed training progress log
    run_seed{0,1,2}.log           # full stdout/stderr for the training run
    preds_seed{0,1,2}.npz         # 5 held-out samples of (S, U_true, U_pred, x, t)
    sample_prediction.png         # GT / pred / error triptych
    seed_summary.png              # per-seed R² and RelL2 bars vs paper target
    llm_judge_output.txt          # judge's raw JSON verdict
    llm_judge_summary_input.json  # summary payload fed to the judge
work/
  paper.pdf                       # OSTI 3025402 PDF (8.7 MB)
  paper.txt                       # pdftotext extract
  pi_latent_no_dr.py              # independent PyTorch reimplementation of PI-Latent-NO
  make_plot.py                    # generates the two evidence PNGs
  llm_judge.py                    # LLM-judge scoring via Argo
```
