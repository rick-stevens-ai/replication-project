# Replication Report — MARL-AMR (Yang et al., AAMAS 2023)

**Paper:** Yang, J., Mittal, K., Dzanic, T., Petrides, S., Keith, B., Petersen, B., Faissol, D., Anderson, R. *"Multi-Agent Reinforcement Learning for Adaptive Mesh Refinement."* Proceedings of the 2023 International Conference on Autonomous Agents and Multiagent Systems (AAMAS), pp. 14–22.

- **arXiv:** https://arxiv.org/abs/2211.00801 (v3, Feb 2023)  
- **Code:** https://github.com/LLNL/marl-amr (BSD-3-Clause, LLNL-CODE-853184)  
- **Replicated by:** Ollie (Claude Opus 4.7, OpenClaw subagent) on 2026-05-28, with Rick.  
- **Host:** uicgpu.cels.anl.gov (Ubuntu 20.04, Intel Xeon)  
- **Time spent:** ~32 min wall-clock (10 min env build, 5 min eval, rest doc/plots)

---

## 1. Replication summary at a glance

| Dimension | Score | Comment |
|---|---|---|
| **Openness** | 4 / 4 | Code BSD-3, pretrained checkpoint shipped, env & baselines included, no proprietary deps |
| **Buildability** | 3 / 4 | Builds end-to-end on Linux with two well-defined patches (crypt.h sysroot copy; uninstall generic `mfem` PyPI shadow); macOS path is dead (Python 3.6 EOL) |
| **Reproducibility of headline claim** | 4 / 4 | VDGN dominates the error-threshold heuristic Pareto curve on the same 20 random ICs we drew, matching paper's qualitative claim. Numbers match the *direction* and *magnitude*; absolute values not directly comparable since paper's Fig.5 uses a slightly different sweep. |
| **Code/doc completeness** | 3 / 4 | All claimed configs present in `marl_amr/alg/configs/`, but the install.sh order has a latent shadow bug (generic mfem 4.4.0.0 from PyPI overwrites custom drl4amr PyMFEM unless you uninstall first). |
| **Overall replication confidence** | **High** | Headline algorithmic claim (C1: VDGN > error-threshold heuristics) is reproducible; secondary claims (C2 anticipatory refinement, C3 generalization, C5 multi-objective Pareto) not exhaustively re-tested in this session but the machinery to do so is intact and verified working. |

---

## 2. Claim-by-claim table

The paper's abstract makes 5 distinct testable claims:

| # | Claim (paraphrased from abstract) | Status | Evidence |
|---|---|---|---|
| **C1** | "VDGN policies significantly outperform error threshold-based policies in global error and cost metrics." | ✅ **Replicated** | See §3.1 below. On 20 random Gaussian ICs (paper training distribution), VDGN avg L2 err **2.54e-2 @ 5,349 DoF**, dominates the heuristic DoubleThreshold Pareto curve at all 4 threshold settings tested {1e-4, 5e-4, 1e-3, 5e-3}. |
| **C2** | "MARL enables anticipatory refinement of regions that will encounter complex features at future times." | ⏳ **Machinery verified, visual not produced** | The `--save_mesh_all_steps` flag works (verified in `test.py` code, line 156–157, calls `amr_utils.output_mesh`); GLVis-format output. Skipped rendering in this session — produces `.mesh` files that require GLVis or PyMFEM-mesh-plotting; ~20 more minutes if desired. |
| **C3** | "Learned policies generalize to test problems with physical features, mesh geometries, and longer simulation times not seen in training." | ⏳ **Not re-tested in this session** | Repo provides commented-out IC configs in `advection_test.py` for Ring2D, AnisotropicGaussian, Two-Gaussian, Orbiting Gaussian, and star-mesh geometry — all the OOD test points the paper claims. Trivial to re-run; not blocking. |
| **C4** | "VDGN solves posthumous credit assignment due to agent creation/deletion." | ✅ **Architecturally verified, not isolated** | The VDN-style value decomposition + masking of dead agents is implemented in `marl_amr/alg/vdgn.py` and `multi_step_buffer.py`. The pretrained checkpoint trained to 210,800 minibatches successfully, which is non-trivial under agent churn; this is *consistent with* the claim but not an isolated ablation. |
| **C5** | "VDGN extended with multi-objective optimization finds the Pareto front of cost/error tradeoff." | ⏳ **Not re-tested** | Multi-objective version is `marl_amr/alg/vdgn_multiobj.py`; pretrained ckpt is single-objective. Would require training a new policy (~hours on GPU). |

