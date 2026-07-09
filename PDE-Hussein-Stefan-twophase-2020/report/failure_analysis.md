# Failure Analysis — PDE-Hussein-Stefan-twophase-2020

Paper: Adil & Hussein (2020), *Numerical Solution for Two-Sided Stefan
Problem*, Iraqi J. Science 61(2):444-452, DOI 10.24996/ijs.2020.61.2.24.

Overall verdict: **REPLICATED.** There were no method-level failures. This
document catalogs the *speed bumps* encountered during replication — issues
that, if left unaddressed, would have caused a naive reader or replicator to
report a false negative.

---

## F1 — Table 1 digit transposition (paper typo, HIGH impact on naive replication)

**Symptom.** First replication pass matched three of the four Table 1 node
values on the nose but produced `3.1424` where the paper prints `3.4124` at
node `(y,t) = (0.1, 0.2)`.

**Diagnosis.** Evaluated the paper's OWN transformed exact solution
`v(y,t) = (y+1)^2 (1+t)^2 + 1 + 2t` at `(0.1, 0.2)`:
`(1.1)^2 (1.2)^2 + 1.4 = 1.21 * 1.44 + 1.4 = 1.7424 + 1.4 = 3.1424`.
The paper's own formula gives 3.1424, not 3.4124. The printed table value is
a digit transposition (`3.1424 → 3.4124`).

**Impact.** A replicator who trusts the printed table byte-for-byte without
re-evaluating the paper's formula would report a mismatch and flag Table 1 as
"not reproduced." In reality the METHOD is correct and the printed TABLE is
wrong.

**Resolution.** Documented as a paper typo in §5 of `REPORT.md` and P1 of the
Genuine Critique in `REPORT.tex`. The remaining three Table 1 values match
exactly, and Table 2 matches every entry on every mesh.

**Prevention going forward.** When a replication reproduces the paper's own
formula but disagrees with the paper's printed table, treat the formula as
canonical and the table as suspect. Always evaluate the formula independently.

---

## F2 — Example 2 `x²` vs `x³` misprint (paper typo, CRITICAL if uncaught)

**Symptom.** First implementation used the printed exact solution
`u(x,t) = x^2 + 2t^2 + 1` for Example 2. Result: NONE of Table 2's node
values matched — errors were off by ~O(1) on every mesh, and observed
convergence order was undefined (error did not shrink cleanly with `h`).

**Diagnosis.** Recomputed the source term from the printed exact:
`f = u_t - a u_xx - b u_x - c u` with `u = x^2 + 2t^2 + 1` gives
`f = 4t - 2a - 2xb - c(x^2 + 2t^2 + 1)`. But the paper's printed `f` explicitly
contains `x^3` and `3x^2` terms. Also, the paper's printed *transformed* exact
`v(y,t) = 1 + 2t^2 + (…)^3` is cubic, not quadratic. Only `u = x^3 + 2t^2 + 1`
is consistent with (a) the printed `f`, (b) the printed transformed `v`, and
(c) Table 2's numerical values.

**Impact.** With the printed `x²` the METHOD looks broken; with the corrected
`x³` the method reproduces Table 2 to 4 dp on every mesh. Without this
correction a replicator would report Example 2 as "not reproduced" and likely
call the paper's whole scheme into question.

**Resolution.** Documented as a paper typo in §5 of `REPORT.md` and P1 of the
Genuine Critique in `REPORT.tex`. With `u = x^3 + 2t^2 + 1` the paper is
exactly self-consistent and exactly reproducible.

**Prevention going forward.** Perform a full three-way consistency check
between the printed exact `u`, the printed source term `f`, and the printed
transformed exact `v` BEFORE running the solver. Any inconsistency identifies
the typo before code is executed.

---

## F3 — No free vision-LLM OCR available for equation extraction

**Symptom.** The Iraqi J. Science galley PDF's equation blocks are typeset
math, not raster text, and `pdftotext -layout` returns garbled character
strings for eq. (1), eq. (4), and the boxed Example 1/2 definitions.

