# Non-LUCID Resource / Tools / Methods Ledger Extract

Scope: replication entries **1–66** in `REPLICATION_EVALUATION_REPORT.tex`, excluding all `LUCID-replications/` directories. Includes Wave 5 gap-fill papers: FFNO, Jouvet, Yuval–O'Gorman, HARMPI, Rasp, and Duthé/PyWake/SOWFA-WindFarm.

Primary sources: `scoring/replication_ledger_v4.jsonl`, `MASTER_RESOURCE_LEDGER_2026-05-31.json`, source `REPORT*.md` files, and the master report quick-reference scores. Scores in this extract follow the master report quick-reference table for entries 1–66; resource estimates preserve explicit parsed values where available and mark heuristics in each record.

## Totals

- Records: **66**
- Estimated CPU: **14648.7 min** (244.15 core-h)
- Estimated GPU: **253.25 GPU-h**
- Estimated LLM tokens: **16,970,000** (null/0 where absent; heuristics marked per record)
- TODO/unmatched records: **0**

## Verdict Counts

- PARTIAL: 50
- REPLICATED: 6
- SPOT-CHECK: 4
- NO-GO: 3
- UNKNOWN: 2
- FAILED: 1

## Method Frequency Counts

- direct code execution: 64
- data extraction/digitization: 58
- benchmark/evaluation: 55
- simulation: 53
- parameter fitting/regression: 41
- training/fine-tuning: 37
- analytic verification: 25
- inference-only: 21
- from-scratch reimplementation: 15
- molecular dynamics simulation: 1
- Markov state model estimation: 1
- observable operator model correction: 1
- timescale comparison: 1
- classifier training: 1
- generative model fine-tuning: 1
- molecular filtering: 1
- clustering: 1

## Tool / Framework Frequency Counts

- Python: 56
- Matplotlib: 44
- Argo/Claude/GPT LLM: 30
- PyTorch: 18
- NumPy: 16
- SciPy: 16
- CUDA: 13
- NCBI/SRA/RefSeq: 9
- TensorFlow: 6
- BV-BRC/PATRIC: 6
- BLAST: 6
- xarray/netCDF: 6
- OpenMP: 4
- MPI: 4
- FEniCS/FEM: 4
- SPAdes: 4
- Zenodo: 4
- NeuralOperator/FNO: 3
- scikit-learn: 3
- Prokka: 3
- Roary: 3
- uicgpu 8xA100: 2
- IQ-TREE: 2
- Quantum ESPRESSO: 2
- pandas: 2
- HuggingFace/Transformers: 2
- JAX: 2
- MMseqs2: 1
- OpenMM: 1
- MSM/OOM custom code: 1
- HMMER: 1
- MAFFT: 1
- PeleC: 1
- RDKit: 1
- GPT-2/HuggingFace: 1
- numpy: 1
- OpenDSS: 1
- LAMMPS: 1
- OpenFOAM: 1
- FastTree: 1
- DeepXDE: 1

## Major Compute Consumers

- **2396968** — GPU 72.00 h; CPU 18.08 h; tokens 220000; Latent Stochastic Differential Equations for Modeling Quasar Variability
- **PVMol-Gen-Fajar2026** — GPU 68.00 h; CPU 4.00 h; tokens 2400000; Generative AI-Driven Accelerated Discovery of Passivation Molecules for Perovskite Solar Cells
- **1565592-MSM-Hempel** — GPU 48.00 h; CPU 2.00 h; tokens 1600000; Markov State Models from Short Non-Equilibrium Trajectories via Observable Operator Models
- **34325466** — GPU 10.00 h; CPU 100.00 h; tokens 170000; Centenarian Bile Acid Pathways (Sato 2021)
- **1861801** — GPU 9.00 h; CPU 1.00 h; tokens 210000; NukeLM Domain Language Models
- **1868518** — GPU 5.60 h; CPU 6.40 h; tokens 120000; Learning Sequential Distribution System Restoration via Graph Reinforcement Learning
- **2306.17648** — GPU 4.50 h; CPU 1.00 h; tokens 220000; Domain-Decomp PINNs (Kopaničáková 2023)
- **1905.01205** — GPU 4.00 h; CPU 3.00 h; tokens 170000; Modal-Space Stochastic PDE (Zhang 2019)
- **BVBRC-01** — GPU 4.00 h; CPU 1.00 h; tokens 220000; ST11 CRKP Genomic Evolution (Zhang 2022)
- **EGU-2026-1909** — GPU 3.40 h; CPU 1.00 h; tokens 220000; F-FNO Tsunami Surrogate
- **1484740** — GPU 3.00 h; CPU 1.00 h; tokens 110000; Electronic and optical properties of two-dimensional GaN
- **2102.01010** — GPU 2.00 h; CPU 1.00 h; tokens 170000; ML-Accelerated CFD (Kochkov 2021)
- **10.1017/jog.2022.41** — GPU 1.70 h; CPU 1.00 h; tokens 170000; IGM Ice-Flow Inversion
- **2587579** — GPU 1.50 h; CPU 1.00 h; tokens 170000; Mesh-based Super-Resolution Multiscale GNN
- **10.1088/1742-6596/2505/1/012014** — GPU 1.25 h; CPU 2.30 h; tokens 170000; Duthé/PyWake Wind-Farm GNN

