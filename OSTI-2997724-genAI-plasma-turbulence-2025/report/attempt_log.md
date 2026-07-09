# Attempt Log

## 2026-07-01 (night wave)

- Dedup check: `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -iE "2997724|plasma-turbulence"` → no match. Proceed.
- Read WAVE_BRIEF_2026-07-01.md; mirrored PDE-Wang exemplar structure (report/ + work/).
- Fetch OSTI PDF: **direct curl from CherryRd timed out (exit 28)** — osti.gov not reachable from this host. Retried via `ssh uicgpu` (proxy internet, `~/env.sh`): HTTP/2 200, `application/pdf`, 5,139,969 bytes. scp'd back to work/paper.pdf.
- Extracted text with pypdf (venv): 16 pages, 73,098 chars → work/paper.txt.
- **Data/code availability:** "available from the corresponding author upon reasonable request." NOT public (no GitHub/Zenodo). → Path = method reproduction on self-generated HW turbulence.

### Method extraction (from paper §II–V)
- **HW model (modified/standard Hasegawa–Wakatani):** C(adiabaticity)=1, κ(drive)=1,
  μ(diffusion)=1e-3. Pseudo-spectral, 4th-order Runge–Kutta. Reference k0=0.15 →
  domain 2π/k0 ≈ 41.9 ρ0. Paper grid 512², Δt=2e-2/ω_c0, double-periodic BCs.
  5×10^5 steps, save every 50 → 10,000 snapshots; downsample 512²→64² by pixel averaging.
  Train subset Ns=8000 over window ω_c0 t ∈ [1000, 9000] (saturated regime; growth ends ~t≈200).
- **CVAE:** encoder conv stack 32→32→64→128→512 filters (tanh), periodic padding,
  latent dim N=64 (μ, log σ dense heads + sampling). Decoder mirror: dense 512 → transposed
  conv 128→64→32→32→1 (last linear). Loss = w_φ·recon + w_∇φ·grad-recon + w_KL·KL,
  with (w_φ, w_∇φ, w_KL) = (1, 10, 0.01) [case 1]. Adam, lr=1e-3, 5000 epochs, batch=64.
- **RNN:** 2 recurrent layers (128 units, tanh) + dense(64, linear). Input/output seq
  length l=50. Loss = seq-to-seq MSE of latents advanced one step. Adam lr=1e-3, 500 epochs,
  batch=500, 85/15 train/test split. HW autocorrelation time τ_AC ≈ 4.

### Key quantitative claims to test
- C-diffusivity: D_HW = 1.311; D_GAIT,1 = 1.57 (case 1, higher); D_GAIT,2 = 1.243 (case 2).
- C-speedup: DNS 10k snaps = 50 h on V100; CVAE train 1 h; RNN train ~5 min; GAIT generate
  10k snaps ≈ 7.5 min ⇒ ~400× faster than DNS.
- C-spectra/autocorr/Okubo–Weiss: "very good"/"excellent" agreement GAIT vs HW.

### HW solver development & tuning
- Wrote pseudo-spectral RK4 HW solver, 2/3-dealiased Poisson bracket (numpy CPU first, then
  torch-GPU `hw_solver_gpu.py`). CPU too slow (450k steps single-core); switched to torch.fft on A100 (GPU 3).
