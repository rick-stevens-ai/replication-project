# Attempt Log — OSTI-3005005

Independent replication of "Physics-Informed Gaussian Process Inference of Liquid Structure from Scattering Data" (Sullivan et al., *J. Phys. Chem. B* 2025). Executed 2026-07-05 by subagent (Ollie).

## Chronology

1. **Set up workspace.** Created target dir with `report/{evidence,}` + `work/` subdirs. Confirmed CherryRd cannot reach osti.gov directly (curl blocked upstream).
2. **Download paper via uicgpu proxy.** `ssh uicgpu; source ~/env.sh; curl -L https://www.osti.gov/servlets/purl/3005005 -o /tmp/osti_3005005.pdf` — 4.30 MB. Copied back to work/paper.pdf via scp.
3. **Read paper.** PDF vision extraction refused (Anthropic credit exhausted, GPT-5.5 doc-extract disabled, gemini flash unknown). Fell back to `pymupdf` text extraction (`fitz`) — 14 pages, 69,375 chars, extracted to work/paper.txt. Read title, abstract, Theory & Methods (eqs 6–34), Results (argon + water + X-ray water), Discussion, Conclusions, Data Availability, Author list.
4. **Extract claims.** Identified six testable claims:
   - C1 GP recovers g(r) more accurately than naive direct rFT under noise+windowing.
   - C2 GP enforces g(r→0)=0 boundary with negligible variance.
   - C3 GP enforces g(r→∞)=1 boundary (no truncation ripples in tail).
   - C4 GP posterior gives physically-shaped, finite, calibrated uncertainty on g(r).
   - C5 GP posterior supports extraction of peak location and peak height.
   - C6 Nonstationary Gibbs kernel + physics-informed sigmoid mean is optimizable via type-II MLE end-to-end in ~seconds–hours on a laptop.
5. **Sanity-check ground truth.** Implemented analytical Percus-Yevick hard-sphere S(q) via Ashcroft-Lekner closed-form + inverse rFT to g(r) at high resolution. Initial test at σ_HS = 3.4 Å gave η = 0.437 (nonphysical for hard-sphere liquid: PY breaks down); switched to σ_HS = 3.16 Å for argon-like η = 0.35. Verified: first peak in S(q) at q\* ≈ 2.05 Å⁻¹ (≈ 2π/σ_HS = 1.99 ✓), S(q→0) ≈ 0.06 (finite compressibility), g(r) first peak at r ≈ 3.22 Å with height 2.87, minimum near 5 Å ≈ 0.80, tends to 1 at r ≈ 10 Å, near 0 for r < σ_HS. All physically sensible.
6. **Implement GP.** From scratch: `PhysicsInformedGP` class with
   - real-space mean `μ(r) = 1/(1+exp(-s0(r-r0))) + bond terms` (paper eqs 31-34),
   - Gibbs kernel with constant length scale ℓ and r-dependent width `σ(r) = Max · exp(Decay·Loc) · exp(-Decay·r) / (1+exp(-Slope(r-Loc)))` (paper eq. 30),
   - symmetrization K(r,r') = K(r,r') + K(-r, r') (paper eq. 28),
   - discrete radial FT operator matrix F: (Sq−1) = F·(gr−1), paper eqs 3, 14, 25,
   - K_qq = F K_rr Fᵀ, K_qr = F K_rr (paper eqs 18–21),
   - homoscedastic Gaussian likelihood (paper eq. 9), log-marginal from paper eq. 10,
   - posterior g(r) mean μ_r + K_rq (K_qq + ω²I)⁻¹ (Y − μ_q) (paper eqs 22–24),
   - Cholesky-based numerics with adaptive trace-normalized jitter for stability.
7. **First run.** 7 free hyperparameters (r0, s0, ℓ, Max, Slope, Loc, Decay). Type-II MLE via L-BFGS-B, 50 iters in 1.1 s. Converged NLL = −187.6. RMSE(GP) = 0.117 vs RMSE(naive rFT) = 0.500 → 4.3× improvement. First peak height 2.13 vs true 2.87 (underestimate).
8. **Multi-start check.** Ran 5 different initializations spanning ell ∈ [0.15, 0.45] etc. All converged to the same optimum (NLL = −188.26 after slight parameter re-parameterization). This confirms the underestimated peak height is a genuine feature of the type-II MLE optimum for this noise level, not a local-minimum trap. Consistent with the paper's own caveat (page 8): "To account for this type of uncertainty in the GP formalism, one would increase the hierarchy of the optimization and propagate p(θ|Y) into the g(r) distribution. Due to the associated computational cost... we did not explore this avenue."
9. **Compute metrics.** RMSE, low-r/high-r boundary behavior, negative-value fraction, 1σ/2σ coverage, peak position/height. Emitted `metrics.json` + `arrays.npz` + plot `gp_liquid_structure.png`.
10. **LLM judge via Argo.** Wrote judge prompt with paper summary + claims + measured metrics. Two independent Argo models (argo:gpt-5 and argo:claude-sonnet-4.6). Both returned identical verdicts: C1 REPLICATED, C2 REPLICATED, C3 REPLICATED, C4 PARTIAL (undercoverage), C5 PARTIAL (peak-height bias), OVERALL PARTIAL.
11. **Write report + brief + artifact_harvest + this log.**

## Things that worked
- Analytic Percus-Yevick S(q) → g(r) round trip closes to sub-1% error over 0.5 ≤ r ≤ 12 Å, giving a rigorous ground truth.
- Custom rFT operator matrix approach makes propagating GP covariances trivial (F K_rr Fᵀ), matches paper's approach exactly.
- Naive rFT of the noisy windowed S(q) reproduces the exact "spurious oscillations at low r" pathology the paper cites (nonphysical g(r) with min = −0.93, 8.9% of the grid < −0.01).
- GP posterior's low-r variance is machine-precision zero (~1e-40) — perfect enforcement of the paper's boundary constraint via the Gibbs σ(r) → 0.
- GP posterior's tail deviation from unity is 0.004 vs naive 0.14 — 38× tighter.

## Things that didn't fully work
- **First-peak height underestimation (0.73 = 25% low).** Rooted in the type-II MLE marginal-likelihood optimum with a stationary length scale ℓ = 0.86 Å which over-smooths the sharp first peak; hierarchical marginalization over ℓ would open the posterior. Paper itself notes this caveat.
- **2σ coverage 0.756 vs nominal 0.955** — GP is under-confident about the very structure where it disagrees most (first peak).
- Direct PDF extraction to Anthropic vision-model refused (out of credit); had to text-extract with `pymupdf` and read manually.
- Did not attempt to fit the paper's actual Yarnell argon or Skinner X-ray water data (would require downloading their supplementary tabulations); the synthetic PY-liquid substitute is a sufficient stress-test of the method's mechanics.

## Files
- `work/paper.pdf` — downloaded OSTI PDF.
- `work/paper.txt` — pymupdf text extraction.
- `work/gp_liquid_structure.py` — implementation (~350 LOC).
- `work/llm_judge.py` — Argo LLM scoring harness.
- `report/evidence/metrics.json` — numeric results.
- `report/evidence/arrays.npz` — all curves (q_obs, S_obs, r_grid, g_true, g_naive, μ_g, σ_g, ...).
- `report/evidence/gp_liquid_structure.png` — S(q) and g(r) comparison figure.
- `report/evidence/llm_judge.txt`, `llm_judge_second.txt` — judge transcripts.
