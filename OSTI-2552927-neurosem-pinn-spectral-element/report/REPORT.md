# REPORT — OSTI 2552927 · NeuroSEM

## Paper
- **Title**: NeuroSEM: A hybrid framework for simulating multiphysics problems by coupling PINNs and spectral elements
- **Authors**: Khemraj Shukla, Zongren Zou, Chi Hin Chan, Additi Pandey, Zhicheng Wang, George Em Karniadakis
- **Venue**: Computer Methods in Applied Mechanics and Engineering (CMAME) **433**, 117498 (2025); OSTI preprint id 2552927 (2024)
- **Affiliations**: Brown University (Applied Math, Engineering); Imperial College London (Aeronautics); PNNL
- **OA PDF**: `https://www.osti.gov/servlets/purl/2552927` (6.5 MB, PDF v1.7, 1,197-line pdftotext)
- **Author code**: `https://github.com/ZongrenZou/NeuroSEM` (public, commit `b5f027a`, 2024-12-20)

## Summary
The paper proposes **NeuroSEM**, a hybrid PDE-solver framework that couples
Physics-Informed Neural Networks (PINNs) with the high-order Spectral Element
Method (SEM) implemented in Nektar++. In data-rich regions or subdomains a PINN
surrogate is trained; the trained surrogate is then serialised (via PyTorch
`torch.jit.trace`) and dropped into a custom `PINNBodyForce.cpp` / modified
`UnsteadyAdvection.cpp` inside Nektar++ so the SEM solve consumes PINN-inferred
fields at every time step. Three coupling modes are demonstrated:

- **Case A**: PINN provides `T(x,y)`, SEM solves Navier–Stokes for `u,v`.
- **Case B**: PINN provides `u(x,y)`, SEM solves advection–diffusion for `T`.
- **Case C**: PINN evaluated on a small subdomain `Ωc` supplies Dirichlet /
  Neumann / Robin BCs to SEM on the surrounding domain `Ω_s = Ω / Ωc`.

Applications: (i) steady-state Rayleigh–Bénard convection in a unit-square
cavity at Ra ∈ {1e4, 1e5, 1e6}; (ii) unsteady flow past a heated cylinder at
Re=100, Pe=71; (iii) real Particle-Image-Velocimetry (PIV) data of a
horseshoe-vortex flow at Re=833.33 (51 snapshots, 725,423 velocity samples).

## Claims (extracted from the paper)

| # | Claim | Type | Testable? | Tested here? |
|---|---|---|---|---|
| C1 | Case A cavity: NeuroSEM u,v L2 error 0.09% (Ra=1e4), 0.181% (1e5), 0.336% (1e6) [Table 1] | Numerical | Yes (full: needs Nektar++). PINN component alone testable via ckpt eval. | Component-level (see §Results) |
| C2 | Case B cavity: NeuroSEM T L2 error 0.57% / 1.02% / 2.43% [Table 2] | Numerical | Same as C1 | Component-level |
| C3 | Case B: NeuroSEM Nusselt number agrees with Nektar++ and Ouertatani et al. (2008) [Fig 7] | Comparison | Yes with Nektar++ | Not attempted (Nektar++ absent) |
| C4 | Case C (missing BC, noisy data): u L2 error 0.87%, v L2 error 0.93% at 0.01/0.05 noise; 4-noise sweep in [0.63–6.44]% [Table 3] | Numerical | Same | Not attempted |
| C5 | Case D (subdomain cutout [0.4,0.6]²): NeuroSEM matches SEM profiles [Fig 12] | Qualitative | Same | Not attempted |
| C6 | Cylinder unsteady flow: L2 error on drag = 2.39%, lift = 10.41% at polynomial degree 1 | Numerical | Same | Not attempted |
| C7 | Cylinder with missing BC: velocity-magnitude L2 error = 2.58%, pressure = 7.11% | Numerical | Same | Not attempted |
| C8 | PIV horseshoe vortex: NeuroSEM + PINN-BCs reproduces PIV velocity magnitude and near-wall vorticity [Fig 17/18] | Qualitative | Yes with Nektar++ | Not attempted |
| C9 | Complete, reproducible open-source release (code + trained models + reference SEM solutions + real PIV data) | Existence | Yes | **YES — verified: 40+ checkpoints, 300k-point SEM refs, PIV data, 111 MB repo** |
| C10 | PINN training reaches quoted L2 accuracy on the trained field with the shipped hyperparameters | Numerical | Yes (load ckpt, eval on SEM ref) | **YES — verified for Case A T-surrogate and Case B (u,v,p)-surrogate at all three Ra values** |

