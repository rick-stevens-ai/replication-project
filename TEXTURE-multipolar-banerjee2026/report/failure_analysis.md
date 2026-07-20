# Failure Analysis — banerjee2026

## Verdict: REPLICATED (headline). Coverage 7/10, Agreement 9/10.

The headline claim — CPL induces an effective static field linearly coupled to
the magnetic octupole (OIFE), of optical-helicity origin, at the meV scale — was
reproduced independently in **form, origin, and magnitude**. The following are
honest gaps and limitations.

## What was fully replicated
- **Pseudospin SU(2) algebra** (Eq.2): projected/normalized Stevens operators
  reproduce [s_a,s_b]=i eps_abc s_c exactly; sigma_y is the magnetic octupole T_xyz.
- **OIFE field form**: h_m multiplies sum_i sigma_i^y — a uniform field linear in
  the octupole, matching Eq.(4).
- **Helicity origin**: h_m(zeta=0)=0 and grows as zeta^2 (fitted 1.96), i.e.
  ~ |E(Om) x E*(Om)|, the inverse-Faraday signature the paper asserts.
- **Magnitude/scaling**: J_eff ~ 1e-2 eV, h_m,Gamma^(3) ~ 1e-4..1e-3 eV,
  consistent with Fig.3 scales.
- **h_m proportional Gamma^(3)**: ratio 9/8 identically (from 1/8 vs 1/9 analytic
  prefactors in Eqs.6e,6f), matching Fig.3(b).
- **van Vleck mechanism**: [V_-1,V_+1]/Omega on the doublet yields a static field
  in the sigma_y (octupole) channel.

## Gaps / not attempted (why Coverage is 7, not 10)
1. **Many-body phase diagram (Fig.8)**: the ED/DMRG identification of AFO, FO,
   PPFQ, IO, and multipolar-liquid phases over the (Gamma^(3)/J_eff, h_m/J_eff)
   plane was NOT performed. We replicated the *couplings that generate* the
   phase diagram, not the phases themselves. (See open_questions #3.)
2. **Absolute anisotropy magnitude (Fig.3a)**: our Gamma^(3)/J_eff reaches only
   ~2.7e-3 at zeta=4, whereas Fig.3(a) suggests the anisotropy can approach the
   dominant exchange scale. This is a **quantitative gap** likely from (a) the
   geometry factors psi_0 and r_pd/r_dd (Slater-Koster edge-sharing details) not
   fully specified in the provided excerpt — we used psi_0=pi/2 and
   r_pd/r_dd=1/sqrt2 as representative choices; and (b) the exact definition of
   U-tilde(U,J_H,lambda) from Appendix A/C, which sets resonance placement.
   The *trend* (growth with zeta) is correct; the *absolute ratio* is not
   pinned. This is the named gap limiting a PARTIAL->full quantitative claim on
   Fig.3(a).
3. **Prethermal lifetime (Eq.5)** and **lattice distortion magnitudes** (trigonal/
   tetragonal) were not numerically evaluated.
4. **Full Hubbard-Kanamori microscopics**: we used the paper's already-derived
   analytic Floquet formulas (Eqs.6a-6f) rather than re-deriving them from the
   many-orbital Hubbard-Kanamori model via an independent FSWT. The FSWT
   derivation itself (Appendices A-C) is trusted, not re-derived.

## Sensitivity notes
- Results are robust to Floquet cutoff p (7 is well-converged; Bessel weights
  suppress high orders, and virtual denominators |U-tilde - m*Om|,
  |Delta_c - n*Om| stay far from resonance for the chosen Omega).
- The 9/8 h_m/Gamma^(3) ratio is prefactor-exact and independent of parameters,
  confirming it is an analytic identity of the minimal single-t2 model (as the
  paper states), not a numerical coincidence.

## Extraction caveat
`extraction/marker.md` and `extraction/nougat.mmd` are **interim pdftotext
fallbacks**, not true marker/Nougat neural OCR (not available in this
environment). Equations are linearized unicode and should not be treated as
faithful LaTeX. The authoritative equations used are transcribed directly in
REPORT.tex and replicate_banerjee2026.py.