## Per-record Short Ledger

### 1997354
- **Title:** Integer Sequences from Configurations in the Hausdorff Metric Geometry
- **Domain:** Mathematics
- **Verdict / scores:** PARTIAL — coverage 10, agreement 10
- **Methods:** direct code execution, simulation, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python
- **Artifacts:** code 7 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Extension beyond m,n≤6 to validate higher-order formulas at scale

### 1379592
- **Title:** Mathematical Foundations of the GraphBLAS
- **Domain:** CS/Graph Algorithms
- **Verdict / scores:** REPLICATED — coverage 9, agreement 10
- **Methods:** direct code execution, from-scratch reimplementation, inference-only, simulation, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, Matplotlib
- **Artifacts:** code 5 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Large-scale performance benchmarks (paper is mostly definitional, so minor)

### 1523841
- **Title:** Quantitative relationship between polarization differences and zone-averaged polarization
- **Domain:** Materials/Condensed Matter
- **Verdict / scores:** PARTIAL — coverage 7, agreement 10
- **Methods:** direct code execution, data extraction/digitization, analytic verification
- **Tools:** Python, NumPy, Matplotlib
- **Artifacts:** code 2 files; data/source files listed in JSON
- **Compute:** CPU 1.02 min (estimated=False), GPU 0.0 h (estimated=True)
- **Main blocker:** General N-band formula (Section III / Eq. 17)

### 2441075
- **Title:** Exactly solved model of light-scattering errors in quantum simulations with metastable states
- **Domain:** Quantum/AMO
- **Verdict / scores:** PARTIAL — coverage 8, agreement 9
- **Methods:** direct code execution, simulation, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, Matplotlib
- **Artifacts:** code 10 files; data/source files listed in JSON
- **Compute:** CPU 0.18 min (estimated=False), GPU 0.0 h (estimated=True)
- **Main blocker:** Penning-trap 2D triangular-lattice ion-crystal mode structure

### 1624105
- **Title:** Clustering huge protein sequence sets in linear time
- **Domain:** Bio/Bioinformatics
- **Verdict / scores:** SPOT-CHECK — coverage 8, agreement 9
- **Methods:** direct code execution, from-scratch reimplementation, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, NumPy, MMseqs2
- **Artifacts:** code 4 files; data/source files listed in JSON
- **Compute:** CPU 2.16 min (estimated=False), GPU 0.0 h (estimated=True)
- **Main blocker:** Production MMseqs2 C++ binary run on UniRef50/UniRef100 (1e8-1e9 sequences)

### 1606674
- **Title:** Common Mode Voltage Reduction of Single-Phase Quasi-Z-Source Inverter-Based PV System
- **Domain:** Power/Electronics
- **Verdict / scores:** REPLICATED — coverage 8, agreement 9
- **Methods:** direct code execution, simulation, benchmark/evaluation
- **Tools:** Python, NumPy, Matplotlib
- **Artifacts:** code 1 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Experimental hardware prototype

