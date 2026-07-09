# Artifact Harvest — OSTI 3025402

| # | Type | URL / accession | Size | Notes |
|---|------|----------------|------|-------|
| 1 | Paper PDF | https://www.osti.gov/servlets/purl/3025402 | 8,711,326 bytes | 33-page preprint. Fetched 2026-07-04 via uicgpu (local network could not reach osti.gov). Saved to `work/paper.pdf` and `work/paper.txt` (pdftotext extract, 2493 lines). |
| 2 | Author code repo | https://github.com/Centrum-IntelliPhysics/Physics-Informed-Latent-DeepONet | 263 files | Cloned to `/tmp/pi-latent-no-repo` on uicgpu 2026-07-04. Contains four `Examples/` dirs (1D_Diffusion-reaction-dynamics, 1D_Burgers, 2D_Burgers, 2D_Stove) each with a_Vanilla-NO.ipynb / b_Latent-NO.ipynb notebooks plus post-processing. Framework: JAX. We did **not** run the author code; our replication is an independent PyTorch reimplementation from the paper's equations and Table 2, so any agreement is not confounded by shared code paths. |
| 3 | Ground-truth solver | (independent) | — | Explicit finite-difference solver in `work/pi_latent_no_dr.py::solve_reaction_diffusion`. Second-order central differences in x, forward Euler in t with sub-stepping for CFL, Dirichlet-zero BCs. Not shared with the paper's solver. |
| 4 | GP source sampler | (independent) | — | Cholesky sampler with paper's kernel k(x,x') = σ² exp(-|x-x'|²/(2ℓ²)) with ℓ=0.2, σ=1.0 (Table 1). |

## No paywalled/private data required
All data (source functions s(x), ground-truth solutions u(t,x)) is synthesized locally per the paper's specification.
