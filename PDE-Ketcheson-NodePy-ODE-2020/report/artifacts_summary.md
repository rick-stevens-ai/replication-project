# Artifacts Summary — PDE-Ketcheson-NodePy-ODE-2020

## Report directory (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md`             | Canonical replication report (verdict + all 4 tables) |
| `REPORT.tex`            | LaTeX version of report, includes dedicated Genuine Critique section |
| `open_questions.json`   | 5 truly-open follow-up questions (order verification edge cases, third-party SSP, low-storage RK, implicit RK, symbolic-vs-numeric) |
| `workflow.md`           | Stage-by-stage workflow used to run the replication |
| `artifacts_summary.md`  | This file — index of everything produced |
| `failure_analysis.md`   | Failures, near-failures, and workarounds encountered |
| `evidence/`             | Machine-generated artifacts from live re-runs |

## Evidence directory (`report/evidence/`)

| Artifact | Type | Produced by | Ties to claim |
|---|---|---|---|
| `stability_RK44.png`    | PNG plot        | `m.plot_stability_region()`   | C3 |
| `stability_DP5.png`     | PNG plot        | `m.plot_stability_region()`   | C3 |
| `stability_SSP104.png`  | PNG plot        | `m.plot_stability_region()`   | C3 |
| `convergence.csv`       | Numeric CSV     | Hand-coded RK integrator on Dahlquist ODE | C4 |

## External inputs

- **Package**: `nodepy==1.0.1` from PyPI.
- **Python**: 3.13 in `work/.venv`.
- **Extra deps**: `numpy`, `matplotlib`, `sympy`, `scipy`.
- **Judge model**: Argo `argo:claude-opus-4.7` via `http://localhost:44497/v1` (FREE endpoint).
- **Host**: macOS 25.3.0.

## Coverage summary

| Claim | Method count | Data points | Verdict-relevant match |
|---|---|---|---|
| C1 — Formal order              | 11 | 11 order values      | 11/11 (SSP53 requires mode='exact') |
| C2 — SSP coefficient           | 7  | 7 radius values      | 7/7 |
| C3 — Stability region          | 3  | 3 PNGs + 18 `|R(iy)|` samples | RK44 hits classical 2√2, DP5 matches published hump, SSP104 stays below 1 to y=3 |
| C4 — Empirical convergence     | 5  | 5 methods × 6 grid sizes = 30 error values, 25 observed-order estimates | 5/5 match formal order to 2 decimals |
| C5 — Install / usability       | 1  | one clean pip install | Success |

## What is NOT in the artifact bundle

- No linear multistep, additive, or two-step method tests (out of scope of C1–C5 for this run).
- No implicit-RK diagnostics (Gauss/Radau/Lobatto not exercised).
- No nonlinear or stiff IVP convergence tests (only scalar Dahlquist).
- No low-storage RK implementation checks.
- No independent contour extraction of stability-region PNGs (only imaginary-axis spot check).

All five gaps are captured as follow-ups in `open_questions.json`.
