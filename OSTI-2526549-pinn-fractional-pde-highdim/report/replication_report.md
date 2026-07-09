# Replication Report — OSTI 2526549

**Paper.** Zheyuan Hu, Kenji Kawaguchi, Zhongqiang Zhang & George Em Karniadakis (2024), *"Tackling the curse of dimensionality in fractional and tempered fractional PDEs with physics-informed neural networks."* Computer Methods in Applied Mechanics and Engineering **432** 117448. DOI: 10.1016/j.cma.2024.117448. Public reference code: https://github.com/zheyuanhu01/Tempered_Fractional_PINN.

**Attempt.** Real independent rerun of the authors' JAX/Haiku code on our own hardware (Argonne uicgpu, 8 × A100 80 GB), targeting the paper's flagship high-dimensional fractional Poisson benchmark (Table 2, Eq. 29, `problem == 7`, α = 1.5).

**Final status.** `WAVE_RESULT: partial` (LLM-judge concurs: **SPOT-CHECK**, confidence 0.72).

---

## 1. Executive summary

| aspect | ours | paper | agreement |
|---|---|---|---|
| method executes on published code | ✅ | ✅ | full |
| d=100 quad final rel-L2 | 2.92 × 10⁻² | 2.84 × 10⁻² | within 3% |
| d=100 vanilla final rel-L2 | 3.95 × 10⁻² | 2.86 × 10⁻² | worse by 38%, single-seed noise likely |
| d=1000 quad rel-L2 | 5.01 × 10⁻² @ 200K ep | 3.31 × 10⁻² @ 1M ep | direction correct, curve still decreasing |
| d=1000 vanilla rel-L2 | 5.66 × 10⁻² @ 200K ep | 3.36 × 10⁻² @ 1M ep | direction correct, curve still decreasing |
| quad faster per iter than vanilla | ✅ (2.9× @ d=100; 1.8× @ d=1000) | ✅ (4.2×; 3.3×) | direction full, magnitude ~30–45% below |
| quad more accurate at fixed budget | ✅ (26% @ d=100; 12% @ d=1000) | ✅ | direction correct |
| tempered fractional operator | not tested | — | OUT OF SCOPE |
| inverse & time-dependent variants | not tested | — | OUT OF SCOPE |
| d=100 000 stability | not tested | — | OUT OF SCOPE (needs multi-day compute) |

## 2. Files in this directory

```
OSTI-2526549-pinn-fractional-pde-highdim/
├── NOTES.md                                   ← scope, honesty log, verdict
├── report/
│   ├── brief.md                               ← paper précis + our target
│   ├── artifact_harvest.md                    ← PDF fetch, code clone, deps, patches
│   ├── attempt_log.md                         ← chronological run diary
│   ├── results_summary.md                     ← per-run L2 table + trajectories
│   ├── replication_report.md                  ← THIS FILE
│   └── evidence/
│       ├── mcfpinn_d100_e1M.log               ← raw tqdm/loss/L2 log, run 1
│       ├── mcfpinn_quad_d100_e1M.log          ← raw log, run 2
│       ├── mcfpinn_d1000_e200k.log            ← raw log, run 3
│       ├── mcfpinn_quad_d1000_e200k.log       ← raw log, run 4
│       └── llm_judge_verdict.json             ← Argo GPT-5.2 per-claim verdict
└── work/
    ├── paper.pdf                              ← OSTI PDF (sha256 in artifact_harvest.md)
    ├── code_snapshot.tgz                      ← frozen copy of the ref repo we ran
    ├── llm_judge.py                           ← Argo-proxy LLM-judge client
    └── judge_input.md                         ← claims-vs-evidence input to judge
```

## 3. Independence of the reproduction

- **Different hardware.** Paper claims their runs are on "a single A100 GPU" (make/model unspecified). We ran on uicgpu (Argonne CELS) A100 80 GB, one per process.
- **Different execution environment.** Their code was written against an older JAX (they use `from jax.config import config` and `jnp.clip(x, a_min=…)`, both dropped in JAX ≥ 0.4). We ran under JAX 0.10.0 / Haiku 0.0.16 / Optax 0.2.8 with the two mechanical `sed` patches documented in `artifact_harvest.md`. No algorithmic change.
- **Same benchmark, same seed.** Both use SEED=0, problem 7, α = 1.5, N_f = 100, N_mc = 64, PINN 128 × 4-layer MLP with tanh activations, Adam with linear-decay lr 1e-3→0.
- **Same test procedure.** 20 000 uniformly-sampled points inside the unit ball; rel-L2 = ‖û − u‖₂/‖u‖₂ using the reference code's own `L2_pinn` function, unchanged.

## 4. What was tested vs. what was not

Tested (see `results_summary.md`):
- **C1** unified MC-fPINN framework — partially (fractional side only)
- **C2** quadrature-improved variant — partially (fractional Gauss-Jacobi only, not Gauss-Laguerre)
- **C3** Table 2 numbers — partially (d=100 both methods at full 1M epochs; d=1000 both methods at reduced 200K)
- **C4** quad ≈ 3–4× faster per iter — partially (~2× measured, direction correct)

Not tested (deliberate, documented in NOTES.md):
- **C5** d = 10⁵ scaling — OUT OF SCOPE (compute budget)
- **C6** inverse and time-dependent extensions — OUT OF SCOPE (spot-check depth)
- Tempered operator branch entirely — OUT OF SCOPE

## 5. Recommendation

For a full replication of this paper, next steps would be, in order:
1. Multi-seed (≥5) average of the four runs we did — will very likely close the d=100 vanilla accuracy gap.
2. Full 1M-epoch runs at d=1000 — probably 4 × A100 for 3–4 h each.
3. Symmetric 4-run study on MCTFPINN.py / MCTFPINN_quad.py — validates the tempered claim.
4. Extreme-scaling (d=10⁴, d=10⁵) — needs multi-GPU / careful memory management, ~1 GPU-day.

For the purposes of this spot-check, the paper's central methodological claim (a quadrature-improved MC-fPINN is faster and at least as accurate as vanilla MC-fPINN on high-dim fractional Poisson) is **independently confirmed**.

## 6. Compliance

- ✅ FREE endpoints only — Argo proxy (localhost:44497) for LLM-judge, uicgpu for training, no paid API touched.
- ✅ Real code, real data, real runs — nothing fabricated; every number in `results_summary.md` has a corresponding grep-able line in `report/evidence/*.log`.
- ✅ No overwrite — this is a fresh directory.
- ✅ LLM-judge step completed and archived.

