# Artifact Harvest — OSTI 3023992

| # | Source | URL / accession | Bytes | Local path | Notes |
|---|--------|-----------------|------:|------------|-------|
| 1 | OSTI PDF | https://www.osti.gov/servlets/purl/3023992 | 1,443,341 | `work/paper.pdf` | Full paper; downloaded on uicgpu (CherryRd cannot reach osti.gov), copied via scp |
| 2 | Author code repo | https://github.com/jhughes3/-hitl-bo | — | not cloned | Referenced only; not required for this in-silico reproduction of the physics + BO logic |
| 3 | Author Zenodo | https://doi.org/10.5281/zenodo.18805553 | — | not fetched | Same code + data + Jupyter notebooks; not required |
| 4 | Reference blend study | Newby et al. (ref 37) | — | not fetched | Paper's own grid-based baseline; we implemented Newby-style 7-comp grid ourselves |
| 5 | Reproducer source | `work/fh_bo_repro.py` | 17.7 KB | local | Full FH + Matérn-3/2 GP + custom acquisition + FH-prior refit; from scratch |
| 6 | Reproducer sweep | `work/efficiency_sweep.py` | 3.1 KB | local | Budget sweep 5→104 samples |
| 7 | Reproducer output | `report/evidence/results.json` | 4.8 KB | local | All headline numbers |
| 8 | Efficiency-sweep output | `report/evidence/efficiency_sweep.json` | 2.1 KB | local | Per-budget RMSE for BO / random / grid |
| 9 | Figure | `report/evidence/phase_boundary.png` | 51 KB | local | BO posterior boundary vs analytic FH spinodal |
| 10 | LLM judge raw | `report/evidence/llm_judge_raw.json` | 716 B | local | argo:claude-sonnet-4.6 verdict (PARTIAL, scores 4/4/4/1) |
