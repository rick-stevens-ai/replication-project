# Failure / gap analysis — Lux et al. 2017 (arXiv:1706.06068)

**Verdict: PARTIAL.** The zero-SOC *structural* headline reproduces cleanly; the
absolute coefficient and the clean μ-parabola do not. Ordered most→least important.

## 1. Absolute 1/4·χ_LP coefficient — NOT matched (the single biggest caveat)
The paper's coefficient is `(1/4) χ_LP^{↑+↓}` with the **continuum** Landau–Peierls
susceptibility `χ_LP = −e²/(12π mₑ)`. Our extracted slope
`M_tom/χ_c ≈ 6.7×10⁻⁴` is in **lattice/tight-binding units** (itinerant ½(r×v)
operator, t=1) and does not map onto the continuum χ_LP without an
operator-normalization bridge. We therefore confirm the *structural* content the
coefficient encodes — **linearity in the scalar spin chirality** and the **sign** —
but not the numerical value 1/4. This is the same
modern-theory-of-orbital-magnetization normalization limit documented for the
sibling gӧbel2024/2025 skyrmion-OHE runs (skill pitfalls 8/11): the itinerant
½(r×v) operator carries a normalization that differs from the Berry-phase orbital
magnetization operator. Closing it needs the Bianco–Resta modern-theory L_z
(open question #1).

## 2. H2 μ-dependence — qualitative only
The paper's `(1 − 3μ²/Δ²)` is a **near-band-edge continuum** result predicting a
single downward parabola with a sign change at `|μ| = |Δ|/√3` and zero beyond
`|μ| = |Δ|`. Our full-band lattice μ-sweep is **oscillatory** (5 sign changes),
dominated by van Hove / finite-size band structure. We reproduce the *qualitative*
prediction (M_tom is a sign-changing, strongly μ-dependent function) but not the
clean parabola. A narrow near-band-bottom sweep at larger L should recover it
(open question #2). Residual: shape mismatch, not a sign/mechanism failure.

## 3. Scope not built (expected, not a shortfall)
- **COM / SOC branch** (Eqs. 8, 11): the α_R-linear chiral orbital magnetization of
  the 1D spiral, with its companion **1/2** prefactor, was not rebuilt — out of
  scope for the zero-SOC TOM headline.
- **Fig. 2 (α_R, Δ_xc) phase diagram**, including the `|α_R|>|Δ_xc|` enhancement
  lobe, not mapped.
These are scoped out deliberately; the zero-SOC headline is the assigned anchor.

## 4. Method substitution (documented, not a defect)
The paper's method is a semiclassical Green's-function / Wigner **gradient
expansion**. We instead **directly diagonalize** the same physical lattice model.
This reproduces the physical observable (chirality-linear TOM at zero SOC) but does
not itself verify the diagrammatic order-counting (COM 1st / TOM 2nd order). Bridging
the two is open question #5.

## 5. Extraction tooling degraded — NOT a physics gap
`marker` and `nougat` are not installed; `extraction/marker.md` (prose, via
`pdftotext -layout`) and `extraction/nougat.mmd` (math, hand-transcribed LaTeX +
raw pdftotext appendix) are the documented interim fallbacks. Unicode math breaks
under pdftotext (known limitation); authoritative equations are hand-transcribed in
REPORT.tex and nougat.mmd. Each file carries a provenance banner and the exact
regen command.

## What would raise the verdict to REPLICATED
Implement the modern-theory-of-orbital-magnetization L_z (open question #1) to
recover the absolute 1/4·χ_LP in physical units, **and** resolve the clean
`(1−3μ²/Δ²)` parabola near the band edge (open question #2). Together these would
close both quantitative gaps that currently cap this at PARTIAL.
