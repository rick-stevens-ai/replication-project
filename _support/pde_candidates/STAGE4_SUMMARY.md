# Stage 4 Summary — PDE 100 Deep-Read & Reproduction Plan

## Deliverables
- `pdfs/` — 70 PDFs successfully downloaded (of 100 targets)
- `pdf_text/` — 70 extracted text files (first 30 pages each via pdftotext -layout)
- `deep_read_results.jsonl` — 100 entries with reproducibility/interest scores, topic, reproduction plan, priority
- `PDE_100_FINAL_RANKED.{md,json}` — final domain-balanced ranked list
- `PDE_100_REPORT.pdf` — master LaTeX report (top-10 summaries, full table, priority lists, appendix)

## PDF Fetch Success Rate
- Downloaded: 70/100
- Abstract-only fallback: 30/100
- Most failures = publisher paywall (JDE, AMS, Hindawi, MDPI variants) returning 403/HTML instead of PDF
- Tried arxiv fallback for papers with arxiv IDs — recovered 7

## Priority Distribution
- **A (ready-to-go):** 14
- **B (needs minor work):** 45
- **C (hard):** 41

## Topic Bucket Distribution (after domain caps)
- Fluid/NavierStokes: 24
- Elliptic: 17
- NonlinearScalar: 14
- ML-operator/PINN: 9
- Heat/Diffusion: 9
- Helmholtz/Wave: 5
- Hyperbolic: 4
- Stochastic: 4
- Quantum/Kinetic: 4
- PhaseField/RD: 3
- AMR/Multigrid: 2
- Relativity/GR: 1
- Fractional: 1
- Other: 1
- FreeBoundary: 1
- Porous/Darcy: 1

## Caps Applied
- Elliptic: target 15, overflow allowed to 17 (limited ML-operator availability)
- Fluid/Navier-Stokes: target 20, overflow to 24 (dominant genre in corpus)
- ML-operator/PINN: reserve 15, actual 9 (corpus has fewer than anticipated)
- Stochastic PDEs: max 10, actual 4

## Top-20 Final Ranked
  1. [19] **A** — *ML-operator/PINN* — Can physics-informed neural networks beat the finite element method? (2023, 188 cites)
  2. [18] **A** — *ML-operator/PINN* — Solving High-Dimensional PDEs with Latent Spectral Models (2023, 95 cites)
  3. [18] **A** — *ML-operator/PINN* — Koopman neural operator as a mesh-free solver of non-linear partial differential equa (2023, 74 cites)
  4. [18] **A** — *Fluid/NavierStokes* — Lifex-cfd: an Open-source Computational Fluid Dynamics Solver for Cardiovascular Appl (2023, 61 cites)
  5. [18] **A** — *ML-operator/PINN* — Enhancing training of physics-informed neural networks using domain-decomposition bas (2023, 28 cites)
  6. [17] **A** — *ML-operator/PINN* — Machine learning–accelerated computational fluid dynamics (2021, 1123 cites)
  7. [16] **B** — *Fluid/NavierStokes* — Dedalus: A flexible framework for numerical simulations with spectral methods (2019, 485 cites)
  8. [16] **A** — *Fluid/NavierStokes* — Physics-informed neural networks for solving Reynolds-averaged Navier-Stokes equation (2021, 404 cites)
  9. [16] **A** — *ML-operator/PINN* — Learning in Modal Space: Solving Time-Dependent Stochastic PDEs Using Physics-Informe (2019, 274 cites)
 10. [16] **A** — *Elliptic* — Poisson Flow Generative Models (2022, 115 cites)
 11. [16] **A** — *ML-operator/PINN* — LNO: Laplace Neural Operator for Solving Differential Equations (2023, 56 cites)
 12. [16] **A** — *Elliptic* — Walk on Stars: A Grid-Free Monte Carlo Method for PDEs with Neumann Boundary Conditio (2023, 48 cites)
 13. [16] **B** — *Elliptic* — Fast Poisson solvers for spectral methods (2017, 47 cites)
 14. [16] **A** — *AMR/Multigrid* — Deep Reinforcement Learning for Adaptive Mesh Refinement (2022, 35 cites)
 15. [16] **A** — *Hyperbolic* — Godunov loss functions for modelling of hyperbolic conservation laws (2024, 5 cites)
 16. [15] **B** — *Helmholtz/Wave* — Plane Wave Discontinuous Galerkin Methods for the 2D Helmholtz Equation: Analysis of  (2011, 199 cites)
 17. [15] **B** — *NonlinearScalar* — Galerkin Approximations for the Stochastic Burgers Equation (2013, 105 cites)
 18. [15] **B** — *Elliptic* — FLUPS: A Fourier-Based Library of Unbounded Poisson Solvers (2020, 18 cites)
 19. [15] **B** — *Hyperbolic* — Kernel‐based active subspaces with application to computational fluid dynamics parame (2020, 15 cites)
 20. [15] **A** — *Elliptic* — On the convergence of discontinuous Galerkin/Hermite spectral methods for the Vlasov- (2022, 6 cites)

