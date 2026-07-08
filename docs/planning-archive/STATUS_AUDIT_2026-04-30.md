# REPLICATE-PROJECT — Honest Status Audit
**Date:** 2026-04-30 · **Auditor:** Ollie (subagent `audit-2026-04-30`) · **Scope:** 56 subdirectories under `~/Dropbox/REPLICATE-PROJECT/` + 12 PDE-replications subdirs
**Reference:** `STATUS_AUDIT_2026-04-28.md` (prior audit, 51 dirs, ~46 papers)

---

## Executive Summary

The corpus has grown from **51 directories / ~46 papers** (2026-04-28) to **56 directories / 50+ distinct paper entries** (2026-04-30). **14 new additions** appeared in the last 48 hours: 7 brand-new paper replications (3 in standalone dirs, 2 as PDE subdirs, 2 already started) + 3 former PREP-ONLY stubs that are now ACTUAL (1578031, 1984484, 1993311) + 4 papers that upgraded from COMPUTE-BOUND/SHALLOW to ACTUAL (1484740, 1868518, 2587225, 1861801).

The distribution has shifted meaningfully toward ACTUAL: **22 ACTUAL** (up from 14) at the cost of clearing 3 PREP-ONLY stubs and resolving 4 COMPUTE-BOUND upgrades. The number of SHALLOW entries drops by 1 (Graph-RL headline claim now replicated). PREP-ONLY entries drop from 5 to 2, STALLED to 0 (though 1609039 is reclassified as UNVERIFIED — see ⚠️ below).

**Key discrepancy confirmed:** `1609039` Cu₆₄Zr₃₆ metallic glass is described in the LaTeX report with specific quantitative claims ("9 σ-ε curves, LAMMPS EAM, 24× atom-count reduction") but **zero artifacts exist in the project directory** (last modified: Apr 8). Work may have run on a compute node without being copied back. Master README says "✅ Complete (7/8+6/8)" — this claim is UNVERIFIED until artifacts land in the project dir.

**Another discrepancy confirmed:** koopman-no LaTeX tier-lift report (2026-04-27) claimed NS-2D was completed with specific KNO/FNO scores — but **no NS-2D artifacts exist**. This is now **explicitly disclosed in the REPORT.md** (updated Apr 30 11:03). Score corrected to 5/10 coverage in REPORT.md.

---

## Distribution

| Assessment | 2026-04-28 | 2026-04-30 | Δ | Notes |
|---|---:|---:|---:|---|
| **ACTUAL** | 14 | 22 | +8 | 3 PREP-ONLY converted + 4 upgrades + 7 new papers all ACTUAL |
| **COMPUTE-BOUND** | 11 | 9 | −2 | ScaWL, GaN, NukeLM, Virophage upgraded; new jax-cfd still COMPUTE-BOUND |
| **SHALLOW** | 8 | 7 | −1 | Graph-RL 8500-bus done; CROC still SHALLOW (REPORT honest, README misleads) |
| **DATA-BLOCKED** | 3 | 3 | 0 | CROC, Latent SDE, fem-vs-pinns (unchanged) |
| **TOOL-BLOCKED** | 2 | 2 | 0 | PATRIC/SEEDtk, unchanged |
| **PREP-ONLY / STALLED** | 5 | 2 | −3 | 1578031 + 1984484 + 1993311 converted; 1578031 PREP-ONLY removed from count |
| **UNVERIFIED (artifacts missing)** | 0 | 1 | +1 | 1609039 metallic glass — LaTeX claims it but no dir artifacts |
| **N/A (meta/alias)** | — | — | — | alias + meta dirs unchanged |

---

## Per-Paper Audit Table
*Sorted by severity. Cov/Agr from REPORT.md or scoring/evaluations_all.jsonl (latest record). "Last activity" = newest non-dotfile mtime.*

### 🔴 UNVERIFIED — Artifacts Missing

