# Artifact harvest — Codina 2001

## Paper PDFs
| URL | Local file | Size | SHA-1 (first 12) |
|---|---|---|---|
| https://www.scipedia.com/wd/images/0/02/Draft_Samper_243095330_6381_1-s2.0-S0021999101967257-main.pdf | `work/codina2001_scipedia.pdf` | 520540 B | (see below) |
| https://www.scipedia.com/wd/images/8/85/Draft_Samper_163828847_3685_Pl_186.pdf | `work/codina2001_cimne_preprint.pdf` (CIMNE preprint 186, March 2000) | 1100126 B | (see below) |

DOI: 10.1006/JCPH.2001.6725 (J. Comput. Phys. 170(1), 112–140).
OA status per Semantic Scholar: GREEN (CC BY-NC-SA on Scipedia mirror).

## Provenance query
Semantic Scholar API v1, with keychain S2 key
(`security find-generic-password -a rick-stevens-ai -s semantic-scholar-api-key -w`):
```
GET https://api.semanticscholar.org/graph/v1/paper/DOI:10.1006/jcph.2001.6725
    ?fields=title,year,authors,openAccessPdf,externalIds
```
returned `openAccessPdf.status=GREEN` with the Scipedia URL used above.

## Code / data produced by this replication
| Path | Contents |
|---|---|
| `work/codina_replication.py` | Q1/Q1 FEM assembly + three fractional-step schemes (first-order, total_second, incremental_second) + analytical-solution convergence harness. |
| `work/cavity_run.py` | Driven-cavity Re=100 experiment at three δt values. |
| `work/make_plots.py` | Contour + bar-chart figure generation. |
| `work/llm_judge.py` | Argo GPT-5 (:44497 free endpoint) verdict request. |
| `work/convergence_results.json` | Analytical-test error table (documented as expectedly non-converging). |
| `report/evidence/cavity_results.json` | Full pressure/velocity fields + convergence residuals for all six cavity runs. |
| `report/evidence/cavity_pressure_contours.png` | 2×3 pressure-contour panel figure. |
| `report/evidence/pressure_stability_bar.png` | log10(P_std) summary bar chart. |
| `report/evidence/llm_judge_verdict.txt` | Full JSON verdict from Argo GPT-5. |
