# Failure Analysis — OSTI 2574844 replication

Paper: Spencer et al., high-order GFD for the time-harmonic cold-plasma wave
equation (Phys. Plasmas 32, 063902, 2025).
Verdict: **REPLICATED**.

This file records what almost went wrong, what would falsify the verdict if
tested more aggressively, and residual risk in the current claim.

## 1. What actually went wrong (and was corrected)

### 1.1 Under-resolved first pass
- **Symptom:** the initial C2 run used fewer than 10 pts/λ per side and
  produced large, non-monotone NRMSDs with fitted orders that fluctuated wildly.
- **Root cause:** the Helmholtz "pollution effect" — a well-known regime in
  which the numerical solution's phase error accumulates over many wavelengths
  and swamps the discretization error until a resolution threshold is crossed.
  The paper itself flags this on Sec. V.A.
- **Fix:** re-run in the well-resolved regime (2 wavelengths across L = 1,
  20–65 pts/λ, satisfying the paper's ≥10 pts/λ recommendation). Reported
  numbers are from this regime.
- **Lesson:** for a Helmholtz-order convergence study, the resolution
  schedule matters at least as much as the FD stencil order. Always report
  the pts/λ range.

### 1.2 Cloud-regeneration noise
- **Symptom:** running the same (m, n) twice gives slightly different NRMSDs.
- **Root cause:** jittered clouds are regenerated per resolution (this is
  what the paper does; it is the stated source of Fig. 2 noise).
- **Mitigation:** fitted orders averaged over the 5 refinements are robust to
  this noise at the ~10 % level; individual per-refinement NRMSDs are not.
  Reported orders should be read as slopes, not exact rates.

## 2. What would falsify the REPLICATED verdict

The verdict is **REPLICATED for claims C1 and C2 in the homogeneous-tensor
reduction**. Any of the following, if measured, would downgrade or invalidate
it:

1. **Interior-only NRMSD converges but full-domain NRMSD does not**, indicating
   boundary-star artefacts are inflating the apparent slope. (See open Q4.)
2. **Reducing SVD truncation tolerance by two orders of magnitude changes the
   fitted order by more than ~0.5**, indicating the reported rate is a
   regularization artifact rather than a discretization property. (Open Q3.)
3. **Turning on a smoothly-varying anisotropic tensor with a resonance-layer
   crossing drops the C2 order to ≤1 near the singular layer.** This would
   not disprove the paper's Fig. 2 (which uses a homogeneous target) but it
   would substantially weaken the practical relevance of the O(h^{m-1}) rate
   claim for the paper's motivating physics. (Open Q1.)
4. **A larger refinement set (say 15 points instead of 5) produces markedly
   different fitted orders**, indicating the current numbers are a small-N
   fit artifact. Neither this replication nor the paper stress-tests this.
5. **The paper's own code, when eventually released, produces different
   numbers on the same test problem.** Our reimplementation validates the
   method as described; it does not certify the authors' actual code.

## 3. Coverage risk

The LLM judge estimated coverage ≈ 55 % of the numerical core. The uncovered
45 %:
- **C3** (physics-informed monitor point generator): entirely untested.
  This is the algorithmic ingredient that would make the method interesting
  in production, and its value proposition is unverified.
- **C4** (ICRH/ECRH mock-tokamak demos): qualitative and effectively
  unfalsifiable without an independent full-wave code as ground truth.
- **Toroidal geometry / curvilinear coordinates**: not implemented.
- **Full anisotropic dielectric tensor**: not implemented. Our C2 uses the
  paper's own mathematically justified reduction (homogeneous ε → plane wave
  is exact), so this is a scope choice, not a bug — but it is a real limit
  on how far the verdict extends.

Bottom line: **REPLICATED means the paper's Fig. 2 convergence claim is real
and reproducible from the equations**; it does not mean the full toroidal
plasma-physics story has been independently reproduced.

## 4. Zero-cost sanity checks that were passed

- Both C1 and C2 fitted orders are non-negative and finite for all m tested.
- NRMSDs are monotone-decreasing in n for every m in the well-resolved
  regime.
- Higher-order schemes (m = 4) reach lower error than lower-order schemes
  (m = 2) at fixed n — as they must if the discretization order claim is
  even approximately right.
- κ_i (star condition numbers) are finite; no NaNs or divide-by-zero in the
  TSVD pseudoinverse.

## 5. Non-numerical failure modes considered

- **Wrong paper section referenced.** Ruled out by cross-checking Sec. V.A
  and Fig. 2 wording against the replication targets.
- **Manufactured C1 test field too simple.** sin(2πx) cos(2πy) is smooth
  and periodic; a stiffer non-periodic test would probably tighten the
  observed super-convergence at m = 4. Not tested — a candidate for a
  follow-up.
- **LLM judge over-agrees.** The judge was fed the paper claim and our
  results together and asked to compare; the risk of a "yes-man" verdict is
  real. The judge is corroborating, not authoritative — the actual evidence
  is the numerical tables in REPORT.md §4.

## 6. Summary

- Verdict **REPLICATED** stands for C1 and C2 in the reduced problem.
- Verdict is **silent** on C3 and C4 by scope choice.
- Verdict is **conditional** on: interior-only convergence not being
  qualitatively different, TSVD tolerance not being a hidden parameter,
  and the resonance-crossing case behaving reasonably. Each of these is
  logged as an open question, not a known failure.