| OSTI ID | Title (short) | Domain | Cov/Agr (claimed) | Last activity | Evidence | Assessment | Action |
|---|---|---|:---:|---|---|---|---|
| **1609039** | Cu₆₄Zr₃₆ Metallic Glass MD | Materials/MD | **7/8** (tex) | **Apr 8 (dir unchanged)** | Plan TeX only in dir (`replication_plan.tex`, `1609039.pdf`). LaTeX report (line 1075–1103) describes 9 σ-ε curves, LAMMPS EAM, 3T×3ε̇, 24× atom-count reduction — **but no `replication/` directory, no LAMMPS output files, no results JSON exist anywhere in the project tree.** Not in `scoring/evaluations_all.jsonl`. Master README claims "✅ Complete (7/8+6/8)". | ⚠️ **UNVERIFIED** — LaTeX appears to describe real work that was never copied to project dir. Could be on uicgpu/sparks scratch. | **CHECK uicgpu/sparks scratch; copy artifacts to `1609039-…/replication/`; then update REPORT.md. Do not leave in paper without artifact trail.** |

---

### 🟠 SHALLOW / DATA-BLOCKED / TOOL-BLOCKED

| OSTI ID | Title (short) | Domain | Cov/Agr | Last activity | Evidence | Assessment | Action |
|---|---|---|:---:|---|---|---|---|
| 1275503 | Cosmic Reionization on Computers (CROC) | Astrophysics | 5/4 | Apr 30 10:18 | FGPA semi-analytic surrogate; 12 figs; `analysis_results.json`. REPORT.md explicitly says "This replication is fundamentally shallow" and "rescaling factors 0.18–0.49 are large." **BUT master README says "✅ Complete."** | **SHALLOW** — REPORT honest, README misleads | **Fix README row 16 to say "⚠️ Partial (surrogate-only, 5/10)"** |
| 2469515 | PATRIC Supervised Genome Extraction | Bioinformatics | 4/5 | Apr 30 10:18 | MetaBAT2 baseline only; PATRIC/SEEDtk supervised arm requires proprietary BV-BRC DB (193k genomes). README correctly shows "⚠️ Partial (4/10)". | **TOOL-BLOCKED** on paper's central contribution | DEFER |
| 2396968 | Latent SDE (Quasar variability) | ML/Astrophysics | 9/6 | Apr 30 10:56 | v1_simplified + v2_faithful trained; WeatherBench2 zarr unreachable; 100× retrain out of scope. | **DATA-BLOCKED + COMPUTE-BOUND** — coverage generous | DEFER (ERA5) |
| 3003857 | Penalty Neural ODE chaos | ML/Math | 7/7 | Apr 30 10:58 | KS/Lorenz ACTUAL; ERA5 atmospheric demo still DATA-BLOCKED | **DATA-BLOCKED** on atmospheric; ACTUAL on KS/Lorenz | DEFER (ERA5) |
| 1275503 | fem-vs-pinns (Grossmann 2023) | PDE/ML | 7/10 | (PDE-replications) | 1D Poisson full; 2D/1D AC partial; 3D Poisson + Schrödinger missing eval data | **DATA-BLOCKED** on 3D/Schrödinger | DEFER |
| PVMol-Gen | Fajar 2026 perovskite passivation | Materials/GenML | 7/5 | Apr 11 (pvmol-gen-fajar2026) | SMILES-X classifier underperforms; 0 of 10 candidates match paper Rep10; xTB/DFT post-filter missing | **COMPUTE-BOUND/SHALLOW** on benchmark match | DEEPEN (xTB filter) |
| 1868518 [↑] | ~~SHALLOW~~ → Graph-RL 8500-bus | ML/Power | 8/7 | Apr 30 10:38 | `8500_comparison_bar.png` + `8500_learning_curves.png` + `eval_summary.json` present: GCN 99.67% restoration at 2.39s vs paper 100%/2.02s; MLP collapses to 55% confirming graph necessity. **WAS SHALLOW, NOW ACTUAL.** | ✅ **ACTUAL** — headline IEEE-8500 reproduced | ACCEPT |

---

### 🟡 COMPUTE-BOUND (real pipeline, reduced scale or missing benchmark)

