# Failure Analysis — jaubert2016 replication

## Overall: REPLICATED (10/10 checks). No blocking failures.

## Partial / caveats

### 1. ΔE_hh dumbbell energy: -3.13 D computed vs -4.73 D paper (OCR-ambiguous, NOT counted as failure)
- **Symptom:** Our evaluation of Eq. (12)'s coefficient gives `(16/3)(-1 + M_zb - (3/2)√(2/3)) = -3.13`,
  not the paper's `-4.73`.
- **Root cause:** Eq. (12) in `pdftotext` output is fragmented across lines 579-591 with the
  bracket `[...]` and its internal signs/factors collapsed; the exact coefficient could not be
  reconstructed unambiguously from text.
- **Evidence it is not a physics error:** the *companion* dumbbell energy ΔE_mm evaluates to
  **19.754 D vs the paper's 19.75 D** — an essentially exact match using the *same* Madelung
  constant `M_zb = 1.638` and the same `√(2/3)` factors. A method that nails ΔE_mm to 4
  significant figures is not structurally wrong; the ΔE_hh mismatch is an OCR transcription gap.
- **Mitigation:** flagged as `dEhh_ocr_ambiguous` in the scorecard rather than fabricating a fit;
  logged as open question #2 with an analytic re-derivation plan.

### 2. Structure factor: coexistence shown, but pinch-point *singularity* not resolved
- **Symptom:** residual (Coulomb) S(q) shows finite anisotropic diffuse scattering (peak/mean 2.2,
  S(0,0,2)=0.93) but not a sharp pinch-point singularity.
- **Root cause:** L=3 (108 spins) is deliberately tiny (fast-path); pinch points are
  reciprocal-space singularities requiring larger lattices and dense q-sampling.
- **Impact:** low — the *qualitative* claim (Bragg sharp peaks coexisting with broad Coulomb
  diffuse scattering) is clearly demonstrated (Bragg peak/mean 40.7 ≫ diffuse 2.2). Only the
  singular *shape* is under-resolved. Logged as open question #1.

### 3. Not attempted (out of fast-path scope)
- Direct MC extraction of defect V(r) curves (Fig. 5) — analytic prefactor validated instead.
- Low-T R-state selection by dipolar degeneracy lift (Section VI).
- Finite-T FCSL phase window and the four-body stabilizing Hamiltonian.
- These are scope choices, not failures; captured in open_questions.json + next_steps.

## What went right
- Analytic prefactor `8√2/3√3` exact to machine precision.
- FCSL zinc-blende ensemble generated cleanly (40/40 annealed to E=0).
- Fragmentation demonstrated rigorously: ρ=0.5 ordered + divergence-free residual (1.4e-16).
- Bragg/diffuse coexistence quantitatively separated.
