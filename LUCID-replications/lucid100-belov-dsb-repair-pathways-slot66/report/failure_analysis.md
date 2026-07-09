# Failure Analysis — Honest Critique

**Slot:** lucid100-belov-dsb-repair-pathways-slot66
**Paper:** Belov et al. 2015, JTB 366:115–130 (open-access surrogate: JINR E19-2014-39)
**Verdict on disk:** PARTIAL (Coverage 7/10, Agreement 6/10)
**Tracker verdict:** REPLICATED

This is a critical audit, not a whitewash. The paper is scientifically interesting and
its 22-ODE / 46-parameter architecture is fully reproducible **as a forward simulation
at the published parameter point**. But there are real structural, quantitative, and
methodological gaps — some in the paper, some in this replication.

---

## 1. What did not work

### 1.1 Fig 11 ratios (C6) — the one hard number-vs-number claim failed

The single claim in the paper body that is a concrete figure-level number-vs-number
comparison is the Fig 11 headline: ERCC1/XPF⁻ : WT γ-H2AX foci ratios of
**2.2 / 2.5 / 2.9 at 12 / 24 / 48 h after 2 Gy γ-rays**.

The replication returns **∞ (degenerate)** for all three timepoints because the WT
γ-H2AX state x14 decays to (numerically) zero long before 12 h. This is not a bug
in the replication; it is a direct consequence of two undisclosed conventions in
the paper's Appendix A:

- **Table A.1 K1..K7 units inconsistent.** The pseudo-first-order Ku→DSB binding
  rate implied by K1 = 1.67×10⁻¹ M⁻¹ min⁻¹ × [Ku] = 9.19×10⁻⁷ M is
  ~1.5×10⁻⁷ min⁻¹, i.e. a half-time of ~4.6 **million** minutes. The data the paper
  fits (Reynolds et al. 2012 FRAP) reports half-times of ~15–30 s. A 6–7 order-of-magnitude
  mismatch. Most plausibly a units typo (M⁻¹ vs µM⁻¹; min⁻¹ vs s⁻¹) but the appendix
  does not disclose which.
- **γ-H2AX x14 has no non-negativity constraint.** The RHS
  `dx14/dτ = K9·sum·x15 / (K10 + sum) − K11·x13 − K12·x14`
  can drive x14 negative once the NHEJ source `sum` decays to zero. The paper's
  figures cannot show negative foci, so an unstated clipping / scaling / steady-state
  convention must be applied at figure-generation time.

**Neither convention can be recovered from the paper alone.** The authors' driver
code is not deposited (`no-code-deposit` friction tag). Corresponding author dem@jinr.ru
has not been contacted (offline-only protocol).

### 1.2 Figs 3, 5, 7, 8, 9, 10 not reproduced curve-by-curve

Six figure panels overlay model curves on cited experimental data (Rydberg 1996,
Löbrich 1996, Reynolds 2012, Rothkamm 2003, Okayasu 2012, Shibata 2011, etc.).
**None of the underlying data tables are deposited.** A bit-exact reproduction
requires WebPlotDigitizer extraction of 6+ panels. This is a small CPU job that
was not done in the first pass and is not done in this backfill (no re-simulation
per the backfill task rules).

Qualitative reproduction (peak timing, peak amplitude ordering by cell line,
LET-dependent shift) matches; **quantitative reproduction of any of these six
panels does not exist** in either the paper's supplement or this replication.

### 1.3 Fig 11 units-repair attempts explored, none satisfactory

Two independent hypotheses were tried:

- **H1: as-published.** Fig 11 fails (degenerate ∞) as documented.
- **H2: binding-speedup by 10⁶ (units typo hypothesis).** Fixes the K1..K7 half-times
  to ~30 s, but then x14 either (a) decays to ~0 within seconds (before any γ-H2AX
  foci can form on the hours timescale the figures show) or (b) goes negative
  under the un-clipped RHS.