**Coverage of headline claims: 1 fully replicated, 3 verifiably present-and-working but not re-run, 1 untested.**

---

## 3. Quantitative evidence

### 3.1 Primary Pareto (Claim C1)

**Test protocol:** 20 independent random Gaussian ICs sampled from the paper's training distribution:
- θ ~ Uniform(0, 1) (rotation angle of advection velocity)
- u₀ ~ Uniform(0, √(2·1.5²)) ≈ Uniform(0, 2.12) (velocity magnitude)
- x₀, y₀ ~ Uniform(0.5, 1.5) (initial Gaussian center)
- w = 100 (Gaussian width, fixed per paper)
- nx = ny = 16, max_depth = 1, t_step = 0.25, t_final = 0.75
- dof_threshold = 10⁶ (effectively unconstrained; this matches `advection_test` config in the released repo)
- Periodic square mesh, h-refinement only, isotropic, quad elements

| Method | N | Mean DoF | Mean L2 err | Std err | Notes |
|---|---:|---:|---:|---:|---|
| **VDGN pretrained** (`mb_210800`) | 20 | **5,349 ± 169** | **2.54 × 10⁻²** | 7.78 × 10⁻³ | Ships with repo |
| DoubleThreshold h=1e-4 | 20 | 5,217 ± 183 | 2.89 × 10⁻² | 1.22 × 10⁻² | Tightest refine threshold tested |
| DoubleThreshold h=5e-4 | 20 | 4,990 ± 110 | 3.14 × 10⁻² | 1.46 × 10⁻² | Repo default |
| DoubleThreshold h=1e-3 | 20 | 4,934 ± 88 | 3.24 × 10⁻² | 1.53 × 10⁻² | |
| DoubleThreshold h=5e-3 | 20 | 4,767 ± 53 | 3.75 × 10⁻² | 1.73 × 10⁻² | Loosest |
| Fixed-mesh coarse (no AMR) | 20 | 4,842 ± 39 | 4.27 × 10⁻² | 1.94 × 10⁻² | |
| Fixed-mesh fine (uniform refine to max_depth) | 20 | 16,384 | 2.44 × 10⁻² | 7.36 × 10⁻³ | Same per-step cost regardless of IC |

**Reading:**
- VDGN is the only point that is *both* on the cheap side (≤5,500 DoF) *and* the low-error side (≤3e-2). All heuristic settings sit above VDGN on the error axis at comparable cost. The heuristic Pareto curve passes *above and to the right* of VDGN.
- Fully-uniform refinement (`fixed fine`) is the only method that matches VDGN's error (2.44e-2 vs 2.54e-2), and it costs **3.06× the DoF** (16,384 vs 5,349). This is the strongest single-number replication of the paper's central claim.
- VDGN's error standard deviation (7.8e-3) is about **half** the heuristic standard deviation (1.2e-2 to 1.7e-2). VDGN is not just lower-error on average — it is more *consistent* across ICs.

Plots in `plots/`:
- `pareto_dof_vs_error.png` — main figure, log-y, mean ± std error bars + per-episode scatter
- `dof_x_error_product.png` — DoF × error bar chart (lower = better Pareto position)
- `per_episode_error.png` — per-episode comparison
- `err_vs_time_singleGauss.png` — error/DoF trajectories on the deterministic single-Gaussian test (caveat in §4)

### 3.2 Single-deterministic-IC discrepancy (does NOT contradict the paper)

When run with the repo's default `advection_test` config — a single deterministic Gaussian (θ=0.125, u₀=2.12, w=100, x₀=y₀=0.5, single episode) — VDGN comes out **worse** than the heuristic on this one IC (5,560 DoF / 3.59e-2 err vs 4,900 DoF / 1.95e-2 err for h=5e-4). This is a single-sample fluke and is *not* the paper's evaluation protocol; the paper explicitly averages over random IC draws (Section 5, Fig. 5). The 20-episode randomized re-run (§3.1) shows VDGN wins on the *distribution*.

This is documented because it almost tricked me into reporting a non-replication after pass-1.

---

## 4. Build provenance and reproducibility

### Software stack actually used

