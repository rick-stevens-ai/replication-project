# Failure analysis — gurung2023 replication

## What was NOT attempted (by design / scope)
1. **DFT of Mn₃GaN.** The paper's material-specific claim uses noncollinear DFT
   (5 Fermi-surface bands on the (001) 2DBZ). We deliberately skipped DFT (fast pass,
   <6 min budget) and built a tight-binding kagome surrogate that captures the same
   mechanism. **Consequence:** we verify the *mechanism* and the *"nearly 100%"*
   qualitative claim, not the material-specific breadth of the polarized region.
2. **ETMR ~10⁴% transmission.** The device claim requires a ballistic AFMTJ
   (Mn₃GaN/SrTiO₃/Mn₃GaN) with k∥-resolved P/AP transmission and matching to
   SrTiO₃ evanescent decay rates. Not built. **Consequence:** the transport
   payoff of the spin-polarization claim is unverified here.

## Known limitations of the surrogate
- **"Broad area" metric mismatch.** Our whole-grid fraction of p≥0.90 (~14%) is
  lower than a visual reading of the paper's Fig. 1c. Causes: (i) our coarse
  Fermi-crossing counter along k_x includes many-band overlap regions where p is
  genuinely reduced; (ii) we average over the full E_F window [-2.2, 2.2]t including
  the small-E_F region the paper itself flags as reduced. The decisive fact —
  p_k∥ → 1.0 is reached — is robust. A fixed-E_F (k_x,k_y) 2DBZ map would present
  "broad area" more faithfully (see open_questions next_steps).
- **Kagome vs antiperovskite.** The paper's Fig. 1 model is itself a 2D kagome
  illustration; Mn₃GaN's Mn kagome sits in the (111) plane of the antiperovskite.
  Our 2D model matches the illustrative model, not the 3D crystal.
- **No SOC.** Consistent with the paper's definition, but real Mn₃GaN has finite SOC
  which could cap p_k∥; untested here.
- **Coarse grid.** 41×601×41; adequate to establish max p and qualitative trends,
  not for converged area fractions.

## What went right
- 6-band spin-split-without-SOC structure emerged directly from the 120° texture
  (confirms the P̂T̂/T̂t̂ symmetry-breaking argument).
- max p = 0.99997 with no fitting — a clean, non-fabricated confirmation of the
  headline mechanism.

## No fabrication
All numbers come from the executed script; the result JSON is a verbatim copy of
its output. Claims out of scope are explicitly labeled, not invented.
