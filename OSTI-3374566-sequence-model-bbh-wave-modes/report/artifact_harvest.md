# Artifact harvest — OSTI 3374566

| # | Artifact | URL / accession | Size | sha256 (first bytes) | Notes |
|---|---|---|---|---|---|
| 1 | Paper PDF (arXiv version) | https://arxiv.org/pdf/2409.03833 (v2, 2025-06-03) | 6,125,280 B | *(see work/arxiv_2409.03833.pdf)* | OSTI direct download unreachable from both driver and uicgpu; arXiv used as canonical source. Content identical to OSTI 3374566. |
| 2 | Paper text (pdftotext) | derived | 1328 lines | – | Used for claims extraction and section indexing. |
| 3 | Code repository | https://github.com/victoria-tiki/transformer_complex | 12 tracked files | – | Cited in paper as ref [29]. Cloned into `work/transformer_complex/`. |
| 4 | Trained model checkpoint | `transformer_complex/inference/model.ckpt` | 6,104,816 B | `7bf08be43792c4fea040cc1314091975b1c7f2ec85d2c5654988da05eef1d550` | The full PyTorch Lightning checkpoint (state_dict + optimizer/lr scheduler state). Loads with 0 missing / 0 unexpected keys into `create_transformer(embed_dim=80, dense_dim=80, num_heads=10)`. **This is the actual model behind the paper's headline overlaps** — enables direct replication without retraining. |
| 5 | NRHybSur3dq8 surrogate model | via `gwsurrogate.catalog.pull("NRHybSur3dq8")`, hosted on Zenodo (paper ref [21]) | 212,935,992 B | – | Downloaded to `/data/stevens/envs/gwsur/lib/python3.10/site-packages/gwsurrogate/surrogate_downloads/NRHybSur3dq8.h5`. Same surrogate the paper trained on. |
| 6 | Independent replication driver | `work/replicate.py` | ~10 KB | – | Author of this run. Generates fresh (q, sz, θ) off training grid, runs the checkpoint, computes overlaps. |
| 7 | Replication result set | `report/evidence/replicate_results.json` | – | – | 24-sample per-waveform overlaps + summary stats. |
| 8 | Replication run log | `report/evidence/replicate_run.log` | – | – | Full stdout of the successful run. |

**Not harvested (but linked in paper):**
- SXS catalog v3.0.0 — https://zenodo.org/doi/10.5281/zenodo.15415231 (multi-GB, used only for the paper's secondary OOD claim; not needed for the primary overlap claim).
- Author-hosted interactive visualisations — https://victoriatiki.com/projects/forecasting_transf/ (informational only, not needed for numerical replication).
