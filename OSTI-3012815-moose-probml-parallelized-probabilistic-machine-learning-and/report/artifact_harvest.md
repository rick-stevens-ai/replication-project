# Artifact harvest — OSTI 3012815

## Paper PDF
| what | URL | size | sha256 |
|---|---|---|---|
| Full paper | https://www.osti.gov/servlets/purl/3012815 | 4,726,725 B | `ec8438ff5a0d7ff854d4f5364c64cc16d2b94fba3d1871f33e7f1ebe55fbc38f` |

Preprint report ID: INL/JOU-25-83717-Revision-0. Preprint submitted to *Journal of Computational Science*, November 14, 2025. DOI 10.1016/j.jocs.2025.102776.

## MOOSE stochastic_tools module (independent code inspection)
- Cloned: `https://github.com/idaholab/moose.git` on uicgpu 2026-07-02 08:13 CDT.
- HEAD commit: `a628b5c041d25281b358585d1657e29f05b2bb1d` (Merge #33111, 2026-07-01 16:48:53 -0700).
- Checkout size: 1.1 GB. License: LGPL 2.1 (per source-file preambles).

### Algorithm-class headers verified to exist (all under `modules/stochastic_tools/include/`):
| Paper claim | File(s) verified present |
|---|---|
| GP + variants (Table 1, Sec 2.1.1) | `covariances/{CovarianceFunctionBase,SquaredExponentialCovariance,MaternHalfIntCovariance,ExponentialCovariance}.h`, `surrogates/GaussianProcessSurrogate.*` |
| Multi-Output GP / LMC (Sec 2.1.2, App. 4.3) | `covariances/LMC.{h,C}` |
| Active-learning GP (Sec 2.2) | `surrogates/ActiveLearningGaussianProcess.h`, `reporters/{ActiveLearningGPDecision,ActiveLearningReporterBase,GenericActiveLearner,BayesianActiveLearner,BiFidelityActiveLearningGPDecision}.h`, `samplers/{ActiveLearningMonteCarloSampler,GenericActiveLearningSampler,BayesianActiveLearningSampler,AISActiveLearning}.h` |
| Parallel Metropolis-Hastings / MCMC (Sec 2.3) | `reporters/{PMCMCDecision,IndependentMHDecision}.h` |
| Affine-invariant stretch sampler (Goodman-Weare) | `reporters/AffineInvariantStretchDecision.h` |
| Differential-evolution ensemble MCMC | `reporters/AffineInvariantDifferentialDecision.h` |
| Adaptive importance sampling (Sec 2.4) | `reporters/AdaptiveImportanceStats.h`, `reporters/AdaptiveMonteCarloDecision.h` |
| Parallel subset simulation (Sec 2.4) | `samplers/ParallelSubsetSimulation.h` (+ `test/tests/samplers/ParallelSubsetSimulation/` with runnable `pss.i`, `pss_cli.i`, `sub.i`, gold-file baselines) |
| Linear PCA / parallel SVD via SLEPc (Sec 2.5) | `reporters/SingularTripletReporter.h`, `reporters/SnapshotContainerBase.h`, `reporters/ParallelSolutionStorage.h` |

### Runnable examples captured
- `examples/paper/` — 3D transient diffusion sub-app + Monte Carlo driver used for the paper's memory/timing/weak-scaling benchmarks. Includes `execute.py` reproducibility driver that supports `--run`, `--replicates`, `--memory-levels`, `--weak-levels`.
- `test/tests/samplers/ParallelSubsetSimulation/` — includes gold-file regression baselines.
- Copies saved locally under `report/evidence/moose_stochastic_tools_artifacts/`.

### Not attached to the OSTI PDF
- Bit-identical input decks for the five application demos (Sec 4.1–4.5) — those live in downstream INL apps: BISON (fission-product silver release), the HP microreactor app (rare-events), an AM process app (MOGP+PCA), Navier-Stokes lid-driven-cavity deck (Dhulipala et al. 2024 [77]), and TMAP8 val-2b. BISON is export-controlled (not public), TMAP8 is public. This is a known limitation of DOE-lab replication.

## Independent surrogate replication
- Script: `work/rare_events_al_ss.py` (RNG_SEED 20260702).
- Environment: uicgpu, Python 3.8.10, NumPy 1.23.5, SciPy 1.10.1, scikit-learn 1.3.2, CPU-only.
- Outputs: `report/evidence/rare_events_al_ss.log`, `report/evidence/rare_events_al_ss_results.json` (sha256 `58db58b815e044fa6c43d49a11fdda1556a7d946fb82916f0fccd97b02a4ab9d`).