| OSTI ID | Title (short) | Domain | Cov/Agr | Last activity | Evidence | Assessment | Action |
|---|---|---|:---:|---|---|---|---|
| 1559043 | Ignition Kernel PeleC | CFD/Combustion | 7/7 | Apr 28 12:26 | PeleC v1-v4: 4φ×5 realizations (13/20 complete); v5 plan ready but Polaris MFA locked. REPORT: "CO2 rollover not captured." | **COMPUTE-BOUND** — v5 parked on Polaris MFA | RICK: restore Polaris MFA → run v5 → 9/10 |
| 1864334 | NN-VMC A≤4 Nuclei | Nuclear/ML | 8/9 | Apr 30 10:36 | PyTorch VMC, A=2/3/4, ³He–³H Coulomb +0.75 vs +0.764 MeV; 3-body V_3N partial; spin-orbit V_LS=0 (symmetry limit on S-wave) | **COMPUTE-BOUND** — 3-body + spinor extension pending | ACCEPT |
| 2571909 | CHF Hybrid ML | Nuclear/ML | 7/8 | Apr 28 12:39 | 96 result files, 55 figs; authors' dataset only partial; NUREG-2014 full table not obtained | **ACTUAL (hybrid arch) / DATA-BLOCKED (full benchmark)** | DEFER full dataset |
| 1606674 | CMV Reduction qZSI | Power Electronics | 8/9 | Apr 30 10:31 | Python state-space + waveforms; sim-only, no hardware-in-loop | **COMPUTE-BOUND** | ACCEPT |
| 2587225 [↑] | ~~COMPUTE-BOUND~~ → ScaWL 3-WL | Graph/HPC | 9/10 | Apr 28 13:06 | C++17/MPI 3-WL on chiatta00; 26.4× strong scaling; memory myth busted (8 MB not 100 GB); multi-node Cray (2193×) still out of scope | ✅ **ACTUAL single-node 3-WL; COMPUTE-BOUND on multi-node** | ACCEPT as is |
| 1981773 | Pt/La₂Ti₂O₇ DFT | DFT/Catalysis | 8/8 | Apr 28 19:55 | Yambo PBE/RPA + HSE06; 2.40 eV redshift vs 2.20 (9%); (010) facet vc-relax abandoned | **COMPUTE-BOUND** on facet comparison | ACCEPT |
| koopman-no | Koopman Neural Op | PDE/ML | 5/7 | Apr 30 11:03 | 1D Burgers + resolution transfer + eigenvalues; NS-2D BLOCKED. REPORT.md NOW EXPLICITLY DISCLOSES phantom LaTeX claim. | **DATA-BLOCKED on NS-2D; ACTUAL on Burgers/eigenvalues** | ACCEPT (phantom now disclosed) |
| jax-cfd | Kochkov 2021 JAX-CFD | PDE/ML | n/a | 2026-04-27 | LI(64) trained 20K steps; Re=4000/7000 partial; decaying turbulence missing | **COMPUTE-BOUND** | DEEPEN |
| laplace-no | Cao 2024 LNO | PDE/ML | 8/8 | recent | 9/12 benchmarks; 3 skipped (Google Drive blocked) | **DATA-BLOCKED** on 3 benchmarks | DEFER |
| 2475938 [↑] | ~~COMPUTE-BOUND~~ → Virophage Tax. | Bioinformatics | 8/10 | Apr 28 19:11 | 279-genome NCBI scale-up (21× baseline); 70-taxon 4-marker ML tree recovers all class boundaries; IMG/VR uncultivated tail still skipped | ✅ **ACTUAL at paper's core claim; COMPUTE-BOUND at IMG/VR scale** | ACCEPT |
| 1412756 | Chiral Spin Kondo-Heisenberg | CMT | 8/8 | Apr 30 10:22 | MF + Wolff-MC 2D Ising test β/ν=0.128 vs 0.125; Sr₂VO₃FeAs material not run | **COMPUTE-BOUND** — material-specific gap | ACCEPT |
| 1523841 | Shift photocurrent | CMT/Optics | 8/10 | Apr 30 10:29 | Rice-Mele + Wilson-loop + BHZ; DFT+Wannier for GeS/BaTiO₃ missing | **COMPUTE-BOUND** on materials | ACCEPT |
| lightning-laplace | Gopal-Trefethen 2019 | Numerical PDE | n/a | recent | Laplace fully done; Helmholtz partial | **COMPUTE-BOUND** on Helmholtz | ACCEPT |

---

### ✅ ACTUAL (full pipeline, key claims reproduced)

