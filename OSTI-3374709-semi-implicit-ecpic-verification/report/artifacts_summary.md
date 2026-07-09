# Artifacts Summary — OSTI 3374709 (semi-implicit ES-PIC verification)

All artefacts under
`~/Dropbox/REPLICATE-PROJECT/OSTI-3374709-semi-implicit-ecpic-verification/`.

## Source paper

| Artefact | Location | Notes |
|---|---|---|
| Paper PDF | `extraction/` | R. M. Hedlof, D. C. Barnes, R. E. Groenewald, *et al.*, *Verification of an energy-conserving semi-implicit electrostatic particle-in-cell scheme for modeling high-density plasma at scale*, Phys. Plasmas 33, 053902 (2026). DOI 10.1063/5.0315721 · OSTI 3374709 · LBNL eScholarship 8xt682g7 · CC-BY 4.0. |
| Extracted text | `extraction/` | `pdftotext` output produced on uicgpu; used to read §III VERIFICATION. |

## Code (from-scratch replication)

| Artefact | Location | Purpose |
|---|---|---|
| SIPIC PIC driver | `work/sipic_dispersion.py` | ~180 lines NumPy 1D ES-PIC. Leapfrog + CIC + spectral (FFT) Poisson. Applies SIPIC operator (Eqs. 9–10) by multiplying the negative-Laplacian by `F = 1 + C_SI·ωpe²·Δt²/4`. Runs the `a ∈ {0.5,1,2,4,8}` sweep at `C_SI = 4` and the classical control at `C_SI = 0`. |
| Plotter | `work/plot.py` | Measured ω/ωpe vs Eq. 16 prediction vs classical baseline across the ωpe·Δt sweep. |
| LLM judge | `work/judge.py` | Free Argo `argo:gpt-5.2` (`localhost:44497`), T=0. Consumes the results table and emits a verdict. |

## Evidence (numbers, plots, judgements)

| Artefact | Location | Content |
|---|---|---|
| Raw results | `report/evidence/sipic_dispersion_results.json` | Measured ω/ωpe for the full sweep, including the `C_SI = 0` validation control. |
| Down-shift plot | `report/evidence/sipic_downshift.png` | Measured vs Eq. 16 vs classical `ω/ωpe = 1` across `ωpe·Δt ∈ {1,2,4,8,16}`. |
| LLM judge verdict | `report/evidence/llm_judge_verdict.txt` | Full text of the Argo gpt-5.2 verdict. Verbatim excerpt quoted in REPORT.md §5. |

## Reports

| Artefact | Location | Purpose |
|---|---|---|
| Markdown report | `report/REPORT.md` | Primary human-readable replication report (9 KB). Contains paper summary, claims table, method, results-vs-paper tables, LLM-judge verdict, and final verdict. |
| LaTeX report | `report/REPORT.tex` | Long-form report + dedicated **GENUINE CRITIQUE** section calling out replication weaknesses. |
| Open questions | `report/open_questions.json` | 5 truly open scientific/technical questions grounded in the paper's domain (Eq. 16 error at ωpe·Δt = 16, κ-notation reading, hybrid modes C4, energy conservation C5, Landau damping C6). |
| Workflow | `report/workflow.md` | Stage-by-stage pipeline (acquisition → claims → code → sweep → plot → judge → report → backfill). |
| Artifacts summary | `report/artifacts_summary.md` | This file. |
| Failure analysis | `report/failure_analysis.md` | Explicit list of what did NOT work / was NOT tested / could go wrong. |

## Key quantitative results (from REPORT.md, single source of truth)

### C1 sweep at C_SI = 4 (measured vs Eq. 16)

| ωpe·Δt | measured ω/ωpe | Eq. 16 prediction | classical (unmodified) | error vs Eq. 16 |
|---|---|---|---|---|
| 1  | 0.731 | 0.707 | 1.000 | 3.3 % |
| 2  | 0.451 | 0.447 | 1.000 | 0.9 % |
| 4  | 0.252 | 0.243 | 1.000 | 3.9 % |
| 8  | 0.126 | 0.124 | 1.000 | 1.9 % |
| 16 | 0.069 | 0.062 | 1.000 | 10.2 % |

### Classical control (C_SI = 0)

| ωpe·Δt | measured ω/ωpe | target |
|---|---|---|
| 0.10 | 1.033 | 1.0 |
| 0.20 | 1.011 | 1.0 |
| 0.50 | 1.017 | 1.0 |

## Verdict

**REPLICATED** (scoped to C1 in the cold 1D limit).

The paper's central SIPIC plasma-frequency down-shift
`ωpe / √(1 + C_SI·ωpe²·Δt²/4)` (Eqs. 12/16) was reproduced by an
independent from-scratch NumPy PIC to ~1–4 % over `ωpe·Δt ≤ 8`
(~10 % at 16), and is decisively distinct from the unmodified
classical `ω = ωpe`. The classical control recovers `ω ≈ ωpe`.

## Endpoints and tools

- Argo `argo:gpt-5.2` on `localhost:44497` (free) — judge.
- Local CherryRd Python 3 + NumPy + Matplotlib — driver, plot.
- `ssh uicgpu` — OA PDF fetch + `pdftotext`.
- No paid endpoints; no WarpX; no Aleph.