### 1565592-MSM-Hempel
- **Title:** Markov State Models from Short Non-Equilibrium Trajectories via Observable Operator Models
- **Domain:** Computational Chemistry
- **Verdict / scores:** None — coverage 9, agreement 8
- **Methods:** molecular dynamics simulation, Markov state model estimation, observable operator model correction, timescale comparison, benchmark/evaluation
- **Tools:** Python, OpenMM, CUDA, NumPy, SciPy, MSM/OOM custom code, uicgpu 8xA100
- **Artifacts:** code 31 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=False), GPU 48.0 h (estimated=False)
- **Main blocker:** Exact force field reproduction (we used ff14SB, paper's choice unclear)

### 1461824
- **Title:** Approximating Photo-z PDFs for Large Surveys
- **Domain:** Astrophysics/Cosmology
- **Verdict / scores:** PARTIAL — coverage 8, agreement 8
- **Methods:** direct code execution, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, SciPy, Matplotlib
- **Artifacts:** code 1 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Actual BPZ-processed mock catalogs (Graham et al. 2018 / Buzzard / Millennium)

### 1842593
- **Title:** Motion Tomography via Occupation Kernels
- **Domain:** Control Theory
- **Verdict / scores:** PARTIAL — coverage 8, agreement 8
- **Methods:** direct code execution, inference-only, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, Matplotlib
- **Artifacts:** code 14 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Experiment 2: Real-world Gliderpalooza dataset from Chang et al. [5]

### 1412756
- **Title:** Chiral Spin Order in Kondo-Heisenberg Systems
- **Domain:** Materials/Condensed Matter
- **Verdict / scores:** PARTIAL — coverage 7, agreement 8
- **Methods:** direct code execution, from-scratch reimplementation, simulation, parameter fitting/regression, data extraction/digitization, analytic verification
- **Tools:** Python, NumPy, SciPy, Matplotlib
- **Artifacts:** code 4 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** 2D Ising critical exponent beta=1/8 (requires MC / field theory)

### 2217719
- **Title:** Molten Salt Reactor Neutronics and Fuel Cycle Modeling with SCALE
- **Domain:** Nuclear
- **Verdict / scores:** PARTIAL — coverage 6, agreement 8
- **Methods:** direct code execution, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, SciPy, Matplotlib
- **Artifacts:** code 4 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Full 3D SCALE/TRITON deterministic model with 1-group transport

### 2439897
- **Title:** Physics and chemistry from parsimonious representations
- **Domain:** Materials/Condensed Matter
- **Verdict / scores:** PARTIAL — coverage 6, agreement 8
- **Methods:** direct code execution, training/fine-tuning, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, Matplotlib, PyTorch
- **Artifacts:** code 6 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 1.0 h (estimated=True)
- **Main blocker:** Original STEM/SPM experimental datasets (proprietary / not linked)

### 1475143
- **Title:** FDTD: Solving 1+1D Delay PDE in Parallel
- **Domain:** Quantum/AMO
- **Verdict / scores:** PARTIAL — coverage 7, agreement 7
- **Methods:** direct code execution, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, Matplotlib, CUDA, OpenMP, Argo/Claude/GPT LLM
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 0.5 h (estimated=True)
- **Main blocker:** Figure 8 non-Markovian regime (requires ~125 GB memory)

### 3014512
- **Title:** Spin-Dependent Scattering of Sub-GeV Dark Matter
- **Domain:** Particle Physics
- **Verdict / scores:** PARTIAL — coverage 7, agreement 7
- **Methods:** direct code execution, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, NumPy, SciPy, Matplotlib
- **Artifacts:** code 7 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Figures 1-4 (mediator constraints: SN cooling, meson decays, SIDM, LHC)

### 2587225
- **Title:** ScaWL: Scaling k-WL Weisfeiler-Lehman Algorithms in Distributed Memory
- **Domain:** CS/Graph Algorithms
- **Verdict / scores:** PARTIAL — coverage 6, agreement 7
- **Methods:** direct code execution, simulation, data extraction/digitization
- **Tools:** Python, Matplotlib, MPI, OpenMP
- **Artifacts:** code 14 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 0.5 h (estimated=True)
- **Main blocker:** 3-WL experiments (memory prohibitive)

### 2571909
- **Title:** Physics-based hybrid machine learning for critical heat flux prediction
- **Domain:** Machine Learning
- **Verdict / scores:** NO-GO — coverage 6, agreement 7
- **Methods:** direct code execution, from-scratch reimplementation, training/fine-tuning, simulation, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, Matplotlib, PyTorch
- **Artifacts:** code 4 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 1.0 h (estimated=True)
- **Main blocker:** Real NRC CHF experimental database

### 2475938
- **Title:** Updated Virophage Taxonomy and Distinction from Polinton-like Viruses
- **Domain:** Bio/Bioinformatics
- **Verdict / scores:** REPLICATED — coverage 6, agreement 7
- **Methods:** direct code execution, benchmark/evaluation
- **Tools:** IQ-TREE, HMMER, MAFFT, NCBI/SRA/RefSeq
- **Artifacts:** code 6 files; data/source files listed in JSON
- **Compute:** CPU 240.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Full paper-scale genome collection (hundreds of genomes)

### 1427646
- **Title:** Deep Learning of Atomically Resolved STEM Images
- **Domain:** Materials/Condensed Matter
- **Verdict / scores:** PARTIAL — coverage 6, agreement 7
- **Methods:** direct code execution, from-scratch reimplementation, inference-only, training/fine-tuning, simulation, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, Matplotlib, PyTorch
- **Artifacts:** code 13 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 1.0 h (estimated=True)
- **Main blocker:** Full multislice simulation (Prismatic / abTEM) as training data

### 1983793
- **Title:** Simple Coplanar Waveguide Resonator Mask Targeting Multiplexed Superconducting-Qubit Readout
- **Domain:** Quantum/AMO
- **Verdict / scores:** PARTIAL — coverage 5, agreement 7
- **Methods:** direct code execution, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, Matplotlib, MPI, FEniCS/FEM, Argo/Claude/GPT LLM
- **Artifacts:** code 2 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 0.5 h (estimated=True)
- **Main blocker:** Full 3D FEM eigenmode simulation (Ansys HFSS or Palace)

### 1484740
- **Title:** Electronic and optical properties of two-dimensional GaN
- **Domain:** Materials/Condensed Matter
- **Verdict / scores:** NO-GO — coverage 5, agreement 7
- **Methods:** direct code execution, training/fine-tuning
- **Tools:** CUDA, MPI, OpenMP, Quantum ESPRESSO
- **Artifacts:** code 8 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 3.0 h (estimated=False)
- **Main blocker:** GW quasiparticle corrections (+3.37 eV monolayer, +2.68 eV bilayer)

### 1559043
- **Title:** Numerical study of ignition behavior of a post-discharge kernel in turbulent flow
- **Domain:** Engineering/Physics
- **Verdict / scores:** PARTIAL — coverage 6, agreement 6
- **Methods:** direct code execution, inference-only, simulation, parameter fitting/regression, data extraction/digitization
- **Tools:** Python, Matplotlib, CUDA, PeleC, Argo/Claude/GPT LLM
- **Artifacts:** code 57 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 0.25 h (estimated=True)
- **Main blocker:** Sustained self-propagating flame (needs ≥5 ms window)

### PVMol-Gen-Fajar2026
- **Title:** Generative AI-Driven Accelerated Discovery of Passivation Molecules for Perovskite Solar Cells
- **Domain:** Materials/Condensed Matter
- **Verdict / scores:** None — coverage 7, agreement 5
- **Methods:** classifier training, generative model fine-tuning, molecular filtering, clustering, benchmark/evaluation
- **Tools:** Python, PyTorch, RDKit, GPT-2/HuggingFace, CUDA, uicgpu 8xA100, pandas, numpy
- **Artifacts:** code 15 files; data/source files listed in JSON
- **Compute:** CPU 240.0 min (estimated=False), GPU 68.0 h (estimated=False)
- **Main blocker:** Matching classifier metrics (F1 0.656 vs 0.80) — root cause not identified

### 2571540
- **Title:** A Portfolio Approach to Massively Parallel Bayesian Optimization
- **Domain:** Machine Learning
- **Verdict / scores:** NO-GO — coverage 5, agreement 6
- **Methods:** direct code execution, from-scratch reimplementation, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, SciPy, Matplotlib, TensorFlow, Argo/Claude/GPT LLM
- **Artifacts:** code 5 files; data/source files listed in JSON
- **Compute:** CPU 720.0 min (estimated=False), GPU 1.0 h (estimated=True)
- **Main blocker:** Noisy benchmarks with replication allocation (Figs 3, 9)

### 1864334
- **Title:** Variational Monte Carlo calculations of A<=4 nuclei with neural-network wave functions
- **Domain:** Nuclear
- **Verdict / scores:** PARTIAL — coverage 5, agreement 6
- **Methods:** direct code execution, training/fine-tuning, simulation, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, Matplotlib, PyTorch
- **Artifacts:** code 28 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 1.0 h (estimated=True)
- **Main blocker:** AV6'/AV8' operator-dependent NN potential (used Minnesota central only)

### 1981773
- **Title:** Effect of Single Atom Pt Doping and Facet Dependence on LTO electronic/optical properties
- **Domain:** Materials/Condensed Matter
- **Verdict / scores:** PARTIAL — coverage 5, agreement 6
- **Methods:** direct code execution, simulation, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, Matplotlib, Quantum ESPRESSO, Argo/Claude/GPT LLM
- **Artifacts:** code 22 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 0.5 h (estimated=True)
- **Main blocker:** Second facet (010) comparison — paper's facet-dependence claim

### 2396968
- **Title:** Latent Stochastic Differential Equations for Modeling Quasar Variability
- **Domain:** Astrophysics/Cosmology
- **Verdict / scores:** PARTIAL — coverage 4, agreement 6
- **Methods:** direct code execution, from-scratch reimplementation, inference-only, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, Matplotlib, PyTorch, Argo/Claude/GPT LLM
- **Artifacts:** code 9 files; data/source files listed in JSON
- **Compute:** CPU 1084.8 min (estimated=False), GPU 72.0 h (estimated=False)
- **Main blocker:** 6-band LSST multivariate architecture

### 1275503
- **Title:** Cosmic Reionization On Computers: post-reionization IGM
- **Domain:** Astrophysics/Cosmology
- **Verdict / scores:** PARTIAL — coverage 5, agreement 5
- **Methods:** direct code execution, simulation, parameter fitting/regression, data extraction/digitization, analytic verification
- **Tools:** Python, NumPy, SciPy, Matplotlib
- **Artifacts:** code 2 files; data/source files listed in JSON
- **Compute:** CPU 3.0 min (estimated=False), GPU 0.0 h (estimated=True)
- **Main blocker:** Full 3D AMR hydrodynamics (ART code) with 100 pc resolution

### 1868518
- **Title:** Learning Sequential Distribution System Restoration via Graph Reinforcement Learning
- **Domain:** Power/Electronics
- **Verdict / scores:** PARTIAL — coverage 5, agreement 5
- **Methods:** direct code execution, from-scratch reimplementation, inference-only, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, Matplotlib, OpenDSS
- **Artifacts:** code 21 files; data/source files listed in JSON
- **Compute:** CPU 384.0 min (estimated=False), GPU 5.6 h (estimated=False)
- **Main blocker:** IEEE 8500-node scalability (the headline scale claim)

### 3003857
- **Title:** Divide and Conquer: learning chaotic dynamical systems with multi-step penalty neural ODEs
- **Domain:** Machine Learning
- **Verdict / scores:** PARTIAL — coverage 5, agreement 4
- **Methods:** direct code execution, inference-only, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, SciPy, Matplotlib, PyTorch, Argo/Claude/GPT LLM
- **Artifacts:** code 17 files; data/source files listed in JSON
- **Compute:** CPU 13.98 min (estimated=False), GPU 0.283 h (estimated=False)
- **Main blocker:** Section 4.3 Kolmogorov flow (2D NS turbulence)

### 2469515
- **Title:** Supervised extraction of near-complete genomes from metagenomic samples
- **Domain:** Bio/Bioinformatics
- **Verdict / scores:** SPOT-CHECK — coverage 4, agreement 10
- **Methods:** direct code execution, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, Matplotlib, BV-BRC/PATRIC, BLAST, SPAdes, NCBI/SRA/RefSeq, Argo/Claude/GPT LLM
- **Artifacts:** code 5 files; data/source files listed in JSON
- **Compute:** CPU 240.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** SEEDtk / RASTtk / PATRIC supervised pipeline

### 1609039
- **Title:** Cu64Zr36 Metallic Glass MD Deformation
- **Domain:** Materials Science
- **Verdict / scores:** PARTIAL — coverage 7, agreement 8
- **Methods:** direct code execution, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, NumPy, Matplotlib, PyTorch, CUDA, OpenMP, LAMMPS, Argo/Claude/GPT LLM
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 1.0 h (estimated=True)
- **Main blocker:** Post-yield serrated flow past 10% strain (capped at 6-8% strain)

### lightning-laplace
- **Title:** Lightning Laplace/Helmholtz Solvers
- **Domain:** Numerical PDE
- **Verdict / scores:** PARTIAL — coverage 8, agreement 10
- **Methods:** direct code execution, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, Matplotlib, FEniCS/FEM
- **Artifacts:** code 8 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** See source report; no additional blocker extracted into ledger.

### fast-poisson-spectral
- **Title:** Fortunato--Townsend Fast Poisson ADI
- **Domain:** Numerical PDE
- **Verdict / scores:** PARTIAL — coverage 9, agreement 10
- **Methods:** direct code execution, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, NumPy, SciPy, Matplotlib
- **Artifacts:** code 38 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** GitHub repository; paywalled/private/missing data; https://arxiv.org/abs/1710.11259

### 2582579
- **Title:** NILC Analytic Power Spectrum Formula
- **Domain:** CMB/Cosmology
- **Verdict / scores:** PARTIAL — coverage 8, agreement 8
- **Methods:** direct code execution, inference-only, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, NumPy, SciPy, Matplotlib, Argo/Claude/GPT LLM
- **Artifacts:** code 48 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=False), GPU 0.0 h (estimated=True)
- **Main blocker:** Cosmological parameter inference (deferred to unpublished Paper II)