| OSTI ID | Title (short) | Domain | Cov/Agr | Last activity | Assessment | Action |
|---|---|---|:---:|---|---|---|
| 1997354 | Hausdorff Integer Sequences | Mathematics | 10/10 | Apr 30 10:15 | All 13 closed-forms; 327k graphs to K₄,₄/K₃,₆ | **ACTUAL** | ACCEPT |
| 1379592 | GraphBLAS Foundations | Graph Algo | 9/10 | Apr 30 10:15 | 5 .py + 4 figs | **ACTUAL** | ACCEPT |
| 2582579 | NILC Cosmological Params | CMB/Cosmology | 8/8 | Apr 30 10:55 | <0.2% recovery Eq.26; pyilc + NILC-PS-Model | **ACTUAL** | ACCEPT |
| 1842593 | Motion Tomography | Signal | 8/8 | Apr 30 10:15 | Algorithm 1 + Expt 1 + sweeps; 10 figs | **ACTUAL** | ACCEPT |
| fast-poisson-spectral | Fortunato-Townsend 2017 | Numerical PDE | 9/10 | recent | Spectral conv 1.8e-14; ADI crossover n=1024; O(n²log²n) to n=2048 | **ACTUAL** | ACCEPT |
| 1565592 | Hempel MSM (via msm-replication/) | Mol Dynamics | 9/8 | Apr 21 (real) | 1D well + 2D + ADP; OOM correction confirmed | **ACTUAL** | ACCEPT |
| 1983793 | CPW Resonator | Quantum Dev | 8/8 | Apr 30 10:54 | Analytical + 2D FD + KI + GDS + Palace 3D eigenmode all 8 resonators | **ACTUAL** | ACCEPT |
| 1997354 | Dark Matter SD (3014512) | Particle | 8/8 | Apr 30 10:15 | DarkELF tier-lift; tierlift_results.pkl; 13 figs | **ACTUAL** | ACCEPT |
| 1461824 | Photo-z PDFs | Astrophysics | 8/8 | Apr 30 10:25 | Stacked N(z), brightness-binned diagnostics | **ACTUAL** | ACCEPT |
| 2441075 | Trapped-Ion Qubits | Quantum | 8/9 | Apr 30 10:16 | Eqs 6-10 + Lindblad ME + Ca-40; Figs 1-4; 2D-crystal modes COMPUTE-BOUND | **ACTUAL** | ACCEPT |
| 2571540 | BayesOpt qHSRI | Optimization | 8/8 | Apr 30 10:55 | BoTorch + trieste + authors' R/PBBO 3-way agreement | **ACTUAL** | ACCEPT |
| 1427646 | Deep Learning STEM | ML/Imaging | 8/8 | Apr 30 10:21 | tier-lift-v2.5: real experimental graphene STEM frames; LOF cross-domain F1=0.75 (**NOTE:** REPORT.md in dir still says 6/7 — outdated; scoring ledger shows 8/8 from tier-lift-v2.5) | **ACTUAL** | UPDATE REPORT.md in dir |
| 2439897 | rVAE | ML/Imaging | 8/9 | Apr 28 13:09 | SE(2)-equivariant; atomai 0.8.1; 4 result files; 10 figs | **ACTUAL** | ACCEPT |
| 1624105 | Linclust | Bioinformatics | 9/10 | Apr 30 10:32 | Algorithm reimpl + benchmarks | **ACTUAL** | ACCEPT |
| 1983793 | (see CPW above) | | | | | | |
| 1484740 [↑] | ~~COMPUTE-BOUND~~ → 2D GaN | DFT/Materials | 9/9 | Apr 28 15:14 | Bilayer now converged (F_max 0.000598 Ry/Bohr); Yambo BSE scissor; plasmon ωp≈10 eV matches paper Fig 5. **WAS bilayer-incomplete, NOW fully done.** | ✅ **ACTUAL** | ACCEPT |
| 2217719 | SCALE MSRE depletion | Nuclear Eng | 8/8 | Apr 30 10:55 | Bateman ODE Hartanto+ 2024; **Attribution FIXED** (was Betzler/Powers/Worrall in old README — now correctly Hartanto, Bostelmann, Betzler, Bekar, Hart, Wieselquist). REPORT.md now present in main dir (Apr 30). | **ACTUAL (Bateman ODE substitutes SCALE/ORIGEN; disclosed)** | ACCEPT with disclosure |
| 1475143 | FDTD delay PDE | Numerical | 8/8 | Apr 30 10:27 | Figs 5–7 reproduced; Fig 8 out of reach. **Attribution still stubs in main dir README** — real work in `fdtd-delay-pde/` alias. | **ACTUAL** | Consolidate alias into main dir |
| 1861801 [↑] | ~~COMPUTE-BOUND~~ → NukeLM | NLP/Domain | 8/10 | Apr 28 18:29 | Full 325K OSTI abstracts (114M tokens); MLM loss 0.641 surpasses paper's 0.95; NukeLM Binary F₁=0.710 tops ranking. **WAS 30k-corpus COMPUTE-BOUND, NOW full-scale.** | ✅ **ACTUAL** | ACCEPT |
| 1868518 [↑] | Graph-RL 8500-bus (see above) | ML/Power | 8/7 | Apr 30 10:38 | (moved to ACTUAL from SHALLOW — see above) | ✅ **ACTUAL** | ACCEPT |
| 2587579 [NEW] | Mesh-based Super-Res GNN | PDE/ML | 8/8 | Apr 28 14:36 | 4.77× L2 reduction; halo-swap bitwise validated 3 configs; 3D BFS hex mesh; DDP_PyGeom multi-rank. All artifacts present. | ✅ **ACTUAL** | ACCEPT |
| 2587945 [NEW] | ELM Tokamak Forecaster | Fusion/ML | 8/8 | Apr 28 13:07 | FNO-2D + ConvLSTM + Chronos + Temporal-VAE on synthetic BES; ConvLSTM > FNO ρ_resid 0.615 vs 0.580 confirms paper ranking; real DIII-D not public. | ✅ **ACTUAL** (synthetic data) | ACCEPT |
| space-nanograv-15yr-gwb [NEW] | NANOGrav 15-yr GWB | Astrophysics/GW | 8/8 | Apr 30 10:14 | DR3 pre-sampled chains; HD correlation + spectral params; γ=3.35 vs paper 3.2 (<0.5σ); full Bayesian inference from scratch not done. All artifacts present. | ✅ **ACTUAL** | ACCEPT |
| space-bls-exoplanets [NEW] | BLS Kepler Transit Detection | Astrophysics | 8/8 | Apr 30 10:14 | From-scratch BLS; 6 Kepler planets to <0.012% period error; beats astropy. Artifacts: bls_results.json + 7 figs. | ✅ **ACTUAL** | ACCEPT |
| space-camels-emulator [NEW] | CosmoPower-style P(k) Emulator | Cosmology/ML | 8/8 | Apr 30 07:34 | 400-cosmo training on CAMB-generated spectra; eval_results.json + training_history.json + 3 figs + emulator_best.pt. | ✅ **ACTUAL** | ACCEPT |
| 1578031 [↑] | ~~PREP-ONLY~~ → fldgen v2.0 | Climate/Stats | 8/8 | Apr 30 06:52 | Code (fldgen.py, synthetic_esm.py, run_replication.py) + 4 figs + 10 data NPZ/JSON. Synthetic ESM input (not CMIP5 — disclosed). **WAS plan-TeX-only.** | ✅ **ACTUAL** (synthetic ESM) | ACCEPT with caveat |
| 1984484 [↑] | ~~PREP-ONLY~~ → DRAS RL | Systems/RL | 8/8 | Apr 30 06:43 | event-driven sim + FCFS/SJF/EASY-BF baselines + DQN + PPO; HPC2N trace 5K jobs×240 nodes; ppo_model.pt + 5 figs + test_results.json. **WAS plan-TeX-only.** | ✅ **ACTUAL** | ACCEPT |
| 1993311 [↑] | ~~PREP-ONLY~~ → DMQMC+GPR | DFT/Stats | 8/8 | Apr 30 06:43 | GPR composite-kernel; 14.6×/44× noise improvement; summary.json + 4 Hubbard result files + 10 figs. Synthetic data only (no HANDE-QMC). **WAS plan-TeX-only.** | ✅ **ACTUAL** (synthetic data) | ACCEPT with caveat |
| PDE-replications/poisson-flow-generative [NEW] | PFGM (Xu et al. 2022) | ML/PDE | 7/8 | Apr 30 | PFGM + VE-diffusion on 2D 8-mode MoG; SWD 0.049 vs 0.059; step-size robustness partially confirmed; CIFAR/CelebA skipped. | ✅ **ACTUAL** (toy 2D) | ACCEPT |
| PDE-replications/godunov-loss [NEW] | Godunov Loss hyperbolic PDE | Numerical PDE | 4/8 | Apr 30 07:09 | MSE vs Godunov-hybrid; honest negative result — MSE competitive/better on all 3 test cases; **paper PDF not found** (reconstructed from concept). All artifacts present. | ✅ **ACTUAL (honest negative)** — **⚠️ paper PDF unlocated** | FIND exact paper; if confirmed negative, PUBLISH as honest null result |
| dedalus | Burns 2020 Dedalus | PDE Spectral | 8/8 | recent | 6/8 demos; sphere/ball missing | **ACTUAL** | ACCEPT |
| walk-on-stars | Sawhney 2023 WoS | Grid-free MC | n/a | recent | Lens/square/L-shape; O(N^-1/2) confirmed | **ACTUAL** | ACCEPT |
| latent-spectral-models | Wu 2023 LSM | PDE/ML | n/a | recent | LSM reimpl on A100 | **ACTUAL** | ACCEPT |
| kinetic-jl | Xiao 2021 Kinetic.jl | Kinetic Theory | n/a | recent | Julia toolbox replicated | **ACTUAL** | ACCEPT |

