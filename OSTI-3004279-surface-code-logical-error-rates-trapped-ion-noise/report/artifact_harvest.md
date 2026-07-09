# Artifact Harvest — OSTI 3004279

| Kind | Source URL | Local path | Size | Notes |
|---|---|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/3004279 | work/paper.pdf | 2,264,867 B (2.16 MiB) | Fetched via uicgpu (curl); CherryRd blocked from osti.gov |
| Paper text | (derived) | work/paper.txt | 118,011 B | `pdftotext -layout` on uicgpu |
| Sim code (main) | (this repo) | work/sim_surface_code.py | 7.7 KiB | 200k-shot Monte Carlo, d=3..9, two scans |
| Sim code (extended paper scan) | (this repo) | work/sim_paper_extended.py | 2.1 KiB | scale ∈ {8,10,12,14,16,20,25,30} |
| Analyze code | (this repo) | work/analyze_final.py | 4.1 KiB | Log-log interpolation crossover of curves |
| Raw results (paper Table-I) | (generated on uicgpu) | report/evidence/results_paper_stochastic.json | 9.9 KiB | 36 rows, s ∈ {0.5..8.0} |
| Raw results (paper Table-I extended) | (generated on uicgpu) | report/evidence/results_paper_stochastic_extended.json | 9.9 KiB | 32 rows, s ∈ {8..30} |
| Raw results (uniform depol) | (generated on uicgpu) | report/evidence/results_uniform_depolarizing.json | 9.0 KiB | 32 rows, p ∈ {0.001..0.02} |
| Threshold summary | (derived) | report/evidence/threshold_summary.json | ~3 KiB | Crossover + Λ table |

## External data
- **No paper-published raw data**: the paper explicitly states data are not publicly available upon publication.
- **TISCC compiler**: mentioned but open-source; not used in this replication (we simulate the abstract rotated surface code with Stim's generator).

## Software versions
- stim 1.16.0 (built-in surface-code circuit generator + detector error models)
- pymatching 2.4.0 (MWPM decoding from Stim DEMs)
- numpy 2.5.1
- Python 3.13 (miniconda3) on uicgpu
- pdftotext (poppler-utils) 22.02.0

## Compute
All Monte Carlo ran on uicgpu CPU cores (no GPU used). Total wallclock ≈ 3.5 minutes across both scans (68 grid points, 200k or 100k shots each). Nothing paid; all-free endpoints (Argo proxy 127.0.0.1:44497 with key `stevens`, model `argo:gpt-5.1`, for LLM-judge scoring only).
