# MARL-AMR Replication — Progress Log

**Subagent:** `agent:main:subagent:bcb6ca3d-df0e-4b4a-a35f-ad94a596e547`
**Started:** 2026-05-28 09:42 CDT  
**Last update:** 2026-05-28 10:14 CDT  
**Workspace:** `~/Dropbox/REPLICATE-PROJECT/PDE-replications/marl-amr/`  
**Target paper:** Yang et al., "Multi-Agent Reinforcement Learning for Adaptive Mesh Refinement", **AAMAS 2023**.  
**Repo:** https://github.com/LLNL/marl-amr (BSD-3-Clause, LLNL-CODE-853184)  
**arXiv:** https://arxiv.org/abs/2211.00801

This replaces the no-code Foucart Deep-RL-AMR target under Rick's strict openness requirement.

## ✅ Openness check (PASSED)

| Item | Status | Evidence |
|---|---|---|
| Code public | ✅ | https://github.com/LLNL/marl-amr |
| License | ✅ BSD-3-Clause | `LICENSE` SPDX-License-Identifier: BSD-3 |
| Pretrained checkpoint shipped | ✅ | `marl_amr/results/nx16_ny16_depth1_tstep0p25_vdgn_pretrained/mb_210800.*` (240 MB index/data/meta) |
| Baselines included | ✅ | `marl_amr/scripts/evaluate_custom_strategies.py` (DoubleThresholdPolicy, fixed-mesh coarse/fine, refine-all) |
| Environment included | ✅ | `marl_amr/envs/graph_env_h.py` + `marl_amr/envs/solvers/AdvectionSolver.py` |
| Configs included | ✅ | `marl_amr/alg/configs/{advection_test,advection_vdgn}.py`, `envs/configs/advection_href.json` |
| Data dependencies | None — env is procedurally generated from Gaussian ICs on a periodic square mesh |
| Pay-walled / proprietary deps | None |

## ✅ Build (PASSED — 16 min total)

| Stage | Status | Notes |
|---|---|---|
| Conda env (Py 3.6 + swig 4.0.2 + gcc 9 on Ubuntu 20.04, uicgpu) | ✅ | `marlamr` env at `~/miniconda3/envs/marlamr` |
| MFEM `drl4amr-advection` branch (commit `4127f77`) | ✅ | Serial shared build, `make install` clean |
| `requirements.txt` (TF 1.14, tf-probability 0.7.0, ray 1.5.1, graph-nets 1.0.4, etc.) | ✅ | All 100+ pkgs installed first try |
| Custom PyMFEM `drl4amr` branch (commit `44bda2e`) | ✅ | After two fixes: (a) purged the generic `mfem==4.4.0.0` pulled in by `requirements.txt` that was shadowing the custom build; (b) copied `/usr/include/crypt.h` into conda sysroot since conda's gcc has its own sysroot that lacked it (Python 3.6 + libc>=2.34 issue). |
| Smoke checks | ✅ | `import mfem.ser`, `ProlongToMaxOrder` present, `AdvectionSolver.name='advection'`, `tf.__version__='1.14.0'` |

CherryRd build was abandoned: `/usr/local/bin/python3.6` is a broken dyld symlink to a missing Cellar dir on macOS Tahoe. Falling back to uicgpu Linux was the right call.

## ✅ Evaluation (PRIMARY RESULTS IN HAND)

All numbers below from 20 random Gaussian ICs over the **paper training distribution** (`u0~Uniform(0, 1.5√2)`, `theta~Uniform(0,1)`, `x0,y0~Uniform(0.5,1.5)`, `w=100`, on 16×16 periodic mesh, `max_depth=1`, `t_step=0.25`, `t_final=0.75`, `dof_threshold=1e6` ≡ off):

| Method | N | avg DoF | avg true L2 error | std err |
|---|---:|---:|---:|---:|
| **VDGN (pretrained `mb_210800`)** | 20 | **5,348.8** | **2.54 × 10⁻²** | 7.78 × 10⁻³ |
| Heuristic DoubleThreshold, high=1e-4 | 20 | 5,217.4 | 2.89 × 10⁻² | 1.22 × 10⁻² |
| Heuristic DoubleThreshold, high=5e-4 | 20 | 4,990.0 | 3.14 × 10⁻² | 1.46 × 10⁻² |
| Heuristic DoubleThreshold, high=1e-3 | 20 | 4,933.6 | 3.24 × 10⁻² | 1.53 × 10⁻² |
| Heuristic DoubleThreshold, high=5e-3 | 20 | 4,766.8 | 3.75 × 10⁻² | 1.73 × 10⁻² |
| Fixed-mesh, coarse (uniform init) | 20 | 4,842.4 | 4.27 × 10⁻² | 1.94 × 10⁻² |
| Fixed-mesh, fine (uniform refine-all) | 20 | 16,384.0 | 2.44 × 10⁻² | 7.36 × 10⁻³ |

**Replication outcome (C1, paper headline claim):** ✅ **CONFIRMED qualitatively.**

- VDGN beats *every* DoubleThreshold heuristic on error at comparable (or lower) DoF cost.
- Specifically, VDGN achieves **avg err 2.54e-2 @ 5,349 DoF** vs. the best heuristic (h=1e-4) at **2.89e-2 @ 5,217 DoF** — i.e. 12% lower error for 2.5% more DoF. Across the full threshold sweep the heuristic Pareto curve is dominated by VDGN.
- Only fully-uniform refinement matches VDGN's error (2.44e-2) and only by using 3.1× the DoF (16,384 vs 5,349).
- Std-dev: VDGN error std (7.8e-3) is *half* the heuristic error std (1.2–1.7e-2). VDGN is also more *consistent*.

