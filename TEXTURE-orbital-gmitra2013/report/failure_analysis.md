# Failure Analysis — TEXTURE-orbital-gmitra2013

## Scope limitation (primary, by design — not a code failure)
The paper's numbers come from relativistic (SOC) FLAPW DFT (FLEUR) on Fe/GaAs
slabs with fine k-meshes — DFT-heavy, requiring cluster dispatch. That step was
**deliberately not attempted in-process**; it cannot be run tractably here.
Consequence: we do **not** independently reproduce the Table I coefficients or
the raw band structure. We take the paper's extracted Table I as ab-initio
ground truth and verify the symmetry model + downstream physics built on it.
This is marked throughout (REPORT, workflow, artifacts_summary) and is the
reason Agreement is capped at 9/10 rather than 10.

## Tooling failures encountered
- `pdf` tool: rejected `paper.pdf` — "Local media path is not under an allowed
  directory" (Dropbox is outside the media sandbox). **Workaround:** used the
  pre-extracted `extraction/marker.md` (pdftotext) directly. No loss of equation
  content; Eqs. 1-12 and Table I were all recoverable from the text dump.
- `image` tool: same path restriction; could not visually QA the generated PNGs.
  **Workaround:** validated figures indirectly via the numeric metrics that the
  figures depict (e.g. alpha_1 zero-crossing, anisotropy max/min ratio), so the
  plotted quantities are confirmed even without pixel inspection.

## Modeling caveats / possible weaknesses
1. **Toy dispersion for the extraction round-trip.** C1 uses a constructed band
   `E = c*k^2 + w(k).m_hat`. This makes the round-trip exact by construction,
   which validates that Eqs.(4-9) are transcribed correctly but does **not**
   test robustness against real DFT features (anticrossings, non-parabolicity).
   The paper itself warns the method fails near energy anticrossings; we did not
   stress-test that regime.
2. **Linear-in-k SOF only.** The butterfly figures use the linear
   (alpha,beta) terms. The paper's most exotic large-k butterflies (Fig. 2c)
   involve the k^2 coefficients (Eq. 2), whose theta-dependence is not in
   Table I; our large-contour textures therefore capture the anisotropy trend
   and axis flip but not the full higher-order node structure. (Logged as
   open question #1.)
3. **theta=0, pi/2 singularities avoided.** The extraction round-trip test
   skips the crystallographic axes where Eqs. 4-5 need L'Hopital's rule; the
   limit was not implemented (open question #3).

## No fabrication
All numbers in `results/metrics.json` are produced by executing
`code/run_analysis.py`. No results were hand-authored. Out-of-scope items are
labeled as such rather than faked.

## Lessons for future replications in this series
- Dropbox-resident papers must be read via the pre-extracted marker text; the
  `pdf`/`image` media tools are sandboxed out. Budget for text-only extraction.
- For DFT-heavy papers with an analytic symmetry backbone, replicating the
  backbone against the paper's own extracted tables is the highest-value
  tractable target and should be the default when cluster DFT is unavailable.