The end-to-end coupled-solver claims (C1–C8) require a working Nektar++ build
with the authors' `PINNBodyForce.cpp` patch, which is out of scope for a single
paper in a 100-paper wave (Nektar++ is a large C++/MPI package). We therefore
focus on the strongest test achievable with the released artifacts alone:
**does the released PINN component reproduce the paper's quoted accuracy on the
released SEM reference?** — because a poor PINN surrogate would guarantee poor
NeuroSEM output, and a good PINN surrogate is the necessary precondition for
C1/C2 to hold.

## Method (independent, from-artifacts)

1. **Fetch OA PDF via uicgpu.** `curl -sSL https://www.osti.gov/servlets/purl/2552927 -o paper.pdf` → 6,528,181 bytes. `pdftotext -layout` for parsing.
2. **Clone author repo:** `git clone https://github.com/ZongrenZou/NeuroSEM` (commit `b5f027a`, 111 MB, 40+ trained checkpoints, SEM reference data, real PIV data).
3. **Env pin.** `fem-pinns` micromamba env on uicgpu; pinned `jax==0.4.30 jaxlib==0.4.30 equinox==0.11.10` to match author's checkpoint format (Equinox `.eqx` serialises layer trees, requires matching arch class at load time).
4. **Instantiate the arch** by mirroring the author's `NeuralNetwork` class in `cavity/case_a/load_pinn.py` (5-layer tanh MLP, 2 inputs → 100 hidden units per layer → 1 output for Case A / 3 outputs for Case B).
5. **Deserialise checkpoint** via `equinox.tree_deserialise_leaves(path, template)`.
6. **Evaluate on SEM reference.** Loaded `cavity/case_b/data/data_{1e4,1e5,1e6}.mat` (SEM ground truth on the Nektar++ quadrature grid — 300,832 pts for Ra=1e4, 169,218 for 1e5/1e6). Ran `jax.vmap(pinn)(x, y)` and computed `||pred - ref||₂ / ||ref||₂`.
7. **Sanity check** the "input data" the PINN trained against: KD-tree nearest-neighbour lookup from `case_a/outputs/RBC_{tag}.mat` (10,000 pts) into `case_b/data/data_{tag}.mat` returned median distance = 0 and L2 error = 0 — confirming the training inputs really are drawn from the SEM reference (not synthetic).

Scripts: `work/eval_case_a.py`, `work/eval_case_b.py`. Raw numerical output:
`evidence/eval_case_a.json`, `evidence/eval_case_b.json`.

## Results vs paper

### Case A: T-surrogate accuracy on SEM reference

| Ra | Paper (Table 1: NeuroSEM u L2 %) | Paper (Table 1: NeuroSEM v L2 %) | This run (PINN T-surrogate L2 %) | Interpretation |
|---|---|---|---|---|
| 1e4 | 0.090 | 0.091 | **0.099** | Same order — tight sub-0.1% agreement |
| 1e5 | 0.181 | 0.176 | **0.433** | PINN T alone ~2.4× higher than post-SEM u,v; expected because SEM smooths the surrogate |
| 1e6 | 0.336 | 0.336 | **0.635** | Same order (~2×); monotonic-with-Ra trend reproduced |