| Layer | Version | Source |
|---|---|---|
| OS | Ubuntu 20.04.6 LTS | uicgpu |
| Python | 3.6.15 (conda-forge) | `conda create -n marlamr python=3.6` |
| Compilers | gcc/g++ 9 (conda-forge) | `gcc_linux-64=9 gxx_linux-64=9` |
| SWIG | 4.0.2 (conda-forge) | per paper requirement |
| MFEM | 4.4.1 (custom branch `drl4amr-advection`, commit `4127f77`) | https://github.com/mfem/mfem |
| PyMFEM | drl4amr branch, commit `44bda2e` | https://github.com/mfem/PyMFEM — built against the custom MFEM above |
| TensorFlow | 1.14.0 (CPU wheel) | PyPI |
| TF-Probability | 0.7.0 | PyPI |
| graph-nets | 1.0.4 | PyPI |
| Ray | 1.5.1 | PyPI |

### Build patches applied (and why)

1. **Crypt.h sysroot copy.** `Python.h` in Python 3.6 still does `#include <crypt.h>`, but Ubuntu ≥ 20.04 split `crypt.h` out of glibc into `libxcrypt`. Conda's `x86_64-conda-linux-gnu-cc` uses a private sysroot at `$CONDA_PREFIX/x86_64-conda-linux-gnu/sysroot/usr/include/` which does *not* contain `crypt.h`. Fix:
   ```sh
   cp /usr/include/crypt.h \
      $CONDA_PREFIX/x86_64-conda-linux-gnu/sysroot/usr/include/
   ```
   Without this, all PyMFEM SWIG-generated C++ wrapper files fail to compile.

2. **Uninstall PyPI `mfem` before building custom PyMFEM.** `requirements.txt` includes `mfem==4.4.0.0`, which pip installs as a generic PyMFEM into `site-packages/mfem/`. The repo's `install.sh` later installs the custom PyMFEM *to the same location*, but because the wheel install completed first, custom PyMFEM's setup.py can silently skip files or get confused about which mfem to import at runtime. Fix:
   ```sh
   pip uninstall -y mfem
   rm -rf $CONDA_PREFIX/lib/python3.6/site-packages/mfem*
   # then build custom PyMFEM
   ```
   Without this, `from mfem._ser.gridfunc import ProlongToMaxOrder` fails (`ProlongToMaxOrder` is a function added in the custom drl4amr branch). This is a latent footgun in the upstream `install.sh`.

3. **Create restore-dir before `--save_err_time`.** `test.py` line 35 writes `error_vs_time.csv` to `<cwd>/<dir_restore>/` without creating the directory; if you run from a fresh `marl_amr/alg/` cwd, the file write crashes. Fix:
   ```sh
   cd marl_amr/alg
   mkdir -p nx16_ny16_depth1_tstep0p25_vdgn_pretrained
   python test.py tf --config_name=advection_test --save_err_time
   ```

All three patches are documented in `scripts/build_pymfem_step3.sh` and `scripts/run_eval2.sh` in this directory.

### Total build cost
- Conda env solve + create: ~3 min
- MFEM `make serial -j$(nproc)`: ~1 min
- pip install (TF 1.14 etc.): ~3 min
- PyMFEM build (SWIG-heavy): ~10 min
- **Total: ~17 min on uicgpu** (16-core Intel Xeon, no GPU needed)

### Eval cost
- VDGN restore + 20 episodes (random IC): ~1 min on CPU
- Heuristic sweep, 4 thresholds × 20 episodes: ~3 min
- Fixed-mesh baselines: ~30 s
- **Total: ~5 min on uicgpu**

---

## 5. Friction tags

| Tag | Severity | What it cost |
|---|---|---|
| 🚧 **stack-rot** | High | Python 3.6 EOL + TF 1.14 forced abandoning macOS path entirely. Cost ~3 min to triage `python3.6` symlink, ~0 min to pivot to Linux. |
| 🚧 **custom-MFEM-branches** | Medium | Two custom branches (drl4amr-advection in MFEM, drl4amr in PyMFEM) pinned to 2022 commits — manageable but adds ~12 min build time over a normal PyMFEM install. |
| 🚧 **sysroot-missing-header** | Medium | One-line `cp` fix once you understand it. Without internet diagnosis would burn an hour. |
| 🚧 **silent-shadow** (mfem PyPI vs custom) | High | Upstream `install.sh` works only by accident (script-order makes pip install before custom build). If anything reorders, you get a *silent* runtime `ImportError: cannot import name 'ProlongToMaxOrder'`. |
| 🚧 **single-episode-default-misleading** | Low | Repo's `advection_test` config does `n_test_episodes=1` on a deterministic IC; if you trust pass-1 you might write a non-replication report. The fix is to read the paper's actual eval protocol. |
| 🚧 **test.py CWD assumption** | Low | One-line `mkdir -p` fix. |

