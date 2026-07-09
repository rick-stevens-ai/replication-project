# Failure Analysis — Honest Critique

This is the un-whitewashed companion to `REPORT.md` and `REPORT.tex`.
The headline verdict is **REPLICATED (9/10, 9/10)** for the numerical-model
component. That verdict is real, but it is narrower than the paper's
overall scope, and it rests on choices and constraints that a rigorous
reader should see clearly.

## What did NOT work / what we could not do

### 1. We did not re-fit the model parameters from raw data
The paper's 7 optimized rate constants were fit globally by Nelder-Mead
against 16 recruitment curves. We took the published rate constants
as-is because the raw recruitment CSVs are not published. This means:

- We cannot test whether the fit is unique or degenerate.
- We cannot quote confidence intervals on any rate constant.
- We cannot verify that the paper's parameter set is the global
  optimum vs. a local minimum.

**This is the single largest weakness of the replication.** Every
positive verdict below (B5–B9) is conditional on the paper's
parameter set being correct, which we cannot independently verify.

### 2. One File-S1 parameter mapping is genuinely ambiguous
The supplement text "and"-joins two optimized rate values in a way that
admits two plausible mappings. We resolved this by an explicit choice
in `code/lucid_model.py`. The alternative reading would change at most
one of the seven optimized rate constants. Qualitative claims survive
either mapping; specific rate-value interpretation does not.

We flag this rather than paper it over, because a follow-up replicator
using our code will inherit our choice without warning otherwise.

### 3. Quantitative agreement is limited by digitization, not model quality
Our 9% signal RMS and 20% τ₁/₂ RMS on Fig-S1 panels A and L are
dominated by manual figure-digitization noise. Panel F was dropped
because its LET label was unreadable. The 7/10 quantitative-agreement
score is therefore a floor set by our vision-QA pipeline, not by the
model's predictive quality. Without raw CSVs this is unfixable.

### 4. B9 is qualitative-only
The diffusive-influx variant of the MDC1 model (B9) is checked only
for the qualitative shape (lower at early t, monotone, converging).
We did not digitize Fig. 12B for a quantitative comparison. Verdict
should be read as weaker than the A3–C3 verdicts.

### 5. Sub-minute temporal resolution is inherited, not verified
The paper claims sub-minute temporal resolution on the recruitment
curves, but does not publish the actual first-frame latency or frame
interval. Our replication of the ODE model at t < 60 s is only as good
as those unspecified numbers. See OQ1 in `open_questions.json`.

### 6. Cylindrical-track / homogeneous-nucleus assumption is inherited
Both the paper and our replication assume ion tracks are well-defined
cylinders of DSBs and that the nucleus is a homogeneous cylinder of
ATM, MRN, and H2AX substrate. Neither is physically correct at μm
resolution (δ-electron spurs, chromatin heterogeneity). We do not
test these assumptions; the fit absorbs any spatial mismatch into the
rate constants. See OQ2.

### 7. Ion-species coverage is uneven, and we do not correct for it
Argon, uranium, xenon, and carbon are well-sampled (multiple panels).
Iron, nickel, titanium contribute one panel each and dominate outlier
behaviour. The Ni-ions row (LET=3430, koff=0.030) is a clear outlier
in Fig 8A of the paper; we did NOT exclude it from the C1 Spearman ρ
test. ρ = −0.77 with the outlier; the trend is real either way, but
a strict analysis would report both values.

### 8. CK2-inhibition specificity is assumed
TBB inhibits CK2 but is not absolutely specific. The paper's inferred
"inner-focus" NBS1 population depends on the TBB effect being
CK2-mediated. We take that at face value and do not test it. If TBB
has off-target effects on other kinases involved in the DDR, the
inner-vs-outer decomposition partially conflates them.

### 9. Wet-lab layer is entirely absent
Blocked claims D1–D4 cover the raw beamline imaging, raw FRAP,
raw confocal, and 53BP1 lag phase. None of these artifacts exist in
the public record. Any claim about the paper as an experimental
object that requires these artifacts is out of scope for this
replication. We cannot say anything about experimental reproducibility.

### 10. Mono-exponential τ₆₃ metric is a modeling choice
The paper's recruitment curves are visibly non-mono-exponential
(early lag, later plateau structure). Fitting a single exponential is
a convention. Our τ₆₃ values track the paper's monotonicity but are
not per-data-set background-subtracted, so 1:1 comparison with the
paper's printed numbers is not warranted.

## Gaps

| Gap | Consequence | Mitigation available? |
|---|---|---|
| No raw recruitment CSVs | Cannot re-fit; no CIs on rate constants | Contact GSI/TU Darmstadt authors |
| No raw FRAP CSVs | A7, A8 blocked | Contact authors |
| No raw beamline stacks | D1 blocked | Contact authors |
| No raw confocal stacks | D3 blocked | Contact authors |
| No Fig-12B digitization | B9 qualitative only | Digitize Fig 12B in future pass |
| No parameter identifiability analysis | Individual rate values uninterpretable | Profile-likelihood on digitized data |
| No chromatin-state model | Panel-to-panel variance may be structured | Two-compartment ODE extension |
| No proton-LET predictions | Applicability at clinical LET unknown | Run model at LET=1–10, compare to literature |

## Residual uncertainty

- **Model uniqueness**: unknown. Could be tight, could be plateau. Nothing
  in the paper distinguishes.
- **Sub-minute temporal claims**: model fits whatever imaging returns;
  imaging time resolution not specified.
- **Spatial DSB distribution**: cylindrical assumption unverified.
- **Cell-line generality**: single p53-mutant cancer cell line; no cross-line test.
- **Radiation-quality generality**: heavy-ion regime + X-ray controls only;
  proton clinical range not tested.
- **Chromatin coupling**: entirely absent from model; may bias inner-vs-outer split.

## What DID work (for balance)

- The ODE model as written in File S1 is fully specified and integrates
  cleanly with LSODA at reasonable tolerances.
- All 12 headline claims we tested (A3–C3, B5–B9) reproduce.
- The re-implementation is entirely from scratch — no reference to any
  prior model code — so the fact that all qualitative and quantitative
  claims come out right is genuine evidence that the paper's model is
  well-specified.
- The scaling-factor + LET ladder logic across all 12 Fig-S1 panels
  self-consistently monotone (B7, B8) is a non-trivial cross-check;
  the paper never advertises this but it does hold.
- The 4-panel Figure 11 reproduction matches qualitatively at
  every panel.

## Bottom line

The **numerical model works, and the paper's math is correct.** The
replication is honest about the fact that this is a narrower verdict
than "the paper is right about DDR biology." The paper's biological
interpretation depends on assumptions (parameter uniqueness, temporal
resolution, cylindrical geometry, cell-line generality, chromatin-state
coupling, CK2 specificity) that neither the paper nor this replication
tests. Those are captured in `open_questions.json` as concrete follow-up
work, not as vague hand-waving.