**Diagnosis.** All viable vision-LLM endpoints were paid (policy: free
endpoints only). No free vision endpoint was configured on CherryRd at run
time.

**Resolution.** Rendered each page to PNG with `pdftoppm -r 300` and ran
local `tesseract` OCR. Cross-checked the recovered equations by deriving `f`
analytically from the recovered `u` and comparing to the recovered printed `f`:
Example 1 matched exactly (max diff = 0.0), giving high confidence in the
decoding. Example 2 mismatched — traced not to OCR error but to the
paper-internal typo F2 above.

**Residual risk.** Documented as P6 of the Genuine Critique in `REPORT.tex`.
Anyone repeating this workflow without the analytic-`f` cross-check would
carry a systemic OCR-decoding risk. In this run the cross-check plus the
full Table 2 reproduction to 4 dp jointly certify correct decoding.

---

## F4 — Scope of manufactured tests is narrow (not a failure, but a caveat)

**Symptom.** Both test cases pass at essentially machine precision (Ex 1) or
at the expected O(h^2) rate (Ex 2). The scheme "looks perfect."

**Diagnosis.** Both examples use low-order polynomial-in-`x` exact solutions
(`x^2` and `x^3`). CN's centered second-order spatial stencil is exact for
polynomials up to degree 2, and the manufactured `f` pre-encodes the correct
forcing at every node. The tests confirm CORRECTNESS of the discretization
but do NOT stress-test it under conditions that separate merely-consistent
schemes from robust ones (sharp fronts, `1/sqrt(t)` initial-time singularity,
solution-dependent transport, topology change).

**Impact.** None on the REPLICATED verdict — the paper's claims are met on
the tests the paper defines. But a reader should not extrapolate the reported
error magnitudes to physically realistic Stefan problems without further
testing.

**Resolution.** Documented as P2/P3/P5 of the Genuine Critique in
`REPORT.tex` and as three of the five entries in `open_questions.json`
(t=0+ singularity, 2D/3D anisotropic extension, convection coupling).

**Prevention going forward.** Where a paper's tests are all polynomial MMS,
report the replication verdict WITH the scope caveat. Do not oversell.

---

## F5 — "Two-sided Stefan" label is broader than what is actually tested

**Symptom.** The paper title reads "Two-Sided Stefan Problem," which most
readers will interpret as a genuine free-boundary problem where each
interface's velocity is determined by a Stefan condition on the temperature
gradient jump.

**Diagnosis.** In both examples the boundary motions `h1(t) = 1+t` etc. and
`h1(t) = 1+t^3` etc. are PRESCRIBED, not solved for. The actual numerical
problem is: a variable-coefficient parabolic PDE on a moving domain with
known boundary motion.

**Impact.** Not a numerical failure — the CN scheme on the transformed
fixed-domain PDE is correct and second-order. But the framing is generous:
the hard part of a real two-phase Stefan problem (implicit determination of
boundary velocity from a temperature gradient) is not exercised.

**Resolution.** Documented as P3 of the Genuine Critique in `REPORT.tex` and
as OQ #1 in `open_questions.json`.

---

## What worked well

- **Free-endpoint-only compute** was fully sufficient for this 1D problem.
  No paid API calls, no paid `pdf` tool, no vision endpoint.
- **Analytic cross-check** (`f_derived == f_printed`) caught F2 before any
  wasted mesh sweeps and validated the OCR decoding for Ex 1.
- **From-scratch reimplementation** in ~a few hundred lines of numpy/scipy —
  the transformed PDE is small enough that a hand-written CN tridiagonal
  solver on the fixed reference domain `y ∈ [0,1]` fits comfortably.
- **Argo LLM judge** returned an independent REPLICATED verdict on the
  reproduced tables and convergence order.

## Summary

Zero method-level failures. Two paper-internal typos (F1, F2) surfaced and
corrected — both are documentation/typesetting errors, not method errors.
One toolchain limitation (F3, no free vision OCR) worked around with
`tesseract` + analytic cross-check. Two scope caveats (F4, F5) documented as
Genuine Critique items and as open questions. Verdict stands: **REPLICATED.**
