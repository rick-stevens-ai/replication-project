# Failure Analysis: MTW 2002 Darcy-Stokes Replication

Not every step worked on the first try. This is the log of dead ends
and near-misses — kept so the next replication doesn't repeat them.

## 1. Paper acquisition: three failed sources before Wayback

**What was tried:**
1. **SIAM publisher URL** for DOI 10.1137/S0036142901383910 →
   `HTTP 403 Forbidden`.
2. **OSTI mirror** for the same paper → `connection timed out`.
3. **Semantic Scholar → dr.ntu.edu.sg** (Green OA copy) →
   `AWS WAF block` on live fetch.

**Root cause:** publisher paywall + institutional Green-OA mirror
sitting behind an aggressive WAF. Semantic Scholar returns the
metadata correctly but the underlying URL is not always reachable.

**What worked:** Internet Archive Wayback Machine snapshot from
2024-05-03 of the dr.ntu.edu.sg URL → HTTP 200, 270 KB, PDF v1.4,
28 pages, SHA1 `c9eee75…`.

**Lesson:** always cascade at least four acquisition routes before
declaring a paper unreachable: publisher → OSTI → Green OA mirror →
Wayback Machine. Semantic Scholar API key is stored in macOS Keychain
(`security find-generic-password -a rick-stevens-ai -s semantic-scholar-api-key -w`).

## 2. PDF text extraction insufficient for tables

**What was tried:** `pdftotext -layout work/paper_MTW2002.pdf` → 1564
lines of text. Fine for prose, but the paper's multi-column
convergence-rate tables (Tables 3.1, 3.3, 3.5, 3.6, 5.1) came out
mis-aligned when parsed programmatically.

**Root cause:** `pdftotext -layout` preserves visual column alignment
only when column separators are consistent; the paper's SIAM-style
tables use variable spacing.

**What worked:** manual visual re-transcription of every rate value
from the PDF into `report/REPORT.md` §1 and §4. Slower, but zero
risk of a typo passing through as a "reproduced" match.

**Lesson:** for tabular data in FEM papers, don't trust automated PDF
table extraction; hand-transcribe.

## 3. Local V(T) construction: constraint-matrix rank scare

**What was tried:** first pass built the 11-row constraint matrix
`C ∈ ℝ^{11×20}` with the div-in-P₀ constraints written as "sample
`div v` at all 6 P₂-unisolvent points and require each equal to zero."
That is 6 constraints, not 5 — one is linearly redundant, but the
symbolic setup gave `rank(C) = 12` under some quadrature perturbations
and `dim ker C = 8`, one short of the required 9.

