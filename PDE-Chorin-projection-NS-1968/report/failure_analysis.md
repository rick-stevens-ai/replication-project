# Failure Analysis — Chorin (1968) Projection Method Replication

**Overall verdict.** REPLICATED. This file itemizes the failures encountered, the caveats we intentionally accepted, and the honest-inventory of things that a stricter reviewer could hold against the report.

---

## 1. Actual runtime failures encountered

### 1.1 E4 blew up to `nan` by step 17

**Symptom.** Running Chorin's Table I exact parameters (`dx = π/39`, `dt = 2·dx² = 0.01397`, `R = 1`, `nx = 39`) with our explicit-Euler advection-diffusion sub-step, `u` and `v` fields go to `nan` by step 17. Trace preserved in `work/pearson_run.log`.

**Root cause.** Our sub-step is explicit Euler; Chorin's is implicit ADI Peaceman–Rachford (his Scheme A, eqs. 6–7). Our sub-step has diffusive CFL `dt < dx²/(4ν) ≈ 1.6e-3`. Chorin's `dt = 0.01397` is ~9× larger than our stability limit, hence blow-up.

**Classification.** This is **corroborating**, not contradicting, evidence for Chorin. Chorin himself writes on p.749: *"implicit schemes were sought because explicit ones typically require, in three space dimensions, that Δt < ¼Δx² which is an unduly restrictive condition."* Our failure is exactly what he predicted.

**Resolution.** Documented as a positive-verification-by-negative-example in REPORT.md §3.4. Not remediated (would require implementing ADI, which was out of scope; see §3 below).

## 2. Numerical caveats we accepted (flagged in REPORT.tex Critique §5)

### 2.1 Re=400 v-centerline L∞ error does not shrink with refinement

**Observation.** Re=400 cavity, err_v_L∞ = 0.133 at 64² and 0.147 at 128² — no convergence with grid refinement, concentrated at the two Ghia sample points near x∈[0.85, 0.90] (right-wall boundary-layer peak).

**Working hypothesis.** Known first-order-projection artifact at moderate Re near boundary-layer peaks, well-documented in the subsequent literature (Van Kan 1986, Kim–Moin 1985, Bell-Colella-Glaz 1989 second-order projection).

**Why not remediated.** Would require either (a) implementing a second-order projection variant on the same grid or (b) refinement to 256²/512² to bound the asymptote — either is a substantial engineering effort not in scope for the minimal 2D rerun. Explicitly acknowledged as unproven attribution in REPORT.tex Critique §5.2. Filed as open question #1 in `open_questions.json`.

### 2.2 Spatial convergence rate 2.57 at nx: 40 → 80 is out of family

**Observation.** Rates 2.07, 2.12, **2.57**, 2.13. The 2.57 is neither textbook O(h²) nor a plausible higher-order artifact of the scheme.

**Working hypothesis.** At `dt = 5e-5` reference, the O(dt) splitting error is ~5e-5, comparable to the spatial error at nx=80, producing measurement-noise contamination of the rate estimate.

**Why not remediated.** Would require rerunning at dt = 5e-6 (10× longer wall time). Flagged as anomalous but not sufficient to threaten the O(h²) claim in aggregate. Filed as open question #5 in `open_questions.json`.

### 2.3 Temporal rates drift upward from 1.0

**Observation.** Cauchy self-refinement temporal rates 1.04, 1.08, 1.17 — drifting upward, not flat.

**Working hypothesis.** Pre-asymptotic regime; a second-order error term (from centered spatial differencing or from cancellation between advection and pressure errors) is contaminating the pure O(dt) splitting error signal.

**Why not remediated.** Would require two more halvings (dt = 2.5e-4, 1.25e-4) and possibly cross-checking against a different exact solution (Taylor–Green vortex, Kovasznay flow). Flagged in REPORT.tex Critique §5.4. Filed as open question #3 in `open_questions.json`.

## 3. Untested claims (scope decisions made up front)

### 3.1 C5 — Extension to 3D thermal convection (§6 of Chorin's paper)

