# Replication: Markov State Models from Short Non-Equilibrium Simulations

**Paper:** Nüske et al., J. Chem. Phys. 146, 094104 (2017)
**OSTI ID:** 1565592
**arXiv:** 1701.01665

## What This Paper Does

Analyzes the estimation bias when building Markov State Models (MSMs) from short,
non-equilibrium molecular dynamics trajectories. Derives analytical expressions for
the bias and proposes an Observable Operator Model (OOM)-based correction method.

## Key Results to Reproduce

1. **Bias analysis on 1D double-well** (7-state discretization, 100 microstates)
   - Implied timescale plots: direct MSM vs OOM-corrected vs reference
   - Stationary probability estimates
   - Two data sets: K=250 (short) and K=2000 (long), Q=5000 each

2. **Alanine dipeptide MD** (40 k-means states, φ/ψ dihedral space)
   - 11,388 trajectories × 20 ps each (non-equilibrium starts)
   - Corrected vs uncorrected implied timescales (t2≈1400ps, t3≈70ps)
   - Stationary probability correction at τ≥500fs

3. **2D potential** (40×40 microstates, 16 MSM states)
   - Poor discretization stress test
   - t2≈144,000, t3≈17,000 steps
   - K=5000, Q=2000 and Q=10,000

## Pipeline

- Phase 1: Synthetic 1D double-well system (Figs 1, 3, 5)
- Phase 2: OOM estimator implementation
- Phase 3: Alanine dipeptide (Fig 6)
- Phase 4: 2D potential stress test (Fig 7)

## Tools

PyEMMA, deeptime, NumPy, SciPy, Matplotlib, MDTraj, OpenMM, scikit-learn
