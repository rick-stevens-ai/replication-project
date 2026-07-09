# Artifacts Summary — Nicoud (2000) Replication

Directory: `~/Dropbox/REPLICATE-PROJECT/PDE-Nicoud-conservative-highorder-lowmach-2000/`

## Code

| File | Purpose | Notes |
|---|---|---|
| `work/nicoud_scheme.py` | Staggered-mesh 4th-order operators (center↔face interp, conservative divergence, 2nd-derivative stencil), RK4 time integrator for variable-density scalar transport, T1/T2/T3 test drivers, characteristic-reference builder | Pure NumPy, ~330 lines, double precision, periodic 1-D |
| `work/llm_judge.py` | Argo REST call to `chat/completions` for judge model; temperature 0; structured JSON output; fallback logic for the opus-4.7/4.8 proxy schema-validation bug | Endpoint `http://127.0.0.1:44497/v1/chat/completions`, key `stevens` |

## Logs

| File | Purpose |
|---|---|
| `work/run.log` | stdout of the full solver battery (T1 + T2 + T3), wall time 2.46 s on `cherryrd` |

## Evidence (numerical)

| File | Content |
|---|---|
| `report/evidence/results.json` | Full T1/T2/T3 numerical results: per-N `h`, `L2` and `L∞` errors, computed convergence orders, T3 discrete-total drifts |
| `report/evidence/judge_verdict.json` | Raw Argo response + parsed judge verdict (C1: REPLICATED, C2: REPLICATED, overall: REPLICATED) with rationale |

## Reports

| File | Content |
|---|---|
| `report/REPORT.md` | Primary human-readable Markdown report (paper summary, claim table, method, results tables, judge verdict, verdict, files list) |
| `report/REPORT.tex` | LaTeX version of the report with dedicated GENUINE CRITIQUE section (scope caveats: 1-D only, periodic BCs, RK4 stronger than paper's 2nd-order integrator, no true M→0 test, spline-inverted reference, LLM-judge fallback, single implementation) |
| `report/brief.md` | One-paragraph executive summary |
| `report/attempt_log.md` | Chronological log of the replication attempt |
| `report/artifact_harvest.md` | Log of external artifacts touched (paper DOI, HAL preprint, Argo endpoint) |
| `report/workflow.md` | This-run workflow: framing → design → implementation → execution → verification → reporting |
| `report/open_questions.json` | 5 genuinely open questions the replication does NOT answer (variable-γ combustion regime, LES subgrid interaction, acoustic-feedback coupling, non-uniform-grid conservation, M→0 stability) |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | Analysis of failures/near-failures encountered (Argo opus-4.7/4.8 proxy bug, characteristic-inversion robustness, scope decisions) |

## Key numerical results (headline)

* **T1 operator convergence:** measured spatial order → 4.00 (L2 & L∞), both operators, N = 32→512.
* **T2 full time-integrated variable-density scalar transport with analytic reference:** spatial order → 4.00 (L2 & L∞), N = 32→512, 384–6132 RK4 steps.
* **T3 long-time discrete conservation, N=128, T=2, 1067 RK4 steps:**
  * Mass drift: **0.0** (exact)
  * Momentum drift: **0.0** (exact)
  * Scalar drift: **1.11 × 10⁻¹⁶** (≈ 5 ε_mach)

## LLM judge

* Requested: `argo:claude-opus-4.7`.
* Used: `argo:claude-opus-4.6` (fallback; opus-4.7/4.8 return an Argo-proxy schema-validation error; verified against 5 models — opus 4.5/4.6, sonnet-4.6, gpt-4o all clean).
* Endpoint: `http://127.0.0.1:44497/v1/chat/completions`, key `stevens`, temperature 0, latency 9.2 s.
* Verdict: C1 REPLICATED, C2 REPLICATED, overall REPLICATED.

## Compliance

* All LLM traffic via Argo proxy (no Anthropic-direct, OpenAI-direct, OpenRouter).
* No paid endpoints.
* All numerical work on local NumPy at `cherryrd`, ~2.5 s wall.
* uicgpu not required (problem is trivially small).
