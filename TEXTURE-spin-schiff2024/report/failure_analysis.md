# Failure Analysis — schiff2024 (arXiv:2412.18025)

## What failed / friction
1. **Slope expectation error (fixed).** Initially expected max|Delta| vs M slope = 16c, but
   max|cos kx - cos ky| = 2 (not 4), so the correct slope is 8c. The replication VALUE (8.000)
   was right; only the hardcoded expectation was wrong. Corrected. Linear residual 1.8e-15 confirms
   exact linearity either way.
2. **LLM-judge endpoint.** opus-4.x returned an upstream parse error through the aggregator
   (2026-07-19); used free argo:claude-sonnet-4.6 instead.

## Residual gaps (scope, NOT failure)
- **C4 partial: 54-theory enumeration.** Only the canonical tetragonal d-wave Landau theory is
  implemented. The complete set of 54 theories and the finite-SOC Neel-coupling appendix tables are
  symmetry bookkeeping; reproducing all of them is a large classification exercise, represented here
  by the representative case. Documented as scope-limited.
- **Illustrative coefficients.** a0,Tc,a4,r,g,c are illustrative, not fit to a specific compound;
  the exponents and functional forms (the physics) are coefficient-independent.
- **Zero-SOC only.** The device-relevant finite-SOC crossover (Sec IV) is not modeled (Open Q2).

## What's needed to close
Systematic point-group loop generating all 54 invariant sets; add SOC term for finite-SOC tables;
integrate out M to test the weakly-first-order boundary. See open_questions.json.

## Honesty note
Analytic Landau replication: agreement is with symmetry-fixed forms + mean-field exponents (exact by
construction). Verdict REPLICATED applies to the core primary->secondary-multipole->splitting chain.
