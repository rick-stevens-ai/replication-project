# Failure Analysis — Gottlieb & Shu (1998) TVD/SSP-RK Replication

**Verdict:** REPLICATED. No showstopper failures during the run.

This file records the **near-misses**, **blind alleys we could have gone
down**, and **honest limits of what our tests do and do not close**. The
purpose is diagnostic: if a future replicator re-runs this or extends it
to the 4-stage case / WENO coupling / implicit-SSP, these are the
tripwires to remember.

---

## 1. What did NOT fail (for the record)

- **C1 order test.** Observed orders 2.005 / 3.005 hit the paper's formal
  2 / 3 to well within noise across seven grid refinements. No convergence
  degradation, no super-convergence artifacts, no roundoff floor visible at
  `N = 512` (finest error still 2.34e-07 for RK2, 1.14e-10 for RK3).
- **C2 TVD tests.** Both directions of the paper's prediction held on the
  first attempt: exact TVD (`0.00e+00`) at CFL = 1 for SSP-RK2/3, blow-up
  past the bound (`3.26e+02` for RK2, `5.51e-02` for RK3 at CFL = 1.05),
  catastrophic failure (`1.23e+06`) for the negative-β counter-example even
  at CFL = 0.5.
- **C3 empirical `c*`.** Binary search converged in 40 bisections to
  `0.99997` for both schemes, matching the paper's `c* = 1` to within the
  search resolution (`gap ≈ 8.85e-05`).
- **LLM-judge.** Argo `argo:gpt-4o` returned a clean structured JSON verdict
  on the first call, no parse failures, no reasoning drift, agreeing with
  the numeric summary claim by claim.

---

## 2. Blind alley avoided: SSP-RK2 order study on imaginary eigenvalues

The most-tempting-and-wrong first move on an SSP-RK order study is to use
`u' = i·ω·u` (or its equivalent, an oscillatory ODE) as the scalar test.
It is the "linear-advection dispersion" toy, so it feels natural.

**Why it would fail.** SSP-RK2's absolute-stability boundary passes
through the imaginary axis at `|z| = √2` but is *tangent*, not
interior-containing. For any `Δt` with `|ω·Δt| ≠ 0`, `|R(z)| = 1` to
leading order in `Δt`, so the error is dominated not by consistency but
by the boundary of the stability region. The observed order collapses
toward 1 (not 2) as `Δt → 0`, giving a false-negative on order.

**What we did instead.** Followed the standard Gottlieb–Shu order test:
scalar ODE `u' = -u`, `u(0) = 1`, exact `exp(-1)`. Real negative
eigenvalue, safely inside the stability region for every `Δt ≤ 1`, so the
error is purely consistency-driven and the log₂ rates converge cleanly to
the formal order. This choice is documented in the report method §3.4.

**Lesson.** Order-of-accuracy tests are only meaningful **inside** the
scheme's absolute-stability region and away from its boundary. If you
find yourself claiming SSP-RK2 is "empirically 1st order," check whether
you accidentally put the eigenvalue on the stability boundary.

---

## 3. Near-miss: TV bookkeeping on periodic domains

Total variation of `u[0..N-1]` on a **periodic** domain is
`sum(|u[i+1] - u[i]|) + |u[0] - u[N-1]|` — the wrap-around term matters.
The natural NumPy one-liner `numpy.sum(numpy.abs(numpy.diff(u)))` **omits**
the wrap term and halves `TV_0` on the symmetric step IC (2.0 → 1.0),
which then rescales every fractional TV metric by a factor of 2.

We caught this via a spot check: the analytic `TV_0` for `u = 1` on
`(0.3, 0.7)` and 0 elsewhere is exactly 2 (up and down). Confirmed
`TV_0 = 2.0000` in `results.json` before trusting the C2 table.

**Lesson.** Any TVD study on a periodic domain must include the wrap-
around term explicitly. Bake it into the TV helper, not into the driver.

---

## 4. Near-miss: sign convention on 1st-order upwind

For linear advection `u_t + a·u_x = 0` with `a > 0`, first-order upwind
takes the `i-1` neighbor: `(du/dt)_i = -(a/Δx)·(u_i - u_{i-1})`. Flip the
sign of `a` (or of the flux difference) and the scheme is *downwind*,
i.e. unconditionally unstable and certainly not forward-Euler-TVD. That
would break the *baseline* on which SSP-RK inherits its TVD property,
producing "SSP-RK3 is not TVD at CFL = 1" false-negatives.

