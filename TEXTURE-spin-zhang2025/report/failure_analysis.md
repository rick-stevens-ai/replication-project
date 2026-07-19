# Failure Analysis — zhang2025 (arXiv:2503.17916)

## What failed / friction
1. **C1 single-Pearson weak (honest nonlinearity, not a bug).** Pearson over all altermagnetic
   points is only 0.42 because both moment and splitting follow the same non-monotonic strain dome;
   the Ets=5-6% collapse branch drags the linear correlation down. Resolved by reporting Spearman
   rho=0.64 (monotone positive) + rising-branch Pearson=0.81, and downgrading the claim language to
   "positive but sub-linear/saturating" — which is what Table I actually shows. This is a genuine
   physics feature (splitting saturates faster than moment), logged as Open Q1, not hidden.
2. **LLM-judge endpoint.** opus-4.x aggregator parse error 2026-07-19; used free sonnet-4.6.

## Residual gaps (scope, some genuine PARTIAL)
- **DFT not run (method-limited).** OsO2/RuO2 DFT+U+Wannier+Kubo is out of scope on CPU-only.
  Absolute meV splittings come from the paper's Table I (analyzed, not regenerated).
- **theta_AS ~7% not recomputed** — requires constant-Gamma Kubo spin conductivity on the material
  Wannier bands. Reported only. (Recurring reduced-model-vs-full-DFT PARTIAL cause for this campaign.)
- **Saturation not captured by linear model.** Our t_AM ∝ m TB is linear; the real moment->splitting
  response saturates (Open Q1). Documented as a known simplification.
- **U-dependence unresolved.** Paper picks U=2.0 eV to force intrinsic altermagnetism (OsO2 is
  non-magnetic at its own linear-response U=1.13 eV); this assumption is untested here (Open Q3).

## What's needed to close
Strain-dependent multi-orbital TB fit to Table I; constant-Gamma Kubo for theta_AS; U- and
strain-resolved magnetic-stability scan for OsO2/RuO2. See open_questions.json.

## Honesty note
Verdict PARTIAL is correct and expected: the MECHANISM (strain->Stoner altermagnet, SOC-free
splitting, moment-splitting correlation, non-monotonic dome) is reproduced; the DFT/transport
headline numbers (absolute meV, theta_AS) are method-limited, not independently verified.