## Scoring Methodology Notes
- Reproducibility (1-10): signal-based — full-PDF availability, GitHub/Zenodo/code mention, concrete
  numerical methods (FEM/FVM/FDM/DG/spectral/PINN), open-source tool compatibility, test problems,
  convergence/error tables, benchmarks. Pure-theory / existence papers penalized.
- Interest (1-10): citation count, recency, methodological novelty, ML/QC bonus, venue prestige,
  benchmark utility for AI agents.
- Final score = reproducibility + interest (max 20).
- Topic classification: title → abstract → full-text signals (in that priority order) to avoid
  misclassifying papers that merely mention "Navier-Stokes" in the intro.

## Obstacles & Observations
1. **PDF paywall wall:** 30 papers (esp. legacy journal of differential equations, AMS journals,
   Asme, some MDPI variants) returned HTML landing pages despite OA URLs from S2. Full deep-read
   had to use abstracts + S2 metadata for these. Scoring adjusted (-1 repro base for abstract-only).
2. **Topic over-matching:** Initial topic classifier over-assigned "Fluid/Navier-Stokes" because many
   PDE papers cite Navier-Stokes in intro for motivation. Fixed by prioritizing title matches.
3. **PINN/Neural-operator papers are unusually high-scoring:** 9/14 Priority A are ML-PDE works
   (PINN, neural operators, latent spectral models). These have strong repro signals (GitHub, JAX/PyTorch,
   concrete test problems like Darcy, Navier-Stokes benchmarks). Good for AI agent benchmarks but
   risk of homogeneity — mitigated by domain caps (max 15 ML, ended up 9).
4. **Elliptic papers over-represented:** Many "Poisson-solver" papers survived from Stage 1 due to
   topic seeding. Cap of 15 was hit but one Fourier-based solver paper (#18 FLUPS) is genuinely valuable.
5. **Relativity/GR, free-boundary, fractional:** Each has 1 paper; interesting diversity but heavy
   machinery makes them hard (Priority C likely despite decent scores).

## Recommended First Targets
Begin with Priority A papers that have GitHub code repos + concrete benchmarks:
- #1 Grossmann et al. "Can PINNs beat FEM?" — direct benchmark against deal.II/FEniCS on Poisson/heat/NS
- #4 lifex-cfd (ArXiv 2304.12032) — open-source cardiovascular CFD solver, benchmarks available
- #6 Kochkov et al. "ML-accelerated CFD" (PNAS) — Google; code+data, decaying turbulence benchmark
- #14 Deep RL for AMR — concrete benchmark against deal.II AMR
- #12 Walk-on-Stars (Sawhney) — reference impl exists, Monte Carlo PDE baseline

## Followups / Stage 5 Candidates
- Deep-read top-30 papers with pdf tool individually to sharpen reproduction plans (not done here
  due to sub-agent compute budget; signal-based scoring used instead)
- Attempt programmatic replication of top-5 Priority A papers with actual AI agent runs
- Backfill the 30 missing PDFs by requesting preprints via author pages / institutional repositories
- Check for Zenodo-hosted companion datasets for any paper with `has_benchmark=True`