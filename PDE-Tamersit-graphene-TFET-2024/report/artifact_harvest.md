# Artifact Harvest — Tamersit 2024

| Artifact | URL | Size / checksum | Notes |
|---|---|---|---|
| Paper PDF (OA CC-BY) | https://europepmc.org/articles/PMC10821285?pdf=render | 3.76 MB, 10 pages | MDPI direct blocked by Akamai; PMC ID PMC10821285 |
| Paper full text (pdftotext -layout) | (local) `work/paper.txt` | 1,652 lines | All figures' captions + inset text recovered |
| Semantic Scholar record | `https://api.semanticscholar.org/graph/v1/paper/DOI:10.3390/nano14020220` | JSON | paperId `e630a0a706c34ba84103e4cfbeac81ffba6f05fd`; PubMed 38276738 |
| Source code (author's MATLAB simulator) | **NOT PUBLIC** — "available from the first-corresponding author (K.T.) upon reasonable request" | — | Data Availability Statement in the paper |
| Referenced NEGF recipe #47 (Zhao-Guo 2009) | J. Appl. Phys. 105 034503 | (upstream cited) | The main methodological reference the paper builds on |
| Referenced Sarkar 2013 (TFET gas-sensor foundation) | Appl. Phys. Lett. 102 023110 | (upstream cited) | Provides the ΔΦ ↔ gas-pressure translation used by paper |
| Our re-implementation | `work/negf_gnr_tfet.py` | 466 lines, ~14 KB | Independent Python re-implementation of the paper's Appendix A recipe (single-band mode-space simplification) |
| Analytical spot-checks | `work/analytical_checks.py` | 120 lines | Bandgap, effective mass, SS limit, Landauer G0, sensitivity |
| Transfer-curve JSONs | `report/evidence/transfer_baseline.json`, `transfer_gas_scan.json` | ~35 KB each | 5 sweeps × 25 V_GS points |
| Transfer-curve plot | `report/evidence/transfer_curves.png` | ~90 KB | Baseline + 4 gas-shift curves |
| Analytical checks log | `work/analytical_checks.log` | ~2 KB | printed summary |
| Metrics log | `work/transfer_metrics.log` | ~2 KB | Selectivity + peak-current tables |
| NEGF run log | `work/negf_run.log` | ~15 KB | Full sweep console output |

## Public code that would have helped (not present on this machine)
- **NanoTCAD ViDES** (Fiori, Iannaccone) — free Fortran/Python NEGF for AGNRs, but requires build; not attempted in this time window.
- **KWANT** — general quantum-transport Python lib; would need AGNR-TFET geometry + BTBT setup written by hand.
- Neither is installed on `uicgpu` per `python3 -c "import kwant"` (module not found).
