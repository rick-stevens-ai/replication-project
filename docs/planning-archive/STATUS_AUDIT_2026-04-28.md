# REPLICATE-PROJECT — Honest Status Audit
**Date:** 2026-04-28 · **Auditor:** Ollie (subagent) · **Scope:** 51 subdirectories under `~/Dropbox/REPLICATE-PROJECT/`

---

## Executive Summary

The corpus contains **~46 distinct paper replications** packaged across 51 directories (a few OSTI papers have duplicate work-area aliases — e.g. `1565592-…` (plan) ≡ `msm-replication/` ≡ `replicate-msm/`; `2217719-SCALE-…` ≡ `2217719-scale-msr/`; `pvmol-gen/` ≡ `pvmol-gen-fajar2026/` ≡ `perovskite-Passivation-Molecules-AI-Discovery/`). On honest inspection, **roughly one-third of the corpus genuinely qualifies as ACTUAL** (full pipeline run, paper-claimed quantities reproduced within tolerance), another **third is COMPUTE-BOUND or honest-partial** (real pipeline, reduced scale, score honestly reflects depth), and the **remaining third is SHALLOW, PLAN-ONLY, or DATA/TOOL-BLOCKED** — including five plan-stub directories (`1578031`, `1609039`, `1984484`, `1993311`, `1565592`-stub) where no replication code or results exist beyond the plan TeX. The master `README.md` overstates depth in several places — most notably **1609039 ("Running 76%")** which has zero output artifacts; **1275503 (CROC)** which is a semi-analytic FGPA surrogate, not the actual radiation-hydro simulation; and **1868518 (Graph-RL)** which trains on IEEE-33/123 but skips the paper's headline 8500-bus result. Plan-v5 should retire or relabel these. The strongest replications — `1379592`, `1997354`, `1842593`, `1624105`, `2582579`, `2439897`, `2441075`, `1559043` (PeleC ensemble), `1981773`, the `fast-poisson-spectral` and `dedalus` PDE entries — are real and worth highlighting; the rest needs disclosure.

---

## Distribution

| Assessment | Count | Notes |
|---|---:|---|
| **ACTUAL** | 14 | Full pipeline ran, key claims reproduced within tolerance |
| **COMPUTE-BOUND** | 11 | Real pipeline, scale reduced, score honest |
| **SHALLOW** | 8 | Surrogate/baseline only — paper's headline contribution NOT actually replicated |
| **DATA-BLOCKED** | 3 | Code ready, dataset unobtainable (Google Drive, paywall, or CROC sims) |
| **TOOL-BLOCKED** | 2 | Code ready, proprietary tool unavailable (SEEDtk/PATRIC, BV-BRC) |
| **PREP-ONLY / STALLED** | 5 | Plan TeX + paper PDF only, no replication dir |
| **UNKNOWN** | 0 | All cases adjudicated with file evidence |

---

## Per-Paper Audit Table
*Sorted by severity: SHALLOW + STALLED first, ACTUAL last. Cov/Agr from `scoring/evaluations_all.jsonl` (latest record). "Last activity" is newest non-dotfile mtime.*

