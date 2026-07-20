# Failure Analysis — lee2025 replication

## Verdict: REPLICATED (7/7 checks)

No blocking failures. Notes on scope, approximations, and limitations:

## Deliberately out of scope (not attempted)
- **DFT-GGA MnF2 calculation (Fig 5).** Skipped per task instructions (no DFT).
  The paper's ab-initio validation of the minimal model is therefore *assumed*,
  not reproduced. Our replication covers the analytic minimal-model claims only.
- **Absolute eV-scale splitting for real MnF2.** The paper quotes ~eV splitting
  from h_eff ~ few eV; we work in units of t1 and do not fit real material
  parameters. Our numbers (e.g. ΔE=1.109 t1 at (π/2,π/2)) are model-unit values,
  not calibrated to MnF2.

## Approximations / simplifications
- Single-orbital minimal model (as in the paper's Eq 1). The multi-orbital
  (X2-Y2 / Z2) structure of Fig 5 is not built; the paper itself presents it as
  an extension.
- SOC-free throughout. Spin is a good quantum number, so we diagonalize the 4x4
  directly instead of invoking the full Kubo-Bastin routine. Weyl/AHE topology
  (intro references [2-4,6,17,18]) is consequently not tested — moved to open
  questions.
- Fig 4(d) is reproduced via the analytic Eq (3), cross-checked against the
  independent numeric diagonalization (agreement to 1e-15), so the analytic
  short-cut introduces no error.

## Potential subtleties handled
- **"Both required" claim wording.** Naively, turning on h_eff alone opens a
  spin gap (2*h_eff) everywhere, which could be mis-scored as "splitting without
  δt." We distinguish the *momentum-dependent / anisotropic* splitting (the
  actual altermagnetic signature) from a trivial uniform AFM gap by measuring
  max-min of ΔE over the BZ. That anisotropy is nonzero only when both terms are
  on — the physically correct interpretation of the paper's statement that the
  splitting "is related to 2 t_{k,z} h_eff ... nonzero only when both h_eff and
  δt are nonzero."

## Extraction caveat
- Marker/nougat OCR unavailable in this environment; `extraction/marker.md` and
  `extraction/nougat.mmd` are `pdftotext -layout` interim outputs with proper
  headers, not true Marker/nougat renders. Equation typesetting is degraded but
  the model equations were transcribed correctly into the code from the source
  text.

## Reproducibility
- Deterministic (fixed RNG seed 0 for the k-sampling verification). Runtime
  ≈0.08 s on comfyui-env python. Re-run: `comfyui-env/bin/python
  work/lee2025_replicate.py`.
