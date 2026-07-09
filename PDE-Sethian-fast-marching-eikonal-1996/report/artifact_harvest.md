# Artifact harvest

| artifact | URL | size | notes |
|---|---|---|---|
| Sethian (1996) PNAS preprint PDF | http://ugweb.cs.ualberta.ca/~vis/courses/CompVis/readings/modelrec/sethian95fastlev.pdf | 356 160 B | 17-page PDF, PDF 1.2, Type-3 fonts (pdftotext garbled; pdftoppm + tesseract used to extract eqns) |
| DOI (canonical) | https://doi.org/10.1073/pnas.93.4.1591 | — | PNAS host returned HTML wrapper, not the PDF; used the Alberta mirror above |

No code from the paper was downloaded — this is a from-scratch reimplementation using only the mathematical descriptions in the paper (Eqns. 6, 8, 9 and the algorithm in Sec. 3.2 / 4.1).

Local artifacts produced (all under this directory):
- `work/sethian1996.pdf` — the paper
- `work/fmm.py` — from-scratch FMM implementation (NumPy + heapq narrow band)
- `work/experiments.py` — the three experiments (C1, C2, C3)
- `work/make_figures.py` — plotting
- `report/evidence/convergence.json` — per-grid errors + fitted order
- `report/evidence/complexity.json` — runtime vs N, power-law fit, N log N ratios
- `report/evidence/variable_speed.json` — monotone-violation count + axial-ray error
- `report/evidence/variable_speed_T.npy` — arrival-time field for the two-material case
- `report/evidence/fig_convergence.png`, `fig_complexity.png`, `fig_variable_speed.png`
- `report/evidence/run_log.txt` — captured stdout of `experiments.py`
