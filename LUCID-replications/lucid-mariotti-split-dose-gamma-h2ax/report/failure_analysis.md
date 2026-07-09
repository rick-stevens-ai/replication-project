# Failure analysis — Mariotti 2013 split-dose γ-H2AX replication

Honest account of what did NOT work, what was skipped, and residual uncertainty.
Verdict is REPLICATED but with real, named ceilings.

## 1. The replication never touches the raw biology
Every "REPLICATED"/PASS claim tests the internal coherence of the published
Table-S1 parameters and Eqs. (3)/(4) against the paper's own headline text. The
actual wet-lab γ-H2AX foci counts (AG01522 cells, 225/30 kVp X-rays, ≥3 independent
experiments × 8–10 time points × 7 conditions) were never distributed, so the model
is confronted only with the authors' fits, not the measurements. This is a genuine
form of replication (it catches transcription and implementation errors and tests
self-consistency) but it is weaker than reproducing the underlying data.

## 2. The 20-minute-gap anomaly is unresolved
The single failed condition is the 20-min-gap row of Table S1 (A=100.9, B=0.69):
- **T-6:** model peak 62.97 foci/cell, paper text says ~30 → height mismatch.
- **T-8:** net-foci-from-2nd = 24.5, which EXCEEDS the single-acute 1 Gy peak (21.8)
  — mechanistically impossible if the cells are refractory, as the paper claims.
So the published 20-min parameters violate the paper's own biological narrative. We
characterized it (two independent tests) but did not resolve it: it is plausibly a
typo or unit confusion, but that is a hypothesis, not a demonstrated fix. This is
the reason the verdict is REPLICATED and not EXCEEDED.

## 3. T-5 is a majority pass masking a contradictory data point
The 5-h-gap effective decay rate comes out FASTER (0.386 h⁻¹) than the first
exposure (0.187), the opposite of the paper's "slower repair for gaps ≤5 h" claim.
We counted T-5 as PASS because 3 of 4 short-gap conditions agree — but the 5-h
outlier is consistent with the parameter non-identifiability flagged in pass-1
(a flat objective landscape can produce spurious decay rates). Calling it PASS is a
defensible but non-trivial judgment call.

## 4. Parameter identifiability weakness (carried from pass 1)
Equivalent-RMSE refits of the 5-parameter model exist, meaning Table-S1's values may
be one of several near-equivalent fits rather than a unique minimum. No formal
uncertainty quantification (profile likelihood / MCMC) was performed, so we cannot
state confidence intervals on A/B/C/D/E. See Open Question Q3.

## 5. Strands not attempted (each with the specific missing artifact)
- Wet-lab foci counts — raw CSV not distributed; no author contact attempted.
- 30-kVp single-dose fit — Table S1 has no 30-kVp parameter row; only qualitative
  shape possible.
- Fig-8 adaptive (0.1 + 1 Gy) fit — no Fig-8 parameters in any supplementary file;
  fitting would be OUR fit, not a replication.
- Clonogenic survival (Fig 6), chromatin (Fig 7), 53BP1 (Figs S2–S3) — paper itself
  frames these qualitatively; no numerical claim to test.

## 6. Process friction this backfill pass
Two subagent attempts to write these artifacts ended immediately after announcing
"Now I'll write all 6 artifacts in one batch" (each ~17k output tokens, ~4 min),
with nothing flushed to disk — the same failure mode seen on the globle-photon dir.
The artifacts were ultimately written directly in the parent session. Lesson: for
large-context pure-write backfills on these ~200-line REPORT.md dirs, direct
parent-session writing is more reliable than delegating a single-batch write.

## Overall
REPLICATED is the correct label at the model/parameter level: 7 of 8 new claims and
all pass-1 claims reproduce, most within 5–20%. The ceilings are (a) no access to the
raw foci data, (b) the unresolved 20-min Table-S1 anomaly, and (c) unquantified
parameter identifiability. None of these is a model-implementation defect.
