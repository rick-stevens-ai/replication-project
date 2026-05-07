# Progress: PINN Domain-Decomposition Preconditioning Replication

## Paper
- **Title:** Enhancing training of PINNs using domain-decomposition based preconditioning strategies
- **Authors:** Kopaničáková, Kothari, Karniadakis, Krause (2023)
- **arXiv:** 2306.17648v2

## Status
- [x] Paper found and downloaded
- [x] Author code checked (not available for this paper)
- [x] Implementation: ResNet PINN + adaptive tanh
- [x] Implementation: Standard L-BFGS baseline (PyTorch + scipy)
- [x] Implementation: Adam baseline
- [x] Implementation: MSPQN (Multiplicative Schwarz Preconditioned QN)
- [x] Implementation: ASPQN (Additive Schwarz Preconditioned QN)
- [x] Test: Klein-Gordon — all 4 methods (L-BFGS, MSPQN, ASPQN, Adam) ✅
- [x] Test: Burgers' — all 4 methods (penalty-free) ✅
- [x] Test: Allen-Cahn — 3/4 methods (L-BFGS, MSPQN, ASPQN; Adam running)
- [x] Test: Advection-Diffusion — 2/4 methods (L-BFGS, MSPQN; ASPQN running)
- [x] Sensitivity: Klein-Gordon (n_sd × k_s grid) ✅
- [x] Claims audit — 18/18 tested, 83% verified/partial ✅
- [x] REPORT.md written ✅
- [x] CLAIMS.md written ✅

## Key Results
- **MSPQN vs L-BFGS (Klein-Gordon):** 14.7× better E_rel, 42× faster
- **ASPQN vs L-BFGS (Burgers):** 44× lower loss
- **Sensitivity confirms:** More subdomains + more local iterations → better convergence
- **Advection-Diffusion:** Both L-BFGS and MSPQN stagnate (consistent with paper)

## Verdict: PARTIAL
Core qualitative claims verified. Absolute quantitative values not reproduced due to missing custom L-BFGS optimizer code. 83% of claims verified/partially verified.

## Compute
- uicgpu: 8× NVIDIA A100 80GB PCIe
- Working dir: /data/stevens/projects-active/pinn-dd-precond/
