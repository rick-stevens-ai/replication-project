# Open-artifact non-climate PDE/scientific-computing candidates

Date: 2026-05-28 12:08 CDT

Rick asked: "I want you to find more papers with open data and open source codes."

## Ground rules
- Exclude climate papers.
- Prefer papers with live public repo + license + examples/open/generated data.
- Avoid already-completed/launched targets when possible.
- Mark software-framework papers honestly; they are often open and reproducible, but the replication target is examples/benchmarks rather than a single physical result.

## Best next candidates

### 1. PDEBench — An Extensive Benchmark for Scientific Machine Learning
- Paper: NeurIPS 2022 Datasets & Benchmarks.
- Repo: `pdebench/PDEBench`.
- Data: DaRUS dataset, DOI 10.18419/darus-2986; generated PDE datasets including advection, Burgers, diffusion-reaction, shallow-water, Navier-Stokes-style tasks.
- Openness: public repo + public benchmark data; license needs direct inspection because GitHub API reported NOASSERTION.
- Why good: Very strong open-data target; benchmark suite can validate data generation + baseline model claims.
- Replication path: download or generate small subset; run baseline FNO/UNet/PINN on 1D Burgers/advection; compare reported error scale.
- Effort: 4–8h for small subset; more for full suite.

### 2. Fourier Neural Operator / NeuralOperator library
- Paper: Li et al., Fourier Neural Operator for Parametric PDEs / NeuralOperator library papers.
- Repo: `neuraloperator/neuraloperator` (MIT) and historical FNO code.
- Data: public/generated Darcy, Burgers, Navier-Stokes datasets; some dataset downloads are standard in examples.
- Openness: MIT repo, active.
- Why good: Original neural-operator baseline; we have replicated LNO/Koopman/LSM but not the original FNO paper itself as a standalone.
- Replication path: run one official example (Burgers or Darcy) and compare relative L2 / resolution generalization.
- Effort: 4–8h GPU.