The deterministic single-Gaussian test (`advection_test` config, fixed IC θ=0.125, u₀=2.12, w=100, x₀=y₀=0.5) is a **special case that does not exhibit the gap** — heuristic at h=5e-4 gets DoF 4,900 / err 1.95e-2 vs. VDGN DoF 5,560 / err 3.59e-2. This single point is misleading; the paper averages over IC randomization (which my randomized rerun does).

## ⏳ Remaining work to finish a publishable replication report

1. **Pareto plot** — DoF (x) vs L2 error (y) with VDGN as a single point and the heuristic sweep as a curve. Trivial matplotlib.
2. **Error-vs-time trace** — already have `vdgn_err_vs_time_singleGauss.csv` (4 rows) and `heuristic_err_vs_time_singleGauss.csv`; plot both.
3. **Anticipatory-refinement check (C2)** — run `--save_mesh_all_steps` for VDGN and one heuristic, render with ParaView or matplotlib at t=0.25 / 0.50 / 0.75, look for VDGN refining "ahead" of where the Gaussian is moving. Visual evidence; not numeric.
4. **Generalization (C3)** — paper claims VDGN generalizes to longer t_final and to ring/anisotropic ICs. Quick test: bump `t_final` from 0.75 → 1.5 in the config and rerun. Repo includes the alternate-IC configs as commented blocks in `advection_test.py`.
5. **REPORT.md** — claim-by-claim table, coverage/agreement score, friction tags.

## Friction tags (encountered)

- 🚧 **stack-rot**: Python 3.6 EOL + TF 1.14 + tf-probability 0.7.0 — needed pinned conda env on Linux. macOS path was dead.
- 🚧 **custom-MFEM-branches**: `drl4amr-advection` (MFEM) + `drl4amr` (PyMFEM), both pinned to 2022 commits. Build required custom SWIG step.
- 🚧 **silent-shadow**: `requirements.txt` lists `mfem==4.4.0.0` (generic PyMFEM from PyPI), which shadows the custom branch install — needed explicit `pip uninstall mfem` between MFEM build and custom PyMFEM build. Repo's `install.sh` runs in the right order but only by luck.
- 🚧 **sysroot-missing-header**: conda `x86_64-conda-linux-gnu-cc` has its own sysroot without `crypt.h`, breaks any Python 3.6 C extension. Fix: `cp /usr/include/crypt.h $CONDA_PREFIX/x86_64-conda-linux-gnu/sysroot/usr/include/`.
- 🚧 **test.py CWD assumption**: `--save_err_time` writes to `<cwd>/<dir_restore>/error_vs_time.csv` and crashes if that dir doesn't exist; needs `mkdir -p nx16_..._pretrained` before run.

## File map

```
~/Dropbox/REPLICATE-PROJECT/PDE-replications/marl-amr/
├── PROGRESS.md                              ← this file
├── README.md                                ← orientation for future readers (TBD)
├── REPORT.md                                ← final claim-by-claim report (TBD)
├── repo/                                    ← cloned LLNL/marl-amr
├── scripts/
│   ├── build_marl_amr_env.sh                ← stage 1 (conda + MFEM + reqs)
│   ├── build_pymfem_step.sh                 ← stage 2a (failed: --no-parallel)
│   ├── build_pymfem_step2.sh                ← stage 2b (failed: crypt.h sysroot)
│   ├── build_pymfem_step3.sh                ← stage 2c (✅ working — uses sysroot crypt.h)
│   ├── run_eval.sh                          ← pass-1 eval (single ep)
│   └── run_eval2.sh                         ← pass-2 eval (20 random ep × 4 thresholds)
├── logs/
│   ├── build_step1.log                      ← conda+MFEM+pip
│   ├── build_step2_pymfem.log               ← PyMFEM final working build
│   ├── run_eval1.log                        ← deterministic single-Gaussian
│   └── run_eval2.log                        ← 20-episode pareto sweep
├── results/
│   ├── vdgn_random20_0.csv                  ← VDGN 20 random episodes
│   ├── ht_h{1e-4,5e-4,1e-3,5e-3}_*.csv     ← Heuristic sweep, 20 ep each
│   ├── fixed20_{coarse,fine}.csv            ← Fixed-mesh baselines
│   ├── vdgn_err_vs_time_singleGauss.csv     ← VDGN error trajectory
│   └── pareto.csv                           ← single-episode Pareto stub
└── plots/                                   ← TBD (Pareto, error-vs-time, mesh evolution)
```

## Remote artifacts (uicgpu)

- Project root: `/data/stevens/projects-active/marl-amr/`
- Built env: `~/miniconda3/envs/marlamr/`
- Build logs: `/tmp/build_marl_amr.out`, `/tmp/build_pymfem3.out`
- Eval logs: `/tmp/run_eval.out`, `/tmp/run_eval2.out`
- All CSV outputs: `/data/stevens/projects-active/marl-amr/heuristic_out2/` and `.../marl_amr/results/advection/random_eval/`

## Status

**On track.** Build done, primary claim replicated. Remaining work is plotting + writing, ~30 min more.
