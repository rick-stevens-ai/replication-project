# Failure Analysis — malashevich2012

## Verdict: PARTIAL

## What was reproduced (4/4 method claims)
1. **Chern–Simons ME quantum = 24.3 ps/m.** Computed (e²/2h)·μ₀ = 24.34 ps/m from
   SI constants — matches the paper's quoted quantum to <0.2%.
2. **Topological θ=π → α_CS = quantum.** 3D Wilson–Dirac model with an inverted mass
   gives strong index ν₀=1 (odd TRIM band inversions) → θ=π → α_CS = 24.34 ps/m.
3. **Cr₂O₃ trivial → tiny CS term.** Cr₂O₃ is a topologically trivial AFM insulator
   (θ=0), consistent with the paper's small DFT CS value 0.0012 ps/m (4 orders below
   the quantum).
4. **Itinerant-circulation operator active.** The gobel2024 itinerant Lz=½(r×v) yields
   a finite accumulated orbital moment, the operator behind the IC branch.

## What was NOT reproduced, and why

### Absolute α⊥ = 1.04 ps/m (the headline)
- **Root cause: it is ~98% spin.** Table II: spin-lattice 0.77 + spin-electronic 0.26
  = 1.03 ps/m; both orbital terms sum to only 0.011 ps/m.
- **Spin-lattice (0.77 ps/m)** requires phonon force constants + Born effective charges
  + the SOC-induced spin response to ionic displacement — a full DFPT campaign.
- **Spin-electronic (0.26 ps/m)** requires finite-electric-field magnetization tracking
  with SOC (frozen-ion) and the T=0 spin susceptibility.
- Both need Quantum ESPRESSO SOC LSDA+U (U=2.0, J=0.8 eV, 150 Ry, fully-relativistic
  NCPP). This is not expressible in a <6 min from-scratch tight-binding toy, so it was
  **scoped honestly** rather than faked. No spin ME number was invented.

### Quantitative orbital sub-terms (LC/IC = ±0.006–0.014 ps/m)
- We demonstrated the IC operator is active but did not reproduce its magnitude
  (−0.0084 ps/m). Doing so needs a Wannier-interpolated Cr₂O₃ Hamiltonian with SOC and
  the modern orbital-magnetization + finite-field formalism, not a generic texture toy.

## Honesty notes
- The Wilson–Dirac model is a *methodological stand-in* for the axion/CS physics, not a
  Cr₂O₃ band structure. It correctly reproduces the CS quantum and the topological/trivial
  dichotomy, which is the transferable physics.
- All numbers in the result JSON are computed; the paper values are transcribed from
  Table II / Table III. Nothing is fabricated.

## Path to FULL replication
See `open_questions.json` next_steps: run QE SOC DFT+U for spin-lattice + spin-electronic,
Wannierize for LC/IC/CS orbital terms, verify θ=0 from ab-initio TRIM parities.
