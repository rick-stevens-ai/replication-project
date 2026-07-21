# Artifacts Summary: dai2018 (arXiv:1802.03009v2)

**Paper:** Dai, Zhang, Senthil, Lee — "Pair density wave, charge density wave and vortex in high Tc cuprates"
**Assigned class:** loop-current (MISLABEL — actually cuprate PDW/CDW vortex physics)
**Verdict:** PARTIAL (see verdict.json)

## Files
| Artifact | Path | Description |
|---|---|---|
| PDF | `dai2018.pdf` | Source (4.6 MB, verified %PDF) |
| Parsed text | `work/textures-loop-current-dai2018.txt` | pdftotext, 2092 lines |
| Extraction (marker) | `extraction/marker.md` | pdftotext interim + header |
| Extraction (nougat) | `extraction/nougat.mmd` | pdftotext interim + header |
| Recipe | `report/evidence/replication_recipe.json` | method + testable headline |
| Physics code | `code/dai2018_replicate.py` | from-scratch PDW/CDW split-peak model |
| Result | `work/dai2018_result.json` | 4/4 checks (also copied to evidence/) |
| Kernel (provenance) | `report/evidence/loop_current_meanfield_kernel.py` | Ollie, credited |
| Report | `report/REPORT.tex` | full writeup |
| Open questions | `report/open_questions.json` | 5 Qs + next_steps |
| Workflow | `report/workflow.md` | pipeline log |
| Failure analysis | `report/failure_analysis.md` | limitations |
| Verdict | `report/evidence/verdict.json` | judge output |

## Headline reproduced
PDW-driven period-8 CDW → SPLIT Q/2 FFT peak + real-space nodal line (from d-wave 2π winding);
CDW-driven → SINGLE peak. 4/4 qualitative checks pass.

## Honest scope
Reproduced the paper's phenomenological experimental discriminator, NOT the full BdG ED (Appendix B).
Split magnitude grid-limited (δq≈0.157 vs predicted 1/ξ≈0.067). Kagome kernel is wrong model class → provenance credit only.
