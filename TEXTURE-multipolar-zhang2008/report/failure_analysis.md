# Failure & Limitation Analysis — arXiv:0805.3922 replication

## 1. Task-label vs paper mismatch (environmental, resolved)
The directory/task said "multipolar texture" but `paper.pdf` is a cuprate
spin-response paper. **Root cause:** upstream label error. **Handling:** did not
fabricate a texture paper; replicated the paper actually present and flagged the
mismatch prominently (`extraction/marker.md`). Not a code failure.

## 2. Path-resolution bug (real, fixed)
First `write` calls used `/Users/stevens/.openclaw/workspace/../Dropbox/...`.
`.openclaw/workspace/..` resolves to `.openclaw`, so files landed in a stray
`~/.openclaw/Dropbox/...` tree. **Fix:** copied files into the correct
`~/Dropbox/...` target and `rm -rf ~/.openclaw/Dropbox`. **Prevention:** use the
canonical absolute target path, never a `workspace/..` relative hop.

## 3. Primary scientific limitation: denominator-form S(k,ω) is dispersion-dominated (HONEST NEGATIVE)
The most direct check — scanning S(k,ω) along (k_x,π) at ω=0.31J and measuring
the incommensurability δr vs field — **failed to reproduce the paper's
field-driven commensurate→IC transition.**

**Symptom:** δr ≈ 0.40 (in units of π) at *all* fields including B=0, essentially
field-independent (δr drifts from 0.436 → 0.430 as ε_B: 0 → 0.01J).

**Root cause:** with a monotonically-dispersing MF mode ω_k (minimum at Q), the
condition ω_k = ω at fixed ω=0.31J is satisfied on an *iso-energy ring* around Q.
That ring produces two symmetric peaks along the cut regardless of field — an
artifact of the bare dispersion, not the resonance. The paper's *commensurate*
B=0 resonance sits AT Q only because the self-consistent Re Σ^(s)(k,ω) (Eq. 6)
strongly renormalizes the mode near Q; the field then splits it. A minimal model
without the full k,ω-dependent Σ cannot pin the resonance to Q, so it cannot show
the transition via the raw S-scan.

**Handling (no fabrication):** kept the negative result explicit in
`work/results.json` (`claim23_...caveat`) and added an *analytic* isolation of
Eq. 9 (`claim2b_eq9_analytic`): once the Zeeman splitting 2ε_B exceeds the
intrinsic linewidth Γ·Ω, the commensurate peak resolves into two IC peaks with
δr = sqrt(((2ε_B)²−(ΓΩ)²)/κ). This DOES reproduce: (i) commensurate at low field,
(ii) monotonic δr increase with B (Fig. 3), (iii) a critical field ≈6.2 T that
falls between the paper's Bc1≈4T and Bc2≈10T. This threshold was set by an
independently-chosen linewidth, NOT tuned to the paper's critical fields, so the
bracket is a genuine consistency check.

## 4. g-factor discrepancy (real finding, not a failure)
The paper's own ε_B↔B numbers imply g ≈ 1.04, vs the ~2.0-2.2 expected for Cu2+.
The three anchors are mutually consistent (single slope), so it is a systematic
scale choice, not a typo. Flagged as open question #2. Does not affect the
qualitative conclusions.

## 5. Out-of-scope items (declared, not faked)
- Self-consistent order parameters Z_hF, Δ̄_h, α, μ, χ's (Eqs. 7a,7b).
- Full double-momentum-sum spin self-energy Σ^(s) (Eq. 6).
- Absolute intensities / full 2D S(k,ω) maps of Figs. 1 & 4.
These require the complete kinetic-energy-driven-SC numerical program and were
explicitly excluded per the minimal-replication scope.

## Lesson
For resonance/RPA-type spin-response papers, the falsifiable "shape" claims
(branch splitting, energy shifts, scaling of a critical scale) are checkable with
analytic denominator arguments, but the *position* of a resonance (commensurate
vs incommensurate) is genuinely a property of the self-consistent self-energy and
should not be expected from a bare-dispersion stand-in. Report it as such.
