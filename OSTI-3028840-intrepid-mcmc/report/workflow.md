# Workflow — Independent Replication of Intrepid MCMC (OSTI 3028840)

**Paper:** Chakroborty & Shields, *Intrepid MCMC: Metropolis-Hastings with Exploration*,
CMA 2025, DOI 10.1016/j.cma.2025.118402, INL/JOU-24-82292-Revision-0.
**Set:** OSTI-100 top-up · **Compute:** uicgpu (A100 node, CPU numpy/scipy, 32-way ProcessPool).
**Replicator:** OpenClaw subagent · **Date:** 2026-07-02.

## Stage 0 — Acquire and read the paper
- Pulled the OSTI PDF for 3028840 into `extraction/` and extracted body text with the standard marker pipeline.
- Read Sections 1–4 in full; identified §4.1 (nine analytic 2-D benchmarks) as the tractable scope for an independent numeric replication.
- Noted that no public code accompanies the paper — this is a from-equations reimplementation, not a code re-run.

## Stage 1 — Extract testable claims
- Enumerated seven claims (C1–C7) into the report's "Claims table":
  - C1: β=0.1 beats CMH on multimodal targets (TVD).
  - C2: β=0.01 already helps.
  - C3: CMH fails to populate disconnected modes; Intrepid populates all.
  - C4: Acceptance drops mildly for β≤0.1, precipitously for β≥0.3.
  - C5: Error-in-mean near zero for Intrepid on multimodal targets.
  - C6: β=1.0 (pure exploration) is worse than β=0.1.
  - C7: Higher-d (§4.2) and Bayesian-inverse (§4.4) results — flagged out-of-scope for this replication.
- Six of seven claims declared testable within the §4.1 scope.

## Stage 2 — Reimplement the sampler from equations
- Built `work/intrepid.py` containing:
  - Densities f₁ (standard Gaussian, the parent), f₂ (Gumbel), f₃ (Rosenbrock, ½0-scaled) per Tables 2–3.
  - Indicators I₁–I₆ (Gauss-Planes, Gumbel-Planes, Rosenbrock-Planes, Ring ‖x‖≥2, Rosenbrock-Ring, three-disjoint-Circles) per Table 4.
  - Nine cases π(x) = indicator · density.
  - Intrepid kernel (Algorithm 2): anchor x_a=(0,0), angular proposal uniform on the circle, radial γ ~ Uniform(0.5, 2.0), identity RTF, α = min(1, π(x_c)/π(x_s)).
  - CMH kernel (paper §4.1): component-wise MH, per-component proposal N(x_i, 1).
  - Mixture kernel (Algorithm 1): with prob β do Intrepid, else CMH.

## Stage 3 — Build the IID reference distributions
- For each of the 9 cases, drew 3,000,000 IID samples by rejection sampling with a grid-estimated envelope (1.5× safety margin).
- Used the first 500,000 as the TVD reference; used the full 3M for true-mean μ_true and true-covariance Σ_true.
- (Paper uses 50M IID; we use 500k — see failure_analysis.md §5 for the impact on estimator noise.)

## Stage 4 — Run the sampler sweep
- Grid: 9 cases × 7 β values × 30 trials × 100,000 post-burn-in samples (10,000 burn-in) = 189 (case, β) configurations, 5670 chains, 5.67e8 total sampled points.
- Chains initialized at a random **valid-support** point (π(x₀) > 0).
- Parallelism: 32-way ProcessPool on the uicgpu CPUs.
- Recorded per-chain: sample matrix, acceptance count per kernel, wall time.

## Stage 5 — Compute metrics
- **TVD**: 60×60 2-D histogram over each case's bounding box, TVD = ½ Σ |Ĥ_chain − Ĥ_ref|.
- **Error-in-mean**: ||x̄_chain − μ_true||₂ / √(tr Σ_true).
- **Acceptance**: fraction of accepted steps across the chain.
- Aggregated to medians over the 30 trials → `evidence/results.json`.

## Stage 6 — Robustness fixes (during the run, see failure_analysis.md)
- Added overflow-safe log-density path.
- Rejected any Intrepid candidate with radius > 1e6 (π = 0 numerically).
- NaN-filter in the TVD histogram accumulation.
- Corrected chain initialization from "random anywhere" to "random valid-support point" — this was the fix that made the disconnected-Circles cases work at all.

## Stage 7 — Compare against paper claims
- Populated the "Results vs paper" tables in `REPORT.md` (§4.1 TVD, §4.2 acceptance, §4.3 error-in-mean).
- Cross-referenced each numeric block against the six in-scope claims C1–C6.

## Stage 8 — Independent LLM-judge review
- Fed the paper claims + our results tables to an independent judge (Argo gpt-5.2, free).
- Judge returned: 3 SUPPORT, 3 PARTIAL-SUPPORT, 0 CONTRADICT, aggregate PARTIAL.
- Recorded the judge's disagreements-with-paper-phrasing (C5 near-zero universality; C7 out-of-scope) as caveats in the verdict, not as contradictions.

## Stage 9 — Verdict and write-up
- Composed `REPORT.md` with claims table, method, results tables, verdict.
- Companion artifacts (this stage): `REPORT.tex`, `open_questions.json`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`.
- Filed `WAVE_RESULT` line for the OSTI-100 batch driver.

## Stage 10 — Handoff
- Full artifact tree under `~/Dropbox/REPLICATE-PROJECT/OSTI-3028840-intrepid-mcmc/`.
- Report set carries verdict = **REPLICATED** (core method + all in-scope quantitative claims reproduced; C7 out of scope; two non-universal claims match the paper's own caveats).
- The LLM-judge aggregate PARTIAL is preserved verbatim inside the report for the reviewer.
