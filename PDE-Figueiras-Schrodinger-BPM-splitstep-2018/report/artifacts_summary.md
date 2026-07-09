# Artifacts Summary — Figueiras 2018 Split-Step BPM Replication

Directory: `~/Dropbox/REPLICATE-PROJECT/PDE-Figueiras-Schrodinger-BPM-splitstep-2018/`

## Reports (`report/`)
| File | Purpose |
|---|---|
| `REPORT.md` | Canonical replication narrative — paper summary, claims table (C1–C4), results table, method, honest negatives, judges, verdict |
| `REPORT.tex` | Typeset LaTeX version with a dedicated **Genuine Critique** section |
| `open_questions.json` | Five open questions grounded in what REPORT.md tested vs did not test |
| `workflow.md` | Stage-by-stage replication workflow (paper ingestion → verdict) |
| `artifacts_summary.md` | This file |
| `failure_analysis.md` | Explicit failure-mode ledger for the replication effort |

## Solver + tests (`work/`)
Based on REPORT.md §3. Not re-inspected by this backfill; treat filenames as authoritative per the report.
| File | Role |
|---|---|
| `bpm.py` | `BPM1D` / `BPM2D` split-step Fourier solver classes (angular-k, kinetic `exp(-i·dt·k²/2)`, position-space potential kick, nonlinear `V(ψ)=κ|ψ|²` supported) |
| `test1_free_gaussian.py` | Analytic-first: free minimum-uncertainty Gaussian vs exact free propagator (L2 ~ 1e-14; σ(T) to 12 digits) |
| `test3_reflectionless.py` | Wavepacket scattering on `V = -s(s+1)/cosh²x` for s ∈ {1,2,3,10}; Fourier-partition reflection metric |
| `test3d_verify_formula.py` | Exact closed-form `R(k,s) = sin²(πs)/(sinh²(πk)+sin²(πs))`; proves R=0 iff s ∈ ℤ |
| `test4_soliton.py` | Bright soliton vs eq. (5); two-soliton head-on collision |
| `test5_order_selfconv.py` | Cauchy self-convergence on nonlinear soliton → observed order 1.000 |
| `make_figs.py` | Regenerates paper-figure reproductions |
| `test3c` (discarded) | Stationary-Schrödinger ODE scattering integrator — unstable for odd integer s; explicitly discarded (see failure_analysis.md) |

## Evidence (`evidence/`)
Per REPORT.md §4 and §6:
| File | Content |
|---|---|
| `evidence_test1.json` | Free Gaussian: IC match, L2 vs analytic, group velocity, spreading law numbers |
| `evidence_test3.json` | Reflectionless: wavepacket R for s ∈ {1,2,3,10} (e.g. R ≈ 2.6e-8 at s=10), T |
| `evidence_test3d.json` | Closed-form R vs numerical for integer/non-integer s (≈1e-32 at integer s) |
| `evidence_test4.json` | Single-soliton peak (1.00007), field L2 (≈7e-4 over T=15); collision peaks/norm |
| `evidence_test5.json` | Self-convergence order values 1.0005, 1.0002, 1.0001 |
| `evidence_judges.json` | Three-judge (argo:gpt-5.2, argo:gemini-2.5-pro, argo:gpt-4.1) verdicts + C1–C4 coverage |
| `fig1_reflectionless_s10.png` | Reproduction of paper Fig 1 |
| `fig2_soliton_collision.png` | Reproduction of paper Fig 2 |

## Key numerical results (from REPORT.md)
| Quantity | Value |
|---|---|
| Norm conservation (real V) | \|norm − 1\| ≈ 1e-13 |
| Free-propagation L2 vs analytic | ≈ 1e-14 |
| Gaussian spreading agreement | 12 digits |
| Reflection at s=10 (wavepacket) | R ≈ 2.6e-8 |
| Transmission at s=10 (wavepacket) | T = 1.000000 |
| Reflection integer-s (closed form) | R = 0 exactly (numerical ~1e-32) |
| Bright soliton peak (exact 1) | 1.00007 |
| Bright soliton field L2 over T=15 | ≈ 7e-4 |
| Two-soliton collision peaks | 1.0 → 0.99989 |
| Two-soliton collision norm | 4.0000 |
| Self-convergence orders | 1.0005 / 1.0002 / 1.0001 |

## Judges (all Argo, temperature 0)
| Judge | Verdict | Coverage |
|---|---|---|
| argo:gpt-5.2 | REPLICATED | C1,C2,C3,C4 |
| argo:gemini-2.5-pro | REPLICATED | C1,C2,C3,C4 |
| argo:gpt-4.1 | REPLICATED | C1,C2,C3,C4 |

## Provenance
- Paper PDF sha256: `034a26a1f606e6b1f5c5a0135a89d45c0ef137b5e763cabb10a190d67e933486`
- Paper license: Open Access CC-BY 3.0 (IOP)
- Authors' shipped supplementary library: **not** downloaded, **not** consulted (independence guarantee)
- Environment: CherryRd (Darwin), CPU-only; Python 3.14.6, numpy 2.4.3, scipy 1.18.0, matplotlib 3.10.8

## Scope notes
- Verdict REPLICATED covers C1–C4 (solver, integer-s Pöschl-Teller reflectionless, 1D bright soliton + collision, first-order accuracy).
- The paper's 2D headline demonstrations (vortex beams, filamentation, GP vortex precession) were **not** run to full paper-figure fidelity; `BPM2D` exists in the solver but was not exercised as thoroughly. See open_questions.json Q1.
