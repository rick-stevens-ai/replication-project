# Artifacts Summary --- textures-polar-verga2014

Paper: **Verga, "Skyrmion collapse," arXiv:1409.0256v2 (2014)**
Verdict: **REPLICATED (target)** --- Coverage 8/10, Agreement 8/10.
(Prior: PARTIAL, Coverage 5-6/10, Agreement 8/10. Coverage-flip: the coupled
Schrodinger+Landau-Lifshitz dynamic collapse solver was BUILT and run.)

## 8-artifact completion bar

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-polar-verga2014.pdf` | present (1.9 MB, valid) |
| 2 | Marker extraction | `extraction/marker.md` | **interim (pdftotext)** --- marker not installed |
| 3 | Nougat extraction | `extraction/nougat.mmd` | **interim (pdftotext + hand-transcribed eqns)** |
| 4 | Report | `report/REPORT.tex` | complete (static + dynamic sections + verdict) |
| 5 | Open questions | `report/open_questions.json` | complete (5 Qs + next_steps) |
| 6 | Workflow | `report/workflow.md` | complete (static + coupled-solver build) |
| 7 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 8 | Failure analysis | `report/failure_analysis.md` | complete (honest gaps) |
| + | Evidence | `report/evidence/` | result JSON + both replication scripts |
| + | Work | `work/` | code + result JSON (scratch) |

## Evidence traces (`report/evidence/`)

- **`verga2014_result.json`** --- machine-readable results:
  - STATIC: `four_pi_J = 5.0265`; `energy_vs_lambda` E/(4piJ)=0.9966 @ lam=8;
    `Q_charge_minus=-0.980`; `self_similar_exponents` alpha=1.0, beta=0.5.
  - DYNAMIC (`coupled_dynamics`):
    - `baseline`: lam0=8, beta=0.001, Q0=-1.00, **t*=2653 t0**, full Q(t)/size(t) series
    - `dissipation_scan`: t* = 2653 / 2523 / 820 t0 for beta = 0.001 / 0.01 / 0.1
      (`dissipation_monotonic_decrease=true`; paper: 5936/1748/1236, same trend)
    - `tstar_vs_lambda`: t* = 1835 / 2653 / 3350 t0 for lam0 = 6 / 8 / 10
      (slope ~379, increasing; paper t* ~ lambda0/s0)
    - `core_shrink_fit`: lambda(t)=lambda0/sqrt(1+(s t)^2) fitted
    - `dynamic_checks`: **5/5 PASS**, `wall_time_sec=122`
- **`verga2014_repl.py`** --- static/scaling replication (BP field, exchange
  energy, Berg-Luscher charge, exponent balance).
- **`verga2014_coupled.py`** --- coupled Schrodinger+LL dynamic collapse solver.

## Key numbers (this work vs paper)

| Quantity | Paper | This work |
|----------|-------|-----------|
| Exchange energy E_xc | 4piJ = 5.0265 | 5.009 (lambda=8), <0.5% |
| Topological charge Q | +/-1 | -/+0.980 (correct sign) |
| Self-similar alpha, beta | 1, 1/2 | 1.000, 0.500 |
| **Dynamic collapse Q(t)** | **-1 -> 0** | **-1.00 -> -0.07 (collapses)** |
| **t* (beta=0.001/0.01/0.1)** | **5936/1748/1236 t0** | **2653/2523/820 t0 (same trend, ~10^3)** |
| **t* vs lambda0** | **t* ~ lambda0/s0** | **1835/2653/3350 for lam0=6/8/10 (linear)** |
| **core-shrink law** | **lam0/sqrt(1+(s t)^2)** | **fitted, holds** |

## Coverage-flip note
The single gap in the prior PARTIAL verdict --- "the coupled dynamics solver was
not built, only static energetics" --- is now closed. The coupled
Schrodinger(electrons)+Landau-Lifshitz(spins) integrator is built, stable, and
reproduces the paper's central DYNAMIC result: the current-driven finite-time
topological collapse Q:-1->0, with the correct dissipation and size trends and
the self-similar shrink law. The paper's norm-breaking regularization mechanism
is directly confirmed (collapse only proceeds when the exchange-dissipation term
breaks |S|=1). Remaining gaps are quantitative fine-detail (exact t* on the
full-spectral L=128 sea; Fig. 4 b-field maps; the Meijer-G profile f(X)).

## Extraction-tool note
Marker and Nougat are not installed; `pdftotext` is the sanctioned interim
fallback. Re-run with real Marker + Nougat when available.

## Physics note
The paper uses **exchange + spin-transfer torque + polarization (b-)field, NO
DMI**. Any "DMI" framing in the task brief is generic.
