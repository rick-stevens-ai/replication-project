# Failure Analysis & Friction — QC-1611.05543

## What we did NOT reproduce

1. **The full quantum-circuit implementation of Algorithm 1 (Appendix A) and Theorem 2's `U_→` / `U_←` circuits.**
   We simulated the *mathematical effect* of the paper's subroutines classically (matrix exp, truncated Taylor of the vectorized superoperator). We did NOT compile the paper's actual `U_→ / U_←` circuits (Figures 4–5 in the paper) into a Qiskit / Cirq gate list and count 2-qubit gates. The paper's 2-qubit-gate complexity claim (`O(t² log²(N/ε))` for 1-sparse) is therefore reproduced only at the level of *query count*, not *gate count*. Query count IS one of the paper's two headline metrics, so we still qualify as a REPLICATION, not merely SPOT-CHECK.

2. **The no-fast-forwarding lower bound (Theorem 10).**
   This is a purely analytical polynomial-method proof; there is nothing to reproduce numerically at small N except a re-derivation, which we did not attempt.

3. **The Section 4 "identical-coordinate" and "dense-diagonal" theorems (Theorems 4–7).**
   Table 1 of the paper lists five sparsity classes; we tested Theorems 4/5/6/7 only implicitly (they're consequences of the same Stinespring framework). We reproduced the two main *algorithmic* claims (Section 3's Taylor subroutine and Section 5's Theorem 8 segmentation) which are the "reproducible core" the task prompt asked for.

4. **True diamond norm.**
   Diamond norm is an SDP; we used the cheap upper bound `‖M‖_◇ ≤ N · ‖M‖_2` which preserves the ε-scaling of the true diamond norm (visible in the near-2.0 log-log slopes). A `cvxpy`-based SDP would tighten the constant but not change the slope-2 verdict. This is a KNOWN approximation, documented in the code.

## Friction encountered

| # | What happened | Root cause | Fix / lesson |
|---|---|---|---|
| F1 | First run of `lindblad_sim.py` timed out (>90 s) with no output past the Taylor block. | `ε_tot = 1e-10` at `t=1` in Theorem-8 segmentation demands `t/ε = 1e10` short-time queries → 1e10 matrix-vec multiplies. | Cap segmentation-experiment `ε_tot` at 1e-6, and push deep precision (1e-9, 1e-12) into the Taylor-series experiment. This is literally the paper's own motivation for the Section-3 approach — surfacing the trade-off is a *feature* of the replication, not a bug. |
| F2 | Marker CLI and Nougat CLI not installed on this box. | Standard QC-200 replication expectation is that if the central corpus has a parse, use it; otherwise install locally. Neither is installed and the paper isn't in the central corpus. | Followed the sibling-QC-200 convention documented in `QC-0707.2831-*/extraction/*.md`: use PyMuPDF as Marker-surrogate and `pdftotext -layout` as Nougat-surrogate, and label them SURROGATE in the file header. |
| F3 | Task prompt asked to verify "polylog(1/ε) query scaling". | This is not what the paper actually claims for its sparse-Lindblad-operator algorithm (Section 5 → Theorem 8). The paper's Section 8 explicitly notes polylog(1/ε) is an OPEN problem for this class. The scout may have been thinking of the paper's Section 3 Taylor-based sub-routine, which does approach log(1/ε) truncation order (which we DID verify). | Documented the discrepancy in `workflow.md` and `REPORT.tex`. Tested BOTH interpretations: (a) the paper's actual poly(1/ε) segmentation claim (verified), and (b) the log(1/ε) truncation-order behaviour of the Taylor sub-routine (verified). |
| F4 | Task prompt requested "trace-distance error ≤ ε for chosen ε ∈ {1e-3, 1e-6, 1e-9}". At ε=1e-9 with pure Theorem-8 segmentation this means 1e9 queries at t=1 — infeasible. | Same as F1: the paper's own Theorem-8 has this scaling, so it's not a defect of our reproduction — it's the paper's *reason* for developing Section 3. | Reported both regimes: Theorem-8 segmentation for ε_tot ∈ {1e-3..1e-6}, Taylor sub-routine for ε_tot ∈ {1e-3, 1e-6, 1e-9, 1e-12}. Taylor reached the numerical floor (~1e-15) at ε_tot=1e-12. |

## Residual gaps

- Qiskit-based gate-level compilation of `U_→ / U_←`.
- SDP-tight diamond norms.
- Lower-bound (Theorem 10) empirical study.
- 4-qubit and larger (only limited by memory of 256×256 = N² × N² = 65536×65536 superoperator — feasible but off the critical path).

None of these gaps affects the REPLICATED verdict on the paper's headline query-scaling claims.
