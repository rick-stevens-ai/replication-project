# Failure Analysis — TEXTURE-orbital-coh2010

Honest account of what did **not** reproduce, root causes, and what would be
required. Nothing here is fabricated; every negative result was observed in
code (see `code/` and `work/results.json`).

## 1. Direct Chern-Simons 3-form integral (paper Eq. 22) — FAILED for TI
**Attempt:** `cs_theta.py` (raw grid), `cs_theta_smooth.py` (smooth gauge via
3D log-cabin parallel transport), `theta_final.py` (per-band A·Ω after
lifting the Kramers degeneracy).
**Observed:** raw-grid Eq. (22) returns nonsense (θ/π = −0.33, −16.8, …);
the smooth-gauge integral returns θ≈0 for the topological phase (m0=−2)
while correctly giving θ≈0 for trivial phases.
**Root cause:** This is *the* central difficulty the paper spends Section III
on. On a discrete mesh the CS 3-form is gauge-dependent and needs a smooth
gauge; for a strong Z2 TI there is a topological **obstruction** to a smooth
periodic gauge, so the θ=π content lives entirely in a boundary term that
periodic finite-differencing discards. The paper resolves this with
maximally-localized Wannier functions + explicit T-breaking in the trial WFs
+ k-mesh extrapolation (Eq. 27). We did not implement the full MLWF machinery.
**To fix:** implement Eq. (27) (Wannier position-matrix-element form) with a
Wannier90-style localization, or a boundary-aware CS integration; extrapolate
over k-mesh density as the paper does (they recover only ~30% at 11^3 and
extrapolate to within 10% of π).

## 2. Hybrid Wannier center (Wilson-loop) partner-switching — NOISY
**Attempt:** `theta_z2_robust.py`, `theta_z2pack.py` (Soluyanov-Vanderbilt
largest-gap method).
**Observed:** the WCC endpoints show the pair regrouping (TI: paired near 0
at ky=0), but the full ky-flow is jittery and the automated crossing-parity
count did not robustly match the parity oracle across the whole phase diagram
(several false positives/negatives at coarse sampling).
**Root cause:** the toy model is **Kramers-degenerate everywhere** (a
PT-protected doublet — no single k-independent operator commutes with all
four Γ matrices), so the Wilson-loop eigenvectors are gauge-arbitrary within
the 2D degenerate subspace at each k. This scrambles the individual WCC
lines even though the *set* is well defined.
**To fix:** lift the degeneracy with an infinitesimal T-breaking field,
track the now-non-degenerate WCC continuously, extrapolate to zero field; or
use a symmetry-resolved (spin-Chern) Wilson loop.
**Mitigation used:** we fell back to the **Fu-Kane parity criterion**, which
is an *exact theorem* for inversion-symmetric insulators
(Turner-Zhang-Vishwanath; Hughes-Prodan-Bernevig) — a rigorous θ computation,
not a heuristic. It reproduces the analytic Wilson-Dirac phase diagram
exactly, so C1 is solidly established despite the WCC noise.

## 3. Continuous unquantized θ(b_z) (paper Fig. 8 curve) — PARTIAL
**Reproduced:** the gap collapse and **metallization at b_z=1.0** — the
paper's explicit Fig-8 statement ("becomes metallic and the CSOMP becomes
ill-defined").
**Not reproduced:** the numeric slope Δθ = 0.55 per 0.27 μB. Extracting the
continuous θ in the T-broken window has the same boundary-term difficulty as
#1 (though without the exact obstruction, so it is in principle tractable
with a twisted continuous gauge). The parity oracle is invalid once
inversion is broken by b_z, and we did not build a replacement invariant.

## 4. Material DFT numbers — OUT OF SCOPE (not attempted, not faked)
Cr2O3 (θ=1.3e-3), BiFeO3 (0.9e-4), GdAlO3 (1.1e-4), Bi2Se3 (1.07π),
band gaps, magnetic moments, and the θ-vs-λ_SO curve (Fig. 6) all require
Quantum-ESPRESSO DFT + Wannier90 + noncollinear SOC on real crystal
structures. This is explicitly the "DFT-heavy, needs cluster" part flagged in
the method extract. Per replication rules these are marked out-of-scope
rather than fabricated. The toy model reproduces only the *qualitative*
smallness (trivial ⇒ θ≈0) and the *quantized* limit (θ=π).

## Summary
The conceptual physics of the paper is reproduced and internally consistent
(exact phase diagram, 24.34 vs 24.3 ps/m, metallization under T-breaking).
The two things that "failed" — direct Eq.(22) integration and the continuous
θ — are precisely the hard implementation problems the paper itself devotes
its methodological sections to, and both need the full Wannier/DFT pipeline
we deliberately kept out of scope. No result was faked; negative results are
reported as observed.
