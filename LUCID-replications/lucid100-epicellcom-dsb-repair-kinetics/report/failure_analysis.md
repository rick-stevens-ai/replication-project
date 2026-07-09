# Failure Analysis — Scott 2011 Epicellcom DSB Repair Kinetics

## 1. Verdict cross-check (Rick's 2026-07-05 rule)

**Queue verdict:** REPLICATED.
**On-disk actual verdict (from REPORT.md line 5):** REPLICATED — model.
**Cross-check result:** **MATCH.** No verdict-inflation detected.

Confidence: **high**. The REPORT.md verdict is specific about scope
("REPLICATED — model") and is backed by:
- All model equations re-implemented in `code/multisig1.py`.
- All five model figures regenerated in `figures/`.
- 7 of 8 numerical spot-checks against the paper's own body text within
  <=0.1%.
- The single mismatch (Att_2 at 1000 mGy) is diagnosed as a paper labeling
  typo, not a model error, with the three neighbouring numbers in the same
  sentence all agreeing exactly.
- The paper's own Fig 2 (authoritative) is reproduced faithfully.

The verdict is honest: it does not claim wet-lab agreement (which is not
tested) and it does not claim generalisability outside the paper's fitted
parameter set.

## 2. Genuine failure modes / limitations in this replication

### 2.1 Wet-lab data not overlaid
- The paper says the model's 5 mGy and 20 mGy curves "compare favorably"
  with Rothkamm & Lobrich 2003.
- This replication does not digitise R&L Fig 1/Fig 2 and does not overlay
  them on `figures/fig5_residual_DSBs.png`.
- Impact: the "REPLICATED — model" verdict is silent on whether the model
  actually matches the wet-lab data the author claims it fits. This is a
  genuine gap and is captured in Q4 / Q5 of `open_questions.json`.

### 2.2 Cell-communication claim not tested
- The paper is titled "Epiregulated Cell-Community-Wide (Epicellcom)
  Response...".
- The mathematics (Eqs 3-14) contains no explicit intercellular signaling
  term.
- This replication reproduces the mathematics faithfully but cannot test
  a claim the paper never operationalised. Reported as Q2 in open questions.

### 2.3 Cell-type mismatch: "Epi-" is not epithelial
- The parameter set is fit against MRC-5 lung fibroblasts.
- The paper's "Epi-" prefix is epigenetic / epi-regulated, not epithelial.
- The task brief hypothesised an epithelial cell-cell communication study;
  the paper is actually a fibroblast pharmacokinetic model with an
  intercellular-signaling narrative frame. Documented and flagged as Q1.

### 2.4 Threshold model may be a fit-simplification
- T = 1.4 mGy is a bright-line cutoff below which BPM(D) is undefined.
- R&L's own reported 5 mGy hypersensitivity suggests a graded low-dose
  response.
- Not tested here. Q4 in open questions.

### 2.5 2D-only geometry
- Confluent monolayer calibration; no 3D / organoid extension.
- Recent literature (Broutier 2017; Driehuis 2019; Bhaduri 2020) shows
  2-3x slower repair in 3D vs matched 2D. Not addressed. Q5 in open
  questions.

### 2.6 Author typo left in paper (informational, not a replication failure)
- p. 589 says "Att_2(D) = 46.7%" at D = 1000 mGy. The value 46.67% is
  actually Att_1 with BPM = 0.762. Att_3 and Att_4 in the same sentence
  match our re-derivation to 2 significant figures.
- No author contact per task rules.

## 3. What did NOT fail

- Equation transcription (all cross-checked against the PDF).
- Figure regeneration (all 5 model figures match visually).
- Parameter values (matched to paper's Table 1 / body text).
- Numerical spot-checks (7/8 agree to <=0.1%; 8th is a paper typo).
- Reproducibility (deterministic, pure Python, <1 s runtime).
- Cost discipline (no paid endpoints, no LLM calls, no HPC).

## 4. Write-strategy compliance (Rick's 2026-07-06 rule)

This backfill followed the incremental-write protocol:
1. Read REPORT.md once (first tool call).
2. Wrote each of the 7 artifacts as a separate `write` tool call.
3. No batch multi-file patches.
4. No re-runs of sims.
5. All pre-existing files preserved (verified by `find . -type f` before
   and after).