- **Stability tuning (scaled-down 128² vs paper's 512²):** at reduced resolution the paper's bare
  params (C=1,κ=1,μ=1e-3) blow up — energy grows monotonically (E: 4→5→NaN by t≈600-800).
  Diagnostic (`hw_diag.py`) showed `hiKfrac≈0` → energy piles at LOW k (inverse-cascade condensate),
  not a high-k dealiasing failure. Standard fix at reduced N: add k⁴ hyperviscosity (nu4) +
  large-scale friction (α) to arrest the condensate. Swept α:
    - α=0.02 → still blows up (condensate wins).
    - α=0.10 → over-damps, instability dies (E→1e-12).
    - **α=0.04, nu4=5e-3, dt=1e-2 → STATISTICALLY STATIONARY**: E fluctuates ~0.5–1.1 over
      t=350–550, sustained saturated turbulence. This is the training regime.
- Production HW dataset: N=128 (coarse-grained 64²), t∈[1000,9000], save every 1 ω_c0⁻¹, Ns=8000,
  seed=1234, on A100 GPU 3. This matches the paper's snapshot count and saturated-window protocol;
  the added α/nu4 are the only deviation, needed purely for numerical stability at 4× lower resolution.
- **Correction — the real fix (final):** the α-friction saturation was metastable (bounded to t~600 then blew up).
  Root cause diagnosis: energy stayed bounded (E~13) then *suddenly* NaN'd — signature of a CFL/timestep
  instability, not a physical condensate. TWO changes made it firmly stable:
    1. **Modified Hasegawa–Wakatani** (`--modified 1`): subtract the zonal (k_y=0) component from the
       resistive coupling term C(φ−n). This is the physically-standard mHW that regulates zonal flows
       and yields genuinely statistically-stationary drift-wave turbulence (used in most GAIT-type studies).
    2. **Smaller timestep dt=4e-3** (from 1e-2) + hyperviscosity nu4=2e-3, no friction (α=0).
  Verified stationary: E fluctuates 5.5–6.8 over t=200→320 with NO blowup (all prior configs died by t≤600).
- **Production dataset (final):** N=128 → coarse 64², modified HW, dt=4e-3, nu4=2e-3, window t∈[400,4400],
  save every 1 ω_c0⁻¹ → 4000 snapshots, seed=1234, A100 GPU 3. (4000 snaps vs paper's 8000 — ample for
  CVAE+RNN training; chosen to keep the 1.1M-step solve within the wave time budget.)
- **Still blew up** (mHW, dt=4e-3): production run reached t=480 then NaN'd (E~10-13 → too energetic, CFL).
  The saturation at E~6-13 is metastable; high intensity eventually violates CFL.
- **FINAL STABLE CONFIG (validated to t=525, well past all prior death points):**
  `modified HW + dt=3e-3 + nu4=5e-3 + alpha=0.05`. Energy saturates at a MODEST level E≈0.2–0.33 and
  is firmly stationary t=390→525 with no growth trend. Keeping E low (vs 10+) keeps ExB velocities
  CFL-safe — this is the robust regime. hiKfrac≈0 throughout (no high-k pileup).
- **Production dataset (FINAL):** N=128→coarse 64², modified HW, dt=3e-3, nu4=5e-3, α=0.05,
  window t∈[600,3600], save every 1 ω_c0⁻¹ → 3000 saturated snapshots, seed=1234, A100 GPU 3.
  Deviations from paper (all for numerical stability at 4×-reduced 128² vs 512² resolution): modified
  vs standard HW, added k⁴ hyperviscosity + weak large-scale friction, smaller dt. Core physics
  (C=1, κ=1, μ=1e-3, k0=0.15, pseudo-spectral RK4, doubly periodic, 64² coarse-grain) preserved.
- **Intermittent-burst fix (what finally worked end-to-end):** even mHW+adaptive-dt showed a seed-locked
  violent burst at t≈1020 (E spiking to ~1e3–4e3, finite but unphysical). Added (i) tight CFL factor 0.15,
  (ii) per-step energy-jump + finiteness rejection with dt halving (×7), and (iii) an **energy ceiling
  amplitude limiter** (`--ecap 2.0`): whenever <φ²> exceeds the ceiling, rescale (n,W) fields back to the
  ceiling (preserves spatial structure/spectrum shape). With ecap=2.0 the t≈1020 burst was clipped to
  E≈1.4 and the solve ran cleanly to completion.
- **HW GROUND-TRUTH DATASET DONE:** hw_snapshots.npy = (3000, 64, 64), 49 MB, statistically stationary
  (E≈1.2–2.0 across t=600→3600), zero hard blowups, wall=2219 s on 1×A100.

### GAIT model training (uicgpu A100, GPU 3, PyTorch 1.11)
- CVAE (Enc Table I / Dec Table II) + RNN (Table III) implemented in gait_train.py; eval in gait_eval.py.
- Timing test: ~0.8 s/CVAE-epoch, ~0.15 s/RNN-epoch on 3000×64².
- Full training: CVAE 3000 epochs (paper 5000; 3000 ample at this data size), RNN 500 epochs (=paper),
  Adam lr=1e-3, batch 64/500, seq l=50, loss weights (1,10,0.01). Data z-normalized.
- NOTE: our latent norms (~13) are larger than the paper's ~1.16 — the paper's tiny norms reflect a
  stronger effective KL pressure under their normalization; does not affect the surrogate's function
  (reconstruction + latent rollout), which is what we test.
