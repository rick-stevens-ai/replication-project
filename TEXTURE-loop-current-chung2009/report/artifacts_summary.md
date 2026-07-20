# Artifacts summary — chung2009 (chiral spin liquid, flux 1/3)

**Verdict: REPLICATED** · Coverage 8/10 · Agreement 9/10

## Headline numbers (traced to evidence)
| Quantity | This work | Paper | Source key in `chung2009_result.json` |
|---|---|---|---|
| `<Phi_x>` non-Abelian ($g<\sqrt3$) | **1/3** (exact) | 1/3 | `counting.non_abelian.phi_x` |
| `<Phi_x>` Abelian ($g>\sqrt3$) | **0** (exact) | 0 | `counting.abelian.phi_x` |
| $n_{DEG}$ nA / A | **3 / 4** | 3 / 4 | `counting.*.n_deg_from_relation` |
| Transition $g_c$ (gap min) | **1.725** | $\sqrt3$=1.7321 | `gc_measured.g_at_min_gap` |
| $g_c$ relative error | **0.41%** | — | `comparison.gc_rel_err` |
| `<Phi_x>(T→0)` via Eq.13 | **0.33333** | 1/3 | `comparison.phi_x_lowT_via_Eq13` |
| Chern (nA, g=1.0/1.3) | +3 (nonzero) | chiral | `chern` |
| Chern (A, g=2.5) | 0 | trivial | `chern` |

## The 8 artifacts
| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | Source paper | `textures-loop-current-chung2009.pdf` | present |
| 2 | Marker extraction (PROSE) | `extraction/marker.md` | present (pdftotext -layout interim; marker not installed) |
| 3 | Nougat extraction (MATH) | `extraction/nougat.mmd` | present (hand-transcribed Eqs 1–13 + pdftotext appendix; nougat not installed) |
| 4 | Report | `report/REPORT.tex` | present (ships as .tex; pdflatex not installed) |
| 5 | Open questions | `report/open_questions.json` | present (5 heavy Qs + next_steps) |
| 6 | Workflow | `report/workflow.md` | present |
| 7 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 8 | Failure analysis | `report/failure_analysis.md` | present |

## Evidence & code
- `report/evidence/chung2009_result.json` — full run output (counting, gap scan, Chern, finite-T)
- `report/evidence/code/chung2009_kernel.py` — from-scratch Majorana kernel
- `report/evidence/replication_recipe.json` — extracted recipe
- `work/chung2009_kernel.py`, `work/chung2009_result.json` — working copies

## Reproduce block
```bash
cd /home/stevens/textures-100/corpus/textures-loop-current-chung2009/work
~/comfyui-env/bin/python chung2009_kernel.py
# prints: <Phi_x>_nA = 0.3333..., gap min near g=1.725 (paper sqrt3=1.7321),
#         Chern +3 (nA) -> 0 (A), <Phi_x>(T) plateau at 1/3 then decays
```

## Extraction fidelity note
`marker`/`nougat` are not installed on this runner; artifacts 2+3 are the
documented `pdftotext` interim fallback. This is a **tooling** limitation, not a
physics gap — the authoritative equations are hand-transcribed into
`extraction/nougat.mmd` and `report/REPORT.tex`.
