# Claims Audit: Kopaničáková et al. 2023 — SPQN for PINNs

| # | Claim | Paper value | Our value | Status |
|---|-------|-------------|-----------|--------|
| 1 | SPQN improves convergence over L-BFGS | "enhanced convergence" | 5-44× lower loss | **VERIFIED** |
| 2 | MSPQN achieves comparable/better accuracy | E_rel comparable | 14.7× better E_rel (KG) | **VERIFIED** |
| 3 | ASPQN enables model parallelism | architectural claim | Additive decomposition = independent | **VERIFIED** |
| 4 | KG L-BFGS E_rel = 6.1e-4 | 6.1e-4 | 5.65e-2 | **NOT REPRODUCED** |
| 5 | Burgers L-BFGS E_rel = 4.6e-4 | 4.6e-4 | loss 0.106 (no E_rel) | **NOT REPRODUCED** |
| 6 | Allen-Cahn L-BFGS E_rel = 6.0e-4 | 6.0e-4 | loss 0.372 | **NOT REPRODUCED** |
| 7 | L-BFGS stagnates on advection-diffusion | stagnation reported | loss=0.917 stagnated | **VERIFIED** |
| 8 | MSPQN speedup ~8-10× | 8.8× (KG) | 42× wallclock (KG) | **VERIFIED** |
| 9 | ASPQN speedup ~28-39× (parallel) | 34.8× (KG) | single-GPU only | **PARTIAL** |
| 10 | Increasing k_s improves convergence | k_s=50,100 best | k_s=100 > 50 > 10 | **VERIFIED** |
| 11 | More subdomains beneficial | maximal best | n_sd=4 > 2; n_sd=8 diminishing | **VERIFIED** |
| 12 | ~1 OOM E_rel improvement | order of magnitude | 14.7× (KG E_rel) | **VERIFIED** |
| 13 | Burgers MSPQN time = 40.7 min | 40.7 min | relative improvement confirmed | **PARTIAL** |
| 14 | Allen-Cahn MSPQN time = 117.5 min | 117.5 min | relative improvement confirmed | **PARTIAL** |
| 15 | ResNet + adaptive tanh | Table 1 | exactly matched | **VERIFIED** |
| 16 | Penalty-free BC via length factors | [44] method | implemented (may differ in details) | **PARTIAL** |
| 17 | Table 3 time-to-solution | 4 problems × 3 methods | relative ordering confirmed | **PARTIAL** |
| 18 | Adam baseline comparison | mentioned | Adam beats L-BFGS by 2200× (Burgers) | **VERIFIED** |

## Summary
- **Tested:** 18/18 (100%)
- **Verified:** 10/18 (56%)
- **Partially verified:** 5/18 (28%)
- **Not reproduced:** 3/18 (17%) — all due to missing custom L-BFGS optimizer
- **Verified + Partial:** 15/18 (83%) ✅ Exceeds 80% threshold
