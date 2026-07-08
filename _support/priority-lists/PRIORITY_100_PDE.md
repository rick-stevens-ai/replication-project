# PRIORITY_100_PDE — Top-100 PDE Papers for Replication

*Built 2026-06-20 14:28 CDT by Ollie. Refreshed with Wave 4 multi-judge audit verdicts.*

## Source mix
- **Rows 1-36**: existing PDE-replications/ dirs. Verdicts from `MASTER_SCORES_2026-06-20.csv` where available.
  - Wave 4 (5 papers, multi-judge 2026-06-20): pyclaw-wave4 PARTIAL, pdebench-wave4 SPOT-CHECK, mfem-wave4 NO-GO, fno-original-wave4 PARTIAL, fipy-wave4 SPOT-CHECK
- **Rows 37-86**: PDE NEXT-50 queue from `~/Dropbox/XFER/replication-atlas/pde_next50_queue/` (2026-06-10), atlas-gap-fill ranked.
- **Rows 87-100**: top 14 raw candidates from the 662-paper pool.

## AI ATLAS gap-fill priorities
- P021 ice-sheet basal friction (12 queued)
- P007 GRMHD / EHT black-hole imaging (10 queued)
- P001 dark-matter / cosmological emulators (10 queued)
- P080 storm-surge / tsunami surrogate (10 queued)
- P077 wind-farm LES + control (6 queued)
- P018 climate / cloud parameterization (2 queued — DEPRIORITIZED 2026-05-28 per Rick "skip climate papers")

## Standing policies
- Free endpoints only (Argo / Sophia / CELS chicago-1/2/4)
- AUDIT_PROTOCOL.md scope ≥80% AND claims ≥80% for REPLICATED
- Multi-judge (3 judges) for every NEW report

---

