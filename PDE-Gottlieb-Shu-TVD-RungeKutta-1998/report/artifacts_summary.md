# Artifacts Summary — Gottlieb & Shu (1998) TVD/SSP-RK Replication

**Paper:** *Total variation diminishing Runge-Kutta schemes*, Gottlieb & Shu,
*Math. Comp.* 67(221):73–85, 1998. DOI 10.1090/S0025-5718-98-00913-2.
**Verdict:** REPLICATED (all three tested claims C1/C2/C3 reproduced).
**Date:** 2026-07-04.

---

## 1. Directory layout (canonical)

```
PDE-Gottlieb-Shu-TVD-RungeKutta-1998/
├── extraction/                             (upstream marker.md if any; not required)
├── work/
│   ├── ssp_rk_replication.py               # eqs. (4.1)/(4.2) + C1/C2/C3 drivers
│   └── judge.py                            # LLM-judge call to Argo argo:gpt-4o
└── report/
    ├── REPORT.md                           # canonical Markdown report (8 KB source)
    ├── REPORT.tex                          # LaTeX mirror + Genuine Critique §7
    ├── workflow.md                         # step-by-step execution recipe
    ├── artifacts_summary.md                # this file
    ├── failure_analysis.md                 # blind alleys & recovery
    ├── open_questions.json                 # 5 open follow-ups grounded in SSP-RK theory
    └── evidence/
        ├── results.json                    # raw C1/C2/C3 numeric outputs
        └── judge.json                      # LLM-judge prompt + parsed verdict
```

Everything replication-critical lives under `PDE-Gottlieb-Shu-TVD-RungeKutta-1998/`.
No external data, no downloads, no lock file. Determinism only relies on
NumPy 2.x + IEEE-754.

---

## 2. Code artifacts

| File | Purpose | Notes |
|---|---|---|
| `work/ssp_rk_replication.py` | Implements SSP-RK2 (paper eq. 4.1), SSP-RK3 (paper eq. 4.2), and a negative-β non-SSP RK2 counter-example. Runs C1 (order on `u' = -u`), C2 (TVD on 1D linear advection + upwind + step IC), C3 (binary-search on empirical `c*`). | Single-file NumPy 2.4.3. |
| `work/judge.py` | POSTs a compact numeric summary to Argo `argo:gpt-4o` (FREE proxy 127.0.0.1:44497, T=0). Parses the JSON verdict. | Uses `Authorization: Bearer stevens` per standing Argo convention. |

---

## 3. Evidence artifacts

| File | Contents |
|---|---|
| `report/evidence/results.json` | Full C1 error/rate table for `N ∈ {8,16,32,64,128,256,512}`, full C2 table for all five (scheme, CFL) cases with initial and max TV, full C3 binary-search history and final `c*` estimate. |
| `report/evidence/judge.json` | Judge prompt (numeric summary text), Argo response body verbatim, and parsed per-claim verdict fields. |

---

## 4. Report artifacts

| File | Role |
|---|---|
| `report/REPORT.md` | Canonical narrative (source of all other report files). ~8 KB. |
| `report/REPORT.tex` | LaTeX version with tables, listings, and a dedicated §7 Genuine Critique of *our own replication scope*. |
| `report/workflow.md` | Step-by-step recipe to reproduce end-to-end from a clean checkout. |
| `report/open_questions.json` | Five genuinely open questions grounded in SSP-RK / hyperbolic-conservation-law theory (SSP coefficients across spatial ops, sharp CFL transition curves past `c*`, implicit/IMEX-SSP extensions, 4-stage order-4 SSP-RK, WENO+SSP-RK3 on Euler shocks). |
| `report/failure_analysis.md` | Narrative of the blind alley that would have contaminated C1 if we had used it (imaginary-eigenvalue ODE for SSP-RK2 order study), and other near-misses. |

---

## 5. Headline numbers (single-glance)

| Claim | Paper says | We measured | Match |
|---|---|---|---|
| C1: SSP-RK2 formal order | 2 | **2.005** (mean of last 3 log₂ rates) | ✅ |
| C1: SSP-RK3 formal order | 3 | **3.005** | ✅ |
| C2: SSP-RK2 @ CFL 1.00, step IC + upwind | TVD | frac TV incr = **0.00** | ✅ |
| C2: SSP-RK3 @ CFL 1.00, step IC + upwind | TVD | frac TV incr = **0.00** | ✅ |
| C2: SSP-RK2 @ CFL 1.05 | Fails | frac TV incr = **3.26 × 10²** | ✅ |
| C2: SSP-RK3 @ CFL 1.05 | Fails | frac TV incr = **5.51 × 10⁻²** | ✅ |
| C2: non-SSP `-β` RK2 @ CFL 0.50 | Fails (no SSP) | frac TV incr = **1.23 × 10⁶** | ✅ |
| C3: empirical `c*` SSP-RK2 | 1 | **0.99997** (gap 8.85e-05) | ✅ |
| C3: empirical `c*` SSP-RK3 | 1 | **0.99997** (gap 8.85e-05) | ✅ |
| LLM-judge overall verdict | — | **REPLICATED** | (courtesy check) |

---

## 6. Provenance & determinism

- Host: CherryRd (macOS).
- Interpreter: Python 3.14.6.
- NumPy: 2.4.3.
- Judge: Argo `argo:gpt-4o` (FREE endpoint, 127.0.0.1:44497), T = 0.
- RNG: none — all experiments deterministic (fixed grids, fixed ICs).
- No external data downloaded. No pinned lock file (see workflow.md §1).

---

## 7. Honest scope caveat

"REPLICATED" here means the three headline claims C1/C2/C3 we tested were
reproduced. It does not cover the paper's 4-stage results, its non-existence
theorem for a 4-stage order-4 all-positive SSP-RK, or its higher-stage-count
optimal-coefficient constructions. See `REPORT.tex` §7 Genuine Critique
item 1 for the explicit scope statement, and `open_questions.json` for
follow-up directions.
