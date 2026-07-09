# Failure analysis — Kou (2002) replication

Verdict: **REPLICATED**. Numerical benchmark reproduced to `~1e-6`. This document catalogues what did *not* work and what remains unresolved despite the overall REPLICATED verdict.

## 1. Primary failure: literal Hh-based Theorem 2 pricer

### What we tried
Directly transcribed Kou (2002) Appendix B.1 Theorem B.1 into code:
- The `Hh_n(x)` special-function recursion (`Hh_{n+1}(x) = (Hh_{n-1}(x) - x·Hh_n(x)) / (n+1)` with initial `Hh_{-1}(x) = e^{-x^2/2}` and `Hh_0(x) = sqrt(2π)·Φ(-x)`).
- The `I_n(c; α, β, δ)` integral-assembly formula (which combines the incomplete gamma / mixed-gamma pieces into the closed-form probability `Υ(μ, σ, λ, p, η1, η2; a, T)`).
- The double series over Poisson counts and jump-count decompositions from Theorem B.1.

Wired into the Theorem 2 (eq. 20) call-price formula.

### What went wrong
- Direct implementation diverged from paper's `C = 9.14732` by **>20 %** at the footnote-9 parameters.
- A publicly available StackOverflow reference implementation of the Hh pricer produced a similarly wrong number, so this is not a niche bug of ours alone — the Hh assembly is genuinely hard to get right from paper text alone.

### Diagnosed root cause (probable)
- **Backward recursion instability of `Hh_n`**: for large negative arguments, `Hh_n` grows very fast, so backward recursion accumulates catastrophic cancellation. The correct stable direction depends on the argument regime; a single naïve recursion cannot be right everywhere.
- **Sign-convention ambiguity in `I_n(c; α, β, δ)`**: the `I_n` formula involves several conditional-sign branches and terms with `(-1)^k` factors that are easy to mis-transcribe from OCR'd PDF text.

### What would fix it
- Symbolic re-derivation of the recursion + stability analysis by argument regime.
- Use `mpmath` at arbitrary precision as a ground-truth cross-check for individual `Hh_n(x)` and `I_n(c; …)` values.
- Verify against a small hand-computed toy case (`n=0, 1, 2`) before scaling up.

### Impact on the replication verdict
- **None on the price itself.** The characteristic-function + Fourier-cosine (COS) inversion route (mathematically equivalent — both invert the same `φ_X`) reproduces `9.14732` to `2.7 × 10^-6`.
- **Non-zero on completeness.** The paper's *specific implementation recipe* (Hh series) is not independently vetted here. What is vetted is the *risk-neutral price*, via a different but provably-equivalent path.
- Reported honestly in `REPORT.md` §2 (row `C1'`) and §5 (last paragraph), and in `REPORT.tex` §7 (Genuine critique).

## 2. Coverage gap: only the footnote-9 parameter set exercised for the paper benchmark

- Kou (2002) contains additional numerical tables (comparisons vs Merton normal jumps, sensitivity to jump-tail asymmetry `η1 / η2`, etc.) that were not re-run.
- The 5-strike sensitivity sweep varies `K` only; `σ, λ, p, η1, η2` were held fixed at footnote-9 values.
- No sweep over the jump intensity `λ`, up/down jump asymmetry `p`, or tail decay parameters `η1, η2`.
- **Impact**: the LLM-judge coverage grade is `B` (not `A`) specifically because of this. Verdict still REPLICATED because agreement on the one benchmark that *is* tested is essentially perfect via multiple independent routes.

## 3. Empirical / practical claims: entirely untested

- The paper's principal *practical* motivation is that the double-exponential jump distribution fits observed leptokurtic equity return distributions and implied-volatility smiles better than Merton normal jumps.
- No market data was downloaded. No smile was calibrated. No head-to-head vs Merton or Heston on real option chains was performed.
- **Impact**: the whole practitioner case for the model is untested. This is a bounded scope decision (replicate the *mathematical* claim first), not an oversight — but it should be flagged clearly, and it is (`REPORT.md` §5; `REPORT.tex` §7.3).

## 4. PIDE route is only at `O(10^-2)` — plausibility check, not tight independent witness

- Explicit-Euler finite-difference solver on a `N_x = 601`, `N_t = 20,000` grid gave `9.16756` vs the paper's `9.14732` — error `~2 × 10^-2` on a `~9.15` price (i.e. `~0.2 %`).
- Consistent with the expected discretisation order of the scheme, but **not tight enough** to independently distinguish e.g. a sign error in the drift-correction term `-λζ` from a `~1 %` FD artefact.
- No Richardson-extrapolation convergence study was performed.
- **Fix path**: Crank-Nicolson time-stepping + implicit (or FFT-based) jump-kernel convolution + Richardson extrapolation → should tighten to `~10^-4` and turn PIDE into a true third-witness route rather than a sanity check.

## 5. COS payoff coefficients `U_k` not symbolically re-derived

- The analytic Fourier-cosine coefficients of the European call payoff on `[0, b]` (Fang-Oosterlee 2008 formulas) were implemented as coded from the paper, not re-derived from scratch.
- A sign or normalisation bug in `U_k` that happened to cancel at the footnote-9 parameter set would be invisible to the tests here.
- **Partial mitigation**: the Black-Scholes limit test (`λ = 10^-10`) matches to `10^-12` against analytic BS, which does independently constrain `U_k` correctness in the degenerate (no-jump) regime. But degenerate-model agreement is a weaker check than a full symbolic re-derivation.

## 6. LLM-judge is a single scorer, not an audit

- Verdict rubric scored by exactly one LLM (`argo:claude-opus-4.7`) on pre-summarised numerical inputs.
- Not an independent audit. The load-bearing evidence is the numerical agreement itself.
- No cross-check against a second LLM (e.g. `argo:gpt-5.x` or `nemotron-3-ultra`) was done.

## Summary

| # | Failure | Severity | Impact on REPLICATED verdict |
|---|---|---|---|
| 1 | Literal Hh Theorem 2 recursion — implementation wrong | high (paper-implementation completeness) | **none on price**; flagged as caveat |
| 2 | Only footnote-9 params exercised for benchmark | medium | drops coverage grade A → B |
| 3 | Empirical smile-fit claims untested | high (practical scope) | out of stated scope |
| 4 | PIDE only at O(1e-2) — plausibility not third witness | low-medium | verdict still safe (two independent routes agree to `1e-6` and MC-error) |
| 5 | COS `U_k` not symbolically re-derived | low | BS-limit test partially mitigates |
| 6 | Single LLM judge | low | numerical evidence is load-bearing anyway |

The verdict **REPLICATED** rests on the C1 (COS) result matching the paper's `9.14732` to `2.7 × 10^-6`, the C2 (Monte Carlo) result agreeing within `z = +0.13`, the C1' strike sweep agreeing everywhere within `|z| < 1.5`, put-call parity holding, and the Black-Scholes limit recovered to `7 × 10^-12`. These are strong, independent, and mutually consistent — the failures above bound what has *not* been resolved, but do not undermine the price-reproduction claim.
