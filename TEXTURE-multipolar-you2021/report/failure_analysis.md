# Failure Analysis — You et al. 2021 replication

## What was reproduced (successfully)
- The **symmetry-defined theory core**: the antidamping σz torque
  τ_C = m×(m×σz) produces deterministic field-free switching of a PMA magnet,
  with polarity set by current sign, and no such switching when σz is absent (only σy).
- Structural match to the paper's key control (J‖T [001] switches; J⊥T [110] does not).
- Existence of a finite threshold current for deterministic switching.

## What was NOT reproduced (and why)
1. **Absolute critical current density (~9×10⁶ A/cm²).** The macrospin runs in
   reduced units; the SOT amplitude was scaled by an arbitrary factor C using only the
   FL/AD *ratio*. Mapping C→A/cm² requires SI parameterization (Ms, Hk, thickness,
   spin-torque efficiency) not fully specified in the text. → left as open question #1.
2. **ST-FMR angular dependence / VS,VA fitting.** Requires the measured spectra and
   AMR calibration; purely experimental. Not attempted.
3. **Materials growth, XRD/Φ-scan, SQUID, AHE, MOKE imaging.** Physical-sample
   measurements; intrinsically non-reproducible computationally.
4. **~60% partial switched volume.** A macrospin cannot capture partial/domain
   switching; this is a multidomain (micromagnetic) effect. → open question #5.
5. **σz microscopic origin (H_so × T, carrier-spin precession).** We *assume* σz
   as an input polarization rather than deriving it from a band/scattering model of
   Mn3SnN's Γ4g texture. The Landau/octupole kernels available were not needed for
   the switching claim and would be the route to derive σz magnitude ab initio.

## Assumptions / caveats
- Single-macrospin, coherent rotation, T=0 (no thermal noise). Determinism under
  Langevin noise at 300 K is untested (open question #4).
- Case A polarization set to p≈ẑ with a small σy admixture; Case B to pure σy. This
  encodes the binary symmetry rule rather than a continuous J–T angle dependence.
- FL/AD ratio taken from paper; individual absolute values used only via scaling C.

## Risk of false positive
Low for the qualitative claim: the dichotomy (switch iff σz present) is robust across the
current-strength sweep (C_crit≈12, deterministic for all C≥12 tested up to 40). The
result is a direct, expected consequence of the LL antidamping term and does not
over-claim quantitative agreement.