### 2587579
- **Title:** Mesh-based Super-Resolution Multiscale GNN
- **Domain:** PDE / Scientific ML
- **Verdict / scores:** PARTIAL — coverage 8, agreement 8
- **Methods:** direct code execution, from-scratch reimplementation, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, Matplotlib, PyTorch, CUDA, OpenFOAM, Argo/Claude/GPT LLM
- **Artifacts:** code 42 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 1.5 h (estimated=False)
- **Main blocker:** Actual OpenFOAM BFS dataset (requires separate foamToVTK pipeline)

### 2587945
- **Title:** ELM Spatiotemporal NN Forecaster
- **Domain:** Fusion / ML
- **Verdict / scores:** PARTIAL — coverage 8, agreement 8
- **Methods:** direct code execution, inference-only, training/fine-tuning, simulation, parameter fitting/regression, benchmark/evaluation
- **Tools:** Python, Matplotlib, PyTorch, NeuralOperator/FNO, Argo/Claude/GPT LLM
- **Artifacts:** code 11 files; data/source files listed in JSON
- **Compute:** CPU 30.0 min (estimated=False), GPU 1.0 h (estimated=True)
- **Main blocker:** Real DIII-D BES data (not publicly released)

### 1861801
- **Title:** NukeLM Domain Language Models
- **Domain:** NLP / Domain LMs
- **Verdict / scores:** PARTIAL — coverage 8, agreement 10
- **Methods:** direct code execution, from-scratch reimplementation, inference-only, training/fine-tuning, benchmark/evaluation
- **Tools:** Python, PyTorch, HuggingFace/Transformers, Argo/Claude/GPT LLM
- **Artifacts:** code 40 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 9.0 h (estimated=False)
- **Main blocker:** Full 13K DAPT steps (did 4K on large)

