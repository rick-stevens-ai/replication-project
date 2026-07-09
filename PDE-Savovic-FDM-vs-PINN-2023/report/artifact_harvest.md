# Artifact Harvest — Savović 2023

| Artifact | Source URL | Size | Notes |
|---|---|---|---|
| Paper PDF | https://mdpi-res.com/d_attachment/axioms/axioms-12-00982/article_deploy/axioms-12-00982.pdf?version=1697606956 | 6.96 MB | MDPI CDN direct; main URL (`www.mdpi.com/.../pdf`) is Akamai-blocked. |
| Paper DOI landing | https://doi.org/10.3390/axioms12100982 | — | Open-access, CC-BY 4.0. |
| Semantic Scholar record | https://www.semanticscholar.org/paper/A-Comparative-Study-of-the-Explicit-Finite-Method-Savovi%C4%87-Ivanovic/b855b5e7a04b9e1905fa7334e59c9ffa4f138395 | — | Metadata cross-check. |
| Extracted text | `work/savovic_2023.txt` | 44 KB | `pdftotext -layout` output. |

## Referenced but not fetched
| Reference | Why | Notes |
|---|---|---|
| Cole 1951, Wood 2006 | Provided the analytical solutions (Eqs 13, 21, 28) we reimplemented. | Standard textbook Cole–Hopf; no need to fetch. |
| DeepXDE (Lu et al. 2021) | Paper's PINN library. | We used raw PyTorch to keep the replication independent of DeepXDE's own vectorization. |

## Data / code produced
| File | Purpose |
|---|---|
| `work/fdm_burgers.py` | Explicit FDM + Cole–Hopf analytical solutions, all 18 (ν,T) cases |
| `work/pinn_burgers.py` | PyTorch PINN, 3×20 tanh, 5560 collocation, Adam+L-BFGS |
| `work/build_comparison.py` | Merges FDM+PINN JSON, formats table, calls Argo judge |
| `work/fdm_results.json` | 18 EFDM RMSEs + paper values |
| `work/pinn_results.json` | 18 PINN RMSEs + train wall-time |
| `work/pinn_full.log` | Full training log on uicgpu |
| `report/evidence/comparison.csv` | Side-by-side table (paper vs ours, EFDM & PINN) |
| `report/evidence/comparison.json` | Same, JSON |
| `report/evidence/llm_judge.txt` | Full prompt + Argo GPT-5.2 verdict |