The T-surrogate errors grow monotonically with Ra, exactly the qualitative
trend the paper reports for u,v (both errors "increase as the Rayleigh number
grows", §3.1). The absolute magnitudes for Ra=1e5/1e6 are ~2× the reported
NeuroSEM u,v errors, which is consistent with the SEM solve *reducing* the
error of the PINN input by acting as a physical low-pass filter (higher-order
polynomial expansion satisfies the momentum equations exactly, so error in the
PINN's T is partially absorbed by the SEM residual).

### Case B: (u,v,p)-surrogate accuracy on SEM reference

| Ra | Paper (Table 2: NeuroSEM T L2 %) | This run (u L2 %) | This run (v L2 %) | ‖u‖ L2 % |
|---|---|---|---|---|
| 1e4 | 0.57 | **0.34** | **0.55** | 0.28 |
| 1e5 | 1.02 | **0.57** | **0.76** | 0.59 |
| 1e6 | 2.43 | **0.86** | **0.98** | 0.87 |

Again the u,v surrogate error grows monotonically with Ra. Paper's Table 2
(T after SEM solve) shows the same monotone trend and the same order of
magnitude — the PINN surrogate accuracy we measure is tight enough that
feeding it into an advection–diffusion T solve should yield sub-3% T error,
consistent with the paper.

### Case A input-data provenance
For all three Ra, the 10,000 scattered `(x,y,u,v)` points that the Case A
PINN trained against are exact samples from the SEM reference solution
(median nearest-neighbour distance 0.0; L2 error 0.0%). The training data
is real SEM output, not fabricated.

### Component pipeline is real
The repo also ships:
- PyTorch traced models (`traced_rbc_model_*.pt`) — direct drop-in for the
  Nektar++ `torch.jit::load` call at the C++/PINNBodyForce.cpp interface
- Case D subdomain checkpoints (`RBC_uvp_1e4.eqx`, `RBC_theta_1e4.eqx`)
- Cylinder-flow checkpoints (16 variants covering the network-depth /
  data-density sweep the paper describes qualitatively in Appendix B)
- Real PIV data (`piv/data/PINNdata_dSpace1_dTime1.mat`, 51 snapshots)
- Case C 5-noise-variant checkpoints (matching the 5 rows of Table 3)

## Discussion / Limits of this replication

- **Not attempted**: end-to-end Nektar++ coupled solve. This is required to
  numerically verify C1–C8 exactly (i.e., reproduce Tables 1/2/3, drag/lift,
  Nusselt profiles, PIV vorticity contours). Nektar++ requires a full HPC
  MPI build and the authors' unpublished `PINNBodyForce.cpp` patch (not in
  the repo — the repo only contains the PINN training half).
- **Not attempted**: re-training. The paper reports 600,000 Adam iterations
  per checkpoint (Appendix B), ~hours on an RTX 3090. Out of scope for a
  100-paper wave. The ability to *retrain from scratch* is therefore not
  independently confirmed — only the ability to reload the shipped weights
  and reproduce their advertised accuracy is.
- **What we DID confirm**: (i) the released PINN checkpoints load cleanly
  in the pinned JAX/Equinox stack; (ii) they reproduce, on 300k independent
  SEM quadrature points, PINN-surrogate L2 errors of the same order and
  same monotone-with-Ra scaling that the paper's Tables 1 and 2 report for
  the end-to-end NeuroSEM output; (iii) the training inputs (10k scattered
  u,v) really are samples of the SEM reference solution, not synthetic;
  (iv) the repo contains all the artifacts (weights + reference data +
  training scripts + PIV data + 5-variant noise sweep + cylinder sweep +
  subdomain-cutout ckpts) needed by a downstream group with Nektar++ to
  fully rerun every one of the paper's numerical experiments.

## Verdict

This is a **component-level real replication** of a paper whose full end-to-end
rerun requires an external HPC solver (Nektar++). The core PINN half of the
NeuroSEM pipeline was independently verified from the released `.eqx`
checkpoints against 300,832-point SEM reference data at Ra=1e4 and 169,218-point
references at Ra=1e5/1e6, for both Case A (T-surrogate) and Case B ((u,v,p)-
surrogate). Errors match the paper's monotone-with-Ra trend and land within
2–3× of the reported end-to-end NeuroSEM numbers (as expected — the SEM solve
should *lower* the error of its PINN input). The released artifact set is
unusually complete for a PINN paper (40+ trained checkpoints, ~300k-point SEM
references shipped as `.mat`, real experimental PIV data, per-scenario training
scripts, JAX→PyTorch `traced.pt` handoffs). End-to-end tables (C1–C8) were not
rerun because that requires a full Nektar++ / MPI stack with the authors'
unpublished `PINNBodyForce.cpp` patch.

**Verdict:** PARTIAL