### 1578031
- **Title:** fldgen v2.0 ESM Temperature--Precipitation Emulator
- **Domain:** Climate / Stats
- **Verdict / scores:** PARTIAL — coverage 8, agreement 8
- **Methods:** direct code execution, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, NumPy, SciPy, Matplotlib, xarray/netCDF, Zenodo, Argo/Claude/GPT LLM
- **Artifacts:** code 4 files; data/source files listed in JSON
- **Compute:** CPU 0.48 min (estimated=False), GPU 0.0 h (estimated=True)
- **Main blocker:** Real ESM dataset (NetCDF files in Git LFS)

### 1993311
- **Title:** DMQMC + GPR for electronic heat capacities and entropies
- **Domain:** DFT / Stats
- **Verdict / scores:** PARTIAL — coverage 8, agreement 8
- **Methods:** direct code execution, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** NumPy, SciPy, Matplotlib, scikit-learn, Argo/Claude/GPT LLM
- **Artifacts:** code 11 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Real DMQMC stochastic data (HANDE-QMC not compiled/run)

### 1984484
- **Title:** DRAS Deep RL HPC Cluster Scheduler
- **Domain:** Systems / RL
- **Verdict / scores:** PARTIAL — coverage 8, agreement 8
- **Methods:** direct code execution, inference-only, training/fine-tuning, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, NumPy, Matplotlib, PyTorch, Argo/Claude/GPT LLM
- **Artifacts:** code 6 files; data/source files listed in JSON
- **Compute:** CPU 10.98 min (estimated=False), GPU 1.0 h (estimated=True)
- **Main blocker:** Hierarchical two-network design (Level-1 select + Level-2 backfill)

