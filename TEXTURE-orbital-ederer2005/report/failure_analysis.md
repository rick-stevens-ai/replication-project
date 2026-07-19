# Failure Analysis — TEXTURE-orbital-ederer2005

## Overall
No targeted claim failed. This section records the one quantitative residual, the
modeling limitations, the debugging incidents during implementation, and the
boundaries of what a non-DFT replication can assert.

## 1. C1 polarization-quantum residual (3.9%)
- **Symptom:** first run gave 59.4 uC/cm^2 (68% off) — wrong choice of primitive
  lattice vector R (used c/3 with V_prim, double-mismatched by a factor ~3).
- **Root cause:** modern-theory quantum eR/V requires R and V from the SAME cell.
  Fixed by pairing R = full hex c-axis repeat with the 2-f.u. primitive volume,
  giving 178.3 uC/cm^2 (3.9% off 185.6).
- **Remaining residual:** the paper used an LSDA+U-relaxed cell ~4% smaller in
  volume than the Kubel-Schmid experimental cell we used. Back-calculation shows
  V_prim=119.7 A^3 reproduces 185.6 exactly (vs 124.6 experimental). LSDA
  under-estimates volume → larger quantum → **sign of the discrepancy is consistent**.
  Not a model failure; a lattice-input difference. Logged as open question 1.

## 2. Modeling limitations (honest scope boundaries)
- **C2:** the Rice-Mele model reproduces quantization and the odd single-valued
  switching path EXACTLY, but its path amplitude (spontaneous P) is parameter-set
  dependent and was not tuned to BiFeO3's real ~half-quantum value. Reproduces the
  *concept* (Fig.1 construction), not the *magnitude*. Open question 2.
- **C3:** the vibronic model captures the d0 vs d^n dichotomy but does NOT model the
  lone-pair (Bi 6s2) ferroelectric route that the review says drives BiFeO3/BiMnO3.
  So the model explains *scarcity* (d0 rule) but not *how the known multiferroics
  escape it*. Open question 3.
- **C4:** the Landau coupling was assumed λQ²P; the true YMnO3 irrep analysis
  (Fennie-Rabe) may require a trilinear term with a third mode, which would change
  the P(Q) exponent. The 80:15 split was matched by tuning λ, so it demonstrates
  *consistency*, not an independent prediction. Open question 4.
- **C5:** D/J=0.02 was solved to hit the target 0.1 μB/cell; the magnitude is
  therefore reproduced by construction. Physical validity depends on whether that
  ratio matches literature J and D for BiFeO3 (unchecked). Open question 5.

## 3. What CANNOT be claimed from this replication
- No statement about DFT-absolute magnitudes (polarization 95 μC/cm^2, phonon
  frequencies, exchange constants) — these require the actual LSDA+U/DFPT machinery
  that is out of scope. They are flagged, not estimated or faked.
- The review's qualitative narrative (theory-experiment interplay, materials-design
  successes) is not a numerical claim and was not "tested"; only the embedded
  quantitative/mechanistic statements were.

## 4. Debugging incidents
- C1 factor-of-3 error (above) — fixed.
- C3 first run: d0 minimum pinned to the scan boundary (Q*=−1.0); widened the Q
  range to ±2.0 → genuine interior minimum at Q*=−1.11. No physics change, just
  grid extent.

## Prevention notes
- Always verify eR/V by pairing R and V from one cell; sanity-check the numeric
  order of magnitude against the paper before trusting.
- For Landau/tuned-parameter reproductions, state explicitly whether a number is an
  independent prediction or a consistency fit (done throughout).
