# Computational Tools Inventory for Replication

## Summary by Category

### Simulation & Modeling Codes
| Tool | Papers | Description |
|------|--------|-------------|
| **LAMMPS** | #3 (Cu64Zr36 MD) | Molecular dynamics simulation |
| **VASP** | #4 (Pt/La2Ti2O7 DFT), #11 (Perovskite DFT) | Ab initio DFT calculations |
| **SCALE 6.3** (ORIGEN, TRITON, KENO-VI, NEWT) | #5 (Molten salt reactors) | Nuclear reactor physics code suite |
| **Serpent** | #5 (Molten salt reactors) | Monte Carlo neutron transport (benchmark comparison) |
| **MATLAB/Simulink** | #8 (CMV Reduction Inverter) | Circuit simulation |
| **FEM EM solver** (Ansys HFSS or COMSOL) | #7 (CPW Resonator) | Finite-element electromagnetic simulation |
| **Mathematica** | #6 (FDTD) | Analytical validation expressions |

### Programming Languages
| Language | Papers |
|----------|--------|
| **Python** | #5 (ChemTriton), #6 (FDTD input), #9 (Virophage), #10 (STEM DL), #11 (Perovskite AI) |
| **R** | #2 (Bayesian Opt), #9 (Virophage) |
| **C (C99)** | #6 (FDTD) |
| **C/C++** | #8 (DSP programming) |

### Parallel Computing Libraries
| Tool | Papers |
|------|--------|
| **OpenMP** | #6 (FDTD) |
| **POSIX Threads (pthreads)** | #6 (FDTD) |
| **MPI** | #6 (FDTD, future work) |

### Machine Learning / Deep Learning
| Tool | Papers |
|------|--------|
| **Keras 2.0** | #10 (STEM DL) |
| **TensorFlow** | #10 (STEM DL) |
| **scikit-image** | #10 (STEM DL) |
| **NetworkX** | #10 (STEM DL) |
| **GPT-2 (Hugging Face Transformers)** | #11 (Perovskite AI) |
| **LLaMA-2** | #11 (Perovskite AI, comparison) |
| **SMILES-X** | #11 (Perovskite AI) |
| **RDKit** | #11 (Perovskite AI) |
| **scikit-learn** | #11 (Perovskite AI) |
| **UMAP** | #11 (Perovskite AI) |

### R Packages (Bayesian Optimization)
| Package | Paper #2 Purpose |
|---------|-----------------|
| **hetGP** | Heteroscedastic Gaussian process modeling |
| **DiceOptim** | Batch Expected Improvement |
| **GPareto** | Multi-objective batch EHI |
| **DiceKriging** | Deterministic GP modeling |
| **mlrMBO** | Model-based optimization |
| **mco** | NSGA-II multi-objective EA |
| **pso** | Particle swarm optimization |

### R Packages (Virophage Taxonomy)
| Package | Paper #9 Purpose |
|---------|-----------------|
| **ggplot2** | Visualization |
| **dplyr** | Data manipulation |
| **tidyr** | Data tidying |
| **ggtree / ggtreeExtra** | Phylogenetic tree visualization |

### Bioinformatics Tools (Virophage Taxonomy)
| Tool | Purpose |
|------|---------|
| **hmmsearch 3.3.2** | HMM profile searching |
| **BLAST+ (BlastP 2.10.0+)** | Protein comparison |
| **MAFFT 7.490** | Multiple sequence alignment |
| **MUSCLE 3.8.1551** | Multiple sequence alignment |
| **DIAMOND 0.9.24** | Fast protein alignment |
| **IQ-Tree 2.2.0** | Maximum-likelihood phylogenetics |
| **clipkit 1.3.0** | Alignment trimming |
| **SDT** | Sequence Demarcation Tool |
| **Prodigal 2.6.3** | Gene prediction |
| **hhblits / hhmake / hhsearch 3.1.0** | HMM-HMM comparison |
| **MCL 14-137** | Markov clustering |
| **InfoMap 0.18.25** | Network clustering |
| **MUMmer 4.0.0** | Genome dereplication / ANI |
| **CheckV** | Viral genome quality assessment |
| **EasyFig 2.2.3** | Genome map visualization |

### Databases
| Database | Papers |
|----------|--------|
| **OEIS** | #1 (Integer Sequences) |
| **NCBI nr / GenBank / RefSeq** | #9 (Virophage) |
| **IMG/VR v3** | #9 (Virophage) |
| **Pfam** | #9 (Virophage) |
| **Pdb70** | #9 (Virophage) |
| **ENDF/B-VII.1** | #5 (Nuclear data) |
| **IRPhEP** | #5 (Reactor benchmark data) |
| **MNIST** | #2 (CNN benchmark) |
| **PubChem** | #11 (Perovskite - Tanimoto similarity search for data augmentation) |

