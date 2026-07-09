# Artifacts Summary — Zang, Street & Koseff (1994) Replication

**Replication id:** `PDE-Zang-Street-Koseff-fractional-step-1994`
**Verdict:** REPLICATED (Cartesian limit)
**Run date:** 2026-07-04

## Directory layout

```
PDE-Zang-Street-Koseff-fractional-step-1994/
├── report/
│   ├── REPORT.md                          narrative report (canonical)
│   ├── REPORT.tex                         LaTeX version + Genuine Critique
│   ├── open_questions.json                5 open follow-on questions
│   ├── workflow.md                        execution recipe
│   ├── artifacts_summary.md               this file
│   ├── failure_analysis.md                anomalies & known limits
│   └── evidence/
│       ├── centerlines_vs_ghia.png        centreline u & v vs Ghia (all 3 Re)
│       ├── streamlines_Re1000.png         primary vortex + corner secondaries
│       ├── divergence_summary.png         ||div U|| vs Re
│       ├── sweep_metrics.json             per-Re metrics table (machine)
│       └── judge_verdict.json             LLM-judge response + fallback log
├── work/
│   ├── zsk_solver.py                      solver, ~300 lines numpy/scipy
│   ├── ghia_data.py                       Ghia (1982) Tables I & II transcribed
│   ├── run_sweep.py                       driver: Re ∈ {100, 400, 1000}
│   ├── make_plots.py                      figure generation
│   ├── judge.py                           Argo LLM-judge call
│   ├── cavity_N128_Re100.npz              full u, v, p + centrelines
│   ├── cavity_N128_Re400.npz              full u, v, p + centrelines
│   └── cavity_N128_Re1000.npz             full u, v, p + centrelines
└── extraction/                            paper extraction workspace
```

## Code artifacts (`work/`)

| File | Purpose | Approx size |
|---|---|---|
| `zsk_solver.py` | Cell-centred collocated fractional-step solver: predictor (forward Euler), face-flux averaging, sparse-LU pressure Poisson, face + cell-centred velocity corrections. | ~300 lines |
| `ghia_data.py` | Ghia, Ghia & Shin (1982) centreline u (17 pts) and centreline v (17 pts) at Re = 100, 400, 1000. | 1 file |
| `run_sweep.py` | Loop over Re values; save `cavity_N128_Re{Re}.npz`; append to `sweep_metrics.json`. | 1 file |
| `judge.py` | Argo call, tries `argo:claude-opus-4.7`, falls back to `argo:claude-opus-4.5` on 502 schema-validation error. | 1 file |
| `make_plots.py` | Generate PNGs. | 1 file |

## Data artifacts

| File | Contents | Notes |
|---|---|---|
| `work/cavity_N128_Re100.npz`  | u, v, p on 128×128 grid + 17-pt centrelines | ~500 KB |
| `work/cavity_N128_Re400.npz`  | u, v, p on 128×128 grid + 17-pt centrelines | ~500 KB |
| `work/cavity_N128_Re1000.npz` | u, v, p on 128×128 grid + 17-pt centrelines | ~500 KB |
| `report/evidence/sweep_metrics.json` | Per-Re: u_min/v_min/v_max/Ghia refs, ||div U||_2, ||div U||_∞, RMS(u−u_G), RMS(v−v_G), wall (s) | machine-readable |
| `report/evidence/judge_verdict.json` | LLM-judge response, requested_model, actual_model, fallback log | machine-readable |

## Figures (`report/evidence/`)

| File | Description |
|---|---|
| `centerlines_vs_ghia.png` | Left: centreline u vs y at x=0.5. Right: centreline v vs x at y=0.5. Colours = Re (100 blue, 400 orange, 1000 green). Solid lines = ours, open markers = Ghia (1982). |
| `streamlines_Re1000.png` | Steady-state streamlines at Re=1000 showing the main primary vortex and the two lower-corner secondary vortices characteristic of the cavity at that Re. |
| `divergence_summary.png` | ||div U||_2 and ||div U||_∞ of the corrected face fluxes at final step, across all Re. All ≲ 10⁻¹³ (machine precision). |

## Key numerical results (from `sweep_metrics.json`)

| Re | u_min (ours vs Ghia) | v_min (ours vs Ghia) | v_max (ours vs Ghia) | ‖div U‖₂ | ‖div U‖∞ | RMS(u−u_G) | RMS(v−v_G) | wall (s) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100  | −0.2136 / −0.2109 | −0.2534 / −0.2453 |  0.1792 /  0.1753 | 2.2e−15 | 6.7e−14 | 0.0066 | 0.0053 |  57 |
| 400  | −0.3256 / −0.3273 | −0.4502 / −0.4499 |  0.3006 /  0.3020 | 2.5e−15 | 7.2e−14 | 0.0098 | 0.0363 |  99 |
| 1000 | −0.3789 / −0.3829 | −0.5151 / −0.5155 |  0.3670 /  0.3710 | 2.6e−15 | 1.9e−14 | 0.0155 | 0.0101 | 146 |

## LLM-judge summary (from `judge_verdict.json`)

- `requested_model`: `argo/argo:claude-opus-4.7`
- `actual_model`: `argo:claude-opus-4.5` (fallback due to Argo proxy 502)
- `verdict`: `REPLICATED`
- `core_claim_reproduced`: `true`
- `quantitative_agreement`: `high`

## Documentation artifacts (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Canonical narrative report (14 KB). |
| `REPORT.tex` | LaTeX version with dedicated *GENUINE CRITIQUE* section. |
| `open_questions.json` | 5 truly open follow-on research questions with basis and next steps. |
| `workflow.md` | Reproducible execution recipe. |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Anomalies, known limitations, and what did NOT work cleanly. |

## Reproduction cost

- Solver: ~300 lines numpy/scipy, single-threaded, single-CPU.
- Total wall-clock (all 3 Re): ~5 minutes on a single core of `uicgpu`.
- No GPU used (although an 8×A100 host was available).
- LLM-judge call: ~15 s (one Argo request + one fallback).