**Root cause:** the "constant" constraint should be "`div v(x_i) −
div v(x_0)` = 0 for i = 1..5" (5 independent conditions), not "`div
v(x_i)` = 0" (6 conditions, which force `div v ≡ 0`, over-constraining).

**Fix:** rewrite the div-in-P₀ block as differences from the value at
`x_0`, giving 5 rows. Then `rank(C) = 11` exactly and
`dim ker C = 9`, as required by Lemma 4.1. Verified numerically.

**Lesson:** "div v ∈ P₀" is not "div v = 0"; it is "div v is constant."
Encode as differences, not as absolutes.

## 4. Global sign transform: k=1 first-moment mix under tangent reversal

**What was tried:** initial global assembly assumed the per-edge
sign transform `R_T[e]` was purely diagonal: flip the sign of the two
normal-moment DOFs when `n_local` disagrees with `n_global`, flip the
sign of the tangential DOF when `t_local` disagrees with `t_global`.

**Symptom:** convergence rates in the sweep were noisy at `ε = 2⁻⁴`
and `ε = 2⁻⁸`, with occasional negative rates and non-monotone error
sequences. The divergence error was also 10⁻³ instead of the expected
machine zero.

**Root cause:** the k=1 normal moment `∫_e (v·n) τ dτ` transforms
non-diagonally when the edge parameterization reverses (`s_local =
1 − s_global`). Substituting gives
`local_n1 = 2 s_n global_n0 − s_n global_n1`, i.e. the reversed
first-moment mixes with the (constant) zeroth-moment. The zeroth
moment and the tangent mean are self-consistent under reversal, but
the first moment is not.

**Fix:** derive the 3×3 `R_T[e]` per edge analytically for both
`s_t = +1` and `s_t = −1` cases; unit-test that
`R_T · local_dofs(exact linear v·n) = global_dofs(same v·n)` on a
manually-set-up reversed edge. After fix: divergence errors dropped
to machine zero, and rates snapped to the paper's Table 5.1 values.

**Lesson:** for polynomial-moment DOFs with degree ≥ 1, always
rederive the orientation transform analytically and unit-test it
against a known linear polynomial before running the full sweep.
Sign flips are not enough.

## 5. Divergence error 10⁻³ that turned out to be a boundary-condition bug

**What was tried:** during debugging of item (4), even after fixing
the sign transform, the interior divergence was machine-zero but the
overall `‖div u_h‖_0` sat at ~10⁻³.

**Root cause:** boundary edges were having only the two normal-moment
DOFs set to zero, and the tangent-mean DOF was left free. Since the
paper requires u = 0 on ∂Ω (all three components zero, in the mean),
this was a partial BC.

**Fix:** for every boundary edge, set **all 3 DOFs** (mean-n,
first-moment-n, mean-t) to zero. After this: `max ‖div u_h‖_0 =
6.4e-11` across all 20 solves.

**Lesson:** "u = 0 on ∂Ω" for an H(div) element with per-edge DOFs
means "every DOF on every boundary edge is zero," not "the normal
component is zero."

## 6. Standard-elements sweep: rate at ε = 0 near-zero on the second try

**What was tried:** first scikit-fem run of the P2-P0 sweep at ε = 0
gave rates like +0.30 at all h, not the expected ≈ −0.03 (paper Table
3.1). Investigated whether the mesh convention was wrong.

**Root cause:** the pressure post-processing had subtracted the
*arithmetic* mean of pressure DOFs rather than the mass-weighted mean
over Ω. At ε = 0 the pressure error is dominated by the null-space
mode, so any bias in the mean subtraction leaks directly into the
reported rate.

**Fix:** subtract `∫_Ω p_h dΩ / |Ω|` computed by mass-matrix
integration, not arithmetic mean of DOF values. Rates then matched
the paper to within ±0.10.

**Lesson:** for saddle-point systems with a pressure null space, mean
subtraction must use the L² inner product (weighted by the mass
matrix / element areas), not raw DOF averaging.

## 7. Claims not tested (residual coverage gaps)

Three of the paper's seven claims were **not** replicated here:

- **C5** (Theorem 5.1 error bound): tested only by empirical proxy
  (the rate transition from ~1 to ~2 as ε → 0 is qualitatively
  consistent with `h² + εh`). No direct constant estimation.
- **C6** (Example 6.1 boundary-layer solution): not tested at all.
  This is the more delicate regime; deferred as beyond the sub-agent's
  time budget.
- **C7** (§7 elliptic-system extension): not tested. Deferred as a
  corollary.

**Why deferred, not failed:** the sub-agent's charter was to
replicate the paper's *central novel contribution* (the new nonconforming
element and its ε-uniform convergence in Table 5.1). C6 and C7 are
generalizations. C5 is analytical, and while a direct constant fit is
possible in principle, it requires a family of manufactured solutions
of varying regularity (‖u‖₂ known) — a separate study.

**Not a failure, but a boundary of scope.** Documented so the next
replication can prioritize.

## Summary

Six real dead ends were resolved; three claims (C5 analytical, C6
boundary-layer, C7 elliptic extension) are documented deferrals, not
silent gaps. The rate agreement in Table 5.1 (mean |Δ| = 0.024, all
15 within ±0.07) and the machine-zero divergence error
(6.4×10⁻¹¹) give strong evidence that the surviving pipeline is
correct.
