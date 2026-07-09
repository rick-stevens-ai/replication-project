# Attempt Log — PDE-Davis-LeVeque-adjoint-AMR-2020

Timezone: America/Chicago. Runner: OpenClaw subagent, session `agent:main:subagent:9b8e8da6-4a79-47a8-a567-0691a5a548ec`.

## 2026-07-04 08:09 — Setup
- Read wave brief. Created `~/Dropbox/REPLICATE-PROJECT/PDE-Davis-LeVeque-adjoint-AMR-2020/{report,work}` skeleton.
- Confirmed target dir empty (only `.DS_Store`); no sibling pollution risk.
- Pulled S2 metadata for DOI 10.1145/3392775 → confirmed title "Analysis and Performance Evaluation of Adjoint-Guided Adaptive Mesh Refinement for Linear Hyperbolic PDEs Using Clawpack" by B. N. Davis & R. LeVeque (2018 arXiv/2020 ACM TOMS). arXiv preprint 1810.00927.
- Downloaded arXiv PDF (5.1 MB) → `work/davis_leveque_2020.pdf`.

## 08:10 — Environment on uicgpu
- SSH uicgpu OK (uicgpu01, 255 cores).
- Created `~/work/pde-davis-leveque-amr/`; created Python 3.8 venv `clawvenv`.
- `pip install clawpack==5.9.2` → installs Python bindings only, NO examples/data.
- pip's clawpack loc: `/home/stevens/work/pde-davis-leveque-amr/clawvenv/lib/python3.8/site-packages/clawpack/`.
- Verified `import clawpack` works, version 5.9.2.

## 08:11 — Full Clawpack source + submodules
- `git clone --depth 1 -b v5.9.2 https://github.com/clawpack/clawpack.git` (7 submodules: amrclaw, classic, clawutil, geoclaw, pyclaw, riemann, visclaw at their pinned v5.9.2 hashes).
- Found paper-referenced examples: `amrclaw/examples/acoustics_1d_adjoint/` and `amrclaw/examples/acoustics_2d_adjoint/` (both with `adjoint/` subdir for adjoint solve). README explicitly says "similar to the problem in Example 3 of the paper" (README wording — but 1D example parameters match Example 1 setup).

## 08:12 — 1D adjoint run
- Built adjoint problem in `adjoint/` subdir: `make new` OK with `gfortran -O2 -fopenmp` (warnings about F2018 deprecated `do 10` termination, no errors).
- `make .output` initially failed: Makefile invokes bare `python setrun.py` which resolved to /usr/bin/python (no numpy). Fixed by `pip install numpy matplotlib scipy` in venv, then invoking `make .output PYTHON=$(which python)`.
- Adjoint solve completed: 30 frames, 15s tfinal, 4 threads, 0.019s total wall time.
- Forward problem with adjoint flagging (tol=0.01, use_adjoint=True): completed 30 frames, 0.094s wall time, 157,452 total cell updates (2700/24992/129760 at levels 1/2/3).

