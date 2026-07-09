# Failure Analysis — s100-072 (Analytical track-structure formulas)

**Paper:** Kundrát et al., *Analytical formulas representing track-structure simulations on DNA damage induced by protons and light ions at radiotherapy-relevant energies*, Sci. Rep. 10:15775 (2020).

**Verdict-preserved:** REPLICATED (analytical-scope). See caveats below.

This is a candid accounting of what the replication **did not** achieve, what could go wrong with the "clean pass" verdict, and where a critical reviewer would legitimately push back.

---

## 1. The near-tautology risk (the biggest honest concern)

The paper publishes:
- Two closed-form equations (Eq. 1, Eq. 2).
- 540 fit parameters (Tables 1 + 2).

The reproduction:
- Coded those same two equations.
- Transcribed those same 540 parameters.
- Regenerated the fitted curves.
- Checked that body-text numerical claims come out right.

**By construction, agreement was essentially guaranteed.** A critical reviewer could reasonably say this test only proves (a) the parameters were transcribed without typos and (b) the equations were coded without algebra bugs. It does **not** prove the equations themselves are physically correct, nor that the parameters were fit correctly by the authors.

**What would have made this stronger:** running an independent MC (Geant4-DNA on `uicgpu`, available and free) on the same target geometry, and computing residuals of formula vs. MC yields point-by-point. That was not done. See open_question Q1 for the concrete next-step.

## 2. No independent Monte Carlo cross-check

- PARTRAC (Helmholtz Munich) is proprietary and was not re-run.
- Geant4-DNA is available on `uicgpu` and free, but was not run for this dir.
- TRAX / KURBUC likewise not run.

Consequence: the analytical formulas are validated against the paper's own claims, not against an independent physical calculation. If the underlying PARTRAC fits were themselves biased (e.g. by chemistry-model assumptions), that bias propagates undetected into our reproduction. **This is a legitimate downgrade point** — a stricter reviewer might argue this dir deserves `PARTIAL` or `ANALYTICAL-ONLY` rather than plain `REPLICATED`. We flag this explicitly and preserve `REPLICATED` on the grounds that the paper's *own* deliverable is the analytical formulas, which we did reproduce exhaustively.

## 3. PARTRAC MC datapoints (Fig. 1–5 symbols) not reproduced

The paper's figures overlay:
- Smooth curves (analytical fits) → **reproduced exactly by construction.**
- Symbols (underlying PARTRAC MCTS output) → **not reproduced; underlying data not published.**

So the "goodness of fit" of formula vs. MC — the whole reason the analytical formulas exist — was **not re-derived**. We take the authors' quoted global fit quality on trust. A stricter replication would ask the authors for the PARTRAC output CSV or run an equivalent MC to reconstruct the symbols.

## 4. LET-range extrapolation not tested

The formulas were only evaluated within (or slightly beyond) the paper's fit range (0.25–512 MeV/u, LET ≈ 0.1–1000 keV/µm depending on species). At the extremes:
- **Ultra-low LET (< 0.1 keV/µm):** SB/SSB from Eq. (1) may drop unphysically below the electron/gamma limit. Not tested.
- **Ultra-high LET (> 2000 keV/µm):** Eq. (2) asymptotes as LET^(p3-p5), which for typical params ≈ LET^0.3 — grows unboundedly, physically wrong at extreme LET where overkill should saturate. Not tested.

Extrapolation safety of the formulas is a real open question (open_question Q2).

## 5. Documentation inconsistency in the paper itself

The paper's text calls the log-LET dip in Eq. (1) "Gaussian bell-shaped"; the printed formula is actually **Lorentzian** in log-LET. We implemented the Lorentzian (matches the printed formula and the fit parameters). A naive re-implementer working from the prose alone would get subtly different curves. This is an authorial slip in the paper, but our reproduction inherits the correct printed form.

## 6. Chromatin/cell-state universality untested

All 540 fit parameters are specific to the PARTRAC G0/G1 spherical lymphocyte nucleus (10 µm, 6.6 Gbp). Real applications (proton therapy planning, radioprotection) span cell types with very different chromatin condensation. The formulas as-published cannot be dialed to cell state; whether they generalize is an open question (open_question Q3). Our reproduction inherits this restriction verbatim.

## 7. No downstream survival mapping

The paper stops at DSB / DSB-cluster / DSB-site yields. The clinical endpoint that matters (cellular survival, RBE) requires an additional model (LEM, MKM, RMF, or PARTRAC's repair chain). The paper does not perform this mapping and neither did we. So the paper's *usefulness for treatment planning* is asserted but not demonstrated. This is a legitimate gap between "we reproduced the formulas" and "the formulas are demonstrably useful for their stated purpose". Open_question Q4.

## 8. No experimental cross-check

No comparison against γ-H2AX foci data, PFGE DSB measurements, or the PIDE database of ion-beam survival curves. The paper does not perform such comparisons and we did not add them. So the biological plausibility of the formulas is only as good as PARTRAC's biological plausibility, which is a separate literature.

## 9. Sensitivity to direct/indirect chemistry not analyzed

The paper commits to fixed direct/indirect probabilities (linear SB probability 0→1 from 5–37.5 eV; 65% breakage per •OH attack). Other track-structure codes use different assumptions (KURBUC: stochastic OH scavenging; Geant4-DNA-Chem: energy-dependent OH yields). If the direct/indirect split changes, the shape of the Lorentzian dip in Eq. (1) will shift — the paper does not report this sensitivity. We did not re-fit under alternative assumptions. Open_question Q5.

## 10. Minor engineering / evidence gaps

- No unit tests around `yield_eq1` and `yield_eq2` (regression coverage for NaN-skip logic is by inspection only).
- No CI wiring to auto-regenerate figures on parameter change.
- `extraction/nougat.mmd` is a stub; only pdftotext + tesseract were used. For a fully-preservationist archive, running nougat once would produce a machine-readable equation extraction (LaTeX-form) that would be more robust than the plain-text OCR.

---

## Bottom line

This is a **clean formula-and-parameter replication** of a paper whose entire deliverable is a set of closed-form formulas. It is **not** an independent physical revalidation. The verdict `REPLICATED` is defensible on the "paper's own deliverable was reproduced" grounds, but a stricter reviewer might argue for a `REPLICATED-ANALYTICAL-ONLY` sub-tag to distinguish this from replications where an actual MC pipeline was re-run. We flag the caveat prominently in `REPORT.tex` §Verdict.

**Not downgraded** because the paper is explicitly, self-consciously, the analytical reduction of a Monte Carlo pipeline — reproducing its formulas fully **is** reproducing the paper. A `PARTIAL` verdict would misrepresent the paper's scope. **REPLICATED (analytical-scope)** is the honest label.
