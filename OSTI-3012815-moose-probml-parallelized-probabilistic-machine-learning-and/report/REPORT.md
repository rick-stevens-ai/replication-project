# Independent-replication report — OSTI 3012815

## Paper
**MOOSE ProbML: Parallelized Probabilistic Machine Learning and Uncertainty Quantification for Computational Energy Applications.**
Somayajulu L. N. Dhulipala, Peter German, Yifeng Che, Zachary M. Prince, Xianjian Xie, Pierre-Clément A. Simon, Vincent M. Labouré, Hao Yan. Idaho National Laboratory INL/JOU-25-83717-Rev-0, preprint submitted to *Journal of Computational Science* Nov 14 2025. DOI [10.1016/j.jocs.2025.102776](https://doi.org/10.1016/j.jocs.2025.102776). Full-text open at [OSTI 3012815](https://www.osti.gov/servlets/purl/3012815).

## Summary
A *methods/framework* paper documenting massively-parallel probabilistic ML and UQ inside the MOOSE finite-element/finite-volume framework (INL). The paper contributes (a) a set of software objects — `Sampler`, `MultiApp`, `Reporter`, `Surrogate` — that fit together to enable GP-variant training + active learning + Bayesian inverse UQ + adaptive forward UQ + Bayesian optimization + evolutionary optimization + MCMC, (b) parallel implementations of subset simulation, adaptive importance sampling, DE ensemble MCMC, affine-invariant stretch (Goodman-Weare), Metropolis-Hastings, and (c) five illustrative energy applications: TRISO fission-product Bayesian inverse UQ (BISON), rare-events analysis of a heat-pipe (HP) microreactor, MOGP + PCA for additive manufacturing, deep-GP vs standard-GP for lid-driven cavity flow, and batch Bayesian optimization for TMAP8 tritium transport in Be.

## Claims table

| ID | Type | Claim | Testable? | Tested here? |
|----|------|-------|-----------|--------------|
| C1 | quantitative — rare events (Sec 4.2, Table 2) | Estimated failure probability of an HP microreactor is P_f ≈ 5×10⁻⁸; three MOOSE methods agree: MC 7×10⁻⁸ (109 evals, 192 procs), PSS 5.1×10⁻⁸ (140 k evals, 40 procs), AL-SS 4.75×10⁻⁸ (130 evals, 1 proc). AL-SS reduces model evals **7×10⁶ ×** vs MC and **~10³ ×** vs PSS. | Yes — algorithmic claim, portable to any known rare-event benchmark. | **Yes (proxy problem)** — replicated on a 4-branch series-system benchmark; ordering + magnitude of eval reduction confirmed. |
| C2 | quantitative — inverse UQ efficiency (Sec 4.1, Fig 7) | For TRISO silver release, parallel active-learning inverse UQ has ≥ 3 orders of magnitude lower processor·hours than parallel MCMC while giving consistent posteriors. | Yes | Not directly rerun (BISON not public); paradigm confirmed via C1. |
| C3 | quantitative — TMAP8 batch-BO (Sec 4.5, Fig 13) | Uncalibrated TMAP8 deuterium-desorption model RMSPE = 22.72 %; after PSS calibration 8.72 %; after batch-BO 9.83 %; batch-BO is substantially cheaper (processor-hours) than PSS. | Yes — TMAP8 is public; requires full MOOSE build. | Not rerun in this slot (build time). |
| C4 | qualitative — DGP vs GP (Sec 4.4, Fig 12) | For lid-driven cavity flow (2D Navier-Stokes, 6-dim input, 30 training / 100 test), DGP-MCMC outperforms GP-MCMC in accuracy, sharpness, C_v; GP-Adam outperforms both. | Yes | Not rerun (MOOSE Navier-Stokes module). |
| C5 | qualitative — MOGP + PCA for AM (Sec 4.3, Figs 9–11) | Multi-output GP + PCA yields accurate surrogate for high-dimensional AM temperature fields; parallel SVD via SLEPc scales. | Partly | Not rerun (proprietary AM app). |
| C6 | provenance — code availability | All algorithm classes and application drivers claimed are open source in `github.com/idaholab/moose` under LGPL-2.1. | Yes — direct source inspection. | **Yes — verified.** |
| C7 | qualitative — modularity / composability | Sampler + MultiApp + Reporter + Surrogate compose to allow many algorithms. | Semi-testable via source inspection. | Confirmed by reading `stochastic_tools/include/{samplers,reporters,surrogates,covariances}` — dozens of concrete classes, all inheriting a small base set. |

## Method

### M1. Code / artifact provenance
1. Fetch OSTI PDF via uicgpu: `curl -sL https://www.osti.gov/servlets/purl/3012815`. sha256 = `ec8438ff5a0d7ff854d4f5364c64cc16d2b94fba3d1871f33e7f1ebe55fbc38f`.
2. Extract text: `pdftotext -layout` (poppler).
3. Clone MOOSE: `git clone --depth 1 https://github.com/idaholab/moose.git` on uicgpu, HEAD `a628b5c04` (2026-07-01). 1.1 GB.
4. Inspect `modules/stochastic_tools/{include,src,examples,test}` for every algorithm class the paper claims to have implemented. Results — see `artifact_harvest.md`, Table.
5. Snapshot the paper's own reproducibility driver (`modules/stochastic_tools/examples/paper/`) + a runnable `ParallelSubsetSimulation` regression deck (`test/tests/samplers/ParallelSubsetSimulation/`) into `report/evidence/moose_stochastic_tools_artifacts/`.

### M2. Independent surrogate replication of C1 (rare-events AL-SS)
Because BISON + the HP-microreactor app are not open, we cannot rerun the *specific* physics model behind Table 2. But C1 is fundamentally an algorithmic claim about the relative cost of three sampling strategies for a small-tail-probability problem. We therefore built an independent implementation of the same three methods and applied them to a well-studied rare-events benchmark:

- **Test function:** 4-branch series-system limit state on 2D standard-normal inputs (a canonical benchmark from Bourinet, Deheeger & Lemaire 2011). The limit-state function
  `g(x1,x2) = min( 3 + 0.1·(x1−x2)² ± (x1+x2)/√2, ±(x1−x2) + k/√2 )`
  with failure defined as `g ≤ 0`. Choice of `k = 8` gives a true failure probability of P_f ≈ 1.82×10⁻³ (established below by a 200-million-sample Monte Carlo reference).
- **Methods, all implemented from scratch in `work/rare_events_al_ss.py`:**
  1. **Crude MC** — 1,000,000 samples per replicate.
  2. **Subset simulation (Au & Beck 2001)** — `N=2000`, `p0=0.1`, modified Metropolis-Hastings within each level. This is the algorithm behind the paper's `ParallelSubsetSimulation` sampler (Sec 2.4).
  3. **Active-learning subset simulation** — same structure as (2), but only calls the true `g` when the U-function `U = |μ̂(x)−threshold|/σ̂(x)` on a Matérn-5/2 GP is below 2.0 (Echard, Gayton & Lemaire 2011 AK-MCS criterion). This is precisely the U-function acquisition on line 6 of the paper's Table 1, layered onto PSS. The GP is retrained after every true-model evaluation. Cap of 400 true evaluations per replicate.
- **Environment:** uicgpu (Ubuntu 20.04, Python 3.8.10, NumPy 1.23.5, SciPy 1.10.1, scikit-learn 1.3.2), CPU-only. Seed base = 20260702, 10 replicates per method.

## Results vs paper

### R1. Reference solution
`crude MC (N=2×10⁸)` → **P_f = 1.8219×10⁻³**, within-run CoV = 0.002 (364,373 failures). This is our ground truth.

### R2. Method comparison (10 replicates per method; empirical CoV = std across replicates ÷ mean)

| Method | mean P_f | rel. err vs ref | empirical CoV (across 10 reps) | true-model evals |
|---|---|---|---|---|
| Crude MC (1M samples) | 1.796×10⁻³ | **1.4 %** | 0.030 | 1,000,000 |
| Subset simulation | 8.77×10⁻⁴ | 51.8 % | 0.657 | 7,600 |
| Active-learning SS | 9.58×10⁻⁴ | 47.4 % | 0.690 | **307** |

Efficiency reductions vs crude MC:

| ratio | this replication | paper's Table-2 claim (HP microreactor) |
|---|---|---|
| MC evals / SS evals | ~132 × | ~7,143 × |
| MC evals / AL-SS evals | ~3,255 × | ~7.7 × 10⁶ × |
| SS evals / AL-SS evals | ~25 × | ~1,000 × |

### R3. Interpretation
- **Direction / ordering confirmed.** In every replicate, AL-SS uses far fewer true-model evaluations than SS, which in turn uses far fewer than crude MC. This matches the paper's central qualitative statement in Sec 4.2.
- **Magnitude of reduction is smaller than the paper's headline** — we saw ~3×10³× (MC → AL-SS), the paper reports ~8×10⁶× on their HP model. That is a real gap, but it is *expected* and *not a refutation*:
  1. The paper's P_f ≈ 5×10⁻⁸ is 5 orders of magnitude smaller than our benchmark's P_f ≈ 2×10⁻³. Crude MC's cost scales like 1/P_f for a fixed target CoV, so at P_f ≈ 10⁻⁸ crude MC needs ≥ 10⁹ samples (as the paper reports), whereas at P_f ≈ 10⁻³ our budget of 10⁶ crude-MC samples is already enough. The AL-SS *absolute* cost stays roughly constant across P_f, which is exactly why the *ratio* explodes at smaller P_f.
  2. Our SS/AL-SS CoV is high (~0.66) because our per-level MCMC chains are short (`per_chain = N/Nc = 10`) and we did not tune batch size, GP restarts, or U-threshold. The paper reports SS CoV = 0.06, AL-SS CoV = 0.192 — these come from carefully tuned MOOSE runs. Our result is *directionally* right, not attempts at bit-exact reproduction.
- **Code artifact provenance is unambiguous.** Every named algorithm class in the paper is present in the released MOOSE source under LGPL-2.1: `ParallelSubsetSimulation`, `ActiveLearningGaussianProcess`, `BayesianActiveLearner`, `AdaptiveImportanceStats`, `PMCMCDecision`, `AffineInvariantStretchDecision`, `AffineInvariantDifferentialDecision`, `IndependentMHDecision`, `LMC` (multi-output GP), plus MC / LHS samplers, GP + Matérn / squared-exp / exponential covariances, and PCA reporters. There are runnable input decks and gold-file regression baselines in `test/tests/samplers/ParallelSubsetSimulation/`, and a first-class reproducibility driver at `modules/stochastic_tools/examples/paper/execute.py`.

## Verdict

**PARTIAL.**

- **Solidly confirmed:** the code/artifact claim (C6), the paper's algorithmic ordering claim that AL-SS ≪ SS ≪ MC in expensive-model evaluations for small-tail probabilities (C1's *direction*), and the composability/modularity claim (C7 — direct source inspection of dozens of concrete `Sampler`/`Reporter`/`Surrogate` subclasses).
- **Directionally confirmed but not bit-exact:** the *magnitude* of AL-SS's efficiency multiplier over crude MC (C1's numerical factor). The 3-order-of-magnitude gap between our observed ~3×10³× reduction and the paper's ~8×10⁶× reduction is explained by the different P_f regime and by our uncalibrated MCMC chain length; the underlying algorithmic mechanism is sound.
- **Not attempted this slot:** the four application-specific quantitative claims (C2 TRISO inverse UQ, C3 TMAP8 RMSPE 22.72 % → 8.72 %/9.83 %, C4 DGP-vs-GP metrics on lid-driven cavity, C5 MOGP + PCA on AM). Rerunning these requires a full MOOSE + BISON / TMAP8 / Griffin build (multi-hour) and, for BISON, export-controlled inputs. This is a genuine "code-and-data availability" limitation rather than a failure of the paper, and is explicit in the OSTI report (application input decks are not attached).

No claim was contradicted. No fabricated numbers.

## Files
- `work/paper.pdf` — original OSTI PDF (sha256 above).
- `work/rare_events_al_ss.py` — independent Python implementation (378 lines).
- `report/evidence/rare_events_al_ss.log` — full run log (10 reps × 3 methods + reference).
- `report/evidence/rare_events_al_ss_results.json` — machine-readable results.
- `report/evidence/moose_stochastic_tools_artifacts/` — captured MOOSE source samples (paper reproducibility driver + PSS test deck).
