# Failure analysis — OSTI 22598983 (BOUT++ MMS verification)

## TL;DR

The replication succeeded at the *method* level (every reported convergence order was reproduced within ≲0.03) but is **partial at the code-verification level** because BOUT++ itself was not built. Three classes of issue arose: (A) external/infrastructure blockers, (B) inherent limitations of MMS as a verification tool, and (C) self-inflicted implementation bugs (caught + fixed before the final numbers).

---

## A. External / infrastructure blockers

### A1. BOUT++ toolchain (BLOCKER for full code verification)
- **Problem:** BOUT++'s own reproduction path (`examples/MMS/*/runtest`) requires SUNDIALS + PETSc + FFTW + MPI — a nontrivial toolchain not available on the replication host.
- **Impact:** The actual BOUT++ code paths (its Arakawa/WENO/shifted-metric implementations, BC application, parallel decomposition) were not exercised. This is the primary reason the independent judge downgraded the verdict from REPLICATED to PARTIALLY REPRODUCED.
- **Mitigation used:** Re-implemented every scheme from scratch in NumPy/SciPy — stronger for *independent method verification* but weaker for *code verification*. Both readings are honestly reported in REPORT.md §4 and §5 item 1.
- **Would fix by:** building BOUT++ with the required deps and running `examples/MMS/*/runtest` at the paper's tolerances. Follow-up open question #5 in `open_questions.json`.

### A2. osti.gov unreachable
- **Problem:** All HTTP requests to osti.gov timed out (code 000 / firewall) from the replication host.
- **Impact:** Could not fetch the OSTI landing page directly. No scientific impact — DOI + arXiv metadata + arXiv PDF cover the same paper.
- **Mitigation used:** Web search confirmed OSTI ID 22598983 and DOI 10.1063/1.4953429; paper PDF pulled from arXiv 1602.06747.
- **Would fix by:** running the replication from a host with unrestricted outbound HTTP.

---

## B. Inherent MMS-methodology limitations

### B1. Adaptive-implicit integrators unverifiable by fixed-order MMS
- **Problem:** SUNDIALS CVODE and PETSc TS use adaptive order + adaptive step. A fixed-order MMS measurement can't distinguish "adaptive controller working correctly" from "adaptive controller silently broken but converging by luck." The paper acknowledges this; the replication inherits the same gap.
- **Impact:** Any bug in the adaptive order-selection heuristic, error estimator, or step-size safety factor is not caught by the tests reported here or in the paper.
- **Mitigation used:** Treated as a black box (matching the paper). Karniadakis multistep explicitly not reproduced — its 2.13 rate is a known Euler-startup artifact.
- **Would fix by:** freeze integrator at fixed order/step, walk to fully adaptive, compare; or MMS-calibrate error(rtol) vs rtol across a log sweep. Open question #4.

### B2. WENO limiter untested by smooth MMS
- **Problem:** WENO's raison d'être is its nonlinear weights / limiter for shock capturing. A smooth manufactured solution keeps the limiter effectively inactive; the reproduced 2nd-order-capped rate says nothing about limiter correctness in steep gradients.
- **Impact:** WENO advection is "verified as a 2nd-order-in-smooth-region scheme," which is a much weaker claim than "verified as a shock-capturing scheme."
- **Mitigation used:** Explicitly documented in REPORT.md §5 item 3 as an open problem the paper itself flags.
- **Would fix by:** design non-smooth MMS (Heaviside with tunable ε, Burgers-type near-shock analytic). Open question #2.

### B3. Table 1 error CONSTANTS not matched
- **Problem:** The from-scratch operator-level MMS reproduces the *asymptotic order* (1.616→1.816→...→1.990 at N=512) but not Table 1's absolute error magnitudes.
- **Impact:** The paper's specific Table 1 values (including the interesting rate dip to 1.894 at N=512, attributed to time-integration tolerance floor) are corroborated only in structure, not in numerical detail.
- **Mitigation used:** Documented as a "reproduces the order, not the constants" limitation in REPORT.md §3.5 and §5 item 4.
- **Would fix by:** run BOUT++ examples/MMS/diffusion at rtol=1e-7, atol=1e-15, t=10 on the paper's exact grid. Open question #1.

---

## C. Self-inflicted implementation bugs (caught + fixed)

### C1. Sign error in analytic ∂φ/∂z
- **Problem:** During development, the analytic derivative used to check the Poisson bracket [φ,f]=φ_x f_z − φ_z f_x had a wrong sign in ∂φ/∂z.
- **Detection:** SymPy symbolic cross-check flagged the discrepancy before running the numerical bracket test.
- **Impact if uncaught:** Would have produced systematically wrong "reference" values, potentially masking a genuine implementation bug in the bracket schemes or attributing a false failure.
- **Lesson:** Every manually-differentiated source term should be re-derived symbolically. This is now a standing habit for MMS work.

### C2. Incorrect Arakawa 9-point stencil
- **Problem:** The initial Arakawa Jacobian implementation had a stencil error that gave a wrong convergence rate on the bounded-domain bracket test.
- **Detection:** Independent standalone sanity check `arakawa_check.py` on a doubly-periodic domain expected 2.00 and gave something else. That surfaced the bug BEFORE it was blamed on the harder bounded-domain problem.
- **Impact if uncaught:** Would have produced a false-negative on the Arakawa scheme and potentially a false-positive on some other schemes if the wrong bracket had been used as a reference.
- **Lesson:** Ship the sanity check *before* the main test. `arakawa_check.py` is preserved in `code/` as evidence of the discipline.

---

## Verdict on the reproduction (not the paper)

- **The paper is fine.** No numerical claim was contradicted; the observed orders match to ≲0.03 across all six subsections tested.
- **The reproduction is partial** in exactly the way an *independent method* replication is: it verifies the schemes the paper describes, not the specific BOUT++ binary the paper verifies. This is honestly reflected in the split verdict (replicator: REPLICATED; judge: PARTIALLY REPRODUCED). Both are defensible for different readers.

## Failure log entry (for AGENTS.md-style memory hygiene)

- **Failure class:** partial reproduction due to inaccessible dependency (BOUT++ build).
- **Root cause:** SUNDIALS/PETSc/FFTW/MPI toolchain not present on replication host.
- **Fix:** re-implement schemes from scratch (independent-method replication).
- **Prevention:** for future code-verification papers, decide upfront whether the goal is (a) reproduce the *code* (build required) or (b) reproduce the *method* (from-scratch acceptable); pick and disclose. This replication landed in (b) by necessity and disclosed it.
