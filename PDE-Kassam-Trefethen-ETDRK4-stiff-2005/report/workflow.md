# Workflow — Kassam & Trefethen (2005) ETDRK4 Replication

**Paper:** Kassam & Trefethen, *Fourth-Order Time-Stepping for Stiff PDEs*, SIAM J. Sci. Comput. 26(4):1214–1233, 2005. DOI [10.1137/S1064827502410633](https://doi.org/10.1137/S1064827502410633).

**Host / environment:** local CPU (macOS, `CherryRd`), Python 3.13, NumPy 2.4.3, SciPy 1.18.0, mpmath 1.3.0, Matplotlib 3.10.8. No paid endpoints; no external data (analytic ICs only).

**Dates:** 2026-07-02 initial draft; 2026-07-04 promotion pass (full rerun + figures).

## Phases

### Phase 0 — Paper ingest
- Read paper (arXiv/SIAM); identify seven testable claims (C1–C7).
- Choose four benchmark PDEs matching the paper: KS, Burgers, Allen–Cahn, KdV.
- Explicit scope cut: skip C7 (Krogstad ETDRK4-B variant) — secondary.

### Phase 1 — Clean-room implementation
1. `work/etdrk4_core.py`
   - `etdrk4_coeffs(L, h, M=32, r=1)` — full unit-circle contour, complex coefficients preserved.
   - `etdrk4_coeffs_direct(L, h)` — naive floating-point evaluation, kept only for the C1 cancellation demo.
   - `etdrk4_step(...)` — Cox–Matthews update stages.
2. `work/pdes.py` — periodic Fourier-spectral setups (KS N=128, Burgers N=128, Allen–Cahn N=256, KdV N=512).
3. `work/integrators.py` — `integrate_etdrk4` and competitor `integrate_ifrk4`.

### Phase 2 — Numerical experiments (in dependency order)

| Step | Script | Claims | Command |
|------|--------|--------|---------|
| C1/C2 | `run_cancellation.py` (+ `_figure.py`) | direct vs contour coefficient error | `cd work && python3 run_cancellation.py \| tee ../report/evidence/cancellation.log` |
| C3/C4 | `run_convergence.py` (+ `_figure.py`) | 4th-order fit; ETDRK4 vs IFRK4 | `cd work && python3 run_convergence.py \| tee ../report/evidence/convergence.log` |
| C3 (KdV) | `run_kdv_selfconv.py` | Cauchy self-convergence (bias-free order) | `cd work && python3 run_kdv_selfconv.py \| tee ../report/evidence/kdv_selfconv.log` |
| C5 | `run_kdv_soliton.py` | exact soliton error + mass / L² invariants | `cd work && python3 run_kdv_soliton.py \| tee ../report/evidence/kdv_soliton.log` |
| C6 | `run_ks_figure.py` | long-time chaotic KS (T=150) | `cd work && python3 run_ks_figure.py \| tee ../report/evidence/ks_figure.log` |

### Phase 3 — Debugging / mid-course correction
- KdV initially gave 1st-order convergence — traced to the coefficient routine using a half-circle contour and `real()`, which silently zeroes imaginary parts required for KdV's pure-imaginary spectrum.
- Fix: switched to FULL unit circle and kept coefficients complex throughout.
- Cross-checked with Cauchy self-convergence (bias-free) — recovered log₂ ratios of 4.09 and 3.85 in the mid-range.
- Logged in `attempt_log.md`.

### Phase 4 — Reference-comparison saturation handling
- For every PDE, reference-solution errors saturate at the spatial spectral floor (~4e-11 for KdV) at the smallest step sizes, deflating the fitted temporal-order slope.
- Mitigation: report both (a) reference-based slope and (b) Cauchy self-convergence log₂ ratios; document floor explicitly in results tables.

### Phase 5 — Report + figures + judge
- Assemble `REPORT.md` with claims table, method, results, verdict, and reproducibility notes.
- Generate figures: `cancellation.png`, `convergence.png`, `ks_spacetime.png`.
- Argo LLM judge pass → `judge_result.txt` (single-source sanity check, not peer review).

### Phase 6 — Promotion pass (2026-07-04)
- Full clean rerun of all experiments; regenerate figures; refresh `REPORT.md` with the promotion-pass numbers.
- Backfill supporting artifacts: `REPORT.tex`, `open_questions.json`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`.

## Reproducibility (single-command view)

```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Kassam-Trefethen-ETDRK4-stiff-2005/work
python3 run_cancellation.py       | tee ../report/evidence/cancellation.log
python3 run_cancellation_figure.py
python3 run_convergence.py        | tee ../report/evidence/convergence.log
python3 run_convergence_figure.py
python3 run_kdv_selfconv.py       | tee ../report/evidence/kdv_selfconv.log
python3 run_kdv_soliton.py        | tee ../report/evidence/kdv_soliton.log
python3 run_ks_figure.py          | tee ../report/evidence/ks_figure.log
```

Total wall time on CherryRd: well under 10 minutes end-to-end.

## Endpoints / data policy
- Compute: local CPU only.
- No paid model endpoints used in the numeric pipeline. Argo LLM judge (free) used once for a sanity read of the draft.
- No external datasets — every initial condition is analytic and specified in `pdes.py`.