| Rank | Status | Paper / Project | Year | Atlas | Score | Verdict | Cov | Agr | DOI / Slug |
|---:|:---|:---|---:|:---|---:|:---|---:|---:|:---|
| 1 | IN-PROGRESS | amr-vs-mr-euler | — | — | — | — | — | — | `PDE-replications/amr-vs-mr-euler/` |
| 2 | IN-PROGRESS | apbs-pb | — | — | — | — | — | — | `PDE-replications/apbs-pb/` |
| 3 | IN-PROGRESS | dedalus | — | — | — | — | — | — | `PDE-replications/dedalus/` |
| 4 | IN-PROGRESS | deep-rl-amr-2022 | — | — | — | — | — | — | `PDE-replications/deep-rl-amr-2022/` |
| 5 | IN-PROGRESS | fast-poisson-spectral | — | — | — | — | — | — | `PDE-replications/fast-poisson-spectral/` |
| 6 | IN-PROGRESS | fem-vs-pinns | — | — | — | — | — | — | `PDE-replications/fem-vs-pinns/` |
| 7 | DONE-NEW-AUDIT | fipy-wave4 | — | — | — | SPOT-CHECK | 4 | 7 | `PDE-replications/fipy-wave4/` |
| 8 | IN-PROGRESS | flups-poisson | — | — | — | — | — | — | `PDE-replications/flups-poisson/` |
| 9 | IN-PROGRESS | fno-neuraloperator | — | — | — | — | — | — | `PDE-replications/fno-neuraloperator/` |
| 10 | DONE-NEW-AUDIT | fno-original-wave4 | — | — | — | PARTIAL | 5 | 5 | `PDE-replications/fno-original-wave4/` |
| 11 | IN-PROGRESS | galerkin-stochastic-burgers | — | — | — | — | — | — | `PDE-replications/galerkin-stochastic-burgers/` |
| 12 | IN-PROGRESS | godunov-loss | — | — | — | — | — | — | `PDE-replications/godunov-loss/` |
| 13 | IN-PROGRESS | jax-cfd | — | — | — | — | — | — | `PDE-replications/jax-cfd/` |
| 14 | IN-PROGRESS | kernel-active-subspaces | — | — | — | — | — | — | `PDE-replications/kernel-active-subspaces/` |
| 15 | IN-PROGRESS | kinetic-jl | — | — | — | — | — | — | `PDE-replications/kinetic-jl/` |
| 16 | IN-PROGRESS | koopman-no | — | — | — | — | — | — | `PDE-replications/koopman-no/` |
| 17 | IN-PROGRESS | laplace-no | — | — | — | — | — | — | `PDE-replications/laplace-no/` |
| 18 | IN-PROGRESS | latent-spectral-models | — | — | — | — | — | — | `PDE-replications/latent-spectral-models/` |
| 19 | IN-PROGRESS | lifex-cfd | — | — | — | — | — | — | `PDE-replications/lifex-cfd/` |
| 20 | IN-PROGRESS | lightning-laplace | — | — | — | — | — | — | `PDE-replications/lightning-laplace/` |
| 21 | IN-PROGRESS | lowrank-vlasov-poisson | — | — | — | — | — | — | `PDE-replications/lowrank-vlasov-poisson/` |
| 22 | IN-PROGRESS | marl-amr | — | — | — | — | — | — | `PDE-replications/marl-amr/` |
| 23 | DONE-NEW-AUDIT | mfem-wave4 | — | — | — | NO-GO | 1 | 0 | `PDE-replications/mfem-wave4/` |
| 24 | IN-PROGRESS | modal-space-stochastic-zhang-2019 | — | — | — | — | — | — | `PDE-replications/modal-space-stochastic-zhang-2019/` |
| 25 | IN-PROGRESS | modified-pnp | — | — | — | — | — | — | `PDE-replications/modified-pnp/` |
| 26 | IN-PROGRESS | optimized-schwarz-helmholtz | — | — | — | — | — | — | `PDE-replications/optimized-schwarz-helmholtz/` |
| 27 | IN-PROGRESS | pdebench | — | — | — | — | — | — | `PDE-replications/pdebench/` |
| 28 | DONE-NEW-AUDIT | pdebench-wave4 | — | — | — | SPOT-CHECK | 3 | 8 | `PDE-replications/pdebench-wave4/` |
| 29 | IN-PROGRESS | pinn-domain-decomp-2023 | — | — | — | — | — | — | `PDE-replications/pinn-domain-decomp-2023/` |
| 30 | IN-PROGRESS | pinn-rans-eivazi-2022 | — | — | — | — | — | — | `PDE-replications/pinn-rans-eivazi-2022/` |
| 31 | IN-PROGRESS | poisson-flow-generative | — | — | — | — | — | — | `PDE-replications/poisson-flow-generative/` |
| 32 | IN-PROGRESS | pwdg-helmholtz | — | — | — | — | — | — | `PDE-replications/pwdg-helmholtz/` |
| 33 | DONE-NEW-AUDIT | pyclaw-wave4 | — | — | — | PARTIAL | 6 | 9 | `PDE-replications/pyclaw-wave4/` |
| 34 | IN-PROGRESS | vlasov-poisson-dg-hermite | — | — | — | — | — | — | `PDE-replications/vlasov-poisson-dg-hermite/` |
| 35 | IN-PROGRESS | vqapoisson | — | — | — | — | — | — | `PDE-replications/vqapoisson/` |
| 36 | IN-PROGRESS | walk-on-stars | — | — | — | — | — | — | `PDE-replications/walk-on-stars/` |
| 37 | QUEUED | A Hybrid Deep Neural Operator/Finite Element Method for Ice-Sheet Modeling | 2023 | P021 | 9.01 | — | — | — | `10.48550/arxiv.2301.11402` |
| 38 | QUEUED | Forward and Inverse Modeling of Ice Sheet Flow Using Physics‐Informed Neural Networks: ... | 2024 | P021 | 8.46 | — | — | — | `10.1029/2024jh000169` |
| 39 | QUEUED | A Python library for solving ice sheet modeling problems using physics-informed neural ... | 2025 | P021 | 8.41 | — | — | — | `10.5194/gmd-18-5311-2025` |
| 40 | QUEUED | Hierarchical off-diagonal low-rank approximation of Hessians in inverse problems, with ... | 2023 | P021 | 7.97 | — | — | — | `10.1088/1361-6420/acd719` |
| 41 | QUEUED | Arctic sea ice data assimilation combining an ensemble Kalman filter with a novel Lagra... | 2023 | P021 | 7.5 | — | — | — | `10.5194/tc-17-1735-2023` |
| 42 | QUEUED | Using visible satellite images for model evaluation and data assimilation | 2021 | P021 | 7.4 | — | — | — | `10.5194/ems2021-308` |
| 43 | QUEUED | Comparison of adjoint and nudging methods to initialise ice sheet model basal conditions | 2016 | P021 | 7.33 | — | — | — | `10.5194/gmd-9-2549-2016` |
| 44 | QUEUED | Spatial probabilistic calibration of a high-resolution Amundsen Sea Embayment ice sheet... | 2019 | P021 | 7.31 | — | — | — | `10.5194/tc-14-1459-2020` |
| 45 | QUEUED | Towards a better ice sheet model initialisation and basal knowledge using data assimila... | 2016 | P021 | 7.21 | — | — | — | `10.5194/gmd-2016-7` |
| 46 | QUEUED | Regularized Coulomb Friction Laws for Ice Sheet Sliding: Application to Pine Island Gla... | 2019 | P021 | 7.01 | — | — | — | `10.1029/2019gl082526` |
| 47 | QUEUED | Time Series Classification of Supraglacial Lakes Evolution over Greenland Ice Sheet | 2024 | P021 | 6.93 | — | — | — | `10.1109/icmla61862.2024.00072` |
| 48 | QUEUED | Hyper-differential sensitivity analysis in the context of Bayesian inference applied to... | 2022 | P021 | 6.92 | — | — | — | `10.1615/int.j.uncertaintyquantification.2023047605` |
| 49 | QUEUED | First M87 Event Horizon Telescope Results. V. Physical Origin of the Asymmetric Ring | 2019 | P007 | 10.65 | — | — | — | `10.3847/2041-8213/ab0f43` |
| 50 | QUEUED | Modeling non-thermal emission from the jet-launching region of M 87 with adaptive mesh ... | 2019 | P007 | 10.08 | — | — | — | `10.1051/0004-6361/201936150` |
| 51 | QUEUED | The Event Horizon General Relativistic Magnetohydrodynamic Code Comparison Project | 2019 | P007 | 10.03 | — | — | — | `10.3847/1538-4365/ab29fd` |
| 52 | QUEUED | General relativistic magnetohydrodynamical κ-jet models for Sagittarius A | 2017 | P007 | 9.97 | — | — | — | `10.1051/0004-6361/201732025` |
| 53 | QUEUED | Accretion Flow Morphology in Numerical Simulations of Black Holes from the ngEHT Model ... | 2022 | P007 | 9.94 | — | — | — | `10.3390/galaxies11020038` |
| 54 | QUEUED | The Role of Adaptive Ray Tracing in Analyzing Black Hole Structure | 2021 | P007 | 9.93 | — | — | — | `10.3847/1538-4357/abee13` |
| 55 | QUEUED | GR-Athena++: General-relativistic Magnetohydrodynamics Simulations of Neutron Star Spac... | 2023 | P007 | 9.91 | — | — | — | `10.3847/1538-4365/ad87d4` |
| 56 | QUEUED | Black Hole–Disk Interactions in Magnetically Arrested Active Galactic Nuclei: General R... | 2024 | P007 | 9.88 | — | — | — | `10.3847/1538-4357/ad3ae2` |
| 57 | QUEUED | Generalized, Energy-conserving Numerical Simulations of Particles in General Relativity... | 2018 | P007 | 9.81 | — | — | — | `10.3847/1538-4365/aafcb3` |
| 58 | QUEUED | Radiative, two-temperature simulations of low luminosity black hole accretion flows in ... | 2016 | P007 | 9.18 | — | — | — | `10.1093/mnras/stw3116` |
| 59 | QUEUED | Introducing the DREAMS Project: DaRk mattEr and Astrophysics with Machine Learning and ... | 2024 | P001 | 11.88 | — | — | — | `10.3847/1538-4357/adb8e5` |
| 60 | QUEUED | Field-level Neural Network Emulator for Cosmological N-body Simulations | 2022 | P001 | 11.02 | — | — | — | `10.3847/1538-4357/acdb6c` |
| 61 | QUEUED | NECOLA: Toward a Universal Field-level Cosmological Emulator | 2021 | P001 | 10.91 | — | — | — | `10.3847/1538-4357/ac5c4a` |
| 62 | QUEUED | Evaluating machine learning techniques for predicting power spectra from reionization s... | 2018 | P001 | 10.81 | — | — | — | `10.1093/mnras/sty3168` |
| 63 | QUEUED | PySCo: A fast particle-mesh N-body code for modified gravity simulations in Python | 2024 | P001 | 10.81 | — | — | — | `10.1051/0004-6361/202452770` |
| 64 | QUEUED | Cosmological N-body simulations: a challenge for scalable generative models | 2019 | P001 | 10.8 | — | — | — | `10.1186/s40668-019-0032-1` |
| 65 | QUEUED | AbacusSummit: A Massive Set of High-Accuracy, High-Resolution N-Body Simulations | 2021 | P001 | 10.54 | — | — | — | `10.1093/mnras/stab2484` |
| 66 | QUEUED | A Physics-Informed, Machine Learning Emulator of a 2D Surface Water Model: What Tempora... | 2021 | P001 | 10.46 | — | — | — | `10.3390/w13243633` |
| 67 | QUEUED | Machine Learning‐Based Emulator for the Physics‐Based Simulation of Auroral Current System | 2024 | P001 | 10.32 | — | — | — | `10.1029/2023sw003720` |
| 68 | QUEUED | THE COYOTE UNIVERSE. III. SIMULATION SUITE AND PRECISION EMULATOR FOR THE NONLINEAR MAT... | 2009 | P001 | 10.31 | — | — | — | `10.1088/0004-637x/713/2/1322` |
| 69 | QUEUED | Physics-informed neural networks for tsunami inundation modeling | 2024 | P080 | 10.82 | — | — | — | `10.1016/j.jcp.2025.114066` |
| 70 | QUEUED | Implicit Adaptive Mesh Refinement for Dispersive Tsunami Propagation | 2023 | P080 | 8.79 | — | — | — | `10.1137/23m1585210` |
| 71 | QUEUED | An adaptive discontinuous Galerkin method for the simulation of hurricane storm surge | 2020 | P080 | 8.31 | — | — | — | `10.1007/s10236-020-01352-w` |
| 72 | QUEUED | Hybrid Modelling of Extreme Storm Processes and Navigation Risks in the Azov Sea Based ... | 2026 | P080 | 8.25 | — | — | — | `10.23947/2587-8999-2025-9-4-10-21` |
| 73 | QUEUED | Combining machine learning with computational hydrodynamics for prediction of tidal sur... | 2017 | P080 | 8.24 | — | — | — | `10.1016/j.piutam.2017.09.005` |
| 74 | QUEUED | Accelerating an Adaptive Mesh Refinement Code for Depth‐Averaged Flows Using GPUs | 2019 | P080 | 8.2 | — | — | — | `10.1029/2019ms001635` |
| 75 | QUEUED | SWEMniCS: a software toolbox for modeling coastal ocean circulation, storm surges, inla... | 2024 | P080 | 7.29 | — | — | — | `10.1038/s44304-024-00036-5` |
| 76 | QUEUED | Inundation Characteristics of Solitary Waves According to Revetment Type | 2022 | P080 | 7.29 | — | — | — | `10.3390/w14233814` |
| 77 | QUEUED | FNO Tsunami Flooding Simulation for Arbitrary Bathymetries, Shorelines, and Land Topogr... | 2024 | P080 | 7.25 | — | — | — | `10.1109/oceans55160.2024.10754544` |
| 78 | QUEUED | A MIXED GRID, GPU BASED, NON-LINEAR SHALLOW WATER SOLVER FOR RIVERINE, TSUNAMI, AND STO... | 2019 | P080 | 7.05 | — | — | — | `10.3850/38wc092019-0363` |
| 79 | QUEUED | A physics-guided machine learning framework for real-time dynamic wake prediction of wi... | 2024 | P077 | 9.38 | — | — | — | `10.1063/5.0194764` |
| 80 | QUEUED | Deep Neural Learning Based Distributed Predictive Control for Offshore Wind Farm Using ... | 2021 | P077 | 8.51 | — | — | — | `10.1109/tie.2020.2979560` |
| 81 | QUEUED | Machine Learning-Based Approach to Wind Turbine Wake Prediction under Yawed Conditions | 2023 | P077 | 8.32 | — | — | — | `10.3390/jmse11112111` |
| 82 | QUEUED | Applied Machine Learning to Study the Movement of Air Masses in the Wind Farm Area | 2024 | P077 | 8.22 | — | — | — | `10.3390/en17163961` |
| 83 | QUEUED | A parametric large-eddy simulation study of wind-farm blockage and gravity waves in con... | 2023 | P077 | 8.01 | — | — | — | `10.1017/jfm.2023.1088` |
| 84 | QUEUED | Predicting the benefit of wake steering on the annual energy production of a wind farm ... | 2020 | P077 | 7.77 | — | — | — | `10.1088/1742-6596/1618/2/022024` |
| 85 | QUEUED | Deep learning to represent subgrid processes in climate models | 2018 | P018 | 10.45 | — | — | — | `10.1073/pnas.1810286115` |
| 86 | QUEUED | Using Machine Learning to Parameterize Moist Convection: Potential for Modeling of Clim... | 2018 | P018 | 10.14 | — | — | — | `10.1029/2018ms001351` |
| 87 | CANDIDATE | GX: a GPU-native gyrokinetic turbulence code for tokamak and stellarator design | 2022 | P071 | 11.72 | — | — | — | `10.1017/s0022377824000631` |
| 88 | CANDIDATE | Using HPC infrastructures for deep learning applications in fusion research | 2021 | P071 | 11.59 | — | — | — | `10.1088/1361-6587/ac0a3b` |
| 89 | CANDIDATE | Special issue: Machine learning methods in plasma physics | 2023 | P071 | 11.06 | — | — | — | `10.1002/ctpp.202300060` |
| 90 | CANDIDATE | Efficient training sets for surrogate models of tokamak turbulence with Active Deep Ens... | 2023 | P071 | 10.65 | — | — | — | `10.1088/1741-4326/ad240d` |
| 91 | CANDIDATE | Kinetic modeling of neutral transport for a continuum gyrokinetic code | 2022 | P071 | 10.64 | — | — | — | `10.1063/5.0087131` |
| 92 | CANDIDATE | Gyrokinetic simulations of plasma turbulence in a Z-pinch using a moment-based approach... | 2022 | P071 | 10.61 | — | — | — | `10.1017/s0022377823000284` |
| 93 | CANDIDATE | Gyrokinetic simulations of neoclassical electron transport and bootstrap current genera... | 2023 | P071 | 10.57 | — | — | — | `10.1063/5.0148138` |
| 94 | CANDIDATE | $\texttt{matryoshka}$: Halo Model Emulator for the Galaxy Power Spectrum | 2021 | P001 | 9.88 | — | — | — | `10.1093/mnras/stac239` |
| 95 | CANDIDATE | Data‐Driven Equation Discovery of a Cloud Cover Parameterization | 2023 | P018 | 9.88 | — | — | — | `10.1029/2023ms003763` |
| 96 | CANDIDATE | Inferring dark matter substructure with astrometric lensing beyond the power spectrum | 2021 | P001 | 9.87 | — | — | — | `10.1088/2632-2153/ac494a` |
| 97 | CANDIDATE | The scatter in the galaxy–halo connection: a machine learning analysis | 2022 | P001 | 9.86 | — | — | — | `10.1093/mnras/stac1609` |
| 98 | CANDIDATE | Calibrating Cosmological Simulations with Implicit Likelihood Inference Using Galaxy Gr... | 2022 | P001 | 9.85 | — | — | — | `10.3847/1538-4357/aca8fe` |
| 99 | CANDIDATE | Physics-informed neural networks in the recreation of hydrodynamic simulations from dar... | 2023 | P001 | 9.84 | — | — | — | `10.48550/arxiv.2303.14090` |
| 100 | CANDIDATE | Sesame: A power spectrum emulator pipeline for beyond-Lambda CDM models | 2023 | P001 | 9.84 | — | — | — | `10.1051/0004-6361/202347892` |

## Provenance
- Source A: `~/Dropbox/REPLICATE-PROJECT/PDE-replications/*/` (36 dirs)
- Source B: `~/Dropbox/XFER/replication-atlas/pde_next50_queue/PDE_NEXT50_REPLICATION_QUEUE_2026-06-10.tsv`
- Source C: `~/Dropbox/XFER/replication-atlas/pde_next50_queue/PDE_NEXT50_CANDIDATES_RAW_2026-06-10.tsv`
- Verdict mapping: `MASTER_SCORES_2026-06-20.csv` (refreshed today with 23 multi-judge rows)