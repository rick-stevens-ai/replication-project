# Failure Analysis — OSTI 3002302 Replication

Independent replication of Ding & Do, *APL Machine Learning* 3, 036112 (2025).
Final verdict: **REPLICATED**. This document catalogues what could have gone
wrong, what did go wrong, and how each issue was handled — so that a future
replicator (human or agent) does not have to rediscover the same lessons.

## 1. Failures that did NOT occur (and why)

### 1.1 Paywall
The paper is published in *APL Machine Learning* under CC BY-NC 4.0, and the
AIP-hosted PDF is paywalled through the publisher's copy. This would have
been a hard blocker for automated fetch. **Mitigation used:** OSTI hosts an
open-access mirror of the same PDF (Ding & Do are ORNL, so OSTI deposition
is mandatory). Direct pull from `https://www.osti.gov/servlets/purl/3002302`
worked without authentication. Recorded PDF MD5
`2b7c8c230cb802ab89cb25f2ec8eb14b` for provenance.

### 1.2 Missing code / data / weights
The single most common failure mode in ML-paper replication is that the
"released" repository is either incomplete, requires proprietary data, or
ships broken weights. **Not applicable here.** The authors' repo
(https://github.com/ljding94/Polydisperse_Sphere) contains:
* Complete network definitions.
* All three distribution families' training + test data (as .npz).
* Normalization statistics.
* Trained VAE / Generator / Inferrer weights for each family.

A `strict=True` load of the released state_dicts into the independently
re-implemented network succeeded with **zero missing and zero unexpected
keys** — this is the cleanest possible confirmation that our architecture
matches theirs.

### 1.3 Percus–Yevick baseline "borrowing"
It would have been tempting to reuse the authors' own `analyze/analyze_PY.py`
for the PY baseline, but that would make the NN-vs-PY comparison
non-independent (any bug in their PY implementation would be silently
inherited). **Mitigation used:** the PY baseline was re-implemented from
scratch from Wertheim's 1963 analytic S(Q) form, including the polydisperse
β correction `β = ⟨F⟩² / ⟨F²⟩` with N=20,000 diameter draws per (pdType, σ)
pair. This means the qualitative agreement (PY, PYβ ≫ NN) is a genuinely
independent confirmation, not a self-comparison.

## 2. Real deviations from the paper's protocol

### 2.1 Compressed retrain schedule
The paper trains the VAE for 1000 epochs and each converter for 300 (frozen)
+ 200 (fine-tune) epochs. Our from-scratch retrain used 300 / 100+50 —
approximately 3–4× less compute. This was a deliberate budget compression,
not an accidental deviation.

**Impact:** every metric on the from-scratch retrain landed within a factor
of ~2 of the released weights (η MAE 0.00161 vs 0.00082; σ MAE 0.00069 vs
0.00060; generator MSE_log10 5.72×10⁻⁵ vs 2.32×10⁻⁵). This is a mild but
non-negligible degradation — consistent with "training is real, not
weight-dependent, but the full 1000-epoch schedule squeezes out the last
factor of ~2 in accuracy."

**Handling:** the released weights remain the primary comparison target
throughout REPORT.md §4; the from-scratch retrain is presented as an
independent confirmation of reproducibility (§4.3), not as the headline
numbers.

### 2.2 PY effective-radius choice
The paper does not specify exactly which R the PY baseline in Figs 5–6
uses. Common choices are ⟨D⟩/2, ⟨D²⟩^(1/2)/2, or ⟨D³⟩^(1/3)/2. We picked
`R_eff = ⟨D³⟩^(1/3)/2` (the volume-averaged effective radius, a standard
monodisperse-equivalent choice for polydisperse systems).

**Impact:** absolute PY MSE_log10 numbers in §4.2 are NOT expected to match
the paper's PY curves exactly. The comparison is qualitative — "PY and PYβ
are 1–2 orders of magnitude worse than the NN" — which is what the paper
also reports and what we do observe.

**Handling:** noted explicitly in REPORT.md §3 "Deviations from the paper"
and again in the Critique section of REPORT.tex.

## 3. Claims not directly tested

### 3.1 Claim C4 — latent-dimensionality / SVD analysis
Paper Fig 4 argues that a 3-dimensional latent space is sufficient, backed
by an SVD/PCA analysis of the dataset. This replication accepts the
architecture (3-dim latent) as-is and does not independently rerun the
SVD/PCA analysis or sweep the latent dimensionality.

**Impact on verdict:** minor. The claim is a design justification, not a
performance claim; the model as delivered works, and this replication
confirms both directions of the mapping at high accuracy on all three
distribution families. The LLM-judge (`argo:gpt-5.2`) flagged this as the
one significant gap and reduced coverage to 0.8 accordingly.

**Handling:** explicitly flagged in Claims table (§2 of REPORT.md) as
`❌ not tested`; called out in the LLM-judge verdict (§4.4); enumerated as
open question OQ4 in `open_questions.json` with concrete next steps.

## 4. Weaknesses of the replication (and of the paper) — from the critique

These are not failures of the replication per se, but boundary conditions
that a user of the paper's method should be aware of. All are documented
in REPORT.tex §"Genuine critique":

1. **PY baseline may be a straw man.** The paper compares against
   monodisperse-decoupling PY, not against stronger polydisperse-aware
   analytic frameworks (Vrij 1979, Kotlarchyk–Chen 1983 LMA, Griffith 1987).
   The 17–120× "win" would likely shrink against a fair baseline. Open
   question OQ2.
2. **Ground truth is synthetic in-distribution only.** No experimental SANS
   / SAXS cross-check. Reported accuracy quantifies in-distribution
   generalization, not real-world inversion. Open question OQ1.
3. **Narrow, dimensionless Q-grid.** Q ∈ [3,13] reduced units, 100 fixed
   points. Deployment to a different instrument grid would require
   retraining or interpolation.
4. **No noise / resolution model.** Training I(Q) are noiseless simulated
   intensities; real SANS has Poisson counting statistics and instrumental
   resolution smearing. Sub-1% rel-err may not survive on noisy data.
   Open question OQ3.
5. **No uncertainty quantification.** The VAE encoder is stochastic and
   could yield calibrated posteriors, but the paper reports point
   estimates only. Open question OQ5.

## 5. Meta: what worked well for future replications

* **Fetch from OSTI, not from the publisher.** OSTI mirror is a reliable
  paywall bypass for any ANL/DOE-lab-authored paper.
* **`strict=True` state_dict load as an architecture sanity check.** This is
  the fastest way to detect a subtle mismatch between your re-implementation
  and the authors' released model.
* **Re-implement baselines from primary literature, not from the paper's
  own code.** Preserves independence of the comparison. Wertheim 1963 is
  short enough (about 20 lines of numerics) to be worth the effort.
* **Compressed training schedules are fine for "does the recipe reproduce?"
  questions.** A 132-second retrain on 1× A100 was sufficient to
  demonstrate the training pipeline is not weight-dependent. Save the
  full-schedule retrain for cases where the compressed version fails to
  reproduce.
* **Always run an LLM-judge with structured JSON output on the same claim
  set as the human-authored verdict.** Provides an independent
  cross-check and forces the verdict prose to be reducible to a small
  number of dimensions (verdict, coverage, agreement).