**Both hypotheses fail C6.** A third path — digitising the Fig 11 curves themselves
and back-fitting the missing units + clip conventions — was ruled out of scope for
the first-pass replication.

---

## 2. Structural gaps in the paper (independent of the replication)

These are gaps in the paper's model, not gaps in this replication's fidelity.

### 2.1 Pathway competition assumed, not fit

The three-pathway architecture (NHEJ + HR + SSA) is **imposed by construction**,
not fit against pathway-choice data. There is no likelihood ratio / model comparison
against a 2-pathway (NHEJ + HR only), 4-pathway (adding MMEJ), or 5-pathway
(adding B-NHEJ resection-independent branch) alternative. The 3-pathway choice is
justified biologically in §2 but not statistically defended.

### 2.2 Cell-cycle dependence not tested

The model has **no cell-cycle compartment**. HR is biologically restricted to S/G2
(requires a sister chromatid); the paper acknowledges this but runs HR and NHEJ in
parallel without any cycle-phase gating. G1-vs-S/G2 differential kinetics — a first-order
prediction any DSB repair model should make — is **neither predicted nor validated**.
The four repair-deficient cell lines are treated as parameter shifts on the same
acyclic pool, not as population mixtures over G1 / S / G2.

### 2.3 Identifiability not quantified

Forty-six rate constants fit to ~10 literature time-courses via Newton–Raphson.
**No profile likelihood, Fisher information, or Sobol sensitivity analysis is
reported.** Practical unidentifiability is nearly certain: many parameter
combinations will fit the training data equally well. Predictions on unseen
conditions (e.g. high-LET MMEJ upregulation, resection-checkpoint kinetics,
cancer cell lines) have no confidence intervals — and the paper does not claim
they do, but readers may not notice.

### 2.4 Alt-EJ / MMEJ omission

Acknowledged limitation in the paper's Discussion. But given that MMEJ is now
known to carry >30% of end-joining at high LET where classical NHEJ is
overwhelmed (Sharma 2015, Truong 2013), Belov's Fig 10 high-LET slow-clearance
attribution to reduced NHEJ efficiency is **partially confounded** by an
absent MMEJ compartment. The two explanations are not identifiable from a
γ-H2AX-only read-out.

### 2.5 γ-H2AX foci as dead-end read-out

The model stops at foci. There is no coupling to mis-rejoining, chromosome
aberration formation (dicentrics, translocations), or downstream carcinogenic
endpoints. Other frameworks — BIANCA (Ballarini 2014), MEDRAS (McMahon 2016),
NASA NSCR-2020 — include an aberration-formation step. Belov's framework's
utility for the LUCID initiative's downstream use case (predicting late
cytogenetic endpoints from early DSB kinetics) is therefore **limited by
construction**.

---

## 3. Methodological gaps in this replication

These are honest limitations of the replication itself.

### 3.1 No re-fitting

Table A.1 rate constants used verbatim. The paper's Newton–Raphson fitting step
was **not** redone. This means the replication verifies the model **structure**
+ the **parameters as printed**, but does not independently confirm that those
parameters actually best-fit the cited literature time-courses. If Table A.1
has any transcription typos (beyond the K1..K7 units issue), they would propagate.

### 3.2 Integrator substitution not sensitivity-tested

Paper: RK4. Replication: LSODA. Verified integrator-independent for α(L) and
Nir-row checks (both are analytic in the relevant regime); **not formally tested
for γ-H2AX curves**. The x14 source/decay structure is potentially stiff, so
LSODA is safer, but a controlled RK4 vs LSODA comparison for the Fig 5–11
scenarios was not done.

### 3.3 No experimental overlay digitisation

Would have taken 2–4 hours with WebPlotDigitizer. Not done in the first pass.
Would enable quantitative validation of Figs 3 / 5 / 7 / 8 / 9 / 10 / 11 against
their published overlays even without author code.

### 3.4 No author contact

dem@jinr.ru not pinged. A single email requesting the driver code would likely
resolve the K1..K7 units question and the x14 clipping convention in one round
trip. Not done per offline-only protocol.

