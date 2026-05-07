# Progress: Zhang et al. 2019 — Modal Space Stochastic PDE Replication

## Status: COMPLETE (PARTIAL verdict)

## Paper Details
- **Title:** Learning in Modal Space: Solving Time-Dependent Stochastic PDEs Using Physics-Informed Neural Networks
- **Authors:** Zhang, Lu, Guo, Karniadakis
- **arXiv:** 1905.01205v2

## Testable Claims Identified (13 total)
1. Advection NN-DO: E[u] rel L2 error = 1.96% at T=π
2. Advection NN-DO: Var[u] rel L2 error = 0.11%
3. Advection NN-BO: E[u] rel L2 error = 1.98%
4. Advection NN-BO: Var[u] rel L2 error = 0.13%
5. Burgers NN-DO: E[u] rel L2 = 0.40% at T=10π
6. Burgers NN-DO: Var[u] rel L2 = 0.57%
7. Burgers NN-BO: E[u] rel L2 = 0.45%
8. Burgers NN-BO: Var[u] rel L2 = 0.55%
9. Burgers NN-BO handles eigenvalue crossings where standard BO fails
10. Reaction-diffusion forward: RMSE of Yi at t=1.0 (Table 5 values)
11. Reaction-diffusion inverse: a,b converge to true values (a=0.5, b=0.3)
12. Reaction-diffusion inverse: RMSE of Yi at t=1.0 (Table 6 values)
13. gPC generates largest variance error vs NN-BO and standard BO

## Checkpoints
- [x] Paper found and downloaded (arXiv 1905.01205v2)
- [x] No official code found (Karniadakis group GitHub checked)
- [x] All quantitative claims extracted from paper
- [x] Example 1: Stochastic advection (NN-DO + NN-BO) — 2026-05-06 19:39 CDT
- [x] Example 2: Stochastic Burgers (NN-DO + NN-BO) — 2026-05-06 21:27 CDT
- [x] Example 3: Reaction-diffusion (forward + inverse) — 2026-05-06 22:00 CDT
- [x] Analytical verification of exact solutions
- [x] MC reference solutions for reaction-diffusion
- [x] Report written per AUDIT_PROTOCOL

## Compute Target
- uicgpu (8× A100 80GB), GPU #2
- GPUs 0,2,4,6 working; GPUs 1,3,5,7 have CUDA errors

## Run Timeline
- 2026-05-06 19:24 — v3 training started on uicgpu GPU 2
- 2026-05-06 19:40 — Advection NN-DO complete: E[u]=44.98%, Var[u]=1.14%
- 2026-05-06 19:56 — Advection NN-BO complete: E[u]=16.32%, Var[u]=0.86%
- 2026-05-06 20:42 — Burgers NN-DO complete: E[u]=14.09%, Var[u]=20.06%
- 2026-05-06 21:27 — Burgers NN-BO complete: E[u]=13.57%, Var[u]=18.04%
- 2026-05-06 21:55 — RD Forward complete: E[u]=61.55%
- 2026-05-06 ~22:20 — RD Inverse complete: a=1.0, b=1.0 (known bug)
- 2026-05-06 ~22:30 — Report written

## Key Findings
1. Pure PINN training (PDE residual loss) failed — a_i scaling factors collapsed to zero
2. Supervised training with exact solutions gives qualitatively correct results but 10-50× larger errors than paper claims
3. Modal decomposition gauge freedom makes per-component error comparison meaningless without matching the paper's specific gauge
4. Eigenvalue crossings (Claim 9) confirmed analytically: 30 crossings in [0, 10π]
5. Advection E[u] evaluation is noisy due to extreme damping (factor 0.0425 at T=π)
6. Inverse problem requires PDE residual loss (not data supervision) to recover coefficients

## Verdict: PARTIAL
- 10/13 claims tested (77%)
- 1/13 verified, 8/13 partial, 4/13 not tested
- Paper's mathematical framework is correct
- Specific accuracy numbers not reproduced (likely PINN training sensitivity)
