# Extraction marker — arXiv:2502.16657

**Paper:** "Loop-current order through the kagome looking glass"
**Authors:** Rafael M. Fernandes, Turan Birol, Mengxing Ye, David Vanderbilt
**Date:** 25 Feb 2025 (arXiv:2502.16657v1 [cond-mat.str-el])
**Type:** Focused *Perspective* / review article (NOT a primary-results paper).

## Nature of the paper
This is a perspective that frames the phenomenology of **loop-current (LC) order** (a.k.a. "flux"
or "imaginary CDW" / iCDW order) using the AV₃Sb₅ (A = K, Rb, Cs) kagome metals as the running
example. There are **no new numerical figures with tabulated data to reproduce**; the contributions
are (i) a group-theoretical classification, (ii) a set of well-defined microscopic definitions
(Box 1: current operator / Peierls substitution; Box 2: patch model), and (iii) a table (Table I)
of the magnetic/experimental signatures of the canonical mixed LC–CDW phases.

Because it is a perspective, the machine-checkable content is the **physics the paper asserts to be
true** about the kagome tight-binding model and about loop-current order. We reproduce those
assertions from first principles with a minimal tight-binding + Peierls-flux + Kubo/Berry code.

## Central claims (as stated in the paper)
- **C-BAND (Fig. 3a, Eq. 1):** The nearest-neighbor tight-binding model on the kagome lattice has
  **saddle points (van Hove singularities) at the M points**. Near M, E(k+Q_M) ≈ E0 + (ℏ²/2m*)(kₓ²−k_y²):
  a **minimum along Γ–M–Γ but a maximum along K–M–K̄** (anisotropic / hyperbolic saddle). In 2D the
  DOS shows a **logarithmic divergence** at E0. The kagome band structure additionally has a **flat band**
  and a **Dirac point at K**. (Standard kagome facts the paper relies on.)
- **C-PEIERLS (Box 1, Eq. 5):** LC order = change in the **phase** of the hopping parameters (Peierls
  substitution t_ij → t_ij exp[-(ie/ℏc)∫A·dr]); "quite often, LC order will generate phases of ±π/2 in
  the hopping parameters." This **breaks time-reversal symmetry** via the kinetic energy (not a Zeeman term).
- **C-CDWvsLC (Box 2, Eq. 6):** Real order parameter O⁺ = bond CDW (rCDW → W); imaginary O⁻ = loop
  current (iCDW → −iΦ). rCDW modulates hopping **amplitude**; LC modulates hopping **phase**.
- **C-TABLE (Table I / Fig. 2):** Canonical M-point mixed phases and their signatures:
  - 3Q–3Q  Φ=(Φ₀,Φ₀,Φ₀), W=(W₀,W₀,W₀): **ferromagnetic**, net moment ⇒ **AHE/Kerr ✓**.
  - 2Q–1Q  Φ=(Φ₀,Φ₀,0),  W=(0,0,W₀):  **antiferromagnetic**, moments **cancel** ⇒ no AHE, resistivity anisotropy ✓.
  - 2Q–3Q  Φ=(Φ₀,0,−Φ₀), W=(W₀,W̃₀,W₀): **ferro-octupolar**, net dipole cancels but octupole ≠ 0 ⇒ piezomagnetism ✓.
- **C-ANHARM:** Threefold rotational symmetry allows a third-order term W_{i1} ∼ Φ_{i2}Φ_{i3}: an LC
  order parameter with components at two M-points **necessarily triggers** a CDW at the third M-point.
  The **only pure-LC (no CDW) phase is single-Q** Φ=(Φ₀,0,0).
- **C-PATCH (Box 2):** Patch-model instability channel: iCDW (loop current) favored when
  **g1 < 0, g2 > 0, g3 > 0**.
- **C-AHE-HALDANE:** LC/flux order that gaps the spectrum with staggered fluxes produces an
  **anomalous quantum Hall state** (Haldane-type; ref [5] = Haldane 1988, ref [4] = Sun–Fradkin).

## Machine-checkable claims selected for replication (see report/artifacts_summary.md)
1. **CL1 — Kagome saddle point at M is a hyperbolic vHS** (min along Γ–M, max along K–M) with a
   **log-divergent DOS**; flat band present; Dirac point at K.
2. **CL2 — Peierls π/2 flux breaks TRS and opens a gap** at the Dirac/vHS region; the gapped flux
   state carries **nonzero Berry curvature / integer Chern number** (anomalous Hall / Haldane state).
3. **CL3 — Loop-current order parameter (Box 1 Eq. 4) is purely imaginary** ⟨current⟩ ≠ 0 in the
   flux state and **= 0 in the plain / real-hopping state**; bond charge (real part) is unchanged
   by pure flux ⇒ LC and CDW are the imaginary/real channels of the same bond operator.
3b. **CL3-net — Triple-Q flux magnetization (Table I):** compute the net orbital magnetization
   (sum of triangle plaquette fluxes) for the 3 canonical configs: 3Q ⇒ nonzero (FM), 2Q–1Q ⇒ 0 (AFM),
   2Q–3Q ⇒ dipole 0 but octupole ≠ 0.
4. **CL4 — Anomalous Hall conductivity σ_xy is quantized** (= C·e²/h) inside the gap of the flux state
   and **= 0** in the TRS-preserving state (Kubo–Berry kernel), realizing the paper's AHE claim.

## Extraction method
`pdftotext -layout paper.pdf work/paper.txt` (586 lines). Native PDF/vision not required; text
extraction was clean. Figures were read from captions + text (Fig. 1–3, Table I, Box 1, Box 2).

## Out-of-scope (marked, NOT faked)
- Ab initio (DFT/hybrid-functional) prediction of LC order in real AV₃Sb₅ or CrSi(Ge)Te₃ [ref 34].
- The full patch-model RG flow / weak-coupling phase diagram (we verify the *stated* channel logic
  and the vHS prerequisite, not the RG integration).
- Quantitative μeV internal fields, μSR relaxation rates, experimental Kerr/Hall magnitudes.
- The full anharmonic Landau free-energy minimization over all independent coefficients.
