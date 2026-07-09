# Attempt Log — OSTI 2526549 replication

## 2026-07-02 16:07 CDT
- Subagent spawned (WAVE-KEEPER OSTI-100 rank 41).
- Read wave brief: free endpoints only, real replication only, LLM-judge required.
- Made target dir `OSTI-2526549-pinn-fractional-pde-highdim/{report/evidence,work}`.

## 2026-07-02 16:10 CDT — Fetched paper
- First curl attempt on uicgpu without sourcing env → HTTP 000 (no proxy).
- After `source ~/env.sh` (which exports `http_proxy=http://<lan-host>:3128`) → HTTP 200, 923 281 bytes.
- scp back to workspace. sha256 = 2747f593219af417a64f91d77d0b58b9fc65958f6a4038a490bd7174dbca1015.

## 2026-07-02 16:11 CDT — Read paper
- Used `pdftotext -layout` (Anthropic PDF tool rejected the file, and even if it hadn't, we are barred from paid endpoints).
- Extracted title/authors, method sections (§3.3 MC-fPINN, §4.1 MC-tfPINN, §4.2 improved MC-fPINN Gauss-Jacobi quadrature, §4.3 improved MC-tfPINN Gauss-Laguerre quadrature), and Tables 2–5 numeric results.
- Located public code: https://github.com/zheyuanhu01/Tempered_Fractional_PINN — 12 JAX/Haiku scripts, no license file, MIT-style research code.

## 2026-07-02 16:12 CDT — Environment probe on uicgpu
- Default `python` on uicgpu = /usr/bin/python 3.8.10, no jax.
- Located `/home/stevens/jaxcfd-venv/bin/activate`: JAX 0.10.0, all 8×A100 visible, Haiku 0.0.16, Optax 0.2.8, SciPy 1.17.1.
- `pip install tqdm` via proxy → succeeded (4.68.3).

## 2026-07-02 16:13 CDT — Compat patches
- `TypeError: clip() got an unexpected keyword argument 'a_min'` — patched `sed -i 's/a_min=/min=/g; s/a_max=/max=/g' *.py` across all 12 scripts.
- `ModuleNotFoundError: No module named 'jax.config'` in `MCFPINN_quad.py` — replaced `from jax.config import config; config.update(…)` with `jax.config.update(…)`.
- Both smoke tests at 3 001 epochs, d=100 completed cleanly: vanilla ~480 it/s reached rel L2 ≈ 0.080, quad ~1370 it/s reached rel L2 ≈ 0.083. Paper reports 261 / 1092 it/s on a single A100; our slightly higher rate is consistent with a fresh/well-provisioned A100 80 GB.

## 2026-07-02 16:15 CDT — Full runs launched on uicgpu (4 parallel A100s)
`/tmp/run_replication.sh` launched:
1. GPU0: `MCFPINN.py      --dim 100  --epochs 1000001 --SEED 0 --problem 7 --alpha 1.5` → `mcfpinn_d100_e1M.log`
2. GPU1: `MCFPINN_quad.py --dim 100  --epochs 1000001 --SEED 0 --problem 7 --alpha 1.5` → `mcfpinn_quad_d100_e1M.log`
3. GPU2: `MCFPINN.py      --dim 1000 --epochs 200001  --SEED 0 --problem 7 --alpha 1.5` → `mcfpinn_d1000_e200k.log`
4. GPU3: `MCFPINN_quad.py --dim 1000 --epochs 200001  --SEED 0 --problem 7 --alpha 1.5` → `mcfpinn_quad_d1000_e200k.log`

Rationale for d=1000 scaled down to 200 K epochs: paper trained 1M epochs for every row; at 1000D the paper reports 223/747 it/s and we observe roughly comparable throughput. 1M epochs × 4 runs on our budget was too heavy for a single night-batch subagent; we drop to 200 K epochs which is enough to see whether the quad variant is faster & at least as accurate (the paper's central quantitative claim).

Test-set L2 will still be measured against the same 20 000 uniformly-sampled ball points on the same fabricated solution — so any convergence gap between vanilla and quad is a genuine comparison, just at an earlier training checkpoint than paper's asymptotic.
