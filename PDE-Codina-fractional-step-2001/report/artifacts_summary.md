# Artifacts Summary — Codina (2001) Fractional-Step Replication

All paths are relative to `~/Dropbox/REPLICATE-PROJECT/PDE-Codina-fractional-step-2001/`.

## Source paper PDFs
- `work/codina2001_scipedia.pdf` — GREEN OA mirror from Scipedia.
  SHA-1 `2388ab02e207bd1ff51b7e1443449c001b819775`.
- `work/codina2001_cimne_preprint.pdf` — March-2000 CIMNE preprint.
  SHA-1 `5660dd8cbc04e8c4fcb2f4319c2e7c5c8f15766e`.

## Code (pure NumPy/SciPy, no external FEM library)
- `work/codina_replication.py` — from-scratch Q1/Q1 fractional-step FEM.
  Consistent mass, Gauss–Legendre 2×2 quadrature, Picard convection, pinned-p
  Poisson.
- `work/cavity_run.py` — Re=100 lid-driven cavity harness; sweeps three
  δt values × two schemes; writes JSON + plots to `report/evidence/`.
- `work/llm_judge.py` — Argo GPT-5 (free endpoint `127.0.0.1:44497`) claim-by-claim
  verdict on the numerical outputs.

## Numerical outputs
- `report/evidence/cavity_results.json` — raw metrics per (scheme, δt) case:
  `P_min`, `P_max`, `P_std`, `P_roughness_d2`.
- `report/evidence/llm_judge_verdict.txt` — full JSON verdict from the Argo
  GPT-5 judge (aggregate PARTIAL, per-claim REPLICATED/NOT_TESTED/PARTIAL).

## Figures
- `report/evidence/cavity_pressure_contours.png` — pressure contours across
  the six cavity cases; visualizes checkerboarding at small δt (both schemes)
  and clean field at large δt.
- `report/evidence/pressure_stability_bar.png` — log10(P_std) bar chart across
  the six cases; makes the 5-orders-of-magnitude first-order sweep and the
  catastrophic second-order blow-up visually immediate.

## Report files
- `report/REPORT.md` — narrative report with claims table, method, results,
  interpretation, verdict, reproducibility, deviations.
- `report/REPORT.tex` — LaTeX rendering with an added "Genuine Critique"
  section (eight adversarial limitations).
- `report/open_questions.json` — five genuinely-open questions grounded in
  Codina's pressure-stabilization fractional-step method (OSS not tested,
  2nd-order blow-up magnitude gap, MMS/C5 stabilized rerun, mesh/Re
  robustness, gauge-pin sensitivity).
- `report/workflow.md` — this run's chronological workflow.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — what was tried and did not work; what was
  deferred and why.

## Reproduction command
```
cd work && OUTDIR=../report/evidence python3 cavity_run.py
```
≈ 70 s on one CPU core. Python 3.14, NumPy 2.4.3, SciPy 1.18.0, matplotlib
3.10.8.

## Headline numbers (from `cavity_results.json`, quoted in REPORT.md)
| scheme              | δt / δt_crit | P_std                | roughness_d2         |
|---------------------|-------------:|---------------------:|---------------------:|
| first_order         |          0.1 | 4.15 × 10⁴           | 1.45 × 10⁴           |
| first_order         |          1.0 | 3.28 × 10²           | 1.82 × 10²           |
| first_order         |         56.0 | 1.34 × 10⁻¹          | 3.97 × 10⁻³          |
| incremental_second  |          0.1 | 2.26 × 10⁵³          | 1.94 × 10⁵²          |
| incremental_second  |          1.0 | 1.20 × 10¹⁸          | 5.72 × 10¹⁶          |
| incremental_second  |         56.0 | 8.03 × 10⁻¹          | 2.34 × 10⁻²          |

First-order pressure quality improves ≈ 5 orders of magnitude as δt grows
0.1·δt_crit → 56·δt_crit (matches C1's √δt scaling). Second-order (unstabilized)
is catastrophic at small/critical δt and only OK at large δt (matches C2's
ordering; magnitude exceeds paper's bounded-but-oscillatory Fig 2).
