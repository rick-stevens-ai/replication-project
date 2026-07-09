# Koneru et al. 2026 — Hierarchical RL of a Short-Range Bond-Order Potential for Silica

**Authors**: Aditya Koneru, Henry Chan, Valeria Molinero, Subramanian K. R. S. Sankaranarayanan
**Affiliations**: UIC (Mech+Ind Eng), Argonne (CNM), Utah (Chemistry)
**Journal**: *Journal of Chemical Theory and Computation*, 2026 (accepted May 2026)
**DOI**: 10.1021/acs.jctc.5c01885 · **OSTI ID**: 3363025
**Corresponding**: valeria.molinero@utah.edu, skrssank@uic.edu

## Abstract

Reinforcement learning (RL) parameterizes short-range interatomic potentials data-efficiently. This work extends the prior RL-pairwise silica optimization to a bond-order (Tersoff-type) potential with an analytic three-body term. A hierarchical RL workflow combining continuous-action Monte Carlo Tree Search and property-based rewards explores the 26-D parameter space, sequentially optimizing lattice, densities, angles, and cohesive energies of 21 silica polymorphs. Two models are produced: Q-Tersoff and ML-Tersoff. Both reproduce energetic ordering of low-energy phases and capture amorphous structure factors better than pairwise force fields while remaining orders of magnitude faster than high-D MLIPs. Both underperform on elastic constants and high-energy frameworks.

## Sections (as in PDF)
1. Introduction
2. Methods — Tersoff form, dataset, LAMMPS settings, learning algorithm, hierarchical rewards
3. Results and Discussion
4. Conclusion
5. Acknowledgements / SI / Data / Code / Author contributions / References

## Central equations

**Tersoff energy** (Eq. 1): $V = \tfrac{1}{2} \sum_i \sum_{j\neq i} f_c(r)_{ij} [f_R(r)_{ij} + b_{ij} f_A(r)_{ij}]$

**Cutoff** (Eq. 2): piecewise cosine at radius R with smoothing width D.
**Repulsive/Attractive** (Eq. 3-4): $f_R(r) = A e^{-\lambda_1 r}$, $f_A(r) = -B e^{-\lambda_2 r}$.
**Bond-order** (Eq. 5): $b_{ij} = (1 + \beta^n \zeta^n_{ij})^{-1/(2n)}$.
**ζ term** (Eq. 6): $\zeta_{ij} = \sum_{k \ne i,j} f_c(r_{ik}) g_{ik}(\theta_{ik}) e^{\lambda_3 (r_{ij}-r_{ik})}$.
**Angular** (Eq. 7): $g(\theta) = \gamma (1 + c^2/d^2 - c^2/(d^2 + (\cos\theta - \cos\theta_0)^2))$.
**UCB (RL)** (Eq. 8): $UCB(\theta_j) = \sum_{\mathrm{Hstage}} -\min(r_1,\ldots,r_{n_i}) + c \cdot f(\theta_j) \cdot \sqrt{\ln N_i / n_i}$.

## Methods details

- Dataset: 21 silica polymorphs from IZA + Navrotsky thermochemistry (ref 36).
- LAMMPS package for all MD/minimization.
- Conjugate-gradient minimization, tol 1e-6 eV, 1e-6 eV/Å.
- 3×3×3 replicated unit cell, 1 fs timestep, 1 bar pressure.
- Training equilibration: 300 K, 10 ps NVE.
- Elastic constants: finite positive/negative deformation.
- Amorphous S(q): heat β-cristobalite (4000 SiO2) 300→2500 K with ML-BKS over 1 ns; quench to 300 K; 3 ns equilibration with Tersoff; last 1 ns for S(q).
- Latin hypercube sampling of 12 initial parameter sets; exploration constant c=29; MCTS 4 stages, depth 7 levels, 4 child nodes per expansion, 5 simulations per node.
- Hierarchical reward thresholds (Fig 1d): density <10%, angle <10%, energetics <3%, lattice <3%.

## Table 1 — Tersoff parameters (see PDF page 6)

Full 26-dimensional parameter set for Si-Si (retained from Manna et al. 2022, ref 37), O-O, Si-O for both Q-Tersoff and ML-Tersoff. Reproduced verbatim in `paper.txt` lines 355-373.

## Key numerical results

- Cohesive energy ordering: ML-Tersoff most deviations ≤ 50 meV/atom; largest deviations in FAU, MEI, BEA (overestimates stability).
- **α-quartz Q-Tersoff**: density err ~0%, Si-O-Si err 1.7°, O-Si-O err 0.3°, cohesive-energy err ~0 (reference phase).
- **α-quartz ML-Tersoff**: density err 9.2%, Si-O-Si err 7.0°, O-Si-O err 0.4°.
- **Elastic constants (Fig 5)**: ML-Tersoff C11=701.8%, C33=411.7%, C44=66.6%, C66=539.9%, C12=6012.8%, C13=1918.5%, C14=100.0% error (all vs experiment). Q-Tersoff similarly bad.
- Timing: Tersoff models "at least two orders of magnitude faster" than GAP.

## Data + code availability

- **IZA database**: http://www.iza-structure.org/databases/ (all training structures)
- **BLAST framework** (c-MCTS + HMRRL): only through DOE user program submission (https://cnm.anl.gov/pages/register-to-become-a-cnm-user)
- **Force-field files + LAMMPS example**: https://github.com/miscquanta/HMRRL-tersoff-silica.git (ONLY α-quartz seed + potentials + one input file)

## References of note (for replication)

- Ref 23: BKS force field (van Beest 1990)
- Ref 24: Soules 1990
- Ref 25: GAP silica (Erhard, Deringer 2022)
- Ref 27: Tersoff formalism (Tersoff 1988)
- Ref 29: ML-BKS (Koneru 2023)
- Ref 31: Munetoh Tersoff for Si-O (2007)
- Ref 36: Navrotsky thermochemistry review (2009)
- Ref 37: Manna 2022 Nat. Commun. — source of the c-MCTS + retained Si-Si Tersoff params
- Ref 38: Baerlocher & McCusker IZA database
