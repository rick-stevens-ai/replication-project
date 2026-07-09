# brief

Sun et al. 2024 ("Streamlining Ocean Dynamics Modeling with Fourier Neural
Operators", *Mathematics* 12:1483, OSTI 2477212) use DeepHyper's parallel
multi-objective Bayesian optimization to search architecture + training
hyperparameters for a 2D FNO surrogate of a 100-member SOMA ocean-surface
ensemble (parameter = Gent–McWilliams bolus diffusivity κ_GM ∈ [200, 2000]).
They also propose a composite MSE + negative-ACC loss. The paper reports that
(a) the composite loss beats pure MSE in three of four fields, (b) HPO-optimal
configurations beat the Modulus default baseline on all four fields for both
log(RSE) and log(1−ACC), and (c) autoregressive rollout over 30 days remains
stable for the optimized model while the baseline degrades quickly. We
independently reimplemented FNO2d (Li et al. 2021) from scratch and ran a
method spot-check on a synthetic circular-basin advection-diffusion ensemble
because the paper's SOMA ensemble is explicitly not publicly available; all
three qualitative claims reproduce. In a 2026-07-04 deepening pass, we
additionally trained an independent FNO1d from scratch on the canonical
Li et al. 2021 Section 5.1 benchmark (1D viscous Burgers, ν = 0.01,
1000 train / 200 test, s = 1024, 500 epochs) and verified both a low
relative-L2 test error (≈3.0 %) and the central FNO claim of resolution
invariance: the same trained weights evaluated at
s ∈ {256, 512, 1024, 2048, 4096} yield errors within 0.28 pp across a
16× resolution range. Verdict: PARTIAL (LLM-judged by Argo
`argo:gpt-5.2`).
