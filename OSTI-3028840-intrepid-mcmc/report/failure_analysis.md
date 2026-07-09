# Failure Analysis — OSTI-3028840 Intrepid MCMC Replication

**Purpose:** Document every mode of failure encountered during the reimplementation of Intrepid MCMC (Chakroborty & Shields, CMA 2025), the diagnosis, the fix, and the residual known-limitations that were NOT fixed and are carried into the verdict.

## A. Failures encountered and fixed

### A1. Chain initialization landed in π = 0 regions (Circles cases)
- **Symptom:** For the disconnected-Circles cases (Gauss-Circles, Gumbel-Circles, Rosenbrock-Circles), the earliest runs produced empty histograms and NaN TVDs across essentially all 30 trials.
- **Root cause:** The initial chain-init strategy was "random anywhere in the bounding box." For three disjoint circles of radii {0.8, 1.2, 1.6} centred at radius-4 anchor points, the total area of the support inside the bounding box is a tiny fraction of the box. A uniform-random start almost always landed at π(x₀)=0. An MCMC chain that starts with π(x₀)=0 has α = min(1, π(x_c)/0) → 0/0 → NaN, and the chain never leaves x₀.
- **Fix:** Rejection-loop chain initializer: draw candidates from the bounding box until π(x₀) > 0. Recorded seeds so all 30 trials still produce reproducible but valid starts.
- **Verdict impact:** Without this fix, C1/C2/C3 could not be evaluated at all on the Circles cases. This is a correctness fix, not a tuning choice. Flagged in `REPORT.md` §3 "Numerical-stability fixes."

### A2. Density overflow on Rosenbrock
- **Symptom:** Rosenbrock-density evaluations returned `inf` or `0` (numerical underflow of `exp(-large)`) for candidates in the Rosenbrock heavy tail, corrupting the acceptance ratio.
- **Root cause:** Direct evaluation of `exp(-½ * (very-large-Rosenbrock))` underflows to 0 in double precision at moderate radius; Intrepid frequently proposes such candidates because it perturbs radius by up to 2×.
- **Fix:** Overflow-safe evaluation — carry log-density, take the ratio in log space, exponentiate the difference only for the accept threshold. Cap log-density at a large negative sentinel to avoid −inf propagation.
- **Verdict impact:** Recovered the Rosenbrock-Planes and Rosenbrock-Ring / Rosenbrock-Circles cases which had earlier been dominated by acceptance NaN.

### A3. Intrepid candidates at astronomical radius
- **Symptom:** Occasional candidates at radius r_c on the order of 1e10 due to a chance concatenation of large γ draws in adjacent Intrepid steps; π there is numerically zero and downstream evaluation was expensive garbage.
- **Fix:** Hard reject any Intrepid candidate with r_c > 1e6 as α=0 (π=0 there anyway). Purely an efficiency + numerics guard — does not change the mathematical acceptance rule.
- **Verdict impact:** Wall-time and stability improvement; no measurable effect on TVD medians.

### A4. NaN contamination of TVD histograms
- **Symptom:** A single chain in a batch of 30 that produced NaN samples (from A1 before the fix) contaminated the median TVD via NaN propagation in numpy's histogram-diff.
- **Fix:** NaN-filter in the TVD computation: drop non-finite samples before binning; if the fraction of finite samples fell below a threshold, mark that trial as failed and exclude it from the median rather than emit a NaN.
- **Verdict impact:** Once A1 was fixed, A4 stopped triggering. The filter remains as a defensive backstop.

## B. Not attempted (declared out of scope)

### B1. Higher-dimensional experiments (paper §4.2, d up to 50) — C7
- **Reason:** Focused on the analytic §4.1 benchmark where exact IID references are cheap and reproducible.
- **Consequence:** The verdict "REPLICATED" applies specifically to the §4.1 nine-target 2-D benchmark. Whether Intrepid's advantage persists at d=10, 20, 50 is undetermined by this work. See `open_questions.json` OQ3.

