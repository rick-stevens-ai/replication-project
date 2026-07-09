# Artifacts Summary — Ma-Xu-Zhang mPNP replication

Directory root: `~/Dropbox/REPLICATE-PROJECT/PDE-Ma-Xu-Zhang-mPNP-coulomb-hardsphere-2020/`.

## Paper source
| Path | Purpose |
|---|---|
| `work/paper.pdf` | arXiv 2002.07489 v3, 1,006,890 bytes |
| `work/paper.txt` | `pdftotext -layout` output, 1343 lines |

## Source code (from-scratch, this replication)
| Path | Purpose |
|---|---|
| `work/src/mfmt_1d.py` | Vectorised 1D MFMT weighted-density integrator; cumulative-sum trapezoidal rule + linear endpoint corrections; strict O(h^2) |
| `work/src/experiment_convergence.py` | MFMT convergence test at (ε,q,a)=(0.2,0.3,0.15), c_i(x)≡1, N ∈ {200,400,800,1600,3200}; analytic Carnahan–Starling target |
| `work/src/pb_newton.py` | Steady mPNP Newton solver: MF (single Newton) and SC (outer damped Picard on μ^hs + inner Newton on φ) |
| `work/src/plots.py` | Produces the two evidence PNGs |
| `work/src/llm_judge.py` | Argo :44497 LLM-judge with Opus 4.7 → Sonnet 4.6 → gpt-5.2 fallback chain |

## Evidence artifacts
| Path | Content |
|---|---|
| `report/evidence/fig41_convergence.json` | Table of μ_hs^num vs Carnahan–Starling analytic and observed convergence order per grid doubling |
| `report/evidence/fig41_convergence.png` | log–log convergence plot |
| `report/evidence/fig45_newton_mf_sc.json` | MF and SC steady-state profiles c_+(x), c_-(x), φ(x); scalar summaries c_+^max, c_-^min, Q_left |
| `report/evidence/fig45_mf_vs_sc_replication.png` | Density-profile plot (MF vs SC) |
| `report/evidence/llm_judge.json` | Per-claim SUPPORTED/CONTRADICTED/INSUFFICIENT and overall verdict |
| `report/evidence/llm_judge_model.txt` | Records the actual judge model used (Sonnet 4.6, Opus 4.7 fell back due to HTTP 502) |

## Reports (this directory)
| Path | Content |
|---|---|
| `report/REPORT.md` | Full narrative report (paper summary, claims, method, results, verdict, cross-check) |
| `report/REPORT.tex` | LaTeX rendition of REPORT.md with a dedicated Genuine Critique section |
| `report/open_questions.json` | Five genuinely open questions with basis and next steps |
| `report/workflow.md` | Reproducible workflow from pre-flight through post-flight |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | Explicit inventory of what went wrong, what stayed unresolved, and what could have been better |

## Key numerical results reproduced here
- **MFMT convergence order**: observed 2.001, 2.000, 2.000, 2.000 across N ∈ {200,400,800,1600,3200}; N=3200 error 2.91e-7 vs analytic 0.238752 (Carnahan–Starling at η = 0.028274).
- **MF Newton**: c_+^max = 1.7649 at x = -0.850; c_-^min = 0.5666; residual |R| = 3.5e-12 in 5 iterations.
- **SC nested Newton**: c_+^max = 2.0943 at x = -0.850; c_-^min = 0.6872; μ_rel_diff = 8.7e-10 in 35 outer iterations; μ^hs_bulk numerically = 0.2387 matches Carnahan–Starling analytic exactly.
- **Diffuse charge ordering**: Q^MF_left = 0.2240, Q^SC_left = 0.2300, ratio Q_SC/Q_MF = 1.027 (matches paper's claim Q_SC > Q_MF).

## LLM judge (Argo Sonnet 4.6)
- C1: SUPPORTED (convergence orders + CS target hit)
- C2: SUPPORTED (SC peak 2.0943 > MF peak 1.7649)
- C3: SUPPORTED (Q_SC = 0.2300 > Q_MF = 0.2240)
- Overall: **REPLICATED**

## What is NOT in this artifact set
- WKB Coulomb self-energy of Eq. 3.22 (LC/LS sub-models). See prior Ollie 2026-05-28 replication at `~/Dropbox/REPLICATE-PROJECT/PDE-replications/modified-pnp/` for that piece.
- Time-dependent mPNP simulations (C8 mass-conservation, transient dynamics).
- MC/MD reference data ingestion for C5–C7 (paper's headline physical claims).
