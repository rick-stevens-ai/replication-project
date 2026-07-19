# Failure Analysis — Pendse & Bhattacharyay 2016 replication

## Overall
No failures at the claim level: **12/12 claims reproduced**. The paper is an
analytic/variational theory paper with mostly closed-form results, so the bulk
of the replication is exact algebra verified numerically, plus one genuine
BVP solve. Below are the honest caveats about *what was and was not* replicated
from first principles.

## Bugs encountered and fixed
1. **numpy `bool_` not JSON-serializable.** `match` values from numpy comparisons
   are `numpy.bool_`, which `json.dump` rejects (Python 3.14 stdlib). Fixed by
   wrapping in `bool(...)`. One-line fix; no effect on physics.

## Scope caveats (things reproduced by construction / closed form, not by full solve)
1. **Thin-vortex scale selection is analytic, not a full non-local BVP.**
   We reproduce β = 1/(2√g₂) ~ 1/a from the paper's near-origin subleading
   balance (Eq.8) and the generalized β = 1/(a[(2|s|)!!]^{1/2|s|}) (Eq.9). These
   are the paper's own analytic selections; we verified them numerically and
   built the variational profile, but we did **not** independently solve the full
   non-local radial GP ODE (Eq.10 with the g₂/higher-derivative terms) as a
   self-consistent BVP. So "the thin branch exists" is reproduced at the level of
   the paper's variational argument, not by an independent stationary-profile
   solve. (This is Open Question #1.)
2. **Thin-vortex profile is the paper's two-piece variational ansatz.** α, λ, δ
   are the paper's closed forms; we verified C⁰ matching (diff ~1e-16) and the
   energy-minimizing α, but the profile is prescribed, not solved.
3. **Energy comparison is leading-order log scaling.** E_ξ₀ ~ ln(|s|D/ξ₀) and
   E_a ~ ln(D/(αa)) reproduce the paper's leading-order expressions (order-unity
   prefactors/constants dropped). This correctly captures the *qualitative*
   crossover (comparable at ξ₀~a, thick favoured at ξ₀≫a) but is not a full
   energy-functional evaluation with all subleading terms.
4. **Conventional-vortex core width** is reported via a (1−1/e) threshold proxy
   (1.30 ξ₀); the paper states "of order ξ₀" without a single canonical numeric,
   so this is an O(1) qualitative match, not a digit-for-digit one.
5. **Harmonic-trap case (paper Sec.V, Fig.2) not solved.** Only the uniform-BEC
   (untrapped) analysis was replicated. (Open Question #5.)

## What would strengthen this to a first-principles replication
- Full non-local radial GP BVP / imaginary-time propagation to independently
  produce a core-~a stationary profile and test its stability.
- Complete energy-functional integration (Eq.11) retaining subleading (an) terms
  to pin down the exact crossover boundary quantitatively.
- Trapped-vortex profile reproducing Fig.2.

## Honesty note
No numbers were fabricated. Every "PASS" corresponds either to an exact algebraic
identity (α, β, existence boundary) verified in code, a machine-precision matching
check, or a clearly-stated qualitative O(1) agreement with the paper's stated
scaling. Claims that rest on the paper's own analytic selections rather than an
independent solve are flagged above and in the open questions.
