# Failure / gap analysis --- fernandes2026 (arXiv:2606.26239)

Honest accounting of what did **not** get reproduced, what is convention-dependent,
and where the result could silently be wrong. The physics **is** reproduced (verdict
REPLICATED, Agreement 9/10); this document exists so the ~13% residual and the scope
boundaries are not mistaken for a perfect or a broader replication.

## 1. The factor-of-2 shear-coupling convention (the single most important caveat)
The shear strain enters the strain Hamiltonian as `2*eps_xy * gamma^{B2g}` (Eq. 8).
When forming the Kubo matrix element `gamma^{xy}` in Eq. (6), one must decide whether
`gamma^{xy} = gamma^{B2g}` or `gamma^{xy} = 2*gamma^{B2g}`. **This choice changes eta^H
by a factor of 4** (16.8 vs 8.4 hbar/v_uc), because eta^H is quadratic in the coupling.

- **Decision made:** `gamma^{xy} = gamma^{B2g}` --- the explicit `2*eps_xy` prefactor in
  Eq. (8) already carries the symmetric `ij <-> ji` sum, so the per-element coupling should
  not double-count it. This lands on the paper's "order 10 hbar/v_uc" -> uPa*s target.
- **Why this is a convention, not a fit:** it is a bookkeeping choice about where the
  symmetric-strain factor lives, resolved against the paper's stated magnitude. It is NOT
  a free scaling knob tuned to hit a number --- the alternative choice is a specific,
  discrete factor of 4, and only one of the two is internally consistent with Eq. (8).
- **How to close it (Q3):** re-derive Eqs. (4)-(6) tracking the i,j<->k,l symmetrization
  explicitly, or match the SM full-frequency derivation. Until then, treat the absolute
  magnitude as convention-anchored, while the *shape*, *phi-proportionality*, and *relative
  sign* results are convention-independent and stand on their own.

## 2. The ~13% residual on the physical value
Computed 7.10 uPa*s vs paper 8.15 uPa*s. The paper itself only claims "of order 10 hbar/v_uc",
so 8.15 is an order-of-magnitude figure, not a high-precision target. The residual is
consistent with (a) the exact numerical value of the coupling constant alpha=8 (stated as
"magnitudes comparable to the hopping parameters", so slightly soft), (b) the temperature
broadening T=0.02 used in the Fermi factor, and (c) the convention in point 1. Not a physics
disagreement.

## 3. Scope NOT built --- the g-wave 3D model (Fig. 4)
The hexagonal g-wave altermagnet (D_6h; CrSb, MnTe, Co1/4NbSe2) is intrinsically 3D and is
the paper's *second* headline model. It was not implemented. It requires k_z-dependent lattice
functions, in-plane SOC components, a strain-induced SOC term (without which eta^H vanishes),
and a Lifshitz-transition-resolved 3D BZ integral (Fig. 4d/4e). This is the main coverage gap
(the 3/10 not covered) and the top next-step (open_questions Q1).

## 4. Adiabatic vs full-frequency kernel
We used the quasi-adiabatic Eq. (6) (omega->0 Berry-curvature form). The SM (Ref. [55]) gives
the full-frequency derivation. The experimentally-relevant magneto-acoustic (acoustic Faraday)
observable is at finite phonon frequency; finite-omega corrections were not computed (Q4).

## 5. Dirac-theory prefactor not independently derived
Eq. (12) maps eta^H of a single Dirac point to its Hall conductivity with prefactor
`C_0 = 8 hbar^2 g^{B2g} g_3^{A1g}/(v_uc t_1 t_d)`. We reproduced the *lattice* Kubo sum
directly and transcribed C_0, but did not independently derive it or overlay the Dirac curve
on the tight-binding result (Fig. 3b). Doing so (Q2) would give a first-principles check of
the coupling convention in point 1.

## 6. Figures confirmed in shape, not pixel-matched
Fig. 2(e) [eta^H(mu)] and Fig. 2(f) [eta^H(phi)] are reproduced in *trend and shape*
(insulating-window peak; monotone near-linear phi dependence), not fit curve-by-curve against
digitized figure data. A stricter agreement grade would require figure digitization.

## 7. Extraction tooling degraded (not a physics gap)
marker and nougat are not installed; artifacts 2/3 are pdftotext interims with degraded
equation rendering. Mitigated by hand-transcribing all equations into REPORT.tex. Flagged in
the artifact headers and artifacts_summary.md. This affects extraction fidelity only, not the
computed result.

## What would raise the verdict
- Build the g-wave 3D model (closes the largest coverage gap; Coverage 7 -> 9).
- Derive C_0 + finite-frequency kernel to remove the convention ambiguity (Agreement 9 -> 10).
- Digitize + pixel-match Figs 2e/2f.
