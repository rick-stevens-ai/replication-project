# Failure Analysis — What was NOT reproduced and why

**Verdict: REPLICATED** (tight-binding scope). The gaps below are scoping
decisions, not physics failures; they cap Coverage at 7/10.

## Deliberately out of scope
1. **DFT of monolayer Mg₂Mo₂(PO₅)₂.** The paper's material claim (Fig. 2(f),
   S2) rests on a magnetic (Néel, out-of-plane, μ≈1.6 μ_B) DFT band structure
   with Mo t2g projection. Task explicitly says skip DFT. Consequence: we
   verified the *mechanism* (TB model) but not the *material realization*.
2. **Layer degree of freedom / P(k).** Our 2-band model has spin and ridge but
   no explicit top/bottom Mo sublayer. The "L" in RSLC and the electric-field
   controllability are therefore asserted from the paper's symmetry argument
   ({C₂‖S₄z}), not independently computed. A 4-band spin+layer TB model would
   close this.
3. **Relativistic electric Hall effect (χ_xy, Fig. 4).** Requires spin-orbit
   coupling and an Ez-dependent Berry-curvature/Kubo calculation — entirely
   outside the nonrelativistic TB scope.
4. **Absolute conductivity magnitudes.** We report σ in units of e²τ with π₀=1;
   material-specific magnitudes need the DFT velocities and a real τ.
5. **Spin-layer-group enumeration (Table I).** The 8-SLG / 3-candidate
   discovery table was read, not independently re-derived.

## Minor / convention notes
- **Sign of SP.** We obtain (SP_xx, SP_yy) = (+1, −1); the paper text quotes
  (−1, +1). This is purely which orbital/site is labeled "up" in the basis
  {|dxz,↑⟩₂, |dyz,↓⟩₁}; the invariant physics (|SP|=1, opposite full
  polarization on orthogonal axes) matches exactly.
- **Broadening choice.** Fermi window k_BT=0.02π₀; results are insensitive to
  this within the ridge energy window (the ridge contributes a sharp δ-like
  velocity structure that integrates to exactly 0 for the flat direction
  regardless of broadening).

## What WOULD change the verdict
- If a 4-band spin+layer TB model failed to show opposite P(k) under {C₂‖S₄z},
  the "layer" mechanism would be in doubt → downgrade to PARTIAL.
- If DFT placed non-dxz/dyz bands at E_F, the material claim would fail (but the
  general RSLC concept could still stand).
