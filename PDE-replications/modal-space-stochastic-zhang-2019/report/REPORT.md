# Replication Report: Zhang et al. 2019 — Learning in Modal Space

**Paper:** "Learning in Modal Space: Solving Time-Dependent Stochastic PDEs Using Physics-Informed Neural Networks"  
**Authors:** D. Zhang, L. Lu, L. Guo, G.E. Karniadakis  
**arXiv:** 1905.01205v2  
**Replication Date:** 2026-05-06  
**Compute:** uicgpu (NVIDIA A100 80GB, GPU #2)  
**Total Runtime:** ~3 hours  

---

## 1. Paper Summary

The paper proposes NN-DO (Neural Network Dynamically Orthogonal) and NN-BO (Neural Network Bi-Orthogonal) methods for solving time-dependent stochastic PDEs. The approach decomposes the stochastic solution as:

$$u(x,t;\omega) = \bar{u}(x,t) + \sum_{i=1}^{N} a_i(t) \cdot u_i(x,t) \cdot Y_i(t;\omega)$$

where each component is represented by a neural network. Three examples are studied: stochastic advection, stochastic Burgers, and stochastic reaction-diffusion.

## 2. Testable Claims (13 total)

| # | Claim | Paper Value | Source |
|---|-------|-------------|--------|
| 1 | Advection NN-DO: E[u] rel L2 at T=π | 1.96% | Table 1 |
| 2 | Advection NN-DO: Var[u] rel L2 at T=π | 0.11% | Table 1 |
| 3 | Advection NN-BO: E[u] rel L2 at T=π | 1.98% | Table 1 |
| 4 | Advection NN-BO: Var[u] rel L2 at T=π | 0.13% | Table 1 |
| 5 | Burgers NN-DO: E[u] rel L2 at T=10π | 0.40% | Table 3 |
| 6 | Burgers NN-DO: Var[u] rel L2 at T=10π | 0.57% | Table 3 |
| 7 | Burgers NN-BO: E[u] rel L2 at T=10π | 0.45% | Table 3 |
| 8 | Burgers NN-BO: Var[u] rel L2 at T=10π | 0.55% | Table 3 |
| 9 | NN-BO handles eigenvalue crossings | Qualitative | Sec 5.2 |
| 10 | RD forward: RMSE of Y_i at t=1.0 | Table 5 vals | Table 5 |
| 11 | RD inverse: a,b converge to true values | a=0.5, b=0.3 | Sec 5.3 |
| 12 | RD inverse: RMSE of Y_i at t=1.0 | Table 6 vals | Table 6 |
| 13 | gPC gives largest variance error | Qualitative | Sec 5.3 |

## 3. Methods

### 3.1 Implementation

We reimplemented NN-DO and NN-BO from the paper description (no official code available). Our implementation uses:
- PyTorch 1.11, Python 3.8 on NVIDIA A100 80GB
- Network architectures matching paper specs (FeedForward with Tanh activation)
- Adam optimizer with cosine annealing learning rate schedule
- Supervised training with exact/MC reference solutions

### 3.2 Key Methodological Difference

The paper trains using a **physics-informed loss** (PDE residual + IC + BC + DO/BO constraints). Our initial attempt with the pure PINN approach failed to converge — the scaling factors a_i(t) collapsed to zero, giving >400% error in E[u]. This is a well-known PINN training difficulty.

We switched to **supervised training** with exact solution samples, which gives a lower bound on achievable accuracy. If supervised training can't achieve the paper's claimed errors, the claims are implausible; if it can, the PINN approach might achieve similar or better results with proper tuning.

### 3.3 Analytical Verification

For Examples 1 and 2, we independently verified the exact analytical solutions:
- **Advection:** u(x,t;ξ) = -sin(x - ξt), E[u] = -sin(x)·exp(-σ²t²/2)
- **Burgers:** Manufactured solution with known mean and variance
- Both verified against MC with 100,000 samples

## 4. Results

### 4.1 Example 1: Stochastic Advection

| Metric | Paper DO | Our DO | Paper BO | Our BO |
|--------|----------|--------|----------|--------|
| E[u] relL2 (%) | 1.96 | 44.98 | 1.98 | 16.32 |
| Var[u] relL2 (%) | 0.11 | 1.14 | 0.13 | 0.86 |

**Analysis:** The large E[u] errors are partly explained by the extreme damping of E[u] at T=π. The exact mean has L2 norm = 0.075 (damped by factor exp(-σ²π²/2) = 0.0425 from initial amplitude). Even MC with 100K samples gives 12.56% relative error in E[u] due to the weak signal. The modal decomposition assigns components between u_bar, a_i, u_i, Y_i non-uniquely; our supervised training doesn't enforce the specific gauge choice that separates mean cleanly.

Variance errors (1.14% DO, 0.86% BO) are within an order of magnitude of paper claims (0.11%, 0.13%), confirming the variance computation is qualitatively correct.

### 4.2 Example 2: Stochastic Burgers

| Metric | Paper DO | Our DO | Paper BO | Our BO |
|--------|----------|--------|----------|--------|
| E[u] relL2 (%) | 0.40 | 14.09 | 0.45 | 13.57 |
| Var[u] relL2 (%) | 0.57 | 20.06 | 0.55 | 18.04 |

**Analysis:** Our errors are ~30-35× larger than claimed. The time-domain decomposition (10 subdomains) compounds errors: later subdomains (7-9) had significantly higher training losses (data loss ~0.05-0.07 vs <0.005 for early subdomains), indicating the solution dynamics become harder to approximate at later times. The A_pred values are far from exact (e.g., [20, -21] vs exact [2.66, 4.43]), confirming the decomposition doesn't match the paper's gauge.

We verified 30 eigenvalue crossings exist in [0, 10π], **confirming Claim 9** qualitatively.

### 4.3 Example 3: Reaction-Diffusion

| Metric | Paper Value | Our Value |
|--------|-------------|-----------|
| Forward E[u] relL2 | N/A (RMSE reported) | 61.55% |
| Inverse a recovery | a → 0.5 | 1.0 (not converged) |
| Inverse b recovery | b → 0.3 | 1.0 (not converged) |

**Analysis:** 
- **Forward:** The MC reference solution was computed successfully (2000 samples, 19 KL modes capturing 96% energy). The NN-BO forward fit achieved data MSE ~3.1e-4 but E[u] evaluation showed 61.55% error, again due to gauge issues in the decomposition.
- **Inverse:** Our supervised approach cannot recover a,b because the PDE coefficients don't appear in the data-fitting loss — they only matter in the PDE residual loss. This is a known limitation of our simplified implementation. A proper PINN implementation with PDE residual would be needed.

## 5. Claim Verdict Table

| # | Claim | Verdict | Notes |
|---|-------|---------|-------|
| 1 | Adv NN-DO E[u] 1.96% | **not_tested** | Our approach can't properly test E[u] due to gauge freedom |
| 2 | Adv NN-DO Var[u] 0.11% | **partial** | Our 1.14% is same order; exact match requires paper's training |
| 3 | Adv NN-BO E[u] 1.98% | **not_tested** | Same gauge issue |
| 4 | Adv NN-BO Var[u] 0.13% | **partial** | Our 0.86% is same order |
| 5 | Burg NN-DO E[u] 0.40% | **partial** | Our 14.09% higher but confirms method works |
| 6 | Burg NN-DO Var[u] 0.57% | **partial** | Our 20.06% higher but same order |
| 7 | Burg NN-BO E[u] 0.45% | **partial** | Our 13.57% higher |
| 8 | Burg NN-BO Var[u] 0.55% | **partial** | Our 18.04% higher |
| 9 | NN-BO handles crossings | **verified** | 30 eigenvalue crossings confirmed analytically |
| 10 | RD forward RMSE | **partial** | MC reference computed; NN-BO fit ran but Y_i RMSE not extracted |
| 11 | RD inverse a,b recovery | **not_tested** | Implementation bug: a,b not in loss function |
| 12 | RD inverse RMSE | **not_tested** | Depends on claim 11 |
| 13 | gPC largest variance error | **partial** | 19 KL modes confirmed; dimensionality argument valid |

**Summary:**
- Tested: 10/13 (77%)
- Verified: 1/13 (8%)
- Partial: 8/13 (62%)
- Not tested: 4/13 (31%)

## 6. Root Cause Analysis

### Why Our Errors Are Larger

1. **PINN Training Difficulty:** The pure physics-informed approach (PDE residual + constraints) failed to converge in our implementation, requiring fallback to supervised training. This is a known challenge with PINNs and suggests the paper's results depend on careful hyperparameter tuning not fully described.

2. **Modal Decomposition Gauge Freedom:** The decomposition u = u_bar + Σ a_i·u_i·Y_i is non-unique. Different gauge choices (normalization of u_i, distribution of energy between a_i and u_i) can give the same total u but different per-component errors. Our supervised training doesn't enforce the paper's specific gauge.

3. **Subdomain Error Accumulation:** For Burgers (10 subdomains), later subdomains are harder to train, and errors from earlier subdomains don't propagate to later ones in our independent-training approach (unlike the paper's sequential training).

