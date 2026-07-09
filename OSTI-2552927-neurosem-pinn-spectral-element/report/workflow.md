# Workflow — OSTI 2552927 NeuroSEM Replication

Chronological record of the replication pipeline. All steps executed on
`uicgpu` (8×A100) unless noted.

## Stage 0 — Paper acquisition
1. `curl -sSL https://www.osti.gov/servlets/purl/2552927 -o paper.pdf`
   → 6,528,181 B, PDF v1.7.
2. `pdftotext -layout paper.pdf paper.txt` → 1,197 lines.
3. Register paper metadata: CMAME 433, 117498 (2025); authors Shukla, Zou,
   Chan, Pandey, Wang, Karniadakis; Brown + ICL + PNNL affiliations.

## Stage 1 — Repo acquisition
1. `git clone https://github.com/ZongrenZou/NeuroSEM` (commit `b5f027a`,
   2024-12-20).
2. Repo size: 111 MB. Inventory:
   - 40+ trained checkpoints (`.eqx` for JAX/Equinox, `.pt` traced for
     PyTorch/Nektar++)
   - Reference SEM data (`.mat`, 300,832 pts at Ra=1e4; 169,218 pts at
     Ra=1e5/1e6)
   - Real PIV data (`piv/data/PINNdata_dSpace1_dTime1.mat`, 51 snapshots,
     725,423 velocity samples)
   - Per-scenario training scripts
   - 5-variant noise sweep for Case C
   - 16 cylinder-flow checkpoints (depth × data-density sweep)

## Stage 2 — Environment
1. Create `fem-pinns` micromamba env on uicgpu.
2. Pin critical libs: `jax==0.4.30`, `jaxlib==0.4.30`,
   `equinox==0.11.10`. (Equinox `.eqx` requires a matching arch class at
   load time; version drift silently truncates weights.)
3. Standard scientific stack: `numpy`, `scipy`, `h5py` (for `.mat`),
   `scikit-learn` (KD-tree for provenance check).

## Stage 3 — Arch recovery
1. Read author's `cavity/case_a/load_pinn.py`; mirror the `NeuralNetwork`
   Equinox class exactly:
   - 5-layer MLP
   - `tanh` activation
   - 2 inputs (x, y)
   - 100 hidden units per layer
   - 1 output for Case A (T-surrogate) / 3 outputs for Case B (u, v, p)
2. Build a template `pytree` matching that class; hand to
   `equinox.tree_deserialise_leaves(path, template)`.

## Stage 4 — Component evaluation
1. `work/eval_case_a.py`: for each Ra ∈ {1e4, 1e5, 1e6}:
   - Load `case_a/checkpoints/RBC_theta_{tag}.eqx`.
   - Load SEM reference `case_b/data/data_{tag}.mat` (Nektar++ quadrature
     grid).
   - `jax.vmap(pinn)(x, y)` → predicted T on all reference points.
   - Compute L2 relative error vs reference T column.
   - Dump result to `evidence/eval_case_a.json`.
2. `work/eval_case_b.py`: analogous, but load `RBC_uvp_{tag}.eqx` and
   compare u, v, p (three outputs) against reference u, v.

## Stage 5 — Provenance sanity check
1. For Case A, load 10,000 scattered `(x,y,u,v)` training inputs from
   `case_a/outputs/RBC_{tag}.mat`.
2. KD-tree nearest-neighbour lookup into the SEM reference
   `case_b/data/data_{tag}.mat`.
3. Median distance = 0.0; L2 error = 0.0 → training data really is drawn
   from the SEM reference, not fabricated.

## Stage 6 — Comparison to paper tables
1. Cross-tabulate our measured PINN-surrogate L2 errors against paper
   Tables 1 (Case A NeuroSEM u,v) and 2 (Case B NeuroSEM T).
2. Confirm monotone-with-Ra scaling; confirm absolute magnitudes within
   2–3× of end-to-end NeuroSEM (consistent with SEM smoothing).

## Stage 7 — Report emission
1. Write `report/REPORT.md` (this pipeline's canonical markdown).
2. Emit auxiliary reports:
   - `REPORT.tex` (LaTeX + genuine critique)
   - `open_questions.json` (5 unresolved questions)
   - `workflow.md` (this file)
   - `artifacts_summary.md`
   - `failure_analysis.md`

## Not attempted (scope-limited)
- Nektar++ build + coupled solve (Tables 1–3, drag/lift, Nusselt, PIV
  vorticity). Requires unpublished `PINNBodyForce.cpp` patch.
- Retraining from scratch (600k Adam iters × 40+ checkpoints).
- Case C noise-sweep checkpoint reload.
- Cylinder-flow variant sweep.
- PIV data provenance audit.

## Host / compute
- Primary: `uicgpu` (8×A100).
- Env: `fem-pinns` micromamba.
- All artifacts on Dropbox at
  `~/Dropbox/REPLICATE-PROJECT/OSTI-2552927-neurosem-pinn-spectral-element/`.
