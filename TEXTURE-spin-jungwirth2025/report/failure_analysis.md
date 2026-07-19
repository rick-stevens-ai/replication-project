# Failure Analysis — jungwirth2025 (arXiv:2508.09748)

## What failed / friction
- Clean first run, no code failures. LLM-judge opus-4.x aggregator parse error 2026-07-19 (used free sonnet-4.6).

## Residual gaps (scope, NOT failure)
- **Transverse spin current in raw units.** The SSE transverse spin current is reported as a raw
  Boltzmann sum (unnormalized by cell volume / relaxation time). Only its nonzero-ness and the
  simultaneous zero transverse CHARGE current are the physical claims; the absolute magnitude is not
  a paper-comparable number.
- **Constant-tau clean limit.** No disorder / finite-T (Open Q2); the review's robustness claims for
  the SSE against scattering are not tested.
- **C4 out of scope.** Material-specific TMR/AHE ratios and THz dynamics are review surveys of many
  primary papers; not reproducible in a single model.

## What's needed to close
Landauer junction for TMR (Open Q1); disordered Boltzmann for SSE robustness (Open Q2); coupled
sublattice LLG for THz resonance (Open Q3). See open_questions.json.

## Honesty note
Verdict REPLICATED applies to the review's Fig. 1 CONCEPTUAL model signatures (polarization reversal,
spin-splitter effect, FM/AFM contrasts), reproduced with correct signs and zeros. It is NOT a claim
to have reproduced the review's surveyed material numbers.
