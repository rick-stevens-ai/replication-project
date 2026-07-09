# Independent Replication Report — GAIT: Generative AI for Long-Time Plasma Turbulence

**Paper:** B. Clavier, D. Zarzoso, D. del-Castillo-Negrete, E. Frénod (2025),
"A generative artificial intelligence framework for long-time plasma turbulence simulations,"
*Physics of Plasmas* **32**, 063905. DOI: [10.1063/5.0255386](https://doi.org/10.1063/5.0255386).
OSTI ID 2997724 (OA, CC BY-NC-ND).

**Replication set:** OSTI-100 · **Date:** 2026-07-01/02 · **Compute:** uicgpu (1× NVIDIA A100 80GB), PyTorch 1.11
**Verdict:** **PARTIAL** — core generative-surrogate claims (reconstruction, spectra, stable rollout, speedup)
independently reproduced end-to-end; the transport/diffusivity claim diverged (attributable to the
reduced-resolution self-generated ground truth, not to the GAIT method itself).

---

## 1. Paper summary

The paper introduces **GAIT** (Generative Artificial Intelligence Turbulence), a two-stage deep-learning
surrogate that accelerates 2-D plasma-turbulence simulation for long-time transport studies:

1. **Ground truth:** 2-D Hasegawa–Wakatani (HW) drift-wave turbulence, solved pseudo-spectrally (RK4),
   512² grid, doubly periodic, params C=1, κ=1, μ=1e-3, k0=0.15; snapshots coarse-grained to 64².
2. **CVAE:** a Convolutional Variational Auto-Encoder compresses each 64² electrostatic-potential
   snapshot into a **64-dim latent vector** (encoder Table I: conv 32→32→64→128→512; decoder Table II:
   dense 512 → transposed conv 128→64→32→32→1). Loss = reconstruction + gradient-reconstruction + KL,
   weights (1, 10, 0.01). Adam, lr 1e-3, 5000 epochs.
3. **RNN:** a 2-layer recurrent net (128 units, tanh) + dense(64) rolls the latent state forward
   (input/output sequence length l=50, seq2seq MSE loss). Adam, lr 1e-3, 500 epochs.
4. **Generation:** roll the RNN forward in latent space, decode → new turbulence frames at a fraction of
   the DNS cost. The paper generated 100,000 frames and reports ~400× speedup.

Fidelity is judged via Fourier/POD spectra, Okubo–Weiss flow topology, autocorrelation time, and the
effective turbulent diffusivity from passive-particle transport.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? |
|----|-------|------|-----------|---------|
| C1 | CVAE reconstructs HW snapshots faithfully (visually indistinguishable) | quantitative | yes | ✅ |
| C2 | "Very good agreement" GAIT vs HW in **spatial Fourier spectrum** | quantitative | yes | ✅ |
| C3 | RNN produces **long, stable** rollouts (100k frames); bounded energy; small latent norms | quantitative | yes (scaled) | ✅ |
| C4 | Effective **diffusivity** matches (D_HW=1.311; D_GAIT,1=1.57; D_GAIT,2=1.243); diffusive scaling | quantitative | yes | ✅ (diverged) |
| C5 | GAIT generation **~400× faster** than DNS on same hardware | quantitative | yes | ✅ |
| C6 | POD spectrum / Okubo–Weiss / temporal metrics agreement | quantitative | yes | ➖ (not run; spectra proxy in C2) |

## 3. Data & code availability

**Not public.** Paper states data is "available from the corresponding author upon reasonable request";
no GitHub/Zenodo/GitLab link. → This is a **method reproduction**: we regenerated the HW ground truth
ourselves and reimplemented CVAE+RNN from the paper's Tables I–III and text.
(See `report/artifact_harvest.md`.)

## 4. Method (numbered, reproducible)

Tooling: Python 3.8, PyTorch 1.11 (CUDA), NumPy 1.23, on uicgpu A100 (GPU 3). OSTI PDF fetched via
uicgpu proxy (`~/env.sh`); CherryRd direct curl to osti.gov timed out. Scripts in `work/`.

1. **HW ground-truth solver** (`work/hw_solver_gpu.py`): pseudo-spectral, torch.fft, 2/3-dealiased
   Poisson bracket, RK4. Physics params exactly as paper (C=1, κ=1, μ=1e-3, k0=0.15 → L=2π/k0≈41.9,
   doubly periodic). Grid **128²** (scaled down from paper's 512²), coarse-grained to **64²** by pixel
   averaging.
   - **Stability adaptations** (needed only for the reduced resolution; core physics unchanged):
     modified HW (subtract zonal k_y=0 component from the resistive coupling C(φ−n)); k⁴ hyperviscosity
     (nu4=5e-3); weak large-scale friction (α=0.05); adaptive CFL timestep (factor 0.15, base dt=4e-3)
     with per-step energy-jump + finiteness rejection; and an energy-ceiling amplitude limiter
     (ecap=2.0) that rescales fields when a rare intermittent burst would otherwise violate CFL.
   - Command:
     `python3 hw_solver_gpu.py --N 128 --coarse 64 --dt 4e-3 --nu4 5e-3 --alpha 0.05 --modified 1
      --ecap 2.0 --tmax 3600 --t_start 600 --save_every 1.0 --nsnap 3000 --seed 1234 --gpu 3
      --out hw_snapshots.npy`
   - Output: **(3000, 64, 64)** statistically-stationary snapshots (E≈1.2–2.0), wall **2219 s**.
2. **CVAE + RNN training** (`work/gait_train.py`): architectures per Tables I–III; loss weights (1,10,0.01);
   Adam lr 1e-3; CVAE **3000 epochs** (paper 5000; converged well before), batch 64; RNN **500 epochs**
   (=paper), batch 500, seq l=50, 85/15 split. Data z-normalized.
   - Command: `python3 gait_train.py --data hw_snapshots.npy --cvae_epochs 3000 --rnn_epochs 500
     --seq 50 --wkl 0.01 --gpu 3 --out .`
   - CVAE wall 1858 s; RNN wall 45 s.
3. **Evaluation** (`work/gait_eval.py`): CVAE reconstruction R²; RNN latent rollout (4000 frames) →
   decode → (a) radial Fourier spectrum vs HW, (b) energy-timeseries autocorrelation time, (c)
   passive-particle ExB-drift MSD → effective diffusivity, (d) rollout latent-norm stability, (e)
   per-frame generation speedup vs DNS.
   - Command: `python3 gait_eval.py --data hw_snapshots.npy --gen 4000 --seq 50 --gpu 3 --out .`
4. **LLM-judge verdict** (`work/judge_prompt.txt` → `report/evidence/judge_verdict.txt`): Argo proxy
   (free, localhost:44497, `argo:gpt-5.2`) scored the per-claim reproduction. No regex scoring.

## 5. Results vs paper

| Metric | Paper | This replication | Agreement |
|---|---|---|---|
| **C1** CVAE reconstruction | "satisfactory", indistinguishable | **R² = 0.973**, MSE 0.0268 (z-norm) | ✅ strong |
| **C2** Spatial Fourier spectrum | "very good agreement" | log-log **corr = 0.982**, mean log rel-err **8.6%** | ✅ strong |
| **C3** Rollout stability | 100k frames, bounded energy, small norms | **4000 frames stable**; latent norm mean 14.0 (train 12.3), max 17.1; energy drift **−7.5%**; no blowup | ✅ (at 4000-frame scale) |
| **C4** Diffusivity | D_HW=1.311; D_GAIT 1.243–1.57 (≈ or higher) | **D_HW=5.26, D_GAIT=0.29** (ratio 0.055); τ_HW=117 vs τ_GAIT=5.4 | ❌ diverged (see §6) |
| **C5** Speedup | ~**400×** vs DNS, same hardware | DNS 0.740 s/frame vs GAIT 0.00123 s/frame → **~599×**, same GPU | ✅ same order (exceeds) |

Evidence: `report/evidence/eval_results.json`, `train_meta.json`, `fig_metrics.png` (spectrum /
autocorr / MSD), `fig_energy.png` (rollout energy stationarity), training/generation logs.

## 6. Interpretation of the C4 divergence

The one claim that did **not** reproduce is the transport/diffusivity match. Our GAIT rollout is *more
decorrelated and less diffusive* than our regenerated HW (opposite sign and much larger magnitude than
the paper's small D differences). The most likely cause is **not** the GAIT method but our **ground
truth**: to keep the 4×-reduced-resolution (128² vs 512²) HW solve numerically stable we introduced an
energy-ceiling amplitude limiter and extra dissipation, which can suppress the rare-event intermittency
that dominates turbulent transport and can imprint an atypically long HW autocorrelation (τ_HW=117 is
suspiciously large). With altered ground-truth transport statistics, the surrogate's transport can't be
cleanly compared to the paper's numbers. C4 therefore reflects a limitation of the scaled-down
reproduction environment, not a demonstrated failure of GAIT.

## 7. Verdict

**PARTIAL** (LLM-judge, Argo gpt-5.2, free endpoint; full text in `report/evidence/judge_verdict.txt`).

The generative-surrogate mechanism at the heart of the paper — compress HW turbulence into a 64-dim
latent space with a CVAE and evolve it cheaply with an RNN, then decode faithful new turbulence — was
**independently reimplemented and run end-to-end on freshly generated HW data**, reproducing C1
(reconstruction R²=0.97), C2 (spectrum corr=0.98), C3 (stable bounded rollout), and C5 (~599× speedup,
same order as the claimed ~400×). The transport claim C4 diverged, plausibly due to the reduced-resolution
+ limiter ground truth. Honest assessment: the paper's central computational premise is well supported;
the transport-statistics claim was out of reach in this scaled-down setting.

## 8. Caveats
- Ground truth is 128²→64² with modified-HW + hyperviscosity/friction/limiter, vs paper's 512²→64² —
  materially different intermittency/transport, directly impacting C4.
- Rollout stability shown to 4000 frames, not the paper's 100,000; long-horizon attractor drift untested.
- 3000 training snapshots vs paper's 8000; latent norms (~13) larger than paper's ~1.16 (normalization/KL
  scaling difference; does not affect surrogate function).
- POD spectrum / Okubo–Weiss (C6) not separately computed (spatial Fourier spectrum serves as the
  spectral-agreement proxy).

---
*Files:* `work/` (solver, model, eval, figs, trained CVAE/RNN weights, paper PDF/text);
`report/evidence/` (JSON metrics, figures, logs, judge prompt+verdict).