| OSTI ID | Title (short) | Domain | Cov/Agr | Last activity | Output evidence | Honest assessment | Recommended action |
|---|---|---|---:|---|---|---|---|
| 1578031 | Joint emulation of Earth System Model | Climate/ML | n/a | 2026-04-04 | Plan TeX only (6 files, no `replication/`) | **PREP-ONLY** — no code, no runs | DROP or DEFER |
| 1609039 | Cu64Zr36 metallic glass MD | Materials/MD | n/a | 2026-04-04 | Plan TeX only; README all checkboxes ❌; master README says "Running 76%" — **misleading** | **STALLED** — claim in master is aspirational | RERUN (LAMMPS in-band) or DROP |
| 1984484 | DRAS Deep RL for Cluster Scheduling | Systems/RL | n/a | 2026-04-04 | Plan TeX only | **PREP-ONLY** | DEFER or DROP |
| 1993311 | Electronic specific heat / entropies | DFT/Thermo | n/a | 2026-04-04 | Plan TeX only | **PREP-ONLY** | RERUN (1-day DFT) or DROP |
| 1565592 (stub dir) | MSM from short non-equilibrium | Mol Dynamics | (real work via `msm-replication/`) | 2026-04-04 (stub) | Stub dir is plan-only; **real replication lives in `msm-replication/` (8/10)** | **PREP-ONLY (this dir)** — see alias | Consolidate dirs; ACCEPT alias |
| 1275503 | Cosmic Reionization on Computers (CROC) | Astrophysics | 5/5 | 2026-04-25 | Single `croc_replication.py` (semi-analytic FGPA + lognormal density), 12 figs, `analysis_results.json`. Report explicitly: *"without access to the original CROC simulation outputs"* | **SHALLOW** — paper's contribution is the radiation-hydro CROC sim; this replicates a downstream FGPA surrogate, not CROC itself | DEFER (DOE access) or DROP — relabel score honestly |
| 1868518 | Graph-RL Distribution Restoration | ML/Power | 5/5 | 2026-04-25 | GCN-DQN + MLP-DQN trained on IEEE-33 & IEEE-123; training history JSON; figs. Report: *"The 8500-node system was not replicated"* — **that is the paper's headline scaling claim** | **SHALLOW** on headline; ACTUAL on small networks | DEEPEN: 8500-bus run on uicgpu (~24 GPU-h) |
| 2469515 | Supervised genome extraction (PATRIC) | Bioinformatics | 3/5 | 2026-04-25 | MetaBAT2 baseline on 5-species synthetic; 5 HQ bins. Report: *"PATRIC supervised pipeline (SEEDtk) — Out of scope: requires the proprietary SEEDtk + 193k-genome BV-BRC reference"* | **TOOL-BLOCKED** on the paper's actual contribution; baseline is honest | DEFER (need PATRIC access) |
| 2396968 | Latent SDE for Motion Capture / WeatherBench | ML | 9/6 | 2026-04-25 | v1_simplified + v2_faithful trained; v2 report: *"WeatherBench2 zarr store could not be reached … did not retrain to convergence … 100× retraining out of scope"* | **DATA-BLOCKED + COMPUTE-BOUND** — coverage 9 is generous; agreement 6 honest | DEEPEN (V100 6-week budget) or DEFER |
| PVMol-Gen Fajar2026 | Generative AI passivation molecules | Materials/GenML | 7/5 | 2026-04-19 | `pvmol-gen/` + `pvmol-gen-fajar2026/`: SMILES-X classifier (underperforms paper); SELFIES pipeline 53k filtered candidates; **0 of 10 final candidates overlap with paper's Rep10** (1 partial G7) | **COMPUTE-BOUND / SHALLOW on benchmark match** — pipeline reproduced but classifier doesn't match paper; missing xTB/DFT post-filter | DEEPEN (xTB filter + DFT), or accept honest gap |
| 1864334 | NN-VMC for A≤4 nuclei | Nuclear/ML | 7/7 | 2026-04-25 | PyTorch VMC, ANN correlator, A=2 + A=4. Report: *"three-body forces, spin-orbit not implemented; main capability gap"* | **COMPUTE-BOUND** — toy ansatz reproduces qualitative behavior; true paper requires full AV18+IL7 | ACCEPT or DEEPEN (3-body, ~1 GPU-week) |
| 2475938 | Updated Virophage Taxonomy | Bioinformatics | 6/7 | 2026-04-26 | 4-marker phylogeny (PRO/MCP/ATPase/Penton) + HMM heatmap on 13-genome subset. Report: *"Class-level revision — Out of scope for 13-genome subset … full IMG/VR dataset out of scope"* | **COMPUTE-BOUND** — sub-sampling honest, headline taxonomy claim not at full scale | DEEPEN (full IMG/VR) |
| 1559043 | Ignition Kernel in Turbulent Flow | CFD/Combustion | 7/7 | 2026-04-26 | PeleC v1→v4: 4φ × 5 realizations on Polaris (20 runs, 13 partial); ignition-propensity Fig.3 analog reproduced. v5 plan exists for AMR + 5ms. Report has explicit "did not capture CO2 rollover" honesty | **COMPUTE-BOUND** (honest 7/10 — reflects partial-run extrapolation) | ACCEPT (current) or DEEPEN via v5 (~4 node-h Polaris) |
| 1606674 | CMV Reduction qZSI Inverter | Power Electronics | 8/9 | 2026-04-25 | Python state-space sim + matplotlib waveforms, "Reproduced leakage-current reduction within spec — Partial" | **COMPUTE-BOUND** — sim-only, no hardware-in-loop validation | ACCEPT |
| 1484740 | 2D GaN electronic/optical | DFT/Materials | 8/8 | 2026-04-25 | QE pseudopotentials, monolayer fully relaxed, **bilayer not converged** (forces ~0.01 Ry/Bohr per report) | **COMPUTE-BOUND** — bilayer is a paper deliverable, partial only | DEEPEN (1-2 days SCF on 1 GPU) |
| 1981773 | Single-atom Pt on La₂Ti₂O₇ | DFT/Catalysis | 8/8 | 2026-04-26 | PBE+USPP slabs + JDOS proxy + Yambo RPA + HSE06; Pt-doped slab partial relax (F_max 0.006). Report: *"facet comparison and optical absorption out of scope of 5-hour run"* | **COMPUTE-BOUND** — solid coverage, headline qualitative | ACCEPT |
| 1427646 | Deep Learning STEM (defect classification) | ML/Imaging | 8/8 | 2026-04-26 | Multislice training set, ResNet trained, `test_metrics.json`, confusion matrix, peak-detection figs | **ACTUAL** | ACCEPT |
| 2587225 | ScaWL — k-WL distributed | Graph/HPC | 7/8 | 2026-04-25 | 2-WL impl + benchmarks. Report: *"3-WL skipped (~100GB at k=3,n=100); single-node only (no distributed); UFL Sparse Matrix Collection skipped"* | **COMPUTE-BOUND** — paper's headline IS distributed/3-WL | DEEPEN (cluster MPI run) |
| 2571909 | Hybrid ML for CHF | Nuclear/ML | 7/8 | 2026-04-25 | 8675 .py files (incl. authors' code drop); 96 result files, 55 figs | **ACTUAL (hybrid arch)** with reduced ensemble | ACCEPT |
| 2571540 | BayesOpt portfolio (qHSRI) | Optimization | 8/8 | 2026-04-25 | BoTorch + trieste re-impl, comparison plots | **ACTUAL** | ACCEPT |
| 2217719 | SCALE MSRE depletion | Nuclear Eng | 8/8 | 2026-04-25 | Bateman-ODE 3-mixture (Pa-233/U-233/Nd-148); Xe-135 sensitivity. Master claims SCALE depletion replicated — actually solved analytically without SCALE | **COMPUTE-BOUND / methodologically-substituted** — substitutes Bateman ODE for ORIGEN/SCALE; result physical but not "SCALE replicated" | ACCEPT (with disclosure) or DEEPEN (actual SCALE6.3 run) |
| 1412756 | Chiral Spin Order Kondo-Heisenberg | CMT | 8/8 | 2026-04-26 | MF treatment + Wolff-cluster MC for 2D Ising universality test (β/ν=0.128 vs 0.125) | **COMPUTE-BOUND** — material-specific Sr2VO3FeAs not run | ACCEPT |
| 1523841 | Polarization-difference / shift photocurrent | CMT/Optics | 8/10 | 2026-04-26 | Rice-Mele + multi-band Wilson-loop + BHZ tier-lift. Report: *"material-specific DFT+Wannier (GeS, BaTiO3) missing"* | **COMPUTE-BOUND on materials, ACTUAL on theory** | ACCEPT |
| 3014512 | Sub-GeV DM SD scattering | Particle | 8/8 | 2026-04-25 | DarkELF tier-lift, `tierlift_results.pkl`, 13 figs | **ACTUAL** within stated scope | ACCEPT |
| 3003857 | Penalty NeuralODE chaotic dynamics | ML/Math | 7/7 | 2026-04-25 | v2_faithful trained; report: *"WeatherBench mirror could not be reached — ERA5 we did not obtain"* | **DATA-BLOCKED** on atmospheric demo, ACTUAL on KS/Lorenz | DEFER (ERA5) |
| 1461824 | Photo-z PDFs for Large Surveys | Astrophysics | 8/8 | 2026-04-19 | Stacked N(z), brightness-binned diagnostics, 4 figures | **ACTUAL** | ACCEPT |
| 1842593 | Motion Tomography (occupation kernels) | Signal | 8/8 | 2026-04-19 | 14 .py files, Algorithm 1 + Expt 1 + sensitivity sweeps, 10 figs | **ACTUAL** | ACCEPT |
| 1379592 | GraphBLAS Foundations | Graph Algo | 9/10 | 2026-04-19 | Definitional paper, fully implemented (5 .py + 4 figs) | **ACTUAL** | ACCEPT |
| 1997354 | Hausdorff Integer Sequences | Mathematics | 10/10 | 2026-04-25 | All 13 closed-forms verified; 327k graphs enumerated to K₄,₄/K₃,₆ | **ACTUAL** (pure math, fully verified) | ACCEPT |
| 1983793 | CPW resonator mask targeting | Quantum Devices | 8/8 | 2026-04-25 | v2.5: analytical + 2D FD + KI + GDS + 3D Palace eigenmode (4 MPI), all 8 designed lengths | **ACTUAL** | ACCEPT |
| 1475143 | FDTD 1+1D delay PDE | Numerical | 8/8 | 2026-04-25 | Figs 5–7 reproduced; Fig 8 noted out of reach | **COMPUTE-BOUND** but high coverage | ACCEPT |
| 2441075 | Light-scattering errors in trapped-ion qubits | Quantum | 8/9 | 2026-04-25 | Analytic Eqs 6-10 + 5-jump Lindblad ME + Ca-40 branching; Figs 1-4 reproduced (1D-chain J_ij approx vs 2D crystal) | **ACTUAL theory, COMPUTE-BOUND on 2D-crystal modes** | ACCEPT |
| 1624105 | Linclust (huge protein clustering) | Bioinformatics | 8/9 | 2026-04-26 | Algorithm reimpl + benchmarks. Report: *"did not rerun full UniRef/Metaclust benchmarks"* | **ACTUAL on algorithm, COMPUTE-BOUND on full corpus** | ACCEPT |
| 2439897 | Parsimonious rVAE | ML/Imaging | 8/9 | 2026-04-26 | Two SE(2)-equivariant impls run head-to-head with authors' atomai 0.8.1; 4 result files, 10 figs | **ACTUAL** | ACCEPT |
| 1861801 | NukeLM | NLP/Domain | (no master entry) 7-ish | 2026-04-25 | RoBERTa + SciBERT fine-tuning runs on ~30k OSTI abstracts (paper used ~1.5M); per-config `result.json`. Report: *"corpus 50× smaller; no hyperparameter grid"* | **COMPUTE-BOUND** — pipeline real but reduced corpus | DEEPEN (full corpus, ~7-10 days scrape) |
| 2582579 | NILC Cosmological Parameters | CMB/Cosmology | (no master eval entry) | 2026-04-24 | Authors' `pyilc` + `NILC-PS-Model`; 6 contributions to Eq.26; **<0.2% recovery** of ref power spectra at 2≤ℓ≤20 | **ACTUAL** — strong replication of headline | ACCEPT |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **PDE-replications/** | (10 sub-papers) | | | 2026-04-25 to 04-27 | | | |
| — | Gopal-Trefethen 2019 Lightning Laplace/Helmholtz (`lightning-laplace/`) | Numerical PDE | n/a | recent | Laplace fully reproduced; Helmholtz partial | **COMPUTE-BOUND** on Helmholtz | ACCEPT |
| — | Fortunato-Townsend 2017 Fast Poisson ADI (`fast-poisson-spectral/`) | Numerical PDE | n/a | recent | Spectral conv to 1.8e-14 by n=24, ADI vs direct crossover at n=1024, scaling to n=2048; cylindrical/3D not ported | **ACTUAL** | ACCEPT |
| — | Grossmann 2023 PINN-vs-FEM (`fem-vs-pinns/`) | PDE/ML | n/a | recent | 1D Poisson full sweep; 2D Poisson partial 5/11; 1D AC partial 1/14; 3D Poisson + Schrödinger skipped (missing GT) | **DATA-BLOCKED** on 3D & Schrödinger | DEFER for skipped problems |
| — | Kochkov 2021 jax-cfd (`jax-cfd/`) | PDE/ML | n/a | 2026-04-27 | LI(64) trained 20K steps + DNS at 64/128/256/1024; Re=4000/7000 + decaying turbulence missing | **COMPUTE-BOUND** | DEEPEN (~1 GPU-day) |
| — | Sawhney 2023 Walk-on-Stars (`walk-on-stars/`) | Grid-free MC | n/a | recent | Lens, square, L-shape; O(N^-1/2) confirmed; FEM comparison | **ACTUAL** | ACCEPT |
| — | Cao 2024 LNO Laplace Neural Op (`laplace-no/`) | PDE/ML | 8/7→8/8 | recent | 9/12 paper benchmarks; 3 skipped (Burgers/Brusselator/shallow-water — Google-Drive datasets unreachable from uicgpu) | **DATA-BLOCKED** on 3 benchmarks | DEFER |
| — | Xiong 2023 Koopman Neural Op (`koopman-no/`) | PDE/ML | 8/8 | recent | KNO + S=128→2048; Navier-Stokes long-horizon stability missing (needs FNO NS-2D dataset) | **COMPUTE-BOUND / DATA-BLOCKED** on headline | DEFER (NS-2D dataset) |
| — | Burns 2020 Dedalus (`dedalus/`) | PDE Spectral | 8/8 | recent | 6/8 demos: Poisson LBVP, RB-IVP, KH-IVP, clamped EVP, MPI scaling, disk EVP. Sphere/ball missing | **ACTUAL** | ACCEPT |
| — | Wu 2023 Latent Spectral Models (`latent-spectral-models/`) | PDE/ML | n/a | recent | LSM reimpl on uicgpu A100 80GB | **ACTUAL** (per scope) | ACCEPT |
| — | Xiao 2021 Kinetic.jl (`kinetic-jl/`) | Kinetic Theory | n/a | recent | Julia install + replication suite | **ACTUAL** (toolbox replication) | ACCEPT |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1565592 | Hempel MSM bias correction (real work in `msm-replication/` & `replicate-msm/`) | Mol Dynamics | 9/8 | 2026-04-19 | All 3 phases (1D well, 2D, ADP); paper's main claim confirmed (OOM corrects MSM bias) | **ACTUAL** | ACCEPT |
| 2217719-scale-msr (alias) | (duplicate of 2217719) | | | 2026-04-25 | xe_sensitivity.png, replication scripts | (see 2217719 above) | Consolidate dirs |
| `pde_candidates/` | meta — top-30 PDE corpus survey | meta | n/a | 2026-04-24 | `PDE_TOP30_DEEP_REPORT.pdf` (172 figs) | **N/A — selection corpus, not a replication** | ACCEPT (meta artifact) |
| `pde_corpus/` | empty (txt subdir) | meta | n/a | — | empty | **N/A — empty staging dir** | DROP |
| `drafts/` | `email_gnedin_croc.md` only | meta | n/a | 2026-04-25 | 1 file | **N/A — correspondence draft** | retain |
| `scoring/` | scoring ledger + tier-lift bookkeeping | meta | n/a | 2026-04-25 | `evaluations_all.jsonl`, 22 figs | **N/A — meta** | retain |
| `perovskite-Passivation-Molecules-AI-Discovery/` | duplicate plan stub of pvmol-gen | Materials/GenML | (see PVMol-Gen) | 2026-04-02 | README + paper PDF only | **PREP-ONLY (alias)** | merge into pvmol-gen-fajar2026 |
| `bayesopt-qhsri/` (alias) | (duplicate of 2571540) | Optimization | 7/7 | 2026-04-17 | `replication_report.md` + 5 figs + 5 data | (see 2571540) | Consolidate |
| `cpw-resonator/` (alias) | (duplicate of 1983793) | Quantum Dev | (see 1983793) | 2026-04-17 | `results_hires.json` | (see 1983793) | Consolidate |
| `fdtd-delay-pde/` (alias) | (duplicate of 1475143) | Numerical | (see 1475143) | 2026-04-16 | `replication_report.md` | (see 1475143) | Consolidate |
| `photoz-pdfs/` (alias) | (duplicate of 1461824) | Astrophysics | (see 1461824) | 2026-04-16 | `stacked_nz_faint.png` | (see 1461824) | Consolidate |
| `replicate-1559043-combustion/` | (v5 plan stub for 1559043) | CFD | (see 1559043) | 2026-04-24 | `v5_plan.md` only | **PREP-ONLY (v5 not yet executed)** | DEEPEN (run v5) |

---

## Top-5 Papers Most Worth DEEPENING
*Highest "score-gap that compute could close" — invest GPU-hours here for biggest paper-v5 honesty boost.*

| # | OSTI / Paper | Current | After DEEPEN | Cost estimate | Action |
|---|---|---|---|---|---|
| 1 | **1868518 Graph-RL Distribution Restoration** | 5/5 (SHALLOW — IEEE-33/123 only) | 7-8/10 if 8500-bus runs | ~24 GPU-h on uicgpu A100 | Run authors' GCN-DQN on IEEE 8500-node feeder; the architecture is in place |
| 2 | **1559043 Ignition Kernel v5** (PeleC) | 7/7 (COMPUTE-BOUND, 13/20 partial runs) | 9/10 with full 5ms + AMR | ~4 node-h Polaris (preemptable) | v5 plan is written and ready (`replicate-1559043-combustion/v5_plan.md`) |
| 3 | **1484740 2D GaN bilayer** (DFT) | 8/8 (bilayer not converged) | full bilayer band gap | ~1-2 days, 1 GPU | Continue SCF on partially-relaxed bilayer; report says "limited by compute time" |
| 4 | **2587225 ScaWL 3-WL + distributed** | 7/8 (single-node only) | 8-9/10 | MPI cluster run, ~few hundred CPU-h | Authors' code attempted; distributed harness needed |
| 5 | **1861801 NukeLM full corpus** | (no eval) | publishable replication | ~7-10 days OSTI scrape (rate-limited) + 1 GPU-day fine-tune | Pipeline works on 30k abstracts; just needs scale |

**Honorable mentions for DEEPEN:** 1864334 NN-VMC (3-body forces, ~1 GPU-week), 2475938 Virophage full IMG/VR (large), 2396968 Latent SDE (V100 6-week, probably too costly).

---

## Top-5 Papers That Should DROP (or DEFER indefinitely)
*Structurally unreplicable from this lab's resources, or where the master-README claim is materially misleading.*

| # | Paper | Reason | Action |
|---|---|---|---|
| 1 | **1275503 CROC Cosmic Reionization** | Paper IS the radiation-hydro CROC simulation; we only have a semi-analytic FGPA surrogate. Score 5/5 is honestly low but the directory is positioned as a CROC replication when it isn't. | **RELABEL** as "FGPA-surrogate analysis" or **DROP**; alternatively DEFER until DOE/NCSA CROC sim access |
| 2 | **2469515 PATRIC Supervised Genome Extraction** | Requires proprietary SEEDtk + 193k-genome BV-BRC reference DB; the paper's actual contribution is the supervised arm, which we cannot run. | **DEFER** with disclosure, or DROP from active set |
| 3 | **1609039 Cu64Zr36 metallic glass** | Master README says "Running 76%"; reality is plan-only, no LAMMPS run, no checkbox checked. Either run it (1-2 days LAMMPS on UIC) or remove. | **DROP** unless someone runs LAMMPS this week |
| 4 | **1984484 DRAS RL for Cluster Scheduling** | Plan-only stub; no scaffolding. RL-for-systems is replicable but nothing exists yet. | **DROP** or commit to PoC week |
| 5 | **1993311 Electronic specific heat** | Plan-only stub; trivially replicable in 1 day with QE/ABINIT but nobody has. | **DROP** or run in 1 day |

Plus **1578031 Joint emulation Earth System Model** (plan-only — could be a 6th DROP candidate).

---

## Recommendations for Paper Draft v5

1. **Acknowledge the depth distribution explicitly.** The current draft positions all entries as "complete." Honest framing: ~14 ACTUAL, ~11 COMPUTE-BOUND-but-honest, ~13 with material gaps disclosed in their own reports. State this in the abstract.

2. **Drop or relabel five PREP-ONLY/STALLED entries** (1578031, 1609039, 1984484, 1993311, perovskite-Passivation duplicate) before submission. Including them as "complete" is a misrepresentation risk.

3. **Distinguish "headline-reproduced" vs "method-implemented" replications** in the figure-of-merit table. 1275503 (FGPA surrogate, not CROC), 1868518 (small networks only, not 8500-bus), 2469515 (baseline, not PATRIC supervised), 2217719 (Bateman ODE, not SCALE/ORIGEN), and PVMol-Gen (no overlap with paper's Rep10) are method-implemented but headline-not-matched. They should not be averaged equally with full replications.

4. **Add a "limitations" subsection per replication** in the supplementary table — most of the per-paper reports already have these; surface them in the main draft.

5. **The 5 strongest replications worth highlighting as exemplars:**
   - **1997354** Hausdorff integer sequences (10/10, fully verified, 327k-graph enumeration)
   - **1379592** GraphBLAS Foundations (9-10/10, definitional paper fully implemented)
   - **2582579** NILC cosmological power spectra (<0.2% recovery on Eq.26)
   - **1842593** Motion Tomography occupation kernels (Algorithm 1 + Expt 1 + sensitivity sweeps)
   - **fast-poisson-spectral** (Fortunato-Townsend 2017: spectral convergence to 1.8e-14, ADI crossover and O(n²log²n) confirmed)

6. **Run v5 of 1559043 PeleC.** It is the cheapest single intervention that converts a 7/10 to a 9/10 honestly, and the v5 plan is already written. Same for the bilayer GaN SCF continuation.

7. **Reconcile master `README.md` with the per-paper reality** — particularly the "Running 76%" line for 1609039 (delete or replace with "plan-only"). Several "✅ Complete" entries should read "✅ Complete, partial-scale" with a footnote.

8. **Consolidate alias directories** before publishing: `bayesopt-qhsri/` ↔ `2571540-…`; `cpw-resonator/` ↔ `1983793-…`; `fdtd-delay-pde/` ↔ `1475143-…`; `photoz-pdfs/` ↔ `1461824-…`; `msm-replication/`/`replicate-msm/` ↔ `1565592-…`; `2217719-scale-msr/` ↔ `2217719-SCALE-…`; `pvmol-gen/`/`pvmol-gen-fajar2026/`/`perovskite-Passivation-Molecules-AI-Discovery/` → one canonical PVMol-Gen dir. Saves reviewers from confusion and cuts spurious "53 papers" inflation to a more honest **~46 distinct papers**.

---

*Audit method: file-tree inventory + size/timestamp scan + grep for "TODO/skipped/out of scope/partial/not implement/limitation" across all `report/*.tex` and `replication_report.md`, cross-referenced with `scoring/evaluations_all.jsonl` (latest record per OSTI ID). Specific files inspected: each per-paper README/replication_report; `analysis_results.json` (1275503); `all_results.json` + training_history (1868518); `v2_faithful/report/report.tex` (2396968 + 3003857); `tierlift_results.pkl` (3014512); ICTV phylogeny logs (2475938); v1-v4 PeleC reports (1559043); `evaluations_all.jsonl` (66 records, 35 unique OSTI/paper keys after dedup-by-latest).*
