# Artifacts Summary — QC-1712.05384

Paper: Boixo, Isakov, Smelyanskiy, Neven — "Simulation of low-depth quantum
circuits as complex undirected graphical models" (arXiv:1712.05384).
Verdict: **REPLICATED** (C1–C4 scaling / functional-form claims; C5
supercomputer-scale numbers out of scope).

## Directory layout
```
QC-1712.05384-low-depth-circuits-graphical-models/
├── report/
│   ├── REPORT.md                     # canonical prose report (original)
│   ├── REPORT.tex                    # LaTeX version (backfilled 2026-07-06)
│   ├── open_questions.json           # 5 open questions (bare JSON list)
│   ├── open_questions_section.tex    # LaTeX rendering of open questions
│   ├── workflow.md                   # end-to-end reproduce recipe
│   ├── artifacts_summary.md          # this file
│   ├── failure_analysis.md           # honest critique + failure modes
│   └── evidence/                     # raw numerical outputs (see below)
├── src/                              # code
├── work/                             # source paper + text extract
└── extraction/                       # nougat/marker mmd stubs
```

## Code artifacts (`src/`)
| File | Purpose |
|---|---|
| `tn_sim.py` | Main sweep: circuit generator, TN builder, opt_einsum contract, statevector ground-truth, cost extraction. |
| `smoke.py` | 6-config TN ≡ SV sanity check (~5 s). |
| `smoke2.py` | Broader multi-seed TN ≡ SV correctness check. |
| `analyze.py` | Per-grid width/bound/FLOPs table, monotonicity check. |
| `analyze2.py` | Ratio stats, log-linear fits, TN-vs-2ⁿ crossover, wall-clock counts. |
| `plots.py` | Fig. 4 analog + TN-vs-statevector-ratio plot. |

## Numerical evidence (`report/evidence/`)
| File | Content |
|---|---|
| `sweep.json` | 70 configs (n=8–16, d=2–6, grids 1×m/2×m/3×m/4×4). Per-config: TN amp, SV amp, `max_abs_diff` < 1e-16, `contraction_width`, `opt_cost_flops`, wall-times. |
| `analysis.txt` | Per-grid width vs bound vs FLOPs, monotonicity. |
| `analysis2.txt` | Width/bound ratio stats (min 0.333 / med 0.667 / mean 0.810 / max 2.0), per-grid log-linear fits (slope ≈ ℓ_min), TN/2ⁿ at fixed d, wall-clock crossover count 38/70. |
| `fig4_analog_width_vs_depth.png` | Analog of paper Fig. 4: contraction width vs depth for all grids, `min(d·ℓ, n)` bound overlaid. |
| `tn_vs_statevector_ratio.png` | Bonus plot: TN_FLOPs / 2ⁿ vs n at d ∈ {2,4,6}. |

## Source paper (`work/`)
| File | Content |
|---|---|
| `1712.05384.pdf` | arXiv PDF (v2, 19 Jan 2018). |
| `1712.05384.txt` | Text extraction, for grep. |

## Backfill artifacts (added 2026-07-06)
| File | Content |
|---|---|
| `report/REPORT.tex` | LaTeX version of REPORT.md with a new §5 Critical assessment. |
| `report/open_questions.json` | 5 open questions with concrete next steps (noise extension, cotengra head-to-head, ML-boosted BP, XEB amortization, MERA/MBQC topology extension). |
| `report/open_questions_section.tex` | LaTeX rendering of the 5 open questions for inclusion in REPORT.tex. |
| `report/workflow.md` | Full reproduce recipe (~4 min end-to-end on a laptop). |
| `report/artifacts_summary.md` | This manifest. |
| `report/failure_analysis.md` | Honest critique — what was NOT verified, what could be wrong. |
| `extraction/nougat.mmd` | Nougat OCR-extraction stub (not run; see file). |

## Reproducibility gates satisfied
- ✅ Real numerical run (no fabricated numbers).
- ✅ Fresh venv, pinned deps documented.
- ✅ Sweep JSON on disk with per-point ground truth.
- ✅ Correctness check to machine precision (3.4e-17).
- ✅ Two independent analysis scripts consistent.
- ✅ Two figures reproducing paper's qualitative shape.
- ⚠️ Paper's supercomputer-scale points (Fig. 3 headline numbers) NOT reproduced (out of scope — see failure_analysis.md).
