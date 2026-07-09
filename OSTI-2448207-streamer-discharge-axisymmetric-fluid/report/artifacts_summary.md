# Artifacts Summary — OSTI 2448207

## Source paper
- **Title:** Massively parallel axisymmetric fluid model for streamer discharges
- **Authors:** Fierro, Alibalazadeh, Stephens, Moore (UNM / Texas Tech / Sandia)
- **Report:** SAND2024-12794J
- **Journal:** Comput. Phys. Commun. 2024
- **DOI:** 10.1016/j.cpc.2024.109345
- **OSTI:** 2448207
- **PDF fetched:** 1.99 MB; MD5 `41204e9adef92fa85c980f66c0d8d39f`
- **PDF acquisition path:** `ssh uicgpu` → `curl https://www.osti.gov/servlets/purl/2448207` → scp to CherryRd

## Directory layout (this replication)

```
OSTI-2448207-streamer-discharge-axisymmetric-fluid/
├── report/
│   ├── REPORT.md                    ← primary human-readable replication report (canonical)
│   ├── REPORT.tex                   ← LaTeX version with dedicated GENUINE CRITIQUE section
│   ├── open_questions.json          ← 5 truly-open plasma-physics questions (this file's siblings)
│   ├── workflow.md                  ← pipeline + step-by-step method
│   ├── artifacts_summary.md         ← this file
│   └── failure_analysis.md          ← honest accounting of what didn't work
├── extraction/                      ← (raw pdftotext output)
├── evidence/
│   ├── analytic_checks.json         ← C1–C4 numeric results
│   ├── mms_order_result.json        ← C5 order-of-accuracy table + fitted p
│   └── llm_judge.json               ← Argo gpt-5.2 judge output
└── work/
    ├── analytic_checks.py           ← arithmetic/CFL/element-count checks
    ├── mms_order.py                 ← MMS discretization-order test (verifies C5)
    ├── streamer1d_convergence.py    ← 1-D nonlinear surrogate (unstable, not evidence)
    ├── streamer1d_stable.py         ← stabilization attempt (still not usable as evidence)
    └── judge.py                     ← LLM-judge harness (free Argo gpt-5.2)
```

## Claims outcome (from REPORT.md §2, §4)

| ID | Claim | Verdict |
|----|-------|---------|
| C1 | Domain reconstruction 1.25 × 1.0 cm from two grid/Δh combos | ✅ exact |
| C2 | Courant numbers linear in Δt | ✅ max dev 1.4% |
| C3 | Benchmark CFL ≈ 0.1 | ✅ 0.096 ≈ 0.1 |
| C4 | Six element-count products | ✅ all exact |
| C5 | 1st-order spatial convergence (base scheme) | ✅ observed p = 0.995 (MMS) |
| C6 | Coupled peak-E convergence <1% at 4 μm | ⛔ out of scope (needs full HPC + CWI ref) |
| C7 | Peak-E within 5% of CWI for all times | ⛔ out of scope (proprietary reference) |
| C8 | Upwind overestimates streamer velocity vs Koren | ⚠️ attempted; surrogate unstable |
| C9 | Strong scaling ~perfect ≤256 procs; FV to 1024 | ⛔ out of scope (no cluster rerun) |

## Key numeric evidence
- **MMS order sweep (nz 64→4096):** successive observed orders 0.983, 0.992, 0.996, 0.998, 0.999, 1.000; fitted p = **0.995 (L∞)** / **0.997 (L2)**.
- **Courant slopes:** 0.1076, 0.1088, 0.110, 0.110 ps⁻¹ (mean 0.1091, max dev 1.4%).
- **CFL:** 6e5 · 5e-13 / 3.125e-6 = **0.096** ≈ 0.1.
- **Element counts:** 12,800,000; 800,000; 125,000,000; 268,435,456; 524,288; 33,554,432 — all six exact.

## LLM-judge (evidence/llm_judge.json)
- Model: free Argo `argo:gpt-5.2` at `localhost:44497`
- Coverage: **60%**
- Agreement: **moderate**
- Verdict: **PARTIAL**
- Note: replication "strongly validates several numerical/arithmetic claims … independently confirms that the stated base spatial discretization is first-order accurate (via MMS) … does not reproduce the paper's key physics-output claims tied to the full coupled streamer simulation."

## Overall verdict (from REPORT.md §5)
**PARTIAL** — core method + all analytic claims independently reproduced; full-simulation coupled physics and HPC scaling claims out of budget and unreproduced.

## Reproducibility notes
- Environment: CherryRd, Python 3.14, numpy 2.4.3, scipy 1.18.0.
- All scripts standalone; no external services beyond Argo (free) at run time (PDF already cached).
- To rerun MMS test: `python work/mms_order.py` — completes in <1 min on CherryRd.
- To rerun analytic checks: `python work/analytic_checks.py` — completes in <1 s.
- Judge rerun requires Argo proxy at `localhost:44497` (free, `Bearer stevens`).