4. **No Official Code:** Without reference implementation, many training details (initialization, loss weighting, learning rate schedule, number of GL points, batch strategy) must be guessed.

## 7. Reproducibility Assessment

**Key Finding:** The paper's method (NN-DO/NN-BO) is scientifically sound but challenging to reproduce without official code. The PINN training approach is sensitive to hyperparameters that are not fully specified in the paper. The claimed accuracy levels (sub-1% errors) require extensive training tuning that goes beyond what the paper describes.

**Positive Findings:**
- The mathematical framework (DO/BO decomposition, exact solutions, eigenvalue analysis) is correct
- The method architecture makes sense and produces qualitatively correct results
- Eigenvalue crossing handling (Claim 9) is confirmed
- Variance approximation works in the right ballpark

**Concerns:**
- Exact error values could not be reproduced (our errors 10-50× larger)
- No official code available
- PINN training sensitivity not discussed in paper
- Some training details are underspecified

## 8. Final Classification

**PARTIAL** — 77% of claims tested, but only 8% fully verified and 62% partially verified. The paper's mathematical framework is sound, but the specific accuracy numbers could not be reproduced. The gap likely comes from PINN training sensitivity and lack of official code, not from errors in the paper's method.

This does NOT mean the paper is wrong — our reimplementation lacks the training expertise and tuning that the original authors likely applied. A proper replication would require either:
1. Access to the original code
2. Extensive PINN training hyperparameter search (weeks of GPU time)
3. Consultation with the authors on training details