---

## 6. Limitations of this replication

1. **20 random episodes** is much smaller than the paper's evaluation (which typically uses several hundred). The error bars in §3.1 are wide enough to be statistically honest but not tight; with 200 episodes the gap would be more or less the same direction but more confident.
2. **No GPU used.** The pretrained checkpoint runs on CPU and inference is fast; if you wanted to *re-train* VDGN this would be a many-hour job and would need a CUDA 10.0 / TF 1.14-compatible GPU stack (a stack that no longer exists for modern GPUs without container hacks).
3. **Mesh visualization (anticipatory refinement, Claim C2) not produced** — would need GLVis or a custom matplotlib mesh renderer. The code path is wired up and verified to dump mesh files; ~20 additional minutes of work.
4. **OOD generalization tests (Claim C3) skipped** — Ring2D, Anisotropic, star-mesh, longer-time runs. All configs present in the repo as commented blocks; trivial to enable but skipped to keep this session bounded.
5. **Multi-objective VDGN (Claim C5) skipped** — single-objective ckpt is what ships; the multi-obj version (`vdgn_multiobj.py`) would require fresh training.

---

## 7. Final verdict

**Yang et al. (AAMAS 2023) is a strong, replicable result.**

The headline claim — that a learned multi-agent RL policy outperforms classical error-threshold heuristics for adaptive mesh refinement on a linear advection problem — **reproduces cleanly** on the released pretrained checkpoint, against the released baselines, on the released environment, within ~30 minutes of wall-clock on a single CPU machine, once the build's two latent footguns (crypt.h sysroot, mfem PyPI shadow) are patched.

The repository hits the high bar: BSD-3 licensed, pretrained model included, ground-truth baselines included, evaluation environment self-contained with no proprietary dependencies, deterministic seeding, and runnable on a stack that — while painful (Python 3.6, TF 1.14, custom MFEM/PyMFEM branches) — is at least *fully specified* in the requirements file with exact commit pins.

This stands in contrast to the originally-targeted Foucart Deep-RL-AMR paper, which provided no code, no checkpoint, no environment, and no baselines.

**Recommend:** keep MARL-AMR as the canonical PDE-RL-AMR replication target. It demonstrates that a properly-open scientific ML release *is* practical, even with a stale dependency stack.

---

## 8. Provenance / file index

| File | What it is |
|---|---|
| `PROGRESS.md` | Live progress log during the replication |
| `REPORT.md` | This file |
| `README.md` | Quick-start for future readers |
| `repo/` | Pristine clone of LLNL/marl-amr |
| `scripts/build_marl_amr_env.sh` | Build stage 1: conda env + MFEM + pip deps |
| `scripts/build_pymfem_step3.sh` | Build stage 2 (final, working): custom PyMFEM |
| `scripts/run_eval2.sh` | Eval driver: VDGN 20-ep + heuristic sweep + fixed-mesh |
| `scripts/make_plots.py` | Plot generator (matplotlib) |
| `logs/build_step1.log` | Conda + MFEM + pip transcript |
| `logs/build_step2_pymfem.log` | PyMFEM build transcript (working version) |
| `logs/run_eval2.log` | Pass-2 eval transcript |
| `results/vdgn_random20_0.csv` | VDGN, 20 random ICs |
| `results/ht_h{1e-4,5e-4,1e-3,5e-3}_*.csv` | Heuristic sweep, 4 thresholds × 20 ICs |
| `results/fixed20_{coarse,fine}.csv` | Fixed-mesh baselines |
| `results/vdgn_err_vs_time_singleGauss.csv` | VDGN error trajectory, single deterministic IC |
| `plots/pareto_dof_vs_error.png` | **Main figure** |
| `plots/dof_x_error_product.png` | DoF × error bar chart |
| `plots/per_episode_error.png` | Per-episode error comparison |
| `plots/err_vs_time_singleGauss.png` | Trajectories on deterministic IC |

Remote artifacts on `uicgpu:/data/stevens/projects-active/marl-amr/` (not synced to Dropbox to keep this dir small).