### 3.5 JTB version not fetched

Elsevier paywall. Replication relied entirely on the JINR E19-2014-39 open-access
preprint. **No evidence the JTB Appendix differs** from the preprint Appendix
(same equation numbering, same tables, same parameter values), but not
independently verified. If the JTB version silently fixed the K1..K7 units issue,
this replication would not have caught it.

### 3.6 Verdict inconsistency preserved, not resolved

On-disk `REPORT.md` = PARTIAL (7/10, 6/10). Tracker slot = REPLICATED. Backfill
preserves both. The scientifically honest call is **PARTIAL** — the "REPLICATED"
tracker entry is an over-optimistic aggregation of the 5/6 pass rate that ignores
the C6 blocker. A proper reconciliation would either (a) reclassify the tracker
entry to PARTIAL, or (b) require the tracker to distinguish "structural
replication PASS" from "figure-level replication PASS".

---

## 4. Residual uncertainty summary

| Question | Resolution status | Confidence |
|----------|-------------------|:----------:|
| Are Appendix A eq (1)–(22) correctly transcribed? | Yes, verbatim | high |
| Are Table A.1 46 constants correctly transcribed? | Yes, verbatim | high |
| Are Table A.1 K1..K7 in the units they claim? | **Almost certainly NOT** (6–7 orders of magnitude off) | high |
| Which units convention is correct for K1..K7? | Unknown (M⁻¹ vs µM⁻¹? min⁻¹ vs s⁻¹? both?) | low |
| Does x14 need clipping to ≥ 0 in the figure code? | Almost certainly yes | high |
| What is the exact x14 post-processing convention? | Unknown | very low |
| Are Fig 11 ratios 2.2/2.5/2.9 recoverable with the right conventions? | Plausibly yes | medium |
| Are the 46 rate constants practically identifiable? | Almost certainly NOT | high |
| Does the 3-pathway architecture generalise to cancer lines? | Untested | very low |
| Does the model predict cytogenetic aberrations? | No (out of scope) | high |

---

## 5. What would close the gaps (if we could re-run)

Ordered by effort × payoff:

1. **[1 email, ~1 day round-trip]** Ping dem@jinr.ru for driver code. Would resolve
   K1..K7 units + x14 clip in one shot.
2. **[2–4 h CPU]** WebPlotDigitizer on Figs 3 / 5 / 7 / 8 / 9 / 10 / 11 experimental
   overlays. Enables quantitative validation without author code.
3. **[4–8 h CPU]** Profile-likelihood or Sobol sensitivity on the 46 constants
   using the digitised overlays. Quantifies identifiability.
4. **[1–2 d dev]** Add MMEJ compartment (4th pathway) + refit against Grabarz 2013
   MMEJ-reporter data. Tests whether the high-LET slow-clearance attribution is
   confounded.
5. **[2–4 d dev]** Add cell-cycle compartment (G1 / S / G2 population mixture).
   Tests whether the acyclic pool ansatz is defensible.
6. **[1 wk dev]** Couple foci output to a Ballarini-style pairwise-misrejoining
   dicentric predictor. Tests whether the model has extrapolation value for
   LUCID's downstream cytogenetic use case.

None of the above is planned in the current backfill scope.

---

## 6. Bottom line

**The paper's model IS reproducible as a forward simulation** — 22 ODEs, 46 constants,
16-row Nir table, all typed in verbatim from the open-access preprint, all
5/6 structural claims verified. **The paper is NOT reproducible at the figure-level
number-vs-number bar** — the one testable Fig 11 headline (ratios 2.2/2.5/2.9)
degenerates to ∞ because two Appendix A conventions (K1..K7 units + x14 non-negativity)
are undisclosed. This is the paper's fault, not the replication's; but this replication
did not close either gap either. Honest verdict: **PARTIAL**. The "REPLICATED" tracker
label overstates the depth of the verification.