---

### 📁 PREP-ONLY (no replication pipeline executed)

| Dir | Title | Last activity | Evidence | Assessment |
|---|---|---|---|---|
| 1578031 | (see above — now ACTUAL) | | | |
| 1565592 (stub dir) | MSM stub | Apr 8 | Plan TeX only; real work in `msm-replication/` | PREP-ONLY (this dir); ACCEPT alias |
| perovskite-Passivation-Molecules-AI-Discovery | PVMol-Gen plan stub | Apr 5 | README + paper PDF only | PREP-ONLY (alias stub); merge into pvmol-gen-fajar2026 |

---

### 📁 Meta / Alias / Staging (not unique papers)

| Dir | Purpose | Status |
|---|---|---|
| `2217719-scale-msr/` | alias for 2217719 | Consolidate |
| `bayesopt-qhsri/` | alias for 2571540 | Consolidate |
| `cpw-resonator/` | alias for 1983793 | Consolidate |
| `fdtd-delay-pde/` | alias for 1475143 (has real work!) | Merge real work to main dir |
| `msm-replication/` | real replication work for 1565592 | ACCEPT (canonical) |
| `replicate-msm/` | alias for 1565592 | Consolidate |
| `photoz-pdfs/` | alias for 1461824 | Consolidate |
| `pvmol-gen/` | alias for pvmol-gen-fajar2026 | Consolidate |
| `replicate-1559043-combustion/` | v5 plan for 1559043 (plan-only, run blocked on Polaris MFA) | DEEPEN when MFA restored |
| `pde_candidates/` | meta — 30-paper PDE survey | N/A — retain |
| `pde_corpus/` | empty staging | DROP |
| `scoring/` | evaluation ledger | retain |
| `drafts/` | email draft | retain |

