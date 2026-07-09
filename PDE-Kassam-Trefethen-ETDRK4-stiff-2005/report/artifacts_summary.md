# Artifacts Summary — Kassam & Trefethen (2005) ETDRK4 Replication

**Directory:** `~/Dropbox/REPLICATE-PROJECT/PDE-Kassam-Trefethen-ETDRK4-stiff-2005`

## Report artifacts (`report/`)

| File | Purpose |
|------|---------|
| `REPORT.md` | Primary narrative report (claims, method, results, verdict, caveats). |
| `REPORT.tex` | LaTeX rendering with a dedicated GENUINE CRITIQUE section. |
| `brief.md` | One-paragraph what/why summary. |
| `attempt_log.md` | Chronological log of implementation attempts, including the KdV first-order bug and its fix. |
| `artifact_harvest.md` | External-artifact inventory (none — analytic ICs only). |
| `judge_result.txt` | Single Argo LLM sanity read of the initial draft (not peer review). |
| `workflow.md` | End-to-end phase-by-phase workflow. |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Detailed failure/near-miss diagnosis. |
| `open_questions.json` | Five open questions grounded in the paper, with basis + next steps. |

## Evidence artifacts (`report/evidence/`)

| File | Generator | Content |
|------|-----------|---------|
| `cancellation.log` | `run_cancellation.py` | Sweep of direct vs contour relative error on `f1, Q`. |
| `cancellation.png` | `run_cancellation_figure.py` | K&T Fig. 2-style plot; contour flat near machine ε, direct diverges as \|hL\|→0. |
| `cancellation_data.json` | `run_cancellation.py` | Raw 60-point sweep, mpmath 50-digit reference. |
| `convergence.log` | `run_convergence.py` | ETDRK4 & IFRK4 fitted orders + mean error ratios per PDE. |
| `convergence.png` | `run_convergence_figure.py` | K&T Fig. 3-style log-log convergence panels (4 PDEs). |
| `convergence_data.json` | `run_convergence.py` | Raw error tables (5 halved h × 4 PDEs × 2 integrators). |
| `kdv_selfconv.log` | `run_kdv_selfconv.py` | Cauchy self-convergence log₂ ratios (recovers order 4 mid-range). |
| `kdv_soliton.log` | `run_kdv_soliton.py` | Exact single-soliton error + mass / L² invariants. |
| `ks_figure.log` | `run_ks_figure.py` | Long-time chaotic KS diagnostics stdout. |
| `ks_spacetime.png` | `run_ks_figure.py` | K&T Fig. 4-style space-time contour, T=150. |
| `ks_figure_diagnostics.json` | `run_ks_figure.py` | Bound / drift / RMS diagnostics. |

## Code artifacts (`work/`)

| File | Role |
|------|------|
| `etdrk4_core.py` | ETDRK4 step + `etdrk4_coeffs` (contour) + `etdrk4_coeffs_direct` (naive, for demo). Full unit circle, complex coefficients preserved. |
| `pdes.py` | Fourier-spectral PDE setups: KS (N=128), Burgers (N=128, ν=0.03), Allen–Cahn (N=256, ε=0.01), KdV (N=512). |
| `integrators.py` | `integrate_etdrk4` and `integrate_ifrk4` time-stepping loops. |
| `run_cancellation.py` | C1/C2 numeric sweep. |
| `run_cancellation_figure.py` | C1/C2 figure. |
| `run_convergence.py` | C3/C4 numeric convergence + IFRK4 comparison. |
| `run_convergence_figure.py` | C3/C4 figure. |
| `run_kdv_selfconv.py` | C3 clean order via Cauchy self-convergence for KdV. |
| `run_kdv_soliton.py` | C5 exact-soliton error + invariants. |
| `run_ks_figure.py` | C6 long-time KS space-time figure + diagnostics. |

## Headline numbers (from `REPORT.md`)

- Coefficient cancellation gap: worst direct \|f1\| error 2.24e-6 vs worst contour 3.06e-15 on \|hL\|<0.5 → ratio **7.31 × 10⁸**.
- Fitted temporal orders (reference-based): **KS 3.80, Burgers 3.88, Allen–Cahn 4.05**; KdV 2.65 (reference-floor-limited).
- KdV Cauchy self-convergence log₂ ratios: **4.09, 3.85** in the mid-range.
- ETDRK4 vs IFRK4 mean error ratio: **1.40× (Burgers) to 5.14× (KdV)**.
- KdV soliton error T=2: **3.28e-9** across h ∈ {2e-3, 1e-3, 5e-4} (spatial-floor limited); mass drift 2.8e-16; ∫u² drift 4.5e-14.
- Long-time KS T=150: solution finite, max\|u\|=3.37, RMS 1.18, mean drift 4.4e-17.

## What is NOT in this deliverable

- Krogstad ETDRK4-B variant (paper's C7) — explicit scope cut.
- Chebyshev-spectral / non-diagonal L runs — Fourier only.
- Wall-clock work-precision study vs IMEX-RK or split-step — accuracy-only comparison.
- Extended-precision (fp128 / mpmath) integration runs — fp64 only.
- Pixel-level match of K&T Fig. 4 chaotic KS trajectory — qualitative match on bound / RMS / drift / pattern only.

## Verdict
**REPLICATED (strong).** 6 / 6 attempted claims (C1–C6) reproduced; C7 explicit scope cut. See `REPORT.md` §6.
