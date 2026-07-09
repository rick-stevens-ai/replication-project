# Workflow — Poisson Neural Networks (Jin 2022) Replication

## 0. Target
Section IV-A Lotka–Volterra experiment of Jin, Zhang, Kevrekidis, Karniadakis
(arXiv:2012.03133 / IEEE TNNLS 2022 DOI 10.1109/TNNLS.2022.3148734).

Focal claims: **C1** (architectural Poisson preservation), **C2** (stable
long-time LV rollouts vs unstructured baseline), **C3** (small drift of LV
invariant `H(u,v) = u − ln u + v − 2 ln v`).

## 1. Environment
- Host: `uicgpu` (UIC-managed, 8× A100 80GB; we use `CUDA_VISIBLE_DEVICES=0`).
- Python: `/gpustor/stevens/anaconda3/bin/python3.11`.
- Author code: `git clone --depth 1 https://github.com/jpzxshi/pnn.git`.
- Working dir: `/data/stevens/replicate/PNN-2022/work`.
- Local report/evidence copy: `~/Dropbox/REPLICATE-PROJECT/PDE-Jin-PoissonNeuralNetworks-2022/`.

## 2. Data generation
Three trajectories of `(u̇, v̇) = (u(v−2), v(1−u))` from IC `(1, 0.8)`, `(1, 1)`,
`(1, 1.2)`. Step `h = 0.1`, 100 training points each (300 one-step pairs total).

Ground-truth long-time rollouts (1000 steps from each training endpoint) are
produced via the authors’ own 4th-order Störmer–Verlet integrator
(`learner.integrator.hamiltonian.SV`, `order=4, N=10`) in log-canonical
coordinates `(p, q) = (log u, log v)`. Sanity: SV invariant drift ~4.77e-7.

## 3. Models
| Component | Config | Params |
|---|---|---:|
| PNN.INN | `dim=2, split_dim=1, layers=3, sublayers=2, subwidth=30, sigmoid, VP=False` | — |
| PNN.SympNet (G-type) | `dim=2, layers=3, width=30, sigmoid` | — |
| **PNN total** | INN ∘ SympNet ∘ INN⁻¹ | **816** |
| MLP baseline | Lin(2,64)→tanh→4×(Lin(64,64)→tanh)→Lin(64,2), residual | **12 802** |

## 4. Training
- Adam, `lr=1e-3`, full-batch (`batch_size=None`).
- **30 000** iterations each (paper uses 200k for PNN LV — this is the sole
  intentional deviation, made for wall-time reasons).
- MSE loss on one-step predictions.
- Wall time: PNN 311 s, MLP 61 s on 1× A100.

## 5. Evaluation
- 1000-step autoregressive rollouts from each of 3 training endpoints.
- Per-step MSE vs SV ground truth (mean over trajectories).
- Invariant drift `|H(u_n,v_n) − H(u_0,v_0)|` per step; report max and final.
- LLM judge: Argo `argo:claude-opus-4.7` (free tier), reads results JSON,
  returns per-claim verdict.

## 6. Exact command
```bash
ssh uicgpu
cd /data/stevens/replicate/PNN-2022/work
git clone --depth 1 https://github.com/jpzxshi/pnn.git   # first time only
PATH=/gpustor/stevens/anaconda3/bin:$PATH \
  PNN_ITERS=30000 MLP_ITERS=30000 CUDA_VISIBLE_DEVICES=0 \
  /gpustor/stevens/anaconda3/bin/python3.11 lv_replicate.py
```

## 7. Deliverables
- Numeric results table (rollout MSE + H-drift).
- Phase-portrait, rollout-MSE, and H-drift PNG plots.
- LLM-judge JSON with per-claim verdicts.
- Report (Markdown + LaTeX).

## 8. Deviations vs paper (transparent)
1. **Training iterations** 30k vs 200k (15%). PNN is clearly in a stable
   regime (step-1000 MSE < step-100 MSE) but absolute error may not match
   the paper’s original numbers.
2. **Baseline** is a residual MLP with ~16× the PNN parameter count, not the
   paper’s illustrative bare-SympNet-on-multi-trajectory-non-canonical-data
   failure mode. Ours is a fair unstructured control; the paper’s counter-
   example remains unreplicated.
3. **Scope** limited to Sec IV-A; claims C4 (extended pendulum), C5 (charged
   particle / NLS / two-body pixel), C6 (single non-Hamiltonian trajectory,
   Thm 3) are unattempted, not refuted.
4. **Single seed, single run** — no confidence bands.
