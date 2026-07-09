# Failure Analysis / Honest Critique — Franken 2012 alpha vs gamma RBE

## TL;DR
Verdict: **REPLICATED (model + result level).** But "REPLICATED" here means
the paper's *analytical/numerical* claims all reproduce from Table I; it does
NOT mean the underlying biology was re-experimented. Below is an honest list
of what this replication does not touch, and where the residual uncertainty
lives.

---

## 1. What was fully exercised (headline claims)

- **All four Table-I RBEs** (γ-H2AX 1.0, survival 14.7, fragments 15.3,
  colour junctions 13.3) recomputed from α-coefficients + first-order σ.
  Match to <0.5% central, <1.7% σ.
- **All three Discussion ratios** ("~1% γ-DSBs lethal", "~10% α-DSBs lethal",
  "factor 4 aberrations vs survival") recomputed and passing.
- **All four Fig-2 effect-level RBEs** (γ-H2AX 1, survival 4, fragments 13,
  colour junctions 13) reproduced.
- **Survival divergence >1 decade at 2 Gy** reproduced (1.61–1.78 decades
  depending on β_γ model).
- **Inferred β_γ ≈ 0.096 Gy⁻² / α/β ≈ 1.57 Gy** — value the paper does
  NOT tabulate; recovered by inverting the iso-survival LQ constraint;
  physically sensible (canonical late-tissue range).

---

## 2. What was NOT done

### 2.1 Wet-lab clonogenic assay not reproduced
The actual biological experiment — SW-1573 lung tumour cells, Am-241
α-source at 130 keV/μm mean LET, Cs-137 γ-reference at 0.85 Gy/min,
6-well plating in triplicate, 14-day colony incubation, colony counting
with cutoff ≥50 cells/colony — was not re-performed. This is out of LUCID
scope (no wet-lab capability).

**Impact on verdict:** Neutral. If the *paper's own reported* Table-I
α-values are wrong (i.e. the wet-lab data are compromised), no amount of
downstream arithmetic can rescue the claim. But this replication doesn't
claim to have re-verified the underlying data; it claims to have re-verified
that the paper's numerical conclusions follow correctly from its own tabulated
inputs. That is a real (if narrower) thing to establish.

### 2.2 Monte-Carlo track-structure simulation not re-run
Unusually for a "high-LET RBE" paper, Franken 2012 does not itself contain
a Geant4-DNA / PARTRAC / TOPAS-nBio track-structure MC. Its dosimetry rests
on a transmission-ionization-chamber-calibrated physical Am-241 source, and
its RBE derivation is purely empirical via Table-I LQ fits.

**Impact on verdict:** Neutral — there was no MC pipeline to re-run in the
first place. This is worth flagging because most LUCID targets DO involve
a Monte-Carlo simulation that was never re-run (the classic "LUCID PARTIAL"
pattern). Here, the absence of an MC stage in the original paper means
this replication is unusually complete relative to typical LUCID targets.

### 2.3 Fig-2 raw per-dose data points not digitised (C13)
The 4 endpoints × 2 radiation qualities × 6–7 dose levels of Fig. 2 exist
only as figure pixels. No supplement, no data deposit, no figshare / Dryad
/ Zenodo record found in 2026-06-23 searches. Corresponding author
(n.a.franken@amc.uva.nl) is named but agent-initiated contact is out of scope.

**Impact on verdict:** This is the single named "6/22 rule" missing artifact.
Coverage is 12/13 = 92%. Closing it would require WebPlotDigitizer or
equivalent on Fig. 2 (a manual step). It does not affect the headline
RBE numbers, because those numbers are already the fit outputs printed
in Table I — the raw points would only allow re-fitting from scratch to
check whether the paper's LQ fits were computed correctly, not whether
the RBE conclusions are correct given the fits.

---

## 3. Residual uncertainty (what could still bite)

### 3.1 Interpretation of Fig-2 "RBE=4" for survival
The paper's Fig-2 caption says "RBE=4" for survival without specifying an
effect level. This replication assumed the D₁₀ (10% survival) convention,
which is standard in radiobiology. Alternative conventions:
- D₃₇ (37% survival, natural LQ e-folding) → β_γ shifts ~20% higher
- D₅₀ (50% survival) → β_γ shifts ~30% higher
- iso-2Gy (clinical fraction) → β_γ shifts lower
All choices keep β_γ in the physically sensible 0.05–0.15 Gy⁻² range;
none change the qualitative RBE story. See Open Question 3 for a
sensitivity study extension.

### 3.2 First-order error propagation
Some Table-I α-values have σ/α ≈ 0.3, which is not deep in the
first-order regime. The true σ on the RBE ratio may be 5–10%
underestimated at the tail. Central values are unaffected. Higher-order
propagation (Monte Carlo sampling of α distributions) would be a trivial
extension but was not done because the paper itself uses first-order
propagation.

### 3.3 Table-I precision
`α_α` for survival is given as 2.2 (two sig figs). Half-unit-in-last-place
uncertainty alone shifts RBE by ±0.34, which is well below σ=5.1. Not a
practical issue but worth flagging.

---

## 4. Generalisation warnings (why users should not overclaim from this replication)

- **Single cell line.** SW-1573 is one squamous-carcinoma line. RBE varies
  by 2–3× across cell lines for the same α-source. Do not treat 14.7 as
  "the alpha survival RBE" — it is SW-1573's. See Open Question 4.
- **Single LET point.** Am-241's 130 keV/μm is above the RBE-vs-LET peak
  (~100 keV/μm). Extrapolating to clinical TAT isotopes (Ac-225, Th-227
  at 55–70 keV/μm) requires an explicit LET-RBE model. See Open Question 1.
- **Endpoint = 14-day clonogenic survival.** In vivo, dose-fractionation
  and repair kinetics matter enormously; the LQ fit here is
  single-fraction only. Do not use these numbers directly for fractionation
  planning without a full LQ+repair model.

---

## 5. Verdict rationale

**REPLICATED, not PARTIAL, because:**
1. The paper's headline scientific claim (large RBE for α-particle survival,
   fragments, junctions; RBE≈1 for γ-H2AX) is the direct output of Table-I
   LQ fits.
2. Every one of those fits was re-derived from the paper's own α-coefficients
   and agrees to within 1-digit rounding (12/12 recomputable claims pass).
3. There is no simulation stage or complex pipeline to have "not re-run".
4. The single failed claim (C13) is a data-deposit gap, not a computational
   or scientific gap; it does not falsify or weaken any RBE number.
5. Downgrading to PARTIAL on the basis of the missing raw data would
   conflate "the paper did not deposit its data" (a valid scholarly-practice
   complaint) with "the paper's central claim could not be replicated"
   (empirically false in this case).

This is one of the cleanest LUCID replications on the roster precisely
because the target paper is a numerically-complete, algebraically-simple
analytical result rather than a large simulation study.
