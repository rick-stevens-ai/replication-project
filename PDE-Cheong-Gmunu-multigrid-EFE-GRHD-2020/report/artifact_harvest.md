# Artifact harvest

| URL / source | Artifact | Size | Notes |
|---|---|---|---|
| https://arxiv.org/pdf/2001.05723v2.pdf | `paper.pdf` (v2, 14 Apr 2020) | 953 KB, 30 pp | Class. Quantum Grav. 37 145015. Free/OA. |
| — | `extraction/marker.md` | 2111 lines | pdftotext (poppler) on paper.pdf |
| — | `extraction/nougat.mmd` | (copy of marker) | Nougat not installed here; central corpus does not have this DOI cached. Documented as pdftotext-derived placeholder in artifacts_summary.md. |
| Independent | `work/fas_multigrid_v2.py` | 8.9 KB, ~250 LOC | Independent FAS nonlinear multigrid (NumPy). Not from Gmunu. |
| Independent | `work/spatial_order.py` | 1.0 KB | Convergence-order harness. |
| Independent | `work/plot_convergence.py` | 1.7 KB | Fig-11-analog plotting. |
| Independent | `work/llm_judge.py` | 4.8 KB | Argo judge invocation. |
| Argo `argo:claude-sonnet-4.5` @ localhost:44497 | `report/evidence/llm_judge.json` | ~2 KB | LLM-judge PARTIAL verdict, structured JSON. Free endpoint. |
| Solver output | `report/evidence/fas_convergence_v2.json` | 22 KB | Iteration histories for V1..V6 |
| Solver output | `report/evidence/spatial_order.json` | ~0.5 KB | N vs error table |
| Solver output | `report/evidence/fig11_reproduction.png` | 77 KB | Full V1..V6 curves |
| Solver output | `report/evidence/fig11_zoom.png` | 86 KB | V2..V6 zoom |

## Not harvested (attempted, unavailable)

- **Gmunu source code.** Paper abstract advertises "open-source" but no repo URL is provided in:
  - The paper itself (checked references section).
  - Corresponding author Patrick Cheong's website (kidcheong.github.io / research/research-2/).
  - GitHub search (`gmunu`, `Cheong Gmunu`, `general-relativistic multigrid`).
  - Bitbucket / GitLab searches.
  - Follow-up papers (Cheong+2021 MNRAS 508, Cheong+2026 arXiv:2510.12978 on nuclear-networks Gmunu).
  → Documented as blocking C5-C8 in failure_analysis.md.
