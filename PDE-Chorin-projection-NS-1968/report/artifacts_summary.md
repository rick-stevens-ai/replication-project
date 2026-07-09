# Artifacts Summary — Chorin (1968) Replication

All paths relative to `~/Dropbox/REPLICATE-PROJECT/PDE-Chorin-projection-NS-1968/`.

## `report/` — Human-readable outputs

| File | Purpose |
|---|---|
| `REPORT.md` | Canonical narrative (17 KB): claims C1–C6, methods, per-claim results tables, verdict + justification, file manifest. |
| `REPORT.tex` | Detailed LaTeX version + dedicated GENUINE CRITIQUE section (substitutions, Re=400 v-profile caveat, convergence-rate anomalies, untested claims C5/C6, LLM-judge caveat, what we do not claim). |
| `brief.md` | 1-paragraph elevator summary. |
| `attempt_log.md` | Chronological log of the replication effort. |
| `artifact_harvest.md` | Data + URL manifest (paper PDF URL, SHA-256, reference-benchmark citations). |
| `workflow.md` | Reproduction procedure (paper → solver → experiments → judge → report). |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | What went wrong (E4 nan blow-up), what we flagged as caveat vs actual bug, honest error inventory. |
| `open_questions.json` | 5 grounded truly-open research questions on Chorin projection method (Poisson BCs, splitting error, second-order variants, ADI verification, spatial-rate anomaly). |

## `report/evidence/` — Machine-readable evidence + plots

| File | Contents |
|---|---|
| `cavity_results.json` | E1, E2 detailed numbers: per-grid centerline L2/L∞ errors vs Ghia (1982), wall time, final ‖div u‖_∞. |
| `pearson_results.json` | E3 (nx=20,40,80 with auto CFL-safe dt): e(u_1), e(u_2), ‖div‖_∞. E4 (Chorin Table I params, nx=39, explicit sub-step): timestep at which run went nan. |
| `convergence_results.json` | E5 spatial convergence table: nx=10,20,40,80,160 with fixed dt=5e-5, computed rates 2.07, 2.12, 2.57, 2.13. |
| `temporal_convergence.json` | E6 Cauchy self-refinement on nx=16 with reference dt=1e-4: computed temporal rates 1.04, 1.08, 1.17. |
| `llm_judgment.json` | Full raw response from LLM judge (`argo:claude-sonnet-4.6`): verdict, coverage, agreement, per-claim rationale citing specific numerical values. |
| `ghia_comparison.png` | Centerline u(y) at x=L/2 and v(x) at y=L/2 vs Ghia sample points, for cavity Re=100 (32²,64²,128²) and Re=400 (64²,128²). |
| `convergence.png` | Log-log plots: spatial (5 grid levels) and temporal (Cauchy self-refinement) with fitted slopes overlaid. |
| `divergence_audit.png` | ‖div u‖_∞ vs wall time across all 15 runs, showing machine-precision floor (n·eps). |

## `work/` — Executable code + raw logs

| File | Purpose |
|---|---|
| `chorin1968.pdf` | Source paper. SHA-256 `94c4a22f71ab16675207a1b44daa42e2e517896175a2061d2f6dfcfdfcf1dcef`, 1.59 MB. Fetched from `https://www.ams.org/journals/mcom/1968-22-104/S0025-5718-1968-0242392-2/S0025-5718-1968-0242392-2.pdf`. |
| `chorin1968.txt` | `pdftotext -layout` extract for downstream reference. |
| `chorin_projection.py` | From-scratch MAC-grid projection solver (~250 LOC). No external NS library — only `scipy.sparse` + `scipy.sparse.linalg.splu`. |
| `run_cavity_experiments.py` | Drives E1, E2, E7 (cavity divergence). Emits `evidence/cavity_results.json`. |
| `pearson_test.py` | Drives E3, E4. Emits `evidence/pearson_results.json` + `pearson_run.log`. |
| `convergence_study.py` | Drives E5 spatial convergence. Emits `evidence/convergence_results.json` + `convergence_run.log`. |
| `temporal_convergence.py` | Drives E6 temporal Cauchy self-refinement. Emits `evidence/temporal_convergence.json`. |
| `make_plots.py` | Generates the 3 evidence PNGs. |
| `llm_judge.py` | Sends the paper claims + our evidence to `argo:claude-sonnet-4.6` via free Argo proxy (`127.0.0.1:44497`). No regex on the verdict — parses the JSON response. Emits `evidence/llm_judgment.json`. |
| `cavity_run.log` | E1/E2 stdout + stderr. |
| `pearson_run.log` | E3/E4 stdout + stderr (includes the E4 nan blow-up trace at step 17). |
| `convergence_run.log` | E5 stdout + stderr. |

## Key numerical results (indexed for quick lookup)

| Quantity | Value | Location |
|---|---|---|
| Divergence-free (C1), all runs | ‖div u‖_∞ ∈ [3.5e-16, 1.6e-13] | `cavity_results.json` + `convergence_results.json` |
| Cavity Re=100, 128², err_u_L2 vs Ghia | 2.2e-3 | `cavity_results.json` |
| Cavity Re=400, 128², err_v_L∞ vs Ghia | 1.47e-1 (right-wall b.l. peak) | `cavity_results.json` |
| Pearson nx=20, e(u_1) | 5.7e-6 (~30× better than Chorin Table II) | `pearson_results.json` |
| Spatial rate, nx 80→160 | 2.13 (textbook O(h²)) | `convergence_results.json` |
| Temporal rate, dt 1e-3 → 5e-4 | 1.17 (drifting from 1.0) | `temporal_convergence.json` |
| E4 (Chorin Table I dt with explicit) | blew up to nan by step 17 | `pearson_run.log` |
| LLM judge verdict | REPLICATED, coverage 0.92, agreement 0.85 | `llm_judgment.json` |

## Third-party benchmarks referenced (not shipped)

- Ghia, Ghia & Shin (1982), *High-Re solutions for incompressible flow using the Navier–Stokes equations and a multigrid method*, J. Comput. Phys. 48, 387–411. Tables I & II provide the 17 sample points used for C2 comparison. Values embedded in `run_cavity_experiments.py`.

## Not included / out of scope

- No implementation of Chorin's implicit ADI Peaceman–Rachford sub-step (C6 not tested; see `failure_analysis.md` §"untested claims").
- No 3D or thermal-convection reproduction (C5 not tested; see REPORT.md §4 + Critique §5.5).
- No pressure-field convergence measurement (see REPORT.md Critique §5.6).
