# Artifact harvest — OSTI 2552927 (NeuroSEM)

## Paper PDF (OSTI OA)
- URL: `https://www.osti.gov/servlets/purl/2552927`
- Downloaded via `ssh uicgpu` (CherryRd → osti.gov times out).
- Size: 6,528,181 bytes (6.5 MB). PDF v1.7. Text: 1,197 lines via `pdftotext -layout`.

## GitHub code repository
- URL: `https://github.com/ZongrenZou/NeuroSEM`
- Clone commit: `b5f027a` "Update README.md" (2024-12-20 21:30:24 -0500)
- Size on disk after clone: 111 MB, 303 tracked entries
- License: (repo default, no explicit LICENSE file present as of clone)
- Cited in paper (Section 3, first paragraph).

### Trained model checkpoints (JAX/Equinox `.eqx` + PyTorch traced `.pt`) — 40+ files
Cavity (Rayleigh–Bénard, Ra ∈ {1e4, 1e5, 1e6}):
- `cavity/case_a/checkpoints/RBC_{1e4,1e5,1e6}.eqx` + `.pt` (T-surrogate for u,v→T)
- `cavity/case_a/checkpoints/RBC_1e4_{few_data,noisy_data}.eqx` + `.pt`
- `cavity/case_b/checkpoints/RBC_{1e4,1e5,1e6}.eqx` + `.pt` (uvp-surrogate for T→u,v,p)
- `cavity/case_b/checkpoints/RBC_1e4_{2,nn}.eqx`
- `cavity/case_c/`, `cavity/case_c_revised/checkpoints/` (5 noise-variant `.eqx`)
- `cavity/case_d/checkpoints/RBC_{theta,uvp}_1e4.eqx` (subdomain cutout)

Flow past cylinder (unsteady, Re=100, Pe=71):
- `flow_past_cyl/flow_past_cyl/checkpoints/RBC_*.eqx` (16 checkpoints with varying
  data density, network depth/width, and time window)
- `flow_past_cyl/flow_past_cyl_revised/checkpoints/RBC_T_20_*.eqx` (extended-time
  variants, network 4×100 / 5×100, data density 1k/2k/3k per snapshot)

PIV horseshoe-vortex (real experimental data):
- `piv/checkpoints/PINN{,1,2}.eqx` + `traced_pinn{1,2}.pt`

### Reference data (SEM ground truth + real PIV)
- `cavity/case_b/data/data_{1e4,1e5,1e6}.mat` — SEM reference u,v,theta on
  quadrature points (300,832 for Ra=1e4; 169,218 for Ra=1e5/1e6)
- `cavity/case_a/outputs/RBC_{1e4,1e5,1e6}.mat` — the 10,000 scattered (x,y,u,v)
  points Case A used as PINN training input (verified drawn from SEM ref)
- `cavity/case_b/outputs/uv_grid_{1e4,1e5,1e6}.mat` — 100×100 grid PINN
  predictions used for figures
- `cavity/case_d/outputs/data.mat` — subdomain data
- `flow_past_cyl/*/data/train.mat` — cylinder SEM training snapshots
- `piv/data/PINNdata_dSpace1_dTime1.mat`, `PINNdata_grids.mat`,
  `gauss_quad.mat`, `output{1,2}.mat` — real PIV dataset (51 snapshots,
  725,423 velocity data points per paper §3.3)

### Author-generated figures
- Streamline plots for all Ra in `cavity/case_{a,b,c_revised}/outputs/*.png`
- Cylinder wake plots in `flow_past_cyl/*/outputs/*.png` (`sem.png`, `pinn.png`,
  `error.png`, `l2s.png`, `mses.png`)

### Code
- Per-case training scripts (`rbc_pinn.py`, `rbc_pinn_few_data.py`,
  `rbc_pinn_noisy_data.py`, etc.)
- `load_pinn.py` in each case dir (checkpoint-loading + eval script the
  authors ship — I mirrored this behaviour in my `eval_case_{a,b}.py`)
- `from_eqx_to_torch.py` / `from_eqx_to_pt.py` (JAX→PyTorch conversion for
  Nektar++ integration via `torch.jit.trace`)

## Cited but NOT co-released
- Nektar++ v5.x — the SEM solver. Available at `nektar.info`; large C++/MPI
  package; not exercised in this replication (would require full HPC build).

## My reproduction artifacts (also in `evidence/` and `work/`)
- `paper.pdf` (from OSTI)
- `eval_case_a.py`, `eval_case_b.py` — the evaluation scripts
- `eval_case_a.json`, `eval_case_b.json` — numerical output
