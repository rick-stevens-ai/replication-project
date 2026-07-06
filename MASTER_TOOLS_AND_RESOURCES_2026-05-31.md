# Master Tools / Methods / Resources / Scores Inventory

**Generated:** 2026-05-31 by Kukla (Hermes/Argo-Opus-4.7) — v3, pure-LLM scoring  
**Corpus:** 129 replication reports across `~/Dropbox/REPLICATE-PROJECT/`  

## Methodology

- **Tools / datasets / hardware** (structural fields): keyword extraction over canonical REPORT files. Tracks what the document literally mentions; no judgment involved.
- **Coverage / Agreement / Verdict** (judgmental fields): **Sonnet 4.6 (Argo `argo:claude-sonnet-4.6`) scored 100% of reports** under a single rubric, single prompt, in one ~2.5 min parallel pass (8 concurrent workers). No regex-based score extraction — that produces a biased aggregate by mixing author self-reports with independent judgment. v3 of this document discards the regex-extracted scores from v2.
- **Rubric:** Coverage 0-10 = how much of the paper's scope was attempted (10 = every claim, 0 = nothing); Agreement 0-10 = of what was tested, how well it matched the paper (10 = bit-exact, 0 = couldn't test).
- **Verdict labels:** REPLICATED · PARTIAL · SPOT-CHECK · NO-GO · FAILED.
- **Compute budgets:** lower bounds only — only what reports explicitly state.

## Headline numbers

- **Reports analyzed:** 129
- **Mean Coverage:** **5.47/10** (single-judge Sonnet 4.6, all 129 reports)
- **Mean Agreement:** **6.60/10** (single-judge Sonnet 4.6, all 129 reports)

### Verdict mix

| Verdict | Count | % |
|---|---:|---:|
| REPLICATED | 15 | 12% |
| PARTIAL | 97 | 75% |
| SPOT-CHECK | 9 | 7% |
| NO-GO | 7 | 5% |
| FAILED | 1 | 1% |

### Score distributions

```
Coverage:                          Agreement:
   0: █████                            0: ███████
   1:                                  1: 
   2: ███                              2: █
   3: ██████████                       3: 
   4: ███████████████████              4: ███████
   5: ██████████████████████████       5: ██████
   6: ███████████████████████          6: ██████████████████████████████
   7: ██████████████████████           7: ████████████████████████████
   8: ██████████████████               8: ██████████████████████████████████████
   9: ███                              9: █████████
  10:                                 10: ███
```

## Compute budgets (lower bounds)

- **GPU-hours explicitly reported:** ≥454.7 GPU-h across 7 report-mentions
- **CPU-hours explicitly reported:** ≥603.7 CPU-h across 5 report-mentions
- Most reports omit a budget line. Project-wide accurate numbers would need launchd/scheduler log walks.
- **LLM tokens for the replications themselves:** unrecorded in-band. For LLM cost picture see agent transcripts under `~/Dropbox/XFER/agent-transcripts/`.
- **LLM tokens for this scoring pass:** ~129 LLM calls × ~12K input / 200 output ≈ **1.55M input tokens, 26K output** (Sonnet 4.6 via Argo, ~2.5 min wall).

## Most-used tools / codes / frameworks

| # papers | Tool / framework |
|---:|---|
| 68 | Python |
| 25 | matplotlib |
| 24 | Claude (Anthropic) |
| 22 | NumPy |
| 20 | PyTorch |
| 18 | CUDA |
| 16 | Conda/Mamba |
| 14 | SciPy |
| 12 | BLAST/BLAST+ |
| 10 | MPI |
| 9 | BV-BRC / PATRIC |
| 8 | Prokka |
| 7 | SPAdes/metaSPAdes |
| 5 | TOPAS / Geant4-DNA |
| 4 | C/C++ |
| 4 | scikit-learn |
| 4 | Prodigal |
| 4 | Roary |
| 4 | TensorFlow |
| 4 | JAX |
| 3 | OpenMP |
| 3 | RAxML |
| 3 | pandas |
| 3 | MATLAB |
| 3 | Fortran |
| 2 | NetworkX |
| 2 | PeleC |
| 2 | R (language) |
| 2 | CD-HIT |
| 2 | DIAMOND |
| 2 | HuggingFace Transformers |
| 2 | MetaBAT2 |
| 2 | minimap2 |
| 2 | samtools |
| 2 | IQ-TREE |
| 2 | OpenFOAM |
| 2 | PyTorch Geometric |
| 2 | Singularity/Apptainer |
| 2 | DeepXDE |
| 1 | LAMMPS |
| 1 | MMseqs2 |
| 1 | Quantum ESPRESSO |
| 1 | VASP |
| 1 | OpenMC |
| 1 | SCALE 6 |
| 1 | UMAP |
| 1 | CheckM |
| 1 | CheckV |
| 1 | HMMER |
| 1 | MAFFT |

_(77 distinct tools/codes — showing top 50)_

## Datasets / databases cited

