# Failure Analysis — PDE-Bernardi-Darcy-heat-spectral-2016

**Overall verdict:** REPLICATED. This file logs the anomalies, dead ends, and gaps encountered
during replication — none of them defeat the verdict, but each is worth naming so the record is
honest.

---

## 1. Typo in the printed source terms of eq. (5.6) — resolved

**Symptom.** Plugging the paper's stated exact solution + printed source terms into the
strong-form PDE (with spectral derivatives at N=30) leaves residuals of `O(π)` for the
Darcy-momentum equation and the heat equation. Only `∇·u = 0` is satisfied by the printed forms.

**Diagnosis.** Symbolic computation with `sympy` pins the discrepancies exactly:

```
F1_paper − F1_required = (π − 1) · cos(πx) cos(πy)
F2_paper − F2_required = (1 − π) · sin(πx) sin(πy)
h_paper  − h_required  = (2π² − 1) · (2π cos(πx) + cos(πy)) · sin(πy) / π
```

Consistent with a missing/mis-scaled `1/π²` factor in T inside the buoyancy source, and a
mis-scaled diffusion coefficient in the heat forcing. Typical transcription / typesetting bug in
the printed forcings; not a methodological flaw.

**Recovery.** Discarded the printed source terms. Used analytically consistent forcings derived
by direct substitution of `u_ex, p_ex, T_ex` into the strong PDE:
`F = α(T_ex) · u_ex + ∇p_ex`, `h = −ΔT_ex + (u_ex · ∇)T_ex`.

**Impact on verdict.** None. The paper's central numerical claim (spectral convergence of the
GLL discretization on a smooth solution) is about the discretization, not the specific forcings.
With the corrected MMS, all five error norms decay spectrally as claimed.

**Reproducibility hazard.** Anyone who copies eq. (5.6) verbatim without checking it will not
reproduce Fig. 1. This is called out prominently in REPORT.md § 5 and in REPORT.tex § 4.

**Artifact.** `report/evidence/mms_residual_printed_sources.txt`.

---

## 2. Argo opus-4.8 LLM-judge endpoint returned proxy 502 — worked around

**Symptom.** The first-choice free LLM judge (Argo `argo:claude-opus-4.8`) returned an HTTP 502
from the local Argo proxy at the moment of the judge call. Retry within the same minute also
502'd.

**Diagnosis.** Transient upstream/proxy fault on the opus-4.8 route. Not the replication's
concern — sibling endpoints on the same proxy answered normally.

**Recovery.** Per the wave-brief fallback rule, invoked two other free Argo models in place of
opus-4.8:
- `argo:gpt-5.2` → verdict REPLICATED.
- `argo:claude-sonnet-4.5` → verdict REPLICATED (quantitative agreement, complete coverage).

Two independent free judges concurring is stronger evidence than a single judge; the 502 was a
minor operational hiccup, not a scientific one.

**Impact on verdict.** None. Full JSON in `report/evidence/llm_judge_verdict.txt`.

---

## 3. No number-for-number match possible with the paper's figures

**Symptom.** The paper reports Fig. 1 (semilog convergence) and Fig. 2 (side-by-side solution
plot) with no numeric error table. The exact numbers on the y-axis at each N are readable only to
the resolution of the printed figure.

**Diagnosis.** Structural constraint of a 2016 IMA-NUMER paper — figure-only reporting is
common. Nothing to fix in this replication.

**Recovery.** Matched the paper's claims at the *qualitative and structural* level: spectral
rate, five norms all decaying, machine-precision plateau near N≈20, indistinguishable exact vs
discrete at N=17. These are the load-bearing claims of § 5.2. Reported observed rates and floor
locations for reader inspection.

**Impact on verdict.** None. Called out explicitly in REPORT.md § 4 ("Magnitude comparison") so
that the reader knows the match is structural, not point-for-point.

---

## 4. Out-of-scope items — acknowledged, not attempted

These are honest gaps, not failures, but they belong on the failure-analysis ledger for
transparency:

- **C6 (a priori estimate proof).** The paper's Thm. 4.7 / eq. (4.16) is a theoretical result.
  This numerical replication confirms *consistency* with the estimate (observed decay is
  spectral / algebraic-N as the estimate allows) but does not re-derive the proof. Full proof
  replication is out of scope for a numerical PDE replication.

- **C7 (existence/uniqueness).** Same status. A weak-solution existence proof cannot be
  numerically replicated.

- **C8 (Horton–Rogers–Lapwood physics demo, Figs. 3–5).** The paper's Sec. 5.3 presents a
  physical illustration with no error metric, no manufactured solution, and no benchmark against
  known stability curves. Reproducing colorful streamlines proves nothing about the
  discretization; skipped by design. If it were to be included in a future extension, the target
  would need to be quantitative (e.g., critical Rayleigh number vs. tabulated values).

- **3D convergence.** Paper's Fig. 1 is 2D only, though the theory in (4.16) covers d ∈ {2,3}.
  The `N^{d/6-s}` velocity pre-factor in the estimate is never numerically exercised. Recorded
  as `open_questions.json` item #4.

---

## Net

- 1 substantive latent bug in the paper (eq. 5.6 typo), diagnosed symbolically and corrected;
  does not change the verdict.
- 1 operational hiccup (Argo opus-4.8 502), routed around via two other free judges.
- 1 structural constraint (no numeric error table in the paper), addressed by matching structural
  claims.
- Several out-of-scope items honestly declared.

No unresolved failures. Verdict: REPLICATED.
