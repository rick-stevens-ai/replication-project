# Failure Analysis — Fukui et al. 2022 IMK Replication (Honest Critique)

**Verdict:** PARTIAL (strong). Coverage 9/10, Agreement 9/10.
**Headline exercised?** ✅ Yes — `w_SLDR` independently refit and recovered within 1σ; ALDH+ ↔ f_s consistency confirmed 4/4.

## 1. What the paper claims (headline)

Fukui et al. propose an Integrated Microdosimetric-Kinetic (IMK) model that explains radioresistance in oral SCC cell lines (SAS-R, HSC2-R vs their parental SAS, HSC2) via two mechanisms:
1. **Increased ALDH+ stem-like fraction** (f_s: 0.97% → 9.65% for SAS→SAS-R; 1.36% → 12.61% for HSC2→HSC2-R).
2. **Increased sublethal-damage-repair rate** (w_SLDR = (a+c)_H/(a+c)_p ≈ 1.06 for SAS-R, ≈ 1.90 for HSC2-R).

The IMK model integrates LQ kinetics + SLDR cross-term + stem-cell mixture. Table 1 lists all fit parameters; Figs 5, 6, 7 show acute-dose, split-dose, and dose-rate survival curves.

## 2. What LUCID DID (exercised)

### 2a. Model implementation ✅
Pure NumPy implementation of Eqs 1, 2, 4, 6, 7, 12, 13, 14 (`code/imk_model.py`), Table 1 verbatim (`code/params_table1.py`). Runnable, reproducible.

### 2b. Fig 5 acute-dose forward replication ✅
Using Table 1 means + digitized Fig 5 survival points: R² 0.960–0.997 in −ln S space, RMS log₁₀(S) residual 0.078–0.196. Forward pass matches.

### 2c. Independent MCMC refit of headline w_SLDR ✅
Refit against digitized Fig 5 alone (no prior on (a+c) from paper), recovered:
- w_SLDR(SAS-R) = **1.11 ± 0.20** (paper 1.06 ± 0.12) — within 1σ.
- w_SLDR(HSC2-R) = **1.93 ± 0.47** (paper 1.90 ± 0.45) — within 1σ.

**This is the strongest single result of the replication:** the paper's central quantitative claim was independently recovered from public information alone.

### 2d. Text-grounded internal consistency (re-pass, 7 checks) ✅
- ALDH+ % (Fig 3) ↔ f_s posterior: 4/4 within 1σ.
- Fig 2 (a+c) ↔ Table 1 (a+c)_p*: within 3% for both lines.
- Eq 9 w_SLDR self-consistency: exact to 4 sig figs.
- Fig 6 split-dose recovery: forward-predicted saturation at τ ≈ 2–3 h ✓.
- Fig 7 dose-rate: forward-predicted saturation above 1 Gy/min and below 0.01 Gy/min ✓.
- (a+c)_H within Matsuya 2018 reference range: ±1σ overlap ✓ (lenient).

### 2e. Honest negative surfaced ⚠
Table 1 HSC2 α₀,s = 0.194 > α₀,p* = 0.166, violating the paper's own MCMC prior (stem-cell parameters < progeny). Within ±1σ so not strongly wrong, and downstream survival unaffected (f_s(HSC2) = 0.014), but a real Table-1 inconsistency that pass 1 missed.

## 3. What LUCID DID NOT DO (not-exercised)

### 3a. Wet-lab clonogenic assay ❌ (impossible)
LUCID does not have wet-lab. The paper's Fig 5, 6 survival points come from ~2 weeks of colony-formation assay per condition. Not reproducible in this pipeline.

### 3b. Raw flow-cytometry FCS re-analysis ❌ (impossible)
Fig 3 ALDH+ percentages come from aldefluor flow cytometry. Raw FCS files not released. Gating sensitivity (see Q3) unquantified.

### 3c. Vision digitization of Fig 7 ❌ (not done at re-pass)
Fig 7 dose-rate curves were forward-predicted qualitatively but not vision-digitized for a quantitative point-by-point residual. Vision model unavailable at re-pass time. This limits Fig 7 agreement to "qualitative match" rather than numerical.

### 3d. IMK microdosimetric-kernel first-principles re-derivation ❌
(a+c)_H is fit as an output, not derived from a first-principles LET / track-length calculation using Matsuya 2018 track-structure formalism. A true first-principles chain (track → damage → repair-rate) was not attempted.

### 3e. Fig 6 vision-digitization not redone ❌
Pass-1 Fig 6 digitization was wrong-signed. Re-pass switched to forward-prediction only. A correct vision digitization of Fig 6 was not produced; the R² of digitized-vs-model Fig 6 is therefore unreported.

### 3f. Author raw survival CSVs ❌ (impossible)
No Data Availability or Code Availability statement in the paper. No author contact per free-endpoint / no-outreach policy.

### 3g. Extension experiments (Q1–Q5 in open_questions) ❌
Cross-marker (CD44, CD133), cross-tumor-type (GBM, breast), repair-pathway decomposition, ALDH-isoform transcriptomic prediction — all deferred to future work.

## 4. Why not FULL?

**FULL requires:** authors' source code run against authors' raw data, reproducing all published numerics to ≤5%. The authors released **neither** code nor data. Therefore FULL is categorically unreachable from public artefacts. The strongest possible LUCID verdict for this paper is PARTIAL.

## 5. Why not WEAK, SPOT-CHECK, or NO-GO?

- **WEAK** (narrative-only) understates: we have a full numerical implementation, independent MCMC refit within 1σ, and 7 internal-consistency checks. That is far beyond narrative agreement.
- **SPOT-CHECK** does not apply: this is a systematic multi-claim replication, not a targeted single-claim probe.
- **NO-GO** would require the model to fail or contradict the paper. It reproduces cleanly (with one honest sub-σ negative).

## 6. Why PARTIAL rather than PARTIAL-upgrade to REPLICATED?

Per the LUCID guidance (2026-07-05 Rick directive): an analytical/statistical paper with no wet-lab element LUCID could have done may legitimately upgrade PARTIAL → REPLICATED. **This paper does have a wet-lab element** (clonogenic assays behind Figs 5/6, aldefluor flow cytometry behind Fig 3) that LUCID did not reproduce. So the paper does NOT qualify for the analytical-upgrade rule. Verdict stays **PARTIAL**.

## 7. Honest bottom line

- **What we can defend:** independent recovery of headline w_SLDR to within 1σ; 6 of 7 text-grounded consistency checks pass cleanly, 1 fails honestly at <1σ; forward-model qualitative match for Figs 6 and 7.
- **What we cannot defend:** the wet-lab origin of the survival and ALDH+ numbers themselves; a quantitative Fig 7 residual; a first-principles derivation of (a+c)_H.
- **Verdict:** PARTIAL (strong). Coverage 9/10, Agreement 9/10. Ceiling for this paper without author-supplied raw data or code.