| # papers | Source |
|---:|---|
| 12 | NCBI/GenBank/RefSeq |
| 9 | Zenodo |
| 6 | SRA |
| 3 | ENA |
| 2 | UniProt |
| 2 | Figshare |
| 2 | PDB / PDB70 |
| 2 | CAMELS sims |
| 1 | Materials Project |
| 1 | OEIS |
| 1 | IMG/VR |
| 1 | Pfam |
| 1 | PubChem |
| 1 | Kepler/TESS |
| 1 | NanoGrav 15yr |

## Hardware / compute platforms

| # papers | Platform |
|---:|---|
| 29 | uicgpu (8×A100) |
| 27 | NVIDIA A100 |
| 27 | cherryrd (M1) |
| 5 | Aurora (ALCF) |
| 4 | chiatta00 (JLSE) |
| 3 | M1 Mac mini |
| 3 | ALCF |
| 3 | JLSE |
| 2 | Polaris (ALCF) |
| 2 | NVIDIA V100 |
| 1 | Theta (ALCF) |
| 1 | Frontier (OLCF) |
| 1 | CELS |
| 1 | Intel Max GPU |

## Per-paper master table

All Coverage/Agreement scores are single-judge Sonnet 4.6 (uniform provenance). Columns: ID · Verdict · C/A (/10) · Tools · Hardware · Runtime · Repo

