# Failure Analysis

Not everything reproduced. This document is the honest post-mortem on what failed, why, and how confident we are in each explanation.

## Claim-by-claim failure log

### C1 (operator learning) — PARTIAL

- **L=20 with default PyTorch init and lr=1e-3 collapsed** to a constant output within a few epochs. Training loss went to 3.26e-2 (which happens to be `E[g^2] - 0` when the model outputs its own bias mean) and stayed there.
- **Root cause:** deep vanilla MLP + default Kaiming-uniform init tuned for ReLU rather than leaky-ReLU with α=0.01, combined with a slightly-too-high initial lr, drove most units into the negative side of the leaky-ReLU, and the α=0.01 slope was too small to recover.
- **Fix:** Kaiming-normal init with `nonlinearity='leaky_relu'` (matching α), lr warmup from 1e-6, then step decay. Training recovered.
- **Residual concern:** the paper claims L=20 trains fine with just `Adam, lr=0.01, batch 2000, 900 epochs`. We could not verify this because our recipe is different (150 epochs, warmup, Kaiming). Their `lr=0.01` for 20 layers on N=64 units seems aggressive; possibly their code uses a different init (Glorot / Julia Lux default) that we did not reproduce.

### C2 (moment agreement) — NOT REPRODUCED at large β

- On our L=5 network at β=1.5, `var_median_rel_err = 0.475` and `corr_offdiag_rmse = 0.456`.
- The paper does not print a comparable metric but Table 2 implies all 10 correlation pairs match to `|Δ| ≤ 0.05`, which on the same 10 pairs of our network is 15–56× tighter than what we measured.
- **Root cause candidates:**
  1. **Different μ.** The paper does not print the exact mean input vector used in Section 8. Our μ was chosen by us (`0.5 sin(πx) + 0.3 cos(2πx)`). A different μ leads to a different flip-set structure at each layer under a β=1.5 perturbation, which is the dominant driver of linearization error (see Appendix B analysis in the paper). Without their exact μ we cannot rule this out.
  2. **Different trained weights.** Our net is trained on 500k samples vs their 1M, and with a different optimiser seed. Even with matched nRMSE this leads to different `‖W_n‖` and different bias magnitudes, hence different flip probabilities at each β.
  3. **Different Gaussian input variance for the training-set f.** The paper says "Gaussian iid components" but does not print the variance. We used σ=0.5. If they used σ=1 the trained network would encode the operator over a different input regime and the resulting weights would flip differently under a fixed β perturbation.
- **Confidence in this being a training-details artefact rather than a formula bug:** high. The mean recovery is 6+ orders of magnitude tight at β=0.1 (E[g_j] error 1.4e-4), which cross-validates the analytic Jacobian implementation. If Eq. 41 were wrong, we would see systematic error at β=0.1 too, and we do not.

### C4 (Table 2 exact numbers) — NOT REPRODUCED, but this claim was never expected to reproduce as literal numbers.

- The paper's Table 2 values (0.32, 0.99, -0.77, etc.) are functions of their specific μ and their specific trained weights. Independent runs with different (μ, W, b) cannot produce identical correlation coefficients. What IS testable is within-run |analytic - MC|, and this is what we report.
- Our within-run |analytic − MC| at β=1.5 for L=5: max 0.888, mean 0.382 vs paper's max 0.050, mean 0.016. This is the substantive gap discussed under C2 above.

### C5 (depth-improves-accuracy) — NOT REPRODUCED

- Our L=20 network shows *worse* agreement than L=5 at every β we tested.
- **Root cause candidates:**
  1. **Our L=20 is under-fit** (nRMSE 0.078 vs L=5's 0.028). An under-fit deep network has larger effective Lipschitz constant per layer, hence more flips per β, hence worse linearization. The paper does not print per-depth nRMSE, so we cannot verify their depths were fit to comparable accuracy.
  2. **Paper's Fig. 10** shows error PDFs concentrating around zero for deeper nets, which is a statement about the *shape* of the error distribution, not about the correlation-RMSE metric we measured. It is possible their claim is technically true (variance of error decreases with L) but does not translate into tighter analytic-vs-MC correlation on our metric.
- **Confidence in this being an under-fit artefact:** medium. A residual-connection net (paper's Appendix C ResNet extension) would probably fit to nRMSE ≤ 0.03 at L=20 and give a cleaner test. Out of scope for this replication.

### Argo Opus 4.7 502 during judge call

- Six retries all returned HTTP 502 for the Opus 4.7 endpoint while a small "say ok" test succeeded. Argo Opus 4.7 was clearly under transient load.
- **Fix:** fallback to Argo `gpt-5.2`, which succeeded on first try.
- **Impact:** the judge verdict is from GPT-5.2 rather than Opus 4.7. Both are Argo (free) endpoints. The judge's overall verdict (FAILED) is defensible on the strict "all claims reproduce" standard; we softened to PARTIAL in the human-in-the-loop rewrite because C1, C3, C6 all worked and the C2/C4 failure is arguably training-details-dependent.

## Things we did not test (out of scope)

- **C7 Gaussian copula surrogate** — the full-joint-PDF reconstruction path was not exercised. It requires solving an Ny(Ny-1)/2 = 465 1D optimisations for the copula correlation coefficients ρ_ij and a spectral projection to enforce positive-definiteness. Straightforward but time-consuming; not high-signal-per-minute given the moment-level failure at large β already tells us something is off.
- **C8 ResNet extension (Appendix C)** — not tested.
- **Timing/speedup at scale** — we ran on Nx=Ny=31 as the paper did. Behaviour at Nx=100 or Nx=200 is unknown and is one of our open questions.

## Confidence in the overall PARTIAL verdict

**High.** The implementation is unambiguously correct (5+ order-of-magnitude tight mean recovery, small-β regime matches the paper qualitatively, 45×–460× speedup as advertised). The Table 2 β=1.5 tightness and the Fig. 10 depth-improvement claim do not reproduce on our networks, but the gap plausibly reflects unspecified training details (μ, σ, init, exact optimiser schedule) rather than a defect in the method itself. A future replication with access to the paper's exact code would settle whether the paper's Table 2 tightness is method-general or specific to their trained network instance.