---

## ⚡ DIFF vs 2026-04-28

### 1. Newly Added Papers (created after Apr 28)

| Paper | Dir | Score | Status |
|---|---|---|---|
| Mesh-based Super-Resolution GNN (new) | `2587579-…` | 8/8 | ✅ ACTUAL |
| ELM Tokamak Forecaster (new) | `2587945-…` | 8/8 | ✅ ACTUAL |
| NANOGrav 15-yr GWB (new) | `space-nanograv-15yr-gwb/` | 8/8 | ✅ ACTUAL |
| BLS Kepler Exoplanet Transit (new) | `space-bls-exoplanets/` | 8/8 | ✅ ACTUAL |
| CosmoPower P(k) Emulator (new) | `space-camels-emulator/` | 8/8 | ✅ ACTUAL |
| PFGM Poisson Flow Generative (new PDE) | `PDE-replications/poisson-flow-generative/` | 7/8 | ✅ ACTUAL |
| Godunov Loss PDE (new PDE, honest negative) | `PDE-replications/godunov-loss/` | 4/8 | ✅ ACTUAL (null result) |

### 2. Score Changes / Status Upgrades vs Prior Audit

| Paper | Prior status | Prior score | New status | New score | Mechanism |
|---|---|---|---|---|---|
| **1484740 2D GaN** | COMPUTE-BOUND (bilayer not converged) | 8/8 | ✅ ACTUAL | **9/9** | Bilayer F_max 0.000598 Ry/Bohr; Yambo BSE scissor; plasmon match |
| **1868518 Graph-RL** | SHALLOW (8500-bus missing) | 5/5 | ✅ ACTUAL | **8/7** | `eval_summary.json` + 2 figs confirm 99.67% 8500-bus restoration |
| **2587225 ScaWL** | COMPUTE-BOUND (2-WL only, no 3-WL) | 7/8 | ✅ ACTUAL (single-node) | **9/10** | C++17/MPI 3-WL on chiatta00; memory myth busted (8 MB not 100 GB) |
| **1861801 NukeLM** | COMPUTE-BOUND (30k abstracts) | ~7 | ✅ ACTUAL | **8/10** | 325K OSTI abstracts; MLM 0.641 surpasses paper |
| **2475938 Virophage** | COMPUTE-BOUND (13-genome) | 6/7 | ✅ ACTUAL (279-genome) | **8/10** | 279-genome NCBI scale-up; all class boundaries recovered |
| **1578031 fldgen** | PREP-ONLY | n/a | ✅ ACTUAL | **8/8** | code + 4 figs + 10 data files (synthetic ESM) |
| **1984484 DRAS** | PREP-ONLY | n/a | ✅ ACTUAL | **8/8** | DQN + PPO on HPC2N trace; ppo_model.pt + 5 figs |
| **1993311 DMQMC+GPR** | PREP-ONLY | n/a | ✅ ACTUAL | **8/8** | GPR beats FD 14.6×/44×; synthetic Hubbard data |
| **koopman-no** | COMPUTE-BOUND (claimed NS-2D in LaTeX) | ~8/8 | COMPUTE-BOUND (honest) | **5/7** | REPORT.md now explicitly discloses phantom LaTeX claim |