| ID | Verdict | C/A | Tools | Hardware | Runtime | Repo |
|---|---|---|---|---|---|---|
| 1275503-COSMIC-REIONIZATION-ON-COMPUTERS | PARTIAL | 5/5 | Claude (Anthropic), Python | — | — | — |
| 1379592-Mathematical-Foundations-of-the-GraphBLAS | REPLICATED | 8/9 | NetworkX, Python | — | — | — |
| 1412756-Chiral-Spin-Order-in-Kondo-Heisenberg-systems | PARTIAL | 6/6 | Claude (Anthropic), Python | — | — | — |
| 1427646-Deep-Learning-of-Atomically-Resolved-Scanning | PARTIAL | 4/6 | — | NVIDIA A100, uicgpu (8×A100) | — | — |
| 1461824-APPROXIMATING-PHOTO-Z-PDFS-FOR-LARGE-SURVEYS | PARTIAL | 6/7 | Python | — | — | — |
| 1475143-FDTD-solving-1+1D-delay-PDE-in | PARTIAL | 8/8 | CUDA, Claude (Anthropic), Python | — | — | — |
| 1484740-Electronic-and-optical-properties-of-two-dimensional-GaN | NO-GO | 2/0 | Claude (Anthropic), Python | — | — | — |
| 1523841-Quantitative-relationship-between-polarization-differences-a | PARTIAL | 6/8 | Claude (Anthropic), Python | — | — | — |
| 1559043-ignition-kernel-turbulent | PARTIAL | 6/6 | CUDA, PeleC | Aurora (ALCF), NVIDIA A100 +3 | — | — |
| 1565592-Markov-state-models-from-short-non-equilibrium | REPLICATED | 8/7 | CUDA, Conda/Mamba | NVIDIA A100 | — | — |
| 1578031-Joint-emulation-of-Earth-System-Model | PARTIAL | 5/6 | NumPy, Python, R (language), SciPy +1 | — | — | — |
| 1606674-Common-Mode-Voltage-Reduction-of-Single-Phase | REPLICATED | 8/9 | Claude (Anthropic), NumPy, Python | — | — | — |
| 1609039-Deformation-behavior-of-annealed-Cu64Zr36-metallic | PARTIAL | 5/4 | C/C++, CUDA, Conda/Mamba, LAMMPS +3 | NVIDIA A100, uicgpu (8×A100) | — | — |
| 1624105-Clustering-huge-protein-sequence-sets-in | SPOT-CHECK | 3/6 | CD-HIT, DIAMOND, MMseqs2, Python | M1 Mac mini, cherryrd (M1) | — | — |
| 1842593-MOTION-TOMOGRAPHY-VIA-OCCUPATION-KERNELS | PARTIAL | 8/8 | — | — | — | — |
| 1861801-NukeLM-Pre-Trained-and-Fine-Tuned-Language-Models | PARTIAL | 4/6 | CUDA, HuggingFace Transformers, PyTorch, Python | NVIDIA A100, uicgpu (8×A100) | — | gh:pnnl/NUKELM |
| 1864334-Variational-Monte-Carlo-calculations-of-A | PARTIAL | 4/4 | Claude (Anthropic), PyTorch, Python | — | — | — |
| 1868518-Graph-RL-Distribution-Restoration | PARTIAL | 5/5 | Claude (Anthropic), NetworkX, PyTorch, Python | — | — | — |
| 1981773-Effect-of-Single-Atom-Platinum-Pt | PARTIAL | 4/6 | CUDA, MPI, Quantum ESPRESSO, VASP | NVIDIA A100, uicgpu (8×A100) | — | — |
| 1983793-Simple-coplanar-waveguide-resonator-mask-targeting | PARTIAL | 8/8 | Claude (Anthropic), MPI, Python | — | — | — |
| 1984484-DRAS-Deep-Reinforcement-Learning-for-Cluster | PARTIAL | 3/5 | Conda/Mamba, matplotlib | ALCF, Theta (ALCF) | — | — |
| 1993311-Electronic-specific-heat-capacities-and-entropies | PARTIAL | 4/6 | NumPy, SciPy, scikit-learn | — | — | — |
| 1997354-Integer-Sequences-from-Configurations-in-the | PARTIAL | 7/8 | Claude (Anthropic), Python | — | — | — |
| 2217719-SCALE-depletion-capabilities-for-molten-salt | PARTIAL | 6/5 | Claude (Anthropic), OpenMC, Python, SCALE 6 | — | — | — |
| 2396968-Latent-Stochastic-Differential-Equations-for-Modeling | PARTIAL | 8/6 | — | NVIDIA A100, NVIDIA V100 +1 | — | gh:JFagin/latent_SDE |
| 2439897-Physics-and-chemistry-from-parsimonious-representations | PARTIAL | 4/7 | PyTorch, UMAP | — | — | — |
| 2441075-Exactly-solved-model-of-light-scattering-errors-in | PARTIAL | 8/9 | Claude (Anthropic), Python | — | — | — |
| 2469515-Supervised-extraction-of-near-complete-genomes-from | SPOT-CHECK | 2/6 | BLAST/BLAST+, BV-BRC / PATRIC, CheckM, Conda/Mamba +5 | cherryrd (M1) | — | — |
| 2475938-Updated-Virophage-Taxonomy-and-Distinction-from | REPLICATED | 8/8 | CheckV, Conda/Mamba, HMMER, IQ-TREE +4 | cherryrd (M1) | — | gh:simroux/ICTV_VirophageSG |
| 2571540-A-Portfolio-Approach-to-Massively-Parallel | NO-GO | 0/0 | Claude (Anthropic), Python | — | — | — |
| 2571909-Physics-based-hybrid-machine-learning-for-critical | NO-GO | 4/0 | Claude (Anthropic), Python | — | — | — |
| 2582579-Constraining-Cosmological-Parameters-with-Needlet-Internal | PARTIAL | 5/8 | Conda/Mamba, Python, matplotlib | cherryrd (M1) | — | gh:jcolinhill/pyilc |
| 2587225-ScaWL-Scaling-k-WL-Weisfeiler-Lehman-Algorithms-in | PARTIAL | 7/8 | Claude (Anthropic), MPI, NumPy, Python | JLSE, cherryrd (M1) +1 | — | — |
| 2587579-Mesh-based-super-resolution-multiscale-GNN | PARTIAL | 4/6 | CUDA, OpenFOAM, PyTorch Geometric | Aurora (ALCF), NVIDIA A100 +3 | — | — |
| 2587945-Edge-Localized-Modes-NN-forecaster | PARTIAL | 5/6 | — | — | — | — |
| 26392213-Outer-mucus-niche | PARTIAL | 6/6 | Conda/Mamba, Python, R (language) | — | — | — |
| 28589945-ARG-dissemination | PARTIAL | 7/8 | BLAST/BLAST+, BV-BRC / PATRIC | — | — | — |
| 29769716-Mutant-phenotypes-bacterial-genes | PARTIAL | 7/7 | — | — | — | — |
| 3003857-DIVIDE-AND-CONQUER-CHAOTIC | PARTIAL | 6/4 | PyTorch | NVIDIA A100, uicgpu (8×A100) | — | — |
| 3014512-Spin-dependent-scattering-of-sub-GeV-dark-matter | PARTIAL | 7/8 | NumPy, Python, SciPy, matplotlib | — | — | — |
| 34325466-Centenarian-bile-acid | PARTIAL | 3/5 | CONCOCT, DESeq2, DIAMOND, MetaBAT2 +3 | cherryrd (M1) | 10 GPU-h / 100 CPU-h | — |
| 36123438-Anti-phage-defense-Ecoli | SPOT-CHECK | 3/8 | BLAST/BLAST+, BV-BRC / PATRIC | — | — | gh:chrisdoering8197/phagedefense |
| BVBRC-01-CRKP-Zhang2022 | REPLICATED | 8/7 | BLAST/BLAST+, BV-BRC / PATRIC, Conda/Mamba, IQ-TREE +6 | NVIDIA A100, uicgpu (8×A100) | — | — |
| BVBRC-02-Ralstonia-Fluit2021 | PARTIAL | 6/8 | BLAST/BLAST+, SPAdes/metaSPAdes | — | — | — |
| BVBRC-03-Saureus-mastitis-Sivakumar2023 | REPLICATED | 8/7 | BV-BRC / PATRIC, Prokka, Roary, SPAdes/metaSPAdes | — | — | — |
| BVBRC-04-Variovorax-trehalose-Shrestha2022 | PARTIAL | 6/8 | BV-BRC / PATRIC | — | — | — |
| BVBRC-05-Trueperella-pyogenes-Thakur2022 | REPLICATED | 7/8 | BLAST/BLAST+, CD-HIT, MUSCLE, Prokka +1 | — | — | — |
| BVBRC-06-Smaltophilia-iron-Kalidasan2018 | SPOT-CHECK | 3/8 | BV-BRC / PATRIC | — | — | — |
| BVBRC-07-Sherry-AMR-workflow-2023 | REPLICATED | 7/9 | BLAST/BLAST+, C/C++, Python | — | — | gh:MDU-PHL/abritamr |
| BVBRC-08-Lplantarum-DJF10-Kandasamy2022 | PARTIAL | 6/8 | BLAST/BLAST+, BV-BRC / PATRIC, Prokka, SPAdes/metaSPAdes +1 | — | — | — |
| BVBRC-09-blaNDM5-K-pneumoniae-Yuan2019 | REPLICATED | 8/8 | BLAST/BLAST+, Prodigal, Prokka, RAxML | JLSE, chiatta00 (JLSE) | — | — |
| BVBRC-10-Llactis-LL16-Mileriene2023 | PARTIAL | 7/7 | BLAST/BLAST+, Prokka, SPAdes/metaSPAdes | — | — | gh:ncbi/fcs |
| BVBRC-11-VREfm-LatAm-Rios2020 | PARTIAL | 6/8 | BLAST/BLAST+, Conda/Mamba, Prodigal, Prokka +2 | cherryrd (M1) | — | — |
| BVBRC-14-HybridAssembly-Ecoli-Kpneu-Khezri2021 | PARTIAL | 5/7 | BLAST/BLAST+, BV-BRC / PATRIC, Conda/Mamba, Flye +3 | — | — | — |
| CAMELS-Multifield-VillaescusaNavarro2022 | SPOT-CHECK | 4/7 | CUDA, PyTorch | NVIDIA A100, uicgpu (8×A100) | 000 GPU-h / 500 CPU-h | — |
| FFNO-Tsunami-Makarynskyy2026 | PARTIAL | 6/8 | CUDA, PyTorch, Python, matplotlib +1 | NVIDIA A100, uicgpu (8×A100) | 3.40 GPU-h | — |
| HARMPI-GRMHD | PARTIAL | 4/6 | HARMPI (GRMHD), MPI | uicgpu (8×A100) | — | gh:atchekho/harmpi |
| Jouvet-2023-IGM-IceFlow | PARTIAL | 5/4 | CUDA, Conda/Mamba, IGM (glacier model), Python +1 | NVIDIA A100, uicgpu (8×A100) | — | — |
| LUCID-replications/lucid-actinium-lutetium-dose-effect | PARTIAL | 6/6 | — | — | — | — |
| LUCID-replications/lucid-autofoci-detection | REPLICATED | 8/9 | Python, matplotlib, pandas, scikit-image +1 | — | — | gh:nleng/AutoFoci |
| LUCID-replications/lucid-bnct-radioresistant-hcc | PARTIAL | 5/8 | — | — | — | — |
| LUCID-replications/lucid-cu64-topas-nbio-lethal-damage | PARTIAL | 5/10 | TOPAS / Geant4-DNA | — | — | — |
| LUCID-replications/lucid-dna-repair-kinetics-doserate-rbe | PARTIAL | 4/8 | — | — | — | — |
| LUCID-replications/lucid-dsb-repair-history-review-triage | NO-GO | 0/0 | — | — | — | — |
| LUCID-replications/lucid-franken-alpha-gamma-rbe | PARTIAL | 6/10 | — | — | — | — |
| LUCID-replications/lucid-fukui-saga-lq-sldr-aldh | PARTIAL | 7/8 | NumPy | — | — | — |
| LUCID-replications/lucid-globle-photon-cell-killing | REPLICATED | 7/8 | — | — | — | — |
| LUCID-replications/lucid-grandt-fibroblast-rnaseq | PARTIAL | 8/9 | Python, Trimmomatic, limma, matplotlib | — | — | — |
| LUCID-replications/lucid-h2ax-phosphorylation-review-triage | NO-GO | 0/0 | Claude (Anthropic) | — | — | — |
| LUCID-replications/lucid-hsgc-c5-repair-performance | PARTIAL | 6/7 | Python, SciPy, TOPAS / Geant4-DNA, matplotlib +1 | — | — | — |
| LUCID-replications/lucid-lung-fibrosis-abm | PARTIAL | 4/6 | Python, TOPAS / Geant4-DNA | — | — | gh:BioDynaMo/biodynamo |
| LUCID-replications/lucid-mariotti-split-dose-gamma-h2ax | PARTIAL | 7/7 | — | — | — | — |
| LUCID-replications/lucid-matsuya-nte-integrated | PARTIAL | 8/6 | NumPy, SciPy, matplotlib | — | — | — |
| LUCID-replications/lucid-medras-mc | PARTIAL | 4/8 | Python, matplotlib | cherryrd (M1) | — | gh:sjmcmahon/Medras-MC |
| LUCID-replications/lucid-nuclear-matrix-uv-repair-triage | NO-GO | 0/0 | — | — | — | — |
| LUCID-replications/lucid-p53-repair | PARTIAL | 5/6 | NumPy, Python, SciPy, matplotlib | cherryrd (M1) | — | — |
| LUCID-replications/lucid-pariset-53bp1-mouse-strains | PARTIAL | 6/8 | — | — | — | — |
| LUCID-replications/lucid-partrac-analytical-formulas | PARTIAL | 5/7 | PARTRAC | — | — | — |
| LUCID-replications/lucid-patra-polbeta-radiosensitivity | PARTIAL | 5/7 | Python, matplotlib | — | — | — |
| LUCID-replications/lucid-pyfoci-miscounting | PARTIAL | 6/7 | Python | — | — | — |
| LUCID-replications/lucid-skin-inflammation-nfkb-cox2 | SPOT-CHECK | 3/9 | — | — | — | — |
| LUCID-replications/lucid-slow-fast-nhej | PARTIAL | 5/6 | Python, SciPy, TOPAS / Geant4-DNA | — | — | gh:topas-nbio/TOPAS-nBio |
| LUCID-replications/lucid-spatiotemporal-early-dna-damage | REPLICATED | 7/8 | Python, matplotlib | — | — | — |
| LUCID-replications/lucid-staaf-mixed-beam-gamma-h2ax | PARTIAL | 7/8 | Claude (Anthropic) | — | — | — |
| LUCID-replications/lucid-stochastic-poisson-dna-damage | REPLICATED | 9/10 | NumPy | cherryrd (M1), uicgpu (8×A100) | — | — |
| LUCID-replications/lucid-stochastic-rejoining | PARTIAL | 6/7 | NumPy, Python, TOPAS / Geant4-DNA, matplotlib | cherryrd (M1) | — | — |
| LUCID-replications/lucid-turner-gamma-h2ax-biodosimetry | REPLICATED | 9/8 | — | — | — | — |
| LUCID-replications/lucid-ulyanenko-gammah2ax-patm-msc | REPLICATED | 8/9 | NumPy, Python | — | — | — |
| LUCID-replications/lucid-universe-repair-doserate-rbe | PARTIAL | 5/6 | — | — | — | — |
| PDE-replications/amr-vs-mr-euler | PARTIAL | 4/6 | C/C++, MPI, Python | cherryrd (M1) | — | gh:waveletApplications/carmen |
| PDE-replications/apbs-pb | PARTIAL | 6/9 | APBS, Conda/Mamba, MPI, Python | M1 Mac mini, cherryrd (M1) | — | gh:Electrostatics/apbs |
| PDE-replications/dedalus | PARTIAL | 7/8 | Claude (Anthropic), Dedalus, JAX, MPI +1 | — | — | — |
| PDE-replications/fast-poisson-spectral | PARTIAL | 7/8 | MATLAB, NumPy, Python, SciPy | — | — | — |
| PDE-replications/fem-vs-pinns | PARTIAL | 5/8 | JAX, Python | Frontier (OLCF), NVIDIA A100 | — | gh:TamaraGrossmann/FEM-vs-PINNs |
| PDE-replications/flups-poisson | PARTIAL | 4/8 | Claude (Anthropic), FLUPS, MPI, OpenMP | ALCF, Aurora (ALCF) +1 | — | gh:vanreeslab/h3lpr |
| PDE-replications/fno-neuraloperator | SPOT-CHECK | 3/7 | Claude (Anthropic), HuggingFace Transformers, NumPy, PyTorch +2 | cherryrd (M1) | — | gh:neuraloperator/neuraloperator |
| PDE-replications/galerkin-stochastic-burgers | PARTIAL | 5/7 | NumPy, Python, SciPy | cherryrd (M1), uicgpu (8×A100) | — | — |
| PDE-replications/godunov-loss | FAILED | 2/2 | — | NVIDIA A100, uicgpu (8×A100) | — | — |
| PDE-replications/jax-cfd | PARTIAL | 7/7 | CUDA, Claude (Anthropic), JAX, JAX-CFD +1 | NVIDIA A100 | — | gh:google/jax-cfd |
| PDE-replications/kernel-active-subspaces | PARTIAL | 5/7 | OpenFOAM, Python, scikit-learn | cherryrd (M1) | — | gh:mathLab/ATHENA |
| PDE-replications/kinetic-jl | PARTIAL | 4/7 | Fortran | cherryrd (M1) | — | gh:vavrines/Kinetic.jl |
| PDE-replications/koopman-no | PARTIAL | 5/7 | Claude (Anthropic), NumPy, PyTorch, Python +2 | — | — | gh:Koopman-Laboratory/KoopmanLab |
| PDE-replications/laplace-no | PARTIAL | 8/6 | CUDA, Claude (Anthropic), PyTorch, Python | NVIDIA A100, uicgpu (8×A100) | — | — |
| PDE-replications/latent-spectral-models | SPOT-CHECK | 3/6 | PyTorch | NVIDIA A100, uicgpu (8×A100) | — | — |
| PDE-replications/lifex-cfd | PARTIAL | 5/6 | Conda/Mamba, Docker, MPI, Singularity/Apptainer +1 | NVIDIA A100, uicgpu (8×A100) | — | — |
| PDE-replications/lightning-laplace | PARTIAL | 7/8 | MATLAB | — | — | — |
| PDE-replications/lowrank-vlasov-poisson | PARTIAL | 5/7 | NumPy, Python, SciPy, matplotlib | cherryrd (M1) | — | — |
| PDE-replications/marl-amr | PARTIAL | 5/7 | CUDA, Claude (Anthropic), Conda/Mamba, Python +2 | CELS, uicgpu (8×A100) | — | gh:LLNL/marl-amr |
| PDE-replications/modal-space-stochastic-zhang-2019 | PARTIAL | 7/5 | DeepXDE, PyTorch | NVIDIA A100, uicgpu (8×A100) | — | — |
| PDE-replications/modified-pnp | PARTIAL | 4/8 | NumPy, Python, SciPy, matplotlib | cherryrd (M1) | — | — |
| PDE-replications/optimized-schwarz-helmholtz | PARTIAL | 7/7 | C/C++, Python, matplotlib | cherryrd (M1) | — | — |
| PDE-replications/pdebench | PARTIAL | 4/6 | JAX, NumPy, PDEBench, PyTorch +1 | Aurora (ALCF), M1 Mac mini +2 | — | gh:pdebench/PDEBench |
| PDE-replications/pinn-domain-decomp-2023 | PARTIAL | 7/4 | PyTorch | NVIDIA A100, NVIDIA V100 +1 | — | — |
| PDE-replications/pinn-rans-eivazi-2022 | PARTIAL | 9/6 | CUDA, PyTorch, Python, SciPy +1 | NVIDIA A100, uicgpu (8×A100) | — | gh:Fantasy98/Physics-informed-neural-networks-for-solving-Reynolds-averaged-Navier-Stokes-equations |
| PDE-replications/poisson-flow-generative | SPOT-CHECK | 3/6 | — | — | — | — |
| PDE-replications/pwdg-helmholtz | PARTIAL | 6/7 | NumPy, Python, SciPy | — | — | — |
| PDE-replications/vlasov-poisson-dg-hermite | PARTIAL | 5/6 | NumPy, Python, matplotlib | cherryrd (M1) | — | — |
| PDE-replications/vqapoisson | PARTIAL | 5/8 | Python | cherryrd (M1) | — | gh:ToyotaCRDL/VQAPoisson |
| PDE-replications/walk-on-stars | PARTIAL | 6/8 | OpenMP, Python, Singularity/Apptainer, matplotlib | — | — | gh:GeometryCollective/wost-simple |
| Rasp-2018-Climate | PARTIAL | 6/7 | CUDA, Conda/Mamba, Fortran, Keras +4 | ALCF, NVIDIA A100 +2 | 0.13 GPU-h | — |
| SOWFA-WindFarm | PARTIAL | 7/7 | PyTorch, PyTorch Geometric, PyWake, SOWFA (LES wind) +1 | NVIDIA A100, uicgpu (8×A100) | 2.3 CPU-h | gh:gduthe/windfarm-gnn |
| Yuval-OGorman-2020-Climate | PARTIAL | 3/6 | Fortran, MATLAB, Python, scikit-learn | uicgpu (8×A100) | 1.4 CPU-h | — |
| pvmol-gen-fajar2026 | PARTIAL | 5/4 | GPT-2, PyTorch, Python, RDKit | cherryrd (M1) | — | gh:Lambard-ML-Team/SMILES-X |
| replicate-1559043-combustion | NO-GO | 0/0 | AMReX, CUDA, MPI, PeleC +1 | Aurora (ALCF), Intel Max GPU +2 | — | gh:AMReX-Combustion/PeleC.git |
| replicate-msm | PARTIAL | 8/7 | CUDA, Conda/Mamba | NVIDIA A100 | — | — |
| space-bls-exoplanets | PARTIAL | 5/8 | Python | — | — | — |
| space-camels-emulator | PARTIAL | 4/6 | — | NVIDIA A100, uicgpu (8×A100) | — | — |
| space-nanograv-15yr-gwb | PARTIAL | 7/8 | NumPy, Python | — | — | gh:nanograv/15yr_stochastic_analysis |
| zhang-spde-deepxde | PARTIAL | 6/4 | CUDA, DeepXDE, PyTorch, Python | NVIDIA A100, uicgpu (8×A100) | — | — |