We verified sign convention by observing exact TVD (`0.00e+00`) at
CFL = 1, which is only possible when the spatial op is truly forward-
Euler-TVD.

**Lesson.** Whenever an SSP-RK test says "it's not TVD," first check the
spatial op is forward-Euler-TVD in isolation. Bug is almost always there,
not in the time integrator.

---

## 5. Honest limits of our tests (things that DID stay open)

These are not failures — they are boundaries of what "REPLICATED" here
means. Full detail in `REPORT.tex` §7 Genuine Critique and in
`open_questions.json`.

1. **4-stage results not tested.** The paper's non-existence theorem for
   an all-positive-β 4-stage order-4 SSP-RK, and its higher-stage
   optimal-coefficient constructions, are outside our minimum scope. If a
   future replication wants to close this, the entry point is paper eq.
   (4.3)-style candidates with negative-β pairs and matching downwind
   `L~(u)` operators.

2. **`c* = 1` demonstrated, not proven optimal.** The C3 binary search
   establishes `c ≥ 0.99997` preserves TVD on step-IC + first-order
   upwind + `N = 400`. Optimality is a separate order-barrier argument in
   the paper. An adversarial IC or a different limiter could in principle
   expose a smaller usable CFL. Open question 1 in `open_questions.json`.

3. **CFL-transition curve past `c*` not characterized.** We tested one
   point (`CFL = 1.05`) and observed a 4-order-of-magnitude asymmetry
   between SSP-RK2 (`3.3e+02`) and SSP-RK3 (`5.5e-02`) failure
   magnitudes. Whether that follows a predictable power law in
   `(CFL - c*)` is a full sweep away. Open question 2.

4. **Spatial op fixed at first-order upwind.** WENO-5 / limited MUSCL /
   Burgers with sonic point / Euler shocks were not tested. The SSP
   guarantee only transfers if the spatial op is forward-Euler-TVD, and
   WENO is technically only essentially non-oscillatory. Open question 5.

5. **No cross-implementation check.** Single NumPy implementation. A
   second, independently written implementation (Julia, C) would harden
   the numbers against subtle same-bug-same-answer situations.

6. **Not pinned in a lock file.** Deterministic on any modern NumPy 2.x +
   IEEE-754, but a future NumPy that changes accumulation order could
   shift the last digit of the reported errors. The verdict would not
   change; the exact numbers might.

---

## 6. LLM-judge failure modes we watched for (and did not observe)

- **Judge reasons past the numbers.** Would appear as an "overall
  reproduced" verdict on a claim where our numeric summary shows a miss.
  Did not happen — every per-claim verdict field matched the numeric
  evidence.
- **Judge parses JSON wrong.** Would appear as missing fields or as prose
  instead of a JSON block. Did not happen — Argo returned a clean JSON
  body verbatim, stored in `judge.json`.
- **Judge assumes we tested things we did not.** We deliberately sent
  only the C1/C2/C3 summary; the judge's verdict is over C1/C2/C3 only,
  matching the report's scope statement.

---

## 7. Recovery playbook (if you re-run and something breaks)

| Symptom | Most likely cause | Fix |
|---|---|---|
| SSP-RK2 order ≈ 1 in C1 | Test ODE has imaginary eigenvalue | Use `u' = -u`, not `u' = i·ω·u` |
| `TV_0 = 1.0` on symmetric step IC | Missing wrap-around term in TV | Add `|u[0] - u[-1]|` to `sum(|np.diff(u)|)` |
| SSP-RK3 not TVD at CFL = 1 | Sign flip in upwind flux | Verify baseline: forward-Euler alone should be TVD at CFL ≤ 1 |
| Binary search `c* ≈ 0.5` | Tolerance loose or wrong integrator wired in | Tolerance `1e-10` on `(TV_max - TV_0)/TV_0`, verify scheme identity |
| Judge returns free-form prose | Temperature > 0 or prompt lost the JSON demand | Set `T = 0`, restate "respond with a JSON object with keys ..." |
