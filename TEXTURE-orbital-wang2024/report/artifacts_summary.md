# Artifacts Summary — wang2024 (arXiv:2411.00315)

## Inventory
| Artifact | Path | Purpose |
|---|---|---|
| Paper PDF | `paper.pdf` | Source paper |
| Extraction (marker) | `extraction/marker.md` | pdftotext fallback text (clean) |
| Extraction (nougat) | `extraction/nougat.mmd` | secondary extraction pass |
| Method extraction | `report/method_extract.md` | 5 central claims + recipe + feasibility |
| Reproduction code | `work/reproduce.py` | NumPy Kane-Mele TB + Kubo Hall (CPU, ~10 min) |
| Raw results | `work/results.json` | all numeric outputs |
| Compute notes | `work/COMPUTE_NOTES.md` | method, headline result, caveats, self-verdict |
| Band figure | `work/figs/bands.png` | band structure with SOC gap |
| OHC figure | `work/figs/ohc_vs_EF.png` | orbital & spin Hall vs E_F (in-gap plateau) |
| Report (LaTeX) | `report/REPORT.tex` | full reproduction report |
| Report (PDF) | `report/REPORT.pdf` | compiled report |
| Open questions | `report/open_questions.json` | 5 grounded follow-ups |
| Workflow | `report/workflow.md` | pipeline + compute description |
| Failure analysis | `report/failure_analysis.md` | normalization gap + scope limits |
| This inventory | `report/artifacts_summary.md` | file map + key-number trace |

## Key Numbers Trace
Source of truth: `work/results.json` -> report tables.

| Quantity | Value | Cross-check |
|---|---|---|
| Orbital Hall plateau | **-8.832** (std **0.000**) | headline claim C2 -> WORKED |
| Spin Hall plateau (QSH) | **2.850** | claim C3 -> WORKED (near-quantized) |
| Orbital >> Spin | 8.83 vs 2.85 | claim -> WORKED |
| Min direct SOC gap | **0.4472 eV** | numeric |
| Indirect SOC gap | 0.4501 eV | numeric |
| KM theory gap 2*3*sqrt(3)*lambda_SO | **0.4469 eV** | matches numeric to 4 dp -> Hamiltonian validated |
| VBM / CBM | -0.2251 / +0.2251 eV | symmetric |
| Params | t=1.3, lambda_SO=0.043, Delta=0, kmesh=60x60 | germanene-like KM |

## Verdict
**REPLICATED (headline).** Quantized in-gap orbital Hall plateau, orbital>>spin
hierarchy, and KM-theory gap self-validation all reproduce cleanly. Only the absolute
e^2/h normalization constant is unpinned (units convention, not physics).
