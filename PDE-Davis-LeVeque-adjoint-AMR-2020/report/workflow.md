# Workflow — Davis & LeVeque 2020 Adjoint-AMR Replication

**Paper:** Davis & LeVeque, *Analysis and Performance Evaluation of Adjoint-Guided Adaptive Mesh Refinement for Linear Hyperbolic PDEs Using Clawpack*, ACM TOMS 2020, DOI [10.1145/3392775](https://doi.org/10.1145/3392775).
**Host:** `uicgpu01` (Ubuntu 20.04, 8×A100, 255 CPU cores, 2 TB RAM). CPU-only.
**Verdict:** REPLICATED.

## Stage 0 — provisioning

1. SSH into `uicgpu`.
2. Create Python 3.8.10 virtualenv at `~/work/pde-davis-leveque-amr/clawvenv/`.
3. `pip install numpy==1.24.4 matplotlib==3.7.5 scipy==1.10.1`.
4. Verify `gfortran` present; export `FC=gfortran FFLAGS="-O2 -fopenmp"`.

## Stage 1 — Clawpack build

```bash
cd ~/work/pde-davis-leveque-amr
git clone --depth 1 -b v5.9.2 https://github.com/clawpack/clawpack.git
cd clawpack
git submodule update --init --recursive --depth 1
export CLAW=$(pwd)
export PYTHONPATH=$CLAW
pip install -e .
```

Submodule pins (recorded):
- amrclaw @ 4b50c26
- classic @ a27a495
- clawutil @ 5aaee22
- geoclaw @ 2226769
- pyclaw @ c2b04786
- riemann @ c7a9ed0
- visclaw @ 32e257c8

## Stage 2 — 1D adjoint solve (once)

```bash
cd $CLAW/amrclaw/examples/acoustics_1d_adjoint/adjoint
make new PYTHON=$(which python)
make .output PYTHON=$(which python)
```

Produces the stored adjoint snapshots consumed by the forward runs.

## Stage 3 — 1D forward sweep

For each `(method, tol)` pair:

| Method | Tolerances |
|---|---|
| adjoint-magnitude (`flag2refine=True, use_adjoint=True, flag_richardson=False`) | 0.1, 0.01, 0.001, 0.0005 |
| Richardson (`flag_richardson=True, flag2refine=False, use_adjoint=True`) | 1e-4, 1e-5, 1e-6 |

For each:
1. Edit `setrun.py` to set method + tolerance (workaround: keep `use_adjoint=True` even for Richardson-only run — setting it False triggers a `free()` crash unrelated to physics; see `attempt_log.md`).
2. `make new PYTHON=$(which python)` — full rebuild.
3. `make .output PYTHON=$(which python)` — run.
4. Copy `fort.amr` (per-level cell-update counts) and all `fort.q00xx` frames to a run-tagged directory under `work/runs/1d/`.

Driver: `work/run_amr_sweep.sh`.

## Stage 4 — 1D functional J

`work/compute_functional_all.py`:
1. Load each run's `fort.q0030` (t=15 = final).
2. Overlay finest-available level data on a common fine grid.
3. Simpson/left-Riemann integrate `φ(x) · p(x, t_f)` with `φ(x) = exp(−50(x−1.5)²)`.
4. Emit per-run `J` and relative error vs. Richardson tol=1e-6 reference (`J_ref = 2.44403775e-2`).

## Stage 5 — 1D figures

- `evidence/fig_error_vs_work.png`: J relative error vs total L3 cell updates, log-log, adjoint (blue circles) vs Richardson (red squares).
- `evidence/fig_refinement_levels.png`: refinement level vs x at t=15, one line per method.

## Stage 6 — 2D adjoint solve (once)

```bash
cd $CLAW/amrclaw/examples/acoustics_2d_adjoint/adjoint
make new PYTHON=$(which python)
OMP_NUM_THREADS=8 make .output PYTHON=$(which python)
```

## Stage 7 — 2D forward runs

Two runs, matched physics, only flagging method differs:

1. Adjoint-magnitude: `flag2refine=True, flag2refine_tol=0.04, use_adjoint=True`.
2. Richardson: `flag_richardson=True, flag_richardson_tol=1e-3, flag2refine=False, use_adjoint=True`.

Each:
- `OMP_NUM_THREADS=8 make new PYTHON=$(which python)`
- `OMP_NUM_THREADS=8 make .output PYTHON=$(which python)`
- Capture `fort.amr` (per-level cell counts), `timing.csv` (wall clock and CPU), final `fort.q0007` frame.

## Stage 8 — 2D accuracy proxy

Compute total mass ∫∫ p(x,y,t=7) dx dy from `fort.q0007` for each run. Confirm agreement <0.4%.

## Stage 9 — 2D figures

`evidence/fig_2d_refinement.png`: refinement-level heatmap at t=7 side-by-side (adjoint left, Richardson right). Adjoint concentrates L3 in triangular region between origin and target (3.5, 0.5); Richardson refines every wave crest.

## Stage 10 — LLM verdict

`evidence/llm_judge_verdict.json`: Argo `claude-opus-4.7` fed the claims table + numerical results, returns per-claim reproduced/not-reproduced + overall verdict.

## Stage 11 — Report

`report/REPORT.md` compiled from claims table, run tables, figures, LLM verdict. `report/REPORT.tex` for typeset deliverable.

## Stage 12 — Final line

```
WAVE_RESULT set=PDE paper=PDE-Davis-LeVeque-adjoint-AMR-2020 verdict=REPLICATED
  dir=/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-Davis-LeVeque-adjoint-AMR-2020
  one_line=Independent Clawpack-5.9.2 build reproduces adjoint-AMR paper's
    central claim: adjoint-magnitude flagging uses ~62% of the L3 cell updates
    in 1D and is 5.6× cheaper (total updates), 3× faster (wall clock) than
    Richardson AMR in 2D at matched final-time mass conservation (<0.4% diff).
```

## Reproducibility notes

- The full sweep (1D 7 runs + 2D 2 runs + adjoint solves) fits comfortably in a
  single overnight interactive session on `uicgpu`.
- Total disk footprint of `work/` is a few hundred MB (dominated by `fort.q*`
  frame files).
- No GPU is used; the 8×A100 host is used purely for its 255-core CPU capacity.
- No proprietary or non-free dependencies.