### DFT / Quantum Chemistry Specifics
| Tool/Method | Papers |
|-------------|--------|
| **PBE / PBE0 functionals** | #4 (DFT), #11 (DFT) |
| **DFT-D3 dispersion** | #4 (DFT) |
| **PAW pseudopotentials** | #4 (DFT), #11 (DFT) |
| **Bader charge analysis** | #4 (DFT) |
| **VESTA** | #4 (DFT visualization) |

### MD Specifics
| Tool/Method | Papers |
|-------------|--------|
| **EAM potential (Cheng Cu-Zr)** | #3 (MD) |
| **Voronoi tessellation** | #3 (MD post-processing) |
| **OVITO** (implied) | #3 (MD visualization) |

### Open Source Repos
| Repository | Paper |
|------------|-------|
| https://github.com/leofang/FDTD | #6 (FDTD code, MIT license) |
| https://github.com/Boulder-Cryogenic-Quantum-Testbed/simple-resonator-mask | #7 (CPW mask GDS files) |
| https://github.com/simroux/ICTV_VirophageSG | #9 (Virophage classification pipeline) |
| https://github.com/adroitfajar/pvmol-gen | #11 (Perovskite passivation molecule generation) |

---

## Per-Paper Summary

| # | Paper | Key Tools |
|---|-------|-----------|
| 1 | Integer Sequences (Hausdorff) | Computer algebra system, OEIS |
| 2 | Bayesian Optimization Portfolio | R, hetGP, DiceOptim, GPareto, mlrMBO, NSGA-II |
| 3 | Cu64Zr36 MD Deformation | LAMMPS, EAM potential, Voronoi analysis |
| 4 | Pt/La2Ti2O7 DFT | VASP, PBE/PBE0, Bader analysis, VESTA |
| 5 | SCALE Molten Salt Reactors | SCALE 6.3 (ORIGEN/TRITON/KENO-VI), Serpent, Python |
| 6 | FDTD Delay PDE | C99, OpenMP, pthreads, Mathematica, Python |
| 7 | CPW Resonator Mask | FEM EM solver (HFSS/COMSOL), open-source GDS mask |
| 8 | CMV Reduction Inverter | MATLAB/Simulink |
| 9 | Virophage Taxonomy | ~20 bioinformatics tools, R, NCBI databases |
| 10 | Deep Learning STEM | Keras/TensorFlow, scikit-image, NetworkX, Python |
| 11 | Perovskite Passivation (AI-Driven) | Python, GPT-2 (Transformers), SMILES-X, RDKit, scikit-learn, UMAP, VASP (DFT), PubChem |

---

### Generative AI / Cheminformatics (Perovskite Passivation)
| Tool | Purpose |
|------|---------|
| **GPT-2** (via Hugging Face Transformers) | Generative language model fine-tuned on SMILES for molecule generation |
| **LLaMA-2** (7B) | Alternative generative model (comparison, not primary) |
| **SMILES-X** | Discriminative classifier for molecular SMILES -> passivation effectiveness |
| **RDKit** | Molecular filtering (SA score, PAINS, HBD/HBA, TPSA), SMILES canonicalization, Morgan fingerprints |
| **scikit-learn** | Agglomerative clustering, PCA, random forest (comparison) |
| **UMAP (umap-learn)** | Chemical space visualization |
| **PubChem API** | Tanimoto similarity search for dataset augmentation |
| **VASP** | DFT calculations for molecule-surface adsorption energies on FAPbI3 |
| **Morgan fingerprints** | Molecular fingerprinting for clustering and similarity |

### Open Source Code Repos
| Repository | Paper |
|------------|-------|
| https://github.com/adroitfajar/pvmol-gen | #11 (Full pipeline code) |

---

## Installation Complexity Estimate

- **Straightforward** (pip/conda/CRAN): Python, R, Keras, TensorFlow, scikit-image, NetworkX, most R packages, most bioinformatics tools, GPT-2/Transformers, SMILES-X, RDKit, scikit-learn, UMAP
- **Moderate** (compiled codes, licenses): LAMMPS, GCC/OpenMP, C99 FDTD code, Mathematica, LLaMA-2 (GPU required)
- **Complex / Licensed**: VASP (academic license required), SCALE 6.3 (DOE/RSICC distribution), Ansys HFSS or COMSOL (commercial), MATLAB/Simulink (commercial), Serpent (academic license)
