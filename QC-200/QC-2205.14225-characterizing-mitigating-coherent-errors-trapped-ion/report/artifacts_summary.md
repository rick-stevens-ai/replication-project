# Artifacts summary

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2205.14225-characterizing-mitigating-coherent-errors-trapped-ion/`

## 8 mandatory artifacts
| # | Path | Status | Notes |
|---|---|---|---|
| 1 | `paper.pdf` | ✅ present | 763 KB, 11pp, downloaded from arxiv.org |
| 2 | `extraction/marker.md` | ⚠ fallback | Marker not installed (PEP-668); `marker.md.notrun` holds pdftotext content |
| 3 | `extraction/nougat.mmd` | ⚠ fallback | Nougat not installed; `nougat.mmd.notrun` holds pdftotext content |
| 4 | `report/REPORT.tex` | ✅ present | Full section-by-section report with verdict = **REPLICATED** |
| 5 | `report/open_questions.json` | ✅ present | 5 numbered questions with `q`/`basis`/`next_steps` each |
| 6 | `report/workflow.md` | ✅ present | Tools/versions + step list + work estimate |
| 7 | `report/artifacts_summary.md` | ✅ present | this file |
| 8 | `report/failure_analysis.md` | ✅ present | Marker/Nougat gap + C7 stochastic-model gap + C8 VQE not attempted |

## Simulation code + traces
| File | Purpose |
|---|---|
| `report/evidence/sim_hidden_inverses.py` | Main sim: noise model + H decomps + 100-block fit + MS budget |
| `report/evidence/sim_hi_cancellation.py` | Focused HI-cancellation order test |
| `report/evidence/sim_rb_style.py` | Interleaved-RB-style per-Clifford error rate |
| `report/evidence/results.json` | Output of sim_hidden_inverses.py |
| `report/evidence/results_hi_cancellation.json` | Output of sim_hi_cancellation.py |
| `report/evidence/results_rb.json` | Output of sim_rb_style.py |

## Working files
| File | Purpose |
|---|---|
| `work/paper.txt` | pdftotext of the paper (used for claim extraction) |

## Reproducibility
All simulation results are deterministic given the seeded RNG (numpy seed `20260705` for the phase-space + shot-noise, `42` for the RB-style bench). Re-running any of the three scripts produces bit-identical JSON outputs.