### 3. Phantom Claims Caught / Resolved

#### ⚠️ PHANTOM CLAIM — CONFIRMED UNRESOLVED
> **`koopman-no` LaTeX tier-lift report (2026-04-27):** Claimed NS-2D completed with KNO=0.0118 vs FNO=0.0186. **No NS-2D artifacts exist on disk.** Now explicitly disclosed in REPORT.md (updated Apr 30 11:03). Score corrected to 5/10 coverage in REPORT.md. **However, the LaTeX report file `report/2301.10022_replication_report.tex` still contains the phantom numbers** — it should be edited or retracted.

#### ⚠️ PHANTOM CLAIM — UNVERIFIED ARTIFACTS
> **`1609039` Cu₆₄Zr₃₆ metallic glass:** The REPLICATION_EVALUATION_REPORT.tex (lines 1075–1103) describes "9 σ-ε curves (3T×3ε̇), LAMMPS EAM, 24× atom-count reduction" and the master README says "✅ Complete (7/8+6/8)." The `1609039-…/` project directory shows **last modified: Apr 8**, contains **only the plan TeX + paper PDF**, has **no `replication/` directory**, and does **not appear in `scoring/evaluations_all.jsonl`**. The work may exist on a compute node (uicgpu/sparks) but was never committed to the project directory. **This is an artifact-trail gap, not a fabrication, but it cannot be audited or verified as stated.**

#### ✅ ATTRIBUTION ERRORS — FIXED
> **`2217719` SCALE:** Prior README had wrong authors (Betzler/Powers/Worrall); REPORT.md now correctly attributes to Hartanto, Bostelmann, Betzler, Bekar, Hart, Wieselquist (2024). ✅ Fixed.

> **`1475143` FDTD:** Main dir README still shows old plan stub (unchecked boxes) — real work is in `fdtd-delay-pde/` alias. Not a phantom claim but a consolidation gap. ⚠️ Not yet merged.

### 4. REPORT.md vs README vs Scoring Ledger Inconsistencies

| Paper | REPORT.md | Master README | Scoring Ledger | Verdict |
|---|---|---|---|---|
| **1427646 STEM** | 6/10 cov, 7/10 agr (**outdated REPORT.md**) | 8/8 ✅ Complete | tier_lift_v2.5 → 8/8 (Apr 27) | Scoring ledger + README correct; **REPORT.md in dir needs update** |
| **koopman-no** | 5/10 cov, 7/10 agr (REPORT.md updated Apr 30) | README not listed | not in ledger | REPORT.md is the authoritative source; LaTeX tex still has phantom numbers |
| **1275503 CROC** | 5/4 (REPORT.md: "fundamentally shallow") | "✅ Complete" | 5/5 in ledger (old) | Master README **MISLEADS** — should be "⚠️ Shallow (surrogate only)" |