### 3. WaveTrain / scikit_tt tensor-train quantum dynamics
- Paper: WaveTrain: Python package for numerical quantum mechanics of chain-like systems based on tensor trains (JCP 2023-ish local corpus rank #44).
- Repo: `PGelss/scikit_tt` and associated WaveTrain materials; local PDF references Zenodo DOI 10.5281/zenodo.7354077.
- Data: examples/generated chain Hamiltonians; Zenodo artifact.
- Openness: open repo signal in local corpus; license to verify live before launch.
- Why good: PDE-adjacent Schrödinger/tensor-train propagation; complements VQAPoisson with classical tensor methods.
- Replication path: run one chain dynamics example; compare energy/norm conservation and tensor-rank behavior.
- Effort: 3–6h CPU.

### 4. NodePy / RK-Opt — analysis of numerical time integrators
- Paper: NodePy package paper / RK-Opt linked in local PDE corpus rank #57.
- Repo: `ketch/nodepy` / `ketch/RK-Opt`.
- Data: generated stability regions/order-condition examples.
- Openness: open-source package likely BSD/MIT style; verify before launch.
- Why good: Core time-stepping infrastructure for PDE solvers; useful to replicate stability-region/order claims.
- Caveat: ODE/time-integrator framework rather than PDE application paper.
- Effort: 2–4h CPU.

### 5. FiPy — A finite-volume PDE solver using Python
- Paper/software: NIST FiPy finite-volume PDE framework.
- Repo: `usnistgov/fipy`.
- Data: examples generated analytically; materials/phase-field examples.
- Openness: NIST open-source project; verify license/repo state before launch.
- Why good: Mature open PDE package; can replicate canonical diffusion/Cahn-Hilliard/electrochem examples.
- Effort: 3–6h CPU.

### 6. PyClaw / Clawpack hyperbolic PDE ecosystem
- Paper: PyClaw / Clawpack open-source ecosystem papers for hyperbolic PDEs.
- Repo: `clawpack/pyclaw` / `clawpack/clawpack`.
- Data: generated Riemann/shallow-water/acoustics examples.
- Openness: public repo; license to verify.
- Why good: Hyperbolic conservation-law solver, useful complement to AMR/MR Euler and Godunov-loss results.
- Effort: 3–6h CPU.

### 7. MFEM — Modular finite element methods library
- Paper: MFEM library paper / high-order finite element applications.
- Repo: `mfem/mfem`.
- Data: bundled examples/meshes; generated PDE problems.
- Openness: public repo; license to verify (commonly LGPL/BSD-like but check).
- Why good: Strong open FEM library; many reproducible examples, AMR, high-order, GPU backends.
- Effort: 4–8h CPU/GPU depending example.

### 8. deal.II — finite element library examples/benchmarks
- Paper: deal.II library papers / step examples.
- Repo: `dealii/dealii`.
- Data: generated examples; open meshes.
- Openness: public repo, open-source; license to verify.
- Why good: Gold-standard FEM framework; could replicate one benchmark or tutorial convergence table.
- Effort: 4–8h CPU, but builds can be heavy.

### 9. Nektar++ — spectral/hp element framework
- Paper: Nektar++ open-source spectral/hp element framework.
- Repo: `Nektar/nektar` or current `Nektar++` organization (verify exact repo).
- Data: bundled examples/benchmarks.
- Openness: public open-source framework; verify live repo/license.
- Why good: Spectral/hp methods complement Dedalus and PWDG Helmholtz.
- Effort: 6–10h, build risk moderate.

### 10. FEST-3D — finite-volume explicit structured 3D solver
- Paper: JOSS paper, "FEST-3D: Finite-volume Explicit STructured 3-Dimensional solver".
- Repo: likely `FEST3D/FEST-3D` (verify exact capitalization/live repo).
- Data: generated CFD test cases.
- Openness: JOSS implies open-source repo/license; verify before launch.
- Why good: Traditional CFD finite-volume code with paper+repo; could run canonical compressible-flow examples.
- Effort: 4–8h CPU/MPI.

### 11. ExaHyPE / ExaHyPE Engine
- Paper: ExaHyPE engine for hyperbolic PDEs / dynamically adaptive simulations.
- Repo: `ExaHyPE-Engine/ExaHyPE-Engine` or successor; verify live status.
- Data: generated wave/Euler/GR examples.
- Openness: public repo historically; verify before launch.
- Why good: High-performance hyperbolic PDE engine; relevant to AMR, GR, wave problems.
- Effort: 8–12h; build risk high.

### 12. preCICE — open-source multiphysics coupling
- Paper/software: preCICE coupling library.
- Repo: `precice/precice`.
- Data: examples/tutorials; FSI/conjugate heat transfer generated cases.
- Openness: open-source, public tutorials.
- Why good: Multiphysics PDE coupling rather than solver; useful but adjacent.
- Effort: 4–8h.

## Prioritization recommendation

If launching another wave, use this order:
1. PDEBench — best open data+code target.
2. NeuralOperator/FNO — high-value ML-PDE baseline not yet standalone replicated.
3. FiPy — mature open finite-volume PDE solver.
4. PyClaw/Clawpack — hyperbolic PDE solver, complements Euler/AMR work.
5. WaveTrain/scikit_tt — tensor-train Schrödinger dynamics, good diversity.

Then, if we want heavier framework builds:
6. MFEM
7. deal.II
8. Nektar++
9. FEST-3D
10. ExaHyPE

## Verification status
- Live web search confirmed PDEBench repo/data references and DaRUS dataset.
- GitHub API confirmed `pdebench/PDEBench` active but license as NOASSERTION — inspect before launch.
- GitHub API confirmed `neuraloperator/neuraloperator` active, MIT, examples present.
- Local corpus confirmed WaveTrain/scikit_tt with Zenodo link.
- API rate limit hit before checking FiPy/PyClaw/MFEM/deal.II/FEST/Nektar/ExaHyPE; these need one live license/repo check before launch.
