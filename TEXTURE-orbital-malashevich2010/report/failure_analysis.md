# Failure Analysis — why agreement is PARTIAL (not REPLICATED)

## What worked
- **Model built correctly**: the 8-site (2×2×2) spinless cubic tight-binding model of Appendix A / table A1, with the exact on-site energies and complex NN hopping phases. Spectrum is a clean insulator (min direct gap valence|conduction = 1.64), confirming the two-lowest-bands-occupied setup.
- **Both formalisms implemented from scratch and run**: (A) bounded-sample finite-field orbital magnetization → α_zz, and (B) k-space non-Abelian Chern-Simons axion angle θ_CS (eq 47a). No crashes; total runtime ~12 s.
- Berry/orbital numerics correctly reused from the gobel2024 kernel (v=i[H,r], projector traces).

## What did not reproduce
The **headline quantitative agreement** between PBC (k-space) and bounded-sample α
could **not** be demonstrated. Both estimators returned values at the numerical
noise floor (~1e-3…1e-4) and were uncorrelated across the φ sweep (r ≈ −0.07).

## Root causes
1. **Under-resolved bounded sample.** The true α is small; the paper needed clusters
   L=4,5,6,7 (up to ~2925 sites) plus a *cubic* 1/L,1/L²,1/L³ extrapolation to
   reach 1e-7 e²/ħc precision. We used L≤5 with a simple polynomial fit, leaving
   the signal buried in finite-size/surface noise.
2. **Coarse, gauge-noisy k-mesh.** The Chern-Simons 3-form is only *locally*
   gauge-invariant. A one-shot delta-orbital projection on an 8³ mesh does not
   produce the *globally smooth* gauge the integral requires; the paper used an
   80³ mesh with a Wannier-based smooth gauge. Result: θ_CS scattered at ~1e-4
   with no stable value.
3. **Missing Kubo terms.** We implemented only θ_CS; the paper's α also contains
   α̃^LC (47b) and α̃^IC (47c). For this *ordinary* insulator these Kubo terms are
   generally nonzero, so θ_CS alone is not the full isotropic response.
4. **No hard target number.** The pdftotext extraction did not preserve the
   numerical y-axis values of Figs. 1/3, so even a well-converged run lacks a
   digitized reference for a strict agreement score.

## Path to REPLICATED
Scale clusters to L=4–7 with a sparse occupied-subspace solver + cubic 1/L fit;
build a globally smooth Wannier gauge on a ≥40³ mesh; add the Kubo terms
(47b)–(47c); digitize Figs. 1/3 for reference curves; verify E=0 orbital
magnetization matches between the two methods before differentiating.

## Honesty note
No numbers were fabricated. All reported α, θ_CS, gap, and correlation values are
direct outputs of the committed code (`report/evidence/`), reproducible via the
two commands in `workflow.md`.