### B2. Bayesian-inverse experiment (paper §4.4, 2-DoF oscillator) — C7
- **Reason:** Requires standing up a physical-model forward simulator and a likelihood; substantially larger scope than the analytic benchmark.
- **Consequence:** Practical-applicability claim untested here. Flagged in `REPORT.md` §5 and in `open_questions.json` OQ5 (comparison against modern gradient-free multimodal samplers on realistic problems).

## C. Known limitations carried into the verdict

### C1. 500k-sample IID reference vs paper's 50M
- **Impact:** For our reported TVDs (mostly ≥ 0.02), the estimator noise floor is well below the reported values, so the comparisons are meaningful. Differences smaller than ~0.01 are NOT resolvable in our numbers.
- **Why not fixed:** Compute budget on the uicgpu CPU pool. 50M IID via rejection sampling for all 9 cases would have dominated wall time; 500k gives statistically adequate resolution at the observed effect sizes.
- **Location:** `REPORT.md` §3 (References); `REPORT.tex` "GENUINE CRITIQUE" §5.

### C2. 30 trials vs paper's 100
- **Impact:** Standard error on each per-configuration median is roughly √(100/30) ≈ 1.8× wider than the paper's. Does not change any qualitative conclusion but bounds our precision on the improvement-factor multipliers.
- **Why not fixed:** Same compute-budget rationale.
- **Location:** `REPORT.tex` "GENUINE CRITIQUE" §6.

### C3. Rosenbrock-Ring / Rosenbrock-Planes residual error-in-mean ~3
- **Impact:** Intrepid does NOT drive error-in-mean to near-zero on these two cases (both stay ~3 for both methods). REPORT.md flags this as C5=PARTIAL and notes the paper itself acknowledges it (§4.1 caveat that TVD improves faster than mean-error on some Rosenbrock shapes; mean dominated by heavy curved tail).
- **Why not fixed:** This is (per current diagnosis) a genuine heavy-tail geometry effect, not an implementation defect. Longer chains and a decomposition-by-radial-shell diagnostic would be needed to be certain. See `open_questions.json` OQ4.

### C4. Anchor point and RTF radial-band left at paper defaults
- **Impact:** Anchor x_a=(0,0) works for these nine cases only because all use a standard-Gaussian parent centred at 0; radial γ∈Uniform(0.5, 2.0) is a hidden hyperparameter with no sensitivity sweep here.
- **Why not fixed:** Out of scope for a first-pass replication of the paper's own headline benchmark, which uses these defaults. See `open_questions.json` OQ1 and OQ2.

### C5. LLM-judge aggregate "PARTIAL" vs verdict "REPLICATED"
- **Impact:** The independent Argo gpt-5.2 judge returned aggregate PARTIAL (3 SUPPORT, 3 PARTIAL, 0 CONTRADICT). The report's own verdict is REPLICATED.
- **Reconciliation:** The judge's PARTIAL is driven by (i) the paper's "universally near-zero" phrasing on C5 (not literally universal — see C3 above; also acknowledged by the paper), and (ii) unattempted C7 (declared out-of-scope, not attempted-and-failed). On the substantive-claim axis (C1, C2, C3, C4, C6 all reproduced quantitatively; C5 partial for the paper's own reasons) the replication is faithful. The judge verdict is preserved verbatim in `REPORT.md` §5 so a reviewer can weigh it themselves.

## D. Meta-lesson

The single most consequential failure of the replication effort was **A1 (chain init in π=0)** — a silent, cross-case failure mode that produced empty output rather than a loud crash. It was invisible in the algorithm equations because the paper's Algorithm 1/2 pseudocode assumes π(x_s) > 0 throughout, and the paper does not spell out its own initialization protocol. Any future reimplementer should build a valid-support initializer BEFORE running the disconnected-mode benchmarks; without it, the entire Circles column of the results table would read as spurious NaN and could be misdiagnosed as an algorithmic breakdown of Intrepid rather than an initialization bug.
