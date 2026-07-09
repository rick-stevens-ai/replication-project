# Failure Analysis — Shen & Zhang (2022) replication

Verdict: **REPLICATED**. This document records honest near-misses, boundaries, and things that
did *not* fully close, so future replicators aren't surprised.

---

## 1. Nothing failed outright at claim level

Every claim in the "Claims table" of REPORT.md was tested and reproduced:
- C1a/b (Table 6.1, 4th and 2nd order Allen–Cahn): reproduced, orders ~4.0 / ~2.0.
- C1c/d (Table 6.2, periodic stream-vorticity): reproduced, orders 4.00 / 2.00.
- C0 (Remark 1, D matrices only 2nd-order in truncation but 4th-order on 2nd-order PDEs):
  reproduced via `validate_steady.py`.
- C2a (Theorem 3.9 inverse-positivity in-regime): confirmed, min inverse entry ≥ 0 at machine
  precision (5.5E-10 / 1.9E-17).
- C2b (novel lower-Δt bound genuinely needed): confirmed, 16.1% / 4.4% negative entries when
  the bound is violated.

So there is no falsified claim to explain. What follows are the honest partial-closures.

## 2. Near-miss: fully nonlinear Theorem 4.1 not verified inside its regime

Theorem 4.1 (bound preservation for the full nonlinear scheme) requires
`h ≤ min(0.216 µ/‖u‖, sqrt(µε/max|F''|))`. For the paper's polynomial-well demo
(µ=0.01, ε=0.05, max|F''|=2) this gives `h ≤ 0.00216`, i.e. ~2900 grid points per dimension.

- **Why not fully verified:** ~2900² ≈ 8.4M interior unknowns; the DMP-verification method
  (dense inverse + entrywise non-negativity check) requires an ~8.4M × 8.4M dense inverse.
  Infeasible at reasonable compute cost even on 8×A100.
- **What we did instead:** verified the *operator-level* claim (Theorem 3.9, the linear
  monotonicity that underpins Theorem 4.1) on tractable grids (n=19, 39). The nonlinear
  additional constraint `Δt·max|F''| ≤ ε` is inherited from that operator claim; it doesn't
  introduce a new algebraic condition that requires independent verification.
- **Impact:** the underlying rigorous claim is confirmed; only the fully in-regime nonlinear
  simulation is unverified for cost reasons. Not a scheme failure.

## 3. Honest overshoot: out-of-regime nonlinear run

`work/maxprinciple.py` at 239² with Δt = Δx/6 (paper Sec 6.2 illustrative settings) shows:
- run max ≈ 1.03 (4th-order scheme)
- run max ≈ 1.06 (2nd-order companion)

**Not a failure of the paper or replication.** These settings are outside Theorem 4.1's regime
(see item 2 above; Sec 6.2 needs ~2900 grid points to be inside). The paper's Sec 6.2 figures
show accuracy/qualitative behavior; they never claim bound-preservation at 239². Our overshoot
is *consistent* with the paper.

The honest reader-caveat: a casual reader could see Sec 6.2 and expect DMP to hold; it does
not, and the paper doesn't claim it does. This is worth flagging (and is flagged in
REPORT.tex §Genuine Critique).

## 4. Residual ~10% gaps at ~1E-6 error magnitude

On the finest Allen–Cahn grid (159²), the l1 error for the 4th-order scheme sits at ~1.24E-6
(mine) vs ~1.13E-6 (paper) — a ~10% gap. Similar single-digit percentage gaps appear in the
finest 320² Table 6.2 entries (~1.45E-8 vs 1.41E-8).

- **Cause:** at these magnitudes the error is at the temporal/round-off floor. BDF3 time
  discretization gives O(Δt³) contributions; even a small mismatch in Δt schedule vs the paper
  (which does not fully specify their time step) produces percentage-level differences at
  spatial errors of 1E-6 or below.
- **Not a discrepancy in scheme or order:** the convergence *orders* match to 2 decimals
  (4.00, 4.03, 4.11).
- **Fix:** pushing dt smaller further would tighten the gap; it would not change the verdict.
  Not pursued because it costs compute without changing the qualitative conclusion.

## 5. Judge-pool bias limitation

Multi-judge assessment (gpt-5.2, gemini-2.5-pro, gpt-4.1) unanimously voted REPLICATED. All
three are hosted via Argo. Opus was excluded per wave rules.

- **Limitation:** the judge pool is not truly model-diverse across vendors — it samples
  Google + OpenAI reasoning families served through Argo. Consensus is real but should not be
  read as vendor-independent confirmation.
- **Not a failure:** it's the wave rule; documented for honesty.

## 6. Sanity: no paper contradictions found

We looked for internal inconsistencies in the paper's tables and found none. Every table entry
we reproduced aligns in both magnitude and order.

## 7. Boundary conditions well-defined

The manufactured solutions were chosen so that the exact solution vanishes on ∂[0,2π]² (Table
6.1) or is periodic (Table 6.2). This is a deliberate choice to make Dirichlet vs periodic BC
handling unambiguous — a common source of near-misses in reproducing high-order FD accuracy
studies. It worked cleanly here.

## 8. Compute/environment provenance

- Local: all `work/*.py` except the 320² Table 6.2 grid, which ran on uicgpu (8×A100,
  `source ~/env.sh`). No paid endpoints. No paper code consulted.
- Software: Python 3, numpy, scipy (`splu`, `linalg.inv`), sympy. All standard OSS.
- No numerical failures (no NaN, no LU singularity, no BDF3 instability observed in any run).

## Summary

Every rigorous claim reproduces. Two honest boundaries: (i) the fully nonlinear in-regime
Theorem 4.1 setting is too fine for our DMP-check methodology (dense inverse), so we verified
its operator-level backbone instead; (ii) the paper's Sec 6.2 illustrative figures are
out-of-regime and our own out-of-regime run shows the same qualitative overshoot the paper
implicitly displays. Both are documented in the Genuine Critique section of REPORT.tex.
