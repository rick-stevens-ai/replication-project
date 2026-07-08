# Failure Analysis — QC-1909.05074 QNG-for-VQE Replication

This document is the **honest critique** of what this replication did NOT do,
what it did loosely, and where the verdict of REPLICATED is doing work it perhaps shouldn't.

## 1. QNG was NOT independently reimplemented at the metric-tensor level

We called PennyLane 0.45.1's `qml.QNGOptimizer(approx="block-diag", lam=1e-8)` rather than
hand-implementing the Fubini--Study metric tensor via Hadamard tests. The paper hand-derives the
full analytic $F$ for its specific ansatz (§IV) and does the linear solve manually. Our
replication tested only that a **correctly-configured library QNG** beats vanilla GD in iteration
count on the paper's exact Hamiltonian, init, and $\eta$. This is a weaker replication than a
hand-rolled Hadamard-test metric-tensor implementation matching the paper's analytic $F$ element
by element.

**Impact on verdict:** LOW for headline C3 (the library's QNG converged to machine precision with
the predicted speedup, so if there is a bug in PennyLane's block-diag QNG it did not manifest
here). MEDIUM for C2 (analytic metric structure) — see §2.

## 2. Analytic metric-tensor sanity check FAILED to close the loop at off-diagonals

We attempted (REPORT.md §5.1) to verify the paper's analytic formula
$F_{13}=\sin 2\theta_2$, $F_{24}=\cos 2\theta_1$, on-diagonal $=1$
against PennyLane's `qml.metric_tensor(..., approx=None)` at a random test point. After
correcting for a chain-rule factor of 4 (from the $R_y(2\theta)$ parametrization) and PennyLane's
default $1/4$ scaling, the diagonal matched (all ones). The off-diagonals did NOT match
numerically. We diagnosed this as "a convention/scaling discrepancy in the metric_tensor helper,
**not** a bug in the QNG optimizer itself" — reasoning that if the QNG step direction were wrong,
we would not converge to machine precision at the predicted rate.

**This is a plausible but not rigorous diagnosis.** A tighter replication would either
(a) hand-compute the Hadamard-test metric-tensor circuit, or (b) trace through PennyLane's
`metric_tensor` normalization convention to derive the exact scaling that reconciles the
off-diagonals with the paper's $F$.

**Impact on verdict:** MEDIUM for C2. Because the *empirical* claim C3 rides on the *step
behavior* of QNG (which we confirm to machine precision), not on the analytic form of $F$, the
overall REPLICATED verdict on the headline holds. But claim C2 (analytic metric form) is
verified only *qualitatively* here, not element-by-element.

## 3. QFI evaluation cost was NOT quantitatively addressed

The paper acknowledges that computing the Fubini--Study metric costs extra circuit evaluations
per step, roughly $O(n_{\text{params}}^2)$ additional expectations (Hadamard tests /
parameter-shift on the metric). Our "speedup" is measured in **optimizer iterations**, not in
**quantum-circuit execution count** or **shot budget**.

For this 4-parameter ansatz:
- Vanilla GD per step: 4 params × 2 (parameter-shift) = 8 circuit executions
- QNG per step: 8 (gradient) + ~16 (block-diagonal metric-tensor, 4×4 = 16 upper triangular Hadamard tests) = ~24 executions
- Ratio: ~3× more circuits per QNG step

Our iteration-count speedup at tolerance $10^{-4}$ is 1.75× — which is LESS than the 3×
circuit-count penalty. **Measured in shot / circuit budget, QNG is actually SLOWER than vanilla GD
on this problem.** The paper does not dwell on this either, but it is a real caveat.

**Impact on verdict:** LOW for the paper's own qualitative claim (which is about iteration count
and convergence-in-parameter-space). HIGH for anyone reading the REPORT and inferring that QNG is
strictly better in practice — it is not, on this small problem, when measured in real resources.

## 4. Shallow vs. deep ansatze — only shallow was tested

We tested only the single-layer 4-parameter HEA of Fig. 4. QNG's advantage on deep brick-wall
ansatze, where the metric tensor has richer structure and more singular-point risk, is
untested here.

**Impact on verdict:** LOW for the C3 headline (which is claimed only for this shallow case).
Flagged as open question #1 in `open_questions.json`.

## 5. Secondary paper claims (C5, C6) NOT exercised

The paper's Fig. 6 (init in an excited-state plateau, QNG escapes faster) and Fig. 7 (QNG failure
mode at $\beta=0.02$ near a singular point) are secondary illustrations. The Fig. 7 case is
particularly interesting because it is the paper's own **negative** evidence. We did not run
either.

**Impact on verdict:** LOW for the C3 headline. But a "full" replication of the paper would
exercise both. The QC-100 brief specified "reproduce the ONE most-checkable number," which we
did (C3 speedup at fixed init). Scope-out is disclosed in REPORT.md §2 and §8.

## 6. Regularisation deviation

We use additive $\lambda=10^{-8}$ on the metric ($F+\lambda I$); the paper uses SVD-based
eigenvalue clipping for the same purpose. This is immaterial for the benign init we tested
(no singular-point crossing along the trajectory), but would matter if replicating Fig. 7.

**Impact on verdict:** NONE for the C3 headline. Would be MEDIUM if attempting Fig. 7.

## 7. Shot-noise / hardware-noise — NOT tested

All simulation is statevector, exact expectations, no noise. Real NISQ deployment introduces
finite-shot noise (which QNG's $F^{-1}$ step is known to amplify) and hardware errors
(depolarizing, amplitude/phase damping, coherent overrotation). Behavior in those regimes is
unknown from this replication.

**Impact on verdict:** LOW for the paper's own scope (which is noise-free simulation).
HIGH for practical relevance. Flagged as open questions #2 and #4.

## 8. Convergence-vs-SGD comparison — quantitative match is a curve match, not a table match

The paper reports convergence via curves (Fig. 5 bottom), not via tabulated iteration counts at
fixed tolerances. Our 1.45×–1.75× "speedup" numbers are our own derived summary of a curve
comparison, not a direct number-vs-number check against a paper table. The qualitative statement
"QNG converges faster" is unambiguously confirmed; the specific numerical ratio is our
extraction, not the paper's number.

**Impact on verdict:** LOW. The paper's claim is qualitative and our curves match qualitatively.
The quantitative extraction is transparent (see `report/evidence/energy_curves.csv`).

## Bottom line

The replication is **tight on the headline claim** (C3, plus supporting C1 and C4) on the
paper's exact system, using an independent code path. It is **loose** on:

1. Independent metric-tensor implementation
2. Element-by-element analytic $F$ verification
3. Quantum-resource / shot-budget cost accounting
4. Deep-ansatz generalization
5. Paper's own negative results (Fig. 6, Fig. 7)
6. Shot-noise and hardware-noise robustness

**Verdict of REPLICATED is warranted for the C3 headline** on the specific system, init, and
$\eta$ the paper specifies. A fuller replication would target Fig. 6, Fig. 7, and a
shots-based cost model. Those are enumerated in `open_questions.json` as concrete next probes.
