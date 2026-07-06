# Openness audit — non-climate PDE queue

Date: 2026-05-28 09:40 CDT

Question: do the 10 proposed non-climate PDE papers use open data and open-source programs?

## Summary

Strict standard: public paper/preprint + open-source code or clearly open-source dependencies + no closed/proprietary data required.

- PASS / keep: 5
- CONDITIONAL / keep only as independent open-source reimplementation: 3
- SWAP / demote if strict open-code requirement: 2

Numerical PDE papers often use analytic/manufactured test data rather than external datasets. I treat that as OPEN DATA when initial/boundary conditions are fully specified in the paper and can be regenerated.

## Per-paper audit

| # | Candidate | Open data? | Open-source program/code? | Verdict | Notes |
|---|---|---|---|---|
| 1 | FLUPS unbounded Poisson solvers | Yes — synthetic Poisson tests / examples | Yes — `vortexlab-uclouvain/flups`, BSD-3-clause stated in README/LICENSE | PASS | Strongest clean open target. GitHub active; examples/samples present. |
| 2 | Deep RL for Adaptive Mesh Refinement (Foucart et al.) | Yes — PDE-generated training, no fixed proprietary data | Original paper: no public code found. Related open LLNL `marl-amr` exists, BSD-3, with MFEM/PyMFEM and pretrained checkpoint, but it is a different AAMAS paper | CONDITIONAL / SWAP | If strict same-paper artifact openness is required, swap to LLNL MARL-AMR. If we allow independent implementation, keep Foucart as conceptual target. |
| 3 | Optimized Schwarz Helmholtz | Yes — manufactured Helmholtz benchmarks | No original code found; paper/preprint openly available | CONDITIONAL | Acceptable only as independent Python/FEniCS/FreeFem implementation. No proprietary data. |
| 4 | DG/Hermite Vlasov–Poisson | Yes — analytic VP test initial conditions | No original code found; arXiv open | CONDITIONAL | Good independent implementation target; no closed data. |
| 5 | AMR vs Multiresolution Euler | Yes — benchmark ICs specified | Yes-ish — Carmen open access repo `waveletApplications/carmen`; AMROC open access at vtf website. GitHub repo has no detected license file | PASS with license caution | Open code exists; verify license before redistribution. We can run, but avoid copying code into our repo until license is clear. |
| 6 | Gmunu GR hydro | Yes — code tests/standard GRHD setups | Paper says open-source code Gmunu, but I could not find a live public repo/API match | SWAP/DEMOTE | Too brittle until repo is found. Keep as high-interest watch item, not launch target. |
| 7 | APBS Poisson–Boltzmann | Yes — examples + public PDB/PQR-style data | Yes — `Electrostatics/apbs`, APBS open source; examples/tests present; BSD-like/PNNL license file | PASS | Clean open-source target, though more software-suite than single-paper algorithm. |
| 8 | Kernel active subspaces CFD/DG | Yes — datasets referenced openly (`paulcon/as-data-sets`) and generated CFD samples | Yes — ATHENA is MIT; HopeFOAM is GPL-3; OpenFOAM open source | PASS | Good open target, but HopFOAM dependency may be heavier. |
| 9 | Modified Poisson–Nernst–Planck hard-sphere correlations | Mostly yes — equations/ICs + referenced MC data from a free database | No original code found | CONDITIONAL | Feasible open-source reimplementation in Python/FEniCS, but not same-paper open artifact. |
| 10 | Quantum Poisson / VQA Poisson | Yes — toy Poisson instances generated analytically | Yes if selecting Sato et al. minimum-potential-energy VQA: `ToyotaCRDL/VQAPoisson`, Apache-2.0 | PASS | Prefer the ToyotaCRDL VQAPoisson paper over the no-code Liu et al. variant. |

## Recommended adjusted queue if strict openness is required

1. FLUPS unbounded Poisson solvers — PASS
2. APBS Poisson–Boltzmann — PASS
3. Kernel active subspaces CFD/DG — PASS
4. Quantum Poisson via ToyotaCRDL `VQAPoisson` — PASS
5. AMR vs Multiresolution Euler via Carmen/AMROC — PASS with license caution
6. LLNL MARL-AMR — PASS, but note it replaces Foucart Deep-RL-AMR with a closely related open-code AAMAS paper
7. Optimized Schwarz Helmholtz — CONDITIONAL independent implementation
8. DG/Hermite Vlasov–Poisson — CONDITIONAL independent implementation
9. Modified Poisson–Nernst–Planck — CONDITIONAL independent implementation
10. Replacement for Gmunu needed unless repo is found

## Suggested replacement for Gmunu

Replace Gmunu with one of:

- **Variational quantum algorithm based on minimum potential energy for Poisson** — already in quantum slot if we choose it, Apache-2.0 code.
- **Low-rank projector-splitting integrator for Vlasov–Poisson** — no code found, but analytically specified and reimplementation-friendly.
- **FLUPS companion TPDS FFT library paper** — same open repo, very clean but less domain-diverse.
- **APBS/PDB2PQR companion example** — clean open stack, but maybe too software-suite-heavy.

My recommendation: **swap Gmunu out for LLNL MARL-AMR**, and treat Foucart Deep-RL-AMR as background motivation, unless Rick specifically wants GR hydro despite repo uncertainty.

## Evidence checked
- Local PDE metadata: `pde_candidates/PDE_100_FINAL_RANKED.json` and extracted PDF text.
- Live GitHub API / raw license checks:
  - `vortexlab-uclouvain/flups`: active, README states BSD-3-clause, license file present.
  - `Electrostatics/apbs`: active, license/copying files, examples/tests present.
  - `llnl/marl-amr`: active, BSD-3-Clause, README includes train/eval commands and pretrained checkpoint path.
  - `ToyotaCRDL/VQAPoisson`: active, Apache-2.0.
  - `HopeFOAM/HopeFOAM`: active, GPL-3.0.
  - `mathLab/ATHENA`: active, MIT.
  - `waveletApplications/carmen`: live repo, no license detected by GitHub API.
- Local PDF text showed:
  - AMR/MR paper explicitly cites Carmen GitHub and AMROC open access.
  - Kernel-active-subspace paper cites HopeFOAM, OpenFOAM, ATHENA package, and `paulcon/as-data-sets`.
  - Gmunu paper says “open-source code Gmunu,” but no live repo found in quick checks.
