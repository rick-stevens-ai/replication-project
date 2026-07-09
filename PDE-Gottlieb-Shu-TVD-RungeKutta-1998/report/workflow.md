# Workflow — Gottlieb & Shu (1998) TVD/SSP-RK Replication

**Paper:** Gottlieb & Shu, *Total variation diminishing Runge-Kutta schemes*,
*Math. Comp.* 67(221):73–85, 1998. DOI 10.1090/S0025-5718-98-00913-2.
**Executor:** subagent (`argo/argo:claude-opus-4.7`), local CPU (macOS,
Python 3.14.6 / NumPy 2.4.3).
**Judge:** Argo `argo:gpt-4o` (FREE proxy, 127.0.0.1:44497, temperature 0).
**Date:** 2026-07-04.
**Verdict:** REPLICATED.

---

## 0. Rationale for workflow shape

This is a **numerical-analysis paper**, not an empirical / data-driven paper.
There is no dataset to download, no code artifact to run — the "artifacts" of
the paper *are* equations (4.1) and (4.2), the SSP-RK2 and SSP-RK3
integrators in Shu–Osher form. Replicating the paper therefore means:

1. Implement eqs. (4.1) and (4.2) from scratch.
2. Recover the paper's three headline claims (order 2/3; TVD at CFL ≤ 1
   with directional failure past that bound and for a `-β` counter-example;
   optimal SSP coefficient `c* = 1`) on the same class of scalar test
   problems the paper uses.
3. Have a second pair of eyes (LLM-judge) confirm the numeric summary
   matches theory.

Zero downloads, zero data dependencies, deterministic runs.

---

## 1. Setup

```bash
mkdir -p ~/Dropbox/REPLICATE-PROJECT/PDE-Gottlieb-Shu-TVD-RungeKutta-1998/{report/evidence,work}
cd       ~/Dropbox/REPLICATE-PROJECT/PDE-Gottlieb-Shu-TVD-RungeKutta-1998
# Environment: Python 3.14.6, NumPy 2.4.3 already present on host.
# No pip installs, no lock file - single-file NumPy implementation.
```

Env pinned only informally (host CherryRd, Python 3.14.6, NumPy 2.4.3). No
`requirements.txt` written; a future NumPy that changes accumulation order
could shift the last digit of the reported errors but not the verdict.

---

## 2. Implement — `work/ssp_rk_replication.py`

Three functional pieces, all in one script:

- **`rk_ssp2(u, dt, L)`** — SSP-RK2 Shu–Osher form (paper eq. 4.1):
  ```
  u1  = u + dt * L(u)
  return 0.5*u + 0.5*(u1 + dt*L(u1))
  ```
- **`rk_ssp3(u, dt, L)`** — SSP-RK3 Shu–Osher form (paper eq. 4.2):
  ```
  u1  = u + dt * L(u)
  u2  = 0.75*u + 0.25*(u1 + dt*L(u1))
  return (1/3)*u + (2/3)*(u2 + dt*L(u2))
  ```
- **`rk_neg_beta(u, dt, L)`** — a 2-stage 2nd-order RK constructed with a
  negative β (i.e. a downwind Euler sub-step), used as the paper's own
  counter-example: 2nd-order accurate on smooth problems but *not* SSP,
  so TVD fails even at small CFL.

Plus three drivers:
- `experiment_C1_order()` — scalar ODE `u' = -u` at
  `N ∈ {8, 16, 32, 64, 128, 256, 512}`; error vs. `exp(-1)`; `log2` rates.
- `experiment_C2_TVD()`  — periodic 1D linear advection + first-order upwind
  spatial op + step IC (`u=1` on `(0.3, 0.7)`, else 0); five (scheme, CFL)
  cases; report `(TV_max - TV_0)/TV_0`.
- `experiment_C3_ssp_cfl()` — binary search on
  `CFL ∈ [0.05, 1.5]`, 40 bisections, tolerance `1e-10` on fractional TV
  increase.

All experiments deterministic (fixed grid, fixed IC, no RNG).

---

## 3. Run — three experiments in one shot

```bash
python3 work/ssp_rk_replication.py
# writes:  report/evidence/results.json
```

Runtime: seconds on a CPU (all problems are 1D, `N ≤ 400`, `t_final ≤ 1`).

---

## 4. LLM-judge — `work/judge.py`

Sends a compact numeric summary (per-claim reproduced-or-not table with
observed vs. expected numbers) to Argo `argo:gpt-4o` at the local FREE
proxy (`127.0.0.1:44497`, `Authorization: Bearer stevens`, temperature 0),
and stores the parsed JSON verdict.

```bash
python3 work/judge.py
# writes:  report/evidence/judge.json
```

Judge is a courtesy sanity check, not evidence — it sees only our numeric
summary, not the source code. See critique §7 (item 6).

---

## 5. Write the report

- `report/REPORT.md`  — Markdown report (this replication's canonical
  narrative).
- `report/REPORT.tex` — LaTeX mirror with a dedicated Genuine Critique
  section (self-adversarial critique of *our* tests, not of the paper).
- `report/open_questions.json` — five genuinely open follow-up questions
  grounded in the SSP-RK / hyperbolic-conservation-law literature.
- `report/workflow.md` — this file.
- `report/artifacts_summary.md` — one-page manifest of what was produced.
- `report/failure_analysis.md` — narrative of blind alleys and dead-ends
  encountered en route (see the "attempt log" reference in REPORT.md
  method §3.4 for one such: the SSP-RK2 order test on purely-imaginary
  eigenvalues, which is why we chose `u' = -u` instead of `u' = i·u`).

---

## 6. What could go wrong (and did not, here)

- **Wrong test problem for order.** SSP-RK2 has purely-imaginary stability
  boundary at `|z| = √2`; an order study on `u' = iω u` degrades to
  apparent order 1 from stability, not consistency. Fix used: real
  eigenvalue `u' = -u`. (Recorded in REPORT.md §3.4.)
- **Off-by-one in TV.** `numpy.abs(np.diff(u))` on a periodic domain must
  include the wrap term, else `TV_0 = 2.0` becomes `1.0` and every result
  is scaled wrong. Verified `TV_0 = 2.0000` in results.json.
- **CFL sign conventions.** Advection speed `a > 0` with 1st-order upwind
  uses the `i-1` neighbor; sign flip inverts stability. Verified by
  checking exact TVD (`0.00e+00`) at CFL = 1.
- **Binary-search tolerance too loose.** `1e-4` on TV would classify
  1%-overshoot as "TVD"; we used `1e-10` on fractional TV increase, which
  is essentially machine round-off for the problem size.

---

## 7. Cutover / reproduce elsewhere

```bash
git clone <this-repo-or-workspace>
cd PDE-Gottlieb-Shu-TVD-RungeKutta-1998
python3 work/ssp_rk_replication.py    # regenerate results.json
python3 work/judge.py                 # regenerate judge.json (needs Argo proxy)
```

Same NumPy 2.x + IEEE-754 should reproduce every number to full precision.
No RNG, no data dependency.
