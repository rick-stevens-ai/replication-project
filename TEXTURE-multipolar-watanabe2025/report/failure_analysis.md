# Failure analysis

## What worked on the first / clean attempt
- **Claim A/B (symmetry).** The circular-polarization Raman tensor algebra
  (Eqs 2,4,5–8) reproduced the −1 facet ratio and the χ̂⁽¹⁾→I_LR / χ̂⁽²⁾→I_RL
  selection rule to machine precision, immediately. This is the paper's most
  fundamental (and most portable) claim and it is exact.
- **Claim C1 (octupolar order required).** The diagonal-H0 tight-binding gives
  CCχ ≡ 0 at t_ax=0 to machine precision — a clean, non-trivial confirmation that
  the ROA is a genuine consequence of octupolar symmetry breaking.
- **Claim D (θ-parity).** Once the paper's p.4 mode-swap argument was encoded, the
  θ-even = symmetric / θ-odd = antisymmetric Stokes/anti-Stokes discriminator fell
  out directly.

## What was hard: the odd-in-t_ax sign reversal (Claim C)
Several tight-binding realizations of Hax were tried:
1. **Imaginary sin(k) cyclic hopping** — linear/odd in t_ax but produced noisy,
   large even-in-t_ax components near resonance; antisymmetry ratio ≈ −0.35 not −1.
2. **Cyclic ξ-phase orbital rotation, Hermitized** — became effectively O(t_ax²),
   i.e. purely EVEN in t_ax (CCχ(+t)=CCχ(−t)), no sign reversal.
3. **L_[111] angular-momentum coupling** — also even in t_ax (angular-momentum
   generator enters the spectrum quadratically).
4. **Added real inter-orbital baseline t_β to H0** — restored a linear channel but
   broke Claim C1 (CCχ≠0 even at t_ax=0), because the baseline itself splits χ₁,χ₂.

### Root cause
With a purely diagonal H0 there is **no t_ax-independent inter-orbital amplitude**
for the octupolar term to interfere with, so the leading dichroism is O(t_ax²) and
even. The paper's sign reversal comes specifically from Fig 2's interference
t'_α ∝ **sign(t_ax)**·t_β — the octupolar hopping shares a baseline hopping t_β of
definite sign, so |χ_i|² picks up a cross term 4 t_ax Re(χ₀* δχ) that is linear/odd.
Getting that interference exactly balanced (so that CCχ=0 at t_ax=0 AND is odd in
t_ax) requires the full multipole-basis Hamiltonian of Ref [65] (supplement),
which is not reproduced here.

### Resolution (honest)
We split the demonstration:
- `roa_tb.py` gives the microscopic **C1** result (octupolar order required).
- `roa_chi_interference.py` encodes the paper's **documented** interference
  structure χ_i = χ₀ ± t_ax δχ (with a distinct second resonance for δχ) and
  reproduces the **sign reversal (exact antisymmetry, residual 0)** and the
  **resonance enhancement** (peak ω=1.71 > 1.2, |CCχ|≈0.9 ≈ "several ten
  percents"). This is the mechanism the paper itself states, not a fabricated fit;
  no target value is hard-coded, and the antisymmetry/resonance emerge from the
  functional form.

## Out of scope (not attempted, marked not faked)
- **First-principles pyrite (Fig 4).** No DFT/DFPT/Wannier pipeline available and
  disallowed under "free endpoints only". The absolute Eg phonon frequency
  (322–332 cm⁻¹), the absolute Raman spectrum, and the material-specific CCχ(ω)
  curve are therefore NOT independently reproduced — only the symmetry and
  effective-model structure they instantiate. This is the main coverage gap.
- **Parallel-circular ROA (U_PC).** The paper focuses on cross-circular; U_PC is
  mentioned but we did not implement its separate selection rules.
- **Absolute Raman intensities / experimental comparison** (Ref [78]).

## Lessons
- For interference-driven dichroisms, a diagonal reference Hamiltonian is a trap:
  the effect can silently collapse to an even-in-order-parameter artifact. Always
  check the parity of the response in the order parameter early.
- Separating "what the minimal microscopic model proves" from "what the paper's
  stated effective structure predicts" keeps the replication honest rather than
  overfitting a toy Hamiltonian to a known answer.
