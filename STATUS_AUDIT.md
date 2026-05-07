
## 28589945 — Jiang et al. 2017 (ARG dissemination)
**Verdict: REPLICATED** | 56/56 proteins (100%) | 23/32 claims tested (72%) | 17 verified, 3 partial, 0 contradicted | Mean BLASTP Δ=0.3%

## BVBRC-01 — Zhang et al. 2022 (ST11 CRKP genomic evolution)
**Verdict: REPLICATED** | 955/955 genomes (100%) | 18/20 claims tested (90%) | 8 verified, 9 partial, 0 contradicted | KL47→KL64 transition confirmed (Kleborate v3.2.4)

## jax-cfd — Kochkov et al. 2021 (ML-accelerated CFD)
**Verdict: REPLICATED** | 5/8 scope units (63%, core results covered) | 12/14 claims tested (86%) | 11 verified, 1 partial, 0 contradicted | LI(64) matches DNS256–512 accuracy (~4–8× resolution equiv); author's released model outputs independently confirm 8–10× claim; stability verified over 2000 frames

## fem-vs-pinns — Grossmann et al. 2023 (Can PINNs Beat the Finite Element Method?)
**Verdict: REPLICATED** | 5/6 problems tested (83%) | 11/12 claims verified (92%) | FEM beats PINNs on every tested problem: 8.8×–7900× accuracy advantage, 1.5×–3900× speed advantage | 3D Poisson and 1D Schrödinger unblocked by self-generating ground truth | Coverage: 8/10, Agreement: 9/10

## pinn-rans-eivazi-2022 — Eivazi et al. 2022 (PINN-RANS)
**Verdict: PARTIAL** | 3/5 cases attempted (60%), 2 data-blocked | 14/25 claims tested (56%), 11 data-blocked (100% accounted for) | 0/14 quantitative claims reproduced within tolerance (errors 4–67× higher) | 5/5 qualitative claims confirmed | Primary blocker: unavailable DNS/LES reference datasets from KTH | Coverage: 6/10, Agreement: 5/10

## pinn-domain-decomp-2023 — Kopaničáková et al. 2023 (Domain-Decomposition PINNs)
**Verdict: PARTIAL** | 3/4 test cases complete (75%) | 15/18 claims evaluated, 10 verified + 5 partial (83% confirmed) | MSPQN achieves 5–44× lower loss than L-BFGS (core contribution confirmed) | Absolute E_rel ~100× higher than paper due to unavailable custom L-BFGS optimizer | Coverage: 7/10, Agreement: 7/10

## modal-space-stochastic-zhang-2019 — Zhang et al. 2019 (Learning in Modal Space)
**Verdict: PARTIAL** | 3/3 examples attempted | 10/13 claims tested (77%), 1 verified, 8 partial | Eigenvalue crossings verified (key qualitative claim) | Absolute errors 20–35× higher than paper: advection E[u] 44.98% vs 1.96%, Burgers E[u] 14.09% vs 0.40% | Root causes: PINN training failure (fallback to supervised), gauge freedom in modal decomposition, no official code | Coverage: 7/10, Agreement: 5/10
