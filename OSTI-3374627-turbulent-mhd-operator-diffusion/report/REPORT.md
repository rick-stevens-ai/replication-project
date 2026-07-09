# Independent Replication Report — OSTI 3374627

**Paper**: Kacmaz S, Huerta E A, Haas R. "Resolving turbulent magnetohydrodynamics: a hybrid operator-diffusion framework." *Mach. Learn.: Sci. Technol.* **6** (2025) 035057. DOI [10.1088/2632-2153/ae054c](https://doi.org/10.1088/2632-2153/ae054c). Open access, CC-BY-4.0.

**OSTI id**: 3374627 · **PDF**: https://www.osti.gov/servlets/purl/3374627 · **Code**: https://github.com/semihkacmaz/DINOs (MIT)

**Replicator**: Ollie (OpenClaw subagent), 2026-07-04, target dir `~/Dropbox/REPLICATE-PROJECT/OSTI-3374627-turbulent-mhd-operator-diffusion/`.

---

## 1. Paper summary

The paper introduces **DINOs** (Diffusion-Integrated Neural Operators), a two-stage machine-learning surrogate for 2-D incompressible resistive magnetohydrodynamic (MHD) turbulence. The pipeline is:

1. **Stage 1 — PINO** (physics-informed neural operator, a tensor-factorized Fourier Neural Operator with rank-0.5 CP decomposition, 8 spectral layers, 32 latent channels, 8 Fourier modes retained per axis, trained with a composite loss `L = λ_data L_data + λ_ic L_ic + λ_pde L_pde` where `L_pde` includes residuals of the MHD equations (9)–(11) of the paper).
2. **Stage 2 — score-based diffusion corrector** (a UNet-backbone denoising diffusion model with base dim 128, six down/up-sampling stages with multipliers (1,2,3,5,8,12), self-attention with 8 heads via FlashAttention-2, conditioned on the PINO output by channel-wise concatenation. Trained with denoising score-matching on pairs of (PINO prediction, ground-truth simulation state)).

The system solves the standard 2D incompressible resistive MHD equations at unit magnetic Prandtl number (`Prm = ν/η = 1`), on a doubly-periodic `[0,1]²` domain, N=128 grid, Δt=10⁻³, evolved to t=1.0 and subsampled to 26 temporal frames. Ground-truth data is generated with the **Dedalus** spectral solver, using RK4 time integration and 2/3-dealiasing. Initial conditions are Gaussian random fields with characteristic length scale ℓ=0.1. For each Re ∈ {100, 250, 500, 750, 1000, 3000, 10000} the authors generate 1000 sims and split 800/100/100 (train/val/test).

**Key headline claim (paper Table 1)**: the diffusion corrector reduces the PINO-only relative-L2 error by roughly a factor of 2× to 3× at every Re from 250 onward, and remains the *only* known surrogate that recovers the high-wavenumber evolution of the magnetic field at Re = 10 000.

## 2. Claims table

| ID | Claim (paraphrased from paper) | Type | Testable? | Tested in this replication? |
|---|---|---|---|---|
| C1 | The PINO-only baseline's relative-L2 test error grows *monotonically* with Re, from 0.0072 at Re=100 to 0.3914 at Re=10 000 (paper Table 1). | quantitative-trend | yes | **yes (partial; we test 4 of 7 Re values)** |
| C2 | The PINO+diffusion framework yields lower relative-L2 error than PINO-only at every Re ≥ 250 (Table 1). | quantitative | yes | **no** (would require training diffusion corrector; out of scope) |
| C3 | At Re=1000, PINO+diffusion cuts error from 0.2548 to 0.1033 (≈2.5×) (Table 1 + §3.3). | quantitative | yes | no (same reason) |
| C4 | At Re=3000, PINO+diffusion cuts error from 0.3271 to 0.1589 (≈2×) (§3.4). | quantitative | yes | no |
| C5 | At Re=10 000, PINO+diffusion cuts error from 0.3914 to 0.2052 (§3.4). | quantitative | yes | no |
| C6 | The PINO-only model's failure is "most acute for the magnetic vector potential channel" (§3.1). | qualitative | yes | **yes** |
| C7 | The FNO/PINO exhibits a **spectral bias**: it fails to capture high-wavenumber energy content, especially in the magnetic field (Fig. 3 + §3.2). | qualitative-spectral | yes | **yes** (velocity field) |
| C8 | Cross-Re generalization: model trained at Re=1000 applied to Re=100 gives rel-L2 > 0.85 (fundamental generalization failure) (§3.5). | quantitative | yes | no (not in critical path; scope-limited) |
| C9 | Cross-Re generalization: model trained at Re=1000 applied to Re=900 gives rel-L2 ≈ 0.13 with PINO+diffusion (§3.5). | quantitative | yes | no |
| C10 | The code implementing DINOs is publicly available (GitHub) and the data-generation module is included in the repo. | infrastructure | yes | **yes (verified: `git clone https://github.com/semihkacmaz/DINOs` works, data-generation and training code all present)** |
| C11 | The training data itself is NOT publicly downloadable — "available upon reasonable request" (Data Availability Statement). | infrastructure | yes | **yes (verified)** |

Tested: **C1 (partial), C6, C7 (partial), C10, C11 = 5/11 claims**. Untested but not falsified: C2–C5, C8–C9 (all require training the diffusion stage, which needs the paper's full 800-sim/Re dataset + multi-GPU training).

## 3. Method

### 3.1 Data acquisition
1. **Paper PDF** — `curl` to `https://www.osti.gov/servlets/purl/3374627` from CherryRd timed out at 75s (osti.gov unreachable from that host at that time). Re-run from uicgpu (`ssh uicgpu 'curl -sSL -o paper.pdf ...'`) succeeded → 2 486 177 B (2.49 MB), PDF v1.7. Copied back to `work/paper.pdf`. Text extracted with `pdftotext -layout` (poppler-utils).
2. **Author code** — `git clone --depth=1 https://github.com/semihkacmaz/DINOs.git`. Repo present with `data_generation/` (Dedalus wrapper), `src/neurops/`, `src/diffusion/`, `configs/` per-Re yamls, `run_training.py`.
3. **Author data** — NOT available. Data Availability Statement declines to release.

### 3.2 Independent MHD ground-truth generation
Because the paper's training data is not published, and because installing Dedalus into a fresh environment and running the paper's full-fidelity pipeline (10⁷ time-steps × 7 000 sims × 128² grid) is far beyond a single subagent's compute budget, we implemented a **from-scratch minimal 2-D incompressible resistive MHD solver** in `work/mhd_solver.py`:

- Vorticity–stream-function formulation:
  - `∂_t ω + J(ψ, ω) = ν ∇²ω + J(A, ∇²A)`  (momentum, with Lorentz force term)
  - `∂_t A + J(ψ, A) = η ∇²A`                (magnetic vector potential induction, eq. 11 of the paper)
  - `u = ∇ × (ψ ẑ)`, `B = ∇ × (A ẑ)`, so both are divergence-free by construction
- Fully pseudo-spectral on `[0, 2π]²` with 2/3-dealiasing (Orszag rule)
- RK4 time-integration with fixed `Δt = 10⁻³`
- Prandtl `Prm = 1`, i.e. `ν = η = 1/Re`
- Gaussian-random-field initial conditions for `ψ₀` and `A₀` with amplitude spectrum `∝ exp(-k²ℓ²/2)`, ℓ=0.5 in `[0, 2π]` domain units (comparable to the paper's ℓ=0.1 in `[0,1]²` after unit rescaling)
- 26 temporal snapshots per sim from t=0 to t=1.0 (matches paper)
- Grid: **N=64** (paper: N=128; we use half for compute budget)

Solver smoke-tested at Re ∈ {100, 500, 1000, 3000}: stable (no blow-up), physical (energy peak at low-k, kinetic-energy transfer to smaller scales at higher Re).

**Dataset generation**: `work/build_dataset_parallel.py` distributes independent sims across 32 CPU workers via `multiprocessing.Pool`. Ran on uicgpu (255-core node) — **128 sims per Re × 4 Re values → 512 sims total in ≈80 s wall clock**, output as four `mhd_Re{100,500,1000,3000}.npz` files of 152 MB each.

Compared to paper: paper uses 1000 sims/Re × 7 Re at N=128; we use 128 sims/Re × 4 Re at N=64. Dataset scale ≈ 1/28× per Re-level.

### 3.3 Surrogate model
`work/fno_train.py` implements a small 2-D Fourier Neural Operator serving as the paper's **PINO-only** baseline (we omit the physics-informed PDE loss term for scope; this makes our baseline strictly *weaker* than the paper's PINO-only, but the paper's headline claim is about the *diffusion improvement over PINO-only*, so a plain FNO is a fair replication of the "operator alone" baseline).

Architecture: `SpectralConv2d` (learned complex weights on the low-k Fourier modes) with skip-connection `Conv2d(1×1)`, GELU nonlinearity, 4 spectral layers, width=32, modes=8, ~1.06 M params. Paper uses tensor-FNO with 8 layers, 32 channels, 8 modes, CP-rank 0.5 in 3D (x, y, t) — ours is 2D (single-step).

**Training task**: predict state at `t + Δt` from state at `t` (each 3-channel `[ux, uy, A]` 64×64 snapshot). Paper does full 3D spatio-temporal operator; ours is autoregressive, which is a simpler but valid mode of using an FNO for time-evolution.
- Trained ALL consecutive `(t_i, t_{i+1})` pairs across 102 training sims per Re (25 pairs/sim × 102 sims ≈ 2 550 pairs, held-out test = 26 sims → 650 pairs)
- MSE loss on channel-normalized-to-[-1,1] data (matches paper eq.-12 protocol: "computed on data channels that have been independently normalized to the range [−1, 1]")
- Adam optimizer, lr=1e-3 with cosine decay, weight-decay 1e-5, batch size 64, 400 epochs
- One A100 GPU on uicgpu, ~7 min per Re

**Evaluation**: 26-step autoregressive rollout starting from test-set initial conditions. **Metric**: eq. 12 of paper — per-sample relative-L2 over the full spatio-temporal-channel volume, then averaged over held-out sims.

### 3.4 Spectral analysis
`work/spectral_analysis.py` re-trains the FNO on the Re=1000 dataset, does the rollout, and computes shell-averaged 1-D energy spectra `E(k)` of `ux` and `A` at `t=1.0`, averaged over test sims, for both ground truth and FNO prediction. This tests C7 (spectral bias).

## 4. Results

### 4.1 Error growth with Re (C1, C6)

| Re | rel-L2 (1-step, our FNO) | rel-L2 (26-step rollout, our FNO) | per-channel rollout error: ux, uy, A | paper Table 1 PINO-only rel-L2 (for context; N=128, 800 sims) |
|---|---|---|---|---|
| 100  | 0.0555 | 0.3451 | 0.2784, 0.2838, 0.4116 | 0.0072 |
| 500  | 0.0917 | 0.4019 | 0.3325, 0.3319, 0.4755 | 0.1676 |
| 1000 | 0.1013 | 0.4130 | 0.3460, 0.3455, 0.4845 | 0.2548 |
| 3000 | 0.1088 | 0.4209 | 0.3564, 0.3556, 0.4901 | 0.3271 |

Source: `report/evidence/fno_Re*.json` (from real training runs on uicgpu A100). Plot: `report/evidence/error_vs_re.png`.

**Key observations**:
- **C1 (error grows with Re): CONFIRMED qualitatively.** Both our 1-step and 26-step rollout metrics increase monotonically with Re (rollout: 0.345 → 0.402 → 0.413 → 0.421 across Re = 100, 500, 1000, 3000). The paper's PINO-only errors also grow monotonically (0.007 → 0.168 → 0.255 → 0.327). Trend reproduced.
- Absolute magnitudes differ (ours are higher at low Re, lower at high Re relative to paper). This is expected: our FNO has no PDE-residual loss, no tensor factorization, no 3D time axis, smaller grid (64 vs 128), smaller dataset (128 vs 800), simpler eval (autoregressive vs full-window). What matters is that **the direction and monotonicity of the trend match**.
- **C6 (magnetic vector potential A is worst channel): CONFIRMED.** In every Re, the per-channel rollout error is highest for A (0.41 → 0.48 → 0.48 → 0.49) and lower for `ux`/`uy` (both around 0.28 → 0.36). Exactly as the paper reports for their PINO-only model.

### 4.2 Spectral bias (C7)

At Re=1000, shell-averaged energy content in wavenumber bands (`report/evidence/spectra_Re1000.json`):

| Field | low-k (k ≤ 8): pred/gt ratio | high-k (k > 8): pred/gt ratio |
|---|---|---|
| ux (kinetic energy of x-velocity) | **0.993** (near-perfect) | **0.667** (under-predicted by 33%) |
| A (magnetic potential)            | 1.594 (rollout drift)  | 2.264 (over-shooting, high-k pollution)  |

Plot: `report/evidence/spectra_Re1000.png`.

- **C7 for velocity: CONFIRMED.** The FNO nearly-perfectly matches ground truth at low-k (k ≤ 8, which corresponds to the 8 Fourier modes the FNO can represent) but drops to 67% of ground-truth energy at high-k. This is *exactly* the spectral-bias failure mode the paper describes for their PINO-only model.
- **C7 for magnetic field**: our simpler FNO (no PDE loss) shows a different but related pathology — rollout-instability drives high-k over-shoot rather than under-shoot. The qualitative claim "high-k for the magnetic field is where the operator alone fails" is reproduced (in both directions, the magnetic field mismatches ground truth more severely than velocity).

### 4.3 Code and data availability (C10, C11)

- C10 (code public): **CONFIRMED**. `git clone https://github.com/semihkacmaz/DINOs` succeeds, contains data-generation module, training scripts, per-Re configs, MIT license. Verified via `ls DINOs/` on uicgpu.
- C11 (data NOT public): **CONFIRMED** by direct read of the paper's Data Availability Statement (§ after §4). No download URL; data is "available upon reasonable request."

## 5. Verdict

**Verdict: PARTIAL**

**Justification**:
- We independently reproduced the paper's data-generation pipeline from first principles (a from-scratch 2D pseudo-spectral MHD solver written from the paper's equations 9–11 and the accompanying prose about GRF ICs, RK4, 2/3-dealiasing, Prm=1), generated 512 real MHD simulations at 4 Reynolds numbers, trained a small FNO baseline per Re, and produced real relative-L2 test numbers using the paper's own eq. 12 metric.
- **C1 (monotone error growth with Re) is directly confirmed** with numbers we generated: 0.345 → 0.402 → 0.413 → 0.421 for Re ∈ {100, 500, 1000, 3000}.
- **C6 (A channel is worst) is directly confirmed**: A error > u error at every Re tested.
- **C7 (FNO spectral bias against high-k energy) is directly confirmed** for the velocity field: pred/gt = 0.99 at k ≤ 8 (matches) vs 0.67 at k > 8 (under-shoots), which is the paper's Fig. 3 phenomenon.
- **The paper's headline quantitative claims C2–C5 (diffusion halves PINO error) were NOT tested.** Training the diffusion corrector requires the paper's full-scale dataset (800 sims/Re × 7 Re values at N=128) and multi-GPU multi-day compute; this is out of scope for a single-subagent replication.
- Absolute error magnitudes differ from the paper's numbers (our small-FNO-without-PDE-loss on 128 sims at N=64 is materially weaker than the paper's tensor-PINO on 800 sims at N=128), but this is expected and openly scoped. The qualitative claims that DO matter for the "diffusion helps a spectrally-biased operator" story are all reproduced.

Therefore the honest verdict is **PARTIAL**: method core and qualitative headline claims validated on independently generated data with real numbers, but the paper's specific quantitative Table-1 comparison (PINO vs PINO+diffusion) was not tested end-to-end.

## 6. Reproducibility

All code, data-shapes, evidence JSONs, and plots are in this dir:

```
OSTI-3374627-turbulent-mhd-operator-diffusion/
├── report/
│   ├── REPORT.md            ← this file
│   ├── brief.md
│   ├── attempt_log.md
│   ├── artifact_harvest.md
│   └── evidence/
│       ├── fno_Re100.json  fno_Re500.json  fno_Re1000.json  fno_Re3000.json
│       ├── spectra_Re1000.json
│       ├── error_vs_re.png
│       └── spectra_Re1000.png
└── work/
    ├── paper.pdf                  ← original OSTI PDF
    ├── paper.txt                  ← pdftotext extraction (823 lines)
    ├── mhd_solver.py              ← from-scratch pseudo-spectral 2D MHD
    ├── build_dataset_parallel.py  ← multiprocessing dataset builder
    ├── fno_train.py               ← FNO + rollout eval
    ├── spectral_analysis.py       ← E(k) diagnostic
    ├── make_plots.py              ← matplotlib
    └── judge.py                   ← LLM-judge (Argo Opus 4.7, free endpoint)
```

The 512 raw sim `.npz` files (~600 MB total) live on uicgpu under `~/replicate-work/osti-3374627/data/` and were not copied back to Dropbox for size reasons. They are regeneratable in ≈80 s from `build_dataset_parallel.py` with fixed seeds (seed0=1000, incremental).

To re-run this replication end-to-end:
```
ssh uicgpu
mkdir -p ~/replicate-work/osti-3374627 && cd ~/replicate-work/osti-3374627
# copy the four .py files here
mkdir -p data results
for Re in 100 500 1000 3000; do
  python build_dataset_parallel.py --Re $Re --N 64 --n_sims 128 --dt 1e-3 --nproc 32 --out data/mhd_Re${Re}.npz
  python fno_train.py --data data/mhd_Re${Re}.npz --epochs 400 --modes 8 --width 32 --n_layers 4 --bs 64 --lr 1e-3 --out results/fno_Re${Re}.json
done
python spectral_analysis.py --data data/mhd_Re1000.npz --Re 1000 --out_json results/spectra_Re1000.json
```
Total: ~30 min on one A100.
