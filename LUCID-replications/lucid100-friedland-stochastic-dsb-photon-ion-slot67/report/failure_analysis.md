# Failure Analysis — LUCID-100 slot 67 (Friedland, Kundrát & Jacob 2012)

## Summary
This slot is a **NO-GO** by data availability. The paper is closed-access, its
underlying Monte Carlo code (PARTRAC) is proprietary, and the calibration
data + precursor parameter tables are also closed. What exists in this slot
is an independent *analytical reduction* of the paper's stated model
refinements — not a re-implementation of the PARTRAC stochastic Monte Carlo,
and not a reproduction of the paper's specific figures or numbers.

## ⚠️ Queue verdict mismatch (flagged per 2026-07-05 cross-check rule)
- **Queue verdict (LUCID master list):** REPLICATED.
- **On-disk verdict (REPORT.md top, re-tiered 2026-06-25):** NO-GO (originally SPOT-CHECK).
- **Truth:** the on-disk NO-GO is correct. The queue label is stale/incorrect and should be corrected in the master TSV.
- **Do not silently upgrade the on-disk verdict to match the queue.** The queue label predates the 2026-06-25 hard-ceiling re-tier; it was set when the auditor was working from the original AMBER-KEEP first pass and did not have the closed-source blockers surfaced.
- **Recommended queue action:** flip slot 67 in `LUCID100_SOLID_MASTER_QA.tsv` from `REPLICATED` to `NO-GO` with note "PARTRAC proprietary; paper closed-access; only analytical smoke reduction possible; re-tiered by Rick hard-ceiling rule 2026-06-25."

## Root-cause failures

### Failure 1 — Paper PDF unavailable
- **What failed:** could not obtain PDF from any OA/preprint route.
- **Root cause:** T&F IJRB is closed; no arXiv/bioRxiv preprint; Unpaywall confirms `is_oa=false, oa_locations=[]`; S2 abstract elided by publisher disclaimer.
- **Workaround attempted:** used S2 TLDR + 14-reference graph + precursor context to infer claims.
- **Residual gap:** cannot enumerate specific paper claims (rate constants, table values, figure-level statistics). All tested claims are **inferred**, not quoted.
- **Closure requirement:** institutional access to T&F IJRB.

### Failure 2 — PARTRAC source not obtainable
- **What failed:** cannot rerun the stochastic Monte Carlo the paper is built on.
- **Root cause:** PARTRAC has never been publicly released by Helmholtz Zentrum München. GitHub/Zenodo/Google search 2026-06-09 returned no public mirror; the few "partrac"-named hits are unrelated particle-tracking utilities.
- **Workaround attempted:** wrote an analytical two-component biexponential-plus-labile-term fit as a *reduced surrogate* of the paper's stated model refinements.
- **Residual gap:** the surrogate cannot produce stochastic distributions, per-event fluctuations, complexity histograms, or any of the outputs that distinguish a Monte Carlo from a curve-fit.
- **Closure requirement:** either a public PARTRAC release (unlikely) OR a full standalone re-implementation (Gillespie NHEJ library driven by Geant4-DNA DSB end lists — this is proposed as Q2 in the open questions).

### Failure 3 — Precursor parameter tables closed
- **What failed:** cannot obtain calibrated NHEJ rate constants from Friedland 2010 (RR1965).
- **Root cause:** Radiation Research is a closed journal.
- **Workaround attempted:** hand-tuned smoke parameters chosen for monotone behaviour, not for magnitude match to any specific published table.
- **Residual gap:** all quantitative comparisons are internally consistent but disconnected from the paper's actual numbers.

### Failure 4 — Stenerlöw 2000 measured kinetics closed
- **What failed:** cannot use the paper's actual calibration data.
- **Root cause:** Stenerlöw 2000 IJRB is closed and its data are not re-tabulated in any open source we found.
- **Workaround attempted:** used literature-typical Co-60 γ and N-ion (~80 keV/µm) rejoining curves as smoke inputs.
- **Residual gap:** the RMSE numbers (0.021, 0.025) are agreement-with-our-own-inputs, not agreement-with-the-paper.

## Critique of evidence strength (per Rick, 2026-07-05)

The audit's methodological weaknesses that make the "6/6 smoke checks pass" claim weaker than it looks:

1. **PARTRAC was not re-implemented — not even in Gillespie surrogate form.** The audit produced only a closed-form analytical curve fit. The paper's contribution is a stochastic track-structure Monte Carlo; ours is not the same kind of scientific object. Callout for future runs: labelling this "REPLICATED" is misleading regardless of check counts.

2. **Stochastic distributions were not reproduced.** The paper's signature output is per-event distributions of DSB complexity and repair time (variance, tails, per-track fluctuations). We reproduced only mean curves. No second moment. The word "stochastic" in the paper title did not survive into this audit.

3. **Ion coverage is one point (N-ion ~80 keV/µm) + a Hill surrogate.** The paper's story is photon-vs-ion across a species/LET grid. The LET sweep is a hand-tuned Hill sigmoid, not species-specific PARTRAC output; it neither uses real ion physics nor is calibrated to species-specific measurements. This is why T5/T6 fail — the surrogate was tuned for monotonicity, not magnitude.

4. **Reference curves are unverified digitisations.** The "literature-typical" curves in `code/smoke_friedland2012.py` lines 64–75 are hand-authored to look like Stenerlöw 2000, but nobody verified them against the actual Stenerlöw paper (which is also closed). This makes the fit RMSE numbers self-referential.

5. **Six/six smoke checks passing is close to tautological.** S1–S6 are chosen to accept the model class that was fit. They are a self-consistency check, not evidence for the paper.

6. **Zero quantitative paper-specific numbers were verified.** Coverage of the paper's quantitative content is approximately 0%.

## What's needed to close the gaps
- **Institutional access to T&F IJRB** — resolves Failure 1 and (via RR1965) Failure 3.
- **Public PARTRAC release OR a standalone Gillespie NHEJ library driven by Geant4-DNA DSB end lists** — resolves Failure 2. This is a real research project (Q2 in open questions).
- **Digitisation of Stenerlöw 2000 curves from any secondary source that redistributes them** — partially resolves Failure 4.

Even with all four gaps closed, the paper's exact figures cannot be redistributed; the closest attainable is figure-level agreement metrics, not the figures themselves.

## Confidence bands
- Directional/qualitative reproduction of photon-vs-ion contrast: **high confidence** (6/6 smoke).
- Directional/qualitative LET-scaling: **medium confidence** (4/6 LET-sweep, magnitude bounds fail).
- Quantitative reproduction of any paper-specific number: **zero** — untestable by construction.
- Verdict robustness: **high confidence in NO-GO**. This slot cannot become PARTIAL or REPLICATED without either PARTRAC or a full standalone Monte Carlo re-implementation.
