# Artifacts Summary — urazhdin2023

**Paper:** Urazhdin (2023), "Symmetry constraints on the orbital transport in solids," arXiv:2309.04442.
**Verdict:** REPLICATED (all 5 claims matched to paper precision).

## Inventory

| Artifact | Path | Description |
|---|---|---|
| Original PDF | `paper.pdf` (385 KB) | Downloaded + %PDF-validated from arXiv. |
| Marker extraction | `extraction/marker.md` (23 KB) | pdftotext fallback; clean readable text. |
| Nougat extraction | `extraction/nougat.mmd` (stub) | Not required — paper is fully analytic. |
| Method extraction | `report/method_extract.md` | Recipe: 5 claims, method class, parameters. |
| Reproduction code | `work/reproduce.py` (19 KB) | numpy/sympy reproduction of C1-C5. |
| Results | `work/results.json` (2 KB) | All reproduced numbers (trace, below). |
| Figure C2 | `work/figs/c2_dispersion.png` | t2g orbital-selective dispersion. |
| Figure C3 | `work/figs/c3_oscillation.png` | ⟨Lz⟩ coherent oscillation. |
| Report | `report/REPORT.tex` | Section-by-section replication report. |
| Open questions | `report/open_questions.json` | 5 new open questions from this replication. |
| Workflow | `report/workflow.md` | Workflow + tools + effort. |
| Failure analysis | `report/failure_analysis.md` | Honest failure/limitation analysis. |

## Key reproduced numbers (trace vs paper)

| Quantity | Reproduced | Paper | Match |
|---|---|---|---|
| V22 / V_ddσ | 1/16 = 0.0625 | 0.06 | ✓ exact |
| V2-2 / V_ddσ | 35/48 = 0.7292 | 0.73 | ✓ exact |
| V20 / V_ddσ | −5√3/24 = −0.3608 | −0.36 | ✓ (unnormalized real convention) |
| V21, V2-1 | 0 | 0 | ✓ |
| ⟨Lz⟩ static (σ=±1) | ±1.0 ħ | ±ħ | ✓ |
| ⟨Lx⟩, ⟨Ly⟩ | 0 | 0 | ✓ |
| Oscillation frequency | 1.934×10^14 Hz | ~10^14 Hz | ✓ |
| Analytic vs numeric dev | 1.5×10^-14 | — | ✓ (machine precision) |
| Reversal/conserve ratio | 136-148 | ~150 | ✓ |
| Lost/conserve ratio | 33.3 | ~30 | ✓ |
| t2g band width | 1.6 eV = 8V | 8V | ✓ |

All traces reproducible via `python work/reproduce.py` (writes `work/results.json` + figures).