### space-nanograv-15yr-gwb
- **Title:** NANOGrav 15-yr gravitational-wave background evidence
- **Domain:** Astrophysics / GW
- **Verdict / scores:** PARTIAL — coverage 8, agreement 8
- **Methods:** direct code execution, from-scratch reimplementation, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization
- **Tools:** Python, NumPy, Matplotlib, Argo/Claude/GPT LLM
- **Artifacts:** code 32 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Independent MCMC runs from scratch (weeks of CPU on clusters)

### space-bls-exoplanets
- **Title:** BLS Kepler Exoplanet Transit Detection
- **Domain:** Astrophysics / Exoplanets
- **Verdict / scores:** PARTIAL — coverage 8, agreement 8
- **Methods:** direct code execution, from-scratch reimplementation, inference-only, training/fine-tuning, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, Matplotlib, Argo/Claude/GPT LLM
- **Artifacts:** code 3 files; data/source files listed in JSON
- **Compute:** CPU 0.12 min (estimated=False), GPU 0.0 h (estimated=True)
- **Main blocker:** False-alarm rate (FAR) study with injected synthetic transits

### space-camels-emulator
- **Title:** CosmoPower-style P(k) Neural Emulator
- **Domain:** Cosmology / ML
- **Verdict / scores:** PARTIAL — coverage 8, agreement 8
- **Methods:** direct code execution, training/fine-tuning, simulation, parameter fitting/regression, analytic verification, benchmark/evaluation
- **Tools:** Matplotlib
- **Artifacts:** code 6 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 0.1 h (estimated=False)
- **Main blocker:** Nonlinear matter power spectrum emulation (JSC model from CosmoPower)

### poisson-flow-generative
- **Title:** Poisson Flow Generative Models (PFGM)
- **Domain:** ML / PDE
- **Verdict / scores:** SPOT-CHECK — coverage 7, agreement 8
- **Methods:** direct code execution, from-scratch reimplementation, training/fine-tuning, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, Matplotlib
- **Artifacts:** code 4 files; data/source files listed in JSON
- **Compute:** CPU 19.98 min (estimated=False), GPU 0.5 h (estimated=True)
- **Main blocker:** See source report; no additional blocker extracted into ledger.

### godunov-loss
- **Title:** Godunov-Loss PDE honest negative
- **Domain:** Numerical PDE / PIML
- **Verdict / scores:** FAILED — coverage 4, agreement 8
- **Methods:** direct code execution, inference-only, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, analytic verification
- **Tools:** Python, Matplotlib, NeuralOperator/FNO, Argo/Claude/GPT LLM
- **Artifacts:** code 9 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 1.0 h (estimated=True)
- **Main blocker:** See source report; no additional blocker extracted into ledger.

### 28589945
- **Title:** Dissemination of ARGs producer-to-pathogen
- **Domain:** Microbiology / AMR
- **Verdict / scores:** PARTIAL — coverage 9, agreement 9
- **Methods:** direct code execution, simulation, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, BV-BRC/PATRIC, BLAST, NCBI/SRA/RefSeq, Argo/Claude/GPT LLM
- **Artifacts:** code 6 files; data/source files listed in JSON
- **Compute:** CPU 240.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Wet-lab experimental validation (colony PCR, transformation)

### 29769716
- **Title:** Mutant Phenotypes 32 Bacteria (RB-TnSeq)
- **Domain:** Functional Genomics
- **Verdict / scores:** PARTIAL — coverage 10, agreement 9
- **Methods:** direct code execution, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 0.5 h (estimated=True)
- **Main blocker:** Conserved-association analysis (2,316 genes with orthology predictions)

### 36123438
- **Title:** Anti-Phage Defence E. coli Pangenome
- **Domain:** Microbiology / Phage
- **Verdict / scores:** SPOT-CHECK — coverage 8, agreement 9
- **Methods:** direct code execution, training/fine-tuning, data extraction/digitization, benchmark/evaluation
- **Tools:** BV-BRC/PATRIC, BLAST, NCBI/SRA/RefSeq
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 240.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Functional phage challenge assays (wet-lab, core experimental claim)

### 26392213
- **Title:** Outer Mucus Niche (Li 2015)
- **Domain:** Microbiome / 16S
- **Verdict / scores:** PARTIAL — coverage 6, agreement 6
- **Methods:** direct code execution, simulation, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, Matplotlib, NCBI/SRA/RefSeq
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 120.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Exact paper figure reproduction (Fig 1 panel layout)

