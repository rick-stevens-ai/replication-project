# Failure Analysis — martinelli2025 (arXiv:2512.17587)

## What failed / friction
- No code-level failures; ran clean first try. LLM-judge opus-4.x aggregator parse error 2026-07-19
  (used free sonnet-4.6).

## Residual gaps (scope => PARTIAL)
- **DFT not run (method-limited).** SrCrO3 (constrained density) and LaVO3 (GdFeO3 distortion)
  first-principles calculations are out of scope on CPU-only. The absolute multipole magnitudes and
  material-specific NRSS values (the paper's actual figures/tables) are NOT independently verified.
- **C1 and C3 are true by construction.** In this minimal model the quantitative relation and the
  band-independent measure are almost tautological; they carry little independent evidential weight.
  The genuinely non-trivial reproduction is C2 (superposition necessity), which is qualitative.
- **Weights imposed by hand.** The relative octupole/triakontadipole weighting is chosen, not
  derived from a material (Open Q1). Constraint-vs-distortion route equivalence untested (Open Q2).

## What's needed to close
DFT on SrCrO3/LaVO3 with multipole decomposition (e.g. via the multipole code the paper cites) to
regenerate the actual NRSS(multipole) curves; a Fermi-surface-weighted measure comparison (Open Q3).

## Honesty note
Verdict PARTIAL is correct: the paper's CONCEPTUAL contribution (multi-component multipolar order
parameter; single lowest multipole insufficient) is reproduced qualitatively in a toy model; the
material-specific DFT is method-limited and not attempted. Reduced-model-vs-full-DFT PARTIAL.
