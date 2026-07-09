# Artifacts summary — arXiv:2102.12655

## 8-artifact completion bar (per QC_WAVE_BRIEF_2026-07-03.md)
| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | Original PDF | `paper.pdf` | ✅ 497,591 bytes, 20 pages, v1 |
| 2 | Marker extraction | `extraction/marker.md` | ⚠️ Fallback (pdftotext -layout); Marker not installed on host. 1,168 lines. |
| 3 | Nougat extraction | `extraction/nougat.mmd` | ⚠️ Fallback (pdftotext); Nougat not installed on host. 1,968 lines. |
| 4 | LaTeX report | `report/REPORT.tex` | ✅ Section-by-section, verdict = REPLICATED |
| 5 | Open questions | `report/open_questions.json` + `## Open Questions` in report | ✅ 5 objects, each {q, basis, next_steps} |
| 6 | Workflow | `report/workflow.md` | ✅ Full workflow + tool versions + effort estimate |
| 7 | Artifacts inventory | `report/artifacts_summary.md` | ✅ (this file) |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ Honest fallback/friction/gap analysis |

## Evidence files
| Path | Purpose |
|---|---|
| `report/evidence/trotter_scaling.py` | Runs the TFIM Trotter scaling experiment. |
| `report/evidence/trotter_scaling.json` | Raw output: for each n∈{4,6} and δt∈{0.5,0.25,0.125,0.0625,0.03125}, the S1/S2/S4 op-norm error, state infidelity, S1 bound, and derived log-log slopes. |
| `report/evidence/trotter_scaling.png` | Two-panel log-log plot (op-norm; state infidelity) confirming slopes 1/2/4 (op-norm) and 2/4/~8 (state infidelity). |
| `report/evidence/make_plot.py` | Plot script. |

## Intermediates / work
| Path | Purpose |
|---|---|
| `work/paper.txt` | pdftotext raw (reading order) of paper.pdf |
| `work/paper_layout.txt` | pdftotext -layout (preserves columns) of paper.pdf |

## Traces
No external LLM/API traces (nothing routed to Argo/OpenAI/Anthropic for
this replication — the verdict is a deterministic function of the
numerical slopes and needs no LLM judge).

## Reproducibility one-liner
```bash
cd QC-200/QC-2102.12655-spectral-analysis-product-formulas-quantum-simulation-yi-crosson
python3 report/evidence/trotter_scaling.py && python3 report/evidence/make_plot.py
```