### 34325466
- **Title:** Centenarian Bile Acid Pathways (Sato 2021)
- **Domain:** Metagenomics
- **Verdict / scores:** PARTIAL — coverage 4, agreement 6
- **Methods:** direct code execution, training/fine-tuning, simulation, data extraction/digitization, benchmark/evaluation
- **Tools:** SPAdes, Argo/Claude/GPT LLM
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 6000.0 min (estimated=False), GPU 10.0 h (estimated=False)
- **Main blocker:** Full 330-sample × 10–20M read metagenome processing

### BVBRC-01
- **Title:** ST11 CRKP Genomic Evolution (Zhang 2022)
- **Domain:** Epidemiology / AMR
- **Verdict / scores:** REPLICATED — coverage 8, agreement 8
- **Methods:** direct code execution, simulation, data extraction/digitization
- **Tools:** Python, BV-BRC/PATRIC, BLAST, Prokka, Roary, IQ-TREE, Argo/Claude/GPT LLM
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 4.0 h (estimated=False)
- **Main blocker:** wzc recombination detailed sequence alignment (1 claim, not_tested)

### BVBRC-02
- **Title:** Ralstonia Clinical Taxonomy (Fluit 2021)
- **Domain:** Taxonomic Genomics
- **Verdict / scores:** PARTIAL — coverage 7, agreement 8
- **Methods:** direct code execution, training/fine-tuning, simulation, data extraction/digitization
- **Tools:** BLAST, SPAdes, NCBI/SRA/RefSeq
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 240.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** cgMLST analysis (Ridom SeqSphere — commercial)

### BVBRC-03
- **Title:** S. aureus Mastitis (Sivakumar 2023)
- **Domain:** Veterinary Genomics
- **Verdict / scores:** REPLICATED — coverage 9, agreement 9
- **Methods:** direct code execution, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** BV-BRC/PATRIC, Prokka, SPAdes, Roary, NCBI/SRA/RefSeq
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 240.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** Spa typing (not available in BV-BRC API)

### BVBRC-04
- **Title:** Variovorax Trehalose (Shrestha 2022)
- **Domain:** Comparative Annotation
- **Verdict / scores:** PARTIAL — coverage 6, agreement 8
- **Methods:** direct code execution, inference-only, simulation, data extraction/digitization
- **Tools:** BV-BRC/PATRIC, NCBI/SRA/RefSeq
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 240.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** MetaCyc verification (license-gated Pathway Tools required)

### BVBRC-05
- **Title:** T. pyogenes Pangenome (Thakur 2022)
- **Domain:** Bacterial Genomics
- **Verdict / scores:** REPLICATED — coverage 9, agreement 9
- **Methods:** direct code execution, training/fine-tuning, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** BLAST, Prokka, Roary, FastTree, NCBI/SRA/RefSeq
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 240.0 min (estimated=True), GPU 0.0 h (estimated=True)
- **Main blocker:** EDGAR 3.0 direct comparison (web service, manual project creation)

### 2102.01010
- **Title:** ML-Accelerated CFD (Kochkov 2021)
- **Domain:** ML / PDE / CFD
- **Verdict / scores:** PARTIAL — coverage 8, agreement 9
- **Methods:** direct code execution, inference-only, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, Matplotlib, JAX, xarray/netCDF
- **Artifacts:** code 18 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 2.0 h (estimated=False)
- **Main blocker:** GitHub repository; supplementary tables/figures; paywalled/private/missing data

### 2302.04107
- **Title:** FEM vs PINNs (Grossmann 2023)
- **Domain:** Numerical PDE / ML
- **Verdict / scores:** PARTIAL — coverage 8, agreement 9
- **Methods:** direct code execution, training/fine-tuning, simulation, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, SciPy, TensorFlow, JAX, CUDA, FEniCS/FEM, Argo/Claude/GPT LLM
- **Artifacts:** code 48 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 1.0 h (estimated=True)
- **Main blocker:** GitHub repository; synthetic/generated data; paywalled/private/missing data

### 2107.10711
- **Title:** PINN-RANS (Eivazi 2022)
- **Domain:** ML / PDE / CFD
- **Verdict / scores:** PARTIAL — coverage 6, agreement 5
- **Methods:** direct code execution, inference-only, training/fine-tuning, simulation, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, SciPy, PyTorch, TensorFlow, CUDA
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 0.25 h (estimated=False)
- **Main blocker:** See source report; no additional blocker extracted into ledger.

### 2306.17648
- **Title:** Domain-Decomp PINNs (Kopaničáková 2023)
- **Domain:** ML / PDE / Opt
- **Verdict / scores:** PARTIAL — coverage 7, agreement 7
- **Methods:** direct code execution, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, SciPy, PyTorch, FEniCS/FEM, Argo/Claude/GPT LLM
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 4.5 h (estimated=False)
- **Main blocker:** supplementary tables/figures; synthetic/generated data; paywalled/private/missing data

