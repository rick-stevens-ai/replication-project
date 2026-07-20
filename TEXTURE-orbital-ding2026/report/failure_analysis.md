# Failure analysis — Ding et al. 2026 replication

## What was faithfully reproduced
- **Altermagnet symmetry (exact).** The d-wave (dx2-y2) momentum dependence,
  the Gamma-M diagonal nodes, the C4z sign reversal between Gamma-X and Gamma-Y,
  and full spin compensation (zero net moment) all emerge exactly from the
  symmetry-constrained hopping — these are structural, not fitted.
- **Order-of-magnitude splitting.** 720 meV vs claimed 620 meV (16% high),
  achievable with ordinary Fe-d hoppings (t~0.35 eV, m~0.9 eV).

## Where the replication is weaker than the paper (honest gaps)
1. **No DFT / no ground-state proof.** The paper's central *thermodynamic*
   claim — that hole doping drives a dimer->checkerboard transition making the
   altermagnet the ground state — is NOT tested here. We *impose* the
   checkerboard order. The paper itself flags that imposing the config does not
   prove it is the ground state; our surrogate inherits this limitation.
2. **Magnitude is parameter-tuned, not predicted.** The 620 meV scale is set by
   the ligand anisotropy `delta`, which we calibrated (0.26 -> 0.090 eV) to land
   near the claim. Without a Wannier downfold of real DFT bands, the absolute
   number is not an independent prediction — only its symmetry and scale are.
3. **No SOC physics.** The paper's SOC results (Neel-vector-dependent Weyl
   anti-crossings, easy-plane anisotropy, magnetic space groups Pm'm2'/Cm'm2')
   are entirely outside our spin-conserving model.
4. **No multilayer / bulk-limit test.** The 10-layer-slab robustness claim
   cannot be probed by a 2D monolayer TB.
5. **Coarse chemical-potential treatment.** Doping enters only via a rigid-band
   filling (1.5/4 per cell); no self-consistent charge redistribution.

## Failure modes encountered & fixes
- First run gave 1800 meV (delta=0.26 too large). Symmetry was already perfect,
  so we reduced delta to 0.090 eV to match the near-Fermi scale — a calibration,
  transparently logged, not a bug.
- No numerical instabilities; runtime 0.2 s.

## Net assessment
The *qualitative altermagnet physics* of the paper is robustly and
independently reproduced. The *quantitative 620 meV* and the *thermodynamic
ground-state* claims require DFT and are only partially supported here. Hence
**PARTIAL** rather than full REPLICATED.