## Judge notes — lowest-scored reports (Coverage ≤ 3)

| ID | C/A | Verdict | Judge note |
|---|---|---|---|
| 2571540-A-Portfolio-Approach-to-Massively-Parallel | 0/0 | NO-GO | Report is a hollow template with no actual replication content: 'Not recorded' throughout, no results reproduced, no quantitative comparisons, no methods execut |
| LUCID-replications/lucid-dsb-repair-history-review-triage | 0/0 | NO-GO | Review article with no original data, tables, or meta-analysis; only two weak heuristic curve fits in figures, both non-self-contained; triage correctly identif |
| LUCID-replications/lucid-h2ax-phosphorylation-review-triage | 0/0 | NO-GO | Paper is a narrative review with no tables, equations, or reproducible quantitative analyses; triage correctly identifies it as outside LUCID replication scope  |
| LUCID-replications/lucid-nuclear-matrix-uv-repair-triage | 0/0 | NO-GO | Pure wet-lab 1988 paper with no computational artifacts, models, or datasets to replicate; report correctly identifies no executable replication target and docu |
| replicate-1559043-combustion | 0/0 | NO-GO | This is an infrastructure/build validation report for a compute cluster (chiatta00), not a replication of any research paper's scientific claims. No paper claim |
| 1484740-Electronic-and-optical-properties-of-two-dimensional-GaN | 2/0 | NO-GO | Report is a template shell with no recorded content: claims, methodology details, quantitative comparisons, and agreement rationale are all 'Not recorded'. Self |
| 2469515-Supervised-extraction-of-near-complete-genomes-from | 2/6 | SPOT-CHECK | Only the MetaBAT2 comparator baseline was replicated on a synthetic 5-species community; the paper's core contribution (PATRIC supervised binning via pheS ancho |
| PDE-replications/godunov-loss | 2/2 | FAILED | Paper PDF was never located; loss formulation is a best-effort reconstruction from abstract concepts. Only a narrow MLP experiment was run, missing the actual a |
| 1624105-Clustering-huge-protein-sequence-sets-in | 3/6 | SPOT-CHECK | Only the central asymptotic scaling claim (linear vs quadratic complexity) was tested via a from-scratch Python reimplementation on synthetic data. The paper's  |
| 1984484-DRAS-Deep-Reinforcement-Learning-for-Cluster | 3/5 | PARTIAL | Replication tests only the high-level directional claim that DRL outperforms FCFS/EASY-backfill; uses a completely different workload trace (HPC2N 240-node vs T |
| 34325466-Centenarian-bile-acid | 3/5 | PARTIAL | Only 2 of 4 major claims tested computationally; metabolomics and in vitro biology not attempted; 10+10 sample subset at 3-7% read depth too shallow for robust  |
| 36123438-Anti-phage-defense-Ecoli | 3/8 | SPOT-CHECK | Replication only verified protein sequence existence and BLAST conservation for the 21 novel systems; the core experimental claims (functional selection screen, |
| BVBRC-06-Smaltophilia-iron-Kalidasan2018 | 3/8 | SPOT-CHECK | Only the in-silico RAST annotation component (~30% of paper scope) was computationally testable and tested; 15/22 claims (all wet-lab: PCR screening, NanoString |
| LUCID-replications/lucid-skin-inflammation-nfkb-cox2 | 3/9 | SPOT-CHECK | Only Figs 1, 2, and 7 were computationally auditable; wet-lab methods (H&E, IHC, western blots, irradiation) could not be replicated. All audited quantitative c |
| PDE-replications/fno-neuraloperator | 3/7 | SPOT-CHECK | Replication targets only the small-Darcy tutorial example (CPU, 16x16, 1k samples, ~200k params), not the actual ICLR 2021 paper benchmarks (Burgers, full Darcy |
| PDE-replications/latent-spectral-models | 3/6 | SPOT-CHECK | Only 2 of 7 benchmarks tested (Darcy and NS); paper's headline 11.5% claim tested directionally but not quantitatively matched (18% observed vs 11.5% claimed);  |
| PDE-replications/poisson-flow-generative | 3/6 | SPOT-CHECK | Replication covers only a 2D toy dataset; all image-generation results (CIFAR-10 FID/IS, CelebA, LSUN), likelihood evaluation, architecture comparisons, and cor |
| Yuval-OGorman-2020-Climate | 3/6 | PARTIAL | Only methodology/architecture and training-time claims were testable; all quantitative empirical claims (R² values, stability, speedup) were data-blocked. Synth |

## Judge notes — highest-scored reports (Coverage ≥ 8)

| ID | C/A | Verdict | Judge note |
|---|---|---|---|
| LUCID-replications/lucid-stochastic-poisson-dna-damage | 9/10 | REPLICATED | All 13 testable claims verified including headline sub-Poissonian result (Fano≈0.685), moment trajectories, and all three figures; agreement between SSA and LNA |
| LUCID-replications/lucid-turner-gamma-h2ax-biodosimetry | 9/8 | REPLICATED | All central claims reproduced: Table-2 parameters within CIs, all four Table-3 Pearson/Spearman correlations within ~0.04/0.13, spleen day-14 result essentially |
| PDE-replications/pinn-rans-eivazi-2022 | 9/6 | PARTIAL | All 5 test cases and all 22 Table 1 entries addressed (high coverage). Quantitative agreement is mixed: 10/22 claims within 2x tolerance, 7/22 partially reprodu |
| 1379592-Mathematical-Foundations-of-the-GraphBLAS | 8/9 | REPLICATED | All 11 core operations, 7 worked figures, and 6 graph algorithms reproduced with exact or near-exact agreement; algebraic properties verified exhaustively for B |
| 1475143-FDTD-solving-1+1D-delay-PDE-in | 8/8 | PARTIAL | 5 of 6 figures reproduced; Fig 5 bit-exact to 6+ digits, Fig 6/7 g2 values within 5-10% of paper; Fig 8 skipped due to 125 GB memory wall; true intra-timestep p |
| 1565592-Markov-state-models-from-short-non-equilibrium | 8/7 | REPLICATED | All three numerical experiments replicated; 1D exact timescale within 0.2%, 2D within 2%, alanine dipeptide OOM correction recovers slow timescale (2146 vs 2020 |
| 1606674-Common-Mode-Voltage-Reduction-of-Single-Phase | 8/9 | REPLICATED | Central CMV-halving claim reproduced exactly (50% peak reduction, ~40 dB harmonic attenuation at 10 kHz); leakage current reductions consistent with paper envel |
| 1842593-MOTION-TOMOGRAPHY-VIA-OCCUPATION-KERNELS | 8/8 | PARTIAL | All three synthetic flow fields, convergence study, and parameter sweeps replicated with matching qualitative trends and quantitative results in same range or b |
| 1983793-Simple-coplanar-waveguide-resonator-mask-targeting | 8/8 | PARTIAL | Central CPW impedance, 8-resonator frequency plan, quarter-wave lengths, Q_c vs coupler length, and participation ratio ordering all reproduced; 3D FEM eigenmod |
| 2396968-Latent-Stochastic-Differential-Equations-for-Modeling | 8/6 | PARTIAL | Full 6-band physics pipeline with all 9 parameters and GR transfer functions replicated end-to-end; qualitative parameter-recovery hierarchy and calibration rep |
| 2441075-Exactly-solved-model-of-light-scattering-errors-in | 8/9 | PARTIAL | Core analytic solution (Eqs. 6-10), Lindblad numerics, branching ratios, and qualitative figures 2-4 reproduced at machine precision; missing full 2D Penning-tr |
| 2475938-Updated-Virophage-Taxonomy-and-Distinction-from | 8/8 | REPLICATED | Central claims reproduced: HMM-based virophage/PLV discrimination, four-marker phylogenies recovering Mavirus-basal and SW01-YSLV4 sister topology, and marker-p |
| BVBRC-01-CRKP-Zhang2022 | 8/7 | REPLICATED | 90% of claims tested; central KL47→KL64 transition and differential virulence findings strongly replicated; quantitative discrepancies explained by database gro |
| BVBRC-03-Saureus-mastitis-Sivakumar2023 | 8/7 | REPLICATED | 94% of claims tested across all 41 strains; core findings (15 STs, 5 CCs, MSSA status, blaZ/sak/PVL distributions, ica operon) exactly reproduced; 6 partial mat |
| BVBRC-09-blaNDM5-K-pneumoniae-Yuan2019 | 8/8 | REPLICATED | All 19 in-silico claims tested and verified (17 fully, 2 partially); 4 wet-lab claims appropriately flagged as untestable. Minor discrepancies in pgi allele cal |
| LUCID-replications/lucid-autofoci-detection | 8/9 | REPLICATED | Core algorithmic contribution (OEP equations 1-4) fully reimplemented in Python; headline ρ=0.90 reproduced to 0.890; all 5 key metrics within 0.04 of paper; bi |
| LUCID-replications/lucid-grandt-fibroblast-rnaseq | 8/9 | PARTIAL | All downstream quantitative claims checkable from supplementary tables replicate exactly (DEG counts, %up, top genes 11/12, all 7 interaction genes, pathway ORA |
| LUCID-replications/lucid-matsuya-nte-integrated | 8/6 | PARTIAL | All 10 explicit numeric claims attempted; 4 fully replicated, 2 spot-check, 2 partial, 1 contradicted, 1 paper-internal inconsistency. Central qualitative claim |
| LUCID-replications/lucid-ulyanenko-gammah2ax-patm-msc | 8/9 | REPLICATED | All three linear regressions reproduced to ≥3 decimal places from algebraically recovered table data; hockey-stick threshold models qualitatively confirmed; kin |
| PDE-replications/laplace-no | 8/6 | PARTIAL | 9 of 12 benchmarks attempted (3 skipped due to GDrive data access); qualitative LNO>FNO claim reproduced with 4.5x advantage; only 4/9 benchmarks within 20% of  |
| replicate-msm | 8/7 | PARTIAL | All three numerical experiments replicated; central OOM-correction claim confirmed across 1D, 2D, and MD systems. Phase 1 exact timescale within 0.2%, Phase 2 w |

## Source files

- `MASTER_TOOLS_AND_RESOURCES_2026-05-31.md` — this document (v3, pure-LLM scoring)
- `MASTER_SCORES_2026-05-31.csv` — flat per-paper table with full judge notes
- Raw scoring data: `/tmp/replicate_final_v2.json` (regenerable)
- Sonnet 4.6 scoring script: `/tmp/score_unscored.py`

## Methodology change vs v1/v2

v1 (this morning) used only regex extraction — 35/129 reports scored. v2 added LLM gap-fill — 129/129 scored but mixed author self-reports (regex-extracted) with independent judgment (LLM). Rick flagged this: "we have a rule about no regex based reporting and scoring." **v3 (this document) discards the regex scores entirely; all 129 are Sonnet 4.6 single-judge.** The mean coverage dropped from 6.10 (mixed) to 5.47 (pure-LLM) — confirming the regex-extracted author self-scores were biased ~0.6 points high. Rule is now baked into skill `corpus-structured-extraction` (HARD RULE section).