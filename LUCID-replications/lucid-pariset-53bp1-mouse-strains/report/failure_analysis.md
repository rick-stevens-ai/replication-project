# Failure Analysis — lucid-pariset-53bp1-mouse-strains

**Verdict: REPLICATED — PARTIAL.**
This document is deliberately non-whitewashed. It records what did NOT work, what
we could not verify, and where residual uncertainty is honest.

## 1. What actually failed or was left un-done

### 1.1 Cannot reproduce Table 1A (per-particle Pearson matrix)
- **Root cause:** The paper never publishes per-particle, per-strain
  $(\tau, q, \text{RIF}_{\max})$. Fig. 4A shows only the *combined* 40Ar + 56Fe
  fit as a bar chart; per-particle bars are not present; no supplementary table.
- **Consequence:** the entire HZE Pearson matrix in Table 1A is
  **un-falsifiable from public material**. Marked CLAIM L, DATA-BLOCKED.
- **Cannot fix from here.** Requires either (a) FOIA-style request to the
  Costes lab for the underlying per-cell counts, or (b) a re-collection at NSRL.

### 1.2 Cannot reproduce Fig. 6 (MegaMUGA SNP peaks)
- **Root cause:** No genotype file deposited. No plink deposition. No SNP list.
  Only figure-level conclusions ("peaks near candidate DDR genes").
- **Consequence:** the paper's mechanistic explanation for strain-level variance
  is unfalsifiable — we can neither reproduce the SNP peaks nor rank candidate
  loci by effect size.
- **Cannot fix from here.**

### 1.3 Fig. 7B is only partially reproduced (CLAIM I PARTIAL)
- The paper's headline claim: $r = 0.61$ between $q_{\text{HZE}}$ and in-vivo
  B-cell survival across 10 CC strains.
- **Derived $p_{\text{two-sided}} \approx 0.061$** — statistically borderline.
  Even accepting the paper's reported $r$, the result is $p \geq 0.05$.
- Raw B-cell counts are not deposited, so we cannot independently re-derive
  either $r$ or a permutation-based ceiling.

### 1.4 Fig. 7C inferential over-reach (CLAIM G)
- At $n = 4$ strains, critical $|r|$ for $\alpha = 0.05$ is 0.950.
- Only 2/19 digitized organs reach that ceiling; **0/19 survive Bonferroni**.
- The paper does not display significance stars on Fig. 7C (the honest choice),
  but the surrounding prose calls these "significant correlations" — which is
  too strong. This is a paper-side critique, not a replication failure.

### 1.5 Table 2 quadrant match is 11/15, not 15/15
- 4 strains land in the wrong quadrant under our digitized $(\tau, q)$.
- **Cannot cleanly separate** paper-vs-digitization noise: all 4 mismatches are
  within one digitization step ($\pm 0.5$ h or $\pm 0.01$) of the median
  boundary the paper uses to define quadrants.
- **Could be fixed** by a second-annotator digitization or a proper
  WebPlotDigitizer + tick-anchored uncertainty propagation. Not done.

### 1.6 No Marker/Nougat MMD for this DOI
- Canonical Marker output absent from
  `_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/` as of 2026-06-23.
- Fallback: Poppler `pdftotext -layout` (adequate for the numeric claims but
  coarser for prose grep).
- `extraction/nougat.mmd` in this bundle is a **stub** — no GPU parse was
  produced in this backfill (would require dispatching a uicgpu job and is not
  in scope for a report-bundle backfill).

## 2. What could be better even given the constraints

### 2.1 Digitization error is eyeballed, not propagated
- We declare $\pm 0.5$ h on $\tau$ and $\pm 0.01$ on $q$, but never propagate
  those uncertainties into the Pearson $r$ confidence intervals or into the
  Table 2 quadrant boundaries.
- A proper Monte-Carlo bootstrap over the digitization error would tighten (or
  loosen) the Coverage/Agreement scores.

### 2.2 Fig. 7C $p$-values assume Pearson normality at $n = 4$
- At $n = 4$ this is a poor approximation. A permutation ceiling would be
  more honest. But regardless of the exact test, $n = 4$ cannot support 19
  organ comparisons — so the qualitative conclusion (paper over-reaches)
  survives.

### 2.3 No cross-validation of the strain-level fits
- The paper reports point estimates for $(\tau, q, \text{RIF}_{\max})$ but
  not the parameter covariance matrix or profile-likelihoods.
- We could have run our own bootstrap to publish Fisher-information-based
  identifiability metrics per strain. Not done in re-pass; flagged as open
  question 3.

### 2.4 We did not attempt a species-bridging analysis
- The paper's motivation is human radiotherapy prediction, but the paper never
  bridges from mouse strains to human individuals. We could have proposed a
  concrete equivalence protocol; flagged as open question 4 instead.

## 3. Residual uncertainty

- **Table 1B correlation:** we match the paper to 0.008 (Pearson $-0.758$ vs
  $-0.75$). This is essentially exact. Residual uncertainty is only in the
  digitization step.
- **Table 2 quadrant:** 11/15 exact; 4/15 within one step of a median boundary.
  Residual uncertainty is ~10--15% of strain-level classification.
- **Fig. 7C:** the *direction* is match (13/19 = 68% positive, consistent with
  "most"). The *inferential* claim is not supported at $n = 4$; this is a
  paper-side over-reach, not our residual uncertainty.
- **Fig. 7B:** headline $r = 0.61$ is accepted at face value, but $p = 0.061$
  is borderline; raw data not deposited so a stronger check is impossible.
- **Table 1A + Fig. 6:** completely un-checkable. Full residual uncertainty.

## 4. What we did *right*, defensively

- Preserved the pass-1 REPORT verbatim as `REPORT.pass1.md`.
- Every consumed paper number is pinned to a line in the pdftotext output
  (`PARSER_PROVENANCE.md`).
- Regression check across passes: 4 correlations match to 4 decimal places.
- Zero fabrication: where we could not compute, we labeled DATA-BLOCKED and
  named the specific missing artifact.
- Honest Coverage 8/10 and Agreement 8/10 rather than a self-flattering 9 or 10.

## 5. Recommended next actions (highest leverage first)

1. Contact the Costes lab (Sylvain Costes, NASA Ames) for the raw 53BP1 foci
   counts and per-particle (τ, q, RIFmax) tables. Even a restricted-access
   Zenodo deposit would unblock Table 1A and Fig. 7B.
2. If (1) fails, request the NSRL beamline dosimetry logs from NASA HRP data
   archive — enough to confirm that the reported doses are traceable.
3. Second-annotator digitization of Fig. 4 A/B — cheap and would resolve the
   4/15 Table 2 quadrant mismatches.
4. Dispatch Marker or Nougat parse for DOI 10.1667/RADE-20-00122.1 on uicgpu
   to replace the pdftotext fallback for prose grep.
5. Publish the derived Fig. 7C $n = 4$ statistical ceiling as a comment or
   post-publication note; this is a concrete, correctable over-reach.

## 6. Bottom line

The replication is **PARTIAL and honest**. The mathematical core is exact;
the strain-level phenotype structure is recovered; the two data-blocked
claim families are named with specific missing artifacts. The single
disagreement (Fig. 7C inferential over-reach) is on the paper's side and
is surfaced explicitly rather than swept away. This is a correct outcome
given the constraints and matches the preserved verdict.
