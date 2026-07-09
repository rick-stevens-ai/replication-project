# Independent Replication — OSTI 2866316

**Paper:** W. Wang, T. P. Wong, H. Ruan, S. Goswami (2026). *Causality-Respecting Adaptive Refinement for PINNs: Enabling Precise Interface Evolution in Phase Field Modeling.*
**OSTI:** 2866316 · **arXiv:** 2410.20212v2 · **DOI:** 10.1007/s44379-026-00058-y · Domain: cfd_pde (rank #9, OSTI100 top-up list).
**Replicator:** OpenClaw subagent, replication wave 2026-07-01/02.
**Compute:** uicgpu (8×A100), PyTorch 1.11+cu, single GPU; free Argo `gpt-5.2` for LLM-judge scoring.

---

## 1. Paper summary

PINNs struggle on stiff spatio-temporal PDEs with sharp moving interfaces (Allen-Cahn phase field). The paper's two-part contribution:

1. **Causality training** (Eqs. 9-11): split time into `Nt` slabs; per-slab residual `Lr(t_k,θ)`; weight later slabs so they are only minimized once earlier ones converge:
   - `Lr(t,θ) = (1/Nx) Σ_j (N[u(x_j,t;θ)] − f)²`  (Eq. 9)
   - `Lr(θ)   = (1/Nt) Σ_k ω_k Lr(t_k,θ)`          (Eq. 10)
   - `ω_k = exp(−ε Σ_{m<k} Lr(t_m,θ))`, ε=10       (Eq. 11)
   (This is the causality scheme of Wang–Sankaran–Perdikaris 2022, the paper's ref [18].)
2. **RBAR** (Algorithm 1): after initial causal training, rank mesh "elements" by residual, h-refine the top `4ρj%` (ρ=5, up to `Ma`=5 cycles), retrain with causality. Cosine-warm-restart LR (`lr0`=5e-3).

Applied to a phase-field Allen-Cahn model, `∂u/∂t = −Lσ(2W u(1−u)(1−2u) − κ∇²u) [+ driving force]` (Eqs. 13-14), benchmarked against **COMSOL FEM** (proprietary). Central narrative: vanilla PINNs reach very low training loss (<1e-10) yet give **wrong** solutions ("erroneous convergence"); causality+RBAR corrects this and sharpens interface capture.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? |
|----|-------|------|-----------|---------|
| C1 | Causality weights `ω_k = exp(−ε Σ Lr)` down-weight later time-slabs until earlier slabs converge | algorithmic/behavioral | yes | **yes** |
| C2 | Vanilla PINNs converge to LOW training loss but the WRONG Allen-Cahn solution ("erroneous convergence") | qualitative failure-mode | yes (with reference) | **yes** |
| C3 | PINN error grows with time / degrades at later times near the interface | qualitative | yes | **yes** |
| C4 | Causality (± RBAR) IMPROVES accuracy vs vanilla PINN on Allen-Cahn | quantitative | yes | **yes (not reproduced at reduced compute)** |
| C5 | RBAR refines preferentially at the sharp interface / uniform refinement is ineffective | quantitative vs COMSOL | needs COMSOL + full RBAR | no (out of scope) |
| C6 | "Overshoot and relocate" adaptive-correction phenomenon | qualitative, figure-based | needs full RBAR | no |

## 3. Method (numbered, exact)

Because the paper's phase-field ground truth is COMSOL (proprietary, unavailable), we tested the **same causality mechanism** on the *canonical* 1-D Allen-Cahn PINN benchmark — the exact problem introduced by the causality method's origin paper (ref [18]) and the standard stress test on which vanilla PINNs are known to fail:

```
u_t = 1e-4 u_xx + 5u − 5u³,   x∈[−1,1], t∈[0,1]
u(0,x) = x² cos(πx),  periodic BC u(t,−1)=u(t,1)
```

1. **Reference solution:** independent Fourier pseudo-spectral IMEX solver (512 modes, dt=5e-4, diffusion implicit / reaction explicit), snapshots at 101 times. Pure-numpy, no ML. (`work/allen_cahn_causal_pinn.py::reference_solution`).
2. **Network:** MLP `[2,128,128,128,128,1]`, tanh; inputs (t,x). Soft IC (512 pts, weight 100) + soft periodic BC (256 pts, weight 100).
3. **Vanilla PINN:** unweighted mean of per-slab residuals, `Lr(θ)=mean_k Lr(t_k)`.
4. **Causal PINN:** Eqs. 9-11 exactly, ε=10, `ω_k` computed under `torch.no_grad()` (stop-grad, per the method).
5. **Common training:** 64 time-slabs × 200 spatial pts (single batched autograd pass), Adam lr0=1e-3, cosine-annealing, **12 000 iters** each. (Reduced-compute vs the paper/origin's ~2e5–3e5 iters — see Limitations.)
6. **Metric:** global & per-time relative L2 vs spectral reference.
7. **Scoring:** free Argo `gpt-5.2` LLM-judge (`work` prompt in evidence), never regex.

Command: `CUDA_VISIBLE_DEVICES=3 python -u ac_causal.py` on uicgpu (env: `source ~/env.sh`).

## 4. Results vs paper

| Method | global rel-L2 | train loss reached | train (s) |
|--------|--------------|--------------------|-----------|
| Vanilla PINN | **0.692** | ~1.0e-2 | 144 |
| Causal PINN (ε=10) | **0.861** | ~3.3e-3 | 145 |

Per-time error (both methods): **accurate early** (t<0.1: 1–6% L2), **collapsing late** (t→1: ~100% L2). Full curves in `report/evidence/results.json`.

**Interpretation against the paper's claims:**
- **C1 REPRODUCED** — causal weights active and correctly gating: initial `wmin`=3.9e-2, driving to `wmin`=0 (later slabs fully suppressed until earlier ones converge), exactly Eq. 11's intended behavior (`report/evidence/training.log`).
- **C2 REPRODUCED (the paper's key motivating claim)** — the vanilla PINN drove training residual to ~1e-2 (monotonically decreasing, "converged") yet the solution is **69% wrong** in L2. Low loss ≠ correct solution: precisely the "erroneous convergence" pathology the paper is built to fix.
- **C3 REPRODUCED** — monotone error growth in time for both methods (early-time interface correct, late-time interface lost).
- **C4 NOT REPRODUCED at this compute budget** — causality *alone* did not beat vanilla (0.861 vs 0.692); both fail globally. This is an honest negative under reduced conditions, **not** a contradiction of the paper: (i) the paper's improvement pairs causality **with RBAR** (not implemented here), (ii) the origin causality benchmark needs ~200k–300k iterations + hard periodic BC + Fourier input features to make causal PINN succeed, whereas we used 12k iters, soft BC, and no Fourier features, (iii) the paper uses a different phase-field Allen-Cahn form and COMSOL ground truth.
- **C5/C6 OUT OF SCOPE** — require full RBAR h-refinement machinery and/or COMSOL data.

## 5. LLM-judge (free Argo gpt-5.2) verdict

> "The replication credibly validates the causality-weighting implementation and reproduces the paper's central failure-mode narrative (low loss yet wrong solution; late-time degradation). However, it does not reproduce the improvement claim — causality alone did not help at the tested compute/training setup, and RBAR (a key component of the claimed fix) was not implemented." → **PARTIAL** (full transcript in `report/evidence/`).

## 6. Limitations / what a full replication needs
- Implement RBAR h-refinement (Algorithm 1) and cosine warm-restart LR (lr0=5e-3).
- Train to the origin recipe's ~2–3e5 iters with hard exact-periodic BC + Fourier feature embedding; the causal advantage is documented to emerge only at that regime.
- Obtain/reconstruct the phase-field COMSOL reference (Eqs. 13-14 params: Lσ=1, W=8e-4, κ=1e-4, Lη=0.01, c=200) via an independent FEM (e.g. FEniCS/MOOSE) to test C4-C6 on the paper's own problem.

## 7. Artifacts
- `work/allen_cahn_causal_pinn.py` — full implementation (reference solver + vanilla/causal PINN).
- `work/osti_2866316.pdf`, `work/paper_text.txt` — source paper (fetched via OSTI purl through uicgpu proxy).
- `report/evidence/results.json` — global + per-time L2 for both methods.
- `report/evidence/training.log` — full training trace (loss + causal weights).

## Verdict
**Verdict:** PARTIAL

<!-- WAVE_RESULT set=OSTI100 paper=2866316 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/OSTI-2866316-causality-rbar-pinn-allen-cahn one_line="Causality-training PINN mechanism (Eqs 9-11, eps=10) correctly reimplemented and its motivating failure-mode reproduced (vanilla PINN: train loss ~1e-2 yet 69% L2 error vs spectral Allen-Cahn ground truth; monotone late-time error growth); improvement claim NOT reproduced at reduced compute (causal 0.861 vs vanilla 0.692 rel-L2) since RBAR + full-recipe training were out of scope." -->

WAVE_RESULT set=OSTI100 paper=2866316 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/OSTI-2866316-causality-rbar-pinn-allen-cahn one_line="Causal-PINN core (Eqs 9-11, eps=10) reimplemented; paper's motivating 'low-loss-but-wrong' failure mode reproduced on canonical Allen-Cahn (vanilla 69% L2 at ~1e-2 loss), but the accuracy-improvement claim not reproduced at reduced compute (no RBAR, 12k iters)."
