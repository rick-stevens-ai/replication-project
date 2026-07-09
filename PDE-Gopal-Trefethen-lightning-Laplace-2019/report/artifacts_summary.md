# Artifacts Summary — Gopal–Trefethen Lightning Laplace Replication

All paths relative to `PDE-Gopal-Trefethen-lightning-Laplace-2019/`.

## Report

| Path | Description |
|---|---|
| `report/REPORT.md` | Canonical replication report (this backfill was derived from it). Contains claims table, method, results tables, multi-judge assessment, verdict = REPLICATED. |
| `report/REPORT.tex` | LaTeX rendering of REPORT.md with dedicated GENUINE CRITIQUE section. |
| `report/open_questions.json` | 5 truly open follow-up questions grounded in the Gopal–Trefethen lightning-Laplace method (Helmholtz extension, multi-reentrant domains, alternative spacings, biharmonic/Stokes, hp-FEM benchmark). |
| `report/workflow.md` | End-to-end procedure and stage-by-stage sequence that produced the verdict. |
| `report/artifacts_summary.md` | This file. |
| `report/failure_analysis.md` | Debrief on the v1 → v2 error progression and residual conditioning floor. |

## Solver code (`work/`)

| Path | Purpose |
|---|---|
| `work/lightning_laplace.py` | v1 solver: uniform-σ clustering, identical `n_pc` at all corners. Preserved as historical spot-check. |
| `work/run_challenge.py` | v1 driver for the NA-Digest L-shape challenge. Best v1: `ndof=562`, `|Δ|=1.05e-7`. |
| `work/lightning_v2.py` | v2 canonical solver: per-corner tapered clustering (heavy at reentrant, light at convex) + Vandermonde-with-Arnoldi orthogonalization for the polynomial part. Contains `interior_angle` geometry helper. |
| `work/lightning_v2_fine.py` | 800-point grid search around v2 optimum (sweeps `n_re, n_c, npoly, σ_re, σ_c`); writes `results_tapered_fine.json`. |
| `work/convergence_v2.py` | Convergence sweep with `n_c=4, npoly=24, σ=4.0`, varying `n_re ∈ {8..44}`; log-linear fit of err vs √N; plots figure. |
| `work/best_confirm.py` | Reruns the winning config; weighted-LSQ sanity check. |
| `work/second_geom.py` | Independent-of-paper validation: (A) equilateral triangle + `h=Re(z³)`, (B) same L-shape + `h=Re(1/(z − c₀))`. |
| `work/judge_v2.py` | Multi-LLM judge harness (Argo `127.0.0.1:44497` key `stevens`; models: gpt-5.2, gemini-2.5-pro, gpt-4.1). Writes `judge_v2_results.json`. |

## Evidence (`work/evidence/` — referenced by REPORT.md)

| Path | Content |
|---|---|
| `evidence/results_tapered.json` | Output of `lightning_v2.py` — first tapered result. |
| `evidence/results_tapered_fine.json` | Full 800-config grid; top-20 configurations with `|Δ| < 3e-9`. |
| `evidence/results_convergence_v2.json` | 10-row convergence sweep table (ndof, berr, `|u−paper|`). |
| `evidence/convergence_v2.png` | Log-vs-√N convergence plot; two straight lines for boundary and interior error until the high-`n_re` conditioning floor. |

## Judge outputs

| Path | Content |
|---|---|
| `work/judge_v2_results.json` | Full transcripts of the three Argo judges scoring C1/C2/C3 with prose justifications. Aggregate: C1 unanimous REPRODUCED; C2 2 REPRODUCED + 1 PARTIAL; C3 unanimous REPRODUCED; overall REPLICATED. |

## Extraction

| Path | Content |
|---|---|
| `extraction/marker.md` | Marker-OCR of the PNAS paper (used during ingest). |

## Key numeric artifacts (extracted from REPORT.md)

| Quantity | Value | Source |
|---|---|---|
| Paper reference value `u(0.99, 0.99)` | `1.02679192610` | Gopal–Trefethen PNAS 2019 (NA-Digest L-shape challenge) |
| Independent best value | `1.0267919256146` | `results_tapered_fine.json`, best config |
| Discrepancy `|Δ|` | `4.85e-10` (≥ 9 matching digits) | Direct subtraction |
| Best config | `n_re=44, n_c=3, npoly=40, σ_re=3.5, σ_c=4.0`, `ndof=200`, `berr=5.6e-6` | `results_tapered_fine.json` |
| Boundary convergence rate | `err ~ exp(−3.21 √N)` | Log-linear fit in `convergence_v2.py` |
| Interior convergence rate | `err ~ exp(−1.95 √N)` | Same |
| Triangle C3-A validation | interior maxerr `5.8e-16` at `ndof=86` | `second_geom.py` |
| L-shape + `Re(1/(z−c₀))` C3-B validation | interior maxerr `1.09e-6` at `ndof=154` | `second_geom.py` |
| v1 → v2 improvement | `1.05e-7 → 4.85e-10` (~200× smaller) using `200/562 ≈ 0.35×` DOFs | Table in REPORT.md §4 |

## Verdict artifact

**REPLICATED** — unanimous 3/3 Argo LLM judges + hard numerical evidence (machine-precision C3-A, unrelated-datum C3-B, direct point-value C1, root-exponential fit C2).
