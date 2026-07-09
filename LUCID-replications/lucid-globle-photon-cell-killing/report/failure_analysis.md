# Failure analysis — GLOBLE photon cell-killing replication

Honest assessment of what did NOT work, what was skipped, and residual uncertainty.
This is intentionally not a whitewash; the verdict is REPLICATED but the replication
has real ceilings.

## 1. The one empirical test is BLOCKED (the biggest gap)
Claim 7 — exact pointwise overlay of the model against **measured** cell-survival
points — is BLOCKED and remains so. Every other "REPLICATED" claim is either:
- a reproduction of the paper's **equations** against the paper's **own** tabulated
  parameters, or
- an internal self-consistency / closed-form check.

None of them independently corroborate GLOBLE against experimental biology. Root
cause (friction F2): the authors digitized their experimental points with GetData
Graph Digitalizer but never redistributed them; the paper PDF, supplement, and any
locatable author site do not contain the raw CSV. The primary source papers (Steel
1987, Stephens 1987, Holmes 1990, Ruiz de Almodóvar 1994) are not in the reachable
LUCID-100 corpus either. **Consequence:** the model's agreement with nature is
assumed, not verified, in this reproduction.

## 2. Several "new" claims are correctness checks, not corroboration
Claims A (ε_i < ε_c), D (Table 3 = Table 2), F (Eq. 8 identity) mostly confirm that
(a) our transcription of Tables 2/3 is faithful and (b) the ODE reproduces the closed
forms the paper derives from the same parameters. These are worth having — they catch
transcription and implementation bugs — but they are self-referential and should not
be read as independent validation of the GLOBLE hypothesis.

## 3. Column-ambiguous median statistic
The paper's "median HLT_i = 0.458 h" matches only the split-dose column (5 lines).
The dose-rate column median is 0.487 h and the pooled 22-set median is 0.486 h. The
paper text does not say which column it means. We report all three rather than
silently selecting the matching one — but the ~6% discrepancy is unexplained and may
indicate the two assays probe different repair timescales (see Open Question Q3).

## 4. Regime-dependent convergence of the analytical limits
Claim E's high-dose-rate limit only reaches the 0.05 log-space tolerance at ≥10^6
Gy/h. At 10^4 Gy/h it FAILS for the shortest-HLT_i lines (e.g. CHO K1 at 0.035 h).
This is expected physics (the instantaneous limit must beat the repair half-life by
orders of magnitude), not a paper-vs-replication defect — but it means the
"static-GLOBLE limit" is only reproducible at dose rates far above any clinical or
FLASH regime.

## 5. Source ambiguity resolved by choice (F8)
The Fig-4 caption states ε_i = 0.002 for α/β = 5.26 Gy, which is internally
inconsistent with Eq. 8. We used ε_i = 0.005 (Eq.-8-consistent, carried from pass 1).
This is a genuine ambiguity in the published paper; our resolution is defensible but
is a judgment call, not a reproduction of the printed number.

## 6. Scope not attempted
- Deterministic-effect claim (Claim 5) reproduced only at the model level — no
  validation against clinical pneumonitis / bone-marrow endpoints.
- Supplement File S1 closed-form approximation: PARTIAL (we implement the ODE + Eq. 38
  numerically instead; F3).
- No uncertainty quantification on the fitted parameters; all runs are point estimates.

## 7. Process friction this backfill pass
Two subagent attempts to write these report artifacts timed out on the write-flush
step (one at 2m58s, one at 3m37s after announcing "writing in parallel") despite the
underlying task being pure-write from an existing rich REPORT.md. The artifacts were
ultimately written directly in the parent session. Lesson: for large-context
pure-write backfills, direct writing is more reliable than delegating when the
subagent keeps dying before flush.

## Overall
REPLICATED is the right label for the model/equation level and the label is well
supported across 17 cell lines and both Table-3 columns. But the replication's
ceiling is data availability: without the authors' digitized experimental points, the
central empirical validation of GLOBLE cannot be independently reproduced here.
