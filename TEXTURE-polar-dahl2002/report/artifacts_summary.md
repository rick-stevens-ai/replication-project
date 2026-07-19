# Artifacts Summary — TEXTURE-polar-dahl2002

## The 8-artifact bar
| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Model code | `code/ssflc_model.py` | ✅ 5 checks, runs clean |
| 2 | Supporting code | `code/verify_C2_prefactor.py` | ✅ analytic C2 cross-check |
| 3 | Run outputs | `work/results.json`, `work/run.log`, `work/C2_prefactor.log` | ✅ real output |
| 4 | REPORT | `report/REPORT.tex` | ✅ verdict + 5 claims |
| 5 | Open questions | `report/open_questions.json` | ✅ 5 NEW |
| 6 | Workflow | `report/workflow.md` | ✅ |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ this file |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ |

## Claims & results
| ID | Claim | Result | Verdict |
|----|-------|--------|---------|
| C1 | Switch rotates optic axis by 2θ | 45.00° vs 45.0° (err 7e-15°) | PASS (exact) |
| C2 | τ = γ/(Ps·E) switching law | τ∝1/E, R²=0.9999; prefactor analytic | PASS (scaling) |
| C3 | Helix-unwinding ~indep. of elastic stiffness (Dahl) | criterion K-invariant | PASS |
| C4 | Bistability = double-well | 2 minima ±90°, 0 without anchoring | PASS |
| C5 | Static-friction bistability (Dahl, novel) | memory + threshold switch | PASS |

## Verdict
- **Coverage: 6/10** — source is a non-quantitative polemic (no dataset/figure/number); we replicate domain physics + Dahl's 2 original proposals, but nothing the paper itself computes (it computes nothing).
- **Agreement: 8/10** — every checkable statement reproduces; C1 exact, C2 scaling exact (prefactor explained), C3–C5 self-consistent.
- **Overall: REPRODUCED (domain-physics level).** Paper correctly flagged non-replicable as a primary paper; its physics is sound.

## Key parameters (SSFLC, DOBAMBC/HOBACPC-like)
K=5 pN, Ps=40 nC/cm², θ=22.5° (2θ=45°), Δε=1, W_s=1e-4 J/m², γ=0.1 Pa·s, d=1.5 µm, pitch=3 µm.

## Compute
Local Python 3 / numpy 2.4.3 / scipy 1.18.0. No network, no paid endpoints. Deterministic.
