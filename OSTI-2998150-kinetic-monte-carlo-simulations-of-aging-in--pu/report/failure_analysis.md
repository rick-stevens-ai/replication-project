# Failure Analysis — OSTI-2998150

**Paper:** Oppelstrup et al. (2025) — *Kinetic Monte Carlo simulations of aging in δ-Pu*
**Verdict:** REPLICATED (spot-check)
**Date:** 2026-07-03

---

## Summary

The replication succeeded on its scoped target (paper Eq. 5 spot-check), but
the path was not straight. This document catalogues the failures, near-misses,
and unresolved gaps.

---

## Failure 1 — Pre-existing helper script was silently wrong

**Symptom:** Running `work/vac_void_collision.py` produced a fit
`DRρτ ≈ 16.4 − 45.8·(R/L)` — off by a factor of ~200 in the intercept,
completely incompatible with the paper's Eq. 5 (0.078) and the analytical
`1/(4π) ≈ 0.07958`.

**Root cause:** The helper computed absorber density as `rho = N/L³`
(walker density) instead of the correct `rho = 1/L³` (density of the
single absorbing sphere). Since `DRρτ` scales linearly with ρ, the result
was inflated by exactly N = 200.

**How diagnosed:** Compared the shape of the buggy fit against the paper's
Eq. 5 and the analytical limit; the factor-of-200 offset matched N
exactly. Grep of the helper source found the offending line.

**Fix:** Wrote `report/evidence/vac_void_collision_fixed.py` with
`rho = 1.0 / L**3`.

**Lesson:** A workspace "utility" script inherited from an earlier task is
not automatically trustworthy. Any pre-existing analysis script must be
audited against a known-good reference (in this case, the analytical
`1/(4π)` intercept) before its output is used. The buggy artifacts
(`kmc_results.json`, `kmc_run.log`) were **preserved, not deleted**, so
the diagnosis trail is visible to future auditors.

**Preventable next time?** Yes — a 5-second sanity check ("does the
intercept match 1/(4π)?") would have flagged this immediately. Adopted
as a standing rule: any Monte Carlo replication with a closed-form limit
must sanity-check against that limit before proceeding.

---

## Failure 2 — Full FPKMC aging simulation NOT REPLICATED (scope failure)

**Symptom:** Claims C3, C4-partial, C5 could not be tested.

**Root cause:** Two independent gates:
1. LLNL's in-house FPKMC code (Bertin et al. code base) is not
   publicly distributed. The paper cites Refs. 6–7 (Oppelstrup 2006 PRL,
   2009 PRE) which describe the FPKMC algorithm mathematically but
   distribute no reference implementation.
2. δ-Pu-specific vacancy formation/migration/binding energies, He
   absorption parameters, and dislocation network parameters are only
   partially given in the paper (Eqs. 1–4 + scattered constants);
   full tables live in unpublished LLNL internal databases.

**How diagnosed:** Read the paper end-to-end; searched for "code available",
"data available", supplementary materials. Confirmed no such artifacts.

**Fix:** None possible within scope. **Documented explicitly** in
REPORT.md §5 ("What was NOT replicated and why") — this is a scope
boundary, not a bug in the paper or in this replication.

**Lesson:** Field-level reproducibility gap in FPKMC-for-actinides.
Independent verification of century-scale aging predictions requires
either (a) the LLNL code, (b) a from-scratch multi-KLoC reimplementation
of FPKMC + Pu defect energetics (multi-month effort), or (c) a data-sharing
agreement with LLNL. Flagged in `open_questions.json` OQ4 (cascade
library) as a related aspect of the same field-level gap.

**Preventable next time?** Not by us — this is a paper/field property.
The right response is what we did: pick a testable spot-check (Eq. 5)
and be honest about the boundary.

---

## Failure 3 — Slope off by ~24% from paper

**Symptom:** Our fitted slope is −0.235 vs. the paper's −0.19. Correct
sign, right order of magnitude, but not tight agreement.

**Root cause candidates (not yet distinguished):**
1. **Small event budget.** 300 events per (L,R) cell is low for a slope
   estimate on 8 data points; the paper presumably used a larger sweep
   (Fig. 8 shows a denser grid). Monte Carlo noise on individual τ
   measurements propagates directly into the fit slope.
2. **Sparse (L,R) grid.** 8 cells (2 L values × 4 R values) constrains
   the slope less than the paper's finer grid would.
3. **Genuinely different physics?** Cannot rule out that our
   segment-crossing implementation differs subtly from the paper's
   first-passage exit-time computation. This is the least likely
   explanation given the intercept agreement.

**How diagnosed:** Partial — we verified the intercept lands on
`1/(4π)`, so at least the R/L → 0 limit is right. Slope discrepancy is
noted but not driven to closure.

**Fix (partial):** Documented as an honest limitation in REPORT.md §4.3
and REPORT.tex GENUINE CRITIQUE §2.2. Not claimed as agreement.

**Lesson:** For a slope estimate, a rule of thumb is ≥10× more events
than we ran. Reserved as OQ1 in `open_questions.json` — a
sample-size scaling study would settle whether −0.19 and −0.235 are
statistically distinguishable.

**Preventable next time?** Yes — budget more events per cell for slope
work. Trade-off is wall time (our 70 s → probably ~700–7000 s at
higher event counts, still tractable).

---

## Failure 4 — Marker/extraction sidecar absent

**Symptom:** `extraction/marker.md` referenced in the task instructions
does not exist for this replication.

**Root cause:** This replication used direct PDF text extraction
(`work/osti-2998150.txt`, 848 lines) rather than the marker/nougat
pipeline; the marker sidecar was never generated for OSTI-2998150.

**How diagnosed:** Read attempt returned ENOENT.

**Fix:** Task instructions permitted skipping missing files — proceeded
with REPORT.md as the sole authoritative source.

**Lesson:** Not every OSTI replication in the wave has the same
extraction sidecars. Verify presence before writing dependencies on them.

**Preventable next time?** Wave-level: standardize the extraction
pipeline so every replicated paper has a marker.md. Individual-task
level: nothing to fix — behaved correctly by no-oping on the missing
file.

---

## What Did NOT Fail (worth noting)

- **Segment-vs-sphere collision test.** Passed edge-case hand-checks
  on the first try. The naive "endpoint inside sphere?" test would
  have missed fast walkers that tunnel through the absorber and biased
  τ upward — we anticipated this and used the correct segment-based
  test from the start.
- **Steady-state exterior density.** Uniform respawn outside the sphere
  is the correct boundary condition; got it right first pass.
- **Deterministic reproducibility.** Seed `1234 + int(1000·(L+R))`
  makes every run byte-identical. Verified.
- **Analytical `1/(4π)` intercept.** Immediately recognized as the
  correct sanity-check target — this is the textbook steady-state
  diffusion result and is what caught Failure 1.

---

## Recurring Lesson

Every replication task should start with: *"What is the closed-form
limit or textbook sanity-check I can verify before trusting anything
else?"* In this case, `1/(4π)`. Once we knew what the right intercept
should be, the pre-existing helper's wrongness was visible in seconds.
Skipping that step would have propagated the ρ = N/L³ bug into the
verdict.