### 1905.01205
- **Title:** Modal-Space Stochastic PDE (Zhang 2019)
- **Domain:** ML / PDE / UQ
- **Verdict / scores:** PARTIAL — coverage 7, agreement 5
- **Methods:** direct code execution, inference-only, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, analytic verification, benchmark/evaluation
- **Tools:** Python, PyTorch, DeepXDE
- **Artifacts:** code 0 files; data/source files listed in JSON
- **Compute:** CPU 180.0 min (estimated=False), GPU 4.0 h (estimated=False)
- **Main blocker:** See source report; no additional blocker extracted into ledger.

### EGU-2026-1909
- **Title:** F-FNO Tsunami Surrogate
- **Domain:** Tsunami / Neural Operators
- **Verdict / scores:** PARTIAL — coverage 10, agreement 10
- **Methods:** direct code execution, inference-only, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, NumPy, SciPy, pandas, Matplotlib, PyTorch, CUDA, NeuralOperator/FNO, HuggingFace/Transformers, xarray/netCDF, Zenodo, Argo/Claude/GPT LLM
- **Artifacts:** code 1 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 3.4 h (estimated=False)
- **Main blocker:** See source report; no additional blocker extracted into ledger.

### 10.1017/jog.2022.41
- **Title:** IGM Ice-Flow Inversion
- **Domain:** Cryosphere / Inverse Modeling
- **Verdict / scores:** PARTIAL — coverage 6, agreement 5
- **Methods:** direct code execution, inference-only, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, Matplotlib, TensorFlow, CUDA, xarray/netCDF, Argo/Claude/GPT LLM
- **Artifacts:** code 2 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 1.7 h (estimated=False)
- **Main blocker:** t, model: argo/argo:claude-opus-4.7) **Date:** 2026-05-27 **Compute:** uicgpu (NVIDIA A100 80 GB PCIe, CUDA 12.2, TF 2.15.1), pinned to 1 GPU. **AI ATLAS gap:** TIER-1 GAP-FILL for **P021 — ice-sheet basal fr | e pin. The newer netCDF4 is API-compatible. 2. **Missing runtime dependency `pyvista`.** IGM's data_assimilation module writes `.vtp` output via PyVista but does not declare it in `setup.py`. Installed | 78 km²** — the spatial setup is correct to 0.05 %. ### 4.2 Runtime ✅ (within 1 OoM of

### 10.1038/s41467-020-17142-3
- **Title:** Yuval--O'Gorman RF Climate Parameterization
- **Domain:** Climate / Subgrid ML
- **Verdict / scores:** PARTIAL — coverage 5, agreement 6
- **Methods:** direct code execution, from-scratch reimplementation, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, scikit-learn, xarray/netCDF, Zenodo, Argo/Claude/GPT LLM
- **Artifacts:** code 3 files; data/source files listed in JSON
- **Compute:** CPU 600.0 min (estimated=False), GPU 1.0 h (estimated=False)
- **Main blocker:** See source report; no additional blocker extracted into ledger.

### HARMPI
- **Title:** Fishbone--Moncrief GRMHD Torus
- **Domain:** GRMHD
- **Verdict / scores:** PARTIAL — coverage 8, agreement 8
- **Methods:** direct code execution, inference-only, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, Matplotlib, TensorFlow, MPI, Argo/Claude/GPT LLM
- **Artifacts:** code 2 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 0.25 h (estimated=True)
- **Main blocker:** See source report; no additional blocker extracted into ledger.

### 10.1073/pnas.1810286115
- **Title:** Rasp Deep-Learning Climate Parameterization
- **Domain:** Climate / Deep Learning
- **Verdict / scores:** PARTIAL — coverage 6, agreement 7
- **Methods:** direct code execution, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, NumPy, Matplotlib, PyTorch, CUDA, scikit-learn, xarray/netCDF, Zenodo, Argo/Claude/GPT LLM
- **Artifacts:** code 2 files; data/source files listed in JSON
- **Compute:** CPU 60.0 min (estimated=True), GPU 0.167 h (estimated=False)
- **Main blocker:** Zenodo; synthetic/generated data; paywalled/private/missing data; https://doi.org/10.1073/pnas.1810286115; https://arxiv.org/abs/1806.04731

### 10.1088/1742-6596/2505/1/012014
- **Title:** Duthé/PyWake Wind-Farm GNN
- **Domain:** Wind / GNN Surrogate
- **Verdict / scores:** PARTIAL — coverage 9, agreement 9
- **Methods:** direct code execution, from-scratch reimplementation, inference-only, training/fine-tuning, simulation, parameter fitting/regression, data extraction/digitization, benchmark/evaluation
- **Tools:** Python, PyTorch, TensorFlow, CUDA, Argo/Claude/GPT LLM
- **Artifacts:** code 12 files; data/source files listed in JSON
- **Compute:** CPU 138.0 min (estimated=False), GPU 1.25 h (estimated=False)
- **Main blocker:** GitHub repository; supplementary tables/figures; synthetic/generated data; paywalled/private/missing data; https://doi.org/10.1088/1742-6596/2505/1/012014; https://doi.org/10.1017/dce.2024.35

## TODO / Partial coverage notes
- None: all 66 requested non-LUCID entries were matched to an existing master/v4 ledger or source report path.