---

## Summary: Corpus Count (2026-04-30)

| Category | Count |
|---|---|
| Unique paper replications (OSTI + named) | **41** |
| PDE-replications subdirs | **12** |
| **Total distinct paper entries** | **53** |
| Alias/duplicate directories | 8 |
| Meta/staging directories | 5 |
| **Total directories on disk** | **56** |

**Prior audit (2026-04-28):** ~46 papers / 51 dirs.  
**Delta:** +7 net new paper entries, +5 directories.

---

## Top-3 Most Important Diffs (Summary for Main Agent)

### 1. 🔴 1609039 Cu₆₄Zr₃₆ — Artifact Trail Gap (Most Urgent)
The REPLICATION_EVALUATION_REPORT.tex includes a detailed section for 1609039 with specific quantitative claims (9 σ-ε curves, LAMMPS EAM, 3T×3ε̇). Master README says "✅ Complete (7/8+6/8)." But the project directory has **zero artifacts** — only the Apr 8 plan TeX. Work may be on uicgpu/sparks scratch. Before the paper is submitted, either: (a) locate the artifacts and commit them to the project dir, or (b) remove this entry from the paper. This is the most material audit gap in the current corpus.

### 2. 🟠 koopman-no LaTeX Phantom — Partially Resolved, LaTeX Still Dirty  
The REPORT.md now honestly discloses the NS-2D phantom (score corrected to 5/10 coverage). However, `report/2301.10022_replication_report.tex` still contains KNO=0.0118 / FNO=0.0186 NS-2D numbers that were never backed by artifacts. The main REPLICATION_EVALUATION_REPORT.tex should not cite these numbers. The LaTeX tier-lift report file should be annotated or retracted.

### 3. 🟢 8 New ACTUAL Replications in 48 Hours (Most Positive)
Between Apr 28 and Apr 30, 8 brand-new replications reached ACTUAL status (2587579 GNN, 2587945 ELM, NANOGrav, BLS, CosmoPower/CAMB, PFGM, godunov-loss, plus 3 former PREP-ONLY stubs). The corpus added 7 new directories. This is a major productivity burst and represents the best two-day output rate of the project.

---

## Recommended Immediate Actions (Priority Order)

1. **[BLOCKING]** Locate 1609039 LAMMPS artifacts on uicgpu/sparks scratch → copy to `1609039-…/replication/` and create `REPORT.md` + `scoring/` entry. OR remove from REPLICATION_EVALUATION_REPORT.tex. **Do not publish with phantom artifacts.**
2. **[BLOCKING]** Edit `PDE-replications/koopman-no/report/2301.10022_replication_report.tex` to retract phantom NS-2D claims, or add a prominent "retracted" annotation. The REPORT.md is clean; the LaTeX tier-lift report is not.
3. **[HIGH]** Fix master README row 16 (1275503 CROC) from "✅ Complete" to "⚠️ Partial (FGPA surrogate, 5/10)".
4. **[MEDIUM]** Update `1427646-…/REPORT.md` to reflect tier-lift-v2.5 score (8/8), replacing the outdated 6/7 numbers.
5. **[LOW]** Merge alias directories (fdtd-delay-pde → 1475143; bayesopt-qhsri → 2571540; cpw-resonator → 1983793; photoz-pdfs → 1461824; pvmol-gen → pvmol-gen-fajar2026; msm-replication → 1565592; 2217719-scale-msr → 2217719).
6. **[LOW — when MFA restored]** Resume 1559043 PeleC v5 on Polaris → most direct path from 7/7 to 9/10.

---

*Audit method: directory walk (`ls -la`, `find` for non-dotfile type-f files), cross-reference with `scoring/evaluations_all.jsonl` (66 records, 30 unique OSTI keys), `README.md` (44-row table), and `REPLICATION_EVALUATION_REPORT.tex` (LaTeX summary). REPORT.md files read for score/gap claims. Specific artifacts confirmed via `find` + targeted `grep`.*
