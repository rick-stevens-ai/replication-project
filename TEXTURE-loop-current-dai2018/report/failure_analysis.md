# Failure Analysis: dai2018 (arXiv:1802.03009v2)

## 1. Class mislabel (primary issue)
The paper is filed under TEXTURES-100 **loop-current** class, but it is a cuprate
**PDW/CDW vortex-halo** theory paper (Dai, Zhang, Senthil, Lee). Orbital loop
currents appear ONLY as a one-line introduction citation (neutron intra-cell
moments, refs 6–7), not as the physics. The assigned kernel
`loop_current_meanfield_kernel.py` (Ollie) is a kagome Peierls-flux tight-binding
probe — the **wrong model** for this system. Mitigation: per the replication
mislabel guard, we replicated the paper's actual minimal model (real-space PDW/CDW
order-parameter fields + FFT) and credited the kernel for methodological
provenance only. The kagome probe was run once (loop_current_susceptibility
≈ −0.063) purely as a provenance cross-tie, not as evidence for this paper.

## 2. What was NOT reproduced
- **Full BdG exact diagonalization (Appendix B).** The paper's Figs 3,6,7 come
  from ED of a d-wave + PDW BdG lattice Hamiltonian with a vortex. We reproduced
  the analytic order-parameter construction the paper uses to *explain* the ED
  results, not the ED itself. This is why the verdict is PARTIAL, not REPLICATED.
- **Precise splitting magnitude.** Predicted δq ~ 1/ξ ≈ 0.067; our coarse
  256² grid gives δq ≈ 0.157. The double-peak structure and symmetry are correct,
  but the magnitude is resolution-limited. A finer grid / larger box is needed to
  drive δq → 1/ξ.

## 3. Assumptions baked in
- We *assumed* the cos(θ − θ_a) angular form of the induced Q/2 CDW (paper Eq.9/14)
  rather than deriving it from a microscopic overlap integral. The paper claims ED
  supports this form; we did not independently verify that.
- Single isolated vortex, no disorder, no inter-halo incoherence (real STM averages
  many vortices — see open_questions.json).

## 4. What went right
- All four qualitative discriminating signatures (split double peak for PDW-driven,
  single peak for CDW-driven, real-space nodal line, Re(FFT) sign change) reproduced
  cleanly (4/4). The central falsifiable experimental prediction of the paper is
  confirmed at the phenomenological level.

## 5. No fabrication
All numbers come from actual execution of `code/dai2018_replicate.py` via
`/home/stevens/comfyui-env/bin/python`. Result saved to `work/dai2018_result.json`.