## 08:13 — Attempted standard-flagging comparison (initial)
- Copied 1D example to `acoustics_1d_standard/`, set `use_adjoint=False`. Build succeeded.
- Ran → **SIGABRT / free(): invalid pointer** at "there are 1 grids with 30 cells at level 1". Root cause: with `use_adjoint=False`, adjoint.data still gets written with `innerprod_index=None`, and the adjoint_module allocator crashes on subsequent grid creation. Not worth patching the Fortran; instead switched comparison to `flag_richardson=True, flag2refine=False, use_adjoint=True` which keeps the aux/adjoint bookkeeping intact but performs Richardson error estimation for flagging (the paper's "error-flagging" method §5).

## 08:14 — 1D sweep script
- Wrote `run_amr_sweep.sh`: iterates 4 adjoint tolerances (0.1, 0.01, 0.001, 0.0005) and 3 Richardson tolerances (1e-4, 1e-5, 1e-6). Each writes its own `_output` snapshot, all output archived under `~/work/pde-davis-leveque-amr/sweep/`.
- Transport gotcha: /tmp on OpenClaw sandbox ≠ /tmp on uicgpu; used stdin-pipe (`cat file | ssh uicgpu 'cat > dest'`) as the transfer path. Also had to swap `bc` (missing) for python arithmetic in wall-time capture.
- Sweep completed cleanly (all 7 runs). Results parsed by `parse_results.py` → `sweep/results_parsed.csv`.

## 08:15 — Functional-of-interest computation
- Read `adjoint/qinit.f`: adjoint IC is `p_hat(x, t_final) = exp(-50*(x-1.5)^2)`, so functional weight `phi(x) = exp(-50*(x-1.5)^2)`, alpha=1, x_p=1.5, beta_hat=50 (Example 1 form).
- Wrote `compute_functional_all.py`: parses AMRClaw ASCII fort.q0030 for each run, builds a fine-grid overlay picking highest-level q at each x, computes J = sum(phi*p*dx).
- Reference J (Richardson tol=1e-6) = 2.44403775e-02. All converged runs land within 5e-5 absolute of this; adjoint tol=0.01 hits rel_err = 1.01e-3.

## 08:16 — 1D plotting
- Generated 3 diagnostic plots on uicgpu (matplotlib 3.7.5 in venv):
  - `fig_error_vs_work.png` — J relative error vs L3 cell updates (log-log), adjoint and Richardson series with tolerance labels.
  - `fig_pressure_snapshots.png` — pressure p(x, t=15) for best-of-each method, with target weight overlay.
  - `fig_refinement_levels.png` — refinement level along x showing spatial extent of L3 coverage.
- Copied PNGs + parsed CSVs to `report/evidence/`.

## 08:17 — 2D example (paper's Example 3 analog)
- Built and ran `acoustics_2d_adjoint/adjoint/`: 20 frames, tfinal=7, 8 threads, ~8s wall time.
- Ran forward with adjoint flagging (tol=0.04): 0.856s wall, 4.696s CPU, 1,174,420 total cell updates (212500/249008/712912 at L1/L2/L3), archived `_output_adjoint_tol0.04`.
- Reran with Richardson flagging (tol=1e-3, flag2refine=False): 2.545s wall, 7.668s CPU, 6,637,780 total cell updates (212500/850400/5574880). Archived `_output_richardson_tol1e-3`.
- Both matched final total mass at t=7 within 0.4% (adjoint −0.14886, richardson −0.14935). Ratio: adjoint uses 5.65× fewer total cell updates, 7.82× fewer L3 updates, and is 2.97× faster in wall clock.

## 08:19 — 2D plotting
- Wrote `plot_2d.py` (2D fort.q parser included). Generated `fig_2d_refinement.png` (side-by-side cell-by-level rectangle map) and `fig_2d_pressure.png` (pressure field). Snapshot cell counts at t=7: adjoint 6,264 total cells (1+1+4 grids by level); Richardson 28,632 total cells (1+4+16 grids) — 4.57× snapshot reduction.
- Copied fort.amr and timing.csv from both 2D runs to `report/evidence/`.

## 08:20 — LLM judge
- POSTed replication summary to Argo (http://localhost:44497/v1/chat/completions, model=argo:claude-opus-4.7, key=stevens) with all four extracted claims and full evidence tables.
- Judge returned strict JSON: verdict=REPLICATED (high confidence), all 4 claims reproduced. Saved to `evidence/llm_judge_verdict.json`.
- Caveats flagged: (a) Clawpack v5.9.2 not the paper's version, (b) 1D reference is Richardson tol=1e-6 not analytical, (c) 2D "accuracy" compared via mass not J, (d) only one 2D tolerance pair tested, (e) adjoint-error variant not separately tested.

## 08:20 — Reports written
- `report/REPORT.md` (main report), `report/brief.md`, `report/attempt_log.md` (this file), `report/artifact_harvest.md`.
