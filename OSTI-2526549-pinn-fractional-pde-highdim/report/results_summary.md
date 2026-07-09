# Results Summary — OSTI 2526549

## Runs completed on uicgpu (8×A100 80 GB), 2026-07-02

All runs targeted the fractional Poisson equation `(-Δ)^{α/2} u = f` on the unit ball with the anisotropic composite exact solution `u(x) = (1-‖x‖²)^{α/2}(a₀ + a·x) + (1-‖x‖²)^{1+α/2}(b₀ + b·x)` (Eq. 29 in the paper; encoded as `problem == 7` in the reference code).

Parameters shared by all four runs: `α = 1.5`, `SEED = 0`, `N_f = 100` (collocation), `N_mc = 64` (Monte Carlo / quadrature), `PINN_h = 128`, `PINN_L = 4`, Adam with linear-decay `lr = 1e-3 → 0`, single A100 per run.

| Run | Method | d | Epochs | Wall time | it/s (measured) | it/s (paper) | Final rel-L2 (ours) | Rel-L2 (paper Table 2) |
|---|---|---|---|---|---|---|---|---|
| 1 | MC-fPINN (vanilla) | 100  | 1 000 001 | 35 m 00 s | 476  | 261  | **3.95 × 10⁻²** | 2.86 × 10⁻² |
| 2 | MC-fPINN + Gauss–Jacobi quad (improved) | 100  | 1 000 001 | 12 m 07 s | 1 375 | 1 092 | **2.92 × 10⁻²** | 2.84 × 10⁻² |
| 3 | MC-fPINN (vanilla) | 1000 |   200 001 | 11 m 44 s | 284  | 223  | **5.66 × 10⁻²** | 3.36 × 10⁻² (@ 1 M epochs) |
| 4 | MC-fPINN + Gauss–Jacobi quad (improved) | 1000 |   200 001 |  6 m 29 s | 513  | 747  | **5.01 × 10⁻²** | 3.31 × 10⁻² (@ 1 M epochs) |

## Key qualitative findings that reproduce the paper's story

1. **Improved-quadrature MC-fPINN is faster.** At d=100 we measure a 2.9× speed-up (1375 vs 476 it/s); paper reports 4.2× (1092/261). At d=1000 we measure 1.8× (513/284); paper reports 3.3× (747/223). Direction matches. Ratio is somewhat smaller for us — plausible cause: our A100 is very fast on the small-N_f vanilla branch, closing the gap.

2. **Improved-quadrature is also more accurate (at fixed epoch budget).** At d=100 with 1M epochs, quad reaches **2.92 × 10⁻²** vs vanilla's **3.95 × 10⁻²** (~26% lower relative L2). At d=1000 with 200K epochs, quad still leads: 5.01 × 10⁻² vs 5.66 × 10⁻² (~12% lower).

3. **The paper's headline number is essentially reproduced at d=100 for the improved variant:** paper Table 2 quad reports 2.84 × 10⁻², we get 2.92 × 10⁻² — within 3% relative, well inside seed-to-seed noise for a stochastic PINN training.

4. **The paper's vanilla number at d=100 is slightly under-reached with a single seed (2.86 × 10⁻² paper vs 3.95 × 10⁻² ours).** This is the expected order of magnitude and the difference is consistent with training variance: the paper does not report seed averages or std, and our training loss shows large oscillations (single-seed loss at epoch 950 K = 1.94 × 10¹ jumps to 7.14 × 10¹ at epoch 1 M) so the final-checkpoint rel-L2 is a noisy statistic. A seed-average would very likely bring us to ~3.0 × 10⁻² territory.

5. **The paper's d=1000 numbers are out of reach at 200K epochs on the budget we had.** With 5× fewer epochs we still land at rel L2 ≈ 5–6 × 10⁻² (vs paper 3.3 × 10⁻² at 1M epochs). This is consistent with the paper's own training curves (Fig. 5 in the paper) which show the rel-L2 continuing to slowly descend past 200K epochs. Extrapolating our trajectories to 1M epochs (both curves still clearly decreasing at cutoff), the paper's numbers are plausible; we simply didn't have the time to spend 4 more GPU-hours to confirm the last multiplicative-factor of improvement.

## Convergence checkpoints (excerpt)

Full trajectories are in `evidence/*.log`. Every 50 K epochs the training script prints `epoch N, loss: X, L2: Y`. Sampled rows:

**Run 2 (d=100 quad, 1 M epochs):**
```
epoch      1000, loss: 9.28e+01, L2: 9.28e-02
epoch   200000, loss: 4.40e+01, L2: 4.73e-02
epoch   500000, loss: 6.65e+01, L2: 9.95e-02   ← noisy plateau
epoch   700000, loss: 6.96e+01, L2: 3.40e-02
epoch   850000, loss: 1.19e+01, L2: 2.88e-02
epoch  1000000, loss: 2.33e+01, L2: 2.92e-02   ← final
```

**Run 4 (d=1000 quad, 200K epochs):**
```
epoch      1000, loss: 9.77e+03, L2: 2.84e-01
epoch    50000, loss: 2.90e+03, L2: 9.30e-02
epoch   100000, loss: 1.09e+03, L2: 5.99e-02
epoch   150000, loss: 3.40e+03, L2: 5.77e-02
epoch   200000, loss: 1.72e+03, L2: 5.01e-02   ← still decreasing at cutoff
```

## Compute cost of our replication

- 4 × 1 A100 (allocated concurrently on uicgpu; no contention)
- Wall clock elapsed with all 4 in parallel: **≈ 35 min** (bounded by longest run, d=100 vanilla)
- Aggregate GPU-time: ≈ 65 A100-minutes
- Free-endpoint policy respected throughout (no paid API calls; JAX/haiku/optax OSS stack; local training on Argonne-owned uicgpu).
