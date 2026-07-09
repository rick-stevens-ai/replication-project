# Failure Analysis — PARTRAC Analytical Formulas Replication

## Scope
This document is a candid post-mortem of what the replication tried, what worked,
what did not work, and what would be required to close the remaining gaps.

## What worked

1. **Formula transcription.** Equations 1 and 2 in the paper are printed cleanly
   and unambiguously. Encoding them in Python was straightforward, and the
   `N.A.` term-dropping convention is described in the paper text itself.

2. **Parameter transcription.** Tables 1–2 are legible and directly typeable.
   No OCR uncertainty, no hidden footnotes affecting the numeric values used.

3. **Low-LET headline check.** Because Eq. 1 and Eq. 2 both reduce to `p1` at
   LET → 0 for the relevant terms, the paper's prose baselines (SB≈170,
   SSB≈156, DSB≈6.8–7 Gy⁻¹ Gbp⁻¹) fall directly out of the transcribed
   `p1` values. This is a real but shallow confirmation — it verifies
   transcription, not physics.

4. **Qualitative curve shapes.** The regenerated fit-line curves show the
   expected shapes for SB (weak decrease), SSB (weak decrease), DSB (increase
   with LET, roll-over where overkill parameters are present), DSB clusters
   (super-linear increase) and DSB sites (RBE-like peak for heavy ions).
   These match the paper's Figs. 1–4 fit-line shapes by eye.

## What did NOT work / what is missing

### 1. Independent validation against PARTRAC is impossible here
- PARTRAC is closed in-house GSF/HMGU code with no public release.
- The raw simulation points behind Figs. 1–5 (the symbols the fits describe)
  are not in the paper, the supplement, or any companion deposit accessible
  to us.
- The paper's central quantitative claim ("<2% RMS deviation from PARTRAC,
  DSB clusters up to ~9%") is therefore **untestable in this environment**.
- Impact: verdict cannot be upgraded above PARTIAL on validation grounds alone.

### 2. Independent re-derivation of coefficients was not attempted
- Would require running a public track-structure MC (Geant4-DNA Opt2 or
  TOPAS-nBio) at matched LET/ion combinations with a matched chromatin geometry.
- Deferred to open-question Q1; not in this replication pass.

### 3. H-proton DSB-site domain issue
- **Observation.** Table 1's H-proton DSB-site row has `N.A.` in both p4 and p5
  (the overkill-denominator parameters). Following the paper's stated convention,
  the denominator term is dropped, leaving `Y = p1 + (p2·LET)^p3`. This grows
  without bound as LET increases.
- **Tension with paper prose.** The paper states that DSB-site effectiveness
  peaks around ~15 sites/Gy/Gbp at 100–200 keV/µm. Naive extrapolation of the
  transcribed H-proton formula past that region violates this.
- **Not silently patched.** We could have inserted a plausible overkill divisor
  or clamped the domain to the fitted LET range, but either choice would be a
  scientific decision requiring a citation. Instead we logged the anomaly in
  the audit table (claim #8, PARTIAL/caution) and open-question Q2.
- **Possible causes.** (a) The published Table 1 has an omission or typo;
  (b) the H-proton row is intentionally domain-restricted and readers are
  expected to know not to extrapolate past the fitted range; (c) Kundrát's
  fitting protocol drops the overkill term when the fitted LET range is
  entirely below the overkill knee. Determining which of these is correct
  would require contacting the authors or accessing the fitting code.

### 4. No new physics probes
- We did not extend to heavy ions past Ne, low-energy secondary electrons,
  FLASH dose rates, or alternative chromatin geometries. All four are listed
  as open questions (Q2–Q4) with concrete free-endpoint next steps.

### 5. DOI mismatch (task metadata bug, not a replication failure)
- Task DOI `10.3390/cancers11020205` points to a different *Cancers* review,
  not the Kundrát 2020 *Sci Rep* analytical-formulas paper actually cached
  as source. We proceeded with the on-disk source and logged this as F8.
- Not actionable inside this replication; a queue-metadata correction is
  recommended upstream.

## Lessons for future analytical-formula replications

1. **Coefficient tables with `N.A.` denominator entries are a red flag.**
   Always evaluate the resulting formula across the full published LET range
   AND a plausible extrapolation buffer, and check for unbounded growth or
   sign flips before declaring the transcription correct.

2. **Fit-line replication ≠ MC replication.** For any paper whose headline
   claim is "our fits match the underlying MC to X%", access to the underlying
   MC points is a hard prerequisite for full replication. Absent those points,
   the honest verdict cap is PARTIAL.

3. **Task DOI ≠ on-disk source.** Always identity-check the cached source
   before starting; the paper you replicate is the paper you actually have,
   not the paper the queue thinks you have.

## Verdict impact
The queue's PARTIAL verdict is preserved. A defensible case exists for
UPGRADE-to-REPLICATED on the narrow reading "can the analytical surrogate
be re-evaluated end-to-end?", but the validation-against-MC hole plus the
H-proton domain anomaly together justify staying at PARTIAL for this pass.
