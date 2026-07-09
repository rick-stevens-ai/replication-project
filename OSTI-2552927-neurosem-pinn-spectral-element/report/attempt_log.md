# Attempt log — OSTI 2552927 (NeuroSEM)

## 2026-07-02 07:20 CDT (agent: OpenClaw subagent, model argo/argo:claude-opus-4.7, host uicgpu)

1. **Fetch paper OA PDF.** CherryRd cannot reach osti.gov (per brief). SSH'd to
   `uicgpu`, ran `curl -sSL -o paper.pdf https://www.osti.gov/servlets/purl/2552927`.
   Got `6,528,181` bytes, PDF v1.7. Extracted 1,197-line text with `pdftotext -layout`.
2. **Identify quantitative claims.** Read the paper end-to-end; catalogued
   Table 1 (Scenario A u,v L2 error), Table 2 (Scenario B T L2 error),
   Scenario C 4-noise-level table, Scenario D subdomain cutout errors,
   flow-past-cylinder lift/drag errors, PIV horseshoe-vortex velocity/pressure
   errors. All claims listed in REPORT.md.
3. **Locate authors' code repo.** Paper says code released on acceptance at
   `github.com/ZongrenZou/NeuroSEM`. Cloned it — repo is public (commit
   `b5f027a`, "Update README.md", 2024-12-20). 111 MB, ships JAX/Equinox
   `.eqx` checkpoints AND PyTorch traced `.pt` models AND SEM reference
   `.mat` (~300k quad-pts) AND real PIV data.
4. **Set up Python env on uicgpu.** Located existing `fem-pinns` micromamba env
   at `/data/stevens/micromamba/envs/fem-pinns`. Had jax 0.10.2 (too new for
   the checkpoints — segfault at import). Pinned `jax==0.4.30 jaxlib==0.4.30
   equinox==0.11.10` (matches the paper's training era). Confirmed load OK.
5. **Reproduce Case A T-surrogate.** Wrote `eval_case_a.py`: load
   `cavity/case_a/checkpoints/RBC_{1e4,1e5,1e6}.eqx` (5-layer 100-unit tanh MLP,
   2→100→100→100→100→1, temperature surrogate), evaluate on the SEM reference
   `x,y,theta` at 300,832 (Ra=1e4) or 169,218 (Ra=1e5/1e6) quadrature points,
   compute L2 relative error. Results in `evidence/eval_case_a.json`.
6. **Reproduce Case B (u,v,p)-surrogate.** Loaded `cavity/case_b/checkpoints/
   RBC_{1e4,1e5,1e6}.eqx` (5-layer 100-unit tanh MLP, 2→…→3 for u,v,p),
   evaluated at SEM reference u,v on same 300k / 169k point clouds. Results
   in `evidence/eval_case_b.json`.
7. **Cross-check "input data" claim.** The `case_a/outputs/RBC_{tag}.mat`
   holds the 10,000 (u,v) samples Case A trained on. Nearest-neighbour lookup
   against `case_b/data/data_{tag}.mat` (SEM ref) returned median distance
   0.0 and 0.0% L2 error — confirming the training inputs really are drawn
   from the SEM solution (no fake data).
8. **What I did NOT run.** Nektar++ SEM solve is not installed on uicgpu and
   is out of scope for one paper in a 100-paper wave (Nektar++ is a large C++
   spectral-element package requiring a full MPI/hpc build). Therefore the
   final end-to-end Table 1/2 NeuroSEM errors are not directly rerun; instead
   we verified the PINN component that feeds Nektar++.

### Compute
- All numerics on `uicgpu` (JAX CPU, no GPU needed — the eval sweeps ~300k
  points in <1s per checkpoint). No LLM tokens burned on inference — only on
  the final judge (Argo Opus 4.7, free).
