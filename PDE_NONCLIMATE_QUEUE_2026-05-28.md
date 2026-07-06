# Non-climate PDE replication queue — proposed 2026-05-28

Rick asked to skip climate papers and pick 10 of the most interesting remaining PDE papers to replicate. This queue excludes the climate follow-up lane (Yuval/O'Gorman, Rasp, fldgen-style climate emulators) and avoids already-closed PDE replications where possible.

## Selection criteria
- Interesting scientific/computational content, not just easy score-padding.
- Non-climate PDE / numerical methods / scientific computing.
- Feasible with our current resources (CherryRd/uicgpu/Aurora/chiatta00), preferably public code or simple reimplementation.
- Good benchmark value for AI-agent reproducibility: clear claims, figures/tables, measurable metrics.
- Domain diversity: AMR, Poisson/elliptic, Helmholtz/DD, kinetic/plasma, bio-PDE, CFD/UQ, GR, electrochemistry, quantum PDE.

## Recommended 10

### 1. Deep Reinforcement Learning for Adaptive Mesh Refinement
- Source rank: PDE_100 #14, Priority A, 2022, JCP/arXiv.
- Why interesting: Direct AI+AMR problem; tests whether an RL policy actually beats classical refinement heuristics. Very relevant to adaptive simulation workflows.
- Replication path: Reimplement small 1D/2D AMR benchmark or recover authors' code if available; compare RL policy vs gradient/error-indicator AMR on advection/shock/Poisson-style tests.
- Effort: 8–12 h, GPU optional.
- Risk: Original repo may be missing/dead; fallback is independent PyTorch + toy AMR reimplementation.

### 2. FLUPS: A Fourier-Based Library of Unbounded Poisson Solvers
- Source rank: PDE_100 #18, Priority B, 2020, SIAM SISC.
- Why interesting: Core HPC numerical kernel with unbounded boundary conditions; complements our completed Fast Poisson spectral replication.
- Replication path: Build/run FLUPS examples; reproduce convergence and scaling on 2D/3D free-space Poisson; compare against FFT/direct baseline.
- Effort: 4–8 h CPU/MPI.
- Risk: Build/MPI friction; manageable.

### 3. Optimized Schwarz Methods without Overlap for the Helmholtz Equation
- Source rank: PDE_100 #30, Priority B, classic domain decomposition.
- Why interesting: Helmholtz + domain decomposition is hard and valuable; tests iterative convergence claims, not just pointwise solution accuracy.
- Replication path: Implement 1D/2D Helmholtz Schwarz with optimized transmission conditions; reproduce iteration-count vs frequency/subdomain claims.
- Effort: 5–8 h Python/FreeFem/FEniCS-style implementation.
- Risk: Older paper/theory-heavy, but small benchmark is feasible.

### 4. On the convergence of DG/Hermite spectral methods for the Vlasov–Poisson system
- Source rank: PDE_100 #20, Priority A, 2022, SIAM SINA.
- Why interesting: Kinetic/plasma PDE; bridges fusion/plasma and numerical analysis. Good diversity beyond fluids/neural operators.
- Replication path: 1D1V Vlasov–Poisson Landau damping / two-stream instability; verify conservation and convergence trends with Hermite/spectral truncation.
- Effort: 6–10 h CPU, maybe GPU if vectorized.
- Risk: No public code likely; but 1D1V implementation is tractable.

### 5. Comparison of Adaptive Multiresolution and Adaptive Mesh Refinement for Compressible Euler
- Source rank: PDE_100 #26, Priority B, 2015.
- Why interesting: Direct AMR-vs-MR comparison on shocks/compressible flow; useful alongside Deep-RL-AMR as the classical baseline story.
- Replication path: Use Clawpack/Python finite-volume Euler or existing AMROC/Carmen if buildable; reproduce L1 error/cell-count/time tradeoffs on Sod/Lax/shock-vortex style tests.
- Effort: 8–12 h.
- Risk: Original frameworks may be old; fallback independent FV implementation.

### 6. Gmunu: multigrid Einstein-field-equation solver for GR hydrodynamics simulations
- Source rank: PDE_100 #40, Priority B, 2020.
- Why interesting: GR hydrodynamics/numerical relativity; natural follow-on to HARMPI-GRMHD but with elliptic/multigrid GR solver flavor.
- Replication path: Build gmunu if possible; otherwise reproduce a documented TOV/star or spacetime test, checking constraint residuals/convergence.
- Effort: 10–16 h CPU/MPI.
- Risk: Heavier domain setup; high scientific payoff if it lands.

### 7. APBS biomolecular solvation / Poisson–Boltzmann suite improvements
- Source rank: PDE_100 #21, Priority B, 2017.
- Why interesting: PDE methods in molecular biophysics; high-impact, practical Poisson–Boltzmann solver, gives us a biology-facing PDE replication.
- Replication path: Run APBS canonical electrostatics examples; reproduce solvation energy/convergence for one or two proteins or analytic sphere tests.
- Effort: 4–8 h CPU.
- Risk: More software-suite replication than algorithm paper; still valuable if framed honestly.

### 8. Kernel-based active subspaces for CFD parametric problems using DG
- Source rank: PDE_100 #19, Priority B, 2020.
- Why interesting: UQ/reduced-order modeling for CFD; tests parametric surrogate + active-subspace claims instead of yet another solver benchmark.
- Replication path: Reimplement active-subspace regression on a small DG/CFD benchmark or use authors' ATHENA/HOPE workflow if recoverable; verify dimension reduction and prediction error.
- Effort: 6–10 h.
- Risk: Dependencies/code availability uncertain; fallback synthetic parametric PDE.

### 9. Modified Poisson–Nernst–Planck model with Coulomb and hard-sphere correlations
- Source rank: PDE_100 #29, Priority B, 2020.
- Why interesting: Electrochemistry/ion transport; a useful elliptic–parabolic coupled PDE outside fluid/climate.
- Replication path: Implement 1D/2D finite-difference PNP variants; reproduce concentration/potential profiles and correlation corrections vs classical PNP.
- Effort: 5–8 h Python/FEniCS.
- Risk: No code likely; equations are manageable.

### 10. Variational quantum algorithm for the Poisson equation / analog quantum simulation of PDEs
- Source ranks: PDE_100 #32/#39, Priority C/B, 2020–2023.
- Why interesting: Quantum algorithms for PDEs; high novelty and a good stress test for “replication” when the solver is quantum-inspired rather than production-HPC.
- Replication path: Statevector/Qiskit simulation for 1D Poisson/heat equation; reproduce residual/energy convergence vs ansatz depth; compare against classical solve.
- Effort: 4–8 h local CPU.
- Risk: Toy-scale only unless hardware access; that’s acceptable if reported honestly.

## Recommended execution order
1. FLUPS Poisson — fast, likely high confidence.
2. Deep RL AMR — highest AI+PDE interest.
3. Optimized Schwarz Helmholtz — classic DD/Helmholtz gap.
4. DG/Hermite Vlasov–Poisson — kinetic/plasma diversity.
5. APBS Poisson–Boltzmann — biology-facing PDE.
6. AMR vs Multiresolution Euler — classical adaptivity baseline.
7. Kernel active subspaces CFD — UQ/reduced-order angle.
8. Modified PNP — electrochemical transport.
9. Quantum Poisson/PDE — novelty / toy-scale benchmark.
10. Gmunu GR hydro — highest risk, high payoff; run after easier wins.

## Explicit exclusions from this queue
- Climate papers: Yuval/O'Gorman, Rasp, fldgen/ESM, climate parameterization/emulation.
- Already-closed PDE replications: FEM-vs-PINNs, jax-cfd, Latent Spectral Models, Koopman NO, LNO, Walk-on-Stars, Fast Poisson, Lightning Laplace, Dedalus, Kinetic.jl, Godunov loss, PINN-RANS, PINN-domain-decomp, stochastic Burgers, PWDG Helmholtz, lifex-cfd partial unless Rick wants a deepening pass.
