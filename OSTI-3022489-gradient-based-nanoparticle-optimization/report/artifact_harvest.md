# Artifact Harvest — OSTI 3022489

Every public artifact pulled or referenced during this replication.

## Downloaded

| Artifact | URL | Local path | Size | Provenance |
|---|---|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/3022489 | `work/paper.pdf` | 7,220,621 bytes | OSTI, curl via uicgpu (2026-07-05) |
| Extracted text | (from paper.pdf via `pdftotext -layout`) | `work/paper.txt` | 1523 lines | local |

## Referenced but NOT downloaded (out of scope / prohibitive size or runtime)

| Artifact | URL / DOI | Why not pulled |
|---|---|---|
| **SUNSET dataset** (all 4 sub-collections) | Figshare DOI [10.6084/m9.figshare.25130921](https://doi.org/10.6084/m9.figshare.25130921) | Large (thousands of kMC-simulated UCNP spectra in JSON); needed only to retrain the exact hetero-GNN, which we deliberately did not do — we tested the methodology on a faithful surrogate instead. |
| **hetero-GNN model checkpoints** | Figshare DOI [10.6084/m9.figshare.27941694.v1](https://doi.org/10.6084/m9.figshare.27941694.v1) | Same reason; also depends on the paper's specific NanoParticleTools code environment. |
| **Optimized nanoparticle structures** | Figshare DOI [10.6084/m9.figshare.27973206](https://doi.org/10.6084/m9.figshare.27973206) | Not needed for methodology test. |
| **Figures 2 & 5 raw data** | Figshare DOI [10.6084/m9.figshare.29916992](https://doi.org/10.6084/m9.figshare.29916992) | Not needed. |
| **NanoParticleTools code (GNN + representations + training)** | https://github.com/BlauGroup/NanoParticleTools | Full pipeline needs SUNSET + several GPU-days; skipped. |
| **RNMC (kMC engine, NPMC tool)** | https://github.com/BlauGroup/RNMC | kMC validation of optimized structures takes months per particle per the paper; well out of scope. |
| Journal version (Nature Comp Sci) | https://doi.org/10.1038/s43588-025-00917-3 | eScholarship OSTI PDF is the OA version we used. |

## Environment provenance

- Host: CherryRd (macOS, x64)
- Python: `python3.12` from Homebrew, isolated venv at `work/venv/`
- Key package versions: `torch==2.2.2`, `numpy==1.26.4`, `scipy==1.13.1`, `matplotlib==3.11.0`
- LLM judge endpoint: Argo proxy `http://127.0.0.1:44497/v1/chat/completions`, model `argo:gpt-5.2`, key `stevens` (free endpoint per project rules).

## Produced (this replication)

| Artifact | Path | Purpose |
|---|---|---|
| Surrogate model | `work/ucnp_model.py` | Differentiable physics-motivated UCNP forward model |
| Optimizer harness | `work/optimize_compare.py` | Gradient (paper) vs random / DE / Nelder-Mead |
| Analysis + plots | `work/analyze_and_plot.py` | Convergence figure, summary CSV, sample-efficiency, design-rules check |
| Brightness ratio | `work/brightness_analog.py` | Paper's "6.5× vs training-best" analog |
| LLM judge | `work/llm_judge.py` | Scored replication via Argo gpt-5.2 |
| Optimization results | `report/evidence/opt_results.json` | Best-value + history per method per size |
| Optimization histories | `report/evidence/opt_histories.npz` | Full (calls, best) trace for each seed × method |
| Convergence figure | `report/evidence/convergence.png` | Best-so-far vs forward-model calls, 4 panels |
| Summary table | `report/evidence/summary_table.csv` | Best log10 intensity per method per n_regions |
| Sample efficiency | `report/evidence/sample_efficiency.json` | Speedup: gradient vs random-search calls-to-match |
| Best structures | `report/evidence/best_structures.json` | Per-shell radii + [Nd,Yb,Er] concentrations |
| Design-rules check | `report/evidence/design_rules_check.json` | Nd-outer / Er-inner / Yb-buffer verification |
| Brightness ratio | `report/evidence/brightness_analog.json` | ~5× (vs paper's 6.5×) |
| LLM judge output | `report/evidence/llm_judge.json` | Argo gpt-5.2 verdict, C1..C5 status, coverage % |
