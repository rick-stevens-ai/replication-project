# Replication of OSTI 1864334 — NN-VMC for Light Nuclei

**Score: 3/5** — clean deuteron reproduction, honest variational upper bound for 4He.

## Results
| System | E_VMC (MeV) | Minnesota ref | Experiment | |Δ|/E_exp |
|---|---|---|---|---|
| ²H (A=2) | −2.2002 ± 0.0007 | −2.202 | −2.2246 | **1.1 %** |
| ⁴He (A=4) | −24.133 ± 0.10 | −29.94 (FY) | −28.296 | 14.7 % |

- Deuteron meets the 5 % replication target; ⁴He is a rigorous variational
  upper bound limited by ansatz expressivity (no backflow, no operator
  correlators). See `report/replication_report.pdf` for full analysis.

## Contents
- `code/vmc_nuclei.py` — PyTorch NN-VMC for A=2 (relative coord) and A=4
  (spatially-symmetric ansatz), Minnesota potential.
- `code/make_plots.py` — convergence / local-energy histograms.
- `results/*.json, *.npy, *.log` — training history, summary, final samples.
- `report/replication_report.{tex,pdf}` — LaTeX report + compiled PDF.
- `report/figs/` — PDF/PNG figures.

## How to run
```bash
# on a GPU host with PyTorch 2.x + CUDA
python code/vmc_nuclei.py --system both --out ./results
python code/make_plots.py
cd report && pdflatex replication_report.tex
```

## Hardware used
NVIDIA A100-SXM4-40GB (single GPU, host `rbdgx1`).
Wall-time: 23 s (deuteron) + 104 s (⁴He) = ~2 min total.