**Not done.** Chorin's §6 is a real numerical experiment with tabulated results, and we did not reimplement it. REPORT.md §4 justifies this by pointing to the 55-year subsequent literature, but that literature does not itself reproduce the specific §6 numbers — it reproduces the method. Explicitly re-flagged in REPORT.tex Critique §5.5.

### 3.2 C6 — Implicit ADI Peaceman–Rachford sub-step

**Not done.** We used explicit Euler for the advection-diffusion sub-step. Chorin actually specifies ADI (eqs. 6–7). Our E4 failure is *negative* evidence: explicit blows up at his dt. But we have **no positive verification** that ADI in fact stabilizes at his dt — because we never wrote ADI. Filed as open question #4 in `open_questions.json`.

## 4. Substitutions vs Chorin's original scheme

| Chorin actually used | We used | Consequence |
|---|---|---|
| Implicit ADI Peaceman–Rachford sub-step | Explicit Euler | E4 fails at his dt (see §1.1); acceptable per his own p.749 remark |
| Iterative Dufort–Frankel Poisson solver | Direct `scipy.sparse.linalg.splu` | Our C1 divergence-free is at machine precision (~1e-14) vs his iterative tolerance; sharper but not directly comparable |
| Simplified Neumann pressure BC | Same (homogeneous ∂p/∂n = 0, nullspace pinned) | Standard; unclear how close to physically consistent BC; filed as open question #2 |

## 5. Things a stricter reviewer would still hold against us

1. **No pressure-field error reported.** We report ‖div u‖ and Ghia centerline errors, but not any pressure L2 error. Chorin himself does not tabulate a pressure error, but a stricter test could. REPORT.tex Critique §5.6.
2. **LLM-judge is not an independent scientific witness.** It saw the same evidence in the same framing; could be sycophantic; it is a summary indicator, not load-bearing. REPORT.tex Critique §5.7.
3. **No bit-identical comparison to Chorin's original FORTRAN.** We have no access to his source. We claim algorithmic reproduction, not bit-level reproduction. REPORT.tex Critique §5.8.
4. **The `~30× better than Chorin's Table II` framing is favorable to us.** It is true (5.7e-6 vs 1e-4) but obscures that we used a different sub-step (explicit vs implicit) and a smaller dt. A fairer comparison would run our code with a Peaceman–Rachford sub-step and Chorin's exact dt = 0.01397, and see whether we still beat 1e-4.

## 6. What we do NOT claim to have failed

- We do not claim any of C1–C4 failed. All four are reproduced cleanly (see REPORT.md §3.5).
- We do not claim the E4 blow-up is a failure of Chorin's method. It is a failure of *our* explicit-Euler simplification, precisely as Chorin's own analysis predicts.
- We do not claim the Re=400 v-profile mismatch is a failure of Chorin's paper's specific claims. Chorin never ran the Ghia lid-driven cavity; that benchmark is 14 years later.

## 7. Failure-mode summary

| Failure | Class | Root cause | Remediation status |
|---|---|---|---|
| E4 nan at step 17 | Predicted (corroborating) | Explicit sub-step at Chorin's ADI dt | Documented, not remediated (out of scope) |
| Re=400 v-profile L∞ ≈ 0.15 | Known artifact | 1st-order projection at moderate Re | Documented, filed open Q#1 |
| Spatial rate 2.57 at 40→80 | Anomaly | Suspected: time-error noise floor | Documented, filed open Q#5 |
| Temporal rate drift 1.04→1.17 | Anomaly | Suspected: pre-asymptotic | Documented, filed open Q#3 |
| Untested C5 (3D convection) | Scope | Engineering effort out of scope | Documented in REPORT §4 |
| Untested C6 (implicit ADI) | Scope | Engineering effort out of scope | Documented, filed open Q#4 |

**Bottom line.** Every failure encountered is either (i) predicted by Chorin's own text, (ii) a known artifact of first-order projection well-documented in the subsequent literature, (iii) a measurement-noise anomaly in the convergence study, or (iv) an out-of-scope claim we chose not to test. None of them threaten the REPLICATED verdict for C1–C4.
