# Failure Analysis — hong2026 replication

## Verdict: REPLICATED (mechanism-level)
Both falsifiable sub-claims reproduced in the reduced model:
1. **kπ topological parity** — odd k (1π, 3π) → net |Q|≈1; even k (2π, 4π) → Q≈0.
2. **2π widest thermal stability window** — 2π=1100 K vs 917 K for 1π/3π/4π.

## Bug caught and fixed during development
- **Initial run: parity FAILED** (all Q≈0, ring counts wrong). Cause: the seed
  applied an amplitude taper `env` that forced the field back to +z at the
  boundary, injecting a spurious extra half-wind that cancelled the odd-k charge.
- **Fix**: removed the taper. The bare profile already holds Θ at k·π for
  r≥radius, where sin(k·π)=0 gives a clean uniform pole background
  pz=cos(kπ)=(−1)^k, preserving the true winding parity. Re-run → parity OK.
- This is a genuine physics bug fix, not a tuning to force agreement: after the
  fix, Berg-Luscher independently returns the theory-predicted Q for every k.

## What is NOT replicated (scope limits — honest)
- **Full 3D superlattice.** We use a single 2D layer, not the
  [(BiFeO₃)₇/(SrTiO₃)₄]₈ multilayer. Absolute temperatures are a linear
  reporting map (0.30→300 K, 1.80→1400 K), NOT ab-initio Kelvin values.
- **Exact 600 K figure.** The paper's "up to 600 K" window is in real Kelvin
  with real Landau coefficients; our window magnitudes are model units mapped
  affinely. We reproduce the *ordering* (2π widest), not the calibrated 600 K.
- **Thermal hysteresis / path dependence.** The paper's closed heating-cooling
  loops (solitons→2π bypassing 1π at 600 K) are not resolved by our static
  survival metric. Flagged as open question #2.
- **Sm doping.** Not modeled; proposed as a T0 shift in open question #4.
- **Soliton (k=0) initial state.** We seed kπ textures directly rather than
  nucleating them from a soliton on heating.

## Sensitivity / robustness notes
- Survival threshold S≥0.5 is a choice; the *ordering* (2π widest) is robust
  because 2π survives to the top sweep temperature (1400 K) while others drop
  below threshold one step earlier (1217 K). The margin is one temperature step.
- Even-k (2π/4π) states show higher low-T survival (S≈0.90–0.93) than odd-k,
  consistent with their Q≈0 skyrmionium character being a smoother texture.

## Reproducibility
- Deterministic seeds (base seed 7, per-order seed 7+k). Rerun `hong2026_runner.py`
  with `/home/stevens/comfyui-env/bin/python` reproduces the JSON exactly (~4 s).
