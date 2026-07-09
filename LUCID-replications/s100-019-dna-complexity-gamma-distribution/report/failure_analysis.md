# Failure analysis — Slot #19

**Purpose.** This file exists to say honestly, in one place, what this
replication does *not* answer, and where the paper's own claim graph is
vulnerable even if you accept the analytical reproducibility we
demonstrated. This is not the executive-summary spin; this is the
"where would a skeptical reviewer poke."

---

## 1. The verdict-mismatch problem (queue-side vs actual)

The LUCID-Second100 queue labels this slot **REPLICATED**. That label is
misleading on its own. What was actually reproduced is the *analytical
downstream* of the paper — the parametric functional forms, the fitted
constants (taken verbatim from the authors' repo), the closed-form Gamma
PDF, and the end-to-end pipeline against a single bundled X-ray
spectrum. What was *not* reproduced is the upstream that the paper's
central claim actually rests on:

- The TOPAS-nBio Monte-Carlo of 16 monoenergetic ion beams + a 250-keV
  X-ray reference + two 3-MeV validation beams was not re-run.
- The per-track SDD damage tables that the Gammas were fit to were not
  regenerated (and are not deposited).
- The per-beam (α_j, β_j) pairs were not re-fit — we only evaluated the
  authors' published quadratic summary.
- Consequently the paper's central R² > 0.999 goodness-of-fit claim is
  neither verified nor refuted here.

Under the LUCID four-tier rubric (REPLICATED / PARTIAL / SPOT-CHECK /
NO-GO), an honest label would be **PARTIAL** (analytical layer fully
reproduced; upstream MC layer untouched) or, more conservatively,
**SPOT-CHECK** (parameter-constant retrieval + closed-form re-evaluation
+ one end-to-end pipeline against a single bundled data file). The
"MC-code pattern" flagged in the backfill brief applies exactly here:
this is one of the ~39% of session verdicts likely to be a queue-side
mismatch. Preserved as REPLICATED per instruction; flagged so a
downstream re-adjudicator can revisit.

## 2. What could go wrong even if you trust our replication

Suppose everything we did is correct. What still could fail?

**(a) The authors' published parameter constants could themselves be
wrong.** We took them verbatim from `src/mgm.py`; we did not refit. If
`src/mgm.py` disagrees with the paper text (as it does for the Gamma
call — see Issue #1 in REPORT.tex), which is authoritative? We do not
know which convention was used at fit time, so we do not know which
publication of the constants is the intended one. The result: the
paper is potentially internally inconsistent (text formula vs code
call), and no downstream user can be sure which one to trust without
raw SDD data.

**(b) The published R² > 0.999 could be an artifact of over-flexible
fitting.** A Gamma has two free parameters per beam; 16 beams gives
32 (α, β) points, then summarized by 6 quadratic coefficients (3 for α,
3 for β). If the raw complexity histograms are themselves fairly
smooth and narrow (small support: complexity ∈ [1, ~20]), then almost
any two-parameter unimodal distribution family will hit R² > 0.99.
The paper does not compare against alternative distribution families,
and the raw histograms are not deposited, so the "Gamma specifically"
claim is essentially untestable from the deposit. This is Open
Question #1.

**(c) The quadratic α(yF), β(yF) is a phenomenological convenience,
not a mechanism.** β(yF) goes negative at yF ≈ 175 keV/µm, inside the
paper's own stated validity window. The paper does not warn about
this. This is a diagnostic — not proof, but a diagnostic — that the
quadratic form is a curve-fit rather than a mechanistic law. The
paper's own SBI/BDI use physically-motivated saturating exponentials;
switching to unrestricted polynomials for the Gamma parameters is
asymmetric and unexplained. This is Open Question #2.

**(d) The downstream cell-survival application (Fig 5) uses a
"qualitative" sigmoid repair model.** The paper itself uses that word.
That means the RBE-vs-LET curves in Fig 5 are at most a weak
downstream test of the Gamma-complexity hypothesis — if they agree
with data, that could be because the Gamma-complexity is capturing
real biology, or because the sigmoid repair model has enough free
parameters to absorb residuals. A mechanistic repair model
(Medras, LEM-IV, PARTRAC-NHEJ) would be a stronger test. This is
Open Question #3.

**(e) The scoring-volume choice (1 µm sphere) is not tested for
sensitivity.** Complexity is scale-dependent. The Gamma family might
fit at 1 µm but fail at 100 nm (nucleosome scale, dense track-core
physics) or at 5 µm (nucleus scale, multiple independent tracks
smeared together). No sensitivity study is reported. This is
Open Question #4.

**(f) The whole paper is validated only against cell-survival data
(Fig 5), never against repair-free plasmid DSB-yield data.** Plasmid
data would isolate the physics layer from the biology layer and would
be a much cleaner test of the Gamma-complexity model. The paper does
not do this. This is Open Question #5.

## 3. What could go wrong with our own replication

Being honest about our own artifact:

- The `code/replicate_mgm.py` script uses `numpy.random.default_rng(seed=42)`
  for the 1 000-event X-ray subsample from the 116 077-event phase-space.
  A different seed could shift the recovered `n_sites_with_DSB_per_track`
  by ~few%. We report 0.091 as the mean; we did not compute a bootstrap
  CI over subsample seeds. A tighter replication would sweep seeds.

- We did not independently verify that the parametric functions in
  `src/mgm.py` match the paper text formula-by-formula. We copied the
  code verbatim and evaluated it. If `src/mgm.py` had a typo relative
  to the paper text in any of the SBD/SBI/BDD/BDI/N_sites functions,
  we would have inherited that typo silently. (The one place we did
  cross-check, the Gamma call, disagreed with the paper text — see
  Issue #1. That should be treated as a warning that the code and
  paper are not tightly co-audited.)

- We did not attempt to independently derive the microdosimetric
  spectra for the 16 monoenergetic beams (only used the one bundled
  X-ray spectrum). The MGM pipeline was therefore never exercised for
  a proton or alpha beam end-to-end; only for the X-ray reference.
  That is a real gap even within the analytical-layer scope.

- We did not attempt to re-derive the (α, β) parameters from any
  proxy data (e.g., published RBE curves at known LET, or plasmid
  DSB-yield curves at known LET). A proxy re-derivation could have
  provided an independent cross-check of the published constants
  without requiring the missing SDD files. This would have been a
  cheap, high-value probe that we did not do.

## 4. Bottom line

The paper's analytical downstream is internally consistent and
reproducible with the deposited code + one deposited data file. The
paper's central quantitative claim (the Gamma family fits per-track
damage complexity with R² > 0.999 across LET) is not independently
testable from the current deposit — the raw SDD histograms are not
there. The paper's downstream physical-biological application
(RBE-vs-LET via a sigmoid repair model) is explicitly qualitative and
should not be treated as strong validation of the Gamma-complexity
hypothesis.

Honest one-line summary: **the paper is analytically reproducible but
scientifically under-tested against alternative distribution families,
alternative meta-fit functional forms, alternative scoring geometries,
and repair-free plasmid data.**
